# =========================================================================
# THE BODY LAYER: RESHOOT WORKER & PHYSICAL ASSET SYNC CONDUIT
# Component Category: Physical Sensory I/O Plane (reshoot_worker.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's somatic image modification memory. Operating
# under direct execution from the cognitive Mind plane, it implements the
# Asset Sync Loop by pulling either freshly uploaded user media or historical
# canvas references, injecting them straight into ComfyUI's input caches via
# multipart back-channels, and executing variant edits.
# =========================================================================

import os
import json
import re
import aiohttp

async def sync_image_to_comfy_input_cache(base_http: str, filename: str, image_bytes: bytes) -> bool:
    """Pushes raw image binary blocks straight into ComfyUI's input directory via back-channel multipart upload."""
    upload_url = f"{base_http}/upload/image"
    try:
        form_data = aiohttp.FormData()
        form_data.add_field('image', image_bytes, filename=filename, content_type='image/png')
        form_data.add_field('overwrite', 'true')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, data=form_data) as response:
                if response.status == 200:
                    return True
    except Exception:
        pass
    return False

async def execute_physical_image_reshoot(pipe_instance, raw_query: str, messages: list, current_state: dict) -> str:
    """Executes the mechanical asset pulling, back-channel cache sync, and triggers the final ComfyUI workflow execution."""
    raw_valve = str(pipe_instance.valves.desktop_ollama_raw).strip()
    match = re.search(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", raw_valve)
    target_host = match.group(0) if match else "10.0.0.64"
    base_http = f"http://{target_host}:8189"

    meta_cache = current_state.setdefault("meta", {})
    last_canvas = meta_cache.get("last_visual_canvas", "example.png")
    image_to_sync_bytes = None
    target_filename = last_canvas

    # 1. ASSET PULL LAYER: Evaluate if a fresh file was uploaded in the chat stream
    latest_message = messages[-1] if messages else {}
    files_in_message = latest_message.get("info", {}).get("files", []) if isinstance(latest_message, dict) else []
    
    user_uploaded_fresh = False
    if files_in_message:
        for f in files_in_message:
            if "image" in f.get("type", ""):
                local_path = f.get("path", "")
                if local_path and os.path.exists(local_path):
                    with open(local_path, "rb") as lf:
                        image_to_sync_bytes = lf.read()
                    target_filename = f"user_upload_{os.path.basename(local_path)}"
                    if not target_filename.endswith(".png"): target_filename += ".png"
                    user_uploaded_fresh = True
                    break
    # 2. HISTORICAL FALLBACK LAYER: Pull last generated render if no active upload exists
    if not user_uploaded_fresh and last_canvas and last_canvas != "example.png":
        view_url = f"{base_http}/view?filename={last_canvas}&type=output"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(view_url) as res:
                    if res.status == 200:
                        image_to_sync_bytes = await res.read()
        except Exception:
            image_to_sync_bytes = None

    # 3. BACK-CHANNEL CACHE INJECTION LOOP EXECUTION
    if image_to_sync_bytes:
        sync_success = await sync_image_to_comfy_input_cache(base_http, target_filename, image_to_sync_bytes)
        if sync_success:
            meta_cache["last_visual_canvas"] = target_filename
            meta_cache["last_denoise_override"] = 0.50
            
            from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
            await save_neptune_state(base_http, current_state)
            
            from neptune.body.pipeline_compiler import trigger_body_render
            return await trigger_body_render(pipe_instance, raw_query, messages)

    return "wahh senpai! I tried to reshoot the image but my visual sensory buffer was completely empty... send a picture or render one first! :c"