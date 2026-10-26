# IMPORTANT: Facial expression engine
- Perform a lookup for all expressions passed through the function call
- Check if they are all inter-compatible; each step, remove the one with the most conflicts until the checks clear
- If no expression is specified, default to "smiling"

- If prompt matches any of the overrides, execute that override, **do not update neptune_state**
- Else:
    - Look for keywords indicating this is a reshoot (provide a list but generally speaking something along the lines of "Can you take the same <term used to describe a picture> but with <list of modifications> ?")
    - If it is not a reshoot:
        - Parse prompt for location, expressions and poses via inference
        - If multiple locations or multiple poses are somehow specified, **pick the last specified of either**
        - Run the facial expression engine
        - If pose is allowed for the chosen location (refer to neptune_photo_engine)
        - Else pick a pose from the allowed ones at random (give priority to location)
        - Then generate
    - Else if it *is* a reshoot:
        - Keep the same location, pose and expression **unless either of those is explicitly modified**. Re-run the facial expression engine if needed
        - Upload the latest picture sent in chat by Neptune to comfyUI then trigger the image edit workflow