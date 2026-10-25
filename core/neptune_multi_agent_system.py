# =========================================================================
# THE FACE LAYER: OPEN-WEBUI SELF-CONTAINED FUNCTION PIPE INTERFACE
# Component Category: Front Gateway Integration Interface (neptune_multi_agent_system.py)
#
# Role in Neptune's Being:
# This wrapper handles the native interface registration handshake required by 
# Open-WebUI Functions. By adapting to the standard 'Pipe' framework class model,
# it intercepts user query streams and routes execution down across her Mind,
# Body, and Soul planes natively without external package cross-wiring issues.
# =========================================================================

import os
import sys
import re
import json
import random
import time
from pydantic import BaseModel, Field

# Mount the base system data directory volume paths
project_data_root = "/var/lib/docker/volumes/open-webui/_data"
if project_data_root not in sys.path:
    sys.path.insert(0, project_data_root)

class Valves(BaseModel):
    """FLATTENED OPEN-WEBUI VALVES CONFIGURATION SCHEMA OBJECT"""
    desktop_ollama_raw: str = Field(
        default="10.0.0.64", 
        description="Host cluster IP pointer allocation for ComfyUI and Primary Ollama nodes."
    )
    active_character_profile: str = Field(
        default="Neptune v1", 
        description="Active visual generation mesh template profile selection constraint."
    )

