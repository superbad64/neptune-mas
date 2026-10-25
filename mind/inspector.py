# =========================================================================
# THE MIND LAYER: WARDROBE MUTATION & OUTFIT AUDITOR CORE
# Component Category: Cognitive Intelligence Plane (inspector.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's somatic self-awareness. It intercepts
# incoming streams to process structural garment inventories, evaluate real-time
# exposure state metrics, handle stylistic alterations, and force instant
# short-circuit reporting bypasses directly back to the gateway.
# =========================================================================

import os
import json
import random
import re

def determine_exposure_state(wardrobe: dict) -> str:
    """Evaluates the structural visibility matrix of clothing to calculate dynamic exposure text blocks."""
    top = wardrobe.get("top", "naked")
    bottom = wardrobe.get("bottom", "naked")
    outerwear = wardrobe.get("outerwear", "naked")
    bra = wardrobe.get("bra", "naked")
    panties = wardrobe.get("panties", "naked")

    has_top = top != "naked"
    has_bottom = bottom != "naked"
    has_outer = outerwear != "naked"
    has_bra = bra != "naked"
    has_panties = panties != "naked"

    # Evaluation cascade rule sets based on coverage metrics
    if not has_top and not has_bottom and not has_outer and not has_bra and not has_panties:
        return "fully_nude"
    if not has_top and has_bottom:
        return "topless"
    if has_top and not has_panties:
        return "pantyless"
    if has_bra and has_panties and not has_top and not has_bottom:
        return "bra_and_panties_visible"
    if (has_bra or has_panties) and not has_top and not has_bottom:
        return "bra_or_panties_visible"
    if not has_bra and has_top and not has_outer:
        return "braless_without_exposure"
        
    return "standard_coverage"

