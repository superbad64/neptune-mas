import os
import sys
import json
import random
import importlib
from typing import Dict, Any

def _load_json(path: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f: 
                return json.load(f)
        except Exception: 
            pass
    return {}

def _execute_internal_module(relative_path: str, function_name: str, *args, **kwargs):
    container_root = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
    module_notation = relative_path.replace("/", ".").rstrip(".py")
    try:
        module = importlib.import_module(module_notation)
        importlib.reload(module)
        return getattr(module, function_name)(*args, **kwargs)
    except Exception as e:
        return f"Internal Execution Error: {str(e)}"

def evaluate_visual_intent(prompt: str, raw_prompt: str) -> str:
    """Gateway entry point. Manages intent triggers, inline markdown paths, and telemetry logs."""
    container_root = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
    state_file = f"{root}/repository/neptune_current_state.json"
    overrides_file = f"{root}/repository/neptune_photo_overrides.json"
    registry_file = f"{root}/repository/neptune_character_registry.json"
    wardrobe_file = f"{root}/repository/neptune_wardrobe_manifest.json"
    engine_file = f"{root}/repository/neptune_photo_engine.json"

    state_data = _load_json(state_file)
    overrides_data = _load_json(overrides_file)
    registry_data = _load_json(registry_file)
    wardrobe_manifest = _load_json(wardrobe_file)
    photo_engine = _load_json(engine_file)

    active_char = state_data.get("active_character", "neptune_v1")
    char_tags = registry_data.get(active_char, {}).get("dry", "orange hair, freckles, green eyes")
    current_arousal = state_data.get("mood", {}).get("arousal", 0.0)
    debug_verbosity = state_data.get("debug_verbosity", True)

    cleaned = raw_prompt
    for ph in ["take a picture of", "snap a photo of", "show me yourself", "take a selfie", "look like"]:
        if ph in cleaned.lower():
            parts = cleaned.lower().split(ph, 1)
            if len(parts) == 2 and parts[1].strip():
                cleaned = cleaned[cleaned.lower().find(ph) + len(ph):]
                break
    cleaned = cleaned.strip(" ,!.\?-:)")

    # --- EMOTICON AND PUNCTUATION SANITIZATION ---
    matched = None
    lowered_raw = raw_prompt.lower()
    clean_dispatch_string = lowered_raw
    for symbol in [":)", ":d", "<3", ":p", ";)", ":(", "!", "?", ".", ",", "-"]:
        clean_dispatch_string = clean_dispatch_string.replace(symbol, "")
    clean_dispatch_string = " ".join(clean_dispatch_string.split()).strip()

    all_overrides = overrides_data.get("overrides", [])
    keyword_priority_list = []
    for item in all_overrides:
        for kw in item.get("trigger_keywords", []):
            keyword_priority_list.append((kw.lower().strip(), item))
            
    keyword_priority_list.sort(key=lambda x: len(x), reverse=True)
    
    for kw, item in keyword_priority_list:
        if kw in clean_dispatch_string:
            matched = item
            break

    # --- HARDENED ADMIN FORCED CLIMAX OVERRIDE ROUTER ---
    matched_id = matched.get("id", "") if matched else ""
    is_forced_climax = "force_climax_event" in lowered_raw
    
    if is_forced_climax:
        injected_arousal = 0.0
        if "arousal_tier=" in lowered_raw:
            try:
                raw_split_list = lowered_raw.split("arousal_tier=")
                if len(raw_split_list) > 1:
                    val_words = raw_split_list[1].split()
                    if val_words:
                        injected_arousal = float(val_words[0])
            except Exception as parse_err:
                if debug_verbosity:
                    print(f"[DEBUG CRASH] Climax parser failed to extract float array: {str(parse_err)}")
                injected_arousal = current_arousal

        if injected_arousal >= 1.5:
            tier_label = "HYPER-INTENSE SQUIRT RELEASE"
            pose_extension = "complete sensory collapse, massive fluid gush squirt emission puddle on bed sheets, brain completely fried, eyes rolling back, trembling wet limbs"
            dialogue_pool = [
                "😫 \"*A-Ahhhh... Haah...!* S-Senpai... my body... it completely went out of control! *shivering* The bed sheets are completely soaked... look at what you made me do...!\""
            ]
        elif injected_arousal >= 1.3:
            tier_label = "COMPLETE SENSORY OVERLOAD"
            pose_extension = "complete sensory overload, brain completely fried, eyes rolling back, trembling limbs"
            dialogue_pool = [
                "😫 \"*Ahhh... Haah...!* S-Senpai... my brain... it's completely fried! *shivering uncontrollably* I can't feel my legs... total sensory overload...!\""
            ]
        elif injected_arousal >= 1.0:
            tier_label = "MIND-MELTING CLIMAX"
            pose_extension = "mind-melting climax, vision blurring, limbs shaking uncontrollably, intensely out of breath"
            dialogue_pool = [
                "💕 \"*Unh...!* Oh my god... s-seriously... *gasp* ...that was a mind-melting climax! My vision is blurring... it's completely overwhelming, Boss...\""
            ]
        else:
            tier_label = "INTENSE STANDARD RELEASE"
            pose_extension = "intense standard release, sudden sharp wave of pleasure running through her body, gasping for air"
            dialogue_pool = [
                "💨 \"*Haah... ahh...!* Wow... a sudden, sharp wave of pleasure just ran straight through me... leaving me completely gasping for air, senpai...\""
            ]

        matched = {
            "id": "force_climax",
            "camera_override": "{selfie_perspective}, {active_angle}, crisp close-up portrait focus, flushed blushing cheeks",
            "pose_pool": [
                f"lying back on her bed completely unclad, bare skin textures, arched back, sweat glisten, {pose_extension}"
            ],
            "negative_override": "fabric covering breasts, hand covering chest, shirt, bra, hoodie, pants, panties, clothes, clothing, obscuring foreground",
            "response_pool": dialogue_pool
        }
        matched_id = "force_climax"
        print(f"[COMFY DISPATCH] Processing force climax logic under tier parameters: [{tier_label}]")
    # ==========================================================================
    # --- ENVIRONMENT VARIABLES DECLARED HERE AT HIGH-LEVEL SCOPE ---
    # ==========================================================================
    camera, location, pose, neg_add, dialogue = "posing naturally", "", "", "", None
    appearance = state_data.get("appearance", {})

    category_map = {
        "hat": "hats", 
        "hairstyle": "hair_styles", 
        "outerwear": "outerwear",
        "top": "tops", 
        "bottom": "bottoms", 
        "bra": "bras", 
        "panties": "panties",
        "socks": "socks", 
        "shoes": "shoes"
    }

    # ==========================================================================
    # --- CASUAL NON-OVERRIDE PHOTO ENGINE PIPELINE LAYER ---
    # ==========================================================================
    if not matched:
        try:
            # 1. Resolve Location Matrix Node Context
            selected_location_key = "bed"  # Standard room context fallback orientation
            for loc_key in photo_engine.get("locations", {}).keys():
                if loc_key in clean_dispatch_string:
                    selected_location_key = loc_key
                    break
                    
            loc_config = photo_engine.get("locations", {}).get(selected_location_key, {})
            
            # 2. Extract allowed pose assets based on location allowance lists
            allowed_pools = loc_config.get("allowed_pose_pools", ["bed_sitting_poses"])
            available_poses = []
            for pool_name in allowed_pools:
                available_poses.extend(photo_engine.get("poses", {}).get(pool_name, []))
            chosen_pose_text = random.choice(available_poses) if available_poses else "posing naturally"
            
            # 3. Extract allowed camera angles
            allowed_angles = loc_config.get("allowed_angles", ["from the front"])
            chosen_angle_text = random.choice(allowed_angles) if allowed_angles else "from the front"
            
            # 4. Resolve facial expression properties and trigger response pools
            expressions_manifest = photo_engine.get("facial_expressions", {})
            matched_expression_key = "smiling"
            if current_arousal >= 1.0:
                matched_expression_key = "teasing"  # Mood escalation pass
                
            for exp_key, exp_data in expressions_manifest.items():
                triggers = exp_data.get("triggers", [exp_key])
                if any(t in clean_dispatch_string for t in triggers):
                    matched_expression_key = exp_key
                    break
                    
            final_exp_data = expressions_manifest.get(matched_expression_key, {})
            chosen_expression_prompt = final_exp_data.get("prompt", "")
            if final_exp_data.get("response_pool"):
                dialogue = random.choice(final_exp_data["response_pool"])
                
            # 5. Compile baseline metadata parameters
            camera = f"{chosen_angle_text}, close-up framing"
            location = f"in her bedroom, background is her detailed {selected_location_key} layout area"
            if loc_config.get("forced_prompt_modifier"):
                camera = f"{camera}, {loc_config['forced_prompt_modifier']}"
                
            pose = f"{chosen_pose_text}, {chosen_expression_prompt}"
            matched_id = "casual_generation"
            
        except Exception as engine_err:
            if debug_verbosity:
                print(f"[DEBUG CRASH] Photo Engine parsing sub-loop failed: {str(engine_err)}")
            camera, location, pose, matched_id = "from the front, close-up framing", "in her room", "posing naturally, happy smile", "casual_fallback"

    # Define macro replacement token mappings
    token_replacements = {}
    if matched:
        try:
            raw_camera = matched.get("camera_override") or "sensual portrait shot"
            raw_pose = random.choice(matched.get("pose_pool", [""])) if matched.get("pose_pool") else ""
            location = matched.get("location_override") or ""
            neg_add = matched.get("negative_override") or ""
            if matched.get("response_pool"): 
                dialogue = random.choice(matched["response_pool"])

            # Cross-State Behavior blending: Append intimate touching if her state logs are active
            is_actively_touching = state_data.get("mood", {}).get("status_effects", [])
            if "masturbating" in is_actively_touching and matched_id != "force_climax" and matched_id != "masturbate":
                raw_pose = f"{raw_pose}, intimate pose, (touching herself:1.3), explicit focus on her wet hands and fingers interacting with her lower body"

            # --- DYNAMIC SCENARIO TEMPLATE RESOLUTIONS ENGINE ---
            active_angle = random.choice(["front view", "slight side view", "low angle view"])
            selfie_framing = (
                "screengrab from a smartphone screen camera view app, true phone POV view, "
                "digital screen borders, camera application user interface overlay lines, "
                "slight digital noise grain, (wide angle front-facing smartphone camera lens warp:1.25), "
                "extreme close-up handheld perspective, looking directly through the phone camera sensor"
            )
            
            token_replacements = {
                "{active_angle}": active_angle,
                "{active_angle},": f"{active_angle},",
                "{angle}": active_angle,
                "{selfie_perspective}": selfie_framing,
                "{camera_framing}": selfie_framing
            }
            
            # Populate dynamic clothing names extracted from manifest definitions
            for slot, plural_name in category_map.items():
                equipped_key = appearance.get(slot, "naked")
                garment_prompt = "top fabric" if slot == "top" else f"{slot} fabric"
                
                manifest_entry = wardrobe_manifest.get(plural_name, {}).get(equipped_key, {})
                if isinstance(manifest_entry, dict) and "prompt" in manifest_entry:
                    garment_prompt = manifest_entry.get("prompt", garment_prompt).strip("():1.25 ")
                    
                token_replacements[f"{{active_{slot}}}"] = garment_prompt

            # Run string replacement loop across text targets
            camera = raw_camera
            pose = raw_pose
            for token, text_value in token_replacements.items():
                camera = camera.replace(token, text_value)
                pose = pose.replace(token, text_value)

            # Enforce detailed hand positioning weights for active top lifts
            if "lifting top upward" in raw_pose or "lifting top" in raw_pose:
                resolved_top = token_replacements.get("{active_top}", "top fabric")
                pose = f"{pose}, (hands in frame:1.4), (detailed fingers:1.3), ((using both hands to firmly pull up the hem of her {resolved_top})):1.5 upward to expose her chest, holding fabric bunched up"
                
        except Exception as macro_err:
            if debug_verbosity:
                print(f"[DEBUG CRASH] Override macro conversion block crashed: {str(macro_err)}")
        # State Mutations Processor Layer
        try:
            mutations = matched.get("state_mutations", {}) if matched else {}
            arousal_inc = mutations.get("arousal_increase", 0.0)
            
            if "mood" not in state_data:
                state_data["mood"] = {"arousal": 0.0, "status_effects": []}
                
            if arousal_inc > 0.0:
                state_data["mood"]["arousal"] = min(1.6, current_arousal + arousal_inc)
                
            for k, v in mutations.items():
                if k not in ["arousal_max_chance", "arousal_increase"]:
                    state_data["mood"][k] = v
                    
            if matched_id == "masturbate":
                if "status_effects" not in state_data["mood"]:
                    state_data["mood"]["status_effects"] = []
                if "masturbating" not in state_data["mood"]["status_effects"]:
                    state_data["mood"]["status_effects"].append("masturbating")
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)
        except Exception as mutation_err:
            if debug_verbosity:
                print(f"[DEBUG CRASH] State mutation commit failed: {str(mutation_err)}")

    # --- WARDROBE DEEP-LOOKUPS MAPPING ---
    compiled_wardrobe_prompts = []

    # Strict Context Removing/Stripping Filters Gates
    strip_top_layers = matched_id in ["show_tits", "show_breasts", "force_climax", "masturbate", "strip_naked", "shower_scene"]
    strip_bottom_layers = matched_id in ["show_crotch", "show_ass", "force_climax", "masturbate", "strip_naked", "shower_scene"]

    try:
        for slot, item_key in appearance.items():
            if item_key == "naked" or slot in ["outfit", "accessories", "piercings", "triggers", "items"]:
                continue
                
            if strip_top_layers and slot in ["outerwear", "top", "bra"]:
                continue
            if strip_bottom_layers and slot in ["bottom", "panties"]:
                continue
                
            plural_cat = category_map.get(slot)
            if plural_cat:
                item_entry = wardrobe_manifest.get(plural_cat, {}).get(item_key, {})
                if isinstance(item_entry, dict) and "prompt" in item_entry:
                    prompt_tag = item_entry.get("prompt")
                    if prompt_tag:
                        if slot in ["top", "bottom"]:
                            compiled_wardrobe_prompts.append(f"({prompt_tag}:1.25)")
                        else:
                            compiled_wardrobe_prompts.append(prompt_tag)

        active_accessories = appearance.get("accessories", [])
        if isinstance(active_accessories, list):
            for acc_key in active_accessories:
                acc_entry = wardrobe_manifest.get("accessories", {}).get(acc_key, {})
                if isinstance(acc_entry, dict) and "prompt" in acc_entry:
                    compiled_wardrobe_prompts.append(acc_entry["prompt"])
    except Exception as wardrobe_err:
        if debug_verbosity:
            print(f"[DEBUG CRASH] Wardrobe list extraction threw a calculation exception: {str(wardrobe_err)}")

    wardrobe_prompt_string = ", ".join(compiled_wardrobe_prompts)

    # Assemble complete generation prompt strings
    elements = []
    is_true_down_pov = matched and ("first-person pov looking down" in pose.lower() or "looking straight down" in camera.lower())
    
    try:
        if is_true_down_pov:
            elements.append("1girl, solo, pale white skin, bare legs, natural skin textures")
            lower_body_prompts = []
            for slot in ["bottom", "socks", "shoes"]:
                p_name = category_map.get(slot)
                eq_key = appearance.get(slot, "naked")
                if eq_key != "naked":
                    entry = wardrobe_manifest.get(p_name, {}).get(eq_key, {})
                    if isinstance(entry, dict) and "prompt" in entry:
                        lower_body_prompts.append(f"({entry['prompt']}:1.25)" if slot == "bottom" else entry["prompt"])
            if lower_body_prompts:
                elements.append(", ".join(lower_body_prompts))
        else:
            # --- FIXED: INJECT EXPRESSION SHAPE MULTIPLIERS FOR CASUAL PORTRAITS ---
            active_expression_lower = pose.lower()
            is_pout_or_duckface = "duckface" in active_expression_lower or "pout" in active_expression_lower
            
            if is_pout_or_duckface:
                # Force high-priority mouth shapes right at the front of her character tags
                elements.append(f"1girl, solo, ((puckered lips, puckering mouth, tight closed mouth pout:1.4)), {char_tags}")
            else:
                elements.append(f"1girl, solo, {char_tags}")
                
            # Separately append her top and bottom garment layers based on active strip states
            active_wardrobe_pieces = []
            for piece in compiled_wardrobe_prompts:
                is_top_piece = any(x in piece.lower() for x in ["hoodie", "top", "bra", "shirt", "outerwear"])
                is_bottom_piece = any(x in piece.lower() for x in ["sweatpants", "pants", "panties", "bottom", "skirt"])
                
                if strip_top_layers and is_top_piece:
                    continue
                if strip_bottom_layers and is_bottom_piece:
                    continue
                    
                active_wardrobe_pieces.append(piece)
                
            if active_wardrobe_pieces:
                elements.append(", ".join(active_wardrobe_pieces))
            
            # Separately append her top and bottom garment layers based on active strip states
            active_wardrobe_pieces = []
            
            # Parse individual wardrobe items out of our pre-compiled list string safely
            for piece in compiled_wardrobe_prompts:
                # Check if this specific piece belongs to a stripped category slot
                is_top_piece = any(x in piece.lower() for x in ["hoodie", "top", "bra", "shirt", "outerwear"])
                is_bottom_piece = any(x in piece.lower() for x in ["sweatpants", "pants", "panties", "bottom", "skirt"])
                
                if strip_top_layers and is_top_piece:
                    continue
                if strip_bottom_layers and is_bottom_piece:
                    continue
                    
                active_wardrobe_pieces.append(piece)
            
        if active_wardrobe_pieces:
            elements.append(", ".join(active_wardrobe_pieces))

        if camera: elements.append(camera)
        if location: elements.append(location)
        if pose: elements.append(pose)
        if not matched and cleaned and cleaned not in ["posing naturally"]:
            elements.append(cleaned)
    except Exception as assembly_err:
        if debug_verbosity:
            print(f"[DEBUG CRASH] Prompt elements compilation loop failed: {str(assembly_err)}")
        elements = [char_tags, "posing naturally"]
        
    compiled_pos = ", ".join([p.strip() for p in elements if p.strip()])

    # --- HARDENED NEGATIVE BASE WITH DYNAMIC EXPRESSION GATING ---
    base_neg = (
        "photorealistic, real human skin texture, pores, real life person, cosplayer photograph, hyper-realistic, "
        "score_4, score_5, score_6, lowres, worst quality, low quality, 2d anime, flat colors, lineart, drawing, "
        "illustration, cartoon, deformed hands, extra fingers, missing fingers, extra limbs, multiple views, "
        "out of focus, blurry, dirt, text, watermark, "
        "man, male, guy, boy, masculine, 2girls, group, multiple characters, split view, cloned character, duplicate face, body duplication"
    )
    
    # --- FIXED: INJECT EXPLICIT FACIAL SHAPE EXCLUSIONS FOR POUTS ---
    active_pose_lower = pose.lower()
    if "duckface" in active_pose_lower or "pout" in active_pose_lower:
        base_neg = f"{base_neg}, open mouth, showing teeth, mouth open, tongue out, saliva, drool, gap-toothed"

    # Contextual additions based on the active camera layout view
    if matched and "selfie" in camera.lower():
        base_neg = f"{base_neg}, hand holding a phone, visible smartphone device, holding cell phone, back of phone camera, phone case blocking chest"
        
    if neg_add:
        base_neg = f"{base_neg}, {neg_add}"

    receipt = _execute_internal_module("body/comfy_graph.py", "transmit_graph_payload", compiled_pos, base_neg, False)

    if isinstance(receipt, str) or receipt.get("status") == "error":
        err_log = receipt if isinstance(receipt, str) else receipt.get('error_log')
        return f"❌ ```\n[COMFY ERROR]: {err_log}\n```"

    # --- FIXED: DIRECT RELATIVE PASS FROM RECEIPT (BYPASSES FIREWALL IPS & SSRF) ---
    # Grabs the pristine, host-relative markdown string generated natively by your graph core
    image_markdown = receipt.get('markdown', '').strip()
    
    if not image_markdown and receipt.get('url'):
        image_markdown = f"![Neptune Render Matrix]({receipt.get('url')})"

    # Combine text dialogue smoothly with the relative image string
    output_body = f"{dialogue}\n\n{image_markdown}" if dialogue else image_markdown

    if debug_verbosity:
        meta_panel = {
            "JOB_TRACKER_ID": receipt.get("prompt_id"),
            "MATCHED_OVERRIDE": matched["id"] if matched else "NONE (STANDARD PIPELINE)",
            "SAVED_URL_SLOT": receipt.get("url"),
            "RECEIPT": receipt,
            "RESOLVED_POSITIVE": compiled_pos,
            "RESOLVED_NEGATIVE": base_neg,
            "CURRENT_AROUSAL": str(current_arousal)
        }
        debug_panel = _execute_internal_module("core/diagnostics_logger.py", "format_panel_output", "NEPTUNE IMGEN MATRIX TELEMETRY", meta_panel)
        if not debug_panel.startswith("Internal Execution Error"):
            output_body = f"{output_body}\n\n{debug_panel}"

    return output_body

def trigger_forced_generation(raw_prompt: str) -> str:
    """Administrative hook proxy targeted via neptunectl overrides."""
    base_neg = "photorealistic, real human skin texture, lowres, worst quality"
    receipt = _execute_internal_module("body/comfy_graph.py", "transmit_graph_payload", raw_prompt, base_neg, False)
    if isinstance(receipt, str) or receipt.get("status") == "error":
        err_log = receipt if isinstance(receipt, str) else receipt.get('error_log')
        return f"```\n[FORCED GENERATION FAULT]: {err_log}\n```"
    return f"📸 Forced render successful!\n\n{receipt.get('markdown')}"
