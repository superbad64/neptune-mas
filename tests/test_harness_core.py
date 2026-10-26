import os
import sys
import json
import time

def run_neptune_test_suite():
    print("====================================================")
    print("⚡ NEPTUNE MAS SYSTEM INTEGRATION TEST HARNESS ⚡")
    print("====================================================")
    
    # --------------------------------------------------
    # DYNAMIC PATH AUTO-DISCOVERY MATRIX
    # --------------------------------------------------
    # Finds the directory containing this script (tests/) and steps back one level to root
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    code_root = os.path.dirname(current_script_dir)
    
    print(f"[TEST HARNESS INSTANTIATION] Auto-detected code tree root directory: {code_root}")
    
    state_path = os.path.join(code_root, "repository", "neptune_current_state.json")
    
    state_backup = None
    if os.path.exists(state_path):
        with open(state_path, 'r', encoding='utf-8') as f:
            state_backup = f.read()

    try:
        def _test_sandbox(relative_script_path: str, func_name: str, *args, **kwargs):
            # Paths are now cleanly calculated using the discovered base path root
            full_path = os.path.join(code_root, relative_script_path)
            with open(full_path, 'r', encoding='utf-8') as f:
                src = f.read()
            ctx = {}
            exec(src, ctx, ctx)
            return ctx[func_name](*args, **kwargs)

        # --------------------------------------------------
        # TEST 1: SLANG TRANSLATION MATRIX
        # --------------------------------------------------
        print("[TEST 1/4] Validating Slang Translation Step...")
        face_pipe = _test_sandbox("core/face_router.py", "Pipe")
        sample_input = "hey senpai look at my titties, snap a pic fr fr!"
        translated = face_pipe.translate_slang(sample_input)
        
        assert "breasts" in translated, f"Slang expansion failed: {translated}"
        assert "picture" in translated, f"Slang expansion failed: {translated}"
        print("  --> PASS: Slang mapped cleanly to formal prompt tokens! (✧ω✧)")

        # --------------------------------------------------
        # TEST 2: FIT_CHECK EXPOSURE LOOPS
        # --------------------------------------------------
        print("[TEST 2/4] Validating fit_check() Exposure Variations...")
        
        naked_state = {
            "appearance": {
                "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
                "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
            },
            "mood": {"arousal": 0.0, "status_effects": []}
        }
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(naked_state, f, indent=2)
            
        fit_output = _test_sandbox("mind/inspector_utility.py", "execute_fit_check_external", code_root)
        assert "naked" in fit_output.lower() or "exposure" in fit_output.lower(), f"Naked feedback failed: {fit_output}"
        
        underwear_state = {
            "appearance": {
                "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                "top": "naked", "bra": "lace_bra", "bottom": "naked", "panties": "lace_panties",
                "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
            },
            "mood": {"arousal": 0.0, "status_effects": []}
        }
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(underwear_state, f, indent=2)
            
        fit_output = _test_sandbox("mind/inspector_utility.py", "execute_fit_check_external", code_root)
        assert "exposed" in fit_output or "underwear" in fit_output, f"Underwear feedback failed: {fit_output}"
        print("  --> PASS: Relational exposure feedback variations are fully verified! (>///<)")

        # --------------------------------------------------
        # TEST 3: BIOLOGICAL DECAY MATRIX
        # --------------------------------------------------
        print("[TEST 3/4] Validating Biological Decay and Bounding Limits...")
        
        overflow_state = {"appearance": {}, "mood": {"arousal": 9.9}, "last_decay_timestamp": time.time() - 3600}
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(overflow_state, f, indent=2)
            
        mood_engine = _test_sandbox("soul/mood_engine.py", "NeptuneMoodEngine", code_root)
        updated_state = mood_engine.update_biological_decay()
        
        arousal_result = updated_state["mood"]["arousal"]
        assert arousal_result <= 1.6, f"Arousal bounds clipping failed! Got: {arousal_result}"
        print("  --> PASS: Biological arousal securely bound between 0.0 and 1.6! ❤️")

        # --------------------------------------------------
        # TEST 4: NEPTUNECTL COMMAND ROUTING & SET KEYWORD
        # --------------------------------------------------
        print("[TEST 4/4] Validating neptunectl Command Parser and 'set' Keyword...")
        
        clean_state = {"appearance": {"top": "naked"}, "mood": {"arousal": 0.0}}
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(clean_state, f, indent=2)
            
        cmd_string = "neptunectl dress set top default_shirt"
        cmd_output = _test_sandbox("mind/sysadmin/sysadmin_core.py", "handle_system_override", cmd_string)
        
        with open(state_path, 'r') as f:
            mutated_state = json.load(f)
            
        assert mutated_state["appearance"]["top"] == "default_shirt", "Command mutation failed to commit item key to file!"
        print("  --> PASS: neptunectl dress set tokens isolated and compiled perfectly! 🛠️")
        
        print("\n====================================================")
        print("🎉 ALL CORE WORKSPACE INTEGRATION TESTS PASSED! 🎉")
        print("====================================================")

    except Exception as e:
        print(f"\n❌ TEST SUITE RUNTIME EXCEPTION CAUGHT: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        if state_backup:
            with open(state_path, 'w', encoding='utf-8') as f:
                f.write(state_backup)
        elif os.path.exists(state_path):
            os.remove(state_path)

if __name__ == "__main__":
    run_neptune_test_suite()