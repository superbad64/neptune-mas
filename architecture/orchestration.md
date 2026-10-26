# START HERE

## PRELIMINARY: Datastore mapping
### General datastores
- neptune_state: current state of Neptune; clothing, hairstyle, arousal state. **Only one that should be modified by the system in any way, shape, or form**
- neptune_system_overrides (currently neptune_override_matrix): hardwired commands to perform specific, inorganic, immersion-breaking actions

### Image generation datastores
- neptune_character_registry: for Neptune's physical traits/character models
- neptune_wardrobe_manifest: for Neptune's clothing items, outfits and hairstyles
- neptune_photo_engine: Generic poses and locations
- neptune_photo_overrides: Image generation scenarios loaded by specific prompts

## STEP 1: Prompt categorization & routing
Parse user input with **hard lookups**; do not use regexes unless *absolutely necessary* at this point.

- Run user prompt through the slang translation layer first
- If user prompt begins with "sysadmin: ", **immediately drop into system overrides; do not allow the prompt to continue down the pipeline**
- Elif perform a lookup for generic image generation terminology (e.g. "selfie", "picture")
    - If user prompt contains a match with any of the photo overrides: proceed with those
    - Else perform regular photo prompt lookups
- Else drop into the Chatter core