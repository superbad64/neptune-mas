import json
import os
import requests
import re
import random
import time

class ComfyDispatcher:
	def __init__(self, target_host="10.0.0.64", target_port=8189):
		self.server_address = f"{target_host}:{target_port}"
		self.client_id = "neptune_body_agent"
		self.last_saved_filename = None

	def format_ksampler_workflow(self, workflow_template: dict, prompt_tokens: dict) -> dict:
		"""
		Forces an Empty Latent configuration onto Node 4 to establish 
		a clean, uncorrupted character baseline pass.
		"""
		graph = json.loads(json.dumps(workflow_template))
		
		# 1. Inject Dynamic Positional Layout Tokens into PrimitiveString (Node 16)
		if "16" in graph and graph["16"].get("class_type") == "PrimitiveString":
			raw_positive = prompt_tokens["positive_tokens"]
			cache_buster = f"breakcache_{int(time.time() * 1000)}"
			graph["16"]["inputs"]["value"] = f"{raw_positive}, {cache_buster}"
				
		# Safe Seed Randomization (Node 4)
		if "4" in graph and graph["4"].get("class_type") == "KSampler":
			graph["4"]["inputs"]["seed"] = random.randint(0, 1125899906842624)
			
			# Dynamic Graph Mutation: Disconnect Node 19 (VAEEncode) from KSampler's latent_image input slot
			# Connect a fresh EmptyLatentImage structure definition on port 4 to generate a clean canvas
			if "20" not in graph:
				graph["20"] = {
					"inputs": {
						"width": 832,
						"height": 832,
						"batch_size": 1
					},
					"class_type": "EmptyLatentImage",
					"_meta": {
						"title": "Empty Latent Canvas"
					}
				}
			# Link KSampler input index 3 [latent_image] natively to our new Empty Latent Node 20
			graph["4"]["inputs"]["latent_image"] = ["20", 0]

		# 3. Force terminal output execution registration on Node 9
		if "9" in graph:
			graph["9"]["inputs"]["filename_prefix"] = f"Neptune_{int(time.time())}"
			graph["9"]["is_output"] = True
				
		return graph
	def dispatch_to_wsl(self, target_graph: dict) -> str:
		"""Sends execution tokens to the ComfyUI API endpoint."""
		payload = {"prompt": target_graph, "client_id": self.client_id}
		try:
			url = f"http://{self.server_address}/prompt"
			response = requests.post(url, json=payload, timeout=15)
			response.raise_for_status()
			return response.json().get("prompt_id")
		except requests.exceptions.RequestException as e:
			print(f"[Core Error] Remote asset generation pipeline unreachable on WSL node: {e}")
			return None

	def cache_backchannel_variant(self, local_image_path: str, filename_string: str) -> bool:
		"""Streams variants straight into ComfyUI's remote input cache via the upload API."""
		sanitized_filename = re.sub(r"[^\w\-_.]", "_", filename_string)
		url = f"http://{self.server_address}/upload/image"
		
		if not os.path.exists(local_image_path):
			return False
		try:
			with open(local_image_path, "rb") as f:
				files = {"image": (sanitized_filename, f, "image/png")}
				data = {"overwrite": "true"}
				res = requests.post(url, files=files, data=data, timeout=20)
				if res.status_code == 200:
					self.last_saved_filename = sanitized_filename
					return True
				return False
		except Exception as e:
			print(f"[Sync Error] Back-channel cache injection dropped: {e}")
			return False

	def execute_render_pipeline(self, compiler_output: dict, template_path: str) -> dict:
		"""Connects our PipelineCompiler results directly to active ComfyUI worker loops."""
		if not os.path.exists(template_path):
			return {"status": "failed", "reason": "Workflow blueprint file missing"}
			
		with open(template_path, "r", encoding="utf-8") as f:
			workflow_raw = json.load(f)

		ready_graph = self.format_ksampler_workflow(workflow_raw, compiler_output)
		prompt_id = self.dispatch_to_wsl(ready_graph)
		
		if not prompt_id:
			return {"status": "failed", "reason": "WSL server rejected execution block"}
			
		return {
			"status": "queued",
			"prompt_id": prompt_id,
			"assigned_location": compiler_output["target_location"],
			"dialogue_payload": compiler_output["dialogue_payload"]
		}
