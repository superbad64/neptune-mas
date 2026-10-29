import json

def _write_json(path: str, data: dict):
    try:
        with open(path, 'w', encoding='utf-8') as f: 
            json.dump(data, f, indent=2)
    except Exception: 
        pass

def execute_wipe(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """Safely purges temporary session variables and resets arousal gauges back to zero."""
    try:
        # Reset internal arousal indices and clear active sensory modifiers
        state_data["mood"] = {"arousal": 0.0, "status_effects": []}
        state_data["self_arousal"] = 0.0
        
        # Sync the freshly scrubbed tree straight back down to disk storage
        _write_json(state_path, state_data)
        
        return "🧼 *[DATA PURGE SYNC]*: Temporary session variables scrubbed. Arousal state gauges and turn-counters reset to absolute zero baseline."
    except Exception as wipe_err:
        return f"❌ System Admin Error: Purge routine collapsed: {str(wipe_err)}"
