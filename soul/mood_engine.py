# =========================================================================
# THE SOUL LAYER: PERSISTED PSYCHOLOGICAL MOOD ENGINE
# Component Category: Personality & Emotion Processing Plane (mood_engine.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's hormonal state and emotional chemistry.
# By calculating time-decay coefficients across epoch timestamps, it updates her
# internal dopamine, arousal, and affection metrics between message cycles,
# ensuring her baseline reactions shift fluidly depending on interaction gaps.
# =========================================================================

import time
import math
import json
import os

def calculate_time_decay(last_timestamp: float, current_timestamp: float, half_life_seconds: float = 1800.0) -> float:
    """Calculates an exponential decay multiplier based on elapsed epoch time."""
    if last_timestamp <= 0.0:
        return 1.0
        
    elapsed_time = current_timestamp - last_timestamp
    if elapsed_time <= 0:
        return 1.0
        
    # Standard exponential decay formula: e^(-lambda * t)
    # 1800 seconds = 30 minute half-life default for baseline calming loops
    decay_factor = math.exp(- (elapsed_time * math.log(2)) / half_life_seconds)
    return max(0.0, min(1.0, decay_factor))

async def process_emotional_decay_cycle(current_state: dict) -> dict:
    """Ingests the global system state records and applies time-decay cooling rules to emotional metrics."""
    arousal_data = current_state.setdefault("arousal", {})
    meta_cache = current_state.setdefault("meta", {})
    
    # Extract live numeric metrics
    current_arousal = float(arousal_data.get("level", 0.0))
    last_seen = float(meta_cache.get("last_interaction_timestamp", 0.0))
    now = time.time()
    
    # Calculate decay factor if a valid past interaction exists
    if last_seen > 0.0:
        # Arousal decays over a 20-minute half-life (1200 seconds) for responsive cooling
        decay_factor = calculate_time_decay(last_seen, now, half_life_seconds=1200.0)
        
        # Smoothly apply decay math
        new_arousal = current_arousal * decay_factor
        
        # Apply subtle linear decay fallback if exponential drops too slowly at the tail end
        if current_arousal > 0.0 and (now - last_seen) > 300:
            new_arousal -= 0.05
            
        arousal_data["level"] = max(0.0, min(1.0, round(new_arousal, 3)))
    else:
        # Initial handshake: force clamp safety boundary limits
        arousal_data["level"] = max(0.0, min(1.0, current_arousal))

    # Dynamically update structural physical indicators based on calculated level thresholds
    if arousal_data["level"] >= 0.7:
        arousal_data["wetness"] = "dripping wet"
        arousal_data["nipples"] = "hard, erect"
    elif arousal_data["level"] >= 0.4:
        arousal_data["wetness"] = "moist"
        arousal_data["nipples"] = "perky"
    else:
        arousal_data["wetness"] = "dry"
        arousal_data["nipples"] = "soft"

    # Always log the active epoch time marker as the last completed interaction gate
    meta_cache["last_interaction_timestamp"] = now
    return current_state
async def apply_arousal_spike(current_state: dict, spike_value: float) -> tuple:
    """Programmatically increments arousal metrics (e.g. from explicit user praise or clothing updates)."""
    arousal_data = current_state.setdefault("arousal", {})
    
    current_level = float(arousal_data.get("level", 0.0))
    new_level = min(1.0, max(0.0, current_level + spike_value))
    
    arousal_data["level"] = round(new_level, 3)
    
    # Re-evaluate visual physical signs immediately to maintain state continuity
    if arousal_data["level"] >= 0.7:
        arousal_data["wetness"] = "dripping wet"
        arousal_data["nipples"] = "hard, erect"
    elif arousal_data["level"] >= 0.4:
        arousal_data["wetness"] = "moist"
        arousal_data["nipples"] = "perky"
    else:
        arousal_data["wetness"] = "dry"
        arousal_data["nipples"] = "soft"
        
    return current_state, arousal_data["level"]