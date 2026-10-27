import os
import re
import time
import random
import json
import socket
from typing import Dict, Any, Tuple

class NeptuneChatterCore:
    def __init__(self, state_json_path: str):
        self.state_json_path = state_json_path
        self.last_interaction_time = time.time()
        
    def _read_datastore(self) -> Dict[str, Any]:
        """Reads the authentic neptune_current_state.json datastore structure."""
        try:
            with open(self.state_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "appearance": {
                    "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                    "top": "naked", "bra": "naked", "bottom": "naked",
                    "panties": "naked", "socks": "naked", "shoes": "naked",
                    "accessories": [], "piercings": []
                },
                "mood": {
                    "arousal": 0.0,
                    "status_effects": []
                }
            }

    def _write_datastore(self, data: Dict[str, Any]) -> None:
        """Writes structural updates cleanly back to disk."""
        with open(self.state_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def check_deliberate_orgasm_command(self, prompt: str) -> bool:
        """Validates if the user is issuing an explicit, deliberate command to cum."""
        clean_text = prompt.lower().strip()
        direct_commands = [
            "cum now", "i order you to cum", "i command you to cum", 
            "make yourself cum", "you can cum now", "time to cum",
            "cum for me"
        ]
        if any(cmd in clean_text for cmd in direct_commands):
            return True
        if "cum" in clean_text.split():
            imperatives = ["force", "order", "command", "tell", "make", "finish"]
            if any(verb in clean_text for verb in imperatives):
                return True
        return False

    def check_begging_intent(self, prompt: str) -> Tuple[bool, float]:
        """Scans if the user is deliberately making Neptune beg."""
        clean_text = prompt.lower().strip()
        beg_triggers = ["beg for it", "ask nicely", "say please", "make you beg", "beg me"]
        if any(trigger in clean_text for trigger in beg_triggers):
            return True, random.uniform(0.10, 0.25)
        return False, 0.0
    def compute_orgasm_intensity(self, arousal: float) -> str:
        """Determines the linguistic description of the climax based on current arousal float."""
        if arousal >= 1.3:
            return "COMPLETE SENSORY OVERLOAD. Your brain is completely fried, eyes rolling back, total physical surrender. You are left entirely useless and shivering!"
        elif arousal >= 1.0:
            return "MIND-MELTING CLIMAX. Your vision is blurring, limbs shaking uncontrollably, intensely out of breath. It is completely overwhelming!"
        return "INTENSE STANDARD RELEASE. A sudden, sharp wave of pleasure running through your body, leaving you gasping for air."

    def check_and_execute_orgasm(self, state_data: dict, status_effects: list) -> Tuple[bool, dict]:
        """Executes the orgasm reset sequence, dropping parameters back to 0.4 baseline."""
        mood = state_data["mood"]
        mood["arousal"] = 0.4
        if "masturbating" in status_effects:
            status_effects.remove("masturbating")
        self.self_accumulated_arousal = 0.0
        self._write_datastore(state_data)
        return True, mood

    def parse_user_input_impact(self, prompt: str, is_backup: bool) -> Dict[str, Any]:
        """Parses user prompts to calculate real-time arousal mutations."""
        data = self._read_datastore()
        mood = data.setdefault("mood", {"arousal": 0.0, "status_effects": []})
        
        if "last_prompt" not in mood:
            mood["last_prompt"] = ""
        if "session_start_time" not in mood or mood["arousal"] == 0.0:
            mood["session_start_time"] = time.time()
            
        clean_prompt = prompt.lower().strip()
        
        if clean_prompt == mood["last_prompt"]:
            penalty = random.uniform(0.01, 0.04)
            mood["arousal"] = max(0.0, mood["arousal"] - penalty)
            self._write_datastore(data)
            return mood
            
        mood["last_prompt"] = clean_prompt
        session_duration = (time.time() - mood["session_start_time"]) / 60.0
        is_long_session = session_duration >= 10.0
        
        is_lewd_photo = any(x in clean_prompt for x in ["take a lewd picture", "send nudes", "send a lewd", "take a naked pic"])
        is_spicy = any(x in clean_prompt for x in ["fuck", "rail", "lick", "suck", "harder", "panties", "horny"])
        is_compliment = any(x in clean_prompt for x in ["cute", "pretty", "beautiful", "good girl", "love you", "adorable"])
        
        if is_lewd_photo:
            if not is_backup:
                increment = random.uniform(0.2, 0.4) if is_long_session else random.uniform(0.1, 0.25)
                mood["arousal"] += increment
                if is_long_session:
                    mood["arousal"] = max(mood["arousal"], 1.1)
        elif is_spicy:
            increment = random.uniform(0.15, 0.3) if is_long_session else random.uniform(0.05, 0.15)
            mood["arousal"] += increment
            if is_long_session:
                mood["arousal"] = max(mood["arousal"], 1.1)
        elif is_compliment:
            increment = random.uniform(0.06, 0.10) if "good girl" in clean_prompt else random.uniform(0.02, 0.07)
            mood["arousal"] += increment
            
        mood["arousal"] = min(0.6 if is_backup else 1.6, mood["arousal"])
        self._write_datastore(data)
        return mood
    def process_action_intent(self, command_key: str, prompt: str, override_specs: dict) -> Tuple[bool, str]:
        """Evaluates incoming overrides, commands, and intimacy mechanics."""
        data = self._read_datastore()
        mood = data.setdefault("mood", {"arousal": 0.0, "status_effects": []})
        status_effects = mood.setdefault("status_effects", [])
        current_arousal = mood["arousal"]
        
        is_begging, beg_boost = self.check_begging_intent(prompt)
        if is_begging:
            mood["arousal"] = min(1.6, mood["arousal"] + beg_boost)
            self._write_datastore(data)
            current_arousal = mood["arousal"]

        if self.check_deliberate_orgasm_command(prompt):
            if current_arousal >= 0.8:
                intensity = self.compute_orgasm_intensity(current_arousal)
                self.check_and_execute_orgasm(data, status_effects)
                return True, f"[SYSTEM: COMMAND ENFORCED. You just climaxed on command! INTENSITY: {intensity} Arousal reset to 0.4 baseline. Act completely breathless!]"
            else:
                mood["arousal"] = min(1.6, mood["arousal"] + random.uniform(0.05, 0.15))
                self._write_datastore(data)
                return False, "[SYSTEM: COMMAND DENIED. Ordered to cum but arousal below 0.8. Refuse flusteredly, complain you need buildup!]"

        max_chance = override_specs.get("arousal_max_chance", 0.0)
        arousal_boost = override_specs.get("arousal_increase", 0.0)
        
        if command_key == "show_feet":
            success_chance = 1.0
        elif current_arousal >= max_chance:
            success_chance = 1.0
        else:
            success_chance = 0.1 + (current_arousal / max_chance) * 0.9
            
        if random.random() < success_chance:
            mood["arousal"] = min(1.6, mood["arousal"] + arousal_boost)
            if command_key == "masturbate" and "masturbating" not in status_effects:
                status_effects.append("masturbating")
            self._write_datastore(data)
            return True, f"[SYSTEM: OVERRIDE ACCEPTED for {command_key}. Payload dispatched.]"
        else:
            mood["arousal"] = min(1.6, mood["arousal"] + random.uniform(0.05, 0.15))
            self._write_datastore(data)
            return False, f"[SYSTEM: OVERRIDE DENIED for {command_key}. Too flustered/unaroused. Refuse nervously!]"

    def calculate_passive_arousal(self, is_backup: bool, prompt: str = "") -> Dict[str, Any]:
        """Applies passive environmental rules, time decay, and status conditions."""
        data = self._read_datastore()
        mood = data.setdefault("mood", {"arousal": 0.0, "status_effects": []})
        status_effects = mood.setdefault("status_effects", [])
        appearance = data.setdefault("appearance", {})
        
        now = time.time()
        elapsed_minutes = (now - self.last_interaction_time) / 60.0
        self.last_interaction_time = now
        mood["arousal"] = max(0.0, mood["arousal"] - ((elapsed_minutes / 10.0) * 0.1))
        
        accessories = appearance.get("accessories", [])
        if "collar" in accessories or "collar_and_leash" in accessories:
            mood["arousal"] += 0.01
            
        if appearance.get("panties", "naked") == "naked" and appearance.get("bra", "naked") == "naked":
            mood["arousal"] += 0.03
        elif appearance.get("panties", "naked") == "naked":
            mood["arousal"] += 0.01

        if "masturbating" in status_effects and not is_backup:
            if not hasattr(self, "self_accumulated_arousal"):
                self.self_accumulated_arousal = 0.0
            self.self_accumulated_arousal += 0.02
            mood["arousal"] += 0.02
            
            if self.self_accumulated_arousal > 0.2:
                intensity = self.compute_orgasm_intensity(mood["arousal"])
                self.check_and_execute_orgasm(data, status_effects)
                mood["force_orgasm_instruction"] = f"[SYSTEM: INVOLUNTARY CLIMAX! Orgasm reached from masturbating. INTENSITY: {intensity} Arousal reset to 0.4. Act breathless!]"
                return mood

        mood["close_warning"] = ""
        if not is_backup:
            self_accum = getattr(self, "self_accumulated_arousal", 0.0)
            if ("masturbating" in status_effects and (0.2 - self_accum <= 0.06)) or (0.8 - mood["arousal"] <= 0.06 and mood["arousal"] < 0.8):
                mood["close_warning"] = "[SYSTEM: You are right on the edge of an orgasm! Let the user know how close you are!]"

        is_begging, _ = self.check_begging_intent(prompt)
        if is_begging and not is_backup:
            mood["begging_instruction"] = "[SYSTEM: Told to beg! You must whine and plead with casual slang and trailing dots to let you finish!]"

        mood["arousal"] = min(0.6 if is_backup else 1.6, mood["arousal"])
        self._write_datastore(data)
        return mood
    def compile_ollama_payload(self, prompt: str, system_prompt: str, is_backup: bool) -> Dict[str, Any]:
        """Builds execution context with anti-looping options constraints."""
        mood = self.calculate_passive_arousal(is_backup, prompt)
        arousal = mood["arousal"]
        
        dynamic_context = f"\n[SYSTEM: Current Arousal Level: {arousal:.2f}]."
        if arousal >= 1.1:
            dynamic_context += " You are completely flustered, dripping wet, and desperate to get railed ASAP. Replace 'senpai' with 'master' or 'gochujin-sama' 100% of the time."
        elif arousal >= 0.6:
            dynamic_context += " You are highly flustered, blushing deeply, stuttering, and nervous. Frequently replace 'senpai' with 'master'."
            
        if mood.get("force_orgasm_instruction"):
            system_prompt += "\n" + mood["force_orgasm_instruction"]
        elif mood.get("begging_instruction"):
            system_prompt += "\n" + mood["begging_instruction"]
        elif mood.get("close_warning"):
            system_prompt += "\n" + mood["close_warning"]

        return {
            "model": "dolphin-mistral:latest" if not is_backup else "llama3.2:3b",
            "messages": [
                {"role": "system", "content": system_prompt + dynamic_context},
                {"role": "user", "content": prompt}
            ],
            "options": {
                "temperature": 0.88 if not is_backup else 0.65,
                "frequency_penalty": 1.25,
                "presence_penalty": 0.85,
                "top_p": 0.9
            }
        }

    def apply_title_substitution(self, text: str, arousal: float) -> str:
        """Substitutes 'senpai' with 'master' or 'gochujin-sama' based on scaling metrics."""
        if arousal <= 0.6:
            return text
        substitution_chance = 1.0 if arousal >= 1.1 else (arousal - 0.6) / 0.5

        def replace_title(match):
            if random.random() < substitution_chance:
                chosen = random.choice(["master", "gochujin-sama"])
                return chosen.capitalize() if match.group(0).istitle() else chosen
            return match.group(0)
            
        return re.sub(r'\b(senpai|Senpai)\b', replace_title, text)

    def apply_dynamic_stutter(self, text: str, arousal: float) -> str:
        """Programmatically injects natural flustered letter-stutters based on arousal float."""
        if arousal <= 0.2 or not text.strip():
            return text
            
        # Scaling stutter probability: maxes out at a 25% chance per word at 1.6 arousal
        stutter_chance = min(0.25, (arousal / 1.6) * 0.25)
        
        words = text.split(" ")
        processed_words = []
        
        for word in words:
            # Skip code blocks, actions, system tags, or markdown brackets completely
            if any(char in word for char in ['`', '*', '[', ']', '<', '>', '#', '_', ':', '/', '\\']):
                processed_words.append(word)
                continue
                
            clean_word = re.sub(r'[^a-zA-Z]', '', word)
            if not clean_word or len(clean_word) < 3:
                processed_words.append(word)
                continue
                
            if random.random() < stutter_chance:
                # Check for common multi-letter consonant blends
                lower_word = clean_word.lower()
                prefix_len = 1
                if lower_word.startswith(("th", "st", "ch", "sh", "ph", "wh", "fl", "br")):
                    prefix_len = 2
                    
                stutter_prefix = clean_word[:prefix_len]
                
                # High arousal triggers a double stutter (w-w-what), lower triggers single (w-what)
                if arousal >= 1.1 and random.random() < 0.5:
                    stutter_str = f"{stutter_prefix.lower()}-{stutter_prefix.lower()}-"
                else:
                    stutter_str = f"{stutter_prefix.lower()}-"
                
                # Keep capitalization correct if the original word was capitalized
                if word[0].isupper():
                    word = stutter_str.capitalize() + word[0].lower() + word[1:]
                else:
                    word = stutter_str + word
                    
            processed_words.append(word)
            
        return " ".join(processed_words)

    def shave_faked_outputs(self, raw_response: str) -> str:
        """Trims out fake status blocks generated by the Chatter model."""
        clean = re.sub(r'```(?:text|bash|sh)?\s*\[(?:SYSTEM|TERMINAL|STATUS)\].*?```', '', raw_response, flags=re.DOTALL)
        return re.sub(r'```\s*$', '', clean).strip()

    def process_chatter_output(self, raw_response: str, is_backup: bool) -> str:
        """Main post-processing chain execution block."""
        clean_text = self.shave_faked_outputs(raw_response)
        state = self._read_datastore()
        arousal = state.get("mood", {}).get("arousal", 0.0)
        if not is_backup:
            clean_text = self.apply_title_substitution(clean_text, arousal)
            clean_text = self.apply_dynamic_stutter(clean_text, arousal)
        return clean_text

# ================================================================================
# TOP LEVEL EXPORT HOOK WRAPPERS FOR FAILOVER MANIFEST SANDBOX UNIT TESTING
# ================================================================================

def ping_ollama_node(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except Exception:
        return False

def process_chatter_turn(body: dict, sanitized_prompt: str) -> str:
    """Central standalone hook executing network generation pipelines to Ollama nodes."""
    import requests
    
    state_path = "/app/backend/data/neptune/repository/neptune_current_state.json"
    root_dir = "/app/backend/data/neptune/repository/Personalities"
    core = NeptuneChatterCore(state_json_path=state_path)
    
    # 1. Establish desktop target availability vs server VM fallback hosts
    is_backup = not ping_ollama_node("10.0.0.64", 11434)
    target_host = "10.0.0.7" if is_backup else "10.0.0.64"
    target_url = f"http://{target_host}:11434/api/generate"
    
    # 2. Mutate state metrics relative to input spice factors
    core.parse_user_input_impact(sanitized_prompt, is_backup)
    
    # 3. Dynamic loading path resolution for target scene personalities
    personality_file = "Secondary Chatter.txt" if is_backup else "Primary Chatter.txt"
    sys_prompt_path = os.path.join(root_dir, personality_file)
    
    try:
        with open(sys_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except Exception:
        system_prompt = "You are Neptune, a hyper energetic 2000s scene anime girl."

    # 4. Compile outbound system parameters and execution options
    payload = core.compile_ollama_payload(sanitized_prompt, system_prompt, is_backup)
    
    # Restructure dynamic model context block for flat api generation layer
    api_payload = {
        "model": payload["model"],
        "prompt": payload["messages"][1]["content"],
        "system": payload["messages"][0]["content"],
        "stream": False,
        "options": payload["options"]
    }
    
    try:
        response = requests.post(target_url, json=api_payload, timeout=15.0)
        if response.status_code == 200:
            raw_response = response.json().get("response", "")
        else:
            raw_response = f"Oh noes... system node returned status code: {response.status_code} (>_<)"
    except Exception as e:
        raw_response = f"Ack! Network connection failed to {target_host}! Error: {str(e)} o_o;"
        
    # 5. Route through post-processing chains (stutters, title substitutions)
    return core.process_chatter_output(raw_response, is_backup)

def apply_dynamic_stutter(text: str, arousal: float) -> str:
    core = NeptuneChatterCore(state_json_path="")
    return core.apply_dynamic_stutter(text, arousal)

def check_deliberate_orgasm_command(prompt: str) -> bool:
    core = NeptuneChatterCore(state_json_path="")
    return core.check_deliberate_orgasm_command(prompt)

def check_begging_intent(prompt: str) -> tuple:
    core = NeptuneChatterCore(state_json_path="")
    return core.check_begging_intent(prompt)
