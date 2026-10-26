# SYSTEM OVERRIDES

If the user's prompt begins with "sysadmin: ", parse the rest of the command (once again only using hard lookups) for the following commands:

Note: "fit_check()" refers to the function described in "clothing engine.md:1"

---
- "clear cache": Clears the module cache. Returns how many items were cleaned up
- "debug on/off": Toggles a verbose output debug output (formatted JSON output inside its own code block with useful debug info like routing path, job passed to ComfyUI etc). Returns debug state
- "dress <args>"
    - "show": Returns fit_check() but bypasses prompt categorization
    - "<body part> <clothing item>": forces outfit alteration. **Must write to neptune_current_state.json on success**. Returns fit_check()
        - <body part> can be "outfit" in which case all outfit items are loaded at once
        - <body part> can also be "hair"
    - "clear": Shorthand for "dress outfit naked"; clears every clothing item. Returns fit_check()
- "force <args>"
    - "imgen <prompt>": immediately attempts to generate an image using <prompt> as a base (with character attributes and outfit factored in). Returns either an image or an error block detailing why image generation failed.
    - "state"
        - "check": returns neptune_current_state.json
        - "update": immediately writes to neptune_current_state.json. Returns neptune_current_state.json
        - "reset": deletes neptune_current_state.json, returns a message stating the file was deleted, or "file does not exist"
    - "arousal <value>": Sets her arousal value to <value>, bound between 0.0 and 1.6 inclusive.
- "help" or empty args: Returns this block minus this exact line
---