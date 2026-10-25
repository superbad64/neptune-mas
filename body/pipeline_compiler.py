import json
import os
import random
import re

class PipelineCompiler:
	def __init__(
		self, 
		engine_path="/app/backend/data/neptune/repository/neptune_photo_engine.json",
		overrides_path="/app/backend/data/neptune/repository/neptune_photo_overrides.json",
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.engine_path = engine_path
		self.overrides_path = overrides_path
		self.state_path = state_path
		
		self.engine = self._load_json(self.engine_path)
		self.overrides = self._load_json(self.overrides_path)

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)

	def _get_active_state(self) -> dict:
		"""Pulls running state safely from disk without corrupting attributes."""
		if not os.path.exists(self.state_path):
			return {"environment": "bed", "arousal": 0.0, "cosmetics": {}}
		with open(self.state_path, "r", encoding="utf-8") as f:
			return json.load(f)
	def _resolve_expression(self, user_input: str) -> tuple:
		"""
		Scans input text for explicit expressions (like ahegao).
		Falls back to baseline happy/teasing selections if no triggers hit.
		Returns a tuple of (expression_prompt, chosen_dialogue).
		"""
		text_lower = user_input.lower() if user_input else ""
		
		# 1. Check complex triggers first
		expressions = self.engine.get("facial_expressions", {})
		for exp_id, data in expressions.items():
			for trigger in data.get("triggers", []):
				# Use re.search to process true \b word boundary rules programmatically
				pattern = r"\b" + re.escape(trigger.lower()) + r"\b"
				if re.search(pattern, text_lower):
					prompt = data.get("prompt", "")
					dialogue = random.choice(data.get("response_pool", [""]))
					return prompt, dialogue

		# 2. Baseline happy fallbacks if no complex key match
		baselines = self.engine.get("baseline_expressions", {})
		chosen_id = random.choice(list(baselines.keys())) if baselines else "smiling"
		baseline_data = baselines.get(chosen_id, {})
		
		prompt = baseline_data.get("prompt", "")
		dialogue = random.choice(baseline_data.get("response_pool", [""]))
		return prompt, dialogue
	def compile_generation_payload(self, user_input: str = None, force_location: str = None) -> dict:
		"""
		Main execution entry point. Combines location bounds, pose vectors,
		and face prompts into a sanitized dict tailored for your string nodes.
		"""
		state = self._get_active_state()
		location = force_location or state.get("environment", "bed")
		
		loc_matrix = self.engine.get("locations", {}).get(location)
		if not loc_matrix:
			loc_matrix = self.engine.get("locations", {}).get("bed", {})
			location = "bed"

		# Resolve Pose and Camera Angle alignment constraints
		allowed_pools = loc_matrix.get("allowed_pose_pools", [])
		selected_pool = random.choice(allowed_pools) if allowed_pools else "standing_poses"
		pose_string = random.choice(self.engine.get("poses", {}).get(selected_pool, ["standing upright"]))

		allowed_angles = loc_matrix.get("allowed_angles", ["eye-level shot"])
		angle_string = random.choice(allowed_angles)

		forced_mod = loc_matrix.get("forced_prompt_modifier", "")
		face_prompt, matched_dialogue = self._resolve_expression(user_input)

		# Build raw, dynamic layout string targeting PrimitiveString Node 16
		positive_prompt = f"{pose_string}, {angle_string}, {face_prompt}"
		if forced_mod:
			positive_prompt += f", {forced_mod}"

		# Enforce our front-loaded filter constraints targeting Concatenate Node 8
		negative_prompt = "holding a phone, cellphone visible"

		return {
			"target_location": location,
			"pose": pose_string,
			"angle": angle_string,
			"positive_tokens": positive_prompt,
			"negative_tokens": negative_prompt,
			"dialogue_payload": matched_dialogue
		}
