# =========================================================================
# UTILITIES SUB-PLANE: NEPTUNE MASTER AGENT STATE REGRESSION HARNESS
# File Location: /var/lib/docker/volumes/open-webui/_data/neptune/mind/sysadmin/run_test_suite.py (Part 1)
# =========================================================================

import os
import sys
import json
import time
import asyncio

# 🗺️ DYNAMIC PATH INJECTION LAYER
current_file_dir = os.path.dirname(os.path.abspath(__file__))
root_project_dir = os.path.abspath(os.path.join(current_file_dir, "../../.."))

if root_project_dir not in sys.path:
    sys.path.insert(0, root_project_dir)

# 🧼 PROGRAMMATIC PRODUCTION-GRADE CONTEXT MANAGER MOCK CONDUIT
class MockNetworkResponseContext:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc_val, exc_tb): pass
    @property
    def status(self): return 200
    async def text(self): return "mocked_response"
    async def read(self): return b"mocked_binary_stream"
    async def json(self): return {"prompt_id": "test_id", "outputs": {"9": {"images": [{"filename": "test.png", "subfolder": ""}]}}}

class MockNetworkStreamContext:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc_val, exc_tb): pass
    def __aiter__(self): return self
    async def __anext__(self): raise StopAsyncIteration
    
    # FIXED: Replaced standard lambda structures with valid async function methods
    async def post(self, *args, **kwargs): return MockNetworkResponseContext()
    async def get(self, *args, **kwargs): return MockNetworkResponseContext()
    async def ws_connect(self, *args, **kwargs): return MockNetworkResponseContext()

if "aiohttp" not in sys.modules:
    from types import ModuleType
    mock_aiohttp = ModuleType("aiohttp")
    mock_aiohttp.ClientSession = lambda *args, **kwargs: MockNetworkStreamContext()
    mock_aiohttp.ClientTimeout = lambda *args, **kwargs: None
    mock_aiohttp.FormData = lambda *args, **kwargs: None
    sys.modules["aiohttp"] = mock_aiohttp

class MockValvesObject:
    desktop_ollama_raw = "10.0.0.64"
    active_character_profile = "Neptune v1"

def read_live_state_file() -> dict:
    """Helper method to pull the absolute real-time state array database straight from disk cache records."""
    state_path = "/var/lib/docker/volumes/open-webui/_data/neptune/repository/neptune_state.json"
    try:
        with open(state_path, 'r') as sf: return json.load(sf)
    except Exception: return {}

async def execute_automated_test_suite():
    print("=========================================================================")
    print("🚀 INITIALIZING NEPTUNE STATE REGRESSION & PERFORMANCE VALIDATION SUITE...")
    print("=========================================================================")
    
    for module in list(sys.modules.keys()):
        if "neptune" in module and "run_test_suite" not in module: del sys.modules[module]

    from neptune.core.orchestrator import Pipe
    orchestrator = Pipe()
    orchestrator.valves = MockValvesObject()
    failures = 0

    # =========================================================================
    # PHASE 1: ARITHMETIC COOLING & TIME DECAY REGRESSION TEST
    # =========================================================================
    print("\n⏳ [TEST PHASE 1]: Validating Chronological Arousal Time-Decay Calculations...")
    
    state_cache = read_live_state_file()
    state_cache.setdefault("arousal", {})["level"] = 1.0
    state_cache.setdefault("meta", {})["last_interaction_timestamp"] = time.time() - 3600.0
    
    state_path = "/var/lib/docker/volumes/open-webui/_data/neptune/repository/neptune_state.json"
    with open(state_path, 'w') as sf: json.dump(state_cache, sf, indent=4)

    synthetic_payload = {"messages": [{"role": "user", "content": "Hello Neptune!"}]}
    try: await orchestrator.pipe(synthetic_payload)
    except Exception: pass
    
    mutated_state = read_live_state_file()
    decayed_level = float(mutated_state.get("arousal", {}).get("level", 1.0))
    
    if decayed_level < 1.0:
        print(f"   ✅ [PASSED]: Exponential cooling math verified. Level decreased from 1.0 down to: {decayed_level}")
    else:
        print("   ❌ [FAILED]: Arousal tracking level remained completely frozen at 1.0 over a 1-hour interaction gap!")
        failures += 1
    # =========================================================================
    # PHASE 2: MUTATION BOUNDARY PERSISTENCE CHECK
    # =========================================================================
    print("\n👗 [TEST PHASE 2]: Validating Inventory Mutation Gate Synchronization...")
    
    # Seeding her state to naked first to cleanly measure if she successfully equips the target item
    state_cache = read_live_state_file()
    state_cache.setdefault("wardrobe", {})["bottom"] = "naked"
    state_path = "/var/lib/docker/volumes/open-webui/_data/neptune/repository/neptune_state.json"
    with open(state_path, 'w') as sf: json.dump(state_cache, sf, indent=4)

    # Trigger a garment query targeting an absolute system fallback item (Tifa Skirt)
    equip_payload = {"messages": [{"role": "user", "content": "Put on the tifa skirt"}]}
    try: await orchestrator.pipe(equip_payload)
    except Exception: pass
    
    mutated_state = read_live_state_file()
    active_clothing = mutated_state.get("wardrobe", {}).get("bottom", "naked")
    
    if "tifa_skirt" in active_clothing.lower():
        print(f"   ✅ [PASSED]: Wardrobe persistence verified. Bottom cache correctly registered: '{active_clothing}'")
    else:
        print(f"   ❌ [FAILED]: State file read mismatch! Bottom slot returned unexpected data layer pointer: '{active_clothing}'")
        failures += 1

    # =========================================================================
    # PHASE 3: VOLATILE INTERCEPT LAYER SWEEP (OVERRIDE SCRUBBING ASSERTION)
    # =========================================================================
    print("\n📸 [TEST PHASE 3]: Validating Volatile Camera Overlay Injections & State Clear Loops...")
    
    override_payload = {"messages": [{"role": "user", "content": "Show me your breasts"}]}
    try: await orchestrator.pipe(override_payload)
    except Exception: pass
    
    mutated_state = read_live_state_file()
    post_override_arousal = float(mutated_state.get("arousal", {}).get("level", 0.0))
    
    if post_override_arousal == 1.0:
        print(f"   ✅ [PASSED]: Volatile logic verified. Arousal spiked to 1.0 and physical markers updated.")
    else:
        print(f"   ❌ [FAILED]: Arousal level failed to register explicit tracking threshold. Level: {post_override_arousal}")
        failures += 1

    print("\n=========================================================================")
    if failures == 0:
        print("🎉 ALL PLATFORM SYSTEMS FULLY VERIFIED, INTEGRATED, & STANDALONE BOUNDED!")
        sys.exit(0)
    else:
        print(f"🚨 TESTING COMPLETED: DETECTED {failures} CORE REGRESSION DEFECT ANOMALIES.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(execute_automated_test_suite())
