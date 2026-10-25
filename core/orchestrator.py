import json
import os

from mind.inspector import NeptuneInspector
from body.pipeline_compiler import PipelineCompiler
from body.comfy_dispatch import ComfyDispatcher
from soul.dialog_router import NeptuneDialogRouter

class NeptuneOrchestrator:
	def __init__(
		self,
		inspector: NeptuneInspector,
		compiler: PipelineCompiler,
		dispatcher: ComfyDispatcher,
		router: NeptuneDialogRouter,
		state_path="/app/backend/data/neptune/repository/neptune_state.json"
	):
		self.inspector = inspector
		self.compiler = compiler
		self.dispatcher = dispatcher
		self.router = router
		self.state_path = state_path

	def _update_state_matrix(self, mutations: dict) -> None:
		"""Updates persistent tracking variables on disk without touching volatile records."""
		if not mutations or not os.path.exists(self.state_path):
			return
			
		try:
			with open(self.state_path, "r", encoding="utf-8") as f:
				current_state = json.load(f)
			
			# Merge the structural properties inside state_mutations smoothly
			for key, val in mutations.items():
				current_state[key] = val
				
			with open(self.state_path, "w", encoding="utf-8") as f:
				json.dump(current_state, f, indent="\t")
		except Exception as e:
			print(f"[Orchestrator Warning] State sync operation dropped: {e}")
	def process_agent_turn(self, raw_user_prompt: str, workflow_template_path: str) -> dict:
		"""
		Executes a strict sequential pass: Token Inspection -> State Mutation 
		-> Prompt Compilation -> ComfyUI Dispatch -> Dialogue Output Routing.
		"""
		# 1. Evaluate incoming text tokens for routing targets
		eval_vector = self.inspector.evaluate_routing_vectors(raw_user_prompt)
		route_type = eval_vector.get("route_type")

		# Apply state updates directly if an override explicitly registers them
		if route_type == "lewd_photo_override":
			self._update_state_matrix(eval_vector.get("state_mutations", {}))

		# 2. Check if the active vector demands an image generation cycle
		compiled_visuals = None
		render_receipt = None
		
		if route_type in ["lewd_photo_override", "general_photo_engine"]:
			# Pass user input along down to resolve specific facial expression strings
			compiled_visuals = self.compiler.compile_generation_payload(user_input=raw_user_prompt)
			
			# Dispatch rendering parameters out to your remote WSL desktop node
			render_receipt = self.dispatcher.execute_render_pipeline(
				compiler_output=compiled_visuals,
				template_path=workflow_template_path
			)

		# 3. Compute final verbal output string through the Dialog Router matrix
		final_routing = self.router.route_interaction(
			raw_input=raw_user_prompt,
			compiled_generation_data=compiled_visuals
		)

		return {
			"route_type": route_type,
			"output_response": final_routing.get("output_text", ""),
			"render_pipeline_status": render_receipt.get("status") if render_receipt else "skipped",
			"comfy_prompt_id": render_receipt.get("prompt_id") if render_receipt else None
		}
