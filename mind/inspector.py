import json
import os
import re

class NeptuneInspector:
	def __init__(
		self,
		engine_path=None,
		overrides_path=None,
		matrix_path=None
	):
		# Compute absolute repository positions reliably across host filesystems and Docker nodes
		current_dir = os.path.dirname(os.path.abspath(__file__))
		base_dir = os.path.abspath(os.path.join(current_dir, ".."))
		
		self.engine_path = engine_path or os.path.join(base_dir, "repository", "neptune_photo_engine.json")
		self.overrides_path = overrides_path or os.path.join(base_dir, "repository", "neptune_photo_overrides.json")
		self.matrix_path = matrix_path or os.path.join(base_dir, "repository", "neptune_override_matrix.json")
		
		self.engine_data = self._load_json(self.engine_path)
		self.override_data = self._load_json(self.overrides_path)
		self.sysadmin_matrix = self._load_json(self.matrix_path)

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	def _sanitize_and_tokenize(self, text: str) -> list:
		"""Flattens input and creates clean words for strict token evaluation."""
		if not text:
			return []
		clean_text = text.lower()
		for char in [".", ",", "!", "?", "-", "_", "(", ")"]:
			clean_text = clean_text.replace(char, " ")
		return [word.strip() for word in clean_text.split() if word.strip()]

	def evaluate_routing_vectors(self, raw_user_input: str) -> dict:
		"""
		Step 1: Sysadmin Overrides -> Step 2: Lewd Overrides -> Step 3: Engine Triggers.
		Protects against partial word collisions by using direct set tokens.
		"""
		if not raw_user_input:
			return {"route_type": "standard_chat", "payload_id": None}
			
		normalized_input = raw_user_input.lower().strip()
		tokens = self._sanitize_and_tokenize(raw_user_input)

		# 1. Evaluate High-Priority Sysadmin Matrix Triggers (Exact Token Set Check)
		sysadmin_triggers = self.sysadmin_matrix.get("interaction_triggers", {})
		for trigger_id, data in sysadmin_triggers.items():
			for kw in data.get("keywords", []):
				kw_lower = kw.lower()
				# If keyword has spaces, verify full phrase containment
				if " " in kw_lower:
					if kw_lower in normalized_input:
						return {
							"route_type": "sysadmin_override",
							"payload_id": trigger_id,
							"target_subsystem": data.get("target_subsystem")
						}
				# Otherwise, verify exact word matching to protect against word-slice collisions
				elif kw_lower in tokens:
					return {
						"route_type": "sysadmin_override",
						"payload_id": trigger_id,
						"target_subsystem": data.get("target_subsystem")
					}
		# 2. Evaluate Photo Lewd Overrides Array (Explicit Phrase Match)
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

		# 3. Evaluate General Facial Expression Triggers (Exact Token Check)
		expressions = self.engine_data.get("facial_expressions", {})
		for exp_id, data in expressions.items():
			for trigger in data.get("triggers", []):
				trigger_lower = trigger.lower()
				if " " in trigger_lower:
					if trigger_lower in normalized_input:
						return {
							"route_type": "general_photo_engine",
							"payload_id": exp_id,
							"expression_prompt": data.get("prompt")
						}
				elif trigger_lower in tokens:
					return {
						"route_type": "general_photo_engine",
						"payload_id": exp_id,
						"expression_prompt": data.get("prompt")
					}

		return {"route_type": "standard_chat", "payload_id": None}