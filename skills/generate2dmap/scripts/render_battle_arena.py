from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw


PALETTE = {
    "bg": (18, 27, 32),
    "shadow": (33, 48, 52),
    "sand_a": (119, 103, 76),
    "sand_b": (141, 121, 90),
    "sand_c": (164, 143, 108),
    "stone_dark": (66, 74, 81),
    "stone_mid": (97, 106, 113),
    "stone_light": (136, 145, 150),
    "moss": (74, 104, 70),
    "accent": (190, 110, 76),
}


def clamp_box(x0: int, y0: int, x1: int, y1: int, width: int, height: int) -> tuple[int, int, int, int]:
    return max(0, x0), max(0, y0), min(width - 1, x1), min(height - 1, y1)


def draw_noise(img: Image.Image, rng: random.Random) -> None:
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            dx = (x - width / 2) / (width / 2)
            dy = (y - height / 2) / (height / 2)
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < 0.58:
                color = PALETTE["sand_b"]
                if (x + y) % 5 == 0:
                    color = PALETTE["sand_c"]
                elif (x * 2 + y) % 7 == 0:
                    color = PALETTE["sand_a"]
            else:
                color = PALETTE["shadow"]
                if (x + y) % 6 == 0:
                    color = PALETTE["stone_dark"]
            if rng.random() < 0.045:
                color = tuple(min(255, c + 8) for c in color)
            pixels[x, y] = color


def draw_ring(draw: ImageDraw.ImageDraw, cx: int, cy: int, rx: int, ry: int) -> None:
    draw.ellipse((cx - rx - 4, cy - ry - 4, cx + rx + 4, cy + ry + 4), fill=PALETTE["stone_dark"])
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=PALETTE["stone_mid"])
    draw.ellipse((cx - rx + 6, cy - ry + 6, cx + rx - 6, cy + ry - 6), fill=PALETTE["sand_b"])
    draw.ellipse((cx - rx + 18, cy - ry + 18, cx + rx - 18, cy + ry - 18), outline=PALETTE["stone_light"], width=2)


def draw_wall(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int) -> None:
    draw.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=PALETTE["stone_mid"])
    draw.rectangle((x0, y0, x1, y0 + 2), fill=PALETTE["stone_light"])
    draw.rectangle((x0, y1 - 2, x1, y1), fill=PALETTE["stone_dark"])


def draw_pillar(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int) -> None:
    half = size // 2
    draw.rectangle((cx - half - 2, cy - half + 2, cx + half + 2, cy + half + 4), fill=PALETTE["shadow"])
    draw.rectangle((cx - half, cy - half, cx + half, cy + half), fill=PALETTE["stone_mid"])
    draw.rectangle((cx - half, cy - half, cx + half, cy - half + 2), fill=PALETTE["stone_light"])
    draw.rectangle((cx - half, cy + half - 2, cx + half, cy + half), fill=PALETTE["stone_dark"])


def draw_cracks(draw: ImageDraw.ImageDraw, rng: random.Random, width: int, height: int) -> None:
    for _ in range(45):
        x = rng.randint(18, width - 18)
        y = rng.randint(18, height - 18)
        length = rng.randint(4, 9)
        points = [(x, y)]
        for _ in range(length):
            x += rng.choice((-2, -1, 1, 2))
            y += rng.choice((-2, -1, 1, 2))
            points.append((x, y))
        draw.line(points, fill=PALETTE["stone_dark"], width=1)


def draw_moss(draw: ImageDraw.ImageDraw, rng: random.Random, width: int, height: int) -> None:
    for _ in range(26):
        x = rng.randint(12, width - 32)
        y = rng.randint(12, height - 32)
        w = rng.randint(8, 18)
        h = rng.randint(5, 12)
        draw.ellipse((x, y, x + w, y + h), fill=PALETTE["moss"])


