import json
import os
import random

from mind.inspector import NeptuneInspector
from soul.chatter.chatter_core import NeptuneChatterCore

class NeptuneDialogRouter:
	def __init__(
		self,
		inspector_instance: NeptuneInspector,
		chatter_instance: NeptuneChatterCore,
		matrix_path="/app/backend/data/neptune/repository/neptune_override_matrix.json",
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.inspector = inspector_instance
		self.chatter = chatter_instance
		self.matrix_path = matrix_path
		self.state_path = state_path
		self.override_matrix = self._load_json(self.matrix_path)

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)

	def _get_active_mood(self) -> str:
		"""Fetches current emotional tracking decay profile safely from disk."""
		if not os.path.exists(self.state_path):
			return "neutral"
		with open(self.state_path, "r", encoding="utf-8") as f:
			state = json.load(f)
			# Fallback validation to ensure string routing safety
			return state.get("meta", {}).get("active_mood", "neutral")
	def route_interaction(self, raw_input: str, compiled_generation_data: dict = None) -> dict:
		"""
		Evaluates routing flags from the inspector token matrix and 
		builds the final response payload for Open-WebUI.
		"""
		eval_vector = self.inspector.evaluate_routing_vectors(raw_input)
		route_type = eval_vector.get("route_type")
		payload_id = eval_vector.get("payload_id")
		active_mood = self._get_active_mood()

		# 1. Handle Hard-Matched Sysadmin Core Triggers
		if route_type == "sysadmin_override":
			dialogue_pools = self.override_matrix.get("dialogue_pools", {}).get(payload_id, {})
			options = dialogue_pools.get(active_mood, dialogue_pools.get("neutral", []))
			response_text = random.choice(options) if options else "Sysadmin alert state recognized."
			return {
				"execution_status": "intercepted_sysadmin",
				"output_text": response_text,
				"trigger_id": payload_id
			}

		# 2. Handle Intimate Photo Overrides
		if route_type == "lewd_photo_override" and compiled_generation_data:
			# Pluck the payload that was matched during compiler token pass
			response_text = compiled_generation_data.get("dialogue_payload", "")
			return {
				"execution_status": "intercepted_photo_override",
				"output_text": response_text,
				"trigger_id": payload_id
			}
		# 3. Handle General Engine Matches (Winking, Smile, etc.)
		if route_type == "general_photo_engine" and compiled_generation_data:
			response_text = compiled_generation_data.get("dialogue_payload", "")
			return {
				"execution_status": "intercepted_photo_engine",
				"output_text": response_text,
				"trigger_id": payload_id
			}

		# 4. Standard Flow: Pass input down directly to conversational chatter models
		chatter_response = self.chatter.process_chat_layer(raw_input, active_mood)
		return {
			"execution_status": "standard_chat_pipeline",
			"output_text": chatter_response,
			"trigger_id": None
		}