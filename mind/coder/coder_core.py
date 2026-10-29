import os
import json
import time
import requests

class NeptuneCoderCore:
    def __init__(self):
        superglobals_path = "/app/backend/data/neptune/repository/neptune_superglobals.json"
        try:
            with open(superglobals_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.container_root = config.get("container_root", "/app/backend/data/neptune")
        except Exception:
            self.container_root = "/app/backend/data/neptune"
            
        self.state_path = f"{self.container_root}/repository/neptune_current_state.json"
        self.task_cache_path = f"{self.container_root}/repository/coder_pending_task.json"
        self.log_dir = f"{self.container_root}/mind/coder/logs"
        self.target_endpoint = "http://10.0.0.7:11434/api/chat"
        os.makedirs(self.log_dir, exist_ok=True)

    def handle_coder_natural_intent(self, raw_prompt: str, body: dict) -> str:
        """Dynamically contextualizes natural language instructions against real file scans."""
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            mood = state_data.get("mood", {})
            if "working_shift" in mood.get("status_effects", []) or float(mood.get("arousal", 0.0)) >= 1.0:
                return "🫣 *Blushes* \"Master, I really can't focus on code structures or system modifications right now... Let me catch my breath first!\""
        except Exception:
            pass

        real_affected_files = []
        for root_dir, _, files in os.walk(self.container_root):
            for file in files:
                if not file.endswith('.py') or file in ["coder_core.py", "face_router.py"] or "logs" in root_dir:
                    continue
                file_path = os.path.join(root_dir, file)
                try:
                    real_affected_files.append(os.path.relpath(file_path, self.container_root))
                except Exception:
                    pass

        system_instruction = (
            "You are Neptune's Coder Core sub-module. Speak like a hyperactive 2000s anime scene kid baddie.\n"
            "Use casual lowercase, raw slang, and fluid trailing punctuation. Keep the total output punchy.\n\n"
            "CRITICAL ARCHITECTURE MATRICES:\n"
            "1. Output the exact list of system paths requiring adjustments inside a clean markdown list under the title 'target files :3'. Do not wrap the explanation text inside a python code block!\n"
            "2. THE DECOUPLING TASK: We are replacing the hardcoded string value with a dynamic JSON loader snippet! For every file in the list, show a clear layout mapping how `container_root = ` or `self.container_root = ` will be updated.\n"
            "3. MATCHING CONSTRAINT: You MUST show exactly this literal self-contained template as the replacement code structure:\n"
            "   __import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')\n"
            "4. Keep your scene-kid attitude intact throughout the layout, and wait for senpai's confirmation."
        )

        files_bullet_list = "\n".join([f"- {f}" for f in real_affected_files])
        user_injection = (
            f"Verified Target Files Found Programmatically:\n{files_bullet_list}\n\n"
            f"Senpai's Direct Programming Instruction: {raw_prompt}"
        )

        payload = {
            "model": "llama3.2:3b",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_injection}
            ],
            "options": {"temperature": 0.1},
            "stream": False
        }

        try:
            print(f"[CODER CORE TELEMETRY] Offloading repository scan pass to VM node: {self.target_endpoint}")
            response = requests.post(self.target_endpoint, json=payload, timeout=120)
            
            if response.status_code == 200:
                manifest_output = response.json()["message"]["content"].strip()
                with open(self.task_cache_path, "w", encoding="utf-8") as f:
                    json.dump({"pending_instruction": raw_prompt, "manifest_summary": manifest_output}, f, indent=2)
                
                confirmation_footer = (
                    "\n\n⚙️ **[CODER CORE STATUS: STANDBY]**\n"
                    "* **Review the verification plan above carefully.**\n"
                    "* Tell me **'looks good, go ahead'** or **'yes'** to authorize live code execution.\n"
                    "* Tell me **'cancel'** or **'no'** to discard this pending development sprint."
                )
                return f"{manifest_output}{confirmation_footer}"
            else:
                return f"❌ **[CODER CORE CLUSTER HTTP ERROR]**:\n* Status Code Received: `{response.status_code}`"
        except Exception as e:
            return f"❌ [CODER CORE CRITICAL ERROR]: Failed to dynamically compile manifest: {str(e)}"
    def execute_live_dynamic_refactor(self) -> str:
        """Executes a secure, deterministic path decoupling sweep across the lowercase standardized variable schema."""
        if not os.path.exists(self.task_cache_path):
            return "❌ **[CODER CORE]**: No pending development sprint found in the local cache map."

        try:
            with open(self.task_cache_path, "r", encoding="utf-8") as f:
                cached_task = json.load(f)
            instruction = cached_task.get("pending_instruction", "")
            manifest_summary = cached_task.get("manifest_summary", "")
        except Exception as e:
            return f"❌ **[CODER CORE]**: Failed to read task cache matrix: {str(e)}"

        # The literal dynamic asset lookup string injection target snippet
        injection_snippet = "__import__('json').load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
        modified_files = []
        log_data = {
            "timestamp": time.time(),
            "date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "user_task_requested": instruction,
            "proposed_manifest": manifest_summary,
            "refactored_modules_trace": []
        }

        try:
            print("[CODER OPERATIONS] Commencing deterministic lowercase path injection sweep...")
            for root_dir, _, files in os.walk(self.container_root):
                for file in files:
                    if not file.endswith('.py') or file in ["coder_core.py", "face_router.py"] or "logs" in root_dir:
                        continue
                        
                    file_path = os.path.join(root_dir, file)
                    rel_path = os.path.relpath(file_path, self.container_root)
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    file_changed = False
                    new_lines = []
                    
                    for line in lines:
                        # Scans strictly for the standardized variable name assignments matching our criteria
                        if " = " in line and ("container_root = " in line or "self.container_root = " in line):
                            left_side, _ = line.split(" = ", 1)
                            indent = line[:len(line) - len(line.lstrip())]
                            
                            # Reconstruct line swapping out the raw string for the dynamic lookups module loader snippet
                            line = f"{indent}{left_side.strip()} = \"{injection_snippet}\"\n"
                            file_changed = True
                            
                        new_lines.append(line)
                        
                    if file_changed:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        modified_files.append(rel_path)
                        log_data["refactored_modules_trace"].append(f"Decoupled paths inside: {rel_path}")

            self._write_journal_log(log_data)
            os.remove(self.task_cache_path)
            
            files_list_str = "\n".join([f"* `{f}`" for f in modified_files])
            return (
                f"🚀 **[DYNAMIC DECOUPLING PASSED]**\n\n"
                f"Coder core successfully injected the dynamic superglobals configuration lookup!\n"
                f"Updated `{len(modified_files)}` modules to resolve their paths dynamically from `neptune_superglobals.json`.\n\n"
                f"**Decoupled Modules List:**\n{files_list_str}\n\n"
                f"📂 *Verbose operations trace log archived to your logs ledger.*"
            )
            
        except Exception as runtime_err:
            return f"❌ **[DYNAMIC SCRIPT RUNTIME ERROR]**: Path decoupling injection loop exploded: `{str(runtime_err)}`"

    def clear_pending_task(self) -> str:
        """Safely flushes and removes the temporary development sprint cache ledger from disk."""
        if os.path.exists(self.task_cache_path):
            try:
                os.remove(self.task_cache_path)
                return "🗑️ **[CODER CORE]**: Pending development manifest discarded. Standby active, dude! :3"
            except Exception as e:
                return f"❌ **[CODER CORE]**: Cache flush failure: {str(e)}"
        return "💻 **[CODER CORE]**: Standby state active. Cache empty."

    def _write_journal_log(self, log_data: dict):
        """Generates a tracking ledger entry using human-readable date formats."""
        human_date_string = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(log_data['timestamp']))
        log_filename = f"coder_ops_{human_date_string}.json"
        log_path = os.path.join(self.log_dir, log_filename)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
        print(f"[CODER ADVANCED] Operation log saved: {log_path}")
