# =========================================================================
# THE FACE LAYER: OPEN-WEBUI SELF-CONTAINED FUNCTION PIPE INTERFACE
# Component Category: Front Gateway Integration Interface (neptune_multi_agent_system.py - Part 1)
# =========================================================================

import os
import sys
import re
import json
import random
import time
from pydantic import BaseModel, Field

# Mount the base system data directory volume paths safely inside container workspace
container_data_root = "/app/backend/data"
if container_data_root not in sys.path:
    sys.path.insert(0, container_data_root)

host_volume_root = "/var/lib/docker/volumes/open-webui/_data"
if host_volume_root not in sys.path:
    sys.path.insert(0, host_volume_root)


class Valves(BaseModel):
    """FLATTENED OPEN-WEBUI VALVES CONFIGURATION SCHEMA OBJECT"""

    desktop_ollama_raw: str = Field(
        default="10.0.0.64",
        description="Host cluster IP pointer allocation for ComfyUI and Primary Ollama nodes.",
    )
    active_character_profile: str = Field(
        default="Neptune v1",
        description="Active visual generation mesh template profile selection constraint.",
    )


class Pipe:
    def __init__(self):
        # Register the local system valves data layer configuration maps natively
        self.valves = Valves()

    async def on_startup(self):
        print("👺 Neptune Multi-Agent System Function Pipe interface online.")

    async def on_shutdown(self):
        print("👺 Neptune Multi-Agent System Function Pipe interface offline.")

    def apply_slang_preprocessor_normalization(self, input_text: str) -> str:
        """STRICT HARD-MATCHING TOKEN NORMALIZER to prevent partial-word corruption on custom assets."""
        slang_dictionary = {
            "fit": "outfit",
            "tits": "breasts",
            "pussy": "vagina",
            "coochie": "vagina",
            "booty": "buttocks",
            "ass": "buttocks",
            "pic": "picture",
            "snap": "picture",
        }
        words = re.findall(r"[\w']+|[.,!?;:]", input_text)
        normalized_tokens = []
        for token in words:
            token_lower = token.lower()
            if token_lower in slang_dictionary:
                normalized_tokens.append(slang_dictionary[token_lower])
            else:
                normalized_tokens.append(token)

        rebuilt_text = ""
        for token in normalized_tokens:
            if token in ".,!?;:":
                rebuilt_text = rebuilt_text.rstrip() + token + " "
            else:
                rebuilt_text += token + " "
        return rebuilt_text.strip()

    async def pipe(self, body: dict, __event_emitter__=None) -> str:
        """Master sequential orchestrator processing loop conduit thread (Part 2)."""
        messages = body.get("messages", [])
        if not messages:
            return "wahh senpai! Transmitted execution matrix container was empty down the pipe loop... :c"

        raw_user_query = messages[-1].get("content", "").strip()

        # 1. Hard-matching token normalization preprocessor pass execution
        normalized_query = self.apply_slang_preprocessor_normalization(raw_user_query)

        # Establish base networking addresses mapping properties
        raw_valve = str(getattr(self.valves, "desktop_ollama_raw", "10.0.0.64")).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"

        # Load global system database state files from disk records
        from neptune.mind.sysadmin.sysadmin_core import (
            load_neptune_state,
            save_neptune_state,
        )

        fallback_defaults = {
            "wardrobe": {
                "bra": "black_cotton_bra",
                "panties": "black_string",
                "socks": "black_thigh_highs",
                "top": "white_crop_tank",
                "bottom": "tifa_skirt",
                "shoes": "tifa_boots",
                "accessories": ["tifa_gloves", "suspenders"],
                "jewelry": "teardrop_earrings",
                "outerwear": "naked",
            },
            "cosmetics": {
                "hair_style": "loose_hair",
                "makeup": "default_makeup",
                "nails": "default_nails",
                "piercings": "default_piercings",
            },
            "performance": {
                "body_pose": "default_pose",
                "expression": "default_expression",
            },
            "environment": {
                "location": "inside my private room space",
                "wet_state": "dry",
            },
            "arousal": {"level": 0.0, "wetness": "dry", "nipples": "soft"},
            "meta": {
                "last_visual_canvas": "example.png",
                "last_interaction_timestamp": 0.0,
            },
        }
        current_state = await load_neptune_state(base_http, fallback_defaults)

        # =========================================================================
        # INTERCEPT 0: ADMINISTRATIVE SUPER-OVERRIDE CONTROL CONDUIT
        # =========================================================================
        if normalized_query.lower().startswith("sysadmin:"):
            admin_command = re.sub(
                r"^sysadmin:\s*", "", normalized_query, flags=re.IGNORECASE
            ).strip()

            if any(
                phrase in admin_command
                for phrase in [
                    "clear cache",
                    "clear module cache",
                    "flush cache",
                    "reload modules",
                ]
            ):
                for module in list(sys.modules.keys()):
                    if "neptune" in module:
                        del sys.modules[module]
                return "### 🧼 SYSTEM SUPER-OVERRIDE REPORT\n\n*Administrative bypass executed successfully. Operational module caches have been forcefully evicted from RAM registers, senpai! 💕*"

            elif admin_command.startswith("dress "):
                target_outfit_key = (
                    admin_command.replace("dress ", "")
                    .strip()
                    .replace(" ", "_")
                    .lower()
                )
                manifest_path = "/app/backend/data/neptune/repository/neptune_wardrobe_manifest.json"
                try:
                    with open(manifest_path, "r") as mf:
                        manifest = json.load(mf)
                    outfits_pool = manifest.get("outfits", {})
                except Exception as e:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Failed loading wardrobe manifest: `{str(e)}`*"

                matched_key = None
                for key, data in outfits_pool.items():
                    if key.lower() == target_outfit_key or any(
                        t.lower().replace(" ", "_") == target_outfit_key
                        for t in data.get("triggers", [])
                    ):
                        matched_key = key
                        break

                if matched_key:
                    outfit_data = outfits_pool[matched_key]
                    items = outfit_data.get("items", outfit_data)
                    wardrobe = current_state.setdefault("wardrobe", {})
                    wardrobe["top"] = items.get("top", items.get("tops", "naked"))
                    wardrobe["bottom"] = items.get(
                        "bottom", items.get("bottoms", "naked")
                    )
                    wardrobe["bra"] = items.get("bra", items.get("bras", "naked"))
                    wardrobe["panties"] = items.get(
                        "panties", items.get("panties_layer", "naked")
                    )
                    wardrobe["socks"] = items.get(
                        "socks", items.get("hosiery", "naked")
                    )
                    wardrobe["shoes"] = items.get("shoes", items.get("boots", "naked"))
                    wardrobe["accessories"] = items.get("accessories", [])
                    wardrobe["outerwear"] = "naked"
                    await save_neptune_state(base_http, current_state)

                    from neptune.mind.inspector import evaluate_outfit_interception

                    _, structural_report = await evaluate_outfit_interception(
                        "outfit check", current_state
                    )
                    return f"### 🔮 SYSTEM SUPER-OVERRIDE REPORT\n\n*Force-equipped target wardrobe footprint `{matched_key}` into system slots cleanly!*\n\n{structural_report}"
                else:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Outfit missing! Identifier `{target_outfit_key}` not found under manifest repository keys.*"
            else:
                try:
                    from neptune.mind.sysadmin.sysadmin_core import (
                        handle_sysadmin_terminal_routing,
                    )

                    return await handle_sysadmin_terminal_routing(
                        admin_command, current_state
                    )
                except ImportError:
                    return f"### 🚨 SYSTEM SUPER-OVERRIDE FAULT\n\n*Missing routing blocks from `sysadmin_core.py`!*"

        # 2. Process biological emotional decay ticking loops
        from neptune.soul.mood_engine import process_emotional_decay_cycle

        current_state = await process_emotional_decay_cycle(current_state)
        # =========================================================================
        # INTERCEPT 1: COGNITIVE MIND WARDROBE & EQUIP GATES (ABSOLUTE PRIORITIZED EXIT)
        # =========================================================================
        from neptune.mind.inspector import evaluate_outfit_interception

        triggers_path = (
            "/app/backend/data/neptune/repository/neptune_interaction_triggers.json"
        )
        manifest_path = (
            "/app/backend/data/neptune/repository/neptune_wardrobe_manifest.json"
        )

        try:
            with open(triggers_path, "r") as tf, open(manifest_path, "r") as mf:
                triggers = json.load(tf)
                manifest = json.load(mf)
        except Exception:
            triggers, manifest = {}, {}

        # 1. Check for basic outfit rundown queries (Exits immediately if matched)
        intercepted, report_payload = await evaluate_outfit_interception(
            normalized_query, current_state
        )
        if intercepted:
            return report_payload

        # 2. Check for specialized "show me" visual overrides (Exits immediately if matched)
        from neptune.mind.override_processor import evaluate_visual_overrides

        intercepted_override, override_render_data = await evaluate_visual_overrides(
            self, normalized_query, current_state
        )
        if intercepted_override:
            return override_render_data

        # 3. Check for image reshoots (Exits immediately if matched)
        reshoot_phrases = triggers.get("reshoot_triggers", ["reshoot", "take it again"])
        if any(
            re.search(r"\b" + re.escape(p) + r"\b", normalized_query)
            for p in reshoot_phrases
        ):
            from neptune.body.reshoot_worker import execute_physical_image_reshoot

            return await execute_physical_image_reshoot(
                self, normalized_query, [], current_state
            )

        # 4. Check for clean selfie/picture capture commands (Exits immediately if matched)
        gen_triggers = triggers.get("generation_triggers", {}).get(
            "capture_commands", ["take a selfie", "take a picture"]
        )
        if any(phrase in normalized_query for phrase in gen_triggers):
            from neptune.body.pipeline_compiler import trigger_body_render

            return await trigger_body_render(self, normalized_query, [])

        # 5. Core Wardrobe Equipment Check ("Put on", "Equip", "Wear")
        m_triggers = triggers.get("outfit_mutations", {})
        h_triggers = triggers.get("hair_mutations", {})
        wardrobe = current_state.setdefault("wardrobe", {})
        cosmetics = current_state.setdefault("cosmetics", {})
        state_mutated = False

        if any(k in normalized_query for k in m_triggers.get("nude_keywords", [])):
            for slot in [
                "outerwear",
                "top",
                "bottom",
                "bra",
                "panties",
                "socks",
                "shoes",
            ]:
                wardrobe[slot] = "naked"
            wardrobe["accessories"], wardrobe["jewelry"] = [], "none"
            state_mutated = True

        elif any(k in normalized_query for k in m_triggers.get("equip_keywords", [])):
            outfits_pool = manifest.get("outfits", {})
            outfit_found = None

            def compress(text: str) -> str:
                if not text:
                    return ""
                cleaned = str(text).lower()
                cleaned = (
                    cleaned.replace("'", "")
                    .replace("’", "")
                    .replace("`", "")
                    .replace('"', "")
                    .replace("”", "")
                )
                return re.sub(r"[^\w]", "", cleaned)

            flat_query = compress(normalized_query)

            for name, data in outfits_pool.items():
                triggers_flat = [
                    compress(t)
                    for t in data.get("triggers", [])
                    if len(compress(t)) > 2
                ]
                name_flat = compress(name)
                if (
                    any(t in flat_query for t in triggers_flat)
                    or name_flat in flat_query
                ):
                    outfit_found = data
                    break

            if outfit_found:
                items = outfit_found.get("items", outfit_found)
                wardrobe["top"] = items.get("top", items.get("tops", "naked"))
                wardrobe["bottom"] = items.get("bottom", items.get("bottoms", "naked"))
                wardrobe["bra"] = items.get("bra", items.get("bras", "naked"))
                wardrobe["panties"] = items.get(
                    "panties", items.get("panties_layer", "naked")
                )
                wardrobe["socks"] = items.get("socks", items.get("hosiery", "naked"))
                wardrobe["shoes"] = items.get("shoes", items.get("boots", "naked"))
                wardrobe["accessories"] = items.get("accessories", [])
                wardrobe["outerwear"] = items.get(
                    "outerwear", items.get("coat", items.get("jacket", "naked"))
                )
                state_mutated = True
            else:
                if not any(
                    word in normalized_query
                    for word in ["clothes", "outfit", "gear", "suit"]
                ):
                    for category, items_dict in manifest.items():
                        if category == "outfits":
                            continue
                        for item_key in items_dict.keys():
                            clean_item = item_key.lower().replace("_", " ")
                            if clean_item in normalized_query:
                                slot_map = {
                                    "tops": "top",
                                    "bottoms": "bottom",
                                    "bras": "bra",
                                    "panties": "panties",
                                    "socks": "socks",
                                    "shoes": "shoes",
                                    "jewelry": "jewelry",
                                    "outerwear": "outerwear",
                                }
                                target_slot = slot_map.get(category)
                                if target_slot:
                                    wardrobe[target_slot] = item_key
                                    state_mutated = True
                                    break

        # Check for strip or swap actions
        elif any(
            k in normalized_query for k in m_triggers.get("strip_keywords", [])
        ) or any(k in normalized_query for k in m_triggers.get("swap_keywords", [])):
            slot_keywords = {
                "outerwear": ["outerwear", "coat", "jacket"],
                "top": ["top", "shirt", "blouse", "tank"],
                "bottom": ["bottom", "skirt", "pants", "shorts"],
                "bra": ["bra", "brassiere"],
                "panties": ["panties", "underwear"],
                "socks": ["socks", "stockings"],
                "shoes": ["shoes", "boots"],
            }
            for slot, keywords in slot_keywords.items():
                if any(k in normalized_query for k in keywords):
                    wardrobe[slot] = "naked"
                    state_mutated = True

        # =========================================================================
        # HAIRSTYLE MUTATION MATRIX (HIGH-PRIORITY PHRASE INTERCEPTOR)
        # =========================================================================
        # CHANGED: Replaced 'loose_hair' with 'loose_hair' across all loose anchors
        if any(
            phrase in normalized_query.lower()
            for phrase in [
                "let your hair down",
                "put your hair down",
                "wear your hair down",
                "hair loose",
            ]
        ):
            cosmetics["hair_style"] = "loose_hair"
            state_mutated = True
        elif any(
            k in normalized_query for k in h_triggers.get("hair_down_triggers", [])
        ):
            cosmetics["hair_style"] = "loose_hair"
            state_mutated = True
        elif any(p in normalized_query for p in h_triggers.get("style_prefix", [])):
            if any(b in normalized_query for b in h_triggers.get("bun", [])):
                cosmetics["hair_style"] = "high_bun"
            elif any(p in normalized_query for p in h_triggers.get("ponytail", [])):
                cosmetics["hair_style"] = "high_ponytail"
            elif any(t in normalized_query for t in h_triggers.get("twintails", [])):
                cosmetics["hair_style"] = "twintails"
            elif any(br in normalized_query for br in h_triggers.get("braid", [])):
                cosmetics["hair_style"] = "braid"
            state_mutated = True

        if state_mutated:
            await save_neptune_state(base_http, current_state)
            from neptune.mind.inspector import evaluate_outfit_interception

            _, structural_report = await evaluate_outfit_interception(
                "outfit check", current_state
            )
            return structural_report

        # Standard conversational fallback handling: pass query unmodified down to Ollama container nodes
        from neptune.soul.chatter.chatter_core import prompt_conversational_core

        raw_model_reply = await prompt_conversational_core(
            pipe_instance=self,
            context_prompt=raw_user_query,
            chat_history=messages,
            current_state=current_state,
        )

        from neptune.soul.dialog_router import route_conversational_flavor_injection

        final_conduit_delivery_text = await route_conversational_flavor_injection(
            pipe_instance=self, base_reply=raw_model_reply, current_state=current_state
        )

        await save_neptune_state(base_http, current_state)
        return final_conduit_delivery_text
