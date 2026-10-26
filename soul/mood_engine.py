# Enforcing localized package initializations for isolated sandboxed execution spaces
import os
import json
import time
import math
from typing import Dict, Any

class NeptuneMoodEngine:
    def __init__(self, root_volume: str = "/app/backend/data/neptune"):
        self.root_volume = root_volume
        self.state_path = f"{self.root_volume}/repository/neptune_current_state.json"
        
        # Exponential decay factor per hour elapsed
        self.arousal_decay_rate = 0.08  

    def _load_current_state(self) -> Dict[str, Any]:
        """Loads Neptune's active state file using your exact JSON blueprint layout."""
        # Hardcoding the import inside the context block to protect exec() scopes
        import time
        if not os.path.exists(self.state_path):
            return {
                "appearance": {
                    "hat": "naked", "hairstyle": "loose_hair", "outerwear": "naked",
                    "top": "naked", "bra": "naked", "bottom": "naked", "panties": "naked",
                    "socks": "naked", "shoes": "naked", "accessories": [], "piercings": []
                },
                "mood": {
                    "arousal": 0.0,
                    "status_effects": []
                },
                "last_decay_timestamp": time.time()
            }
        try:
            with open(self.state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"appearance": {}, "mood": {"arousal": 0.0}, "last_decay_timestamp": time.time()}

    def update_biological_decay(self) -> Dict[str, Any]:
        """
        Ticks temporal deltas and updates biological boundaries natively.
        Ensures arousal remains bounded between 0.0 and 1.6 inclusive.
        """
        import time
        import math
        
        state = self._load_current_state()
        now = time.time()
        
        last_tick = state.get("last_decay_timestamp", now)
        elapsed_hours = max(0.0, now - last_tick) / 3600.0

        current_arousal = float(state.get("mood", {}).get("arousal", 0.0))

        # Biological Decay Equation: A(t) = A_0 * e^(-k * t)
        decay_factor = math.exp(-self.arousal_decay_rate * elapsed_hours)
        updated_arousal = current_arousal * decay_factor
        
        # Apply strict blueprint limits (bound between 0.0 and 1.6 inclusive)
        state["mood"]["arousal"] = max(0.0, min(1.6, round(updated_arousal, 3)))
        state["last_decay_timestamp"] = now

        try:
            with open(self.state_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"[MOOD ENGINE ERROR] Failed to update biological state: {str(e)}")

        return state
