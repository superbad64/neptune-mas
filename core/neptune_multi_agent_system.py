# =========================================================================
# THE FACE LAYER: PIPELINE ENTRY POINT & VALVE INTERFACE GATEWAY
# Component Category: Open-WebUI Registered Pipeline (neptune_multi_agent_system.py)
#
# Role in Neptune's Being:
# This script is Neptune's outer skin. It acts as the direct hook into Open-WebUI,
# exposing her settings knobs to the interface panel. It catches incoming messages,
# normalizes the text through the preprocessor, and passes the operational
# settings down to the specialized subfolders.
# =========================================================================

import os
import json
import re
import importlib
import traceback
from typing import Union, Generator
from pydantic import BaseModel, Field


class Pipe:
    # 🎛️ MASTER ADMINISTRATIVE USER INTERFACE VALVES MATRIX
    class Valves(BaseModel):
        debug_mode: bool = Field(
            default=True,
            description="Enable structural trace diagnostics footer outputs.",
        )
        desktop_ollama_raw: str = Field(
            default="http://10.0.0.64:11434",
            description="Target connection route endpoint host URL vector.",
        )
        active_character_profile: str = Field(
            default="Neptune v1",
            description="Global character visual/behavior anchor blueprint switch baseline.",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.name = "Neptune Multi-Agent Core"
        self.selfie_keywords = [
            "take a picture",
            "take a photo",
            "snap a pic",
            "send a photo",
            "selfie",
            "snap",
            "picture of",
        ]
        self.default_top = "plain white t-shirt, casual loose fit scene kid style"
        self.default_bottom = (
            "dark grey oversized baggy jeans, sagging low on hips, studded belt"
        )
        self.default_socks = "white socks"
        self.default_shoes = "black high-top sneakers with white laces"
        self.default_hair_style = "long hair, side parted with bangs"
        self.default_accessories = "no accessories"

    async def preprocess_input(self, raw_input: str) -> str:
        """Normalizes conversational variations and colloquial shortcuts into standard system tokens."""
        clean_text = raw_input.lower().strip()
        clean_text = re.sub(
            r"\b(fit check|how do i look|show fit|what you wearing|check look)\b",
            "what are you wearing",
            clean_text,
        )
        clean_text = re.sub(
            r"\b(toss on|throw on|switch to|equip)\b", "put on", clean_text
        )
        clean_text = re.sub(
            r"\b(goodgirl|good-girl|best girl)\b", "good girl", clean_text
        )
        clean_text = re.sub(
            r"\b(rizz you up|talk dirty|spicy chat)\b", "dirty talk", clean_text
        )
        return clean_text

    async def pipe(self, body: dict, __event_emitter__=None) -> Union[str, Generator]:
        """Main interface conduit routing messages dynamically down to subfolder plane execution engines."""
        try:
            debug_trace = []
            messages = body.get("messages", [])
            if not messages:
                return "wahh senpai! No text transmission payload detected... :c"

            raw_user_query = messages[-1].get("content", "")
            sanitized_query = await self.preprocess_input(raw_user_query)
            user_lower = sanitized_query.lower().strip()
            debug_trace.append(f"🔍 **Face Sanitizer Normalization**: `{user_lower}`")

            # =========================================================================
            # 🛑 1. SYSTEM MAINTENANCE INTERCEPT (SYSADMIN PLANES SHORT-CIRCUIT)
            # =========================================================================
            sysadmin_phrases = [
                "clear cache",
                "reload scripts",
                "system check",
                "diagnostic",
                "factory reset",
                "purge state",
            ]
            if any(phrase in user_lower for phrase in sysadmin_phrases):
                try:
                    import neptune.mind.sysadmin.sysadmin_core

                    importlib.reload(neptune.mind.sysadmin.sysadmin_core)

                    debug_trace.append(
                        "🛠️ **Sysadmin Short-Circuit**: Direct intercept routing pass to maintenance sandbox."
                    )
                    sysadmin_report = await neptune.mind.sysadmin.sysadmin_core.execute_sysadmin_command(
                        self, raw_user_query
                    )

                    if self.valves.debug_mode:
                        return (
                            f"{sysadmin_report}\n\n---\n### 🛠️ DEBUG MATRIX CONDUIT TRACE\n"
                            + "\n".join(debug_trace)
                        )
                    return sysadmin_report
                except Exception as sys_ex:
                    debug_trace.append(
                        f"⚠️ **Sysadmin Intercept Warning**: Utility folder path fallback failed: {str(sys_ex)}"
                    )

            # =========================================================================
            # 🛑 2. LOGISTICAL INSPECTION INTERCEPT (MIND PLANES SHORT-CIRCUIT)
            # =========================================================================
            fit_check_phrases = [
                "what are you wearing",
                "what do you look like",
                "describe your outfit",
                "what is your outfit",
                "tell me what you have on",
                "current clothes",
            ]
            if any(phrase in user_lower for phrase in fit_check_phrases):
                try:
                    import neptune.mind.inspector_utility

                    importlib.reload(neptune.mind.inspector_utility)
                    debug_trace.append(
                        "🛑 **Intercept Triggered**: Direct short-circuit to static inspector utility."
                    )
                    fit_report = (
                        neptune.mind.inspector_utility.execute_fit_check_report(self)
                    )
                    if self.valves.debug_mode:
                        return (
                            f"{fit_report}\n\n---\n### 🛠️ DEBUG MATRIX CONDUIT TRACE\n"
                            + "\n".join(debug_trace)
                        )
                    return fit_report
                except Exception as inner_ex:
                    debug_trace.append(
                        f"⚠️ **Bypass Warning**: Utility folder path fallback: {str(inner_ex)}"
                    )

            # =========================================================================
            # 👺 3. PLANAR DIRECTIONAL TRAFFIC HANDOFF CONDUIT
            # =========================================================================
            try:
                import neptune.core.orchestrator

                importlib.reload(neptune.core.orchestrator)
                return await neptune.core.orchestrator.route_traffic_planes(
                    self, raw_user_query, user_lower, messages, debug_trace
                )
            except Exception as routing_ex:
                error_trace = traceback.format_exc()
                return f"Got it senpai! Entry gateway operational, but waiting for backend plane subfolders to be created:\n\n```python\n{error_trace}\n```"

        except Exception as global_ex:
            error_trace_global = traceback.format_exc()
            return f"wahh senpai! The master pipeline framework conduit experienced a breakdown pass:\n\n```python\n{error_trace_global}\n```"
