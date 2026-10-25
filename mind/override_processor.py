# =========================================================================
# THE MIND LAYER: VOLATILE VISUAL OVERRIDES & COGNITIVE SHORT-CIRCUITS
# Component Category: Cognitive Intelligence Plane (override_processor.py - Part 1)
# =========================================================================

import os
import json
import random
import re

async def evaluate_visual_overrides(pipe_instance, raw_query: str, current_state: dict) -> tuple:
    """
    Evaluates requests for explicit visual displays or environment overrides.
    Enforces strict volatile adjustments: Modifies rendering prompts for the current
    frame only, preventing any permanent clothing corruption or disk state corruption.
    """
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
    
    # Comprehensive check: Trigger if query contains override words OR requests specific rooms like the shower
    is_visual_request = any(base in clean_query for base in ["show me", "lift your", "pull up", "take off", "in the shower", "inside the shower"])
    if not is_visual_request:
        return False, ""

    # Create local shadow variables for the rendering pass to keep persistent disk data completely untouched
    local_wardrobe = dict(current_state.get("wardrobe", {}))
    local_cosmetics = dict(current_state.get("cosmetics", {}))
    local_environment = dict(current_state.get("environment", {}))
    local_arousal = dict(current_state.get("arousal", {}))

    camera_override = ""
    negative_override = ""
    allow_phone_mirror = False
    override_matched = False
    override_key = "shower_override" # <--- No more duplicated lookups!

    # =========================================================================
    # VOLATILE ENVIRONMENT & SHOWER LOCATION OVERRIDES
    # =========================================================================
    if any(phrase in clean_query for phrase in ["shower", "in the shower", "take a picture in the shower"]):
        local_environment["location"] = "(standing inside an enclosed modern glass shower cabin, water spraying, steam filled:1.4)"
        local_environment["wet_state"] = "wet"
        local_arousal["level"] = 0.8
        # Force volatile nudity for the shower frame only
        for slot in ["outerwear", "top", "bottom", "bra", "panties", "socks", "shoes"]:
            local_wardrobe[slot] = "naked"
        local_wardrobe["accessories"] = []
        camera_override = "sensual full body portrait framing, clear wet skin textures, water droplets, steamed glass background, looking into camera"
        override_key = "show me your pussy"  # Maps back to a high-arousal naked dialogue pool entry
        override_matched = True

    # Parse camera angles context variables from triggers database
    active_angle = "eye-level shot, looking directly into camera lens"
    for angle_key, phrases in g_triggers.get("angles", {}).items():
        if any(p in clean_query for p in phrases):
            if angle_key == "above": active_angle = "high angle shot, looking up at camera lens"
            elif angle_key == "below": active_angle = "low angle dynamic view, looking down towards camera lens"
            break
    # =========================================================================
    # TARGET BODY FOCUS OVERRIDES PARSING (DATABASE-DRIVEN LOCAL INJECTIONS)
    # =========================================================================
    if not override_matched:
        if any(phrase in clean_query for phrase in ["tits", "breasts", "boobs", "chest", "topless", "lift your shirt", "pull up your shirt"]):
            override_key = "show me your tits"
            override_matched = True
        elif any(phrase in clean_query for phrase in ["pussy", "coochie", "slit", "vagina", "naked shot", "crotch"]):
            override_key = "show me your pussy"
            override_matched = True
        elif any(phrase in clean_query for phrase in ["feet", "soles", "bare feet"]):
            override_key = "show me your feet"
            override_matched = True
        elif any(phrase in clean_query for phrase in ["toes", "naked toes"]):
            override_key = "show me your toes"
            override_matched = True
        elif any(phrase in clean_query for phrase in ["ass", "booty", "rear", "buttocks", "from behind"]):
            override_key = "show me your ass"
            override_matched = True

    if override_matched:
        # Load the independent camera preset registry database from container volume storage
        preset_path = "/app/backend/data/neptune/repository/neptune_camera_presets.json"
        try:
            with open(preset_path, 'r') as pf:
                preset_db = json.load(pf).get("camera_presets", {})
            preset = preset_db.get(override_key, {})
        except Exception:
            preset = {}

        if preset:
            # Dynamically execute volatile clothing removals based on database blueprints
            for slot in preset.get("strip_slots", []):
                local_wardrobe[slot] = "naked"
            if "strip_slots" in preset:
                local_wardrobe["accessories"] = []

            # Extract variable state factors from JSON rows smoothly
            if "arousal_level" in preset: local_arousal["level"] = preset["arousal_level"]
            if "nipples_state" in preset: local_arousal["nipples"] = preset["nipples_state"]
            if "wetness_state" in preset: local_arousal["wetness"] = preset["wetness_state"]
            if "wet_state" in preset: local_environment["wet_state"] = preset["wet_state"]
            if "location_override" in preset: local_environment["location"] = preset["location_override"]
            
            # Format the camera string anchor to absorb the chosen angle parameter context
            camera_override = preset.get("camera_override", "").replace("{active_angle}", active_angle)
            negative_override = preset.get("negative_override", "")

        # Build the temporary runtime tracking dictionary container for the compiler pass parameters
        volatile_frame_state = {
            "wardrobe": local_wardrobe,
            "cosmetics": local_cosmetics,
            "environment": local_environment,
            "arousal": local_arousal,
            "meta": {
                "last_camera_composition": camera_override,
                "last_negative_override": negative_override,
                "allow_mirror_phone": allow_phone_mirror
            }
        }
        
        # 1. FIXED: Transmit the local volatile shadow state dictionary directly inside the compiler arguments pool
        # This completely short-circuits the disk reader, forcing ComfyUI to render using our temporary naked variables
        from neptune.body.pipeline_compiler import trigger_body_render
        render_output_markdown = await trigger_body_render(pipe_instance, raw_query, [volatile_frame_state])
        
        # 2. Extract the absolute context-matching spoken dialogue line straight out of your repository
        dialog_path = "/app/backend/data/neptune/repository/neptune_dialog_repository.json"
        try:
            with open(dialog_path, 'r') as df:
                dialog_repo = json.load(df)
            pool = dialog_repo.get("override_responses", {}).get(override_key, ["Here is the view you requested, senpai! 💕"])
            chosen_dialog_text = random.choice(pool)
        except Exception:
            chosen_dialog_text = "Here is the exclusive picture view you requested, senpai! 💕"

        # ABSOLUTE SHORT-CIRCUIT EXIT: Returns combined string immediately, cutting off the chatter core completely
        final_unified_payload = f"{render_output_markdown}\n\n{chosen_dialog_text}"
        return True, final_unified_payload

    return False, ""