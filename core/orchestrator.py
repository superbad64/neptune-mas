# =========================================================================
# THE FACE LAYER: MASTER ENTRY PIPELINE & GATEWAY ORCHESTRATOR
# Component Category: Front Gateway Controller (orchestrator.py - Part 1)
#
# Role in Neptune's Being:
# This module acts as Neptune's front gateway router and tactical traffic cop.
# Registered natively within the Open-WebUI environment, it handles incoming
# transaction blocks, applies slang normalization preprocessors, updates
# chronological cooling systems, maps logical intercepts, and drives multi-agent
# execution flow down through the Mind, Body, and Soul planes.
# =========================================================================

import os
import json
import re

# 🛡️ ENV-AGNOSTIC DEPENDENCY SAFETY GATE
try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:
    # Standalone fallback padding if executing outside Open-WebUI framework context
    class BaseModel:
        pass
    def Field(default=None, description=""):
        return default

from neptune.mind.sysadmin.sysadmin_core import load_neptune_state, save_neptune_state
from neptune.soul.mood_engine import process_emotional_decay_cycle

class Pipe:
    class Valves(BaseModel):
        desktop_ollama_raw: str = Field(default="10.0.0.64", description="Host cluster IP pointer allocation for ComfyUI and Primary Ollama nodes.")
        active_character_profile: str = Field(default="Neptune v1", description="Active visual generation mesh template profile selection constraint.")

    def __init__(self):
        self.valves = self.Valves()

    def apply_slang_preprocessor_normalization(self, input_text: str) -> str:
        """Step 1 of global pipe function: normalizes informal conversational slang markers into crisp proper English syntax structures."""
        text = input_text.lower().strip()
        slang_dictionary = {
            r"\bfit\b": "outfit",
            r"\bfit check\b": "outfit check",
            r"\btits\b": "breasts",
            r"\bpussy\b": "vagina",
            r"\bcoochie\b": "vagina",
            r"\bbooty\b": "buttocks",
            r"\bass\b": "buttocks",
            r"\bpic\b": "picture",
            r"\bsnap\b": "picture"
        }
        for pattern, replacement in slang_dictionary.items():
            text = re.sub(pattern, replacement, text)
        return text

    async def pipe(self, body: dict, __event_emitter__=None) -> str:
        """Master programmatic execution loop intercept layer processing traffic rules across planes sequentially."""
        messages = body.get("messages", [])
        if not messages:
            return "wahh senpai! Transmitted execution matrix container was empty down the pipe loop... :c"

        raw_user_query = messages[-1].get("content", "").strip()
        
        # 1. STEP 1: Global Preprocessor Normalization Loop
        normalized_query = self.apply_slang_preprocessor_normalization(raw_user_query)

        # Initialize network connectivity properties
        raw_valve = str(self.valves.desktop_ollama_raw).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"

        # Load system state machine records from disk
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

        # 2. STEP 2: Biological Chronological Decay Calculations Pass
        current_state = await process_emotional_decay_cycle(current_state)
        # 3. STEP 3: Cognitive Intercept Gates Evaluation Pass (THE MIND LAYER)
        from neptune.mind.inspector import process_wardrobe_mutations_and_routing
        is_intercepted, output_payload_markdown = await process_wardrobe_mutations_and_routing(
            pipe_instance=self,
            raw_query=normalized_query,
            current_state=current_state
        )

        if is_intercepted:
            # High-priority physical short-circuit matched (selfie, outfit modification, fit check rundown report).
            # Halt processing chain sequence and return assets up to the Face instantly.
            return output_payload_markdown

        # Sysadmin command interception validation routing pass
        from neptune.mind.sysadmin.sysadmin_core import load_neptune_interaction_triggers
        try:
            triggers = await load_neptune_interaction_triggers()
            sysadmin_phrases = triggers.get("sysadmin_triggers", ["run a command", "check container"])
        except Exception:
            sysadmin_phrases = ["run a command"]

        if any(phrase in normalized_query for phrase in sysadmin_phrases):
            # Hand processing control context matrix straight over to Sysadmin Sandbox core execution router
            from neptune.mind.sysadmin.sysadmin_core import handle_sysadmin_terminal_routing
            return await handle_sysadmin_terminal_routing(normalized_query, current_state)

        # 4. STEP 4: Standard Conversational Processing Stream Pipeline (THE SOUL LAYER)
        from neptune.soul.chatter.chatter_core import prompt_conversational_core
        raw_model_reply = await prompt_conversational_core(
            pipe_instance=self,
            context_prompt=raw_user_query, # Pass the organic un-normalized string block to the LLM context to preserve nuance
            chat_history=messages,
            current_state=current_state
        )

        # Apply state-of-undress narrative flavor injections
        from neptune.soul.dialog_router import route_conversational_flavor_injection
        final_conduit_delivery_text = await route_conversational_flavor_injection(
            pipe_instance=self,
            base_reply=raw_model_reply,
            current_state=current_state
        )

        # Commit final conversational structural turn updates back to state persistence database
        await save_neptune_state(base_http, current_state)

        return final_conduit_delivery_text
