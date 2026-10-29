import os
import json

def _load_json(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception: pass
    return {}

def _write_json(path: str, data: dict):
    try:
        with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)
    except Exception: pass

def execute_character(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Isolates character identity blueprint checks, directory listings, and active profile matrix hot-swapping."""
    
    # --- SHOW ACTIVE COMPANION BLUEPRINT SUMMARY ---
    if lowered_cmd == "character show":
        active_char = state_data.get("active_character", "neptune_v1")
        res = f"### 👤 Active Profile Blueprint (`{active_char}`):\n" + json.dumps(_load_json(registry_path).get(active_char, {}), indent=2)
        return res

    # --- REGISTERED PROFILE MATRIX KEY LISTINGS ---
    elif lowered_cmd == "character list":
        res = "### 👤 Registered Character Blueprint Keys:\n" + "\n".join([f"* `{k}`" for k in _load_json(registry_path).keys()])
        return res

    # --- INITIALIZE ACTIVE MATRIX SWAP OVERRIDE ---
    elif lowered_cmd.startswith("character set "):
        char_name = cmd_body[14:].strip()
        if char_name not in _load_json(registry_path): 
            return f"❌ Error: Identity profile blueprint `{char_name}` is absent from neptune_character_registry.json."
            
        state_data["active_character"] = char_name
        _write_json(state_path, state_data)
        return f"👤 Hot-swap complete. Character matrix shifted to active identity slot: `{char_name}`."

    return f"❌ Unrecognized character modifier option tracking target. Use: `neptunectl character show`, `neptunectl character list`, or `neptunectl character set <id>`"