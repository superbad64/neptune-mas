import json
import os
import requests
import re

class ComfyDispatcher:
	def __init__(self, target_host="10.0.0.64", target_port=8189):
		self.server_address = f"{target_host}:{target_port}"
		self.client_id = "neptune_body_agent"

	def format_ksampler_workflow(self, workflow_template: dict, prompt_tokens: dict) -> dict:
		"""
		Maps tokens directly into your custom StringConcatenate graph layout.
		Injects the visual parameters into Node 16 and front-loads negative 
		electronic filters into Node 8.
		"""
		graph = json.loads(json.dumps(workflow_template))
		
		# 1. Inject Dynamic Positional Tokens into PrimitiveString (Node 16)
		if "16" in graph and graph["16"].get("class_type") == "PrimitiveString":
			graph["16"]["inputs"]["value"] = prompt_tokens["positive_tokens"]
			
		# 2. Prepend electronic filters into the negative StringConcatenate block (Node 8)
		if "8" in graph and graph["8"].get("class_type") == "StringConcatenate":
			# Combine your required front-loaded filters with whatever is currently in string_b
			existing_b = graph["8"]["inputs"].get("string_b", "")
			filter_prefix = prompt_tokens["negative_tokens"]
			
			if existing_b:
				graph["8"]["inputs"]["string_b"] = f"{filter_prefix}, {existing_b}"
			else:
				graph["8"]["inputs"]["string_b"] = filter_prefix
				
		# 3. Dynamic Seed Randomization to prevent output caching duplication
		if "4" in graph and graph["4"].get("class_type") == "KSampler":
			graph["4"]["inputs"]["seed"] = random.randint(10000000000000, 99999999999999)
				
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
		"""
		Asset Sync Loop Step: Bypasses client output routes to stream variants 
		straight into ComfyUI's input cache directory via raw sanitized strings.
		"""
		sanitized_filename = re.sub(r"[^\w\-_.]", "_", filename_string)
		url = f"http://{self.server_address}/upload/image"
		
		if not os.path.exists(local_image_path):
			return False
			
		try:
			with open(local_image_path, "rb") as f:
				files = {"image": (sanitized_filename, f, "image/png")}
				data = {"overwrite": "true"}
				res = requests.post(url, files=files, data=data, timeout=20)
				return res.status_code == 200
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
