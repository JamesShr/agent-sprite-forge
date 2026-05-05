# 互動物件批次生成清單模板（single 或 2x2）

用途：一次整理多個互動物件需求，逐項餵給生成流程，保持風格與規格一致。

建議命名規則：
- object-id 使用 kebab-case
- 路徑格式：`output/object/{object-id}/`

---

## A. 批次清單（先填這張）

| object-id | 類型 | idle 偵數 | sheet 模式 | 朝向策略 | 生態/場景 | 材質 | 主色 | 互動狀態描述 | 備註 |
|---|---|---|---|---|---|---|
| chest-wood | chest | 1 | single | left/up native, right/down mirrored | town | wood+iron | brown+gold | closed idle only | 一次性可開啟（開啟狀態可另做） |
| fence-wood | fence | 1 | single | left/up native, right/down mirrored | town | wood | brown | static fence segment | 可阻擋移動物件 |
| fence-wood-long | fence | 1 | single | left/up native, right/down mirrored | town | wood | brown | long straight fence segment | 可阻擋移動物件 |
| fence-wood-corner | fence | 1 | single | left/up native, right/down mirrored | town | wood | brown | L-shape corner fence segment | 可阻擋移動物件 |
| warp-circle | warp-circle | 4 | 2x2 | non-directional | shrine | stone+magic rune | cyan+blue | faint -> pulse -> peak -> settle | 站上去可傳送 |
| rock-mossy | rock | 1 | single | left/up native, right/down mirrored | forest | stone+moss | gray+green | idle static only | 主要作阻擋 |
| grass | grass | 4 | 2x2 | non-directional | field | living grass tufts | green+yellow-green | neutral -> sway-a -> sway-b -> neutral | 場景裝飾，可循環微動畫 |
| {object-id-4} | {type} | {1 or 4} | {single or 2x2} | {direction policy} | {biome} | {material} | {palette} | {state plan} | {notes} |

朝向策略說明：
- left/up native, right/down mirrored：只生成左與上，右與下由程式鏡像。
- non-directional：不分朝向（例如傳送陣、對稱水晶、地面符文）。

---

## B. 單物件提示詞模板（批次逐項替換）

```text
Create exactly one {SHEET_MODE} pixel-art sprite output for a 2.5D side-scrolling RPG interactive object.
SHEET_MODE is either single (1 frame) or 2x2 (4 frames).

Object identity:
- name: {OBJECT_ID}
- type: {OBJECT_TYPE}
- biome/style: {BIOME_STYLE}
- material: {MATERIAL}
- color accents: {COLOR_ACCENTS}

Direction policy:
- {DIRECTION_POLICY}
- if directional, draw LEFT-facing and UP-facing native variants only
- RIGHT-facing is horizontal mirror of LEFT-facing
- DOWN-facing is vertical mirror of UP-facing
- keep silhouette mirror-safe

View and style:
- 2.5D side-view object for a horizontal side-scrolling game
- viewed from a side-facing low-to-mid angle with roughly 45-degree upward tilt
- crisp dark pixel outlines
- consistent 16-bit RPG pixel-art style

Frame plan:
- if SHEET_MODE=single: one static idle frame
- if SHEET_MODE=2x2:
	- frame 1 (top-left): {FRAME_1}
	- frame 2 (top-right): {FRAME_2}
	- frame 3 (bottom-left): {FRAME_3}
	- frame 4 (bottom-right): {FRAME_4}

Consistency rules:
- same object identity across all frames
- same bounding box and same pixel scale in all frames
- entire object must fit fully inside each frame cell
- leave generous magenta margin on all sides
- keep at least 8% to 12% transparent magenta margin from the object silhouette to every cell edge
- no part may touch or cross any cell edge
- no detached particles outside the main silhouette unless explicitly requested
- avoid semi-transparent magenta fringe on object edges

Background and restrictions:
- background must be 100% solid flat #FF00FF magenta in every cell
- no gradients, no floor plane, no cast shadows
- no text, no labels, no UI, no watermark
- exactly one output matching SHEET_MODE, equal-size cells, no borders between cells
```

輸出路徑：

```text
output/object/{OBJECT_ID}/
```

---

## C. 批次輸入模板（可直接複製，連續生成）

把每一段 `{...}` 改完後，依序送出。

### 1) chest-wood

```text
Create exactly one single pixel-art sprite output for a 2.5D side-scrolling RPG interactive object.
Object identity: chest-wood, type chest, biome town, material wood and iron, color accents brown and gold.
Direction policy: left/up native, right/down mirrored.
Frame plan: one static closed idle frame.
Keep same identity, same scale, same bounding box.
Object fully inside frame with generous margin.
Background 100% solid #FF00FF magenta.
No text, no UI, no watermark, no edge crossing.
```

輸出到：`output/object/chest-wood/`

### 2) warp-circle

```text
Create exactly one 2x2 pixel-art sprite sheet for a 2.5D side-scrolling RPG interactive object.
Object identity: warp-circle, type warp-circle, biome shrine, material ancient stone and runes, color accents cyan and blue.
Direction policy: non-directional radial object.
Frame plan: faint rune glow; brighter pulse; peak energy ring; settle loop glow.
Keep same identity, same scale, same bounding box in all frames.
Object fully inside each cell with generous margin.
Background 100% solid #FF00FF magenta.
No text, no UI, no watermark, no edge crossing.
```

