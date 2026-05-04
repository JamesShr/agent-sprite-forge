## Phase 1 Origin（1x1 靜態原始圖）

```
Character concept: [你的角色描述放這裡]

Create a single 2D pixel-art character sprite.
No animation, no grid, just one static portrait.

Camera and facing style:
Near-frontal 3/4 front view. Not a full side profile.
South-southeast facing (SSE): character is mostly front-facing with a subtle yaw bias toward screen-right.
Yaw around 15 to 25 degrees from frontal, never beyond 30 degrees.
Both eyes must remain clearly visible. The far eye can be slightly narrower.

Pose:
Neutral standing idle, weight settled, at rest.
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

## Phase 2 Idle（6~8 偵，follow Origin）

```
Use the image just shown as the visual reference. This is the established character origin.

Preserve ALL of the following from the reference exactly:
same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE near-frontal facing direction (15 to 25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art idle sprite sheet with 6 to 8 frames.
Preferred layout: 2x3 (6 frames) or 2x4 (8 frames).
No borders, no separators, no labels, no text anywhere.

Frame intent (in order):
1. neutral stance, weight settled
2. subtle inhale
3. slight cloth or hair motion
4. gentle exhale and micro weight shift
5. secondary idle accent
6. return toward neutral loop state
7-8 (if 8 frames): smoother in-between transitions for loop quality

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

## Phase 3 Walk（6~8 偵，follow Origin）

```
Use the image just shown as the visual reference. This is the established character origin.

Preserve ALL of the following from the reference exactly:
same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE near-frontal facing direction (15 to 25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art walk sprite sheet with 6 to 8 frames.
Preferred layout: 2x3 (6 frames) or 2x4 (8 frames).
No borders, no separators, no labels, no text anywhere.

Frame intent (in order):
1. contact pose A (right foot forward)
2. recoil/weight transfer
3. passing pose
4. contact pose B (left foot forward)
5. recoil/weight transfer
6. passing pose
7-8 (if 8 frames): smoother in-between contact and passing poses

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

## Phase 4 Run（6~8 偵，follow Origin）

```
Use the image just shown as the visual reference. This is the established character origin.

Preserve ALL of the following from the reference exactly:
same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE near-frontal facing direction (15 to 25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art run sprite sheet with 6 to 8 frames.
Preferred layout: 2x3 (6 frames) or 2x4 (8 frames).
No borders, no separators, no labels, no text anywhere.

Frame intent (in order):
1. push-off A with stronger forward lean
2. airborne extension
3. landing A with impact absorption
4. push-off B
5. airborne extension
6. landing B with impact absorption
7-8 (if 8 frames): smoother in-between for high-speed loop readability

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

## Phase 5 Jump（6~8 偵，follow Origin）

```
Use the image just shown as the visual reference. This is the established character origin.

Preserve ALL of the following from the reference exactly:
same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same SSE near-frontal facing direction (15 to 25 degree yaw toward screen-right, both eyes visible).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art jump sprite sheet with 6 to 8 frames.
Preferred layout: 2x3 (6 frames) or 2x4 (8 frames).
No borders, no separators, no labels, no text anywhere.

Frame intent (in order):
1. crouch wind-up
2. deeper compression and launch prep
3. takeoff extension
4. apex hold
5. descent
6. landing absorption and recovery
7-8 (if 8 frames): smoother launch and landing in-betweens

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

## new phase1  Generate Origin Sprite

Use $generate2dsprite-origin with the following parameters:

character_name: kebab-case identifier (e.g., elder-samurai, fire-wizard)
character_concept: Brief description of the character (silhouette, costume, key features, expression)
facing_direction: sse (south-southeast, default) | nne (north-northeast) | frontal
output_base_path: Optional override (default: output)

```
Use $generate2dsprite-origin to create a character origin sprite:
- character_name: "elder-samurai"
- character_concept: "elderly samurai with stern expression, white beard, white kimono, holding wooden staff"
- facing_direction: "sse"

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