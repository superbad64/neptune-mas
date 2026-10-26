import os
import sys
import json
import traceback

def handle_system_override(raw_prompt: str) -> str:
    """
    Main system overrides router. Fully synchronized to leverage our universally
    stable sys.sandbox_run() engine and unified superglobal verbosity panels.
    """
    container_root = "/app/backend/data/neptune"
    repository_dir = f"{container_root}/repository"
    state_path = f"{repository_dir}/neptune_current_state.json"

    # Evaluate dynamic superglobal verbose logging states using the sys namespace loader
    try:
        debug_verbosity = sys.sandbox_run("core/diagnostics_logger.py", "check_debug_external")
    except Exception:
        debug_verbosity = True  # Safe resilient fallback default

    if debug_verbosity:
        try:
            sys.sandbox_run("core/diagnostics_logger.py", "log_trace_external", "sysadmin_core", "command_intercept", raw_prompt)
        except Exception:
            pass

    # Isolate parameters from the systemd-style administrative control prefix cleanly
    cmd_body = raw_prompt.replace("neptunectl", "", 1).strip()
    lowered_cmd = cmd_body.lower()
    def _append_console_debug(base_text: str, action_key: str, payload_data: str = None) -> str:
        """Appends a minimalist markdown diagnostic panel with explicit spacing insulation."""
        if not debug_verbosity:
            return base_text
            
        meta = {
            "CONSOLE_ROUTE" : "SYSADMIN_OVERRIDE",
            "ACTION_ENGAGED": action_key.upper(),
            "DISK_ARRAY_IO" : "NOMINAL_PERSISTENT"
        }
        
        receipt = sys.sandbox_run("core/diagnostics_logger.py", "format_panel_output", "CONSOLE EXECUTION RECEIPT", meta, payload_data)
        
        # Adding a strict, padded newline separation isolates the code fence tags, 
        # completely preventing Open-WebUI from rendering empty ghost text frames!
        return f"{base_text}\n\n\n{receipt}"

    try:
        # --- COMMAND 1: HELP PANEL MANUAL ---
        if lowered_cmd in ["help", ""]:
            res = (
                "```text\n"
                "SYSTEM OVERRIDES MANUAL:\n"
                "- clear cache: Clears the module cache. Returns how many items were cleaned up\n"
                "- debug: Checks the active state of superglobal logging parameters\n"
                "- debug on/off: Toggles verbose frame output dictionary details globally\n"
                "- dress show: Returns active fit_check() diagnostics bypassing standard routers\n"
                "- dress set <body part> <clothing item>: Forces localized outfit alteration changes\n"
                "- dress clear: Shorthand loop to strip all current garment tracking metrics\n"
                "- show state: Returns a cleanly formatted version of neptune_current_state.json\n"
                "- character show: Returns information on the active profile variable layout\n"
                "- character set <name>: Hot-swaps the underlying character registry matrices\n"
                "- force state check/update/reset: Direct filesystem access mechanisms\n"
                "- force arousal <value>: Adjusts internal excitation parameters (0.0 to 1.6)\n"
                "```"
            )
            return _append_console_debug(res, "help_menu_query")

        # --- COMMAND 2: SHOW LIVE STATE TREE ---
                # --- COMMAND 2: SHOW LIVE STATE TREE (Duplication & Spacing Fixed) ---
        elif lowered_cmd == "show state" or lowered_cmd == "show status":
            if os.path.exists(state_path):
                with open(state_path, 'r', encoding='utf-8') as f:
                    parsed_json = json.load(f)
                formatted_state = json.dumps(parsed_json, indent=2)
                
                # Base communication message ends cleanly
                res = f"✨ \"Alright, pulling up our raw environment metrics right now, Boss! Here is the live state configuration tree:\n```json\n{formatted_state}\n```\""
                
                # Omit the third parameter to completely kill the duplicate dump below the receipt panel
                return _append_console_debug(res, "state_tree_dump")
                
            return f"```\n[ERROR]: neptune_current_state.json does not exist at {state_path}\n```"

        # --- COMMAND 3: SUPERGLOBAL DIAGNOSTICS SWITCHES ---
        elif lowered_cmd.startswith("debug"):
            sub_arg = cmd_body[5:].strip().lower()
            sg_path = f"{container_root}/repository/neptune_superglobals.json"

            if not sub_arg:
                live_debug_state = False
                if os.path.exists(sg_path):
                    try:
                        with open(sg_path, 'r', encoding='utf-8') as f:
                            sg_data = json.load(f)
                        live_debug_state = bool(sg_data.get("debug_verbosity", False))
                    except Exception:
                        pass
                current_status = "ACTIVE" if live_debug_state else "DISABLED"
                meta = {"SUPERGLOBAL_VERBOSE_STATUS": current_status}
                res = sys.sandbox_run("core/diagnostics_logger.py", "format_panel_output", "DIAGNOSTICS SYSTEM MONITOR", meta)
                return _append_console_debug(res, "debug_status_query")

            elif sub_arg == "on":
                sys.sandbox_run("core/diagnostics_logger.py", "toggle_debug_external", True)
                meta = {"SYSTEM_TRACING": "ENABLED", "LOG_LEVEL": "VERBOSE"}
                res = sys.sandbox_run("core/diagnostics_logger.py", "format_panel_output", "SUPERGLOBAL DIAGNOSTICS ACTIVATED", meta)
                return _append_console_debug(res, "debug_toggle_on")

            elif sub_arg == "off":
                sys.sandbox_run("core/diagnostics_logger.py", "toggle_debug_external", False)
                meta = {"SYSTEM_TRACING": "DISABLED", "LOG_LEVEL": "SILENT"}
                res = sys.sandbox_run("core/diagnostics_logger.py", "format_panel_output", "SUPERGLOBAL DIAGNOSTICS DEACTIVATED", meta)
                return _append_console_debug(res, "debug_toggle_off")

        # --- COMMAND 4: DRESS CONTROL MARGINS ---
        elif lowered_cmd.startswith("dress "):
            args = cmd_body[6:].strip()
            lowered_args = args.lower()
            
            if lowered_args == "show":
                fit_text = sys.sandbox_run("mind/inspector_utility.py", "NeptuneFitCheck.execute_fit_check", root_volume=container_root)
                res = f"📊 \"Pulling up my active equipment logs right now! Here is what my sensors see, Boss:\n\n{fit_text}\""
                return _append_console_debug(res, "wardrobe_fit_check", fit_text)
                
            elif lowered_args == "clear":
                fit_text = sys.sandbox_run("mind/inspector_utility.py", "NeptuneFitCheck.modify_clothing_state", container_root, "go_nude", "outfit")
                res = f"😳 \"Wh-aah! Every item cleared directly through terminal controls! Here is the updated scan log:\n\n{fit_text}\""
                return _append_console_debug(res, "wardrobe_purge_nude", fit_text)
                
            elif lowered_args.startswith("set "):
                set_params = args[4:].strip()
                parts = set_params.split(" ", 1)
                
                if len(parts) == 2:
                    body_slot = parts[0].lower()
                    garment_key = parts[1]
                    fit_text = sys.sandbox_run("mind/inspector_utility.py", "NeptuneFitCheck.modify_clothing_state", container_root, "put_on", body_slot, garment_key)
                    res = f"🔄 \"Altering slot **{body_slot}** to target item **{garment_key}**! Let's check the structural updates:\n\n{fit_text}\""
                    return _append_console_debug(res, f"wardrobe_slot_mutate_{body_slot}", fit_text)
                return "```\n[ERROR]: Syntax error. Correct usage: neptunectl dress set <body part> <clothing item>\n```"
        # --- COMMAND 5: CHARACTER PROFILE MANAGERS ---
        elif lowered_cmd.startswith("character "):
            args = cmd_body[10:].strip()
            lowered_args = args.lower()
            
            registry_path = f"{container_root}/repository/neptune_character_registry.json"
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry_data = json.load(f)

            if lowered_args == "show":
                with open(state_path, 'r', encoding='utf-8') as f:
                    state_json = json.load(f)
                active_char = state_json.get("active_character", "neptune_v1")
                char_metrics = registry_data.get(active_char, {})

                if not char_metrics:
                    return f"❌ \"Active variable tracking key is set to `{active_char}`, but it is missing from the database, Boss!\""

                info_panel = (
                    f"👤 **ACTIVE MATRIX PERSONA PROFILE** 👤\n"
                    f"- **Character Identifier:** `{active_char}`\n"
                    f"- **Default Outfit Slot:** `{char_metrics.get('default_outfit', 'naked')}`\n\n"
                    f"📝 **Dry Canvas Core Tags:**\n```text\n{char_metrics.get('dry', 'N/A')}\n```\n"
                    f"💦 **Wet Canvas Core Tags:**\n```text\n{char_metrics.get('wet', 'N/A')}\n```"
                )
                res = f"🎨 \"Pulling up our active model parameters right now, Boss! Here is who is currently handling runtime loops:\n\n{info_panel}\""
                return _append_console_debug(res, "character_profile_show", json.dumps(char_metrics))

            elif lowered_args.startswith("set "):
                target_char = args[4:].strip()
                if target_char not in registry_data:
                    available = ", ".join([f"`{k}`" for k in registry_data.keys()])
                    return f"❌ \"Character choice `{target_char}` doesn't exist inside registration files, Boss! Available nodes: {available}\""
                    
                with open(state_path, 'r', encoding='utf-8') as f:
                    state_json = json.load(f)
                state_json["active_character"] = target_char
                with open(state_path, 'w', encoding='utf-8') as f:
                    json.dump(state_json, f, indent=2)
                res = f"🎭 \"System override successful, Boss! Swapped our live character variable to **{target_char}**!\""
                return _append_console_debug(res, f"character_profile_mutate_{target_char}")
        # --- COMMAND 6: FORCE FACTORY STATE HOOKS ---
        elif lowered_cmd.startswith("force "):
            args = cmd_body[6:].strip()
            
            if args.lower() == "update":
                os.makedirs(repository_dir, exist_ok=True)
                default_state_tree = {
                    "appearance": {
                        "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                        "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
                        "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
                    },
                    "mood": {"arousal": 0.0, "status_effects": []}
                }
                with open(state_path, 'w', encoding='utf-8') as f:
                    json.dump(default_state_tree, f, indent=2)
                res = f"📁 \"Initialization complete, Boss! Forced default template directly out to `{state_path}`!\""
                return _append_console_debug(res, "force_factory_state_update")

            elif args.lower().startswith("arousal "):
                try:
                    val = float(args.lower().replace("arousal ", "").strip())
                    val = max(0.0, min(1.6, val))
                    with open(state_path, 'r', encoding='utf-8') as f:
                        state_json = json.load(f)
                    state_json["mood"]["arousal"] = val
                    with open(state_path, 'w', encoding='utf-8') as f:
                        json.dump(state_json, f, indent=2)
                    res = f"❤️ \"Internal arousal parameters forced directly to **{val}**! My thermal sensors are acting up, Boss!\""
                    return _append_console_debug(res, "force_arousal_mutate", f"Value forced: {val}")
                except Exception:
                    return "```\n[ERROR]: Invalid numeric float formatting or file missing.\n```"

            elif args.lower() == "state check":
                if os.path.exists(state_path):
                    with open(state_path, 'r', encoding='utf-8') as f:
                        file_data = f.read()
                    return _append_console_debug(f"```json\n{file_data}\n```", "force_state_check_query", file_data)
                return "```\n[ERROR]: file does not exist\n```"

        # --- FALLBACK LAYER: PARALLEL SSH KEY PASS TO REMOTE SHELL ---
        success, shell_result = sys.sandbox_run("mind/sysadmin/sysadmin_ssh_worker.py", "dispatch_remote_ssh_command", cmd_body)
        if success:
            res = f"📟 \"Command sent to the server cluster successfully, Boss! Here is what the terminal returned:\n```text\n{shell_result}\n```\""
            return _append_console_debug(res, "ssh_fallback_terminal_dispatch", shell_result)
        return f"❌ \"Gahh! Terminal command execution loop hit a socket failure, Boss:\n```text\n{shell_result}\n```\""

    except Exception as sys_err:
        error_stack = traceback.format_exc()
        meta = {"FAULT_LOCATION": "SYSADMIN_CORE", "TASK_CONTEXT": "OVERRIDE_COMMAND_EXECUTION", "CRASH_CLASS": type(sys_err).__name__, "ERROR_REASON": str(sys_err)}
        try:
            return sys.sandbox_run("core/diagnostics_logger.py", "format_panel_output", "CRITICAL CONSOLE EXCEPTION INTERCEPTED", meta, error_stack)
        except Exception:
            return f"```text\n[CRITICAL RUNTIME ERROR]: {str(sys_err)}\n{error_stack}\n```"
