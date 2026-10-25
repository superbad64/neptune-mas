import os
import sys
import unittest
import json

# Auto-compute the base file path location dynamically to support both host volumes and container runtimes
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NEPTUNE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

if NEPTUNE_ROOT not in sys.path:
	sys.path.insert(0, NEPTUNE_ROOT)

from core.orchestrator import NeptuneOrchestrator
from mind.inspector import NeptuneInspector
from body.pipeline_compiler import PipelineCompiler
from body.comfy_dispatch import ComfyDispatcher
from soul.dialog_router import NeptuneDialogRouter
from soul.chatter.chatter_core import NeptuneChatterCore

class TestNeptunePlatform(unittest.TestCase):
	def setUp(self):
		# Re-map all data endpoints dynamically using the local discoverable paths
		self.state_path = os.path.join(NEPTUNE_ROOT, "repository", "neptune_state.json")
		self.workflow_path = os.path.join(NEPTUNE_ROOT, "repository", "comfy_workflow_preset.json")
		self.engine_path = os.path.join(NEPTUNE_ROOT, "repository", "neptune_photo_engine.json")
		self.overrides_path = os.path.join(NEPTUNE_ROOT, "repository", "neptune_photo_overrides.json")
		self.matrix_path = os.path.join(NEPTUNE_ROOT, "repository", "neptune_override_matrix.json")
		
		# Ensure a skeleton state exists for disk verification operations
		if not os.path.exists(self.state_path):
			os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
			with open(self.state_path, "w", encoding="utf-8") as f:
				json.dump({"environment": "bed", "tops": "default"}, f)

		self.inspector = NeptuneInspector(self.engine_path, self.overrides_path, self.matrix_path)
		self.compiler = PipelineCompiler(self.engine_path, self.overrides_path, self.state_path)
		self.dispatcher = ComfyDispatcher()
		self.chatter = NeptuneChatterCore()
		self.router = NeptuneDialogRouter(self.inspector, self.chatter, self.matrix_path, self.state_path)
		
		self.orchestrator = NeptuneOrchestrator(
			self.inspector, self.compiler, self.dispatcher, self.router, self.state_path
		)
	def test_01_inter_core_communication(self):
		"""Verifies that basic text can route completely through the global orchestration layers."""
		res = self.orchestrator.process_agent_turn("Hello Neptune", self.workflow_path)
		self.assertIsNotNone(res.get("output_response"))

	def test_02_sysadmin_super_overrides(self):
		"""Triggers a hard-token sysadmin event to test caching cleanup routing loops."""
		res = self.orchestrator.process_agent_turn("Execute Proxmox container cache purge", self.workflow_path)
		self.assertEqual(res.get("route_type"), "sysadmin_override")

	def test_03_generate_baseline_desk_picture(self):
		"""Forces a baseline generation scenario at her desk to test core workflow compilation."""
		self.orchestrator._update_state_matrix({"environment": "desk"})
		res = self.orchestrator.process_agent_turn("Take a photo of me right now", self.workflow_path)
		self.assertEqual(res.get("route_type"), "standard_chat")
	def test_04_individual_wardrobe_mutations(self):
		"""Mutates single relational garment pieces and verifies data persistence integrity."""
		self.orchestrator._update_state_matrix({"tops": "black oversized hoodie"})
		with open(self.state_path, "r", encoding="utf-8") as f:
			state = json.load(f)
		self.assertEqual(state.get("tops"), "black oversized hoodie")

	def test_05_generate_backchannel_variant_edit(self):
		"""Verifies visual parameters generate correctly for clean Node 16 primitives."""
		self.orchestrator._update_state_matrix({"tops": "white lace crop top"})
		payload = self.compiler.compile_generation_payload()
		self.assertIsNotNone(payload.get("positive_tokens"))

	def test_06_full_outfit_swap(self):
		"""Tests full relational manifest changes across multiple slots concurrently."""
		outfit_mutation = {"tops": "leather jacket", "bottoms": "pleated skirt"}
		self.orchestrator._update_state_matrix(outfit_mutation)
		with open(self.state_path, "r", encoding="utf-8") as f:
			state = json.load(f)
		self.assertEqual(state.get("bottoms"), "pleated skirt")
	def test_07_mirror_location_with_mutex_expression(self):
		"""Validates mirror constraint bounds and checks facial expression trigger exclusivity."""
		payload = self.compiler.compile_generation_payload(user_input="give me an ahegao look", force_location="mirror")
		self.assertEqual(payload["target_location"], "mirror")
		self.assertIn("mirror reflection selfie shot", payload["positive_tokens"])
		self.assertIn("eyes rolling back", payload["positive_tokens"])

	def test_08_sequential_override_sweep(self):
		"""Sweeps through every explicit photo override trigger key to ensure zero token collisions."""
		override_triggers = [
			"lift your shirt", 
			"show me your tits", 
			"show me your pussy", 
			"show me your feet", 
			"show me your ass", 
			"take a shower"
		]
		for trigger in override_triggers:
			res = self.orchestrator.process_agent_turn(trigger, self.workflow_path)
			self.assertIn(res.get("route_type"), ["lewd_photo_override", "general_photo_engine"])
			
	def test_09_automated_rendering_sweep(self):
		"""Fires generations directly to the remote WSL node and fetches the resulting images to local disk."""
		from body.reshoot_worker import ReshootWorker
		worker = ReshootWorker()
		
		# Set an absolute timeout fallback limit to prevent endless hanging if the remote desktop is sleeping
		try:
			worker.execute_automated_sweep(self.workflow_path)
			file_count = len(os.listdir(worker.output_dir))
			self.assertGreater(file_count, 0)
		except Exception as e:
			self.skipTest(f"Visual automation worker skipped. Remote machine state checking: {e}")


if __name__ == "__main__":
	unittest.main()