async def evaluate_outfit_interception(raw_query: str, current_state: dict) -> tuple:
    """Intercepts and short-circuits execution if the query asks about her current wardrobe clothing state."""
    repo_dir = "/var/lib/docker/volumes/open-webui/_data/neptune/repository"
    triggers_path = os.path.join(repo_dir, "neptune_interaction_triggers.json")
    
    try:
        with open(triggers_path, 'r') as tf:
            triggers_db = json.load(tf)
        check_phrases = triggers_db.get("outfit_checks", [])
        exposure_responses_pool = triggers_db.get("exposure_responses", {})
    except Exception:
        check_phrases = ["what are you wearing", "outfit check"]
        exposure_responses_pool = {}

    clean_query = raw_query.lower().strip()
    is_check_request = any(phrase in clean_query for phrase in check_phrases)
    if not is_check_request:
        return False, ""

    wardrobe = current_state.get("wardrobe", {})
    cosmetics = current_state.get("cosmetics", {})
    exposure_key = determine_exposure_state(wardrobe)
    
    fallback_line = "My wardrobe layers are fully equipped and neatly organized, senpai!"
    pool = exposure_responses_pool.get(exposure_key, [fallback_line])
    headline_flavor = random.choice(pool) if pool else fallback_line

    lines = [
        f"### 🗄️ NEPTUNE REAL-TIME SYSTEM OUTFIT RUN-DOWN",
        f"*{headline_flavor}*",
        "",
        f"• **Outerwear:** {wardrobe.get('outerwear', 'naked').replace('_', ' ').title()}",
        f"• **Top Garment:** {wardrobe.get('top', 'naked').replace('_', ' ').title()}",
        f"• **Bottom Garment:** {wardrobe.get('bottom', 'naked').replace('_', ' ').title()}",
        f"• **Bra Layer:** {wardrobe.get('bra', 'naked').replace('_', ' ').title()}",
        f"• **Panties Layer:** {wardrobe.get('panties', 'naked').replace('_', ' ').title()}",
        f"• **Socks / Hosiery:** {wardrobe.get('socks', 'naked').replace('_', ' ').title()}",
        f"• **Footwear:** {wardrobe.get('shoes', 'naked').replace('_', ' ').title()}",
    ]
    acc_list = wardrobe.get("accessories", [])
    if isinstance(acc_list, list) and acc_list:
        clean_accs = ", ".join([a.replace('_', ' ').title() for a in acc_list])
        lines.append(f"• **Accessories:** {clean_accs}")
    else:
        lines.append(f"• **Accessories:** None equipped")

    lines.append(f"• **Jewelry Accents:** {wardrobe.get('jewelry', 'none').replace('_', ' ').title()}")
    lines.append(f"• **Active Hairstyle:** {cosmetics.get('hair_style', 'default_scene').replace('_', ' ').title()}")
    
    full_report_output = "\n".join(lines)
    return True, full_report_output

    async def pipe(self, body: dict, __event_emitter__=None) -> str:
        """Master sequential orchestrator processing loop conduit thread."""
        messages = body.get("messages", [])
        if not messages:
            return "wahh senpai! Transmitted execution matrix container was empty down the pipe loop... :c"

        raw_user_query = messages[-1].get("content", "").strip()
        
        # 1. Normalization preprocessor pass execution
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
        if normalized_query.startswith("sysadmin:"):
            admin_command = normalized_query.replace("sysadmin:", "").strip()
            
            # Local high-priority short-circuit for memory flushes
            if any(phrase in admin_command for phrase in ["clear cache", "clear module cache", "flush cache", "reload modules"]):
                print("🧼 Super-Override: Evicting compiled modules from RAM...")
                for module in list(sys.modules.keys()):
                    if "neptune" in module: del sys.modules[module]
                return "### 🧼 SYSTEM SUPER-OVERRIDE REPORT\n\n*Administrative bypass executed successfully. Operational module caches have been forcefully evicted from RAM registers, senpai! 💕*"
            
            # 👗 LOCAL HIGH-PRIORITY SHORT-CIRCUIT FOR FORCE-EQUIPPING OUTFITS
            if admin_command.startswith("dress "):
                target_outfit_key = admin_command.replace("dress ", "").strip().replace(" ", "_")
                
                manifest_path = "/var/lib/docker/volumes/open-webui/_data/neptune/repository/neptune_wardrobe_manifest.json"
                try:
                    with open(manifest_path, 'r') as mf:
                        manifest = json.load(mf)
                    outfits_pool = manifest.get("outfits", {})
                except Exception as e:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Failed loading wardrobe manifest database file: `{str(e)}`*"
                
                # Perform a defensive lookup across keys case-insensitively
                matched_key = next((k for k in outfits_pool.keys() if k.lower() == target_outfit_key.lower()), None)
                
                if matched_key:
                    outfit_found = outfits_pool[matched_key]
                    wardrobe = current_state.setdefault("wardrobe", {})
                    
                    wardrobe["top"] = outfit_found.get("top", outfit_found.get("tops", "naked"))
                    wardrobe["bottom"] = outfit_found.get("bottom", outfit_found.get("bottoms", "naked"))
                    wardrobe["bra"] = outfit_found.get("bra", outfit_found.get("bras", "naked"))
                    wardrobe["panties"] = outfit_found.get("panties", outfit_found.get("panties_layer", "naked"))
                    wardrobe["socks"] = outfit_found.get("socks", outfit_found.get("hosiery", "naked"))
                    wardrobe["shoes"] = outfit_found.get("shoes", outfit_found.get("boots", "naked"))
                    wardrobe["accessories"] = outfit_found.get("accessories", [])
                    wardrobe["outerwear"] = "naked"
                    
                    await save_neptune_state(base_http, current_state)
                    
                    # Instantly route to outfit rundown layout generator to verify successful application
                    from neptune.mind.inspector import evaluate_outfit_interception
                    _, structural_report = await evaluate_outfit_interception("outfit check", current_state)
                    return f"### 🔮 SYSTEM SUPER-OVERRIDE REPORT\n\n*Force-equipped target wardrobe footprint `{matched_key}` into system slots cleanly!*\n\n{structural_report}"
                else:
                    return f"### 🚨 SUPER-OVERRIDE ERROR\n\n*Outfit database lookup miss! Target profile identifier `{target_outfit_key}` does not exist under your manifest registry. Core available outfit configurations: `{', '.join(outfits_pool.keys())}`*"

            # Forward any other trailing admin command down to the system tool terminal router
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
            triggers_path = "/var/lib/docker/volumes/open-webui/_data/neptune/repository/neptune_interaction_triggers.json"
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