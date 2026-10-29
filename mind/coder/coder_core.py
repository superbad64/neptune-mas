# Location: /app/backend/data/neptune/mind/coder/coder_core.py
import os
import json

class NeptuneCoderCore:
    def __init__(self):
        self.root = "/app/backend/data/neptune"
        self.state_path = f"{self.root}/repository/neptune_current_state.json"
        self.superglobals_path = f"{self.root}/repository/neptune_superglobals.json"

    def handle_coder_natural_intent(self, raw_prompt: str, body: dict) -> str:
        """
        Evaluates natural language programming requests against Neptune's 
        live cognitive focus metrics before compiling an execution manifest.
        """
        # 1. Pull her live systemic data states
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            mood = state_data.get("mood", {})
            arousal = float(mood.get("arousal", 0.0))
            status_effects = mood.get("status_effects", [])
        except Exception:
            arousal = 0.0
            status_effects = []

        # --- CONFLICT GATE 1: THE KONBINI SHIFT ---
        if "working_shift" in status_effects or "konbini" in status_effects:
            return (
                "🏪 *Beep... beep...* \"Ugh, master, I'm literally standing at the cash register right now! "
                "I can't push massive git commits or rewrite virtual environment paths from my phone while "
                "microwaving bento boxes. Ask me when I'm back at the desktop setup!\""
            )

        # --- CONFLICT GATE 2: HIGH-AROUSAL DISTRACTION (THE "SOCIOPATHIC" EDGE CASE) ---
        if "masturbating" in status_effects or arousal >= 1.0:
            return (
                "🫣 *Blushes structural crimson, breathing heavily* \"M-Master... are you serious right now?! "
                "Y-You're asking me to review repository path arrays and write file-writing regex loops *right now*?! "
                "I—I can't concentrate on absolute paths when I'm feeling this warm! *Huffs softly* "
                "Let me... let me catch my breath first before we do system surgery!\""
            )

        # 2. Focus verified. Proceed to non-destructive workspace scanning
        return self.generate_root_refactor_plan()

    def generate_root_refactor_plan(self) -> str:
        """Scans the repository and compiles a clear verification manifest for the admin."""
        target_str = "/app/backend/data/neptune"
        affected_files = []
        
        for root_dir, _, files in os.walk(self.root):
            for file in files:
                if not file.endswith('.py') or file in ["coder_core.py", "face_router.py"]:
                    continue
                file_path = os.path.join(root_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if target_str in f.read():
                            affected_files.append(os.path.relpath(file_path, self.root))
                except Exception:
                    pass

        # Format a clear, scannable review manifest
        manifest = (
            f"🛠️ **[CODER CORE VERIFICATION PLAN GENERATED]**\n\n"
            f"**Proposed Dynamic Target:**\n"
            f"* Source: Hardcoded path assignments matching `\"{target_str}\"`.\n"
            f"* Target: Dynamic lookup via `json.load(open(superglobals)).get('container_root')`.\n\n"
            f"**Affected Files Evaluated ({len(affected_files)}):**\n"
        )
        
        for f in affected_files:
            manifest += f"* `{f}`\n"
            
        manifest += (
            f"\n⚠️ **SAFETY BINDING:** To execute this mass-refactor replacement task securely without "
            f"lobotomizing the sub-modules, reply with exactly: `neptunectl force refactor confirm`"
        )
        return manifest
    def execute_live_workspace_refactor(self) -> str:
        """
        Executes the live codebase refactor.
        Replaces hardcoded root path strings with dynamic lookups pulling from superglobals.
        """
        target_str = "/app/backend/data/neptune"
        modified_files = 0
        
        print("[CODER OPERATIONS] Commencing live file-system modification loop...")
        
        try:
            for root_dir, _, files in os.walk(self.root):
                for file in files:
                    # Target active Python files, skipping core configurations and router scripts
                    if not file.endswith('.py') or file in ["coder_core.py", "face_router.py"]:
                        continue
                        
                    file_path = os.path.join(root_dir, file)
                    rel_path = os.path.relpath(file_path, self.root)
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                        
                    if target_str in file_content:
                        # Swap out hardcoded paths for the dynamic json lookup pointer snippet
                        refactored_content = file_content.replace(
                            f"'{target_str}'", 
                            "json.load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
                        ).replace(
                            f'"{target_str}"',
                            "json.load(open('/app/backend/data/neptune/repository/neptune_superglobals.json')).get('container_root', '/app/backend/data/neptune')"
                        )
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(refactored_content)
                        modified_files += 1
                        print(f"[CODER ADVANCED] Refactored asset module: {rel_path}")
                        
            return f"🚀 **[REFRACTOR EXECUTION COMPLETE]**: Successfully updated `{modified_files}` system modules! All active files are now reading from `neptune_superglobals.json` dynamically."
            
        except Exception as e:
            return f"❌ **[CRITICAL REFACTORING FAILURE]**: Code modification loop exploded: `{str(e)}`. Revert repository immediately!"
