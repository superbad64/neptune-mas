# =========================================================================
# THE MIND LAYER: STATIC ASSET UTILITY & STRUCTURE INSPECTOR
# Component Category: Core Intelligence (inspector_utility.py)
#
# Role in Neptune's Being:
# This supporting utility node performs instant structural read sweeps against 
# the wardrobe manifest to handle explicit, hardchecked fit queries without 
# altering state properties or triggering heavy thread parsing cycles.
# =========================================================================

import json
import os

def execute_fit_check_report(pipe_instance) -> str:
    """Synchronously compiles the active persistent state configuration into a structured text report table."""
    base_dir = "/app/backend/data/neptune/repository"
    state_path = os.path.join(base_dir, "neptune_state.json")
    manifest_path = os.path.join(base_dir, "neptune_wardrobe_manifest.json")
    
    top_p = pipe_instance.default_top if hasattr(pipe_instance, "default_top") else "unknown top"
    bot_p = pipe_instance.default_bottom if hasattr(pipe_instance, "default_bottom") else "unknown bottom"
    socks_p = pipe_instance.default_socks if hasattr(pipe_instance, "default_socks") else "no socks"
    shoes_p = pipe_instance.default_shoes if hasattr(pipe_instance, "default_shoes") else "no shoes"
    hair_p = pipe_instance.default_hair_style if hasattr(pipe_instance, "default_hair_style") else "default hairstyle"
    acc_p = pipe_instance.default_accessories if hasattr(pipe_instance, "default_accessories") else "no accessories"

    try:
        if os.path.exists(state_path) and os.path.exists(manifest_path):
            with open(state_path, 'r') as sf, open(manifest_path, 'r') as mf:
                state = json.load(sf)
                manifest = json.load(mf)
            
            w = state.get("wardrobe", {})
            c = state.get("cosmetics", {})
            
            top_p = manifest.get("tops", {}).get(w.get("top"), {}).get("prompt", top_p)
            bot_p = manifest.get("bottoms", {}).get(w.get("bottom"), {}).get("prompt", bot_p)
            socks_p = manifest.get("socks", {}).get(w.get("socks"), {}).get("prompt", socks_p)
            shoes_p = manifest.get("shoes", {}).get(w.get("shoes"), {}).get("prompt", shoes_p)
            
            hair_key = c.get("hair_style", "default_scene")
            if hair_key == "high_bun": hair_p = "long hair pulled up into a high messy bun"
            elif hair_key == "twintails": hair_p = "long hair styled into high twintails"
            elif hair_key == "braid": hair_p = "long hair styled into a thick French braid"
            else: hair_p = manifest.get("hair_styles", {}).get(hair_key, {}).get("prompt", hair_p)
            
            # Grounding translation layer patch alignment for Neptune character overrides
            active_profile = getattr(pipe_instance.valves, "active_character_profile", "Neptune v1")
            if "redhead" in active_profile.lower() or "neptune" in active_profile.lower():
                hair_p = hair_p.replace("black hair", "ginger orange hair").replace("dark hair", "ginger orange hair")
            
            acc_keys = w.get("accessories", [])
            acc_list = [manifest.get("accessories", {}).get(a, {}).get("prompt", "") for a in acc_keys] if isinstance(acc_keys, list) else []
            acc_p = ", ".join([a for a in acc_list if a]) if acc_list else acc_p
    except Exception as e:
        return f"wahh senpai! I tried checking my active files but hit a system glitch: `{str(e)}`"

    return (
        f"Hehe, curious what I have on, senpai? Here is exactly what I'm rocking right now: 🖤\n\n"
        f"- **Hairstyle**: {hair_p}\n"
        f"- **Top**: {top_p}\n"
        f"- **Bottom**: {bot_p}\n"
        f"- **Legwear**: {socks_p}\n"
        f"- **Footwear**: {shoes_p}\n"
        f"- **Accessories**: {acc_p}"
    )