輸出到：`output/object/warp-circle/`

### 3) rock-mossy

```text
Create exactly one single pixel-art sprite output for a 2.5D side-scrolling RPG interactive object.
Object identity: rock-mossy, type rock, biome forest, material stone with moss, color accents gray and green.
Direction policy: left/up native, right/down mirrored.
Frame plan: one static idle frame.
Keep same identity, same scale, same bounding box.
Object fully inside frame with generous margin.
Background 100% solid #FF00FF magenta.
No text, no UI, no watermark, no edge crossing.
```

輸出到：`output/object/rock-mossy/`

### 4) fence-wood

```text
Create exactly one single pixel-art sprite output for a 2.5D side-scrolling RPG interactive object.
Object identity: fence-wood, type fence, biome town, material aged wood planks and posts, color accents brown and dark-brown.
Direction policy: left/up native, right/down mirrored.
Frame plan: one static idle frame.
View: side-view fence segment at roughly 45-degree upward tilt, readable as a movement blocker.
Keep same identity, same scale, same bounding box.
Keep at least 8% to 12% magenta margin from silhouette to each edge.
Object fully inside frame with generous margin.
Background 100% solid #FF00FF magenta.
No text, no UI, no watermark, no edge crossing.
```

輸出到：`output/object/fence-wood/`

### 5) grass

```text
Create exactly one 2x2 pixel-art sprite sheet for a 2.5D side-scrolling RPG interactive object.
Object identity: grass, type grass, biome field, material living grass tufts, color accents green and yellow-green.
Direction policy: non-directional organic object.
Frame plan: neutral idle grass pose; slight sway; strongest sway; return toward neutral for seamless loop.
Keep same identity, same scale, same bounding box in all frames.
Object fully inside each cell with generous margin.
Background 100% solid #FF00FF magenta.
No text, no UI, no watermark, no edge crossing.
```

輸出到：`output/object/grass/`

---

## D. 批次完成後驗收清單

- 每個物件都有獨立資料夾：`output/object/{object-id}/`
- single 物件必須為 1 張，2x2 物件必須為 4 張，且無跨格、無裁切
- 背景皆為純 #FF00FF
- 無文字、無 UI、無 watermark
- 同物件所有偵保持同一身份與一致比例
- directional 物件確認 LEFT/UP 原生圖可安全鏡像成 RIGHT/DOWN
- 互動狀態可被遊戲邏輯直接對應（如 closed/open/active）

---

## E. 地圖物件分類與碰撞欄位模板

建議每個物件都加上這 3 個核心邏輯欄位：
- `isBlocking`：是否阻擋移動
- `isInteractable`：是否可互動
- `triggerType`：互動類型（warp | loot | dialogue | breakable | none）

### 分類範例表

| object-id | isBlocking | isInteractable | triggerType | 備註 |
|---|---|---|---|---|
| rock-mossy | true | false | none | 純阻擋物件 |
| fence-wood | true | false | none | 純阻擋物件 |
| fence-wood-long | true | false | none | 純阻擋物件 |
| fence-wood-corner | true | false | none | 純阻擋物件 |
| chest-wood | true | true | loot | 可互動開箱 |
| warp-circle | false | true | warp | 進入觸發傳送 |
| grass | false | false | none | 純裝飾，不阻擋 |

### 物件定義模板（建議共用 registry）

```json
{
	"objects": [
		{
			"id": "rock-mossy",
			"image": "output/object/rock-mossy/processed/object.png",
			"sheetMode": "single",
			"idleFrames": 1,
			"isBlocking": true,
			"isInteractable": false,
			"triggerType": "none"
		},
		{
			"id": "warp-circle",
			"image": "output/object/warp-circle/processed/sheet.png",
			"sheetMode": "2x2",
			"idleFrames": 4,
			"isBlocking": false,
			"isInteractable": true,
			"triggerType": "warp"
		}
	]
}
```

### 地圖擺放模板（每張地圖一份）

```json
{
	"placements": [
		{
			"instanceId": "rock-mossy-01",
			"objectId": "rock-mossy",
			"x": 420,
			"y": 520,
			"w": 96,
			"h": 72,
			"sortY": 520,
			"collision": {
				"type": "ellipse",
				"x": 420,
				"y": 520,
				"rx": 30,
				"ry": 14
			}
		},
		{
			"instanceId": "warp-circle-01",
			"objectId": "warp-circle",
			"x": 860,
			"y": 488,
			"w": 120,
			"h": 120,
			"sortY": 488,
			"trigger": {
				"type": "circle",
				"x": 860,
				"y": 488,
				"radius": 26,
				"onEnter": {
					"triggerType": "warp",
					"targetMap": "forest-02",
					"targetSpawn": "south-gate"
				}
			}
		}
	]
}
```

### 實作建議

- 生成階段：維持單物件單檔生成（品質穩定，易重做）
- 執行階段：再打包成 atlas/spritesheet（減少載入與 draw call）
- 碰撞請用 footprint（底部碰撞區）而非整張 PNG 外框
