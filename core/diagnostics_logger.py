import os
import sys
import json
import time
import traceback
from typing import Dict, Any, Optional

def _get_superglobals_path() -> str:
    """Returns the synchronized container path for the superglobals datastore."""
    return "/app/backend/data/neptune/repository/neptune_superglobals.json"

def _load_superglobals() -> Dict[str, Any]:
    """
    Loads or instantiates the flat neptune_superglobals JSON datastore file layout.
    Strictly reads and preserves existing disk parameters before defaulting.
    """
    sg_path = _get_superglobals_path()
    
    # Check if the file is already committed to the server partition array
    if os.path.exists(sg_path):
        try:
            with open(sg_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception:
            pass # Fall through to initialization if corruption occurs

    # ONLY generate defaults if the file is physically missing or unreadable
    default_state = {
        "debug_verbosity": False, # Enforce nominal silent defaults for fresh sessions
        "active_job_id": "idle",
        "system_warnings": []
    }
    try:
        os.makedirs(os.path.dirname(sg_path), exist_ok=True)
        with open(sg_path, 'w', encoding='utf-8') as f:
            json.dump(default_state, f, indent=2)
        return default_state
    except Exception:
        return {"debug_verbosity": False}
def check_debug_external() -> bool:
    """Immediate boolean lookup evaluating current verbose tracking states on disk."""
    sg = _load_superglobals()
    return bool(sg.get("debug_verbosity", False))

def toggle_debug_external(state_bool: bool) -> None:
    """Commits systemic debug tracking changes directly back into the superglobals file."""
    sg = _load_superglobals()
    sg["debug_verbosity"] = state_bool
    sg_path = _get_superglobals_path()
    try:
        with open(sg_path, 'w', encoding='utf-8') as f:
            json.dump(sg, f, indent=2)
    except Exception as e:
        print(f"[SUPERGLOBALS CRITICAL ERROR] Failed to write config update: {str(e)}")

def format_panel_output(header_title: str, metadata_dict: dict, raw_payload: Optional[str] = None) -> str:
    """Core Uniform Layout Factory. Wraps all technical diagnostics inside a neat box."""
    lines = [
        "```text",
        f"=== [{header_title.upper()}] ==="
    ]
    for key, val in metadata_dict.items():
        lines.append(f"• {key:<18}: {val}")
        
    if raw_payload:
        lines.append("-" * 50)
        lines.append(raw_payload.strip())
        
    lines.append("```")
    return "\n".join(lines)
def log_trace_external(module_name: str, execution_phase: str, payload_dump: Optional[Any] = None) -> None:
    """Outputs streamlined trace logs to container standard output registries."""
    if not check_debug_external():
        return

    meta = {
        "MODULE_NAME": module_name.upper(),
        "EXEC_PHASE": execution_phase,
        "TIMESTAMP": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    
    payload_str = None
    if payload_dump is not None:
        if isinstance(payload_dump, (dict, list)):
            payload_str = json.dumps(payload_dump, indent=2)
        else:
            payload_str = str(payload_dump)
            
    print(format_panel_output("DIAGNOSTIC TRACE", meta, payload_str))

def log_crash_external(module_name: str, action_context: str, exception_obj: Exception) -> str:
    """Captures un-truncated stack traces and bundles them inside our strict uniform panel template."""
    meta = {
        "FAULT_MODULE": module_name.upper(),
        "TASK_CONTEXT": action_context,
        "CRASH_CLASS": type(exception_obj).__name__,
        "ERROR_REASON": str(exception_obj)
    }
    error_stack = traceback.format_exc()
    return format_panel_output("CRITICAL RUNTIME EXCEPTION CAUGHT", meta, error_stack)

import re

class NeptuneSpiceClassifier:
    @staticmethod
    def classify_prompt_spice(prompt: str) -> str:
        """
        Analyzes the user's prompt lexical footprints to return a scannable
        spiciness rating visual anchor for the markdown debug interface panels.
        """
        clean_text = prompt.lower().strip()
        
        # Explicit/High-Arousal Triggers
        spicy_3 = ["fuck", "rail", "lick", "suck", "harder", "masturbate", "touch yourself", "finger", "cum", "orgasm"]
        # Suggestive/Override Triggers
        spicy_2 = ["tits", "breasts", "pussy", "crotch", "ass", "buttocks", "topless", "naked", "shower view"]
        # Light Compliments/Fit Checks
        spicy_1 = ["cute", "pretty", "beautiful", "good girl", "love you", "adorable", "fit check", "feet", "toes"]

        if any(w in clean_text for w in spicy_3):
            return "🌶️🌶️🌶️ [LEVEL 3: HYPER-SPICY]"
        elif any(w in clean_text for w in spicy_2):
            return "🌶️🌶️ [LEVEL 2: SUGGESTIVE]"
        elif any(w in clean_text for w in spicy_1):
            return "🌶️ [LEVEL 1: MILD]"
        
        return "[LEVEL 0: CLEAR]"

    def log_input_trace(self, prompt: str) -> str:
        """
        Generates pristine, noise-free Markdown panels for trace outputs
        with structural backtick boundaries to keep Open-WebUI stable.
        """
        spice_rating = self.classify_prompt_spice(prompt)
        
        markdown_panel = (
            f"\n\n```text\n"
            f"[NEPTUNECTL: LINGUISTIC INBOUND TRACE]\n"
            f"INPUT     -> \"{prompt}\"\n"
            f"SPICE RATING -> {spice_rating}\n"
            f"```\n\n"
        )
        return markdown_panel

# ================================================================================
# TOP LEVEL EXPORT HOOK WRAPPER FOR FAILOVER MANIFEST SANDBOX UNIT TESTING
# ================================================================================
def classify_prompt_spice(prompt: str) -> str:
    """Standalone wrapper proxy mapping dot-notation scopes to a flat dictionary key."""
    return NeptuneSpiceClassifier.classify_prompt_spice(prompt)