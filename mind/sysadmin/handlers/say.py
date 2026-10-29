import os
import requests
import hashlib
import time
import traceback

def execute_say(cmd_body: str, lowered_cmd: str, state_data: dict, state_path: str, registry_path: str, root: str) -> str:
    """
    Text synthesis executor aligned with the bare-metal WSL F5-TTS streaming API.
    Sends the correct reference voice paths and returns an HTML5 audio control block.
    """
    test_speech = cmd_body.replace("say", "", 1).strip()
    if not test_speech:
        return "❌ Syntax Error. Provide text: `neptunectl say [your text here]`"
        
    try:
        # Target your dedicated WSL AI instance cross-LAN interface over port 8000
        tts_url = "http://10.0.0.64:8000/v1/tts"
        
        # --- FIXED: ALIGN PAYLOAD WITH NATIVE OBJECT API REQUIREMENTS ---
        # ref_audio_path is a local path inside the WSL filesystem where the model runs
        json_payload = {
            "text": test_speech,
            "ref_audio_path": "/home/bad64/neptune-tts/neptune_voice_base.wav", 
            "ref_text": "i'm feeling extra hormonal today i am straight but i wanna be gay i low-key kinda wanna be degraded sorry master sorry gochujin-sama please punish me for talking too loud please"
        }
        
        print(f"[SYSADMIN NATIVE] Dispatching updated payload parameters to {tts_url}")
        
        # Execute the network request to capture the binary audio stream
        response = requests.post(tts_url, json=json_payload, timeout=30)
        
        if response.status_code == 200:
            task_hash = hashlib.md5(f"{test_speech[:10]}{time.time()}".encode('utf-8')).hexdigest()[:8]
            output_filename = f"vacuum_test_{task_hash}.wav"
            
            output_path = f"{root}/public/audio_cache/{output_filename}"
            public_url_route = f"/public/audio_cache/{output_filename}"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write the raw binary stream data directly to the public cache path
            with open(output_path, "wb") as f:
                f.write(response.content)
                
            # --- FIXED: STANDARD HYPERLINK SYNTAX TO BYPASS BROKEN IMAGE CANVAS RUNTIMES ---
            markdown_element = f"\n\n🔗 **[Listen to Neptune Audio Output]({public_url_route})**"
            
            return f"✅ **[VOICE TEST SUCCESSFUL]**: Audio generated successfully!\n{markdown_element}"
        else:
            return f"❌ **[VOICE TEST REJECTED]**:\n* Status Code: `{response.status_code}`\n* Server Error Response: `{response.text}`"
            
    except Exception as say_err:
        return f"❌ **[CRITICAL SYSADMIN NETWORK EXCEPTION]**:\n```\n{traceback.format_exc()}\n```"
