# =========================================================================
# THE BODY LAYER: COMFYUI WORKER TRANSACTIONAL DISPATCHER
# Component Category: Physical Sensory I/O Gateway (comfy_dispatch.py - Part 1)
#
# Role in Neptune's Being:
# This module represents Neptune's nervous system. It acts as the direct
# communication bridge to the external GPU worker node, converting compiled
# prompt matrices into explicit raw JSON execution graphs, establishing
# websocket streams, and tracking image generation pipelines to completion.
# =========================================================================

import json
import uuid
import base64
import random
import aiohttp
import re

async def execute_comfy_generation_dispatch(pipe_instance, target_host: str, base_http: str, full_positive: str, full_negative: str, current_state: dict) -> str:
    """Compiles the dynamic graph node dictionary map payload, establishes websocket connections, and decodes final media buffers."""

    meta_cache = current_state.get("meta", {})
    last_rendered_canvas = meta_cache.get("last_visual_canvas", "example.png")
    
    # Evaluate if this execution pass is a standard text-to-image run or an active image modification pass
    denoise_val = meta_cache.get("last_denoise_override", 1.0)
    is_image_to_image = denoise_val < 1.0

    # 🗜️ METICULOUSLY ALIGNED TYPE-STRICT COMFYUI PRODUCTION GRAPH OBJECT
    comfy_workflow = {
        "1": {
            "inputs": {
                "ckpt_name": "ponyRealism_v22MainVAE.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Load Checkpoint"}
        },
        "4": {
            "inputs": {
                "seed": random.randint(100000000000, 999999999999),
                "steps": 20,
                "cfg": 4,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": denoise_val,
                "model": ["1", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "latent_image": ["19", 0]
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler"}
        },
        "5": {
            "inputs": {
                "samples": ["4", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        },
        "7": {
            "inputs": {
                "string_a": ["16", 0],
                "string_b": "3d game asset mesh, square enix cgi style, final fantasy vii remake style, video game graphics, crisp clean unreal engine 5 render, smooth digital skin textures, highly detailed 3d polygonal model, ambient occlusion, depth of field, professional cinematic studio lighting",
                "delimiter": ", "
            },
            "class_type": "StringConcatenate",
            "_meta": {"title": "Concatenate Text"}
        },
        "8": {
            "inputs": {
                "string_a": "photorealistic, real human skin texture, pores, freckles, real life person, cosplayer photograph, hyper-realistic, score_4, score_5, score_6, lowres, worst quality, low quality, 2d anime, flat colors, lineart, drawing, illustration, cartoon, deformed hands, extra fingers, missing fingers, extra limbs, multiple views, duplicate character, out of focus, blurry, dirt",
                "string_b": full_negative,
                "delimiter": ", "
            },
            "class_type": "StringConcatenate",
            "_meta": {"title": "Concatenate Text"}
        },
        "9": {
            "inputs": {
                "filename_prefix": "neptune_render",
                "images": ["5", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        },
        "10": {
            "inputs": {
                "width": 832,
                "height": 832,
                "crop_w": 0,
                "crop_h": 0,
                "target_width": 832,
                "target_height": 832,
                "text_g": ["7", 0],
                "text_l": ["7", 0],
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncodeSDXL",
            "_meta": {"title": "Node 3"}
        },
        "11": {
            "inputs": {
                "width": 832,
                "height": 832,
                "crop_w": 0,
                "crop_h": 0,
                "target_width": 832,
                "target_height": 832,
                "text_g": ["8", 0],
                "text_l": ["8", 0],
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncodeSDXL",
            "_meta": {"title": "Node 21"}
        },
        "16": {
            "inputs": {
                "value": full_positive
            },
            "class_type": "PrimitiveString",
            "_meta": {"title": "Text"}
        },
        "17": {
            "inputs": {
                "source": ["7", 0]
            },
            "class_type": "PreviewAny",
            "_meta": {"title": "Preview as Text"}
        }
    }

    # =========================================================================
    # DYNAMIC LATENT CANVAS CONFIGURATION LAYER
    # =========================================================================
    if is_image_to_image:
        # Image modification active: Ingest file layout from cache via VAEEncode
        comfy_workflow["18"] = {
            "inputs": {"image": last_rendered_canvas},
            "class_type": "LoadImage",
            "_meta": {"title": "Load Image"}
        }
        comfy_workflow["19"] = {
            "inputs": {"pixels": ["18", 0], "vae": ["1", 2]},
            "class_type": "VAEEncode",
            "_meta": {"title": "VAE Encode"}
        }
    else:
        # Standard execution loop: Generate a clean latent space from scratch
        comfy_workflow["19"] = {
            "inputs": {"width": 832, "height": 832, "batch_size": 1},
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Empty Latent Image"}
        }
    try:
        base_ws, client_id = f"ws://{target_host}:8189/ws", str(uuid.uuid4())
        timeout = aiohttp.ClientTimeout(total=90.0)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # 1. Establish live websocket synchronization channel with the GPU host node
            async with session.ws_connect(f"{base_ws}?clientId={client_id}") as ws:
                # Submit compiled production workflow execution payload packet
                async with session.post(f"{base_http}/prompt", json={"prompt": comfy_workflow, "client_id": client_id}) as response:
                    if response.status != 200:
                        return f"wahh senpai! ComfyUI worker node rejected the pipeline generation matrix: {await response.text()}"
                    res_data = await response.json()
                    target_prompt_id = res_data.get("prompt_id")

                # 2. Block and read server thread events until execution finishes
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if data.get("type") == "executing" and data.get("data", {}).get("node") is None and data.get("data", {}).get("prompt_id") == target_prompt_id:
                            break
                    elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                        break

            # 3. Pull transaction history record payload entries
            async with session.get(f"{base_http}/history/{target_prompt_id}") as history_res:
                if history_res.status == 200:
                    hist_data = await history_res.json()
                    prompt_output = hist_data.get(target_prompt_id, {}).get("outputs", {})
                    found_image_filename, subfolder = "", ""
                    
                    for node_id in sorted(prompt_output.keys(), key=int, reverse=True):
                        node_data = prompt_output[node_id]
                        if "images" in node_data and isinstance(node_data["images"], list) and len(node_data["images"]) > 0:
                            img_meta = node_data["images"][0]
                            found_image_filename = img_meta.get("filename", "")
                            subfolder = img_meta.get("subfolder", "")
                            if found_image_filename: break

                    if found_image_filename:
                        # Store the new file pointer name back to persistent memory cache records
                        current_state.setdefault("meta", {})["last_visual_canvas"] = found_image_filename
                        from neptune.mind.sysadmin.sysadmin_core import save_neptune_state
                        await save_neptune_state(base_http, current_state)

                        # 5. Asynchronously stream finished image binary blocks down the link
                        file_url = f"{base_http}/view?filename={found_image_filename}&subfolder={subfolder}&type=output"
                        async with session.get(file_url) as img_res:
                            if img_res.status == 200:
                                img_bytes = await img_res.read()
                                base64_encoded = base64.b64encode(img_bytes).decode("utf-8")
                                data_uri = f"data:image/png;base64,{base64_encoded}"
                                
                                diag_path = "/app/backend/data/neptune/repository/neptune_dialog_repository.json"
                                try:
                                    with open(diag_path, 'r') as df:
                                        repo = json.load(df)
                                    msg_pool = repo.get("default_delivery", {}).get("selfie", ["Here's your picture!"])
                                    msg_text = random.choice(msg_pool)
                                except Exception:
                                    msg_text = "Snap secured! 📸 Hope this view {location_text} coordinates nicely with your expectations, senpai! 💜"

                                # =========================================================================
                                # DYNAMIC TEMPLATE PLACEHOLDER PARSING ENGINE
                                # =========================================================================
                                env_data = current_state.get("environment", {})
                                wet_state = env_data.get("wet_state", "dry")
                                
                                # Resolve dynamic location context string
                                if wet_state == "wet":
                                    location_string = "from inside the shower"
                                else:
                                    location_string = "here in my room"

                                # Safely patch text leaks
                                msg_text = msg_text.replace("{location_text}", location_string)
                                msg_text = re.sub(r'\s+', ' ', msg_text).strip() # Scrub double spaces layout issues

                                return f"![Neptune Physical Asset Render]({data_uri})\n\n{msg_text}"

        return "wahh senpai! Media pipeline transaction completed but asset tracking was dropped down the pipeline conduit... :c"
    except Exception as e:
        return f"wahh senpai! The Physical Body I/O layer encountered a critical hardware handshake link crash: `{str(e)}`"
