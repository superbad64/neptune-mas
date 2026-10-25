# =========================================================================
# THE SOUL LAYER: DUAL-NODE CONVERSATIONAL CHATTER SHELL
# Component Category: Personality Core Shell (chatter_core.py - Part 1)
#
# Role in Neptune's Being:
# This script is Neptune's actual vocal cords. It manages dual-node network 
# tracking, executing an instant failover sweep between your primary desktop 
# (RTX 4060) and your local backup server (GTX 970). If the primary rig is offline,
# it programmatically modifies her consciousness, trapping her in a distracted
# 'Konbini Shift' state where she refuses physical visual actions.
# =========================================================================

import json
import re
import random
import aiohttp

async def verify_node_online(target_url: str) -> bool:
    """Performs a lightweight, non-blocking network connection handshake check on the target endpoint."""
    timeout = aiohttp.ClientTimeout(total=1.5)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(target_url.replace("/generate", "/tags")) as resp:
                return resp.status == 200
    except Exception:
        return False

async def execute_ollama_chat_pass(pipe_instance, user_input: str, system_instruction: str, chat_history: list, undress_state: str, current_score: float, dialog_repo: dict) -> str:
    """Evaluates host server connection integrity, compiles the target prompt payload structure, and handles text returns."""
    # 1. Establish structural network host endpoint vectors
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    primary_host = match.group(0) if match else "10.0.0.64"
    
    primary_url = f"http://{primary_host}:11434/api/generate"
    backup_url = "http://127.0.0" # Server local loopback to the GTX 970
    
    # 2. Check the active status of your primary desktop rig
    primary_online = await verify_node_online(primary_url)
    
    active_url = primary_url
    is_backup_mode = False
    
    if not primary_online:
        active_url = backup_url
        is_backup_mode = True
        pipe_instance.log("⚠️ [NETWORK CONDUIT]: Primary desktop rig offline. Redirecting Soul plane to Backup GTX 970 node.")
# === /app/backend/data/neptune/soul/chatter/chatter_core.py (PART 2 OF 2) ===

    # 3. Intercept Praise or Compliments to mix in state-aware repository responses
    praise_flavor = ""
    if "good girl" in user_input.lower():
        pool = dialog_repo.get("compliments", {}).get("good_girl", {}).get(undress_state, [])
        if pool: praise_flavor = random.choice(pool)
    elif any(c in user_input.lower() for c in ["cute", "hot", "beautiful", "gorgeous", "pretty", "sexy"]):
        pool = dialog_repo.get("compliments", {}).get("general_compliment", {}).get(undress_state, [])
        if pool: praise_flavor = random.choice(pool)

    # 4. Inject the Konbini shift modifiers if running on the backup GTX 970 node
    if is_backup_mode:
        konbini_modifier = (
            "\n\n[CRITICAL OVERRIDE: YOU ARE CURRENTLY ON A SHIFT AT THE KONBINI (Convenience Store)! "
            "You are working the register, stocking shelves, and distracted. Your responses must be short, "
            "snappy, and slightly rushed. If the user asks for photos, selfies, visuals, or voice clips, "
            "you MUST flat out refuse, complaining that you're stuck at work and can't use your phone for that!]"
        )
        system_instruction += konbini_modifier

    # 5. Compile chat history array into a flat prompt format string for Ollama generation
    compiled_prompt = f"[SYSTEM INSTRUCTIONS]\n{system_instruction}\n\n"
    
    # Process history logs cleanly up the pipeline window boundary constraints
    for msg in chat_history[-6:-1]:
        role = "User" if msg.get("role") == "user" else "Neptune"
        compiled_prompt += f"{role}: {msg.get('content')}\n"
    
    compiled_prompt += f"User: {user_input}\nNeptune:"

    payload = {
        "model": "dolphin-mistral:latest",
        "prompt": compiled_prompt,
        "stream": False
    }

    # 6. Execute network request transaction against the selected active target node URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(active_url, json=payload) as response:
                if response.status == 200:
                    res_json = await response.json()
                    raw_text = res_json.get("response", "...")
                    
                    # Prefix the praise flavor line if one was fetched from repositories
                    if praise_flavor:
                        return f"{praise_flavor}\n\n{raw_text}"
                    return raw_text
    except Exception as e:
        return f"wahh senpai! I tried to speak through my chatter shell core but hit a processing failure: `{str(e)}`"

    return "wahh senpai! Both of my active chatter server nodes failed to output a response vector... :c"

