import json
import os
import re

class NeptuneClothingEngine:
	def __init__(
		self,
		manifest_path="/app/backend/data/neptune/repository/neptune_wardrobe_manifest.json",
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.manifest_path = manifest_path
		self.state_path = state_path

	def _load_json(self, path: str) -> dict:
		if not os.path.exists(path):
			return {}
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)

	def _save_state(self, state: dict) -> None:
		with open(self.state_path, "w", encoding="utf-8") as f:
			json.dump(state, f, indent="\t")

	def run_outfit_check(self) -> str:
		"""Compiles an exhaustive line-by-line text layout inventory tracking exposure boundaries."""
		state = self._load_json(self.state_path)
		manifest = self._load_json(self.manifest_path)

		current_outfit = state.get("active_outfit_key", "scene_gear")
		current_hair = state.get("active_hair_style", "long hair")

		slots = ["top", "bottom", "bra", "panties", "socks", "shoes", "outerwear"]
		inventory_desc = {}
		
		for slot in slots:
			item_key = state.get(slot, "naked")
			inventory_desc[slot] = item_key

		is_topless = inventory_desc["top"] == "naked"
		is_pantyless = inventory_desc["bottom"] == "naked"
		is_braless = inventory_desc["bra"] == "naked"
		is_no_panties = inventory_desc["panties"] == "naked"
		dialogue = "hehe like what you see, senpai? my current layout matches our fallback profile perfectly! 💕"
		
		if is_topless and is_pantyless and is_braless and is_no_panties:
			dialogue = "w-wahh?! senpai you're completely staring right at me while i'm fully nude like this! >///< stop being such a total pervert, i'm freezing! 🫣"
		elif is_topless:
			dialogue = "u-ugh... stop staring so intently at my exposed chest! 🫣 yes, i'm completely topless right now... do they look good to you or what, senpai? 💕"
		elif is_pantyless:
			dialogue = "c-completely bottomless right now... my hips are totally uncovered and it's making me crazy flustered... >///<"
		elif is_braless and not is_topless:
			dialogue = "mhm, i skipped my bra layer under this top today... don't make a big deal out of it or i'll pout, okay? ;P"
		elif not is_braless and not is_no_panties:
			dialogue = "hey there senpai! my undergarments are safely tucked away under my scene gear right now! xD"

		hair_prompt = manifest.get("hair_styles", {}).get(current_hair, {}).get("prompt", "long hair")
		
		output_lines = [
			f"👗 **Current Wardrobe Manifest Registry** ({current_outfit.upper()})",
			"=========================================",
			f"👤 **Hairstyle:** {current_hair.title()} ({hair_prompt})",
			f"外套 **Outerwear:** {inventory_desc['outerwear']}",
			f"👕 **Top:** {inventory_desc['top']}",
			f"👖 **Bottom:** {inventory_desc['bottom']}",
			f"👙 **Bra:** {inventory_desc['bra']}",
			f"🩲 **Panties:** {inventory_desc['panties']}",
			f"🧦 **Socks:** {inventory_desc['socks']}",
			f"👟 **Shoes:** {inventory_desc['shoes']}",
			"=========================================",
			f"💬 *Neptune:* \"{dialogue}\""
		]
		
		return "\n".join(output_lines)
	def process_wardrobe_command(self, processed_input: str) -> tuple:
		"""Evaluates full outfit swaps and hairstyle switches using type-safe fallback arrays."""
		text = processed_input.lower().strip()
		state = self._load_json(self.state_path)
		manifest = self._load_json(self.manifest_path)

		nude_keywords = ["go nude", "strip naked", "go completely nude", "remove all clothes"]
		if any(kw in text for kw in nude_keywords):
			state["active_outfit_key"] = "naked_profile"
			for slot in ["top", "bottom", "bra", "panties", "socks", "shoes", "outerwear"]:
				state[slot] = "naked"
			self._save_state(state)
			return True, self.run_outfit_check()

		if "hair down" in text or "default hairstyle" in text:
			state["active_hair_style"] = "long hair"
			self._save_state(state)
			return True, self.run_outfit_check()
			
		hair_triggers = {"bun": "bun", "ponytail": "sleek_ponytail", "twintails": "twintails", "braid": "braid"}
		for trigger, style_key in hair_triggers.items():
			if f"hair in a {trigger}" in text or f"hair in {trigger}" in text or f"put your hair in {trigger}" in text:
				state["active_hair_style"] = style_key
				self._save_state(state)
				return True, self.run_outfit_check()

		# Type-Safe Outfit Loop Pass: Defends against missing trigger keys natively
		outfits_pool = manifest.get("outfits", {})
		slots_to_update = ["top", "bottom", "bra", "panties", "socks", "shoes", "outerwear"]
		
		for outfit_key, data in outfits_pool.items():
			# Corrected: Use standard type enforcement to block NoneType parsing errors
			triggers = data.get("triggers") if isinstance(data, dict) and data.get("triggers") is not None else []
			for trigger in triggers:
				trigger_lower = trigger.lower()
				pattern_match = (f"put on {trigger_lower}" in text or 
								f"change to {trigger_lower}" in text or 
								f"swap to {trigger_lower}" in text or
								f"wear {trigger_lower}" in text)
				if pattern_match:
					state["active_outfit_key"] = outfit_key
					for slot in slots_to_update:
						if slot in data:
							state[slot] = data[slot]
					self._save_state(state)
					return True, self.run_outfit_check()
		# 3. Individual Garment Swap Check Pass (e.g., "put on white_shirt", "change bottom to baggy_jeans")
		slots_plural_map = {"top": "tops", "bottom": "bottoms", "bra": "bras", "panties": "panties", "socks": "socks", "shoes": "shoes", "outerwear": "outerwear"}
		for slot_singular, manifest_key in slots_plural_map.items():
			items_pool = manifest.get(manifest_key, {})
			if isinstance(items_pool, dict):
				for item_name in items_pool.keys():
					item_lower = item_name.lower()
					if f"put on {item_lower}" in text or f"wear {item_lower}" in text or f"change {slot_singular} to {item_lower}" in text or f"swap {slot_singular} to {item_lower}" in text:
						state[slot_singular] = item_name
						state["active_outfit_key"] = "custom_mix"
						self._save_state(state)
						return True, self.run_outfit_check()

		# 4. Handle Individual Garment Removal Checks ("take off", "remove")
		remove_keywords = ["remove", "take off", "strip", "drop"]
		slots_map = {
			"shirt": "top", "top": "top", "tank": "top", "button": "top",
			"pants": "bottom", "jeans": "bottom", "skirt": "bottom", "trousers": "bottom",
			"bra": "bra", "panties": "panties", "underwear": "panties", "string": "panties",
			"socks": "socks", "thigh_highs": "socks", "shoes": "shoes", "boots": "shoes", "blazer": "outerwear"
		}
		
		for kw in remove_keywords:
			for item_trigger, target_slot in slots_map.items():
				if f"{kw} your {item_trigger}" in text or f"{kw} {item_trigger}" in text:
					state[target_slot] = "naked"
					state["active_outfit_key"] = "custom_mix"
					self._save_state(state)
					return True, self.run_outfit_check()

		return False, ""