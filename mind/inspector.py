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
    repo_dir = "/app/backend/data/neptune/repository"
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

async def process_wardrobe_mutations_and_routing(pipe_instance, raw_query: str, current_state: dict) -> tuple:
    """Primary entry interface for the inspector routine. Handles check interceptions and outfit/hair mutations."""
    clean_query = raw_query.lower().strip()

    # 1. Outfit rundown check
    intercepted, report_payload = await evaluate_outfit_interception(clean_query, current_state)
    if intercepted:
        return True, report_payload

    # 2. Overrides processor loop ("show me" behaviors)
    from neptune.mind.override_processor import evaluate_visual_overrides
    intercepted_override, override_render_data = await evaluate_visual_overrides(pipe_instance, raw_query, current_state)
    if intercepted_override:
        return True, override_render_data

    # Load centralized lookup database registry arrays
    repo_dir = "/app/backend/data/neptune/repository"
    triggers_path = os.path.join(repo_dir, "neptune_interaction_triggers.json")
    manifest_path = os.path.join(repo_dir, "neptune_wardrobe_manifest.json")
    
    try:
        with open(triggers_path, 'r') as tf, open(manifest_path, 'r') as mf:
            triggers = json.load(tf)
            manifest = json.load(mf)
    except Exception:
        return False, ""

    # 2.5. Strict Word-Boundary Reshoot Routing
    reshoot_phrases = triggers.get("reshoot_triggers", ["reshoot", "take it again"])
    is_strict_reshoot = any(re.search(r'\b' + re.escape(phrase) + r'\b', clean_query) for phrase in reshoot_phrases)
    if_strict_reshoot = is_strict_reshoot  # safety padding alias
    if is_strict_reshoot:
        from neptune.body.reshoot_worker import execute_physical_image_reshoot
        reshoot_render_markdown = await execute_physical_image_reshoot(pipe_instance, raw_query, [], current_state)
        return True, reshoot_render_markdown

    # BRANCH E: PURE IMAGE GENERATION / SELFIE INTERCEPT GATE
    gen_triggers = triggers.get("generation_triggers", {}).get("capture_commands", ["take a selfie", "take a picture"])
    if any(phrase in clean_query for phrase in gen_triggers):
        from neptune.body.pipeline_compiler import trigger_body_render
        render_output_markdown = await trigger_body_render(pipe_instance, raw_query, [])
        return True, render_output_markdown

    m_triggers = triggers.get("outfit_mutations", {})
    h_triggers = triggers.get("hair_mutations", {})
    wardrobe = current_state.setdefault("wardrobe", {})
    cosmetics = current_state.setdefault("cosmetics", {})
    state_mutated = False

    # BRANCH A: GO NUDE SYSTEM SHORT-CIRCUIT
    if any(k in clean_query for k in m_triggers.get("nude_keywords", [])):
        for slot in ["outerwear", "top", "bottom", "bra", "panties", "socks", "shoes"]: wardrobe[slot] = "naked"
        wardrobe["accessories"] = []
        wardrobe["jewelry"] = "none"
        state_mutated = True

    # BRANCH B: EQUIP COMMANDS ("PUT ON")
    elif any(k in clean_query for k in m_triggers.get("equip_keywords", [])):
        outfits_pool = manifest.get("outfits", {})
        outfit_found = None
        
        # Apply your specified "s" token replacement rule to handle possessives cleanly
        sanitized_query = clean_query.replace("'s", "s").replace("s'", "s")
        
        for name in outfits_pool.keys():
            outfit_data = outfits_pool[name]
            triggers_list = outfit_data.get("triggers", [name])
            
            # Check both explicit trigger words arrays or raw manifest object key tokens
            has_trigger_match = any(t.lower() in sanitized_query for t in triggers_list)
            if has_trigger_match or name.lower().replace("_", " ") in sanitized_query:
                outfit_found = outfit_data
                break
        
        if outfit_found:
            items = outfit_found.get("items", outfit_found)
            wardrobe["top"] = items.get("top", items.get("tops", "naked"))
            wardrobe["bottom"] = items.get("bottom", items.get("bottoms", "naked"))
            wardrobe["bra"] = items.get("bra", items.get("bras", "naked"))
            wardrobe["panties"] = items.get("panties", items.get("panties_layer", "naked"))
            wardrobe["socks"] = items.get("socks", items.get("hosiery", "naked"))
            wardrobe["shoes"] = items.get("shoes", items.get("boots", "naked"))
            wardrobe["accessories"] = items.get("accessories", [])
            wardrobe["outerwear"] = "naked"
            state_mutated = True
        else:
            for category, items_dict in manifest.items():
                if category == "outfits": continue
                for item_key in items_dict.keys():
                    if item_key.lower().replace("_", " ") in sanitized_query:
                        slot_map = {"tops": "top", "bottoms": "bottom", "bras": "bra", "panties": "panties", "socks": "socks", "shoes": "shoes", "jewelry": "jewelry", "outerwear": "outerwear"}
                        target_slot = slot_map.get(category)
                        if target_slot:
                            wardrobe[target_slot] = item_key
                            state_mutated = True
                            break

    # BRANCH C: STRIP / SWAP ACTIONS
    elif any(k in clean_query for k in m_triggers.get("strip_keywords", [])) or any(k in clean_query for k in m_triggers.get("swap_keywords", [])):
        slot_keywords = {
            "outerwear": ["outerwear", "coat", "jacket"],
            "top": ["top", "shirt", "blouse", "tank", "clothes"],
            "bottom": ["bottom", "skirt", "pants", "shorts", "trousers"],
            "bra": ["bra", "brassiere", "underwear top"],
            "panties": ["panties", "underwear", "panties layer", "string"],
            "socks": ["socks", "stockings", "thigh highs"],
            "shoes": ["shoes", "boots", "footwear"]
        }
        for slot, keywords in slot_keywords.items():
            if any(k in clean_query for k in keywords):
                wardrobe[slot] = "naked"
                state_mutated = True

    # BRANCH D: HAIRSTYLE DYNAMIC TRANSITIONS
    if any(k in clean_query for k in h_triggers.get("hair_down_triggers", [])):
        cosmetics["hair_style"] = "default_scene"
        state_mutated = True
    elif any(p in clean_query for p in h_triggers.get("style_prefix", [])):
        if any(b in clean_query for b in h_triggers.get("bun", [])): cosmetics["hair_style"] = "high_bun"
        elif any(p in clean_query for p in h_triggers.get("ponytail", [])): cosmetics["hair_style"] = "high_ponytail"
        elif any(t in clean_query for t in h_triggers.get("twintails", [])): cosmetics["hair_style"] = "twintails"
        elif any(br in clean_query for br in h_triggers.get("braid", [])): cosmetics["hair_style"] = "braid"
        state_mutated = True

    # PERSISTENCE HANDSHAKE SYNC LAYER
    if state_mutated:
        raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
        match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
        target_host = match.group(0) if match else "10.0.0.64"
        base_http = f"http://{target_host}:8189"
        
        from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
        await save_neptune_state(base_http, current_state)
        
        _, structural_report = await evaluate_outfit_interception("outfit check", current_state)
        return True, structural_report

    return False, ""