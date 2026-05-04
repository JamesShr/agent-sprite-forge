---
name: generate2dsprite-origin
description: "Create a single static character sprite (origin) as the visual anchor for all future animation phases. Outputs to output/{character_name}/origin."
---

# Generate2dsprite-origin

Generate a single 1x1 static character portrait. This origin sprite becomes the visual reference for all subsequent action phases (idle, walk, run, jump).

## Parameters

Infer these from the user request:

- `character_name`: kebab-case identifier (e.g., `elder-samurai`, `fire-wizard`)
- `character_concept`: Brief description of the character (silhouette, costume, key features, expression)
- `facing_direction`: `sse` (south-southeast, default) | `nne` (north-northeast) | `frontal`
- `output_base_path`: Optional override (default: `output/`)

## Agent Rules

- Decide the character concept and facing direction yourself.
- Write the art prompt manually to ensure clarity and consistency.
- Use built-in `image_gen` to generate the origin sprite.
- The origin image is static (no animation), showing the character in neutral idle pose.
- Keep silhouette, palette, and expression clear and readable.
- This origin image will be referenced in all future action phases—ensure it is production-quality before proceeding.
- Do NOT proceed to action phase generation until the user confirms the origin is satisfactory.
- Output path: `{output_base_path}/{character_name}/origin/`

## Workflow

### 1. Infer the origin concept

Pick character silhouette, costume, pose, and facing direction from the request.

Example: "elder-samurai facing southeast with stern expression, white beard, white kimono" → `character_name=elder-samurai`, `facing_direction=sse`

### 2. Write the prompt manually

Use the following template:

**For SSE (South-Southeast) facing:**

```text
Character concept: [your character description].

Create a single 2D pixel-art character sprite.
No animation, no grid, just one static portrait.

Camera and facing style:
Near-frontal 3/4 front view, south-southeast facing (SSE).
Character is mostly front-facing with a subtle yaw bias toward screen-right.
Yaw around 15 to 25 degrees from frontal, never beyond 30 degrees.
Both eyes must remain clearly visible. The far eye can be slightly narrower.

Pose: neutral standing idle, weight settled.
Arms relaxed at sides or natural resting position.
If holding weapon or prop, positioned naturally at rest.

Consistency rules:
Centered in canvas with generous magenta margin on all sides.
Clear, readable silhouette and palette.
Will be used as the visual reference for all future animation sheets.

Background and output rules:
Background must be 100% solid flat #FF00FF.
No gradients. No UI. No speech bubbles. No watermark.
Crisp, gameplay-readable pixel art.
```

### 3. Generate the origin image

Use built-in `image_gen`.

After generation:
- Find the raw PNG under `$CODEX_HOME/generated_images/...`
- Copy or reference it from the output folder
- Keep the original generated image in place

### 4. Output structure

Create output directory at: `{output_base_path}/{character_name}/origin/`

Expected outputs in this folder:
- `sheet-transparent.png` (the main origin sprite)
- `animation.gif` (single frame, or same as PNG for preview)
- `prompt-used.txt` (the prompt that generated this)
- `pipeline-meta.json` (QC metadata)

### 5. User confirmation

Wait for user to confirm the origin sprite is satisfactory.

Only after confirmation should the user proceed to `generate2dsprite-action` to create animation phases.

## Defaults

- **facing_direction**: `sse` (south-southeast, recommended for variety)
- **output_base_path**: `output/`
- **background**: Always solid `#FF00FF`
- **style**: Near-frontal 3/4, pixel-art game-ready

## Resources

- Facing directions: `sse` (15~25° right bias), `nne` (15~25° left bias), `frontal` (0° no bias)
- For more control, pair with `generate2dsprite-action` to create animations
