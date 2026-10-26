import os
import sys
import json
import random
import requests
from typing import Dict, Any

def trigger_comfy_api_transmission(positive_prompt: str, negative_prompt: str, is_reshoot: bool = False) -> str:
    """
    Assembles the exact node dictionary payload and transmits it over 
    the local area network straight down to the WSL ComfyUI backend core.
    """
    import random
    import requests
    
    # Nested helper function right inside the execution scope to guarantee absolute name visibility
    def _commit_prompt_id_to_state_internal(pid: str):
        state_file = "/app/backend/data/neptune/repository/neptune_current_state.json"
        try:
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                state_data["last_pending_prompt_id"] = pid
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(state_data, f, indent=2)
        except Exception as e:
            print(f"[COMFY STATE ERROR] Failed tracking ID write loop: {str(e)}")

    target_host = "10.0.0.64"
    target_port = 8189
    api_endpoint = f"http://{target_host}:{target_port}/prompt"
    
    dynamic_seed = random.randint(10000000000000, 99999999999999)
    
    # Reconstruct your exact structural JSON node canvas workflow graph
    workflow_graph = {
        "1": {"inputs": {"ckpt_name": "ponyRealism_v22MainVAE.safetensors"}, "class_type": "CheckpointLoaderSimple"},
        "4": {
            "inputs": {
                "seed": dynamic_seed,
                "steps": 20,
                "cfg": 4.0,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 0.55 if is_reshoot else 1.0,
                "model": ["1", 0],
                "positive": ["10", 0],
                "negative": ["11", 0],
                "latent_image": ["19", 0]
            },
            "class_type": "KSampler"
        },
        "5": {"inputs": {"samples": ["4", 0], "vae": ["1", 2]}, "class_type": "VAEDecode"},
        "7": {
            "inputs": {
                "string_a": ["16", 0],
                "string_b": "3d game asset mesh, square enix cgi style, final fantasy vii remake style, video game graphics, crisp clean unreal engine 5 render, smooth digital skin textures, highly detailed 3d polygonal model, ambient occlusion, depth of field, professional cinematic studio lighting",
                "delimiter": ", "
            },
            "class_type": "StringConcatenate"
        },
        "8": {
            "inputs": {
                "string_a": negative_prompt,
                "string_b": "",
                "delimiter": ", "
            },
            "class_type": "StringConcatenate"
        },
        "9": {"inputs": {"filename_prefix": "Neptune_Render", "images": ["5", 0]}, "class_type": "SaveImage"},
        "10": {"inputs": {"width": 832, "height": 832, "crop_w": 0, "crop_h": 0, "target_width": 832, "target_height": 832, "text_g": ["7", 0], "text_l": ["7", 0], "clip": ["1", 1]}, "class_type": "CLIPTextEncodeSDXL"},
        "11": {"inputs": {"width": 832, "height": 832, "crop_w": 0, "crop_h": 0, "target_width": 832, "target_height": 832, "text_g": ["8", 0], "text_l": ["8", 0], "clip": ["1", 1]}, "class_type": "CLIPTextEncodeSDXL"},
        "16": {"inputs": {"value": positive_prompt}, "class_type": "PrimitiveString"},
        "17": {"inputs": {"source": ["7", 0]}, "class_type": "PreviewAny"},
        "18": {"inputs": {"image": "example.png"}, "class_type": "LoadImage"},
        "19": {"inputs": {"pixels": ["18", 0]}, "class_type": "VAEEncode"}
    }

    if not is_reshoot:
        workflow_graph["25"] = {
            "inputs": {"width": 832, "height": 832, "batch_size": 1},
            "class_type": "EmptyLatentImage"
        }
        workflow_graph["4"]["inputs"]["latent_image"] = ["25", 0]

    print(f"[COMFY DISPATCH] Firing transaction loop down to {api_endpoint}...")
    try:
        payload = {"prompt": workflow_graph}
        response = requests.post(api_endpoint, json=payload, timeout=20)
        
        if response.status_code == 200:
            prompt_id = response.json().get("prompt_id", "unknown_id")
            _commit_prompt_id_to_state_internal(prompt_id)
            return (
                f"📸 \"*[Neptune snaps a brand new picture and updates her live image matrix stream!]* "
                f"Canvas cleared out to my execution deck, Boss! Rendering under job tracker ID: `{prompt_id}`!\""
            )
        return f"```\n[COMFY ERROR]: Node cluster rejected payload pass with status frame: {response.status_code}\n```"
            
    except Exception as e:
        return f"❌ \"Gah! I compiled our generation vectors perfectly, Boss, but hit a network socket failure clearing traffic to Machine 2: {str(e)}\""

def trigger_forced_generation(raw_prompt: str) -> str:
    """Administrative hook proxy targeted via neptunectl overrides."""
    # Maps natively through our internal transmission runner
    return trigger_comfy_api_transmission(positive_prompt=raw_prompt, negative_prompt="low quality, blurry", is_reshoot=False)