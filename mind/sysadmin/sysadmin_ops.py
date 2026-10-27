import os
import json
import importlib

def _append_console_debug(base_res: str, transaction_id: str, context_details: str = "") -> str:
    """Direct proxy fallback router mirroring the main core panel format."""
    try:
        logger_module = importlib.import_module("core.diagnostics_logger")
        return f"{base_res}\n\n{getattr(logger_module, 'format_panel_output')('SYSADMIN BRIDGE TRANSACTION RECEIPT', {'ADMIN_EXECUTION_CONTEXT': transaction_id.upper(), 'EXECUTION_CONTEXT_DATA': context_details}, base_res)}"
    except Exception: return base_res

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

def handle_operational_overrides(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Processes character hot-swaps, forced parameters, and backend ComfyUI vector payloads."""
    
    # --- CHARACTER BLUEPRINTS ---
    if lowered_cmd == "character show":
        active_char = state_data.get("active_character", "neptune_v1")
        res = f"### 👤 Active Profile Blueprint (`{active_char}`):\n" + json.dumps(_load_json(registry_path).get(active_char, {}), indent=2)
        return _append_console_debug(res, "character_show_query")
    elif lowered_cmd == "character list":
        res = "### 👤 Registered Character Blueprint Keys:\n" + "\n".join([f"* `{k}`" for k in _load_json(registry_path).keys()])
        return _append_console_debug(res, "character_list_query")
    elif lowered_cmd.startswith("character set "):
        char_name = cmd_body[13:].strip()
        if char_name not in _load_json(registry_path): return f"❌ Error: Profile `{char_name}` is absent from registry."
        state_data["active_character"] = char_name
        _write_json(state_path, state_data)
        return _append_console_debug(f"👤 Hot-swap complete. Character matrix shifted to: `{char_name}`.", "character_set_execute")

    # --- FORCED UTILITY CHECKS ---
    elif lowered_cmd == "force state check":
        integrity = "STABLE" if os.path.exists(state_path) else "CORRUPTED"
        return _append_console_debug(f"⚙️ Filesystem check completed. Core status integrity: `{integrity}`.", "force_state_check")
    elif lowered_cmd == "force state update":
        _write_json(state_path, state_data)
        return _append_console_debug("⚙️ Filesystem rewrite complete. Dynamic metrics synced to disk.", "force_state_update")
    elif lowered_cmd == "force state reset":
        _write_json(state_path, {"active_character": "neptune_v1", "debug_verbosity": True, "mood": {"arousal": 0.0}, "appearance": {}})
        return _append_console_debug("💥 Critical Alert: Reset complete. State tree restored to clean baselines.", "force_state_reset")

    # --- FORCED EXCITATIONS ---
    elif lowered_cmd.startswith("force arousal "):
        try:
            val = float(lowered_cmd.replace("force arousal ", "").strip())
            if "mood" not in state_data: state_data["mood"] = {}
            state_data["mood"]["arousal"] = max(0.0, min(1.6, val))
            _write_json(state_path, state_data)
            return _append_console_debug(f"⚙️ Excitation locked onto index value `{state_data['mood']['arousal']}`.", "force_arousal_execute")
        except ValueError: return "```\n[ERROR]: Index must resolve as a float.\n```"

    # ==========================================================================
    # --- ADMINISTRATIVE FORCED CLIMAX OVERRIDE DECK (THRESHOLDS-AWARE) ---
    # ==========================================================================
    elif lowered_cmd == "force climax":
        try:
            if "mood" not in state_data:
                state_data["mood"] = {"arousal": 0.0, "status_effects": []}
            
            # 1. Capture and preserve her real-time pre-climax arousal float index
            pre_climax_arousal = float(state_data["mood"].get("arousal", 0.0))
            
            # 2. Commit the post-climax arousal crash parameters on disk
            state_data["mood"]["arousal"] = 0.1
            if "status_effects" in state_data["mood"] and "masturbating" in state_data["mood"]["status_effects"]:
                state_data["mood"]["status_effects"].remove("masturbating")
                
            _write_json(state_path, state_data)
            print(f"[SYSADMIN OVERRIDE] Climax authorization cleared. Preserved arousal tier float: {pre_climax_arousal}")

            # 3. Dynamic route straight to evaluate_visual_intent
            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            
            # Inject the preserved arousal index directly into the raw execution pass string
            dispatch_receipt = getattr(comfy, "evaluate_visual_intent")("", f"force_climax_event arousal_tier={pre_climax_arousal}")
            
            res_msg = f"⚙️ Administrative Bypass Committed: Forced instant climax event. Arousal crashed back to `0.1`. Handing context to intent core."
            return _append_console_debug(f"{res_msg}\n\n{dispatch_receipt}", "force_climax_administrative_execute")
            
        except Exception as e:
            return f"❌ Forced climax administrative pipeline failed: {str(e)}"

    # --- HARDWARE GENERATION DEPLOYMENT LOOPS ---
    elif lowered_cmd.startswith("force render "):
        prompt_string = cmd_body[12:].strip()
        if not prompt_string: return "```\n[ERROR]: Canvas prompt parameter missing.\n```"
        try:
            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            return _append_console_debug(getattr(comfy, "trigger_forced_generation")(prompt_string), "force_render_execute", prompt_string)
        except Exception as e: return f"❌ Forced generation pipeline failed: {str(e)}"
    elif lowered_cmd.startswith("force render_override "):
        target_override = cmd_body[21:].strip()
        try:
            comfy = importlib.import_module("body.comfy_dispatch")
            importlib.reload(comfy)
            return _append_console_debug(getattr(comfy, "evaluate_visual_intent")("", target_override), "force_render_override_execute", target_override)
        except Exception as e: return f"❌ Forced scenario override failed: {str(e)}"

    return f"```\n[SYSADMIN ERROR]: Unrecognized signature target split group: {cmd_body}\n```"
