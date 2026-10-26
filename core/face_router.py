import os
import sys
import json
import traceback
from typing import Dict, Any, List

# --- BOOTSTRAP ANCHOR ELEMENT ---
# Explicitly inject the absolute container base path if it isn't tracked yet
CONTAINER_BASE_PATH = "/app/backend/data/neptune"
if CONTAINER_BASE_PATH not in sys.path:
    sys.path.insert(0, CONTAINER_BASE_PATH)

class Pipe:
    def __init__(self):
        # Anchor immutable database folder targets securely
        self.root = "/app/backend/neptune"
        self.paths = {
            "state": f"{self.root}/repository/neptune_current_state.json",
            "overrides": f"{self.root}/repository/neptune_system_overrides.json",
            "registry": f"{self.root}/repository/neptune_character_registry.json",
            "wardrobe": f"{self.root}/repository/neptune_wardrobe_manifest.json",
            "photo_engine": f"{self.root}/repository/neptune_photo_engine.json",
            "photo_overrides": f"{self.root}/repository/neptune_photo_overrides.json"
        }
        
        self.slang_map = {
            "titties": "breasts",
            "boobs": "breasts",
            "pussy": "pussy",
            "snap": "picture",
            "pic": "picture",
            "selfie": "selfie",
            "brb": "be right back",
            "idk": "i do not know",
            "gonna": "going to",
            "dunno": "do not know",
            "wanna": "want to",
            "fr fr": "seriously",
            "no cap": "honestly"
        }

    def _load_datastore(self, key: str) -> dict:
        """Reads database matrices cleanly without modifying files."""
        path = self.paths.get(key)
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def translate_slang(self, text: str) -> str:
        """Step 1 Global Preprocessor text standardizer."""
        words = text.split()
        processed = []
        for word in words:
            clean = word.lower().strip(".,!?\"';:")
            if clean in self.slang_map:
                substituted = self.slang_map[clean]
                if word[-1] in [".", ",", "!", "?", ":", ";"]:
                    substituted += word[-1]
                processed.append(substituted)
            else:
                processed.append(word)
        return " ".join(processed)

    def pipe(self, body: dict) -> str:
        """
        Main Open-WebUI entrance controller. Programmatically searches internal
        sys.path packages cleanly now that path bindings are secured.
        """
        try:
            messages = body.get("messages", [])
            if not messages:
                return "System Error: Face interface received an empty payload stream."

            raw_prompt = messages[-1].get("content", "").strip()

            # --- RULE 1: Immediate Admin Intercept Check ---
            if raw_prompt.lower().startswith("sysadmin:"):
                print("[THE FACE] Administrative command prefix caught. Routing to Sysadmin Core.")
                # Python now cleanly resolves mind.* imports perfectly!
                from mind.sysadmin.sysadmin_core import handle_system_override
                return handle_system_override(raw_prompt)

            # Step 1 Pipeline Pass: Normalize the incoming input string
            sanitized_prompt = self.translate_slang(raw_prompt)
            lowered_sanitized = sanitized_prompt.lower()

            # --- RULE 2: Photo Scenario Overrides Lookup ---
            photo_overrides = self._load_datastore("photo_overrides")
            for scenario_key, scenario_data in photo_overrides.get("scenarios", {}).items():
                trigger_phrases = scenario_data.get("triggers", [])
                if any(trigger.lower() in lowered_sanitized for trigger in trigger_phrases):
                    print(f"[THE FACE] Hard lookup match hit on scenario override: {scenario_key}")
                    from body.pipeline_compiler import execute_override_render
                    return execute_override_render(scenario_key, sanitized_prompt)

            # --- RULE 3: Regular Image Generation Keywords Lookup ---
            image_keywords = ["picture", "selfie", "snap", "photo", "look like"]
            if any(keyword in lowered_sanitized for keyword in image_keywords):
                print("[THE FACE] Hard lookup match hit on regular image terminology checklist.")
                from body.pipeline_compiler import compile_fresh_image_generation
                return compile_fresh_image_generation(sanitized_prompt)

            # --- RULE 4: Chat Loop Fallback (The Soul Layer) ---
            print("[THE FACE] No image indicators matched. Passing control to Dynamic Chat Cores.")
            from soul.chatter.chatter_core import process_chatter_turn
            return process_chatter_turn(body, sanitized_prompt)

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"[FATAL FACE ROUTER CRASH] Stack trace:\n{error_trace}")
            return f"Neptune Face Router encountered a critical execution block: {str(e)}"
