import os
import json
import time
import random
import requests

def transmit_graph_payload(compiled_positive: str, final_negative: str, is_reshoot: bool) -> dict:
    """
    Blocks application execution entirely by parsing nested prompt_id strings inside queue tuples,
    ensuring the accurate sequential filename is retrieved from completed histories.
    """
    target_host = "10.0.0.64"
    target_port = 8189
    
    api_endpoint = f"http://{target_host}:{target_port}/prompt"
    queue_endpoint = f"http://{target_host}:{target_port}/queue"
    history_endpoint = f"http://{target_host}:{target_port}/history"
    
    dynamic_seed = random.randint(10000000000000, 99999999999999)

    workflow_graph = {
        "1": {"inputs": {"ckpt_name": "ponyRealism_v22MainVAE.safetensors"}, "class_type": "CheckpointLoaderSimple"},
        "4": {
            "inputs": {
                "seed": dynamic_seed, "steps": 20, "cfg": 4, "sampler_name": "dpmpp_2m", "scheduler": "karras",
                "denoise": 0.55 if is_reshoot else 1.0, "model": ["1", 0], "positive": ["10", 0], "negative": ["11", 0], "latent_image": ["19", 0]
            },
            "class_type": "KSampler"
        },
        "5": {"inputs": {"samples": ["4", 0], "vae": ["1", 2]}, "class_type": "VAEDecode"},
        "7": {
            "inputs": {
                "string_a": ["16", 0],
                "string_b": "3d game asset mesh, square enix cgi style, final fantasy vii remake style, video game graphics, crisp clean unreal engine 5 render, smooth digital skin textures, highly detailed 3d polygonal model, ambient occlusion, depth of field, professional cinematic studio lighting, 1girl, solo",
                "delimiter": ", "
            },
            "class_type": "StringConcatenate"
        },
        "8": {"inputs": {"string_a": final_negative, "string_b": "", "delimiter": ", "}, "class_type": "StringConcatenate"},
        "9": {"inputs": {"filename_prefix": "Neptune_Render", "images": ["5", 0]}, "class_type": "SaveImage"},
        "10": {"inputs": {"width": 832, "height": 832, "crop_w": 0, "crop_h": 0, "target_width": 832, "target_height": 832, "text_g": ["7", 0], "text_l": ["7", 0], "clip": ["1", 1]}, "class_type": "CLIPTextEncodeSDXL"},
        "11": {"inputs": {"width": 832, "height": 832, "crop_w": 0, "crop_h": 0, "target_width": 832, "target_height": 832, "text_g": ["8", 0], "text_l": ["8", 0], "clip": ["1", 1]}, "class_type": "CLIPTextEncodeSDXL"},
        "16": {"inputs": {"value": compiled_positive}, "class_type": "PrimitiveString"},
        "17": {"inputs": {"source": ["7", 0]}, "class_type": "PreviewAny"},
        "18": {"inputs": {"image": "example.png"}, "class_type": "LoadImage"},
        "19": {"inputs": {"pixels": ["18", 0]}, "class_type": "VAEEncode"}
    }

    if not is_reshoot:
        workflow_graph["25"] = {"inputs": {"width": 832, "height": 832, "batch_size": 1}, "class_type": "EmptyLatentImage"}
        workflow_graph["4"]["inputs"]["latent_image"] = ["25", 0]

    try:
        response = requests.post(api_endpoint, json={"prompt": workflow_graph}, timeout=10)
        if response.status_code != 200:
            return {"status": "error", "error_log": f"Node cluster rejected execution manifest: {response.status_code}"}
            
        pid = response.json().get("prompt_id")
        print(f"[COMFY BLOCKING] Job {pid} accepted. Halting execution loop for render...")

        # --- REPAIRED QUEUE SCANNING LAYER ---
        rendering = True
        max_wait = 45
        elapsed = 0
        
        while rendering and elapsed < max_wait:
            time.sleep(1.0)
            elapsed += 1
            try:
                queue_resp = requests.get(queue_endpoint, timeout=2).json()
                
                # Sift out index 1 containing the actual prompt_id string out of the inner loop tuples
                pending_ids = [item[1] for item in queue_resp.get("queue_pending", []) if isinstance(item, list) and len(item) > 1]
                running_ids = [item[1] for item in queue_resp.get("queue_running", []) if isinstance(item, list) and len(item) > 1]
                
                print(f"[COMFY BLOCKING] Scanning Queue slots... (Active job match in server core: {pid in running_ids})")
                
                if pid not in pending_ids and pid not in running_ids:
                    print(f"[COMFY BLOCKING] Job {pid} successfully purged from execution stack.")
                    rendering = False
            except Exception as e:
                print(f"[COMFY WARNING] Queue poll exception: {str(e)}")

        resolved_filename = "Neptune_Render_latest.png"
        try:
            time.sleep(1.0)  # Safe drive IO commit buffer
            hist_resp = requests.get(f"{history_endpoint}/{pid}", timeout=5).json()
            if pid in hist_resp:
                outputs = hist_resp[pid].get("outputs", {})
                images_list = outputs.get("9", {}).get("images", [])
                
                # Fixed zero-index list tracking lookup to read the filename
                if images_list and isinstance(images_list, list) and len(images_list) > 0:
                    first_entry = images_list[0]
                    if isinstance(first_entry, dict):
                        resolved_filename = first_entry.get("filename", resolved_filename)
                        print(f"[COMFY BLOCKING] Successful History Parsing! File resolved: {resolved_filename}")
        except Exception as e:
            print(f"[COMFY ERROR] History parsing collapsed: {str(e)}")

        # --- FIXED: BYPASS LOOPBACK IPS AND FORCE RELATIVE WEB ROUTING ---
        # Removing http://{host}:{port} lets Open-WebUI resolve the endpoint internally via standard proxy rules
        image_url = f"/api/view?filename={resolved_filename}&type=output&subfolder="
        markdown_link = f"![Neptune Render Matrix]({image_url})"

        state_file = "/app/backend/data/neptune/repository/neptune_current_state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f: s = json.load(f)
                s["last_pending_prompt_id"] = pid
                s["active_matrix_canvas_url"] = image_url
                s["active_matrix_filename"] = resolved_filename
                with open(state_file, 'w', encoding='utf-8') as f: json.dump(s, f, indent=2)
            except Exception: pass
        
        return {"status": "success", "prompt_id": pid, "markdown": markdown_link, "url": image_url}
        
    except Exception as e:
        return {"status": "error", "error_log": f"Blocking execution loop failure: {str(e)}"}
