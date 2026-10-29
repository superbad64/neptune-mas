import os
import json

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

def execute_state(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Isolates core savestate snapshot commits, recoveries, and telemetry metric dumps."""
    
    # --- SHOW STATE TELEMETRY MATRIX ---
    if lowered_cmd == "state show":
        return "### 📟 [NEPTUNE CORE APPLICATION STATE MATRIX]\n```json\n" + json.dumps(state_data, indent=2) + "\n```"

    # --- RECOVER STATE FILE FROM DISK ---
    elif lowered_cmd.startswith("state load "):
        target_file = cmd_body[11:].strip()
        target_path = os.path.join(root, "repository", target_file if target_file.endswith(".json") else f"{target_file}.json")
        
        if not os.path.exists(target_path): 
            return f"❌ Savestate file not found at {target_path}"
            
        _write_json_file(state_path, _load_json_file(target_path))
        return f"💾 State recovered from snapshot: `{target_file}`"

    # --- COMMIT ACTIVE TELEMETRY SNAPSHOT TO DISK ---
    elif lowered_cmd.startswith("state save "):
        target_file = cmd_body[11:].strip()
        target_path = os.path.join(root, "repository", target_file if target_file.endswith(".json") else f"{target_file}.json")
        
        _write_json_file(target_path, state_data)
        return f"💾 Active telemetry snapshot committed to: `{target_file}`"

    return f"❌ Unrecognized state command modifier. Use: `neptunectl state show`, `neptunectl state load <file>`, or `neptunectl state save <file>`"