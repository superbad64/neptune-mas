import os
import json
import random
import sys
from typing import Dict, Any, List, Tuple

class NeptuneFitCheck:
    container_root = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
        self.root_volume = root_volume
        self.state_path = f"{self.root_volume}/repository/neptune_current_state.json"
        self.wardrobe_path = f"{self.root_volume}/repository/neptune_wardrobe_manifest.json"

    def execute_fit_check(self) -> str:
        """
        Calculates clothing exposure states using actual nested appearance fields.
        Guaranteed to return a valid string under all logical branches.
        """
        if not os.path.exists(self.state_path):
            return f"System Log: Current state tracking file is missing from disk arrays at {self.state_path}."
            
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

        # --- Fallback Relational Loop ---
        output_lines = ["Current Equipment Layout:"]
        try:
            with open(self.wardrobe_path, 'r', encoding='utf-8') as f:
                wardrobe = json.load(f)
        except Exception:
            wardrobe = {}

        # Mapped categories dictionary matching specific inventory layout slots to manifest names
        category_map = {
            "top": "tops", "bottom": "bottoms", "bra": "bras", "panties": "panties",
            "socks": "socks", "shoes": "shoes", "outerwear": "outerwear", 
            "hat": "hats", "hair": "hairstyles"
        }

        for slot, item_key in appearance.items():
            if slot in ["accessories", "piercings", "hairstyle"]:
                continue
            if isinstance(item_key, str) and (item_key == "naked" or item_key.strip() == ""):
                continue
                
            manifest_category = category_map.get(slot)
            flavor_text = None
            
            if manifest_category and manifest_category in wardrobe:
                if item_key in wardrobe[manifest_category]:
                    flavor_text = wardrobe[manifest_category][item_key].get("flavor_text")

            # Fallback search if category map missing
            if not flavor_text and isinstance(item_key, str):
                for category in ["tops", "bottoms", "bras", "panties", "socks", "shoes", "outerwear", "hats", "hairstyles"]:
                    if item_key in wardrobe.get(category, {}):
                        flavor_text = wardrobe[category][item_key].get("flavor_text")
                        break
            
            if flavor_text:
                clean_flavor = str(flavor_text).strip("'\"")
                output_lines.append(f'"{slot}": "{clean_flavor}"')
            else:
                output_lines.append(f'"{slot}": "{item_key}"')


        # Relational search loop processing accessories list arrays explicitly
        accessories = appearance.get("accessories", [])
        if isinstance(accessories, list) and accessories:
            acc_manifest = wardrobe.get("accessories", {})
            for acc_key in accessories:
                flavor_text = acc_manifest.get(acc_key, {}).get("flavor_text")
                # --- FIXED: Escaped characters are pulled out of the f-string braces ---
                if flavor_text:
                    clean_acc_flavor = str(flavor_text).strip("'\"")
                    output_lines.append(f'"accessory": "{clean_acc_flavor}"')
                else:
                    output_lines.append(f'"accessory": "{acc_key}"')
               
        if len(output_lines) == 1:
            return "Wearing basic components without localized flavor descriptors. (All major layers naked/cleared)"
            
        return "\n".join(output_lines)

    def modify_clothing_state(self, action: str, body_part: str, target_item: str = "") -> str:
        """Mutates wardrobe tracking properties and commits the schema state to disk."""
        if not os.path.exists(self.state_path):
            return "System Log: Cannot mutate state. Tracking file is missing."

        with open(self.state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
            
        appearance = state.setdefault("appearance", {
            "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
            "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
            "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
        })

        try:
            with open(self.wardrobe_path, 'r', encoding='utf-8') as f:
                wardrobe = json.load(f)
        except Exception:
            wardrobe = {}

        if action == "put_on":
            outfit_key = target_item if target_item else body_part
            outfits = wardrobe.get("outfits", {})
            
            if outfit_key in outfits:
                # MATCHED: Pulls item assignments strictly from the interior "items" block
                outfit_items = outfits[outfit_key].get("items", {})
                slots = ["hat", "outerwear", "top", "bottom", "bra", "panties", "socks", "shoes"]
                for slot in slots:
                    appearance[slot] = outfit_items.get(slot, "naked")
                # Accessories parse strictly as a JSON array list footprint
                appearance["accessories"] = list(outfit_items.get("accessories", []))
            else:
                if body_part in appearance:
                    appearance[body_part] = target_item

        elif action in ["remove", "take_off"]:
            if body_part in appearance and body_part != "outfit":
                if body_part == "accessories":
                    appearance["accessories"] = []
                else:
                    appearance[body_part] = "naked"

        elif action == "go_nude":
            for slot in list(appearance.keys()):
                if slot not in ["hairstyle", "piercings"]:
                    if slot == "accessories":
                        appearance[slot] = []
                    else:
                        appearance[slot] = "naked"

        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4)

        return self.execute_fit_check()

def enforce_rule_one_point_five(prompt: str, root_volume: str = "/app/backend/neptune") -> Tuple[bool, str, str]:
    """
    Parses casual user inputs against manifest triggers.
    Executes automated database modifications when triggers match.
    """
    wardrobe_path = f"{root_volume}/repository/neptune_wardrobe_manifest.json"
    if not os.path.exists(wardrobe_path):
        return False, "", ""

    try:
        with open(wardrobe_path, 'r', encoding='utf-8') as f:
            wardrobe = json.load(f)
    except Exception:
        return False, "", ""

    clean_prompt = prompt.lower().strip()
    outfits = wardrobe.get("outfits", {})

    for outfit_id, specs in outfits.items():
        triggers = specs.get("triggers", [])
        if any(trigger.lower() in clean_prompt for trigger in triggers):
            fit_checker = NeptuneFitCheck(root_volume=root_volume)
            fit_status_msg = fit_checker.modify_clothing_state(action="put_on", body_part="outfit", target_item=outfit_id)
            return True, outfit_id, fit_status_msg

    return False, "", ""

container_root = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
    """Entry point invocation signed off directly by the Face Intercept Layer."""
    # First evaluate dynamic conversational outfit changes (Rule 1.5 triggers)
    matched, outfit_id, fit_report = enforce_rule_one_point_five(prompt, root_volume=root_volume)
    if matched:
        return f"╰(✧∇✧)╯ Sweet!! Swapped into my {outfit_id.replace('_', ' ')} layout!\n\n{fit_report}"

    # Parsing hard lookups for directional removal keywords
    fit_checker = NeptuneFitCheck(root_volume=root_volume)
    clean_p = prompt.lower()
    
    if any(kw in clean_p for kw in ["go nude", "get naked", "strip"]):
        return fit_checker.modify_clothing_state(action="go_nude", body_part="all")
        
    slots = ["top", "bottom", "bra", "panties", "socks", "shoes", "outerwear", "hat", "accessories"]
    remove_keywords = ["remove", "take off", "strip off", "drop"]
    
    for slot in slots:
        if slot in clean_p:
            if any(kw in clean_p for kw in remove_keywords):
                return fit_checker.modify_clothing_state(action="remove", body_part=slot)

    return fit_checker.execute_fit_check()
