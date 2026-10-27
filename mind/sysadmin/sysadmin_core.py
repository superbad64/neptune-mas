import os
import sys
import json
import importlib

def _append_console_debug(base_res: str, transaction_id: str, context_details: str = "") -> str:
    """Handles dynamic panel logging via native importlib hooks, preventing sys errors."""
    container_root = "/app/backend/data/neptune"
    state_file = f"{container_root}/repository/neptune_current_state.json"
    debug_active = True
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                debug_active = json.load(f).get("debug_verbosity", True)
        except Exception: pass
    if not debug_active: return base_res
    meta = {
        "ADMIN_EXECUTION_CONTEXT": transaction_id.upper(),
        "TELEMETRY_LOG_TIME": "SYSTEM_LIVE_CLOCK",
        "EXECUTION_CONTEXT_DATA": context_details if context_details else "NO_METADATA_EXTENSIONS"
    }
    try:
        logger_module = importlib.import_module("core.diagnostics_logger")
        importlib.reload(logger_module)
        return f"{base_res}\n\n{getattr(logger_module, 'format_panel_output')('SYSADMIN BRIDGE TRANSACTION RECEIPT', meta, base_res)}"
    except Exception as err:
        return f"{base_res}\n\n```text\n[TELEMETRY FAULT]: Logger unavailable ({str(err)})\n```"

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