def render_arena(width: int, height: int, scale: int, seed: int) -> Image.Image:
    base = Image.new("RGB", (width, height), PALETTE["bg"])
    draw = ImageDraw.Draw(base)
    rng = random.Random(seed)

    draw_noise(base, rng)
    draw_wall(draw, 10, 8, width - 10, 18)
    draw_wall(draw, 10, height - 18, width - 10, height - 8)
    draw_wall(draw, 8, 18, 20, height - 18)
    draw_wall(draw, width - 20, 18, width - 8, height - 18)

    draw_ring(draw, width // 2, height // 2, 34, 20)

    for cx, cy in ((38, 28), (width - 38, 28), (38, height - 28), (width - 38, height - 28)):
        draw_pillar(draw, cx, cy, 10)

    draw.rectangle((width // 2 - 10, 0, width // 2 + 10, 13), fill=PALETTE["accent"])
    draw.rectangle((width // 2 - 10, height - 14, width // 2 + 10, height), fill=PALETTE["accent"])

    draw_moss(draw, rng, width, height)
    draw_cracks(draw, rng, width, height)

    for x in range(28, width - 28, 18):
        draw.rectangle((x, 24, x + 6, 27), fill=PALETTE["stone_light"])
        draw.rectangle((x, height - 28, x + 6, height - 25), fill=PALETTE["stone_light"])

    for y in range(30, height - 30, 18):
        draw.rectangle((24, y, 27, y + 6), fill=PALETTE["stone_light"])
        draw.rectangle((width - 28, y, width - 25, y + 6), fill=PALETTE["stone_light"])

    return base.resize((width * scale, height * scale), Image.Resampling.NEAREST)


def build_collision(export_width: int, export_height: int) -> dict:
    s = export_width / 160
    def px(value: float) -> int:
        return round(value * s)

    return {
        "mapSize": {"width": export_width, "height": export_height},
        "pipeline": {
            "visual_model": "baked_raster",
            "runtime_object_model": "none",
            "collision_model": "coarse_shapes",
            "engine_target": "raw_canvas",
        },
        "spawn": {"x": px(80), "y": px(66)},
        "walkBounds": [
            {"id": "arena-floor", "type": "rect", "x": px(22), "y": px(20), "w": px(116), "h": px(50)}
        ],
        "blockers": [
            {"id": "north-wall", "type": "rect", "x": px(10), "y": px(8), "w": px(140), "h": px(10)},
            {"id": "south-wall", "type": "rect", "x": px(10), "y": px(72), "w": px(140), "h": px(10)},
            {"id": "west-wall", "type": "rect", "x": px(8), "y": px(18), "w": px(12), "h": px(54)},
            {"id": "east-wall", "type": "rect", "x": px(140), "y": px(18), "w": px(12), "h": px(54)},
            {"id": "pillar-nw", "type": "rect", "x": px(33), "y": px(23), "w": px(10), "h": px(10)},
            {"id": "pillar-ne", "type": "rect", "x": px(117), "y": px(23), "w": px(10), "h": px(10)},
            {"id": "pillar-sw", "type": "rect", "x": px(33), "y": px(57), "w": px(10), "h": px(10)},
            {"id": "pillar-se", "type": "rect", "x": px(117), "y": px(57), "w": px(10), "h": px(10)},
            {"id": "center-ring", "type": "ellipse", "x": px(80), "y": px(45), "rx": px(18), "ry": px(11)},
        ],
        "notes": [
            "Openings at the top and bottom center can be used as entrances.",
            "Collision is intentionally coarse and independent from the painted pixels.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--collision", type=Path, required=True)
    parser.add_argument("--width", type=int, default=160)
    parser.add_argument("--height", type=int, default=90)
    parser.add_argument("--scale", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    image = render_arena(args.width, args.height, args.scale, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.collision.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)

    collision = build_collision(args.width * args.scale, args.height * args.scale)
    args.collision.write_text(json.dumps(collision, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
