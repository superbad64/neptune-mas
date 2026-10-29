import json

def _write_json(path: str, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def execute_debug(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Manages telemetry frame verbosity logging toggles dynamically."""
    if lowered_cmd == "debug":
        return f"📟 [DEBUG METRICS]: Superglobal logging status: `{state_data.get('debug_verbosity', True)}`"
    
    elif lowered_cmd == "debug on":
        state_data["debug_verbosity"] = True
        _write_json(state_path, state_data)
        return "📟 Verbose frame logging enabled globally."
        
    elif lowered_cmd == "debug off":
        state_data["debug_verbosity"] = False
        _write_json(state_path, state_data)
        return "📟 Verbose frame logging disabled globally."
        
    return "❌ Invalid debug directive. Use: `neptunectl debug`, `neptunectl debug on`, or `neptunectl debug off`"
