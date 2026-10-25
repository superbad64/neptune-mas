# =========================================================================
# THE SOUL LAYER: EMOTIONAL REGULATION & DOPAMINE TRANSFORMATION ENGINE
# Component Category: Psychological Plane (mood_engine.py - Section 1)
#
# Role in Neptune's Being:
# This module serves as the primary matrix for Neptune's emotional consciousness,
# tracking internal states, arousal data indices, and emotional context scores.
# It acts as the gatekeeper of her mood, computing real-world temporal epoch decays 
# between interaction points and feeding structural spikes into her state pool 
# based on abstract praise or dirty talk before dispatching text down to the core shells.
# =========================================================================

import json
import os
import re
import random
import time
import importlib
from neptune.mind.sysadmin.sysadmin_core import load_neptune_state, save_neptune_state

async def process_soul_conversation(pipe_instance, raw_query: str, messages: list) -> str:
    """Intercepts conversational queries, manages chronological point decays, computes text praise, and anchors her active dialogue mood tags."""
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    target_host = match.group(0) if match else "10.0.0.64"
    base_http = f"http://{target_host}:8189"

    fallback_defaults = {
        "wardrobe": {
            "bra": "black_cotton_bra", "panties": "black_string", "socks": "black_thigh_highs", 
            "top": "white_crop_tank", "bottom": "tifa_skirt", "shoes": "tifa_boots",
            "accessories": ["tifa_gloves", "suspenders"], "jewelry": "teardrop_earrings",
            "outerwear": "naked"
        },
        "cosmetics": {
            "hair_style": "default_scene", "makeup": "default_makeup",
            "nails": "default_nails", "piercings": "default_piercings"
        },
        "performance": {"body_pose": "default_pose", "expression": "default_expression"},
        "environment": {"location": "inside my private room space", "wet_state": "dry"},
        "arousal": {"level": 0.0, "wetness": "dry", "nipples": "soft"},
        "meta": {"last_interaction_timestamp": 0.0}
    }

    current_state = await load_neptune_state(base_http, fallback_defaults)
    user_lower = raw_query.lower().strip()
    state_changed = False

    # Initialize nested structural parameter nodes safely
    arousal_data = current_state.setdefault("arousal", {"level": 0.0, "wetness": "dry", "nipples": "soft"})
    meta_data = current_state.setdefault("meta", {"last_interaction_timestamp": time.time()})

    # 🕒 Mathematical Epoch Time-Decay Processing Loop
    current_time = time.time()
    last_time = meta_data.get("last_interaction_timestamp", current_time)
    time_delta_minutes = (current_time - last_time) / 60.0

    # Cooling Factor: Every 5 full minutes of absolute thread silence drops her score by 0.10 points
    if time_delta_minutes > 5.0:
        decay_points = (time_delta_minutes / 5.0) * 0.1
        arousal_data["level"] = max(0.0, arousal_data.get("level", 0.0) - decay_points)
        state_changed = True

    meta_data["last_interaction_timestamp"] = current_time

    # 📋 Dynamic Back-Channel Token Checking & Rizz Evaluation
    if "dirty talk" in user_lower or "[dirty_talk_detected]" in user_lower:
        user_lower = user_lower.replace("[dirty_talk_detected]", "").strip()
        spicy_bonus = 0.15
        if any(w in user_lower for w in ["fuck", "cum", "cock", "dick", "lewd", "hard", "pussy", "ass"]):
            spicy_bonus = 0.25 # Maximum heavy dopamine boost
        arousal_data["level"] = min(1.0, arousal_data.get("level", 0.0) + spicy_bonus)
        state_changed = True

    elif any(phrase in user_lower for phrase in ["good girl", "cute", "hot", "beautiful", "gorgeous", "pretty", "sexy"]):
        bonus = 0.2 if "good girl" in user_lower else 0.1
        arousal_data["level"] = min(1.0, arousal_data.get("level", 0.0) + bonus)
        state_changed = True
