import os
import json
import random
import sys
from typing import Dict, Any, List

class NeptuneFitCheck:
    def __init__(self, root_volume: str = "/app/backend/data/neptune"):
        self.root_volume = root_volume
        self.state_path = f"{self.root_volume}/repository/neptune_current_state.json"
        self.wardrobe_path = f"{self.root_volume}/repository/neptune_wardrobe_manifest.json"

    def execute_fit_check(self) -> str:
        """
        Calculates clothing exposure states using actual nested appearance fields.
        Guaranteed to return a valid string under all logical branches.
        """
        try:
            debug_active = sys.sandbox_run("core/diagnostics_logger.py", "check_debug_external")
        except Exception:
            debug_active = True

        if not os.path.exists(self.state_path):
            return "System Log: Current state tracking file is missing from disk arrays."
            
        with open(self.state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)

        appearance = state.get("appearance", {})
        bra = appearance.get("bra", "naked").strip().lower()
        panties = appearance.get("panties", "naked").strip().lower()
        top = appearance.get("top", "naked").strip().lower()
        bottom = appearance.get("bottom", "naked").strip().lower()
        outerwear = appearance.get("outerwear", "naked").strip().lower()

        # --- Hardwired Conditional State Returns ---
        if bra == "naked" and panties == "naked" and top == "naked" and bottom == "naked" and outerwear == "naked":
            return "* [Neptune covers herself completely, blushing deeply] * \"H-hey! I'm completely naked right now! Close the console window!\""

        if top == "naked" and bottom == "naked":
            if bra != "naked" and panties != "naked":
                return "\"I'm a bit exposed like this... just standing around in my underwear.\""
            elif bra == "naked" and panties != "naked":
                return "\"Everyone can see my breasts like this! Please tell me the security camera feeds are private!\""
            elif bra != "naked" and panties == "naked":
                return "\"My pussy is out! Oh my gosh, this is a critical system vulnerability!\""

        if bottom != "naked" and top == "naked" and outerwear == "naked":
            return "* [Neptune crosses her arms over her bare chest, pouting slightly] * \"Going topless but wearing a bottom layer is... certainly a statement. My chest feels cold!\""
        # --- Fallback Relational Loop (If no explicit exposure condition is triggered) ---
        output_lines = ["Current Equipment Layout:"]
        try:
            with open(self.wardrobe_path, 'r', encoding='utf-8') as f:
                wardrobe = json.load(f)
        except Exception:
            wardrobe = {}

        for slot, item_key in appearance.items():
            if item_key == "naked" or slot in ["accessories", "piercings", "hairstyle"]:
                continue
                
            flavor_text = None
            for category in ["tops", "bottoms", "bras", "panties", "socks", "shoes", "outerwear", "hats"]:
                if item_key in wardrobe.get(category, {}):
                    flavor_text = wardrobe[category][item_key].get("flavor_text")
                    break
            
            if flavor_text:
                clean_flavor = str(flavor_text).strip('"\'')
                output_lines.append(f'"{slot}": "{clean_flavor}"')
            else:
                # Direct string fallback representation if manifest text is missing
                output_lines.append(f'"{slot}": "{item_key}"')
                
        if len(output_lines) == 1:
            return "Wearing basic components without localized flavor descriptors. (All major layers naked/cleared)"
            
        return "\n".join(output_lines)

    def modify_clothing_state(self, action: str, body_part: str, target_item: str = "") -> str:
        """Mutates wardrobe tracking properties and commits the schema state to disk."""
        if not os.path.exists(self.state_path):
            return "System Log: Cannot mutate state. Tracking file is missing."

        with open(self.state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
            
        if "appearance" not in state:
            state["appearance"] = {
                "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
                "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
            }

        try:
            with open(self.wardrobe_path, 'r', encoding='utf-8') as f:
                wardrobe = json.load(f)
        except Exception:
            wardrobe = {}

        if action == "put_on":
            if body_part == "outfit" or target_item in wardrobe.get("outfits", {}):
                outfit_key = target_item if target_item else body_part
                outfit_data = wardrobe.get("outfits", {}).get(outfit_key, {})
                if outfit_data:
                    for slot, item_key in outfit_data.get("items", {}).items():
                        if slot in state["appearance"]:
                            state["appearance"][slot] = item_key
            else:
                if body_part in state["appearance"]:
                    state["appearance"][body_part] = target_item

        elif action in ["remove", "take_off"]:
            if body_part in state["appearance"] and body_part != "outfit":
                state["appearance"][body_part] = "naked"

        elif action == "go_nude":
            for slot in state["appearance"]:
                if slot not in ["hairstyle", "accessories", "piercings"]:
                    state["appearance"][slot] = "naked"

        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

        return self.execute_fit_check()
