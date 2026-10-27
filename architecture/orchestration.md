# START HERE

## PRELIMINARY: Datastore mapping
### General datastores
- neptune_current_state: current state of Neptune; clothing, hairstyle, arousal state. **Only one that should be modified by the system in any way, shape, or form**
- neptune_system_overrides: hardwired commands to perform specific, inorganic, immersion-breaking actions; go to "system overrides.md"

### Image generation datastores
- neptune_character_registry: for Neptune's physical traits/character models
- neptune_wardrobe_manifest: for Neptune's clothing items, outfits and hairstyles
- neptune_photo_engine: Generic poses and locations
- neptune_photo_overrides: Image generation scenarios loaded by specific prompts

## The Face router
- Handles a "slang translation layer" that picks up various synonyms (e.g. "titties" for "breasts", "snap" for "picture", and so on), acronyms ("brb", "idk", etc), abbreviated forms ("gonna" for "going to", "dunno" for "don't know"). **Don't hesitate to be exhaustive**; I'd rather have way too many synonyms than not enough and discover it in the middle of a session
- Looks up modules and cores in their respective subfolders (body, mind and soul)

## Prompt categorization & routing
Parse user input with **hard lookups**; do not use regexes unless *absolutely necessary* at this point.

- Run user prompt through the slang translation layer first
- If user prompt begins with "neptunectl", **immediately drop into system overrides; do not allow the prompt to continue down the pipeline**
- Perform a lookup for generic image generation terminology (e.g. "selfie", "picture")
    - If user prompt contains a match with any of the photo overrides: proceed with those
    - Else perform regular photo prompt lookups
- Perform a lookup for clothes editing vocabulary ("go nude", "put on...", "remove...")
- Else drop into the Chatter core who will then handle the message through spice gradation