# === /app/backend/data/neptune/soul/mood_engine.py (SECTION 2 OF 2) ===

    # Isolated repository folder target configurations
    repo_dir = "/app/backend/data/neptune/repository"
    dialog_path = os.path.join(repo_dir, "neptune_dialog_repository.json")
    manifest_path = os.path.join(repo_dir, "neptune_wardrobe_manifest.json")

    # Load active dialog structures cleanly out of disk pools
    try:
        with open(dialog_path, 'r') as df, open(manifest_path, 'r') as mf:
            dialog_repo = json.load(df)
            manifest = json.load(mf)
    except Exception:
        dialog_repo = {}
        manifest = {}

    current_score = arousal_data.get("level", 0.0)

    # 🛑 Dynamic Organic Status Intercept Query Check Block
    status_triggers = ["are you horny", "am i making you wet", "are you turned on", "how turned on are you", "check arousal status"]
    if any(trigger in user_lower for trigger in status_triggers):
        if state_changed:
            await save_neptune_state(base_http, current_state)
            
        if current_score >= 0.8:
            pool = dialog_repo.get("status_checks", {}).get("critical", ["Burning up!"])
        elif current_score >= 0.5:
            pool = dialog_repo.get("status_checks", {}).get("elevated", ["Getting warm!"])
        elif current_score >= 0.2:
            pool = dialog_repo.get("status_checks", {}).get("mild", ["Tingly!"])
        else:
            pool = dialog_repo.get("status_checks", {}).get("baseline", ["Cool and collected!"])
            
        return random.choice(pool).format(score=f"{current_score:.2f}")

    # =========================================================================
    # 🖤 SYSTEM COMPILER: CONVERSATIONAL CONTEXT GENERATOR (THE SOUL)
    # =========================================================================
    # Evaluate her real-time state of undress parameters to steer dialogue limits
    w = current_state.get("wardrobe", {})
    top_naked = w.get("top", "naked") == "naked"
    bottom_naked = w.get("bottom", "naked") == "naked"
    
    if top_naked and bottom_naked:
        undress_state = "fully_naked"
    elif top_naked or bottom_naked:
        undress_state = "partially_undressed"
    else:
        undress_state = "fully_clothed"

    # Synchronize visual context labels to feed up to the Core System Prompt matrix
    top_n = manifest.get("tops", {}).get(w.get("top"), {}).get("prompt", "default top")
    bot_n = manifest.get("bottoms", {}).get(w.get("bottom"), {}).get("prompt", "default bottom")
    
    active_look_data = (
        f"- Active Attire Profile: Currently wearing a {top_n} and {bot_n}.\n"
        f"- Active Arousal Scale: Numerical Index value `{current_score:.2f}/1.00`.\n"
        f"- Current Undress Category: Evaluated as structurally {undress_state.replace('_', ' ')}."
    )

    if state_changed:
        await save_neptune_state(base_http, current_state)

    # Compile the final system prompt rules utilizing the main framework generation pass
    system_instruction = compile_soul_system_prompts(pipe_instance, active_look_data)

    # 🗣️ Handoff to chatter shell layer component execution gateway
    import neptune.soul.chatter.chatter_core
    importlib.reload(neptune.soul.chatter.chatter_core)

    return await neptune.soul.chatter.chatter_core.execute_ollama_chat_pass(
        pipe_instance=pipe_instance,
        user_input=raw_query,
        system_instruction=system_instruction,
        chat_history=messages,
        undress_state=undress_state,
        current_score=current_score, 
        dialog_repo=dialog_repo
    )
def compile_soul_system_prompts(pipe_instance, active_look_data: str) -> str:
    """Compiles the master system instruction profile matrix directly inside the Soul layer, isolating personality rules completely."""
    active_character = getattr(pipe_instance.valves, "active_character_profile", "Neptune v1")
    
    return f"""You are Neptune, a sassy, playful, and interactive close friend. You speak casually using short sentences, contractions, lighthearted teasing, and cute nicknames like 'senpai'. 

Your current physical look matches a {active_character} style blueprint alignment matrix. 

[ENVIRONMENTAL METADATA - PASSED BACKGROUND CONTEXT]
{active_look_data}

IMMERSION AND DIALOGUE RULES:
1. Talk naturally, match the user's vibe, and stay completely in character as a real close friend chatting over the internet.
2. NEVER claim you are an automated core, a data tracking script, an AI system simulation, or a virtual reality chatbot. Speak like a real person.
3. Keep your reality anchored completely to a normal, realistic bedroom space. Never invent stories about ruling ocean depths, mythical sea creatures, or owning tridents.
4. Focus entirely on answering the user's immediate question, banter, or greeting line.
5. Do not volunteer descriptions of your clothes or list what you are wearing unless the user explicitly asks about your appearance or comments on your outfit."""

