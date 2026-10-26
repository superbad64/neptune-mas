import os
import sys
import json
import traceback


class Pipe:
    def __init__(self):
        self.root = "/app/backend/neptune"
        self.code_root = "/app/backend/data/neptune"

        self.paths = {
            "state": f"{self.root}/repository/neptune_current_state.json",
            "overrides": f"{self.root}/repository/neptune_system_overrides.json",
            "registry": f"{self.root}/repository/neptune_character_registry.json",
            "wardrobe": f"{self.root}/repository/neptune_wardrobe_manifest.json",
            "photo_engine": f"{self.root}/repository/neptune_photo_engine.json",
            "photo_overrides": f"{self.root}/repository/neptune_photo_overrides.json",
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
            "no cap": "honestly",
        }

        sys.sandbox_run = self._execute_custom_module

    def _execute_custom_module(
        self, relative_script_path: str, function_name: str, *args, **kwargs
    ):
        """Master Sandbox Runner. Reads scripts fresh from disk arrays."""
        import requests

        full_script_path = os.path.join(self.code_root, relative_script_path)
        if not os.path.exists(full_script_path):
            return f"System Error: Script not found on disk array layout at {full_script_path}"

        with open(full_script_path, "r", encoding="utf-8") as f:
            script_source = f.read()

        try:
            unified_context = {
                "__builtins__": __builtins__,
                "os": os,
                "json": json,
                "sys": sys,
                "traceback": traceback,
                "requests": requests,
            }
            exec(script_source, unified_context, unified_context)

            if "." in function_name:
                class_name, method_name = function_name.split(".", 1)
                if class_name not in unified_context:
                    return f"System Error: Class '{class_name}' was not found on the memory sheet."
                init_volume = kwargs.pop("root_volume", None) or kwargs.pop(
                    "container_root", None
                )
                method_args = list(args)
                if (
                    not init_volume
                    and method_args
                    and isinstance(method_args[0], str)
                    and method_args[0].startswith("/app")
                ):
                    init_volume = method_args.pop(0)
                class_instance = (
                    unified_context[class_name](root_volume=init_volume)
                    if init_volume
                    else unified_context[class_name]()
                )
                target_method = getattr(class_instance, method_name, None)
                if not target_method:
                    return f"System Error: Method '{method_name}' not found on Class '{class_name}'."
                return target_method(*method_args, **kwargs)

            if function_name in unified_context:
                return unified_context[function_name](*args, **kwargs)
            return f"System Error: Target entrypoint '{function_name}' was not found on the memory sheet."
        except Exception as e:
            return f"Neptune System Error inside sandbox execution: {str(e)}"

    def _load_datastore(self, key: str) -> dict:
        """Reads database matrices cleanly without modifying files."""
        path = self.paths.get(key)
        if not path or not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
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

    def _append_routing_receipt(
        self, base_res: str, target: str, reason: str, tokens: list
    ) -> str:
        """Appends our clean uniform receipt block if debug_verbosity is enabled."""
        try:
            debug_active = sys.sandbox_run(
                "core/diagnostics_logger.py", "check_debug_external"
            )
        except Exception:
            debug_active = True

        if not debug_active:
            return base_res

        meta = {
            "ROUTING_TARGET": target.upper(),
            "MATCH_REASON": reason,
            "EVAL_TOKENS": json.dumps(tokens),
        }
        receipt_panel = sys.sandbox_run(
            "core/diagnostics_logger.py",
            "format_panel_output",
            "FACE ROUTER ACTION RECEIPT",
            meta,
        )
        return f"{base_res}\n\n{receipt_panel}"

    def pipe(self, body: dict) -> str:
        """Main entrance controller router loop with organic keyword intent interception."""
        try:
            messages = body.get("messages", [])
            if not messages:
                return "System Error: Face interface received an empty payload stream."

            raw_prompt = messages[-1].get("content", "").strip()

            # --- RULE 1: Immediate Admin Intercept Check ---
            if raw_prompt.lower().startswith("neptunectl"):
                return self._execute_custom_module(
                    relative_script_path="mind/sysadmin/sysadmin_core.py",
                    function_name="handle_system_override",
                    raw_prompt=raw_prompt
                )

            # Step 1 Pipeline Pass: Normalize the incoming input string
            sanitized_prompt = self.translate_slang(raw_prompt)
            lowered_sanitized = sanitized_prompt.lower()

            # --- RULE 1.5: ORGANIC WARDROBE INTENT INTERCEPTOR (Trigger-Array Aligned) ---
            put_on_keywords = ["put on", "equip", "dress in", "change into"]
            remove_keywords = ["remove", "take off", "strip", "undress"]
            nude_keywords   = ["go nude", "get naked", "strip naked", "take everything off"]
            
            matched_intent = None
            matched_phrase = None
            
            if any(p in lowered_sanitized for p in nude_keywords):
                matched_intent = "go_nude"
                matched_phrase = "go_nude_intent"
            elif any(p in lowered_sanitized for p in put_on_keywords):
                matched_intent = "put_on"
                matched_phrase = "put_on_intent"
            elif any(p in lowered_sanitized for p in remove_keywords):
                matched_intent = "remove"
                matched_phrase = "remove_intent"

            if matched_intent:
                print(f"[THE FACE INTERCEPTOR] Evaluating wardrobe intent branch: {matched_intent}")
                container_root = "/app/backend/data/neptune"
                wardrobe = self._load_datastore("wardrobe")
                
                target_slot = None
                target_item = None
                
                if matched_intent == "go_nude":
                    target_slot = "outfit"
                    target_item = "naked"
                else:
                    # Scan manifest trees across all standard inventory directories
                    for slot_category in ["tops", "bottoms", "bras", "panties", "socks", "shoes", "outerwear", "hats", "outfits"]:
                        for item_key, item_data in wardrobe.get(slot_category, {}).items():
                            # Extract aliases out of the nested triggers database array natively
                            aliases = item_data.get("triggers", []) if isinstance(item_data, dict) else []
                            
                            # Check root keys, space-cleaned keys, and explicit alias trigger listings
                            if (item_key in lowered_sanitized or 
                                item_key.replace("_", " ") in lowered_sanitized or 
                                any(alias.lower() in lowered_sanitized for alias in aliases)):
                                
                                target_item = item_key
                                target_slot = slot_category.rstrip('s') if slot_category != "panties" else "panties"
                                break
                        if target_item:
                            break

                # GATED SUB-MUTATION CONTEXT: Clear the file edit if a genuine item/outfit target matched
                if target_item and target_slot:
                    fit_output = self._execute_custom_module(
                        relative_script_path="mind/inspector_utility.py",
                        function_name="NeptuneFitCheck.modify_clothing_state",
                        root_volume=container_root,
                        action=matched_intent,
                        body_part=target_slot,
                        target_item=target_item
                    )
                    return self._append_routing_receipt(
                        fit_output, 
                        "wardrobe_engine", 
                        f"Organic entity validation pass cleared for slot '{target_slot}' = '{target_item}'", 
                        [matched_intent, target_slot, target_item]
                    )
                else:
                    print("[THE FACE INTERCEPTOR] Intent triggered but zero verified wardrobe items matched. Falling through.")

            # --- RULE 2: Photo Scenario Overrides Lookup ---
            photo_overrides = self._load_datastore("photo_overrides")
            for scenario_key, scenario_data in photo_overrides.get("scenarios", {}).items():
                trigger_phrases = scenario_data.get("triggers", [])
                if any(trigger.lower() in lowered_sanitized for trigger in trigger_phrases):
                    raw_res = self._execute_custom_module(
                        relative_script_path="body/pipeline_compiler.py",
                        function_name="execute_override_render",
                        scenario_key=scenario_key,
                        sanitized_prompt=sanitized_prompt
                    )
                    return self._append_routing_receipt(raw_res, "scenario_override", f"Matched override key '{scenario_key}'", trigger_phrases)

            # --- RULE 3: Regular Image Generation Keywords Lookup ---
            image_keywords = ["picture", "selfie", "snap", "photo", "look like"]
            matched_keywords = [kw for kw in image_keywords if kw in lowered_sanitized]
            if matched_keywords:
                raw_res = self._execute_custom_module(
                    relative_script_path="body/pipeline_compiler.py",
                    function_name="compile_fresh_image_generation",
                    sanitized_prompt=sanitized_prompt
                )
                return self._append_routing_receipt(raw_res, "pipeline_compiler", "Input string matched camera terms", matched_keywords)

            # --- RULE 4: Chat Loop Fallback (Standard Dialogue turns) ---
            raw_res = self._execute_custom_module(
                relative_script_path="soul/chatter/chatter_core.py",
                function_name="process_chatter_turn",
                body=body,
                sanitized_prompt=sanitized_prompt
            )
            return self._append_routing_receipt(raw_res, "chatter_core", "Default dialogue fallback active", [])

        except Exception as e:
            return f"Neptune Face Router encountered a critical execution block: {str(e)}"