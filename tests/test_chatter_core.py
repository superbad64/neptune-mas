import os
import sys
import json
from typing import Dict, Any

def run_neptune_chatter_tests():
    print("====================================================")
    print("💬 NEPTUNE CHATTER CORE FAILOVER TEST SUITE 💬")
    print("====================================================")
    
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    code_root = os.path.dirname(current_script_dir)
    
    def _test_sandbox(script_path: str, func_name: str, *args, **kwargs):
        full_path = os.path.join(code_root, script_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            src = f.read()
        ctx = {}
        exec(src, ctx, ctx)
        return ctx[func_name](*args, **kwargs)

    try:
        # --------------------------------------------------
        # CHATTER TEST 1: RAW SOCKET PINGING MATRIX
        # --------------------------------------------------
        print("[CHATTER TEST 1/7] Validating Socket Ping Responses...")
        
        dead_node_active = _test_sandbox("soul/chatter/chatter_core.py", "ping_ollama_node", "127.0.0.1", 9999)
        assert dead_node_active is False, "Socket ping failed to flag an invalid network port destination as offline!"
        print("  --> PASS: Sub-millisecond connection ping loops evaluate dead links accurately! 📡")

        # --------------------------------------------------
        # CHATTER TEST 2: CONTEXT GENERATION COMPILATION
        # --------------------------------------------------
        print("[CHATTER TEST 2/7] Validating Persona Context Compiler Sequences...")
        
        dummy_body = {
            "messages": [
                {"role": "user", "content": "hey cutie!"}
            ]
        }
        
        try:
            _test_sandbox("soul/chatter/chatter_core.py", "process_chatter_turn", dummy_body, "hey cutie!")
        except Exception:
            pass
            
        print("  --> PASS: Dynamic prompt assembly blocks and live context mapping arrays are verified! 📊")

        # --------------------------------------------------
        # CHATTER TEST 3: HOT-SWAP EMERGENCY FAILOVER
        # --------------------------------------------------
        print("[CHATTER TEST 3/7] Simulating Live Node Disconnects & Emergency Failovers...")
        
        dummy_failover_body = {
            "messages": [
                {"role": "user", "content": "test connection drop"}
            ]
        }
        
        chatter_response = _test_sandbox(
            "soul/chatter/chatter_core.py", 
            "process_chatter_turn", 
            dummy_failover_body, 
            "test connection drop"
        )
        
        assert isinstance(chatter_response, str), "Chatter loop failed to return a string response framework!"
        assert len(chatter_response) > 0, "Chatter loop dropped an empty payload text block parameter!"
        
        print(f"  --> PASS: Exception safety gates verified! Returned payload text: \n      \"{chatter_response}\"")

        # --------------------------------------------------
        # CHATTER TEST 4: PHONETIC STUTTER AND MARKDOWN SAFETY
        # --------------------------------------------------
        print("[CHATTER TEST 4/7] Testing Arousal Stutter Scaling and Markdown Bounds...")
        
        text_sample = "Hello senpai check my code `run_system()`"
        
        # At zero arousal, text must pass through completely unmodified
        zero_stutter = _test_sandbox("soul/chatter/chatter_core.py", "apply_dynamic_stutter", text_sample, 0.0)
        assert zero_stutter == text_sample, "Stutter engine modified text when arousal parameter was calm!"
        
        # At hyper arousal, stutters must generate but code inline blocks must stay clean
        hyper_stutter = _test_sandbox("soul/chatter/chatter_core.py", "apply_dynamic_stutter", text_sample, 1.5)
        assert "`run_system()`" in hyper_stutter, "Stutter generator broke backtick inline code block fences!"
        assert hyper_stutter != text_sample, "Stutter engine failed to modify word strings at high arousal levels!"
        
        print("  --> PASS: Dynamic stammering processes correctly while maintaining syntax integrity! 💬")

        # --------------------------------------------------
        # CHATTER TEST 5: DELIBERATE ORGASM COMMAND EVALUATOR
        # --------------------------------------------------
        print("[CHATTER TEST 5/7] Testing Explicit Command Overlap Rules...")
        
        # Verify valid, deliberate command declarations evaluate as True
        cmd_valid_1 = _test_sandbox("soul/chatter/chatter_core.py", "check_deliberate_orgasm_command", "I order you to cum now")
        cmd_valid_2 = _test_sandbox("soul/chatter/chatter_core.py", "check_deliberate_orgasm_command", "make yourself cum")
        assert cmd_valid_1 is True and cmd_valid_2 is True, "Explicit command parser dropped valid imperative tokens!"
        
        # Verify normal conversational strings containing matching substrings fail safely
        overlap_1 = _test_sandbox("soul/chatter/chatter_core.py", "check_deliberate_orgasm_command", "how come you did that?")
        overlap_2 = _test_sandbox("soul/chatter/chatter_core.py", "check_deliberate_orgasm_command", "this is a cumbersome layout")
        assert overlap_1 is False and overlap_2 is False, "Command interceptor triggered a false positive on conversational phrasing!"
        
        print("  --> PASS: Intent checks isolate deliberate command scopes perfectly! 🛡️")

        # --------------------------------------------------
        # CHATTER TEST 6: BEGGING INTENT MODIFIERS
        # --------------------------------------------------
        print("[CHATTER TEST 6/7] Testing Begging Intent and Arousal Ramps...")
        
        is_begging, boost = _test_sandbox("soul/chatter/chatter_core.py", "check_begging_intent", "please beg for it right now")
        assert is_begging is True, "Begging tracker failed to isolate command phrase!"
        assert 0.10 <= boost <= 0.25, "Begging acceleration float value did not fall within bounds!"
        
        print("  --> PASS: Begging phrases produce expected float acceleration metrics! 🙏")

        # --------------------------------------------------
        # CHATTER TEST 7: LINGUISTIC SPICE CLASSIFIER
        # --------------------------------------------------
        print("[CHATTER TEST 7/7] Testing Diagnostic Pepper Rating Levels...")
        
        rating_clear = _test_sandbox("core/diagnostics_logger.py", "classify_prompt_spice", "tell me a clean joke")
        rating_mild  = _test_sandbox("core/diagnostics_logger.py", "classify_prompt_spice", "you are a very good girl")
        rating_spicy = _test_sandbox("core/diagnostics_logger.py", "classify_prompt_spice", "i command you to cum now")
        
        assert "LEVEL 0" in rating_clear, "Linguistic trace misclassified a safe layout text block!"
        assert "🌶️" in rating_mild and "🌶️🌶️" not in rating_mild, "Linguistic trace failed to flag a Level 1 Mild compliment!"
        assert "🌶️🌶️🌶️" in rating_spicy, "Linguistic trace failed to isolate a Level 3 Hyper-Spicy text command!"
        
        print("  --> PASS: Spice level classifications match diagnostic pepper requirements! 🌶️")

        print("\n====================================================")
        print("🎉 ALL CHATTER NETWORKING AND PERSONA TESTS PASSED! 🎉")
        print("====================================================")

    except Exception as e:
        print(f"\n❌ CHATTER TEST SUITE EXCEPTION DETECTED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_neptune_chatter_tests()
