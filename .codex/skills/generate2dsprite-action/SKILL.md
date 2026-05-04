---
name: generate2dsprite-action
description: "Create a single action animation (6-8 frames) anchored to an existing origin sprite. Supports idle, walk, run, jump. Outputs to output/{character_name}/action/{action_type}."
---

# Generate2dsprite-action

Generate a single action animation referencing a character origin sprite. Use this after origin is confirmed. Each action can be generated and reviewed independently.

## Parameters

Infer these from the user request:

- `character_name`: must match the origin folder name (e.g., `elder-samurai`)
- `action_type`: `idle` | `walk` | `run` | `jump`
- `target_frames`: `6` | `8` (default: `8`)
- `origin_image_path`: Auto-inferred from `{output_base_path}/{character_name}/origin/sheet-transparent.png`
- `output_base_path`: Optional override (default: `output/`)

## Agent Rules

- Load the origin sprite image before writing the action prompt.
- Use the origin image as the visual reference (call `view_image` if it's a local file).
- Write the action prompt manually using the template below, referencing the origin to maintain character consistency.
- Use built-in `image_gen` to generate the action animation.
- Each action is independent—user can retry, adjust, or skip without affecting other actions.
- Output path: `{output_base_path}/{character_name}/action/{action_type}/`
- Apply consistent QC settings: `shared_scale=true`, `align=feet`, `reject-edge-touch`.

## Workflow

### 1. Load the origin sprite

Retrieve the origin image from: `{output_base_path}/{character_name}/origin/sheet-transparent.png`

Use `view_image` if it's a local file path. Do not rely on a filesystem path as the visual input—make sure the image is visible in context.

### 2. Determine frame count and layout

- 6 frames: `2x3` grid
- 8 frames: `2x4` grid

Infer from `target_frames` parameter or request.

### 3. Write the action prompt manually

Use the auto-generated template from the action script, but customize frame descriptions based on animation intent.

**Common action templates:**

#### Idle (6-8 frames)
```text
Use the image just shown as the visual reference (origin sprite).

Preserve exactly: same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE facing direction (15-25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art idle sprite sheet with exactly [6 or 8] equal cells in a [2x3 or 2x4] grid.
No borders, no separators, no labels, no text anywhere.

Frame intent (in reading order):
1. neutral stance, weight settled
2. subtle inhale
3. slight hair or robe cloth motion
4. gentle exhale and micro weight shift
5. secondary idle accent
6. return toward neutral loop state
[7. smoother in-between (if 8 frames)]
[8. smoother transition (if 8 frames)]

Consistency and containment rules:
Identical character bounding-box width and height in all cells.
Fixed outer bounding-box aspect ratio matching the origin reference, unchanged frame-to-frame.
Identical pixel scale to the origin reference in all frames, no zoom in or zoom out.
If holding weapon or prop, it must stay inside the same bounding-box envelope in every frame.
Leave visible magenta margin on all four sides in every frame.
No body part, weapon, effect, or accessory may cross any cell edge.

Background and output rules:
Background must be 100% solid flat #FF00FF.
No gradients. No UI. No speech bubbles. No watermark.
Crisp, gameplay-readable pixel art suitable for RPG sprite animation.
```

#### Walk (6-8 frames)
```text
Use the image just shown as the visual reference (origin sprite).

Preserve exactly: same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE facing direction (15-25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art walk sprite sheet with exactly [6 or 8] equal cells in a [2x3 or 2x4] grid.
No borders, no separators, no labels, no text anywhere.

Frame intent (in reading order):
1. contact pose A (right foot forward)
2. recoil and weight transfer
3. passing pose mid-stride
4. contact pose B (left foot forward)
5. recoil and weight transfer
6. passing pose mid-stride
[7. smoother contact transition (if 8 frames)]
[8. smoother passing transition (if 8 frames)]

Consistency and containment rules:
Identical character bounding-box width and height in all frames.
Fixed outer bounding-box aspect ratio matching the origin reference, unchanged frame-to-frame.
Identical pixel scale to the origin reference in all frames, no zoom in or zoom out.
If holding weapon or prop, it must stay inside the same bounding-box envelope in every frame.
Leave visible magenta margin on all four sides in every frame.
No body part, weapon, effect, or accessory may cross any cell edge.

Background and output rules:
Background must be 100% solid flat #FF00FF.
No gradients. No UI. No speech bubbles. No watermark.
Crisp, gameplay-readable pixel art suitable for RPG sprite animation.
```

#### Run (6-8 frames)
```text
Use the image just shown as the visual reference (origin sprite).

Preserve exactly: same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE facing direction (15-25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art run sprite sheet with exactly [6 or 8] equal cells in a [2x3 or 2x4] grid.
No borders, no separators, no labels, no text anywhere.

Run is faster and more energetic than walk, with stronger forward lean and airborne moments.

Frame intent (in reading order):
1. push-off A with strong forward lean
2. airborne extension and momentum
3. landing A with impact absorption
4. push-off B with strong forward lean
5. airborne extension and momentum
6. landing B with impact absorption
[7. smoother airborne transition (if 8 frames)]
[8. smoother landing transition (if 8 frames)]

Consistency and containment rules:
Identical character bounding-box width and height in all frames.
Fixed outer bounding-box aspect ratio matching the origin reference, unchanged frame-to-frame.
Identical pixel scale to the origin reference in all frames, no zoom in or zoom out.
If holding weapon or prop, it must stay inside the same bounding-box envelope in every frame.
Leave visible magenta margin on all four sides in every frame.
No body part, weapon, effect, or accessory may cross any cell edge.

Background and output rules:
Background must be 100% solid flat #FF00FF.
No gradients. No UI. No speech bubbles. No watermark.
Crisp, gameplay-readable pixel art suitable for RPG sprite animation.
```

#### Jump (6-8 frames)
```text
Use the image just shown as the visual reference (origin sprite).

Preserve exactly: same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE facing direction (15-25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art jump sprite sheet with exactly [6 or 8] equal cells in a [2x3 or 2x4] grid.
No borders, no separators, no labels, no text anywhere.

Frame intent (in reading order):
1. crouch wind-up, knees bent
2. deeper compression and launch prep
3. takeoff extension, rising from ground
4. apex hold, peak of jump
5. descent, falling
6. landing absorption and recovery
[7. smoother launch phase (if 8 frames)]
[8. smoother descent phase (if 8 frames)]

Consistency and containment rules:
Identical character bounding-box width and height in all frames.
Fixed outer bounding-box aspect ratio matching the origin reference, unchanged frame-to-frame.
Identical pixel scale to the origin reference in all frames, no zoom in or zoom out.
If holding weapon or prop, it must stay inside the same bounding-box envelope in every frame.
Leave visible magenta margin on all four sides in every frame.
No body part, weapon, effect, or accessory may cross any cell edge.

Background and output rules:
Background must be 100% solid flat #FF00FF.
No gradients. No UI. No speech bubbles. No watermark.
Crisp, gameplay-readable pixel art suitable for RPG sprite animation.
```

### 4. Generate the action image

Use built-in `image_gen`.

After generation:
- Find the raw PNG under `$CODEX_HOME/generated_images/...`
- Copy or reference it from the output folder
- Keep the original generated image in place

### 5. Postprocess with `generate2dsprite.py process`

Run the processor with consistent settings:
```
python scripts/generate2dsprite.py process \
  --input <raw-image> \
  --target character --mode <action_type> \
  --output-dir output/{character_name}/action/{action_type}/ \
  --rows <rows> --cols <cols> \
  --shared-scale \
  --align feet \
  --component-mode all \
  --reject-edge-touch
```

### 6. Output structure

Create output directory at: `{output_base_path}/{character_name}/action/{action_type}/`

Expected outputs in this folder:
- `sheet-transparent.png` (the main action sprite sheet)
- `<action>-1.png` through `<action>-N.png` (individual frame PNGs)
- `animation.gif` (loopable animation preview)
- `prompt-used.txt` (the prompt that generated this)
- `pipeline-meta.json` (QC metadata, aspect ratio drift, edge touch info)

### 7. User review and retry

User can review the output and:
- Approve and move to the next action
- Retry this action with adjusted parameters or regenerated prompt
- Skip this action entirely

Each action is independent—retrying one action does not affect others.

## Defaults

- **target_frames**: `8` (2x4 grid)
- **align**: `feet` (for grounded characters)
- **shared_scale**: `true` (all frames same size)
- **component_mode**: `all` (keep weapon/prop silhouettes)
- **aspect_ratio_tolerance**: `0.03` (3% drift allowed, can be tightened)
- **output_base_path**: `output/`
- **background**: Always solid `#FF00FF`

## Resources

- [generate2dsprite script](../../generate2dsprite/scripts/generate2dsprite.py) for postprocessing
- Frame count and grid layout guide: 6 frames = 2x3, 8 frames = 2x4
- QC metadata in pipeline-meta.json includes aspect ratio drift and edge touch detection
