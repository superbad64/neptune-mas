import os
import sys
import json
import importlib
from typing import Dict, Any, Tuple, Optional


def flush_module_cache() -> int:
    """Clears cached multi-agent subsystem modules to guarantee clean disk reloads."""
    modules_to_clear = [
        mod
        for mod in list(sys.modules.keys())
        if any(
            mod.startswith(prefix) for prefix in ["mind.", "body.", "soul.", "core."]
        )
    ]
    for mod in modules_to_clear:
        del sys.modules[mod]
    return len(modules_to_clear)


class Pipe:
    def __init__(self):
        self.root = "/app/backend/data/neptune"

        # --- FIXED: Absolute path injection to preserve module tree on reboots ---
        if self.root not in sys.path:
            sys.path.insert(0, self.root)

        self.paths = {
            k: f"{self.root}/repository/neptune_{k}.json"
            for k in [
                "state",
                "overrides",
                "registry",
                "wardrobe",
                "photo_engine",
                "photo_overrides",
                "superglobals",
            ]
        }
        flush_module_cache()

    def _execute_custom_module(
        self, relative_script_path: str, function_name: str, *args, **kwargs
    ):
        full_path = os.path.join(self.root, relative_script_path)
        if not os.path.exists(full_path):
            return f"System Error: Script not found at {full_path}"

        dir_name = os.path.dirname(full_path)
        if dir_name not in sys.path:
            sys.path.insert(0, dir_name)

        try:
            module_notation = relative_script_path.replace("/", ".")
            if module_notation.endswith(".py"):
                module_notation = module_notation[:-3]
            module = importlib.import_module(module_notation)
            importlib.reload(module)

            if "." in function_name:
                class_name, method_name = function_name.split(".", 1)
                cls = getattr(module, class_name)

                if class_name == "NeptuneChatterCore":
                    state_file = self.paths.get("state")
                    instance = cls(state_json_path=state_file)
                else:
                    instance = cls()

                spice = getattr(module, "classify_prompt_spice", None)
                if spice and "prompt" in kwargs:
                    spice(kwargs["prompt"])

                return getattr(instance, method_name)(*args, **kwargs)

            return getattr(module, function_name)(*args, **kwargs)
        except Exception as e:
            # --- FIXED: EXTRACT THE DEEP NESTED SUB-MODULE CRASH TRACE ---
            if self.paths["superglobals"]["debug_verbose"]:
                tb = traceback.format_exc()
                return f"❌ ```\n[NEPTUNE SUB-MODULE SANDBOX CRASH DETECTED]\nScript: {relative_script_path} -> {function_name}\nError: {str(e)}\n\nFull Stack Traceback:\n{tb}\n```"
            else:
                return f"Neptune System Error inside sandbox execution: {str(e)}"

    def _get_exhaustive_slang_map(self) -> dict:
        return {
            "titties": "breasts",
            "tits": "breasts",
            "boobs": "breasts",
            "boobies": "breasts",
            "bazoongas": "breasts",
            "rack": "breasts",
            "chest": "breasts",
            "vagina": "pussy",
            "cunt": "pussy",
            "cooch": "pussy",
            "coochie": "pussy",
            "slit": "pussy",
            "ass": "butt",
            "booty": "butt",
            "tush": "butt",
            "bum": "butt",
            "snap": "picture",
            "pic": "picture",
            "pics": "pictures",
            "selfie": "picture",
            "selfies": "pictures",
            "photo": "picture",
            "photos": "pictures",
            "photograph": "picture",
            "shot": "picture",
            "vid": "video",
            "vids": "video",
            "clip": "video",
            "brb": "be right back",
            "idk": "i do not know",
            "dunno": "do not know",
            "gonna": "going to",
            "wanna": "want to",
            "gotta": "have to",
            "fr fr": "seriously",
            "no cap": "honestly",
            "imho": "in my honest opinion",
            "imo": "in my opinion",
            "tbh": "to be honest",
            "smh": "shaking my head",
            "omg": "oh my god",
            "irl": "in real life",
            "btw": "by the way",
            "afk": "away from keyboard",
            "jk": "just kidding",
            "nvm": "nevermind",
            "lmao": "laughing my ass off",
            "rofl": "rolling on the floor laughing",
            "wtf": "what the fuck",
            "wth": "what the hell",
            "u": "you",
            "r": "are",
            "ur": "your",
            "b4": "before",
            "cuz": "because",
            "cause": "because",
            "plz": "please",
            "pls": "please",
            "thx": "thanks",
            "ty": "thank you",
        }

    def translate_slang(self, text: str) -> str:
        slang_dictionary = self._get_exhaustive_slang_map()
        words = text.split()
        processed = []
        for word in words:
            clean = word.lower().strip(".,!?\"';:")
            if clean in slang_dictionary:
                substituted = slang_dictionary[clean]
                if word[-1] in [".", ",", "!", "?", ":", ";"]:
                    substituted += word[-1]
                processed.append(substituted)
            else:
                processed.append(word)
        return " ".join(processed)

    def pipe(self, body: dict) -> str:
        try:
            messages = body.get("messages", [])
            if not messages:
                return "╰(•̀ ── •́)╯ Error: Payload empty!"

            raw_prompt = messages[-1].get("content", "").strip()

            # --- STEP 1: Admin Command Intercept Layer ---
            if raw_prompt.lower().startswith("neptunectl"):
                return self._execute_custom_module(
                    "mind/sysadmin/sysadmin_core.py",
                    "handle_system_override",
                    raw_prompt=raw_prompt,
                )

            # --- STEP 2: Slang Translation Engine ---
            sanitized_prompt = self.translate_slang(raw_prompt)
            lowered_sanitized = sanitized_prompt.lower()

            # --- FIXED: REMOVE EMOTICONS & SYMBOLS FOR MATCH ALIGNMENT ---
            # Strips out casual symbols like :), :D, <3, or trailing punctuation marks completely
            clean_match_string = lowered_sanitized
            for symbol in [":)", ":d", "<3", ":p", ";)", ":(", "!", "?", ".", ",", "-"]:
                clean_match_string = clean_match_string.replace(symbol, "")
            clean_match_string = " ".join(clean_match_string.split()).strip()

            # --- STEP 3: High-Priority Photo Overrides Cross-Check ---
            is_imgen = False
            overrides_path = self.paths.get("photo_overrides")
            if os.path.exists(overrides_path):
                try:
                    with open(overrides_path, "r", encoding="utf-8") as f:
                        ov_data = json.load(f)

                    keyword_tuples = []
                    for item in ov_data.get("overrides", []):
                        for kw in item.get("trigger_keywords", []):
                            keyword_tuples.append((kw.lower().strip(), item))

                    keyword_tuples.sort(key=lambda x: len(x[0]), reverse=True)

                    for kw, item in keyword_tuples:
                        # Match against our clean_match_string instead of the raw dirty prompt
                        if kw in clean_match_string:
                            print(
                                f"[ROUTER INTERCEPT] Priority match achieved: {item['id']} via '{kw}'"
                            )
                            is_imgen = True
                            break
                except Exception as e:
                    print(
                        f"[ROUTER WARNING] Photo overrides parsing check failed: {str(e)}"
                    )

            # Fallback traditional keyword lookups
            if not is_imgen:
                imgen_keywords = ["picture", "image", "render", "photo", "look like"]
                is_imgen = any(kw in lowered_sanitized for kw in imgen_keywords)

            if is_imgen:
                return self._execute_custom_module(
                    "body/comfy_dispatch.py",
                    "evaluate_visual_intent",
                    prompt=lowered_sanitized,
                    raw_prompt=raw_prompt,
                )

            # --- STEP 4: Wardrobe Action Keyword Scans (Rule 3) ---
            wardrobe_keywords = [
                "wear",
                "put on",
                "take off",
                "remove",
                "change",
                "swap",
                "naked",
                "clothes",
                "outfit",
            ]
            if any(kw in lowered_sanitized for kw in wardrobe_keywords):
                return self._execute_custom_module(
                    "mind/inspector_utility.py",
                    "process_wardrobe_request",
                    prompt=lowered_sanitized,
                )

            # --- STEP 4.5: INTIMATE ORGASM CLIMAX OVERRIDES ---
            orgasm_triggers = ["cum now", "orgasm", "climax for me", "let it go"]
            if any(trigger in lowered_sanitized for trigger in orgasm_triggers):
                state_file = self.paths.get("state")
                try:
                    with open(state_file, "r", encoding="utf-8") as f:
                        s_data = json.load(f)

                    status_list = s_data.get("mood", {}).get("status_effects", [])
                    current_arousal = s_data.get("mood", {}).get("arousal", 0.0)

                    if "masturbating" not in status_list and current_arousal < 1.0:
                        return '🫣 "W-w-what?! I-I\'m not even close to something like that right now, senpai! *Blushes furiously* (Arousal level too low for climax event)"'

                    print(
                        "[ROUTER INTERCEPT] Climax event authorized. Triggering climax render loop."
                    )

                    # Update state metrics to handle post-climax crash parameters
                    s_data["mood"]["arousal"] = 0.1
                    # --- FIXED: ENSURE MANUAL ROUTER ORGASMS ZERO OUT SELF-AROUSAL ---
                    s_data["self_arousal"] = 0.0

                    if "masturbating" in s_data["mood"].get("status_effects", []):
                        s_data["mood"]["status_effects"].remove("masturbating")

                    with open(state_file, "w", encoding="utf-8") as f:
                        json.dump(s_data, f, indent=2)

                    # Forward directly to the generation engine to handle the portrait compilation
                    climax_prompt = (
                        "sensual portrait snapshot, explicit facial expression of intense climax ecstasy, "
                        "eyes rolled back slightly, flushed blushing cheeks, heavy breathing, open mouth, sweat glisten"
                    )
                    return self._execute_custom_module(
                        "body/comfy_dispatch.py",
                        "trigger_forced_generation",
                        raw_prompt=climax_prompt,
                    )
                except Exception as e:
                    if self.paths["superglobals"]["debug_verbose"]:
                        tb = traceback.format_exc()
                        return f"❌ ```\n[ROUTER ERROR]\nScript: {relative_script_path} -> {function_name}\nError: {str(e)}\n\nFull Stack Traceback:\n{tb}\n```"
                    else:
                        return f"[ROUTER ERROR] Climax intercept failed: {str(e)}"

            # --- STEP 5: Chatter Core Fallback Engine (Rule 4) ---
            return self._execute_custom_module(
                "soul/chatter/chatter_core.py",
                "NeptuneChatterCore.process_chatter_turn",
                body=body,
                sanitized_prompt=sanitized_prompt,
            )

        except Exception as e:
            if self.paths["superglobals"]["debug_verbose"]:
                tb = traceback.format_exc()
                return f"❌ ```\n[ROUTER ERROR]\nScript: {relative_script_path} -> {function_name}\nError: {str(e)}\n\nFull Stack Traceback:\n{tb}\n```"
            else:
                return f"╮(＞_＜)╭ Face Router crashed out! Error: {str(e)}"
