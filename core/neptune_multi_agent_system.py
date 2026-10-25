import json
import os
import re

from mind.inspector import NeptuneInspector
from body.pipeline_compiler import PipelineCompiler
from body.comfy_dispatch import ComfyDispatcher
from soul.dialog_router import NeptuneDialogRouter
from soul.chatter.chatter_core import NeptuneChatterCore
from core.orchestrator import NeptuneOrchestrator

class Pipe:
	def __init__(self):
		# Instantiate all core components across the Mind, Body, and Soul layers
		self.inspector = NeptuneInspector()
		self.compiler = PipelineCompiler()
		self.dispatcher = ComfyDispatcher()
		self.chatter = NeptuneChatterCore()
		
		self.router = NeptuneDialogRouter(
			inspector_instance=self.inspector,
			chatter_instance=self.chatter
		)
		
		# Bind them completely into the global Orchestrator engine
		self.orchestrator = NeptuneOrchestrator(
			inspector=self.inspector,
			compiler=self.compiler,
			dispatcher=self.dispatcher,
			router=self.router
		)
		
		# Step 1 Slang Normalization Dictionary
		self.slang_map = {
			"fr": "for real",
			"rn": "right now",
			"idk": "I do not know",
			"ngl": "not going to lie",
			"afk": "away from keyboard",
			"brb": "be right back",
			"smh": "shaking my head",
			"imo": "in my opinion"
		}
		
		self.workflow_template = "/app/backend/data/neptune/repository/comfy_workflow_preset.json"
	def preprocess_slang(self, text: str) -> str:
		"""Step 1 of Global Pipe Function: Flattens shorthand slang text arrays."""
		if not text:
			return ""
		
		words = text.split()
		normalized_words = []
		
		for word in words:
			# Remove trailing or preceding punctuation to keep lookups accurate
			clean_word = re.sub(r"[^\w]", "", word).lower()
			if clean_word in self.slang_map:
				normalized_words.append(self.slang_map[clean_word])
			else:
				normalized_words.append(word)
				
		return " ".join(normalized_words)

	def pipe(self, body: dict) -> str:
		"""Primary traffic coping point for the Open-WebUI container environment."""
		messages = body.get("messages", [])
		if not messages:
			return "Error: No inbound message payload vectors detected."
			
		raw_user_input = messages[-1].get("content", "")
		
		# Execute Step 1: Slang Normalization
		clean_input = self.preprocess_slang(raw_user_input)
		
		# Dispatch straight through the Orchestrator loop
		turn_result = self.orchestrator.process_agent_turn(
			raw_user_prompt=clean_input,
			workflow_template_path=self.workflow_template
		)
		
		# Extract verbal response output for the front panel display
		return turn_result.get("output_response", "Processing anomaly encountered.")
