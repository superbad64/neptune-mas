# =========================================================================
# THE BODY LAYER: PHYSICAL SENSORY CONTEXT & PROMPT MATRIX COMPILER
# Component Category: Physical Sensory I/O (pipeline_compiler.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's physical skin, eyes, and camera framing lens.
# Operating entirely separated from her cognitive Mind and conversational Soul,
# it is purely responsible for parsing raw Stable Diffusion weights, loading
# character registries, executing local negative injections, and compiling 
# prompt matrices cleanly before handing transaction packages off to ComfyUI.
# =========================================================================

import json
import os
import re
import random
from neptune.mind.sysadmin.sysadmin_core import load_neptune_state

async def trigger_body_render(pipe_instance, raw_user_query: str, messages: list) -> str:
    """Compiles character baselines, camera angles, active styles, and maps out the absolute rendering payload matrix."""
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    target_host = match.group(0) if match else "10.0.0.64"
    base_http = f"http://{target_host}:8189"

    # Core system defaults mapping array properties
    fallback_defaults = {
        "wardrobe": {
            "bra": "black_cotton_bra", "panties": "black_string", "socks": "black_thigh_highs", 
            "top": "white_crop_tank", "bottom": "tifa_skirt", "shoes": "tifa_boots",
            "accessories": ["tifa_gloves", "suspenders"], "jewelry": "teardrop_earrings",
            "outerwear": "naked"
        },
        "cosmetics": {
            "hair_style": "loose_hair", "makeup": "default_makeup",
            "nails": "default_nails", "piercings": "default_piercings"
        },
        "performance": {"body_pose": "default_pose", "expression": "default_expression"},
        "environment": {"location": "inside my private room space", "wet_state": "dry"},
        "arousal": {"level": 0.0, "wetness": "dry", "nipples": "soft"},
        "meta": {"last_interaction_timestamp": 0.0}
    }

    current_state = await load_neptune_state(base_http, fallback_defaults)
    user_lower = raw_user_query.lower().strip()

    repo_dir = "/app/backend/data/neptune/repository"
    manifest_path = os.path.join(repo_dir, "neptune_wardrobe_manifest.json")
    pose_path = os.path.join(repo_dir, "neptune_poses_repository.json")
    registry_path = os.path.join(repo_dir, "neptune_character_registry.json")

    # Dynamic asset repository filesystem mapping ingestion pass
    try:
        with open(manifest_path, 'r') as mf, open(pose_path, 'r') as pf, open(registry_path, 'r') as rf:
            manifest = json.load(mf)
            pose_repo = json.load(pf)
            character_registry = json.load(rf)
    except Exception:
        manifest = {}
        pose_repo = {}
        character_registry = {
            "Neptune v1": {
                "dry": "(neptune_companion, lookalike of tifa lockhart, long ginger orange hair, vibrant green eyes, pale white skin, highly detailed facial features, athletic toned proportions:1.3)",
                "wet": "(neptune_companion, lookalike of tifa lockhart, long ginger orange hair, vibrant green eyes, pale white skin, athletic toned proportions, wet skin textures, water droplets, glistening:1.35)"
            }
        }

    wardrobe = current_state.get("wardrobe", {})
    cosmetics = current_state.get("cosmetics", {})
    arousal_data = current_state.get("arousal", {})
    env_data = current_state.get("environment", {})
    meta_cache = current_state.get("meta", {})

    active_profile = getattr(pipe_instance.valves, "active_character_profile", "Neptune v1")
    state_key = "wet" if env_data.get("wet_state") == "wet" else "dry"
    
    # Secure dynamic extraction from file registry assets
    profile_data = character_registry.get(active_profile, character_registry.get("Neptune v1"))
    character_baseline = profile_data.get(state_key, profile_data.get("dry"))

    # Initialize master compiler state trackers
    pm = {}
    # Initialize look parameters based on active cache records
    pm["outerwear"] = manifest.get("outerwear", {}).get(wardrobe.get("outerwear"), {}).get("prompt", "")
    pm["accessories"] = ""
    pm["jewelry"] = manifest.get("jewelry", {}).get(wardrobe.get("jewelry"), {}).get("prompt", "")
    pm["makeup"] = cosmetics.get("makeup", "")
    pm["nails"] = cosmetics.get("nails", "")
    
    # Piercings Token compiler injection layer
    piece_key = cosmetics.get("piercings", "default_piercings")
    pm["piercings"] = manifest.get("piercings", {}).get(piece_key, {}).get("prompt", "")

    # Consolidate environmental location parameters pulled from the runtime cache
    pm["location"] = env_data.get("location", "(standing inside a cozy room environment:1.35)")

    # Read tracking flags passed downstream by the visual override module
    camera_comp = meta_cache.get("last_camera_composition", "upper body portrait shot including face and head, clear eyes looking forward, eye-level shot, looking directly into camera lens, detailed framing focus")
    custom_negative = meta_cache.get("last_negative_override", "")
    allow_mirror_phone = meta_cache.get("allow_mirror_phone", False)

    pm["expression"] = "subtle smile, looking at viewer"
    if arousal_data.get("level", 0.0) >= 0.7:
        pm["expression"] = "blushing deeply, heavy breathing, sensual gaze looking at viewer"

    # Process standard layout maps assignment loops
    pm["top"] = manifest.get("tops", {}).get(wardrobe.get("top"), {}).get("prompt", "")
    pm["pose"] = random.choice(pose_repo.get("standing_poses", ["standing casually looking forward"]))

    # Compile hairstyle strings dynamically based on selected configurations
    hair_key = cosmetics.get("hair_style", "loose_hair")
    if hair_key == "high_bun":
        raw_hair = "long hair pulled up into a high messy bun, stray strands framing the face"
    elif hair_key == "high_ponytail":
        raw_hair = "long hair styled into a high sleek ponytail swinging backward"
    elif hair_key == "twintails":
        raw_hair = "long hair styled into high twintails on each side of the head, sharp split bangs"
    elif hair_key == "braid":
        raw_hair = "long hair styled into a thick French braid falling forward over the shoulder and chest"
    else:
        raw_hair = manifest.get("hair_styles", {}).get(hair_key, {}).get("prompt", "long hair")
        
    # Apply dynamic coloration replacements
    if "redhead" in active_profile.lower() or "neptune" in active_profile.lower():
        raw_hair = raw_hair.replace("black hair", "ginger orange hair").replace("dark hair", "ginger orange hair")
    pm["hair"] = f"({raw_hair}:1.5)"

    # Compile array loops for accessory strings maps updates
    acc_keys = wardrobe.get("accessories", [])
    if isinstance(acc_keys, list):
        resolved = [f"({manifest.get('accessories', {}).get(a, {}).get('prompt', '')}:1.3)" for a in acc_keys]
        pm["accessories"] = ", ".join([r for r in resolved if "():1.3" not in r])

    # Gather separate garments vectors into the single prompt mesh block
    clothing_list = [pm["top"], manifest.get("bottoms", {}).get(wardrobe.get("bottom"), {}).get("prompt", ""), pm["outerwear"], manifest.get("socks", {}).get(wardrobe.get("socks"), {}).get("prompt", ""), manifest.get("shoes", {}).get(wardrobe.get("shoes"), {}).get("prompt", "")]
    compiled_clothing = ", ".join([c for c in clothing_list if c])

    # Build structural high-fidelity rendering text modifiers
    render_modifiers = "3d game asset mesh, square enix cgi style, final fantasy vii remake style, video game graphics, crisp clean unreal engine 5 render, smooth digital skin textures, highly detailed 3d polygonal model, ambient occlusion, depth of field, professional cinematic studio lighting"
    
    # Compile the ultimate master positive matrix array layout block
    full_positive = f"masterpiece, best quality, {character_baseline}, {pm['hair']}, {compiled_clothing}, {pm['piercings']}, {pm['accessories']}, {pm['jewelry']}, {pm['makeup']}, {pm['nails']}, {pm['pose']}, {pm['expression']}, {camera_comp}, {pm['location']}, {render_modifiers}"

    # Hardcoded character profile color bleeding negative overrides filters
    hair_color_filter = ""
    if "neptune" in active_profile.lower() or "redhead" in active_profile.lower():
        hair_color_filter = "black hair, dark hair, brown hair, brunette, white hair, silver hair, blonde hair, "

    phone_filter = "holding a phone, hand holding camera, cellphone visible, " if not allow_mirror_phone else ""
    negative_base = "lowres, worst quality, 2d anime, drawing, illustration, cartoon, flat colors, lineart, deformed hands, extra fingers"
    
    # Securely append dynamic custom negative injections (e.g. topless anti-clothing requirements)
    full_negative = f"{phone_filter}{hair_color_filter}{custom_negative + ', ' if custom_negative else ''}{negative_base}"

    # Clear short-term override metadata tracks immediately to clean the palette for subsequent standard turns
    for key in ["last_camera_composition", "last_negative_override", "allow_mirror_phone"]:
        if key in current_state["meta"]: del current_state["meta"][key]
    
    from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
    await save_neptune_state(base_http, current_state)

    # Dispatch transactions down the conduit link to the websocket dispatch engine
    import neptune.body.comfy_dispatch
    return await neptune.body.comfy_dispatch.execute_comfy_generation_dispatch(
        pipe_instance=pipe_instance,
        target_host=target_host,
        base_http=base_http,
        full_positive=full_positive,
        full_negative=full_negative,
        current_state=current_state
    )