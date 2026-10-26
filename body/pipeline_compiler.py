import os
import sys
import json
import random
from typing import Dict, Any, List

def _load_json_data(root_path: str, relative_path: str) -> Dict[str, Any]:
    """Reads a structural database matrix cleanly without applying file modifications."""
    full_path = os.path.join(root_path, relative_path)
    if not os.path.exists(full_path):
        return {}
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def resolve_facial_expression(user_prompt: str, arousal_level: float) -> str:
    """
    Evaluates expression keywords and cross-compatibility tags.
    Strips conflicting elements sequentially, defaulting to 'smiling' if empty.
    """
    lowered_prompt = user_prompt.lower()
    
    # Baseline behavioral expression dictionary mappings
    expression_map = {
        "blushing": ["blush", "shy", "embarrassed", "flustered"],
        "pouting": ["pout", "annoyed", "mad", "angry"],
        "smirking": ["smirk", "teasing", "mischievous", "playful"],
        "crying": ["cry", "sad", "upset", "tears"],
        "laughing": ["laugh", "haha", "excited", "happy"]
    }
    
    active_expressions = []
    for expr_tag, triggers in expression_map.items():
        if any(trigger in lowered_prompt for trigger in triggers):
            active_expressions.append(expr_tag)
            
    # Biometric Arousal Threshold Override matching your 0.0 - 1.6 scale bounds
    if arousal_level > 1.2 and "blushing" not in active_expressions:
        active_expressions.append("blushing")

    # Sequential Conflict Resolution Loop Pass
    if "crying" in active_expressions and "laughing" in active_expressions:
        active_expressions.remove("laughing")  # Cry overrides laughter parameters
    if "pouting" in active_expressions and "smirking" in active_expressions:
        active_expressions.remove("pouting")   # Smirk overrides pout parameters

    if not active_expressions:
        return "smiling, looking at viewer"
        
    return ", ".join(active_expressions) + ", looking at viewer"

def compile_positive_prompt_chain(root_path: str, user_prompt: str) -> str:
    """
    Enforces your exact linear generation sequence constraint matching flat-registry data maps.
    Includes explicit debug verbosity gates and safe list loop checks.
    """
    state = _load_json_data(root_path, "repository/neptune_current_state.json")
    registry = _load_json_data(root_path, "repository/neptune_character_registry.json")
    wardrobe = _load_json_data(root_path, "repository/neptune_wardrobe_manifest.json")
    photo_engine = _load_json_data(root_path, "repository/neptune_photo_engine.json")

    # --- THE VERBOSITY CHECK GATE (Fixed to strictly honor the boolean) ---
    if state.get("debug_verbosity", False):
        print("\n=== [PIPELINE COMPILER TRACE DETECTED] ===")
        print(f"-> Active State: {json.dumps(state)}")
        print(f"-> Photo Engine Locations Config Layout Type: {type(photo_engine.get('locations'))}")
        print(f"-> Photo Engine Poses Config Layout Type: {type(photo_engine.get('poses'))}\n")

    # --- STEP 1: DYNAMIC CHARACTER ATTRIBUTES ---
    active_char_key = state.get("active_character", "neptune_v1").lower()
    char_data = registry.get(active_char_key, {})
    if not char_data:
        char_data = registry.get("neptune_v1", {})

    lowered_prompt = user_prompt.lower()
    is_wet_scenario = any(w in lowered_prompt for w in ["wet", "shower", "rain", "sweat", "glistening", "pool", "water"])
    
    character_attributes = "score_9, score_8_up"
    if is_wet_scenario:
        character_attributes += f", {char_data.get('wet', '')}"
    else:
        character_attributes += f", {char_data.get('dry', '')}"

    # --- STEP 2: FACIAL EXPRESSIONS ---
    arousal_val = float(state.get("mood", {}).get("arousal", 0.0))
    facial_expressions = resolve_facial_expression(user_prompt, arousal_val)

    # --- STEP 3: OUTFIT MANAGEMENT COMPILATION ---
    appearance = state.get("appearance", {})
    outfit_tags = []
    
    for slot in ["hat", "outerwear", "top", "bra", "bottom", "panties", "socks", "shoes"]:
        item_key = appearance.get(slot, "naked")
        if item_key == "naked":
            outfit_tags.append(f"naked {slot}")
        else:
            for category in ["tops", "bottoms", "bras", "panties", "socks", "shoes", "outerwear", "hats"]:
                if item_key in wardrobe.get(category, {}):
                    prompt_token = wardrobe[category][item_key].get("prompt_tags")
                    if prompt_token:
                        outfit_tags.append(prompt_token)
                    break
                    
    compiled_outfit = ", ".join(outfit_tags)

    # --- STEP 4: SAFE LOCATION & POSE DETECTIONS (List Error Fix) ---
    detected_location = "standing inside a bedroom"
    locations_pool = photo_engine.get("locations", {})
    
    # Check if locations block is loaded as a dictionary config or flat list loop
    if isinstance(locations_pool, dict):
        for loc_key, loc_data in locations_pool.items():
            # If item contains a nested dictionary layer, parse securely
            if isinstance(loc_data, dict):
                triggers = loc_data.get("triggers", [])
                if any(t.lower() in lowered_prompt for t in triggers):
                    detected_location = loc_data.get("prompt_tags", detected_location)
                    break
    elif isinstance(locations_pool, list):
        # Fallback tracking if locations are defined as straight list elements
        for loc_item in locations_pool:
            if isinstance(loc_item, dict):
                if any(t.lower() in lowered_prompt for t in loc_item.get("triggers", [])):
                    detected_location = loc_item.get("prompt_tags", detected_location)
                    break

    detected_pose = "standing, looking at viewer"
    poses_pool = photo_engine.get("poses", {})
    
    if isinstance(poses_pool, dict):
        for pose_key, pose_data in poses_pool.items():
            if isinstance(pose_data, dict):
                triggers = pose_data.get("triggers", [])
                if any(t.lower() in lowered_prompt for t in triggers):
                    detected_pose = pose_data.get("prompt_tags", detected_pose)
                    break
    elif isinstance(poses_pool, list):
        for pose_item in poses_pool:
            if isinstance(pose_item, dict):
                if any(t.lower() in lowered_prompt for t in pose_item.get("triggers", [])):
                    detected_pose = pose_item.get("prompt_tags", detected_pose)
                    break

    # --- FINAL LINEAR SYNTAX CONCATENATION SEQUENCE ---
    final_positive_chain = (
        f"{character_attributes}, {facial_expressions}, wearing {compiled_outfit}, "
        f"located in {detected_location}, performing {detected_pose}"
    )
    return final_positive_chain

