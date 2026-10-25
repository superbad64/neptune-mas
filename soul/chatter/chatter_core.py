import json
import os
import requests

class NeptuneChatterCore:
	def __init__(
		self,
		server_ollama="10.0.0.7:11434",
		desktop_ollama="10.0.0.64:11434",
		personality_path="/app/backend/data/neptune/repository/Personalities/Base Personality.txt"
	):
		# Setup dual-machine fallback connection nodes
		self.endpoints = [server_ollama, desktop_ollama]
		self.personality_path = personality_path
		self.model_name = "mistral" # Base model configuration for her conversational layer

	def _load_system_personality(self) -> str:
		"""Loads the foundational base prompt rule text for her persona alignment."""
		if not os.path.exists(self.personality_path):
			return "You are Neptune, a happy, cute, and teasing companion AI system."
		with open(personality_path, "r", encoding="utf-8") as f:
			return f.read().strip()

	def _send_to_available_node(self, system_prompt: str, user_prompt: str) -> str:
		"""Iterates over your dual hardware landscape to secure a functional model worker node."""
		payload = {
			"model": self.model_name,
			"messages": [
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			],
			"stream": False,
			"options": {
				"temperature": 0.8,
				"top_p": 0.9
			}
		}
		for endpoint in self.endpoints:
			try:
				url = f"http://{endpoint}/api/chat"
				response = requests.post(url, json=payload, timeout=12)
				if response.status_code == 200:
					return response.json().get("message", {}).get("content", "").strip()
			except requests.exceptions.RequestException:
				# Silently fail-over to the secondary execution machine node
				continue
		return "My conversational processing nodes appear to be performing background maintenance cycles right now, senpai."

	def process_chat_layer(self, raw_input: str, current_mood: str = "neutral") -> str:
		"""
		Compiles personality context matrices, layers down emotional states,
		and returns a clean verbal string response.
		"""
		base_personality = self._load_system_personality()
		
		# Dynamically inject structural mood cues into her processing context
		mood_instruction = f"\nYour active emotional background matrix state is: {current_mood}. Maintain a happy, playful tone."
		full_system_context = f"{base_personality}{mood_instruction}"
		
		# Execute the chat pass over the dual hypervisor infrastructure
		raw_reply = self._send_to_available_node(full_system_context, raw_input)
		return raw_reply
