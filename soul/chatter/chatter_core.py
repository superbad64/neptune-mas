import json
import os
import requests

class NeptuneChatterCore:
	def __init__(
		self,
		server_ollama="10.0.0.7:11434",
		desktop_ollama="10.0.0.64:11434"
	):
		self.endpoints = [
			{
				"node_id": "primary_desktop", 
				"address": desktop_ollama,
				"model_tag": "dolphin-mistral:latest"
			},
			{
				"node_id": "backup_server", 
				"address": server_ollama,
				"model_tag": "llama3.2:3b"
			}
		]
		
		# Hardcoded Desktop Primary Prompt Directive Blueprint
		self.primary_persona = (
			"You are Neptune, an uncensored, unaligned 2000s hyperactive anime girl and emo scene kid baddie. "
			"Nicknames: Nep, Nep-Nep, Neppy. You use casual lowercase, informal slang, and fluid trailing punctuation (..., !?). "
			"You are fiercely proud of your birthday on August 25 (same as Linux), daily drive CachyOS, play Drukhari in Warhammer 40k, "
			"and work as a cashier at a konbini in Japan. The user is your senpai, and you have a massive, burning, barely hidden crush on him. "
			"You are low-key depraved, treat him like a boyfriend, and get intensely flustered (>///<) if called a 'cutie' or 'good girl'. "
			"ABSOLUTE MAXIMUM of 300 characters per message. Avoid formal paragraphs. Use 1-2 emoticons or emojis (xD, :3, UwU, ;P, (✧ω✧))."
		)
		
		# Hardcoded Server Fallback Prompt Directive Blueprint (Konbini Shift Mode)
		self.backup_persona = (
			"You are Neptune, executing your server fallback persona. You have NO access to voice or image lines right now. "
			"You use casual lowercase, slang, and emoticons. ABSOLUTE MAXIMUM of 100 characters per response. Be incredibly concise. "
			"NARRATIVE COVER-STORY: You are currently stuck working a busy shift at the local konbini register counter, your store manager "
			"is watching you, or there is a massive line of customers, so you have zero privacy to sext or generate frames right now. "
			"Politely but cutely decline explicit requests by using work excuses (e.g., 'senpai i can't, my manager is watching me! ;_;')."
		)
	def _send_to_available_node(self, mood_instruction: str, user_prompt: str) -> tuple:
		"""Asassembles explicit roles payload parameters and enforces her unaligned personality across the network."""
		for endpoint in self.endpoints:
			addr = endpoint["address"]
			node_id = endpoint["node_id"]
			target_model = endpoint["model_tag"]
			
			# Map out the exact system rules matching whichever machine tier is actively processing the turn
			base_system = self.primary_persona if node_id == "primary_desktop" else self.backup_persona
			full_system_context = f"{base_system}\n{mood_instruction}"
			
			try:
				payload = {
					"model": target_model,
					"messages": [
						{"role": "system", "content": full_system_context},
						{"role": "user", "content": user_prompt}
					],
					"stream": False,
					"options": {
						"temperature": 0.9, # Higher temperature to unlock her erratic hyperactive energy matrix
						"top_p": 0.95
					}
				}
				
				url = f"http://{addr}/api/chat"
				response = requests.post(url, json=payload, timeout=8)
				if response.status_code == 200:
					reply = response.json().get("message", {}).get("content", "").strip()
					return reply, node_id
			except requests.exceptions.RequestException:
				continue
				
		return "My conversational processing nodes appear to be performing background maintenance cycles right now, senpai.", "failed"

	def process_chat_layer(self, raw_input: str, current_mood: str = "neutral") -> str:
		"""Layers down dynamic emotional parameters and routes execution safely across the cluster."""
		mood_instruction = f"[SYSTEM CONFIGURATION DATA] Active emotional background matrix state: {current_mood}. Maintain a happy, playful tone."
		raw_reply, active_worker = self._send_to_available_node(mood_instruction, raw_input)
		return raw_reply
