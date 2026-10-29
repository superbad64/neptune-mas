def handle_operational_overrides(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """
    Dynamic Manifest Lookup Router.
    Parses neptune_commands_manifest.json to dispatch commands cleanly.
    """
    manifest_path = f"{root}/repository/neptune_commands_manifest.json"
    manifest = _load_json(manifest_path)
    commands_map = manifest.get("commands", {})

    # --- FIXED: SOLID RAW STRING SEPARATION KEYWORDS LIST ---
    # Safely isolate the very first word prefix string token without mutating the trailing body arguments
    parts = clean_prompt = cmd_body.strip().split(None, 1)
    if not parts:
        return "❌ Empty command string provided."
        
    trigger = parts[0].lower().strip()

    # Dynamic matching pass against the JSON manifest ledger
    if trigger in commands_map:
        cfg = commands_map[trigger]
        module_str = cfg.get("module")
        func_str = cfg.get("function")

        try:
            # Dynamically import the isolated handler script on demand
            handler_module = importlib.import_module(module_str)
            importlib.reload(handler_module)
            handler_func = getattr(handler_module, func_str)

            # --- FIXED: PASS CLEAN RAW ARGUMENTS DOWNSTREAM ---
            # Using cmd_body directly ensures your handlers slice clean strings 
            return handler_func(cmd_body, lowered_cmd, state_data, state_path, registry_path, root)
            
        except Exception as e:
            return f"❌ Dynamic Execution Error in handler `{module_str}`:\n```text\n{str(e)}\n```"

    return f"```\n[SYSADMIN ERROR]: Unrecognized dynamic manifest lookup key trigger: '{trigger}'\n```"
