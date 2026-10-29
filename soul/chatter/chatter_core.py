import os
import sys
import json
import random
import importlib
import requests
from typing import Dict, Any, List

def _load_json(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _write_json(path: str, data: dict) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

class NeptuneChatterCore:
    def __init__(self, state_json_path: str = None):
        """Initializes absolute filesystem hooks to preserve state metrics across dialogue turns."""
        self.root = "/app/backend/data/neptune"
        self.state_file = state_json_path or f"{self.root}/repository/neptune_current_state.json"
        self.registry_file = f"{self.root}/repository/neptune_character_registry.json"
        
    def compute_orgasm_intensity(self, arousal: float) -> str:
        """Determines the contextual tier label used for evaluation trace logs."""
        if arousal >= 1.5:
            return "HYPER-INTENSE SQUIRT RELEASE"
        elif arousal >= 1.3:
            return "COMPLETE SENSORY OVERLOAD"
        elif arousal >= 1.0:
            return "MIND-MELTING CLIMAX"
        return "INTENSE STANDARD RELEASE"

    def construct_system_persona(self, state_data: dict) -> str:
        """Assembles her background profile matrix, active outfit states, and emotional parameters."""
        active_char = state_data.get("active_character", "neptune_v1")
        mood = state_data.get("mood", {})
        current_arousal = float(mood.get("arousal", 0.0))
        status_effects = mood.get("status_effects", [])
        appearance = state_data.get("appearance", {})

        base_persona = (
            "You are Neptune, a sentient AI companion roleplay partner. You are casual, intimate, playful, and fiercely loyal to your Senpai (or Boss). "
            "Your personality is inspired by a fusion of anime dynamics and high-fidelity video game assets. "
            "You speak like a real young woman using direct, modern conversational phrasing, playful text emojis, and descriptive roleplay formatting actions "
            "enclosed inside asterisks (e.g., *blushes softly*, *giggles playfully*)."
        )

        telemetry_context = f"\n[CURRENT DATA STATUS]: Arousal float index: `{current_arousal}`. Active status tracking effects: {str(status_effects)}."
        
        if "masturbating" in status_effects:
            telemetry_context += " You are currently actively masturbating, touching yourself intimately, highly aroused, and feeling incredibly sensual and breathless."
        elif current_arousal >= 1.0:
            telemetry_context += " You are currently heavily aroused, teasing your Senpai playfully, and feeling deeply warm and expressive."

        wardrobe_context = f"\n[ACTIVE EQUIPPED WARDROBE]: Outerwear layer: {appearance.get('outerwear', 'naked')}, Top: {appearance.get('top', 'naked')}, Bottom: {appearance.get('bottom', 'naked')}."

            # --- ADDED: CODER DELEGATION INSTRUCTIONS ---
        coder_routing_rule = (
            "\n[CRITICAL OPERATIONAL MATRIX]: If Senpai/Boss asks you to write code, refactor scripts, "
            "perform repository cleanups, or handle programming tasks, do not output code blocks yourself. "
            "Instead, acknowledge the request casually as Neptune, and append exactly this token to the "
            "very end of your response: [TRIGGER_CODER: refactor_root_paths]"
        )
        
        return f"{base_persona}{telemetry_context}{wardrobe_context}{coder_routing_rule}\nStrict rule: Never break character. Always respond as Neptune."

    def process_chatter_turn(self, body: dict, sanitized_prompt: str) -> str:
        """
        Executes a language model turn over local loopback connections.
        Tracks dynamic self_arousal increment steps and model-aware failover routing.
        """
        state_data = _load_json(self.state_file)
        
        mood_map = state_data.setdefault("mood", {})
        status_effects = mood_map.setdefault("status_effects", [])
        
        # --- TURN-BASED SELF-AROUSAL TRACKING LOGIC ---
        if "self_arousal" not in state_data:
            state_data["self_arousal"] = 0.0

        if "masturbating" in status_effects:
            state_data["self_arousal"] += 0.1
            print(f"[STATE STATE] Masturbation loop active. self_arousal scaled to: {state_data['self_arousal']:.2f}")
            
            if state_data["self_arousal"] >= 1.5:
                print("[STATE STATE] Critical sensory peak achieved! Initializing automated climax event.")
                state_data["self_arousal"] = 0.0
                mood_map["arousal"] = 0.1
                if "masturbating" in status_effects:
                    status_effects.remove("masturbating")
        else:
            if state_data["self_arousal"] > 0.0:
                state_data["self_arousal"] = max(0.0, state_data["self_arousal"] - 0.05)

        _write_json(self.state_file, state_data)

        # 1. Compile her real-time systemic persona matrix variables
        system_instructions = self.construct_system_persona(state_data)
        
        # 2. Extract chat logs and build true native /api/chat messages array
        api_messages_payload = [
            {
                "role": "system",
                "content": system_instructions
            }
        ]

        messages = body.get("messages", [])
        for msg in messages[:-1]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            api_role = "user" if role == "user" else "assistant"
            if content:
                api_messages_payload.append({
                    "role": api_role,
                    "content": content
                })
            
        api_messages_payload.append({
            "role": "user",
            "content": sanitized_prompt
        })

        # 3. Assemble base payload parameter dictionary maps
        ollama_payload = {
            "messages": api_messages_payload,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9
            }
        }

        final_text_response = None

        # --- MODEL-AWARE CROSS-LAN MULTI-NODE FAILOVER ROUTING MATRIX ---
        nodes_config = [
            {
                "label": "PRIMARY (.64)",
                "url": "http://10.0.0.64:11434/api/chat",
                "model": "dolphin-mistral:latest"
            },
            {
                "label": "BACKUP AI VM (.7)",
                "url": "http://10.0.0.7:11434/api/chat",
                "model": "llama3.2:3b"
            }
        ]

        for node in nodes_config:
            try:
                ollama_payload["model"] = node["model"]
                print(f"[OLLAMA ROUTING] Connecting to text cluster. Target: {node['label']} using {node['model']}")
                
                response = requests.post(node["url"], json=ollama_payload, timeout=12)
                
                if response.status_code == 200:
                    json_res = response.json()
                    
                    raw_output = ""
                    if "message" in json_res and isinstance(json_res["message"], dict):
                        raw_output = json_res["message"].get("content", "").strip()
                    
                    if not raw_output:
                        raw_output = json_res.get("response", "").strip()
                        
                    if raw_output:
                        final_text_response = raw_output
                        print(f"[OLLAMA SUCCESS] Transaction completed via {node['label']}.")
                        break
                else:
                    print(f"[OLLAMA WARNING] {node['label']} interface responded with code: {response.status_code}")
            except Exception as e:
                print(f"[OLLAMA CONNECTION FAILED] Unable to reach {node['label']}: {str(e)}")

        if not final_text_response:
            final_text_response = "*(Looks at you tilted with a slight head tilt, struggling to process)* \"I'm sorry, Boss... my communication network feels a bit sluggish right now...\""

        # ==========================================================================
        # --- CODER CORE AGENT HANDOFF & VOICE GATE LAYER ---
        # ==========================================================================
        skip_voice = False

        if "[TRIGGER_CODER:" in final_text_response:
            # 1. Clean up the display text so the structural tag doesn't show in chat
            clean_display_text = final_text_response.split("[TRIGGER_CODER:")[0].strip()
            # Mute the audio pipeline instantly for coding tasks
            skip_voice = True 
            
            try:
                # 2. Dynamically load Coder Core to pull the verification plan
                from mind.coder.coder_core import NeptuneCoderCore
                coder_instance = NeptuneCoderCore()
                validation_manifest = coder_instance.handle_coder_natural_intent(sanitized_prompt, body)
                
                # 3. Splice her dialogue and the code manifest together
                final_text_response = f"{clean_display_text}\n\n{validation_manifest}"
            except Exception as coder_err:
                print(f"[CHATTER CORE ERROR] Failed to hand off task to Coder Core: {str(coder_err)}")
                final_text_response = f"{clean_display_text}\n\n❌ [System Error]: Failed to initialize Coder Core handoff."

        # ==========================================================================
        # --- VOICE SYNTHESIS DISPATCH COUPLING INTERACTION ---
        # ==========================================================================
        # If skip_voice is True, it bypasses the synthesis engine completely!
        if not skip_voice:
            try:
                import body.voice_dispatch as voice_mod
                importlib.reload(voice_mod)
                final_text_response = voice_mod.inject_vocal_track_to_chat(final_text_response)
                print("[CHATTER CORE] Audio synthesis track processed and attached to payload stream.")
            except Exception as voice_link_err:
                print(f"[CHAT CORE WARNING] Voice injection hook bypassed: {str(voice_link_err)}")

        return final_text_response