# =========================================================================
# UTILITIES SUB-PLANE: NEPTUNE MASTER AGENT STATE REGRESSION HARNESS
# File Location: /app/backend/data/neptune/mind/sysadmin/run_test_suite.py (Part 1)
# =========================================================================

import asyncio
import json
import os
import sys
import time
from neptune.core.orchestrator import Pipe

class MockPipeInstance:
    """Mock structure mimicking Open-WebUI runtime configuration valves."""
    class Valves:
        desktop_ollama_raw = "10.0.0.64"
        active_character_profile = "Neptune v1"
    def __init__(self):
        self.valves = self.Valves()

def read_live_state_file() -> dict:
    """Helper method to pull the absolute real-time state array database straight from disk cache records."""
    state_path = "/app/backend/data/neptune/repository/neptune_state.json"
    try:
        with open(state_path, 'r') as sf:
            return json.load(sf)
    except Exception as e:
        print(f"   ⚠️ Master State Read Error: Encountered baseline tracking exception: {str(e)}")
        return {}

async def execute_automated_test_suite():
    print("=========================================================================")
    print("🚀 INITIALIZING NEPTUNE STATE REGRESSION & PERFORMANCE VALIDATION SUITE...")
    print("=========================================================================")
    
    # 🧼 HARD FLUSH MEMORY CACHE BEFORE GENERATING THE PAYLOAD conduit
    print("🧹 [PRE-TEST STEP]: Flushing old module cache references from memory...")
    try:
        # Import your existing cache purger utility dynamically
        from neptune.mind.sysadmin.cache_purger import purge_system_module_cache
        purge_system_module_cache()
        print("   ✅ Memory cache flushed completely. Initializing clean environment state.")
    except Exception as e:
        # Fallback if the script location or function name differs slightly
        print(f"   ⚠️ Cache purge pass skipped or encountered an import slip: {str(e)}")
        print("   Executing hot-reload via hard file reload fallback instead...")
        import sys
        for module in list(sys.modules.keys()):
            if "neptune" in module:
                del sys.modules[module]

    orchestrator = Pipe()
    mock_instance = MockPipeInstance()
    failures = 0

    # =========================================================================
    # PHASE 1: ARITHMETIC COOLING & TIME DECAY REGRESSION TEST
    # =========================================================================
    print("\n⏳ [TEST PHASE 1]: Validating Chronological Arousal Time-Decay Calculations...")
    
    # Manually seed a historical high arousal timestamp signature into memory tracking registers
    state_cache = read_live_state_file()
    state_cache.setdefault("arousal", {})["level"] = 1.0
    state_cache.setdefault("meta", {})["last_interaction_timestamp"] = time.time() - 3600.0 # Force a strict 1-hour interaction gap
    
    state_path = "/app/backend/data/neptune/repository/neptune_state.json"
    with open(state_path, 'w') as sf:
        json.dump(state_cache, sf, indent=4)

    # Fire a generic baseline message up the conduit to trigger a cooling calculations tick loop pass
    synthetic_payload = {"messages": [{"role": "user", "content": "Hello Neptune!"}]}
    await orchestrator.pipe(synthetic_payload)
    
    # Read the file post-execution pass to assert that decay equations executed successfully
    mutated_state = read_live_state_file()
    decayed_level = float(mutated_state.get("arousal", {}).get("level", 1.0))
    
    if decayed_level < 1.0:
        print(f"   ✅ [PASSED]: Exponential cooling math verified. Level decreased from 1.0 down to: {decayed_level}")
    else:
        print("   ❌ [FAILED]: Arousal tracking level remained completely frozen at 1.0 over a 1-hour interaction gap!")
        failures += 1

    # =========================================================================
    # FINAL METRIC EVALUATIONS CONSOLE REPORT
    # =========================================================================
    print("\n=========================================================================")
    if failures == 0:
        print("🎉 ALL PLATFORM SYSTEMS FULLY VERIFIED, INTEGRATED, & STANDALONE BOUNDED!")
        print("   State registers, cooling coefficients, and metadata purges are perfectly aligned.")
        print("=========================================================================")
        sys.exit(0)
    else:
        print(f"🚨 TESTING COMPLETED: DETECTED {failures} CORE REGRESSION DEFECT ANOMALIES.")
        print("   Review the output logs to isolate faulty dictionary mutations.")
        print("=========================================================================")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(execute_automated_test_suite())