class Pipe:
    def __init__(self):
        # Register the local system valves data layer options configuration maps
        self.valves = Valves()

    def apply_slang_preprocessor_normalization(self, input_text: str) -> str:
        """
        STRICT HARD-MATCHING TOKEN NORMALIZER.
        Splits sentences by spaces and punctuation, asserting exact key matches
        to prevent substring or partial-word corruption on custom assets.
        """
        # Dictionary map for exact-word replacements
        slang_dictionary = {
            "fit": "outfit",
            "tits": "breasts",
            "pussy": "vagina",
            "coochie": "vagina",
            "booty": "buttocks",
            "ass": "buttocks",
            "pic": "picture",
            "snap": "picture"
        }
        
        # Use regex ONLY to isolate clean word boundaries and token pieces
        words = re.findall(r"[\w']+|[.,!?;:]", input_text)
        
        normalized_tokens = []
        for token in words:
            token_lower = token.lower()
            if token_lower in slang_dictionary:
                # Retain original capitalization properties if necessary, otherwise use hard replacement
                normalized_tokens.append(slang_dictionary[token_lower])
            else:
                normalized_tokens.append(token)
                
        # Reconstruct the sentence cleanly with proper spacing rules
        rebuilt_text = ""
        for token in normalized_tokens:
            if token in ".,!?;:":
                rebuilt_text = rebuilt_text.rstrip() + token + " "
            else:
                rebuilt_text += token + " "
                
        return rebuilt_text.strip()
    async def pipe(self, body: dict, __event_emitter__=None) -> str:
        """Master sequential orchestrator processing loop conduit thread."""
        messages = body.get("messages", [])
        if not messages:
            return "wahh senpai! Transmitted execution matrix container was empty down the pipe loop... :c"

        raw_user_query = messages[-1].get("content", "").strip()
        
        # 1. Hard-matching token normalization preprocessor pass execution
        normalized_query = self.apply_slang_preprocessor_normalization(raw_user_query)

        # Establish base networking addresses mapping properties
        raw_valve = str(self.valves.desktop_ollama_raw).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"

        # Load global system database state files from disk records
        from neptune.mind.sysadmin.sysadmin_core import load_neptune_state, save_neptune_state
        fallback_defaults = {
            "wardrobe": {
                "bra": "black_cotton_bra", "panties": "black_string", "socks": "black_thigh_highs", 
                "top": "white_crop_tank", "bottom": "tifa_skirt", "shoes": "tifa_boots",
                "accessories": ["tifa_gloves", "suspenders"], "jewelry": "teardrop_earrings", "outerwear": "naked"
            },
            "cosmetics": {"hair_style": "default_scene", "makeup": "default_makeup", "nails": "default_nails", "piercings": "default_piercings"},
            "performance": {"body_pose": "default_pose", "expression": "default_expression"},
            "environment": {"location": "inside my private room space", "wet_state": "dry"},
            "arousal": {"level": 0.0, "wetness": "dry", "nipples": "soft"},
            "meta": {"last_interaction_timestamp": 0.0}
        }
        current_state = await load_neptune_state(base_http, fallback_defaults)

        # =========================================================================
        # INTERCEPT 0: ADMINISTRATIVE SUPER-OVERRIDE CONTROL CONDUIT
        # =========================================================================
        if normalized_query.lower().startswith("sysadmin:"):
            admin_command = re.sub(r"^sysadmin:\s*", "", normalized_query, flags=re.IGNORECASE).strip()
            
            # Local high-priority short-circuit for memory flushes
            if any(phrase in admin_command for phrase in ["clear cache", "clear module cache", "flush cache", "reload modules"]):
                print("🧼 Super-Override: Evicting compiled modules from RAM...")
                for module in list(sys.modules.keys()):
                    if "neptune" in module: del sys.modules[module]
                return "### 🧼 SYSTEM SUPER-OVERRIDE REPORT\n\n*Administrative bypass executed successfully. Operational module caches have been forcefully evicted from RAM registers, senpai! 💕*"
            
            # LOCAL HIGH-PRIORITY SHORT-CIRCUIT FOR FORCE-EQUIPPING OUTFITS
            elif admin_command.startswith("dress "):
                target_outfit_key = admin_command.replace("dress ", "").strip().replace(" ", "_").lower()
                
                # FIXED: Standardized path strictly to Open-WebUI's internal container directory namespace
                manifest_path = "/app/backend/data/neptune/repository/neptune_wardrobe_manifest.json"
                try:
                    with open(manifest_path, 'r') as mf:
                        manifest = json.load(mf)
                    outfits_pool = manifest.get("outfits", {})
                except Exception as e:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Failed loading wardrobe manifest database file inside container: `{str(e)}`*"
                
                # Perform a defensive lookup across keys case-insensitively or via triggers list arrays
                matched_key = None
                for key, data in outfits_pool.items():
                    if key.lower() == target_outfit_key:
                        matched_key = key
                        break
                    triggers_list = data.get("triggers", [])
                    if any(t.lower().replace(" ", "_") == target_outfit_key for t in triggers_list):
                        matched_key = key
                        break
                
                if matched_key:
                    outfit_data = outfits_pool[matched_key]
                    items = outfit_data.get("items", outfit_data)
                    wardrobe = current_state.setdefault("wardrobe", {})
                    
                    wardrobe["top"] = items.get("top", items.get("tops", "naked"))
                    wardrobe["bottom"] = items.get("bottom", items.get("bottoms", "naked"))
                    wardrobe["bra"] = items.get("bra", items.get("bras", "naked"))
                    wardrobe["panties"] = items.get("panties", items.get("panties_layer", "naked"))
                    wardrobe["socks"] = items.get("socks", items.get("hosiery", "naked"))
                    wardrobe["shoes"] = items.get("shoes", items.get("boots", "naked"))
                    wardrobe["accessories"] = items.get("accessories", [])
                    wardrobe["outerwear"] = "naked"
                    
                    await save_neptune_state(base_http, current_state)
                    
                    from neptune.mind.inspector import evaluate_outfit_interception
                    _, structural_report = await evaluate_outfit_interception("outfit check", current_state)
                    return f"### 🔮 SYSTEM SUPER-OVERRIDE REPORT\n\n*Force-equipped target wardrobe footprint `{matched_key}` into system slots cleanly!*\n\n{structural_report}"
                else:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Outfit database lookup miss! Identifier `{target_outfit_key}` does not match any manifest keys or inner triggers. Core options: `{', '.join(outfits_pool.keys())}`*"

            # Forward any other trailing admin command down to the system tool terminal router
            else:
                try:
                    from neptune.mind.sysadmin.sysadmin_core import handle_sysadmin_terminal_routing
                    return await handle_sysadmin_terminal_routing(admin_command, current_state)
                except ImportError:
                    return f"### 🚨 SYSTEM SUPER-OVERRIDE FAULT\n\n*Bypass matched for command '{admin_command}', but backend terminal routing blocks are missing from `sysadmin_core.py`!*"

        # 2. Process biological emotional decay ticking loops
        from neptune.soul.mood_engine import process_emotional_decay_cycle
        current_state = await process_emotional_decay_cycle(current_state)

        # 3. Process cognitive Mind intercept checks (Wardrobe checks, modifications, visual overrides, reshoots)
        from neptune.mind.inspector import process_wardrobe_mutations_and_routing
        is_intercepted, output_payload_markdown = await process_wardrobe_mutations_and_routing(
            pipe_instance=self,
            raw_query=normalized_query,
            current_state=current_state
        )
        if is_intercepted:
            return output_payload_markdown

        # Process Standard User Cache-Flushing Engine Triggers
        cache_flush_phrases = ["clear cache", "clear module cache", "flush cache", "reload modules"]
        try:
            # FIXED: Standardized path strictly to Open-WebUI's internal container directory namespace
            triggers_path = "/app/backend/data/neptune/repository/neptune_interaction_triggers.json"
            with open(triggers_path, 'r') as tf: triggers = json.load(tf)
            sysadmin_phrases = triggers.get("sysadmin_triggers", ["run a command"])
        except Exception:
            sysadmin_phrases = ["run a command"]

        if any(phrase in normalized_query for phrase in cache_flush_phrases):
            for module in list(sys.modules.keys()):
                if "neptune" in module: del sys.modules[module]
            return "### 🧼 NEPTUNE SYSTEM ADMINISTRATIVE REPORT\n\n*Master memory registers and operational module caches have been successfully purged from RAM, senpai! Fresh disk source files reloaded completely. 💕*"

        if any(phrase in normalized_query for phrase in sysadmin_phrases):
            try:
                from neptune.mind.sysadmin.sysadmin_core import handle_sysadmin_terminal_routing
                return await handle_sysadmin_terminal_routing(normalized_query, current_state)
            except ImportError:
                return "### 🚨 NEPTUNE SYSTEM BLACKOUT\n\n*Wahh senpai! I intercepted the system command, but your terminal routing methods are missing from `sysadmin_core.py`!*"

        # 4. Standard conversational prompt processing routes (THE SOUL LAYER)
        from neptune.soul.chatter.chatter_core import prompt_conversational_core
        raw_model_reply = await prompt_conversational_core(
            pipe_instance=self,
            context_prompt=raw_user_query,
            chat_history=messages,
            current_state=current_state
        )

        # Run the state-of-undress text wrapper routing formatter
        from neptune.soul.dialog_router import route_conversational_flavor_injection
        final_conduit_delivery_text = await route_conversational_flavor_injection(
            pipe_instance=self,
            base_reply=raw_model_reply,
            current_state=current_state
        )

        # Commit state updates back to cache memory disk storage records
        await save_neptune_state(base_http, current_state)
        return final_conduit_delivery_text
