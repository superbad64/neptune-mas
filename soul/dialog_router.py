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
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.inspector = inspector_instance
		self.chatter = chatter_instance
		self.state_path = state_path

	def _get_active_mood(self) -> str:
		"""Fetches current emotional tracking decay profile safely from disk."""
		if not os.path.exists(self.state_path):
			return "neutral"
		try:
			with open(self.state_path, "r", encoding="utf-8") as f:
				state = json.load(f)
				return state.get("meta", {}).get("active_mood", "neutral")
		except Exception:
			return "neutral"

	def route_interaction(self, raw_input: str, compiled_generation_data: dict = None) -> dict:
		"""Routes traffic cleanly down to the conversational chatter model layer."""
		eval_vector = self.inspector.evaluate_routing_vectors(raw_input)
		route_type = eval_vector.get("route_type")
		payload_id = eval_vector.get("payload_id")
		active_mood = self._get_active_mood()

		# Handle Intimate Photo Overrides directly
		if route_type == "lewd_photo_override" and compiled_generation_data:
			response_text = compiled_generation_data.get("dialogue_payload", "")
			return {
				"execution_status": "intercepted_photo_override",
				"output_text": response_text,
				"trigger_id": payload_id
			}

		# Standard Flow: Pass input down directly to conversational chatter model node layers
		chatter_response = self.chatter.process_chat_layer(raw_input, active_mood)
		return {
			"execution_status": "standard_chat_pipeline",
			"output_text": chatter_response,
			"trigger_id": None
		}
