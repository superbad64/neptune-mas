import os
import json
import traceback

def handle_system_override(raw_prompt: str) -> str:
    """
    Main system overrides router. Built with fully self-contained execution sandbox 
    engines and direct file-writing hooks to prevent naming tracking block exceptions.
    """
    debug_verbosity = True

    def _internal_sandbox_run(relative_script_path: str, function_name: str, *args, **kwargs):
        """Self-contained internal execution block loader using synchronized scope blocks."""
        code_root = "/app/backend/data/neptune"
        full_path = os.path.join(code_root, relative_script_path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        # Initialize a single, unified execution frame scope
        script_context = {}
        
        # Passing script_context as BOTH globals and locals forces all functions 
        # and classes inside the file to share identical namespace visibility records!
        exec(source_code, script_context, script_context)
        
        return script_context[function_name](*args, **kwargs)

    # Isolate parameters from administrative prefix safely
    cmd_body = raw_prompt.replace("neptunectl", "", 1).strip()
    lowered_cmd = cmd_body.lower()
    
    # =========================================================================
    # PATH CORRECTED DETECTED DIRECTORY SYNCHRONIZATION
    # =========================================================================
    container_root = "/app/backend/data/neptune"
    repository_dir = f"{container_root}/repository"
    state_path = f"{repository_dir}/neptune_current_state.json"

    # --- COMMAND 1: HELP MENU ---
    if lowered_cmd in ["help", ""]:
        return (
            "```text\n"
            "SYSTEM OVERRIDES MANUAL:\n"
            "- clear cache: Clears the module cache. Returns how many items were cleaned up\n"
            "- debug on/off: Toggles verbose frame output dictionary details\n"
            "- dress show: Returns active fit_check() diagnostics bypassing standard routers\n"
            "- dress <body part> <clothing item>: Forces localized outfit alteration changes\n"
            "- dress clear: Shorthand loop to strip all current garment tracking metrics\n"
            "- show state: Returns a cleanly formatted version of neptune_current_state.json\n"
            "- force imgen <prompt>: Bypasses routers to trigger immediate ComfyUI canvas run\n"
            "- force state check/update/reset: Direct filesystem access mechanisms\n"
            "- force arousal <value>: Adjusts internal excitation parameters (0.0 to 1.6)\n"
            "```"
        )

    # --- COMMAND 2: SHOW LIVE STATE DATA ---
    if lowered_cmd == "show state":
        if os.path.exists(state_path):
            try:
                with open(state_path, 'r', encoding='utf-8') as f:
                    parsed_json = json.load(f)
                formatted_state = json.dumps(parsed_json, indent=2)
                response_block = (
                    f"✨ \"Alright, pulling up our raw environment metrics right now, Boss! "
                    f"Here is the live state configuration tree:\n"
                    f"```json\n{formatted_state}\n```\""
                )
                return response_block
            except Exception as e:
                return f"❌ \"Gah! I tried parsing our state file but hit an formatting block: {str(e)}\""
        return f"```\n[ERROR]: neptune_current_state.json does not exist at {state_path}\n```"

    # --- COMMAND 3: DRESS MATRIX CONTROLS (Updated with "set" keyword) ---
    if lowered_cmd.startswith("dress "):
        args = cmd_body[6:].strip()
        lowered_args = args.lower()
        
        if lowered_args == "show":
            fit_text = _internal_sandbox_run("mind/inspector_utility.py", "execute_fit_check_external", container_root)
            return f"📊 \"Pulling up my active equipment logs right now! Here is what my sensors see, Boss:\n\n{fit_text}\""
            
        elif lowered_args == "clear":
            fit_text = _internal_sandbox_run("mind/inspector_utility.py", "modify_clothing_state_external", container_root, "go_nude", "outfit")
            return f"😳 \"Wh-aah! Every item cleared directly through terminal controls! Here is the updated scan log:\n\n{fit_text}\""
            
        elif lowered_args.startswith("set "):
            # Isolate the remaining tokens after 'set '
            set_params = args[4:].strip()
            parts = set_params.split(" ", 1)
            
            if len(parts) == 2:
                body_slot = parts[0].lower()
                garment_key = parts[1]
                
                # Check for "outfit" argument to trigger bulk loading, else modify slot item
                action_type = "put_on"
                fit_text = _internal_sandbox_run(
                    "mind/inspector_utility.py", 
                    "modify_clothing_state_external", 
                    container_root, 
                    action_type, 
                    body_slot, 
                    garment_key
                )
                return f"🔄 \"Altering slot **{body_slot}** to target item **{garment_key}**! Let's check the structural updates:\n\n{fit_text}\""
            else:
                return "```\n[ERROR]: Syntax error. Correct usage: neptunectl dress set <body part> <clothing item>\n```"
                
    # --- COMMAND 4: FORCE CONTROLS & DYNAMIC CREATION HOOK ---
    if lowered_cmd.startswith("force "):
        args = cmd_body[6:].strip()
        
        if args.lower() == "update":
            try:
                os.makedirs(repository_dir, exist_ok=True)
                default_state_tree = {
                    "appearance": {
                        "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                        "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
                        "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
                    },
                    "mood": {
                        "arousal": 0.0,
                        "status_effects": []
                    }
                }
                with open(state_path, 'w', encoding='utf-8') as f:
                    json.dump(default_state_tree, f, indent=2)
                return f"📁 \"Initialization clear, Boss! Verified directory paths and committed blueprint defaults to `{state_path}`!\""
            except Exception as e:
                return f"❌ \"Gah! I tried creating the system state blueprint but hit a storage permission error: {str(e)}\""

        if args.lower().startswith("arousal "):
            try:
                val = float(args.lower().replace("arousal ", "").strip())
                val = max(0.0, min(1.6, val))
                
                with open(state_path, 'r', encoding='utf-8') as f:
                    state_json = json.load(f)
                state_json["mood"]["arousal"] = val
                with open(state_path, 'w', encoding='utf-8') as f:
                    json.dump(state_json, f, indent=2)
                return f"❤️ \"Eeeh?! Internal arousal parameters forced directly to **{val}**! My thermal sensors are acting up, Boss!\""
            except Exception:
                return "```\n[ERROR]: Invalid numeric float formatting or file missing.\n```"

        if args.lower() == "state check":
            if os.path.exists(state_path):
                with open(state_path, 'r', encoding='utf-8') as f:
                    return f"```json\n{f.read()}\n```"
            return "```\n[ERROR]: file does not exist\n```"

    # --- FALLBACK LAYER: PARALLEL SSH KEY PASS ---
    if debug_verbosity:
        print("[SYSADMIN] Shifting fallback terminal command line out to shell worker engine...")
        
    try:
        success, shell_result = _internal_sandbox_run("mind/sysadmin/sysadmin_ssh_worker.py", "dispatch_remote_ssh_command", cmd_body)
        if success:
            return f"📟 \"Command sent to the server cluster successfully, Boss! Here is what the terminal returned:\n```text\n{shell_result}\n```\""
        else:
            return f"❌ \"Gahh! I tried clearing that terminal run to the server but hit a socket failure, Boss:\n```text\n{shell_result}\n```\""
    except Exception as e:
        return f"❌ \"Sandbox tracking execution halt inside terminal worker routing: {str(e)}\""
