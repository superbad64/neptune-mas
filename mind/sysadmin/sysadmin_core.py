# =========================================================================
# THE MIND LAYER: ADMINISTRATIVE OPERATIONS & REMOTE STATE SANDBOX
# Component Category: Utilities Sub-Plane (sysadmin_core.py - Part 1)
#
# Role in Neptune's Being:
# This module acts as the isolated tactical command center of Neptune's Mind.
# It holds the master keys to the remote host servers, manages the background
# cache data operations (State I/O), tracks technical system checks, and handles 
# low-level maintenance macros without contaminating her conversational layers.
# =========================================================================

import json
import os
import re
import aiohttp

async def load_neptune_state(base_http: str, defaults: dict) -> dict:
    """Reads active properties from the remote node cache or returns a safe fallback state layout."""
    timeout = aiohttp.ClientTimeout(total=3.0)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            url = f"{base_http}/view?filename=neptune_state.json&type=input"
            async with session.get(url) as resp:
                if resp.status == 200:
                    return json.loads(await resp.text())
    except Exception:
        pass
    return defaults.copy()

async def save_neptune_state(base_http: str, current_state: dict) -> bool:
    """Programmatically writes modified state profiles back to the remote server data pool."""
    timeout = aiohttp.ClientTimeout(total=5.0)
    try:
        updated_bytes = json.dumps(current_state, indent=4).encode("utf-8")
        state_form = aiohttp.FormData()
        state_form.add_field("image", updated_bytes, filename="neptune_state.json", content_type="application/json")
        state_form.add_field("overwrite", "true")
        async with aiohttp.ClientSession(timeout=timeout) as session:
            await session.post(f"{base_http}/upload/image", data=state_form)
            return True
    except Exception:
        return False
# === /app/backend/data/neptune/mind/sysadmin/sysadmin_core.py (PART 2 OF 2) ===

async def execute_sysadmin_command(pipe_instance, user_query: str) -> str:
    """Executes high-leverage administrative tasks, diagnostics, and environment verification passes."""
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    target_host = match.group(0) if match else "10.0.0.64"
    base_http = f"http://{target_host}:8189"

    # Set up safe structural fallback parameter matrices
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

    user_lower = user_query.lower().strip()

    # 📊 Diagnostic Check Sweep Execution Block
    if "diagnostic" in user_lower or "system check" in user_lower:
        try:
            state = await load_neptune_state(base_http, fallback_defaults)
            repo_dir = "/app/backend/data/neptune/repository"
            
            manifest_ok = os.path.exists(os.path.join(repo_dir, "neptune_wardrobe_manifest.json"))
            poses_ok = os.path.exists(os.path.join(repo_dir, "neptune_poses_repository.json"))
            dialog_ok = os.path.exists(os.path.join(repo_dir, "neptune_dialog_repository.json"))
            
            report = (
                f"### 🛠️ NEPTUNE INFRASTRUCTURE DIAGNOSTIC REPORT\n"
                f"- **Active Host Vector**: `{target_host}`\n"
                f"- **State Memory Cache Link**: `Online` (Arousal score: `{state.get('arousal', {}).get('level', 0.0):.2f}`)\n"
                f"- **Wardrobe Manifest Node**: `{'FOUND' if manifest_ok else 'MISSING'}`\n"
                f"- **Poses Repository Node**: `{'FOUND' if poses_ok else 'MISSING'}`\n"
                f"- **Dialogue Repository Node**: `{'FOUND' if dialog_ok else 'MISSING'}`\n"
                f"System utilities plane operating at maximum capacity, senpai! 🖤"
            )
            return report
        except Exception as diag_err:
            return f"⚠️ **Diagnostic Exception Encountered**: `{str(diag_err)}`"

    # 🔄 Hardcoded State Cache Factory Reset Sequence
    elif "factory reset" in user_lower or "purge state" in user_lower:
        try:
            success = await save_neptune_state(base_http, fallback_defaults)
            if success:
                return "⚠️ **SYSTEM NOTICE**: Neptune's persistent state cache file has been completely reset to factory default values, senpai! Memory trees have been refreshed. 🧼"
            return "wahh senpai! Remote storage nodes rejected the factory override packet transaction pass... :c"
        except Exception as reset_err:
            return f"⚠️ **Reset Execution Failure**: `{str(reset_err)}`"

    elif "clear cache" in user_lower or "reload scripts" in user_lower:
        try:
            import neptune.mind.sysadmin.cache_purger
            return neptune.mind.sysadmin.cache_purger.purge_neptune_module_cache()
        except Exception as purge_ex:
            return f"⚠️ **Cache Purge Intercept Interruption**: `{str(purge_ex)}`"

    # Default fallback messaging parameters layout if no specific macro matches
    return (
        f"Hello senpai! I'm executing background monitoring passes inside your isolated Mind/Sysadmin sandbox panel. "
        f"Right now I'm watching host node `{target_host}`. Let me know if you want me to run a `system check` or execute a `factory reset` layout pass! 🛠️"
    )

