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

def execute_voice(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Controls the global disk superglobals killswitch flag for vocal synthesis routing."""
    parts = cmd_body.split()
    if len(parts) >= 2:
        action = parts[1].lower().strip()
        state_flag = True if action in ["on", "enable", "true"] else False
        
        sg_file = f"{root}/repository/neptune_superglobals.json"
        try:
            sg_data = _load_json(sg_file)
            sg_data["voice_active"] = state_flag
            _write_json(sg_file, sg_data)
            
            status_label = "🟢 ENABLED and routing to port 8000" if state_flag else "🔴 DISABLED (Safety Bypass Active)"
            return f"⚙️ *[SYSTEM CONFIG CHANGE]*: Neptune's vocal generation engine has been switched to: **{status_label}**."
        except Exception as sg_err:
            return f"❌ System Admin Error: Failed to write to superglobals config: {str(sg_err)}"
            
    return "❌ Syntax Error. Use: `neptunectl voice on` or `neptunectl voice off`"
