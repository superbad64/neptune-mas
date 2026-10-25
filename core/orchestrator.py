# =========================================================================
# THE MIND CORE: ROUTING ANALYSIS & SYSTEM EXECUTION DISPATCHER
# Component Category: Internal Core System Router (orchestrator.py)
#
# Role in Neptune's Being:
# This script handles the brain routing tasks. It takes the normalized text and
# uses the LLM intent classification matrix to dispatch execution down to the
# mind, body, or soul sub-directories while carrying the valve properties safely.
# =========================================================================

import json
import re
import importlib  # FIXED: Explicitly added the missing import module namespace tracker

async def run_face_intent_router(pipe_instance, user_input: str) -> dict:
    """Invokes llama3.2:3b locally to determine structural target plane intents."""
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    target_host = match.group(0) if match else "10.0.0.64"
    ollama_url = f"http://{target_host}:11434/api/generate"

    system_instructions = (
        "You are the master intent classification router for the Neptune multi-agent system. "
        "Categorize the user prompt into a strict internal plane:\n"
        "- 'mind': Technical utility commands, look checks, outfit changes, wardrobe mutations, or setting changes.\n"
        "- 'body': Explicit requests for a fresh visual render pass, pictures, photos, selfies, or camera reshoots.\n"
        "- 'soul': Conversational banter, general friendly chat, flirting, dirty talk, or character praise.\n\n"
        "Output ONLY a raw JSON string: {\"target\": \"mind|body|soul\", \"reason\": \"summary\"}"
    )

    payload = {
        "model": "llama3.2:3b",
        "prompt": f"{system_instructions}\n\nUser Prompt: \"{user_input}\"\n\nJSON Output:",
        "stream": False,
        "format": "json"
    }

    try:
        import aiohttp
        timeout = aiohttp.ClientTimeout(total=4.0)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(ollama_url, json=payload) as resp:
                if resp.status == 200:
                    res_json = await resp.json()
                    return json.loads(res_json.get("response", "{}"))
    except Exception:
        pass

    if any(k in user_input.lower() for k in pipe_instance.selfie_keywords):
        return {"target": "body", "reason": "Selfie keyword fallback mapping."}
    if any(k in user_input.lower() for k in ["put on", "wear", "dress in", "change to outfit", "switch outfit"]):
        return {"target": "mind", "reason": "Wardrobe change fallback mapping."}
    return {"target": "soul", "reason": "Conversational fallback security line."}

async def route_traffic_planes(pipe_instance, raw_query: str, user_lower: str, messages: list, debug_trace: list) -> str:
    """Evaluates router targets and splits incoming data paths straight down to plane directories."""
    route_matrix = await run_face_intent_router(pipe_instance, user_lower)
    target_plane = route_matrix.get("target", "soul")
    routing_reason = route_matrix.get("reason", "No reason provided.")
    debug_trace.append(f"👺 **Internal Plane Target Acquired**: `{target_plane.upper()}` | *\"{routing_reason}\"*")

    if target_plane == "mind":
        import neptune.mind.inspector
        importlib.reload(neptune.mind.inspector)
        response = await neptune.mind.inspector.process_mind_logic(pipe_instance, user_lower)
    elif target_plane == "body":
        import neptune.body.pipeline_compiler
        importlib.reload(neptune.body.pipeline_compiler)
        response = await neptune.body.pipeline_compiler.trigger_body_render(pipe_instance, raw_query, messages)
    else:
        import neptune.soul.mood_engine
        importlib.reload(neptune.soul.mood_engine)
        response = await neptune.soul.mood_engine.process_soul_conversation(pipe_instance, raw_query, messages)

    if pipe_instance.valves.debug_mode:
        return f"{response}\n\n---\n### 🛠️ ROUTING ENGINE TERMINATION SUCCESS"
    return response

