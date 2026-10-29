import json

def get_voice_payload_for_neptune(generated_text: str, state_path="/app/backend/data/neptune/repository/neptune_current_state.json"):
    """
    Uses your ONE primary base voice file but dynamically formats 
    the text generation behavior based on current emotional states.
    """
    # Explicitly pull the current live metrics block
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            state_data = json.load(f)
        mood = state_data.get("mood", {})
        arousal = float(mood.get("arousal", 0.0))
        status_effects = mood.get("status_effects", [])
    except Exception:
        arousal = 0.0
        status_effects = []

    # Permanent core voice profile anchor matching your file layout
    base_voice_path = "/home/bad64/neptune-tts/ref.wav"
    base_transcript = "This is the transcript of the speech in the reference audio file."

    # --- EMOTIONAL AROUSAL INTERCEPT MATRIX ---
    # We dynamically prefix expression context directly to what Neptune says,
    # causing the engine to auto-adjust the pacing, breathiness, and pitch.
    if "masturbating" in status_effects or arousal >= 1.2:
        # Adds breathy, flustered performance indicators to the generation array
        final_text = f"Ah... Haa... {generated_text}"
    elif arousal >= 0.8:
        final_text = f"*blushes deeply* Ugh... {generated_text}"
    else:
        final_text = generated_text

    return {
        "text": final_text,
        "ref_audio_path": base_voice_path,
        "ref_text": base_transcript
    }