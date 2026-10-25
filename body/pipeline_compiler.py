import json
import os
import random
import re

class PipelineCompiler:
	def __init__(
		self, 
		engine_path=None,
		overrides_path=None,
		state_path=None
	):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		base_dir = os.path.abspath(os.path.join(current_dir, ".."))
		
		self.engine_path = engine_path or os.path.join(base_dir, "repository", "neptune_photo_engine.json")
		self.overrides_path = overrides_path or os.path.join(base_dir, "repository", "neptune_photo_overrides.json")
		self.state_path = state_path or os.path.join(base_dir, "repository", "neptune_state.json")
		
		self.engine = self._load_json(self.engine_path)
		self.overrides = self._load_json(self.overrides_path)

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)

	def _get_active_state(self) -> dict:
		"""Fetches active values, force-injecting scene_gear as the absolute default system configuration."""
		if not os.path.exists(self.state_path):
			return {
				"environment": "bed",
				"active_outfit_key": "scene_gear",
				"top": "white_shirt",
				"bottom": "baggy_jeans",
				"bra": "naked",
				"panties": "white_string",
				"socks": "white_socks",
				"shoes": "high_tops"
			}
		with open(self.state_path, "r", encoding="utf-8") as f:
			return json.load(f)
	def compile_generation_payload(self, user_input: str = None, force_location: str = None) -> dict:
		"""Combines layout properties into a clean primitive block, force-injecting character anchors."""
		state = self._get_active_state()
		location = force_location or state.get("environment", "bed")
		
		loc_matrix = self.engine.get("locations", {}).get(location)
		if not loc_matrix:
			loc_matrix = self.engine.get("locations", {}).get("bed", {})
			location = "bed"

		allowed_pools = loc_matrix.get("allowed_pose_pools", ["standing_poses"])
		selected_pool = random.choice(allowed_pools) if allowed_pools else "standing_poses"
		
		poses_pool = self.engine.get("poses", {}).get(selected_pool, ["standing upright"])
		pose_string = random.choice(poses_pool) if poses_pool else "standing upright"

		allowed_angles = loc_matrix.get("allowed_angles", ["eye-level shot"])
		angle_string = random.choice(allowed_angles) if allowed_angles else "eye-level shot"

		face_prompt, matched_dialogue = self._resolve_expression(user_input)

		# Strict physical-only appearance tokens. Completely strips out any conversational text or relationship words.
		character_anchor = "1girl, solo, clean sharp focus, masterpiece, highest quality, neptune anime character, emo scene kid baddie appearance, dark messy scene hair, sharp framing, piercing blue eyes, realistic detailed skin textures"
		wardrobe_prompt = "wearing a loose fit white t-shirt, dark grey oversized baggy jeans, sagging low on hips, studded belt, striped pink arm warmers, fingerless gloves"

		# Construct the clean text pass
		positive_prompt = f"{character_anchor}, {wardrobe_prompt}, {pose_string}, {angle_string}, happy smile, cheerful expression"

		# Exclude multi-character couple datasets completely via aggressive negative weights
		negative_prompt = "2girls, multi-character, couple, group, boyfriend, husband, male, man, partner, holding a phone, cellphone visible, deformed face, worst quality, low quality, bad anatomy, text, watermark"

		return {
			"target_location": location,
			"pose": pose_string,
			"angle": angle_string,
			"positive_tokens": positive_prompt,
			"negative_tokens": negative_prompt,
			"dialogue_payload": matched_dialogue
		}