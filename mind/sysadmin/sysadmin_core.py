import os
import sys
import json
import importlib
from typing import Dict, Any

def _append_console_debug(base_res: str, transaction_id: str, context_details: str = "") -> str:
    """Handles dynamic panel logging via native importlib hooks, preventing sys errors."""
    container_root = "/app/backend/data/neptune"
    state_file = f"{container_root}/repository/neptune_current_state.json"
    debug_active = True
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                debug_active = json.load(f).get("debug_verbosity", True)
        except Exception: 
            pass
    if not debug_active: 
        return base_res
        
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
            with open(path, 'r', encoding='utf-8') as f: 
                return json.load(f)
        except Exception: 
            pass
    return {}

def handle_system_override(raw_prompt: str) -> str:
    """
    Pure Administrative Gateway Interface Proxy.
    Strips the console hook string and pushes everything straight to the dynamic manifest ops router.
    """
    container_root = "/app/backend/data/neptune"
    state_path = f"{container_root}/repository/neptune_current_state.json"
    registry_path = f"{container_root}/repository/neptune_character_registry.json"

    # Verify signature format before spinning up execution runtimes
    if not raw_prompt.strip().lower().startswith("neptunectl"):
        return None

    # Strip out the 'neptunectl' prefix to capture the raw instruction arguments
    cmd_body = raw_prompt.replace("neptunectl", "", 1).strip()
    lowered_cmd = cmd_body.lower()
    state_data = _load_json_file(state_path)

    # --- UNIFIED PIPELINE FORWARDER ---
    # Handshake with your dynamic JSON manifest tracker loop
    try:
        ops_module = importlib.import_module("mind.sysadmin.sysadmin_ops")
        importlib.reload(ops_module)
        
        # Fire operational handshake pass completely down into your decoupled files
        receipt = getattr(ops_module, "handle_operational_overrides")(cmd_body, lowered_cmd, state_data, state_path, registry_path, container_root)
        
        # Extract the command keyword safely for debugging output logs
        cmd_token = lowered_cmd.split()[0] if lowered_cmd.split() else "unknown"
        return _append_console_debug(receipt, f"{cmd_token}_manifest_router_execute")
        
    except Exception as e: 
        return f"❌ Critical Administrative Manifest Forwarder Exception Error: {str(e)}"