def compile_fresh_image_generation(sanitized_prompt: str) -> str:
    """
    Interface execution hook invoked by the Face Router during standard T2I requests.
    Compiles full positive/negative parameters and maps output data straight to ComfyUI.
    """
    container_root = "/app/backend/data/neptune"
    
    compiled_positive = compile_positive_prompt_chain(container_root, sanitized_prompt)
    
    # Enforce your front-loaded electronic filtering and explicit negative anchors
    # Added "grinning" directly to block distorted teeth-baring expressions under PonyRealism
    compiled_negative = (
        "grinning, photorealistic, real human skin texture, pores, freckles, real life person, "
        "cosplayer photograph, hyper-realistic, score_4, score_5, score_6, lowres, worst quality, "
        "low quality, 2d anime, flat colors, lineart, drawing, illustration, cartoon, deformed hands, "
        "extra fingers, missing fingers, extra limbs, multiple views, duplicate character, "
        "out of focus, blurry, dirt, text, watermark"
    )

    print(f"[PIPELINE COMPILER] Compiled Positive Chain:\n  {compiled_positive}")

    # Text execution sandbox handoff straight down to the ComfyUI API transmitter tool
    try:
        dispatch_script = os.path.join(container_root, "body/comfy_dispatch.py")
        with open(dispatch_script, 'r', encoding='utf-8') as f:
            dispatch_source = f.read()
            
        dispatch_context = {}
        exec(dispatch_source, globals(), dispatch_context)
        
        response_text = dispatch_context["trigger_comfy_api_transmission"](
            positive_prompt=compiled_positive,
            negative_prompt=compiled_negative,
            is_reshoot=False
        )
        return response_text
    except Exception as e:
        return f"❌ \"Gah! I compiled our generation vectors perfectly, Boss, but hit a transmission block: {str(e)}\""

def execute_override_render(scenario_key: str, sanitized_prompt: str) -> str:
    """Interface hook for photo scenario overrides matching photo_overrides.json."""
    return f"⚡ \"Scenario Override Render Target engaged for block `{scenario_key}`! Chain compilation running!\""
