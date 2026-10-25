import os
import sys

# Auto-compute the base file path location dynamically to allow standalone host volume execution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NEPTUNE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

print(f"[DEBUG Init] CURRENT_DIR detected as: {CURRENT_DIR}")
print(f"[DEBUG Init] NEPTUNE_ROOT calculated as: {NEPTUNE_ROOT}")

if NEPTUNE_ROOT not in sys.path:
	sys.path.insert(0, NEPTUNE_ROOT)
	print(sys.path)

import json
import random
import time
import urllib.parse
import urllib.request

from body.pipeline_compiler import PipelineCompiler
from body.comfy_dispatch import ComfyDispatcher

class ReshootWorker:
	def __init__(self, target_host="10.0.0.64", target_port=8189):
		self.server_address = f"{target_host}:{target_port}"
		print(f"[DEBUG Worker] Initializing ReshootWorker pointing to target server address: {self.server_address}")
		
		self.compiler = PipelineCompiler()
		self.dispatcher = ComfyDispatcher(target_host, target_port)
		self.output_dir = os.path.join(NEPTUNE_ROOT, "repository", "test_renders")
		os.makedirs(self.output_dir, exist_ok=True)
		print(f"[DEBUG Worker] Reference assets output directory verified at: {self.output_dir}")

	def _wait_for_render_completion(self, prompt_id: str, poll_interval=2) -> None:
		"""Polls history endpoint and outputs explicit transaction steps until completion."""
		url = f"http://{self.server_address}/history"
		print(f"[DEBUG Worker] Beginning standard HTTP polling loop tracking for completion state on prompt_id: {prompt_id}")
		
		loop_count = 0
		while True:
			loop_count += 1
			try:
				print(f"[DEBUG Poller] Loop pass #{loop_count}: Sending request to url -> {url}")
				with urllib.request.urlopen(url, timeout=5) as response:
					history = json.loads(response.read().decode("utf-8"))
				
				print(f"[DEBUG Poller] Successfully retrieved history registry. Discovered total elements: {len(history)}")
				if prompt_id in history:
					print(f"[DEBUG Success] Target prompt execution found inside completed history indices for ID: {prompt_id}")
					break
				else:
					print(f"[DEBUG Poller] Prompt ID {prompt_id} not yet visible inside history structure keys.")
			except Exception as e:
				print(f"[DEBUG Error] Polling pass encountered a soft failure state exception: {e}")
			time.sleep(poll_interval)
	def _fetch_and_store_image(self, prompt_id: str, label: str) -> None:
		"""Downloads final images and tracks payload sizes while closing the loop."""
		url = f"http://{self.server_address}/history/{prompt_id}"
		print(f"[DEBUG Worker] Initiating reference asset retrieval process for job: {label} (ID: {prompt_id})")
		print(f"[DEBUG Worker] Interrogating job transaction details at url -> {url}")
		
		try:
			with urllib.request.urlopen(url, timeout=5) as response:
				history = json.loads(response.read().decode("utf-8"))
				
			outputs = history[prompt_id]["outputs"]
			print(f"[DEBUG Linker] Extracting execution node mappings. Available output nodes: {list(outputs.keys())}")
			
			for node_id, node_output in outputs.items():
				if "images" in node_output:
					print(f"[DEBUG Linker] Found target image parameters inside node execution block ID: {node_id}")
					for img_meta in node_output["images"]:
						filename = img_meta["filename"]
						
						img_url = f"http://{self.server_address}/view?filename={filename}&subfolder={img_meta['subfolder']}&type={img_meta['type']}"
						local_name = "neptune_frame_latest.png"
						local_path = os.path.join(self.output_dir, local_name)
						
						print(f"[DEBUG Downloader] Fetching raw asset data package stream from network path: {img_url}")
						print(f"[DEBUG Downloader] Committing local data payload down onto disk at target: {local_path}")
						urllib.request.urlretrieve(img_url, local_path)
						
						print(f"[DEBUG Sync] Directing back-channel sync upload loop to inject asset into ComfyUI cache folder...")
						sync_success = self.dispatcher.cache_backchannel_variant(local_path, local_name)
						print(f"[DEBUG Sync] Dispatch cache back-channel response reported: {sync_success}")
		except Exception as e:
			print(f"[DEBUG Fatal Error] Closed-loop generation sync caught a terminal transaction failure: {e}")
	def execute_automated_sweep(self, workflow_template_path: str) -> None:
		"""Runs the visual generation matrix tracking each operational checkpoint."""
		print(f"[DEBUG Sweeper] Pre-flight parsing check: Opening design workflow template configuration -> {workflow_template_path}")
		if not os.path.exists(workflow_template_path):
			print(f"[DEBUG Fatal Error] Pre-flight aborted. Template file missing from disk location space!")
			return

		test_matrix = [
			{"name": "desk_baseline", "input": "sitting at her desk", "loc": "desk"},
			{"name": "mirror_wink", "input": "winking in front of the mirror", "loc": "mirror"},
			{"name": "bed_ahegao", "input": "give me an ahegao look on the bed", "loc": "bed"},
			{"name": "lewd_lift_shirt", "input": "lift your shirt", "loc": "bed"}
		]

		for run in test_matrix:
			print(f"\n=======================================================")
			print(f"🚀 [DEBUG RUN] Launching targeted pipeline phase: {run['name'].upper()}")
			print(f"📍 Location Parameter: {run['loc']} | Input String: '{run['input']}'")
			
			print(f"[DEBUG Compiler] Packaging token properties through PipelineCompiler...")
			payload = self.compiler.compile_generation_payload(user_input=run["input"], force_location=run["loc"])
			print(f"[DEBUG Compiler] Positive layout string generated: '{payload['positive_tokens']}'")
			print(f"[DEBUG Compiler] Negative layout string front-loaded: '{payload['negative_tokens']}'")
			
			print(f"[DEBUG Dispatcher] Forwarding compiled token payload out to remote ComfyDispatcher server workflow graph...")
			receipt = self.dispatcher.execute_render_pipeline(payload, workflow_template_path)
			print(f"[DEBUG Dispatcher] Receipt response array returned: {receipt}")
			
			if receipt["status"] == "queued":
				prompt_id = receipt["prompt_id"]
				print(f"[DEBUG Success] Job registered inside remote queue matrix successfully. Tracking ID achieved: {prompt_id}")
				self._wait_for_render_completion(prompt_id)
				self._fetch_and_store_image(prompt_id, run["name"])
			else:
				print(f"❌ [DEBUG Fatal Error] WSL ComfyUI rejected payload token bundle compilation for phase target: {run['name']}")

if __name__ == "__main__":
	# Target your exact historical subdirectory and file name layout precisely
	template = os.path.abspath(os.path.join(NEPTUNE_ROOT, "repository", "Image generation", "ponyrealism_workflow.json"))
	worker = ReshootWorker()
	worker.execute_automated_sweep(template)
