import os
import json
import importlib

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

def execute_force(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Isolates forced parameters, hardware rendering pipelines, and state file management overrides."""
    
    # --- FILESYSTEM MAINTENANCE AND SNAPS ---
    if lowered_cmd == "force state check":
        integrity = "STABLE" if os.path.exists(state_path) else "CORRUPTED"
        return f"⚙️ Filesystem check completed. Core status integrity: `{integrity}`."
    elif lowered_cmd == "force state update":
        _write_json(state_path, state_data)
        return "⚙️ Filesystem rewrite complete. Dynamic metrics synced to disk."
    elif lowered_cmd == "force state reset":
        _write_json(state_path, {"active_character": "neptune_v1", "debug_verbosity": True, "mood": {"arousal": 0.0}, "appearance": {}})
        return "💥 Critical Alert: Reset complete. State tree restored to clean baselines."

    # --- FORCED EXCITATIONS ---
    elif lowered_cmd.startswith("force arousal "):
        try:
            val = float(lowered_cmd.replace("force arousal ", "").strip())
            if "mood" not in state_data: state_data["mood"] = {}
            state_data["mood"]["arousal"] = max(0.0, min(1.6, val))
            _write_json(state_path, state_data)
            return f"⚙️ Excitation locked onto index value `{state_data['mood']['arousal']}`."
        except ValueError: 
            return "```\n[ERROR]: Index must resolve as a float.\n```"

    # --- FORCED INTENSE CLIMAX THRESHOLDS ---
    elif lowered_cmd == "force climax":
        try:
            if "mood" not in state_data:
                state_data["mood"] = {"arousal": 0.0, "status_effects": []}
            
            pre_climax_arousal = float(state_data["mood"].get("arousal", 0.0))
            state_data["mood"]["arousal"] = 0.1
            state_data["self_arousal"] = 0.0
            if "status_effects" in state_data["mood"] and "masturbating" in state_data["mood"]["status_effects"]:
                state_data["mood"]["status_effects"].remove("masturbating")
                
            _write_json(state_path, state_data)
            print(f"[SYSADMIN OVERRIDE] Climax authorization cleared. Preserved arousal tier float: {pre_climax_arousal}")

            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            
            dispatch_receipt = getattr(comfy, "evaluate_visual_intent")("", f"force_climax_event arousal_tier={pre_climax_arousal}")
            return f"⚙️ Administrative Bypass Committed: Forced instant climax event. Arousal crashed back to `0.1`. Handing context to intent core.\n\n{dispatch_receipt}"
            
        except Exception as e:
            return f"❌ Forced climax administrative pipeline failed: {str(e)}"

    # --- CANVAS AND HARDWARE DEPLOYMENT GENERATIONS ---
    elif lowered_cmd.startswith("force render "):
        prompt_string = cmd_body[12:].strip()
        if not prompt_string: return "```\n[ERROR]: Canvas prompt parameter missing.\n```"
        try:
            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            return getattr(comfy, "trigger_forced_generation")(prompt_string)
        except Exception as e: return f"❌ Forced generation pipeline failed: {str(e)}"
        
    elif lowered_cmd.startswith("force render_override "):
        target_override = cmd_body[21:].strip()
        try:
            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            return getattr(comfy, "evaluate_visual_intent")("", target_override)
        except Exception as e: return f"❌ Forced scenario override failed: {str(e)}"

    # Place this block right inside your execute_force switch matrix:
    # --- CODER CORE LIVE SELF-SURGERY INTERCEPT ---
    elif lowered_cmd == "force refactor confirm":
        print("[SYSADMIN MODULE] Master override key confirmed. Waking Coder Core executor.")
        try:
            # Dynamically import the Coder core logic engine to handle the rewrite securely
            coder = importlib.import_module("mind.coder.coder_core")
            importlib.reload(coder)
            
            # Instantiating the object-oriented logic using the root argument passed down by the core proxy
            coder_instance = getattr(coder, "NeptuneCoderCore")()
            return coder_instance.execute_live_workspace_refactor()
            
        except Exception as surgery_err:
            return f"❌ **[SYSADMIN BINDING ERROR]**: Handoff to Coder Core failed: `{str(surgery_err)}`"

    return f"❌ Unrecognized administrative force sub-directive command: `{cmd_body}`"
