import json
import os

class NeptuneInspector:
	def __init__(
		self,
		engine_path=None,
		overrides_path=None
	):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		base_dir = os.path.abspath(os.path.join(current_dir, ".."))
		
		self.engine_path = engine_path or os.path.join(base_dir, "repository", "neptune_photo_engine.json")
		self.overrides_path = overrides_path or os.path.join(base_dir, "repository", "neptune_photo_overrides.json")
		
		self.engine_data = self._load_json(self.engine_path)
		self.override_data = self._load_json(self.overrides_path)

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	def evaluate_routing_vectors(self, raw_user_input: str) -> dict:
		"""
		Evaluates input phrases cleanly across three tiers.
		Step 1: Explicit Lewd Overrides -> Step 2: Casual Photo Requests -> Step 3: Standard Chat.
		"""
		if not raw_user_input:
			return {"route_type": "standard_chat", "payload_id": None}
			
		normalized_input = raw_user_input.lower().strip()

		# 1. Evaluate Photo Lewd Overrides Array (Strict Phrase Match)
		overrides_list = self.override_data.get("overrides", [])
		for block in overrides_list:
			for keyword in block.get("trigger_keywords", []):
				if keyword.lower() in normalized_input:
					return {
						"route_type": "lewd_photo_override",
						"payload_id": block.get("id"),
						"strip_slots": block.get("strip_slots", []),
						"state_mutations": block.get("state_mutations", {})
					}

		# 2. Evaluate Casual General Photo Triggers (Selfie, Photo, Picture)
		general_photo_keywords = ["selfie", "picture", "photo", "snap", "reshoot"]
		if any(kw in normalized_input for kw in general_photo_keywords):
			return {
				"route_type": "general_photo_engine",
				"payload_id": "general_selfie_trigger"
			}

		# 3. General Fallback to standard conversational traffic
		return {"route_type": "standard_chat", "payload_id": None}