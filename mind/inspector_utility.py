import os
import json
import random
from typing import Dict, Any, List

class NeptuneFitCheck:
    def __init__(self, root_volume: str = "/app/backend/data/neptune"):
        # Confirmed absolute path synchronization mapping
        self.root_volume = root_volume
        self.state_path = f"{self.root_volume}/repository/neptune_current_state.json"
        self.wardrobe_path = f"{self.root_volume}/repository/neptune_wardrobe_manifest.json"

    def execute_fit_check(self) -> str:
        """Calculates clothing exposure states using actual nested appearance fields."""
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

        # --- Rule 1: The 'I'm Naked' Condition Pass ---
        if bra == "naked" and panties == "naked" and top == "naked" and bottom == "naked" and outerwear == "naked":
            naked_responses = [
                "* [Neptune covers herself completely, her cheeks turning bright red] * \"H-hey! I'm completely naked right now! Close the console window!\"",
                "\"E-exposure matrix is maximum! I don't have a single piece of clothing on right now...\""
            ]
            return random.choice(naked_responses)

        # --- Rule 2: Topless & Bottomless Exposure Passes ---
        if top == "naked" and bottom == "naked":
            if bra != "naked" and panties != "naked":
                return "\"I'm a bit exposed like this... just standing around in my underwear.\""
            elif bra == "naked" and panties != "naked":
                return "\"Everyone can see my breasts like this! Please tell me the security camera feeds are private!\""
            elif bra != "naked" and panties == "naked":
                return "\"My pussy is out! Oh my gosh, this is a critical system vulnerability!\""

        # --- Rule 3: Topless with a Bottom Condition ---
        if bottom != "naked" and top == "naked" and outerwear == "naked":
            return "\"Going topless but wearing a bottom layer is... certainly a statement. My chest feels cold!\""

        # --- Rule 4: Structural Format Return Loop ---
        output_lines = ["Current Equipment Layout:"]
        try:
            with open(self.wardrobe_path, 'r', encoding='utf-8') as f:
                wardrobe = json.load(f)
        except Exception:
            wardrobe = {}

        for slot, item_key in appearance.items():
            if item_key == "naked" or slot in ["accessories", "piercings"]:
                continue
                
            flavor_text = None
            for category in ["tops", "bottoms", "bras", "panties", "socks", "shoes", "outerwear", "hats"]:
                if item_key in wardrobe.get(category, {}):
                    flavor_text = wardrobe[category][item_key].get("flavor_text")
                    break
            
            if flavor_text:
                output_lines.append(f'"{slot}": "{flavor_text}"')
                
        if len(output_lines) == 1:
            return "Wearing basic components without localized flavor descriptors."
        return "\n".join(output_lines)

    def modify_clothing_state(self, action: str, body_part: str, target_item: str = "") -> str:
        """Mutates tracking markers and commits parameters to neptune_current_state.json."""
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

        elif action in ["change", "swap"]:
            if body_part in state["appearance"] and body_part != "outfit":
                state["appearance"][body_part] = target_item

        elif action == "go_nude":
            for slot in state["appearance"]:
                if slot not in ["hairstyle", "accessories", "piercings"]:
                    state["appearance"][slot] = "naked"

        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

        return self.execute_fit_check()

# =========================================================================
# GLOBAL INTEGRITY SANDBOX EXPORT HOOKS
# =========================================================================
def execute_fit_check_external(root_volume: str) -> str:
    checker = NeptuneFitCheck(root_volume=root_volume)
    return checker.execute_fit_check()

def modify_clothing_state_external(root_volume: str, action: str, body_part: str, target_item: str = "") -> str:
    checker = NeptuneFitCheck(root_volume=root_volume)
    return checker.modify_clothing_state(action, body_part, target_item)
