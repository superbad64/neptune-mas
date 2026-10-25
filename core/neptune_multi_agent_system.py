import sys
import os
import importlib
import json
import re

try:
	neptune_root = "/app/backend/data/neptune"
	if neptune_root not in sys.path:
		sys.path.insert(0, neptune_root)

	# Brute-force purge the custom modules out of Python's active sys.modules registry map
	for module_key in list(sys.modules.keys()):
		if any(module_key.startswith(pkg) for pkg in ["mind", "body", "soul", "core"]):
			del sys.modules[module_key]

	# Force-compile fresh class definitions natively straight from the disk sector hooks
	import mind.inspector
	import body.pipeline_compiler
	import body.comfy_dispatch
	import soul.dialog_router
	import soul.chatter.chatter_core
	import core.orchestrator

	importlib.reload(mind.inspector)
	importlib.reload(body.pipeline_compiler)
	importlib.reload(body.comfy_dispatch)
	importlib.reload(soul.dialog_router)
	importlib.reload(soul.chatter.chatter_core)
	importlib.reload(core.orchestrator)

	# Purge old references to force clean filesystem module compilation from disk hooks
	for module_key in list(sys.modules.keys()):
		if any(module_key.startswith(pkg) for pkg in ["mind", "body", "soul", "core"]):
			del sys.modules[module_key]

	from mind.inspector import NeptuneInspector
	from body.pipeline_compiler import PipelineCompiler
	from body.comfy_dispatch import ComfyDispatcher
	from body.clothing_engine import NeptuneClothingEngine # Corrected: Linked to Body root package namespace
	from soul.dialog_router import NeptuneDialogRouter
	from soul.chatter.chatter_core import NeptuneChatterCore
	from core.orchestrator import NeptuneOrchestrator

	LOAD_ERROR_TRACEBACK = None
except Exception as e:
	import traceback

	LOAD_ERROR_TRACEBACK = f"🚨 **Top-Level Loading Crash Intercepted**:\n```text\n{traceback.format_exc()}\n```"


class Pipe:
	def __init__(self):
		self.workflow_template = "/app/backend/data/neptune/repository/Image generation/ponyrealism_workflow.json"
		self.state_path = "/app/backend/data/neptune/repository/neptune_state.json"

		self.slang_map = {
			"fr": "for real",
			"rn": "right now",
			"idk": "I do not know",
			"ngl": "not going to lie",
			"afk": "away from keyboard",
			"brb": "be right back",
			"smh": "shaking my head",
			"imo": "in my opinion",
			"wanna": "want to",
			"gonna": "going to",
			"imma": "I am going to",
			"gotta": "got to",
			"tits": "breasts",
			"titties": "breasts",
			"boobs": "breasts",
			"boobies": "breasts",
			"pussy": "crotch",
			"vagina": "crotch",
			"cunt": "crotch",
			"cooch": "crotch",
			"ass": "backside",
			"butt": "backside",
			"booty": "backside",
		}

	def preprocess_slang(self, text: str) -> str:
		"""Step 1 of Global Pipe Function: Flattens conversational shorthand slang lookups."""
		if not text:
			return ""
		words = text.split()
		normalized_words = []
		for word in words:
			clean_word = re.sub(r"[^\w]", "", word).lower()
			if clean_word in self.slang_map:
				normalized_words.append(self.slang_map[clean_word])
			else:
				normalized_words.append(word)
		return " ".join(normalized_words)

	def pipe(self, body: dict) -> str:
		"""Executes turn orchestration while tracking dynamic runtime valve overrides."""
		if LOAD_ERROR_TRACEBACK:
			return LOAD_ERROR_TRACEBACK

		try:
			# Force reload the exact module dependencies directly inside the running execution thread pass
			importlib.reload(mind.inspector)
			importlib.reload(core.orchestrator)

			# Instantiate classes using the freshly reloaded modules directly
			inspector_inst = mind.inspector.NeptuneInspector()
			compiler_inst = PipelineCompiler()
			dispatcher_inst = ComfyDispatcher()
			chatter_inst = NeptuneChatterCore()

			router_inst = NeptuneDialogRouter(
				inspector_instance=inspector_inst, chatter_instance=chatter_inst
			)

			fresh_orchestrator = NeptuneOrchestrator(
				inspector=inspector_inst,
				compiler=compiler_inst,
				dispatcher=dispatcher_inst,
				router=router_inst,
			)

			messages = body.get("messages", [])
			if not messages:
				return "Error: No inbound message payload vectors detected."

			raw_user_input = messages[-1].get("content", "")

			# Dynamic Valve Check Interface
			normalized_check = raw_user_input.lower().strip()
			if normalized_check == "sysadmin: debug on":
				fresh_orchestrator._update_state_matrix({"runtime_debug_active": True})
				return "🔧 **System Valve Overwrite**: Dynamic runtime diagnostics set to **ACTIVE**."
			elif normalized_check == "sysadmin: debug off":
				fresh_orchestrator._update_state_matrix({"runtime_debug_active": False})
				return "🔧 **System Valve Overwrite**: Dynamic runtime diagnostics set to **DISABLED**."

			clean_input = self.preprocess_slang(raw_user_input)
			turn_result = fresh_orchestrator.process_agent_turn(
				raw_user_prompt=clean_input,
				workflow_template_path=self.workflow_template,
			)

			current_state = fresh_orchestrator._get_active_state()
			if current_state.get("runtime_debug_active", False):
				debug_payload = {
					"__valve_status__": "DYNAMIC_DEBUG_ACTIVE",
					"input_processed": clean_input,
					"orchestrator_output": turn_result,
				}
				return f"```json\n{json.dumps(debug_payload, indent=4)}\n```"

			return turn_result.get("output_response", "Processing anomaly encountered.")

		except Exception as run_error:
			import traceback

			return f"💥 **Runtime Exception Caught Intercepted**:\n```text\n{traceback.format_exc()}\n```"
