## new phase1  Generate Origin Sprite

### Sprite Cell Ratio And Size Responsibility

Use these rules for all future generation requests:

- Define sprite cell shape at generation time with `cell_ratio`.
- Define subject occupancy with `fill_margin`.
- Keep one character's `cell_ratio` and `fill_margin` consistent across origin, idle, walk, run, jump, and attack.
- Do not use generation prompts to encode relative in-game height between different characters.
- Relative in-game size is handled in Phaser runtime with `setScale()`.

Cell ratio format:

- `1:1` = 128 x 128 per cell
- `3:4` = 96 x 128 per cell
- `4:3` = 128 x 96 per cell
- `2:3` = 128 x 192 per cell
- `3:2` = 192 x 128 per cell

Fill margin format:

- `tight`: subject fills around 85-90% of the cell
- `normal`: subject fills around 70-80% of the cell
- `safe`: subject fills around 55-65% of the cell

Use $generate2dsprite-origin with the following parameters:

character_name: kebab-case identifier (e.g., elder-samurai, fire-wizard)
character_concept: Brief description of the character (silhouette, costume, key features, expression)
facing_direction: sse (south-southeast, default) | nne (north-northeast) | frontal
cell_ratio: 1:1 | 3:4 | 4:3 | 2:3 | 3:2 (default: 1:1)
fill_margin: tight | normal | safe (default: normal)
output_base_path: Optional override (default: output)

```
Use $generate2dsprite-origin to create a character origin sprite:
- character_name: "elder-samurai"
- character_concept: "elderly samurai with stern expression, white beard, white kimono, holding wooden staff"
- facing_direction: "sse"
- cell_ratio: "1:1"
- fill_margin: "normal"

Output location: output/elder-samurai/origin/
Expected files:
  - sheet-transparent.png (main origin sprite)
  - animation.gif (single frame preview)
  - prompt-used.txt (prompt used for generation)
  - pipeline-meta.json (QC metadata)
```

## new Phase 2: Generate Individual Action Animations

After origin approval, use $generate2dsprite-action for each action independently.

### Phase 2.1: Idle Animation (6-8 frames)

```
Use $generate2dsprite-action to create an idle animation:
- character_name: "elder-samurai"
- action_type: "idle"
- target_frames: 8
- cell_ratio: "1:1"
- fill_margin: "normal"

Output location: output/elder-samurai/action/idle/
Expected files:
  - sheet-transparent.png (2x4 sprite sheet)
  - idle-1.png through idle-8.png (individual frames)
  - animation.gif (loopable idle loop)
  - prompt-used.txt (prompt used)
  - pipeline-meta.json (QC metadata)

Review checklist:
  ✓ Character maintains same silhouette as origin
  ✓ All 8 frames show consistent bounding-box size
  ✓ Aspect ratio drift is within tolerance (check pipeline-meta.json)
  ✓ No frames touch cell edges (edge_touch_frames in JSON)
  ✓ Animation loops smoothly
  ✓ Idle motion is subtle (breathing, weight shift, cloth movement)
```

### Phase 2.2: Walk Animation (6-8 frames)

```
Use $generate2dsprite-action to create a walk animation:
- character_name: "elder-samurai"
- action_type: "walk"
- target_frames: 8
- cell_ratio: "1:1"
- fill_margin: "normal"

Output location: output/elder-samurai/action/walk/
Expected files:
  - sheet-transparent.png (2x4 sprite sheet)
  - walk-1.png through walk-8.png (individual frames)
  - animation.gif (loopable walk cycle)
  - prompt-used.txt (prompt used)
  - pipeline-meta.json (QC metadata)

Review checklist:
  ✓ Character maintains same silhouette as origin
  ✓ Walk cycle is readable with clear foot positions
  ✓ All 8 frames show consistent bounding-box size
  ✓ Aspect ratio drift is within tolerance
  ✓ No frames touch cell edges
  ✓ Walk rhythm feels natural (contact → recoil → passing → repeat)
  ✓ Arms and legs swing in counter-balance
```

### Phase 2.3: Run Animation (6-8 frames)

```
Use $generate2dsprite-action to create a run animation:
- character_name: "elder-samurai"
- action_type: "run"
- target_frames: 8
- cell_ratio: "1:1"
- fill_margin: "normal"

Output location: output/elder-samurai/action/run/
Expected files:
  - sheet-transparent.png (2x4 sprite sheet)
  - run-1.png through run-8.png (individual frames)
  - animation.gif (loopable run cycle)
  - prompt-used.txt (prompt used)
  - pipeline-meta.json (QC metadata)

Review checklist:
  ✓ Character maintains same silhouette as origin
  ✓ Run is noticeably faster and more energetic than walk
  ✓ Forward lean is evident in push-off and airborne phases
  ✓ All 8 frames show consistent bounding-box size
  ✓ Aspect ratio drift is within tolerance
  ✓ No frames touch cell edges
  ✓ Run rhythm feels natural (push-off → airborne → landing → repeat)
```

### Phase 2.4: Jump Animation (6-8 frames)

```
Use $generate2dsprite-action to create a jump animation:
- character_name: "elder-samurai"
- action_type: "jump"
- target_frames: 8
- cell_ratio: "1:1"
- fill_margin: "normal"

Output location: output/elder-samurai/action/jump/
Expected files:
  - sheet-transparent.png (2x4 sprite sheet)
  - jump-1.png through jump-8.png (individual frames)
  - animation.gif (jump sequence preview)
  - prompt-used.txt (prompt used)
  - pipeline-meta.json (QC metadata)

Review checklist:
  ✓ Character maintains same silhouette as origin
  ✓ Jump sequence is complete: crouch → launch → apex → descent → landing
  ✓ Apex frame shows clear peak height
  ✓ Landing frame shows impact absorption (knees bent)
  ✓ All 8 frames show consistent bounding-box size
  ✓ Aspect ratio drift is within tolerance
  ✓ No frames touch cell edges
```