def handle_system_override(raw_prompt: str) -> str:
    """Master Administrative Gateway Interface Deck (neptunectl console hook proxy)."""
    container_root = "/app/backend/data/neptune"
    state_path = f"{container_root}/repository/neptune_current_state.json"
    registry_path = f"{container_root}/repository/neptune_character_registry.json"

    cmd_body = raw_prompt.replace("neptunectl", "", 1).strip()
    lowered_cmd = cmd_body.lower()
    state_data = _load_json_file(state_path)

    # --- CLEAR CACHE ---
    if lowered_cmd == "clear cache":
        try:
            router_module = importlib.import_module("core.face_router")
            cleared_count = getattr(router_module, "flush_module_cache")()
            return _append_console_debug(f"♻️ Cleared module cache. Cleaned up `{cleared_count}` dynamic scripts.", "clear_cache_execute")
        except Exception as e: return f"❌ Error flushing module cache: {str(e)}"

    # --- DEBUG CHANNELS ---
    elif lowered_cmd == "debug":
        return _append_console_debug(f"📟 [DEBUG METRICS]: Superglobal logging status: `{state_data.get('debug_verbosity', True)}`", "debug_status_query")
    elif lowered_cmd == "debug on":
        state_data["debug_verbosity"] = True
        _write_json_file(state_path, state_data)
        return _append_console_debug("📟 Verbose frame logging enabled globally.", "debug_toggle_on")
    elif lowered_cmd == "debug off":
        state_data["debug_verbosity"] = False
        _write_json_file(state_path, state_data)
        return "📟 Verbose frame logging disabled globally."

    # ==========================================================================
    # --- DRESS SHOW DIAGNOSTIC UTILITY HOOK ---
    # ==========================================================================
    if lowered_cmd == "dress show":
        try:
            # Dynamically import and isolate your core wardrobe diagnostic module
            inspector_module = importlib.import_module("mind.inspector_utility")
            importlib.reload(inspector_module)
            
            # Directly execute the live fit check logic by passing the active state
            # This bypasses the input text parser and prints true diagnostic telemetry
            fit_check_receipt = getattr(inspector_module, "process_wardrobe_request")("fit check")
            return _append_console_debug(fit_check_receipt, "fit_check_direct_bypass_execute")
            
        except Exception as inspector_err:
            return f"❌ System administrative fit check bypass failed:\n```text\n{str(inspector_err)}\n```"

    elif lowered_cmd.startswith("dress set "):
        params = cmd_body[9:].strip()
        if " " not in params: 
            return "```\n[ERROR]: Syntax error. Usage: neptunectl dress set <body part/outfit> <clothing item/style_id>\n```"
            
        body_part, clothing_item = params.split(" ", 1)
        body_part = body_part.lower().strip()
        clothing_item = clothing_item.strip()
        
        if "appearance" not in state_data: 
            state_data["appearance"] = {}

        # --- DYNAMIC OUTFIT MATRIX UNPACKING HOOK ---
        if body_part == "outfit":
            wardrobe_path = f"{container_root}/repository/neptune_wardrobe_manifest.json"
            wardrobe_manifest = _load_json_file(wardrobe_path)
            
            # Fetch the parent style profile block
            outfit_profile = wardrobe_manifest.get("outfits", {}).get(clothing_item)
            if not outfit_profile or not isinstance(outfit_profile, dict):
                return f"❌ [WARDROBE ERROR]: The outfit style index key `{clothing_item}` does not exist inside neptune_wardrobe_manifest.json."
                
            # Target the inner nested 'items' configuration block
            outfit_set = outfit_profile.get("items")
            if not outfit_set or not isinstance(outfit_set, dict):
                return f"❌ [WARDROBE ERROR]: The outfit profile `{clothing_item}` is missing an 'items' configuration block."
                
            # Iterate and unpack straight into her flat baseline variables
            unpacked_slots = []
            for slot_key, item_value in outfit_set.items():
                clean_slot = slot_key.lower().strip()
                state_data["appearance"][clean_slot] = item_value
                unpacked_slots.append(f"{clean_slot}: `{item_value}`")
                
            _write_json_file(state_path, state_data)
            
            res = f"👗 **Dynamic Outfit Array Unpacked Successfully!** Overwrote baseline slots with preset `{clothing_item}`:\n" + "\n".join([f"* {s}" for s in unpacked_slots])
            return _append_console_debug(res, "outfit_expansion_execute", f"Preset: {clothing_item}")

        # --- STANDARD SINGLE GARMENT MUTATION FALLBACK ---
        else:
            state_data["appearance"][body_part] = clothing_item
            _write_json_file(state_path, state_data)
            return _append_console_debug(f"✅ Wardrobe update written: `appearance['{body_part}'] = '{clothing_item}'`", "dress_set_execute", f"{body_part}->{clothing_item}")

    elif lowered_cmd == "dress clear":
        # Reset back to unclad factory baselines while preserving essential dictionary slots
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
        return _append_console_debug("👗 Wardrobe strip loop executed. All garment tracking parameters restored to naked factory baselines.", "dress_clear_execute")

    # --- STATE ENGINE CORE ---
    elif lowered_cmd == "show state":
        return _append_console_debug("### 📟 [NEPTUNE CORE APPLICATION STATE MATRIX]\n```json\n" + json.dumps(state_data, indent=2) + "\n```", "show_state_execute")
    elif lowered_cmd.startswith("load state "):
        target_file = cmd_body[10:].strip()
        target_path = os.path.join(container_root, "repository", target_file if target_file.endswith(".json") else f"{target_file}.json")
        if not os.path.exists(target_path): return f"❌ Savestate file not found at {target_path}"
        _write_json_file(state_path, _load_json_file(target_path))
        return _append_console_debug(f"💾 State recovered from: `{target_file}`", "load_state_execute")
    elif lowered_cmd.startswith("save state "):
        target_file = cmd_body[10:].strip()
        target_path = os.path.join(container_root, "repository", target_file if target_file.endswith(".json") else f"{target_file}.json")
        _write_json_file(target_path, state_data)
        return _append_console_debug(f"💾 Snapshot committed to: `{target_file}`", "save_state_save")

    # --- FORWARD TO PART 2 GATEWAY RENDERERS ---
    elif any(lowered_cmd.startswith(p) for p in ["character ", "force "]):
        try:
            ops_module = importlib.import_module("mind.sysadmin.sysadmin_ops")
            importlib.reload(ops_module)
            return getattr(ops_module, "handle_operational_overrides")(cmd_body, lowered_cmd, state_data, state_path, registry_path, container_root)
        except Exception as e: return f"❌ Operational Exception: {str(e)}"

    # --- DEFAULT CONTROL PANEL MANUAL ---
    help_manual = (
        "### 📟 [NEPTUNE MULTI-AGENT SUBSYSTEM MAN-PAGES]\n"
        "Unrecognized administrative command sequence. Refer to the manual:\n\n"
        "```text\nSYSTEM OVERRIDES MANUAL:\n"
        "- clear cache: Clears the module cache. Returns how many items were cleaned up\n"
        "- debug: Checks the active state of superglobal logging parameters\n"
        "- debug on/off: Toggles verbose frame output details globally\n"
        "- dress show: Returns active fit_check() diagnostics bypassing standard routers\n"
        "- dress set <body part> <clothing item>: Forces localized outfit alteration changes\n"
        "- dress clear: Shorthand loop to strip all current garment tracking metrics\n"
        "- show state: Returns a cleanly formatted version of neptune_current_state.json\n"
        "- load state <file>: Overwrites neptune_current_state.json with <file>\n"
        "- save state <file>: Writes neptune_current_state.json to <file>\n"
        "- character show: Returns information on the active profile variable layout\n"
        "- character list: Returns available character keys from the datastore\n"
        "- character set <name>: Hot-swaps the underlying character registry matrices\n"
        "- force state check/update/reset: Direct filesystem access mechanisms\n"
        "- force arousal <value>: Adjusts internal excitation parameters (0.0 to 1.6)\n"
        "- force render <prompt>: Forces a render using <prompt> as positive input\n"
        "- force render_override <override>: Forces a render using <override> template\n```"
    )
    return _append_console_debug(help_manual, "unrecognized_admin_signature_parse")