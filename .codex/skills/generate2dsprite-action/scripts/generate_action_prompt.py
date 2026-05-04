#!/usr/bin/env python3
"""Generate templated action prompts for sprite animations."""

from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"


@dataclass
class ActionPromptConfig:
    action_type: ActionType
    target_frames: int = 8
    character_name: str = "character"
    facing_direction: str = "sse"  # sse, nne, frontal


# Frame descriptions for each action at different frame counts
ACTION_FRAMES = {
    ActionType.IDLE: {
        6: [
            "neutral stance, weight settled",
            "subtle inhale",
            "slight hair or robe cloth motion",
            "gentle exhale and micro weight shift",
            "secondary idle accent",
            "return toward neutral loop state",
        ],
        8: [
            "neutral stance, weight settled",
            "subtle inhale",
            "slight cloth or hair motion",
            "gentle exhale",
            "weight shift",
            "secondary accent",
            "subtle return",
            "loop preparation",
        ],
    },
    ActionType.WALK: {
        6: [
            "contact pose A (right foot forward)",
            "recoil and weight transfer",
            "passing pose mid-stride",
            "contact pose B (left foot forward)",
            "recoil and weight transfer",
            "passing pose mid-stride",
        ],
        8: [
            "contact pose A (right foot forward)",
            "recoil A",
            "passing pose",
            "mid-stride balanced",
            "contact pose B (left foot forward)",
            "recoil B",
            "passing pose",
            "return to contact",
        ],
    },
    ActionType.RUN: {
        6: [
            "push-off A with strong forward lean",
            "airborne extension and momentum",
            "landing A with impact absorption",
            "push-off B with strong forward lean",
            "airborne extension and momentum",
            "landing B with impact absorption",
        ],
        8: [
            "push-off A with forward lean",
            "airborne A",
            "landing A with impact",
            "recovery stride",
            "push-off B with forward lean",
            "airborne B",
            "landing B with impact",
            "recovery stride",
        ],
    },
    ActionType.JUMP: {
        6: [
            "crouch wind-up, knees bent",
            "deeper compression and launch prep",
            "takeoff extension, rising from ground",
            "apex hold, peak of jump",
            "descent, falling",
            "landing absorption and recovery",
        ],
        8: [
            "crouch wind-up",
            "deeper compress",
            "launch extension",
            "apex hold",
            "early descent",
            "descent",
            "landing impact",
            "recovery",
        ],
    },
}


def get_grid_layout(frame_count: int) -> tuple[int, int]:
    """Return (rows, cols) for grid layout."""
    if frame_count <= 6:
        return (2, 3)
    else:
        return (2, 4)


def get_facing_description(facing: str) -> str:
    """Return facing direction description for prompt."""
    if facing.lower() == "sse":
        return "South-southeast facing (SSE): character is mostly front-facing with a subtle yaw bias toward screen-right. Yaw around 15 to 25 degrees from frontal, never beyond 30 degrees. Both eyes must remain clearly visible."
    elif facing.lower() == "nne":
        return "North-northeast facing (NNE): character is mostly front-facing with a subtle yaw bias toward screen-left. Yaw around 15 to 25 degrees from frontal, never beyond 30 degrees. Both eyes must remain clearly visible."
    else:
        return "Frontal facing: character faces straight toward the camera with minimal angle, both eyes fully visible."


def generate_action_prompt(config: ActionPromptConfig) -> str:
    """Generate a templated action prompt."""
    
    action = config.action_type.value
    frame_count = config.target_frames
    
    if frame_count not in ACTION_FRAMES[config.action_type]:
        raise ValueError(f"Unsupported frame count {frame_count} for {action}")
    
    frame_descs = ACTION_FRAMES[config.action_type][frame_count]
    rows, cols = get_grid_layout(frame_count)
    facing_desc = get_facing_description(config.facing_direction)
    
    frame_list = "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(frame_descs)])
    
    prompt = f"""Use the image just shown as the visual reference (origin sprite).

Preserve exactly: same silhouette family, same bounding-box proportions, same palette,
same face and eye style, same costume and accessories, same material rendering.
Same {config.facing_direction.upper()} facing direction ({facing_desc}).
Do not redesign the character. Do not change facing angle.

Create a 2D pixel-art {action} sprite sheet with exactly {frame_count} equal cells in a {rows}x{cols} grid.
No borders, no separators, no labels, no text anywhere.

Frame intent (in reading order):
{frame_list}

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
Crisp, gameplay-readable pixel art suitable for RPG sprite animation."""
    
    return prompt


if __name__ == "__main__":
    # Example usage
    config = ActionPromptConfig(
        action_type=ActionType.IDLE,
        target_frames=8,
        character_name="elder-samurai",
        facing_direction="sse"
    )
    
    prompt = generate_action_prompt(config)
    print(prompt)
