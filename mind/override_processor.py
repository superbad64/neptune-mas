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
    
    # 1. Verify master intercept trigger presence ("show me", etc.)
    has_base_trigger = any(base in clean_query for base in v_triggers.get("base_triggers", []))
    if not has_base_trigger:
        return False, ""

    # Ensure dynamic states exist inside systemic memory loops
    arousal_data = current_state.setdefault("arousal", {})
    env_data = current_state.setdefault("environment", {})
    wardrobe = current_state.setdefault("wardrobe", {})
    cosmetics = current_state.setdefault("cosmetics", {})

    # Initialize dynamic camera matrix configuration parameters
    camera_override = ""
    negative_override = ""
    allow_phone_mirror = False
    state_mutated = False

    # =========================================================================
    # PERSISTENT LOCATION CONSISTENCY RUNTIME ENGINE
    # =========================================================================
    location_found = None
    for loc_key, phrases in g_triggers.get("locations", {}).items():
        if any(p in clean_query for p in phrases):
            location_found = loc_key
            break

    if location_found:
        # Dynamic manual location change requested; update memory cache
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
            # As per spec instructions: force temporary naked composition state without flushing structural memory inventory
            wardrobe["top"] = "naked"
            wardrobe["bottom"] = "naked"
            wardrobe["bra"] = "naked"
            wardrobe["panties"] = "naked"
            wardrobe["outerwear"] = "naked"
    else:
        # Fallback to persistent location cache baseline if none explicitly specified
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
    # TARGET BODY FOCUS OVERRIDES PARSING
    # =========================================================================
    # Pure selfie/fit mode check path execution
    if any(fit in clean_query for fit in v_triggers.get("selfie_fit", [])) or clean_query == "show me":
        camera_override = f"full body mirror portrait framing tracking, showing her entire outfit layout, {active_angle}, crisp focus"
        allow_phone_mirror = True
        state_mutated = True

    # Nude: Topless focusing pass execution
    elif any(t in clean_query for t in v_triggers.get("topless", [])):
        arousal_data["level"] = 1.0
        arousal_data["nipples"] = "hard, erect"
        camera_override = f"sensual upper body portrait shot focusing heavily on exposed chest, entirely topless breasts, {active_angle}, naked upper torso"
        negative_override = "suspenders, overalls, straps crossing chest, bra, shirt, covering breasts"
        wardrobe["top"] = "naked"
        wardrobe["bra"] = "naked"
        wardrobe["outerwear"] = "naked"
        state_mutated = True

    # Nude: Extreme close up focusing pass execution
    elif any(p in clean_query for p in v_triggers.get("pussy", [])):
        arousal_data["level"] = 1.0
        arousal_data["wetness"] = "dripping wet"
        env_data["location"] = "(lying wide open completely on top of a messy unmade bed:1.4)"
        camera_override = "extreme close-up macro focus explicit view highlighting exposed pussy, completely nude, parted legs, spread thighs close-up shot"
        for slot in ["top", "bottom", "bra", "panties", "outerwear"]: wardrobe[slot] = "naked"
        state_mutated = True

    # Feet POVs framing tracking selection
    elif any(f in clean_query for f in v_triggers.get("feet", [])):
        camera_override = f"first-person point-of-view macro down-shot perspective focusing completely on bare feet and naked toes, looking down from POV"
        wardrobe["socks"] = "naked"
        wardrobe["shoes"] = "naked"
        state_mutated = True

    # Rear/Ass focusing profile executions
    elif any(a in clean_query for a in v_triggers.get("ass", [])):
        arousal_data["level"] = 1.0
        camera_override = "provocative rear view tracking shot from behind, focusing entirely on lower back and exposed bare buttocks, back turned towards viewer"
        for slot in ["top", "bottom", "bra", "panties", "outerwear"]: wardrobe[slot] = "naked"
        state_mutated = True

    if state_mutated:
        # Write temporary visual context overrides calculations straight into execution registers
        current_state["meta"]["last_camera_composition"] = camera_override
        current_state["meta"]["last_negative_override"] = negative_override
        current_state["meta"]["allow_mirror_phone"] = allow_phone_mirror
        
        # Hard code save state pass before handing execution matrix straight over to Body Render module
        raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"
        
        from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
        await save_neptune_state(base_http, current_state)
        
        # Intercept complete: Execute render pipeline directly, bypassing conversational scripts entirely!
        from neptune.body.pipeline_compiler import trigger_body_render
        render_output_markdown = await trigger_body_render(pipe_instance, raw_query, [])
        return True, render_output_markdown

    return False, ""