import json
import os
import requests

class NeptuneOrchestrator:
	def __init__(
		self,
		inspector=None,
		compiler=None,
		dispatcher=None,
		router=None,
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.state_path = state_path
		self.inspector = inspector
		self.compiler = compiler
		self.dispatcher = dispatcher
		self.router = router

	def _update_state_matrix(self, mutations: dict) -> None:
		"""Updates persistent tracking variables on disk cleanly."""
		if not mutations or not os.path.exists(self.state_path):
			return
		try:
			with open(self.state_path, "r", encoding="utf-8") as f:
				current_state = json.load(f)
			for key, val in mutations.items():
				current_state[key] = val
			with open(self.state_path, "w", encoding="utf-8") as f:
				json.dump(current_state, f, indent="\t")
		except Exception as e:
			print(f"[Orchestrator Warning] State sync operation dropped: {e}")

	def _get_active_state(self) -> dict:
		if not os.path.exists(self.state_path):
			return {"environment": "bed"}
		with open(self.state_path, "r", encoding="utf-8") as f:
			return json.load(f)
	def _ping_hardware_node(self, ip_address: str) -> bool:
		"""Performs an instant, low-overhead HTTP connection handshake to verify host state."""
		try:
			url = f"http://{ip_address}/"
			res = requests.get(url, timeout=1.5)
			return res.status_code == 200
		except Exception:
			return False

	def process_agent_turn(self, raw_user_prompt: str, workflow_template_path: str) -> dict:
		"""Orchestrates turn transactions, guaranteeing non-empty dictionary responses across all paths."""
		eval_vector = self.inspector.evaluate_routing_vectors(raw_user_prompt)
		route_type = eval_vector.get("route_type")

		# 1. Body Layer Clothing Engine Interceptions
		from body.clothing_engine import NeptuneClothingEngine
		clothing_core = NeptuneClothingEngine(state_path=self.state_path)
		
		outfit_check_triggers = ["what are you wearing", "outfit check", "check inventory", "current outfit", "what clothes do you have on"]
		normalized_check = raw_user_prompt.lower().strip()
		
		if any(trigger in normalized_check for trigger in outfit_check_triggers):
			inventory_rundown = clothing_core.run_outfit_check()
			return {
				"route_type": "standard_chat",
				"active_hardware_node": "intercepted_clothing_engine",
				"output_response": inventory_rundown,
				"render_pipeline_status": "skipped",
				"comfy_prompt_id": None
			}

		mutation_triggered, mutation_output = clothing_core.process_wardrobe_command(raw_user_prompt)
		if mutation_triggered:
			return {
				"route_type": "standard_chat",
				"active_hardware_node": "intercepted_clothing_engine",
				"output_response": mutation_output,
				"render_pipeline_status": "skipped",
				"comfy_prompt_id": None
			}

		# 2. Compute standard verbal text lines from the active router layer
		final_routing = self.router.route_interaction(raw_user_prompt, None)
		
		desktop_online = self._ping_hardware_node("10.0.0.64:11434")
		server_online = self._ping_hardware_node("10.0.0.7:11434")
		
		active_worker = "failed"
		is_konbini_shift = False
		
		if desktop_online:
			active_worker = "primary_desktop"
		elif server_online:
			active_worker = "backup_server"
			is_konbini_shift = True

		# 3. Process image generation payloads cleanly
		compiled_visuals = None
		render_receipt = {"status": "skipped"}
		
		if not is_konbini_shift and route_type in ["lewd_photo_override", "general_photo_engine"]:
			compiled_visuals = self.compiler.compile_generation_payload(user_input=raw_user_prompt)
			render_receipt = self.dispatcher.execute_render_pipeline(compiled_visuals, workflow_template_path)
			
			if compiled_visuals.get("dialogue_payload"):
				final_routing["output_text"] = compiled_visuals["dialogue_payload"]

		return {
			"route_type": route_type,
			"active_hardware_node": active_worker,
			"output_response": final_routing.get("output_text", "Processing anomaly encountered."),
			"render_pipeline_status": render_receipt.get("status", "skipped"),
			"comfy_prompt_id": render_receipt.get("prompt_id") if "prompt_id" in render_receipt else None
		}
