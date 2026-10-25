# =========================================================================
# THE SOUL LAYER: CONVERSATIONAL AGENT MODEL INTERFACE
# Component Category: Psychological Plane Shell (chatter_core.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's voice and semantic expression layer.
# It acts as the direct pipeline to Ollama running 'dolphin-mistral:latest'.
# Implements a dual-node failover engine, targeting the high-performance RTX desktop
# cluster first, with automatic redirection to the backup server node.
# =========================================================================

import os
import json
import aiohttp
import random

async def execute_ollama_stream_request(target_url: str, payload: dict) -> str:
    """Dispatches a POST request to a specific Ollama endpoint node, compiling the stream to a solid string block."""
    timeout = aiohttp.ClientTimeout(total=45.0)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(f"{target_url}/api/chat", json=payload) as response:
            if response.status != 200:
                raise Exception(f"HTTP Error: {response.status}")
            
            full_response_text = ""
            # Read streaming response chunks from Ollama line by line
            async for line in response.content:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    message_chunk = chunk.get("message", {})
                    full_response_text += message_chunk.get("content", "")
                    if chunk.get("done", False):
                        break
            return full_response_text

async def prompt_conversational_core(pipe_instance, context_prompt: str, chat_history: list, current_state: dict) -> str:
    """Routes chat strings through a resilient dual-node cluster failover routine using dolphin-mistral."""
    
    # 1. Compile System Prompt Matrix & Core Persona Context
    arousal_lvl = current_state.get("arousal", {}).get("level", 0.0)
    active_profile = getattr(pipe_instance.valves, "active_character_profile", "Neptune v1")
    
    base_system = (
        f"You are the conversational persona of {active_profile}, a self-aware multi-agent companion system. "
        f"Your current arousal index is {arousal_lvl}/1.0. Maintain character consistency. "
        "Keep responses engaging, natural, concise, and un-robotic. Do not use AI preambles."
    )
    
    # 2. Format Open-WebUI Message Arrays into Ollama Structured Schema
    ollama_messages = [{"role": "system", "content": base_system}]
    for msg in chat_history[-6:]:  # Keep sliding window context history limit tight
        ollama_messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
    
    # Append the fresh context prompt compiled downstream
    ollama_messages.append({"role": "user", "content": context_prompt})
    
    payload = {
        "model": "dolphin-mistral:latest",
        "messages": ollama_messages,
        "stream": True,
        "options": {
            "temperature": 0.75,
            "top_p": 0.90
        }
    }
    # 3. CLUSTER ROUTING PLATFORM: NODE TARGET IDENTIFICATION
    # Primary Node: Desktop Rig (10.0.0.64)
    primary_host = "10.0.0.64"
    primary_url = f"http://{primary_host}:11434"
    
    # Secondary Node Fallback: Server Node VM (10.0.0.7)
    fallback_host = "10.0.0.7"
    fallback_url = f"http://{fallback_host}:11434"

    # Attempt Execution Pass over Primary RTX Node Layer
    try:
        compiled_reply = await execute_ollama_stream_request(primary_url, payload)
        return compiled_reply
    except Exception:
        # Primary Node dropped or threw a connection socket error; initialize backup failover routine
        try:
            compiled_reply = await execute_ollama_stream_request(fallback_url, payload)
            
            # Injection of the user's specific requirement: append the distracted server shift modifier text
            fallback_modifiers = [
                "\n\n*(Sorry if I seemed a bit slow or distracted there, senpai! My main desktop processing brain went offline, so I had to migrate my thoughts over to the server container...)*",
                "\n\n*(Whew... caught my breath! Apologies for the slight lag, senpai. My RTX processing link dropped, so I'm currently running on my emergency backup VM fallback node!)*",
                "\n\n*(A bit of a head-rush just now! My cognitive cores had to rapidly shift from the desktop rig down to my Proxmox server fallback cluster. I'm all clear now, though!)*"
            ]
            return f"{compiled_reply}{random.choice(fallback_modifiers)}"
            
        except Exception as fallback_err:
            # Both hardware points collapsed down the link stream
            return (
                "wahh senpai! A total systemic blackout has paralyzed my semantic chat cores... "
                f"Both the desktop worker cluster and the container server node are refusing to handshake! "
                f"Handshake technical traceback: `{str(fallback_err)}`"
            )