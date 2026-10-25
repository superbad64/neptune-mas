# =========================================================================
# THE MIND LAYER: SYSTEM UTILITY ENGINE & MODULE REFRESH PURGER
# Component Category: Utilities Sub-Plane Sandbox (cache_purger.py)
#
# Role in Neptune's Being:
# This script represents Neptune's mental housecleaner macro. Its singular
# operational mandate is to scan Python's runtime memory state, flush out 
# cached system handles, and force a fresh execution reload pass across all
# sub-directories without needing to bounce or restart the Open-WebUI container.
# =========================================================================

import sys

def purge_neptune_module_cache() -> str:
    """Programmatically clears active internal cache keys out of the local system memory array table."""
    target_modules = [
        "neptune.core.orchestrator",
        "neptune.mind.inspector",
        "neptune.mind.inspector_utility",
        "neptune.mind.sysadmin.sysadmin_core",
        "neptune.body.pipeline_compiler",
        "neptune.body.comfy_dispatch",
        "neptune.soul.mood_engine",
        "neptune.soul.chatter.chatter_core"
    ]
    
    purged_count = 0
    for mod in list(sys.modules.keys()):
        if any(mod.startswith(target) for target in target_modules):
            del sys.modules[mod]
            purged_count += 1
            
    return f"🧹 **System Purge Macro Complete**: Successfully flushed `{purged_count}` live namespace module references out of Python memory cache buffers, senpai! Next transaction pass will compile completely fresh from disk hooks."

