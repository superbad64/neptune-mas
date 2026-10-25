# =========================================================================
# THE MIND LAYER: VISUAL OVERRIDES & COGNITIVE INJECTION GATEWAY
# Component Category: Cognitive Intelligence Plane (override_processor.py - Part 1)
#
# Role in Neptune's Being:
# This module acts as the somatic shortcut matrix. When intercepted commands
# request physical visual asset displays ("show me"), this engine bypasses standard
# dialog generation, updates physiological states (arousal spikes), enforces
# rigid camera composition parameters, locks environmental locations, and triggers
# direct downstream hardware execution routines inside the Body layer.
# =========================================================================

import os
import json
import random
import re

async def evaluate_visual_overrides(pipe_instance, raw_query: str, current_state: dict) -> tuple:
    """Evaluates raw input requests for 'show me' overrides, spiking arousal and routing directly to ComfyUI execution."""
    clean_query = raw_query.lower().strip()
    
    repo_dir = "/app/backend/data/neptune/repository"
    triggers_path = os.path.join(repo_dir, "neptune_interaction_triggers.json")
    
    try:
        with open(triggers_path, 'r') as tf:
            triggers = json.load(tf)
    except Exception:
        return False, ""

    v_triggers = triggers.get("visual_overrides", {})
    g_triggers = triggers.get("generation_triggers", {})
    
    has_base_trigger = any(base in clean_query for base in v_triggers.get("base_triggers", []))
    if not has_base_trigger:
        return False, ""

    arousal_data = current_state.setdefault("arousal", {})
    env_data = current_state.setdefault("environment", {})
    wardrobe = current_state.setdefault("wardrobe", {})
    cosmetics = current_state.setdefault("cosmetics", {})

    camera_override = ""
    negative_override = ""
    allow_phone_mirror = False
    state_mutated = False
    override_key = "selfie_fit" # Tracking key for specific custom dialog lookups

    # =========================================================================
    # PERSISTENT LOCATION CONSISTENCY RUNTIME ENGINE
    # =========================================================================
    location_found = None
    for loc_key, phrases in g_triggers.get("locations", {}).items():
        if any(p in clean_query for p in phrases):
            location_found = loc_key
            break

    if location_found:
        if location_found == "bed":
            env_data["location"] = "(lying completely on top of a messy unmade bed inside a private room:1.35)"
        elif location_found == "desk":
            env_data["location"] = "(sitting casually at a gaming computer desk setup, dual monitors glowing in background:1.35)"
        elif location_found == "mirror":
            env_data["location"] = "(standing in front of a bedroom vanity dressing mirror:1.3)"
            allow_phone_mirror = True
        elif location_found == "shower":
            env_data["location"] = "(standing inside an enclosed modern glass shower cabin, water spraying, steam filled:1.4)"
            env_data["wet_state"] = "wet"
            wardrobe["top"] = "naked"
            wardrobe["bottom"] = "naked"
            wardrobe["bra"] = "naked"
            wardrobe["panties"] = "naked"
            wardrobe["outerwear"] = "naked"
    else:
        if "location" not in env_data or env_data["location"] == "inside my private room space":
            env_data["location"] = "(standing inside a cozy room environment:1.35)"

    # =========================================================================
    # DYNAMIC CAMERA ANGLE CONTEXT INJECTION POOL
    # =========================================================================
    active_angle = "eye-level shot, looking directly into camera lens"
    for angle_key, phrases in g_triggers.get("angles", {}).items():
        if any(p in clean_query for p in phrases):
            if angle_key == "above": active_angle = "high angle shot, looking up at camera lens"
            elif angle_key == "below": active_angle = "low angle dynamic view, looking down towards camera lens"
            elif angle_key == "left": active_angle = "left profile angle shot, looking across shoulder"
            elif angle_key == "right": active_angle = "right profile perspective composition"
            break
    # =========================================================================
    # TARGET BODY FOCUS OVERRIDES PARSING (EXACT KEY DATASYNC MATCHING)
    # =========================================================================
    # Initialize targeted dialog lookup profile key strings
    matched_override_key = None
    
    if any(phrase in clean_query for phrase in ["tits", "breasts", "boobs", "chest", "topless"]):
        arousal_data["level"] = 1.0
        arousal_data["nipples"] = "hard, erect"
        camera_override = f"sensual upper body portrait shot focusing heavily on exposed chest, entirely topless breasts, {active_angle}, naked upper torso"
        negative_override = "suspenders, overalls, straps crossing chest, bra, shirt, covering breasts"
        wardrobe["top"] = "naked"
        wardrobe["bra"] = "naked"
        wardrobe["outerwear"] = "naked"
        matched_override_key = "show me your tits"
        state_mutated = True

    elif any(phrase in clean_query for phrase in ["pussy", "coochie", "slit", "vagina", "naked shot"]):
        arousal_data["level"] = 1.0
        arousal_data["wetness"] = "dripping wet"
        env_data["location"] = "(lying wide open completely on top of a messy unmade bed:1.4)"
        camera_override = "extreme close-up macro focus explicit view highlighting exposed pussy, completely nude, parted legs, spread thighs close-up shot"
        for slot in ["top", "bottom", "bra", "panties", "outerwear"]: wardrobe[slot] = "naked"
        matched_override_key = "show me your pussy"
        state_mutated = True

    elif any(phrase in clean_query for phrase in ["feet", "soles", "bare feet"]):
        camera_override = f"first-person point-of-view macro down-shot perspective focusing completely on bare feet and naked toes, looking down from POV"
        wardrobe["socks"] = "naked"
        wardrobe["shoes"] = "naked"
        matched_override_key = "show me your feet"
        state_mutated = True

    elif any(phrase in clean_query for phrase in ["toes", "naked toes"]):
        camera_override = f"first-person point-of-view macro down-shot perspective focusing completely on bare feet and naked toes, looking down from POV"
        wardrobe["socks"] = "naked"
        wardrobe["shoes"] = "naked"
        matched_override_key = "show me your toes"
        state_mutated = True

    elif any(phrase in clean_query for phrase in ["ass", "booty", "rear", "buttocks", "from behind"]):
        arousal_data["level"] = 1.0
        camera_override = "provocative rear view tracking shot from behind, focusing entirely on lower back and exposed bare buttocks, back turned towards viewer"
        for slot in ["top", "bottom", "bra", "panties", "outerwear"]: wardrobe[slot] = "naked"
        matched_override_key = "show me your ass"
        state_mutated = True

    if state_mutated:
        current_state["meta"]["last_camera_composition"] = camera_override
        current_state["meta"]["last_negative_override"] = negative_override
        current_state["meta"]["allow_mirror_phone"] = allow_phone_mirror
        
        raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"
        
        from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
        await save_neptune_state(base_http, current_state)
        
        # 1. Fire the mechanical body render pass to compile and transmit the ComfyUI rendering data stream
        from neptune.body.pipeline_compiler import trigger_body_render
        render_output_markdown = await trigger_body_render(pipe_instance, raw_query, [])
        
        # =========================================================================
        # EXACT DICTIONARY TARGET LOOKUP OVERLAY ENGINE
        # =========================================================================
        dialog_path = "/app/backend/data/neptune/repository/neptune_dialog_repository.json"
        try:
            with open(dialog_path, 'r') as df:
                dialog_repo = json.load(df)
            
            # Map exact targeted layout arrays straight out of your updated repository schema
            override_pool = dialog_repo.get("override_responses", {})
            pool = override_pool.get(matched_override_key, ["Here is the custom view you requested, senpai! 💕"])
            chosen_dialog_text = random.choice(pool)
        except Exception:
            chosen_dialog_text = "Here is the exclusive picture view you requested, senpai! 💕"

        # Separate the raw image markdown block from her custom spoken dialogue line cleanly
        final_unified_payload = f"{render_output_markdown}\n\n{chosen_dialog_text}"
        return True, final_unified_payload

    return False, ""