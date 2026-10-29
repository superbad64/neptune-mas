import os
import json
import importlib

def _load_json_file(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception: pass
    return {}

def _write_json_file(path: str, data: dict) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
        return True
    except Exception: return False

def execute_dress(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Isolates dynamic wardrobe alterations, manifestation unpacking, and factory stripping loops."""
    
    # --- SHOW ACTIVE APPAREL APPARATUS FIT CHECK ---
    if lowered_cmd == "dress show":
        try:
            inspector_module = importlib.import_module("mind.inspector_utility")
            importlib.reload(inspector_module)
            fit_check_receipt = getattr(inspector_module, "process_wardrobe_request")("fit check")
            return fit_check_receipt
        except Exception as inspector_err:
            return f"❌ System administrative fit check bypass failed:\n```text\n{str(inspector_err)}\n```"

    # --- CLOTHING MUTATION MUTATOR MATRIX ---
    elif lowered_cmd.startswith("dress set "):
        params = cmd_body[9:].strip()
        if " " not in params: 
            return "```\n[ERROR]: Syntax error. Usage: neptunectl dress set <body part/outfit> <clothing item/style_id>\n```"
            
        body_part, clothing_item = params.split(" ", 1)
        body_part = body_part.lower().strip()
        clothing_item = clothing_item.strip()
        
        if "appearance" not in state_data: 
            state_data["appearance"] = {}

        if body_part == "outfit":
            wardrobe_path = f"{root}/repository/neptune_wardrobe_manifest.json"
            wardrobe_manifest = _load_json_file(wardrobe_path)
            
            outfit_profile = wardrobe_manifest.get("outfits", {}).get(clothing_item)
            if not outfit_profile or not isinstance(outfit_profile, dict):
                return f"❌ [WARDROBE ERROR]: The outfit style index key `{clothing_item}` does not exist inside neptune_wardrobe_manifest.json."
                
            outfit_set = outfit_profile.get("items")
            if not outfit_set or not isinstance(outfit_set, dict):
                return f"❌ [WARDROBE ERROR]: The outfit profile `{clothing_item}` is missing an 'items' configuration block."
                
            unpacked_slots = []
            for slot_key, item_value in outfit_set.items():
                clean_slot = slot_key.lower().strip()
                state_data["appearance"][clean_slot] = item_value
                unpacked_slots.append(f"{clean_slot}: `{item_value}`")
                
            _write_json_file(state_path, state_data)
            return f"👗 **Dynamic Outfit Array Unpacked Successfully!** Overwrote baseline slots with preset `{clothing_item}`:\n" + "\n".join([f"* {s}" for s in unpacked_slots])

        else:
            state_data["appearance"][body_part] = clothing_item
            _write_json_file(state_path, state_data)
            return f"✅ Wardrobe update written: `appearance['{body_part}'] = '{clothing_item}'`"

    # --- PURGE MATRIX BACK TO FACTORY NAKED BASELINES ---
    elif lowered_cmd == "dress clear":
        state_data["appearance"] = {
            "hat": "naked",
            "hairstyle": state_data.get("appearance", {}).get("hairstyle", "loose_hair"),
            "outerwear": "naked",
            "top": "naked",
            "bra": "naked",
            "bottom": "naked",
            "panties": "naked",
            "socks": "naked",
            "shoes": "naked",
            "accessories": [],
            "piercings": []
        }
        _write_json_file(state_path, state_data)
        return "👗 Wardrobe strip loop executed. All garment tracking parameters restored to naked factory baselines."

    return f"❌ Unrecognized wardrobe modifier option flag matching rule: `{cmd_body}`"
