# Map Guide

這份文件處理地圖流程前兩步：
- 第一步：生成 ground-only base map
- 第二步：基於 base map 生成 dressed reference

適用情境：
- 你要先做一張可走、可讀、方便後續加 props 的底圖。
- 你想先把地圖的可走區、主題和構圖定下來，再進入 dressed reference 或 props 階段。
- 你想沿用同一種 prompt 骨架，只替換地圖名稱和地圖特色。

## 輸出規則

第一步 base map 一律輸出到：

```text
output/map/{map_name}/
```

建議檔名：

```text
{map_name}-base.png
{map_name}-base.prompt.txt
```

例如：

```text
output/map/forest-clearing-brawler/
output/map/forest-clearing-brawler/forest-clearing-brawler-base.png
```

## 你只需要準備的輸入

最少只要填這兩類資訊：

- `map_name`：地圖名稱，建議用 kebab-case，例如 `forest-clearing-brawler`
- `map_features`：地圖特色，列出 3 到 7 個即可

可選但建議補充：

- `theme`：地圖主題，例如 forest clearing、ruined shrine approach、moonlit marsh
- `ground_surface`：主要地面材質，例如 packed earth、stone court、wooden deck
- `palette_mood`：例如 bright daylight、misty dusk、cool moonlight

## 第一階段空地圖 Prompt 樣板

把下面模板整段複製出去後，只替換 `<...>` 區塊即可。

```text
Ground-only side-view 2.5D pixel-art brawler base map for a <theme> battle stage.

Canvas:
- 1536x1024 pixels
- side-view 2.5D brawler perspective
- base ground map only
- no watermark, no labels, no UI

Output target:
- map name: <map_name>
- save outputs under output/map/<map_name>/
- main image filename: <map_name>-base.png
- if saving the prompt text, use <map_name>-base.prompt.txt

Scene goals:
- wide horizontal combat lane running across the map
- clear shallow depth band so characters can move left/right and slightly up/down on the ground plane
- <ground_surface> as the dominant surface
- readable <theme> mood without filling the playable lane with tall objects
- open center space for sprite readability and combat movement
- left and right ends shaped clearly enough to become future exits, blockers, or encounter boundaries
- ground perspective and value shifts should make the walkable lane easy to read at a glance
- boundaries and path shapes easy to trace for future collision and zone setup
- include these theme-defining features:
  - <map_feature_1>
  - <map_feature_2>
  - <map_feature_3>

Hard exclusions:
- no top-down RPG layout
- no platformer platforms
- no jumping gaps
- no stairs or vertical traversal
- no buildings unless explicitly requested
- no large blockers in the middle of the combat lane
- no tall collidable objects inside the main playable strip
- no NPCs
- no monsters
- no interactables
- no UI
- no text

Composition notes:
- keep the main walkable lane broad and visually continuous across most of the map width
- keep the middle 60 percent of the arena relatively clean and open
- push theme details toward the edges, far background, or upper/lower boundaries of the stage
- add subtle perspective to the ground plane so the depth lane reads clearly, but do not turn it into a top-down view
- reserve a few empty anchor areas near the far left, far right, and deep background edge for later prop placement
- keep contrast controlled so animated character sprites remain readable against the ground
- overall mood: <palette_mood>
```

## 填寫規則

- `theme` 寫主題名詞，不要寫太長句子，例如 `forest clearing`、`abandoned dock`、`shrine courtyard`
- `map_name` 直接對應輸出資料夾名稱，避免空白與中文
- `map_features` 只寫會影響畫面辨識的特色，不要把玩法需求和世界觀背景混在一起
- 如果你要的是空地圖，特色應該偏向地表、邊界、遠景、氛圍，而不是大量中央大物件

## 地圖特色該怎麼寫

好的特色：

- mossy ground edges
- shallow puddles near the lower boundary
- distant tree line with soft fog
- exposed roots and low brush near the sides
- scattered fallen leaves with low density

不好的特色：

- very cool map
- make it awesome
- a lot of details everywhere
- many objects in the center

## 套用範例

```text
map_name: forest-clearing-brawler
theme: forest clearing
ground_surface: packed earth with muted grass, moss, and light leaf scatter
palette_mood: soft daylight under tree cover
map_features:
- distant tree line with filtered light
- edge foliage and low brush near both sides
- exposed roots and moss near the upper boundary
- sparse fallen leaves and soft shadow breakup
```

把上面的值代回模板後，就能得到像目前這張 base prompt 那樣的第一步地圖提示詞。

## 快速填空版（只填名稱與特色）

如果你想最短輸入就能展開成第一步完整 prompt，直接用下面這段。

```text
請依 MAP-GUIDE 的第一階段模板展開完整 prompt。

map_name: <map_name>
theme: <theme>
map_features:
- <feature_1>
- <feature_2>
- <feature_3>
```

如果你暫時只想填最少欄位，下面這版也可以：

```text
請依 MAP-GUIDE 的第一階段模板展開完整 prompt。

map_name: <map_name>
map_features:
- <feature_1>
- <feature_2>
- <feature_3>
```

當 `theme` 沒填時，可把 `map_name` 轉成可讀主題，例如：
- `forest-clearing-brawler` -> `forest clearing`
- `ruined-dock-night` -> `ruined dock at night`

## 第二階段 Dressed Reference Guide

用途：在 base map 已確認後，先做一張「規劃用 dressed reference」，用來決定 props 密度、遮擋層次與視覺焦點。這張圖不是最終 runtime map。

### 第二步輸出規則

第二步 dressed reference 建議輸出到同一張地圖資料夾：

```text
output/map/{map_name}/
```

建議檔名：

```text
{map_name}-dressed-reference.png
{map_name}-dressed-reference.prompt.txt
```

### 第二步 Prompt 樣板

```text
Use the base map just shown as the visual layout reference.
Do not change camera, map size, ground shape, horizon structure, or stage boundaries.

Create a dressed planning reference image for a side-view 2.5D pixel-art brawler stage.

Input map:
- map name: <map_name>
- base map: output/map/<map_name>/<map_name>-base.png

Output target:
- save under output/map/<map_name>/
- output filename: <map_name>-dressed-reference.png
- if saving prompt text: <map_name>-dressed-reference.prompt.txt

What to add:
- add environmental set dressing that matches <theme>
- preserve a broad, readable central combat lane
- place most visual complexity near side edges, far background, and upper/lower boundaries
- include these designed accents:
  - <dressed_feature_1>
  - <dressed_feature_2>
  - <dressed_feature_3>

Gameplay readability constraints:
- keep the middle 50 to 60 percent of the arena mostly open for combat
- avoid dense clutter in the main playable strip
- avoid placing large blockers in the center lane
- maintain clear foreground/midground/background separation
- preserve silhouette readability for animated character sprites

Hard exclusions:
- no camera angle change
- no top-down conversion
- no platformer platforms
- no jumping-gap layout
- no UI
- no text
- no watermark

Reference intent:
- this is a planning/reference pass, not final runtime composition
- prioritize placement guidance and readability over decorative density
```

### 第二步快速填空版

```text
請依 MAP-GUIDE 的第二階段模板展開完整 prompt。

map_name: <map_name>
theme: <theme>
dressed_features:
- <feature_1>
- <feature_2>
- <feature_3>
```

## 建議工作流

1. 先用這份模板生成 base map。
2. 檢查可走區是否夠寬，中央是否乾淨，角色站上去是否清楚。
3. 用第二階段模板生成 dressed reference（同一 map_name 資料夾）。
4. 檢查遮擋關係、視覺密度與角色可讀性。
5. 最後再拆 props、collision、zones 或 preview。