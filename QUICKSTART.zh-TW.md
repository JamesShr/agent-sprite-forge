# Agent Sprite Forge Quick Start

這份文件是給想要快速上手的人用的。

目標很簡單：

1. 你提供角色圖片。
2. 你提供角色名稱。
3. 用 `$generate2dsprite` 做出角色 sprite。
4. 用 `$generate2dmap` 做出可放進遊戲的地圖。

如果你不想先讀完整份 [README.zh-TW.md](./README.zh-TW.md)，直接照這份做就夠了。

## 先理解兩件事

### 1. 這個 repo 有兩個 skill

- `$generate2dsprite`：把角色圖或角色描述做成 sprite、動畫 sheet、透明 PNG、GIF。
- `$generate2dmap`：把地圖需求做成可玩的 2D map，必要時會拆出透明 props、collision、zones、preview。

### 2. 參考圖一定要先出現在對話上下文

如果你要「照這張角色圖做 sprite」或「讓地圖風格配合這個角色」，重點不是把檔案路徑寫進 prompt，而是先讓圖片真的出現在對話裡。

最穩的做法：

- 直接把角色圖片拖進聊天視窗。
- 如果圖片是 local file，先把圖片打開或顯示到對話上下文，再要求 skill 使用它當 reference。

不要只寫「請參考 `C:\somewhere\hero.png`」。這通常不夠。

## 安裝

如果你還沒裝本地後處理依賴，先做一次。

### Windows PowerShell

```powershell
git clone https://github.com/0x0funky/agent-sprite-forge.git
cd .\agent-sprite-forge
python -m pip install -r .\requirements.txt
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force `
  ".\skills\*" `
  "$env:USERPROFILE\.codex\skills\"
```

安裝後建議重開一個新的 Codex session，讓 skill 重新載入。

## 最短流程

### 流程 A：只有角色圖片和角色名稱，先做角色 sprite

你需要準備：

- 1 張角色參考圖
- 1 個角色名稱
- 想要的用途：站立、走路、攻擊、施法、受傷、投射物、爆炸

最短操作順序：

1. 把角色圖片貼到聊天裡。
2. 告訴 agent 角色名稱。
3. 指定要做哪種 sprite。
4. 讓 `$generate2dsprite` 自己推斷 sheet 類型。

直接可用的 prompt：

```text
Use $generate2dsprite to create a top-down 4x4 player_sheet for the character in the image just shown.
Character name: Akiro.
Keep the same identity, silhouette, palette, face, outfit, and accessories.
Make a four-direction walk sprite sheet with 4 frames per direction.
Row order: down, left, right, up.
Same character, same proportions, same pixel scale in every frame.
Solid #FF00FF background.
Each frame must fit fully inside its cell, with clear margin on all sides.
Retro JRPG pixel-art style.
```

這個 prompt 適合：

- 主角
- NPC
- top-down RPG 角色
- 要四方向行走 sheet 的情境

### 流程 B：用同一張角色圖快速做戰鬥或技能動畫

如果你要的是攻擊、施法、投射物、爆炸，不要先自己糾結 sheet 尺寸；直接讓 `$generate2dsprite` 按資產類型決定。

#### 攻擊動畫

```text
Use $generate2dsprite to create an attack animation for the character in the image just shown.
Character name: Akiro.
Keep the same identity, silhouette, palette, face, outfit, and weapon design.
Create a side-view pixel-art attack sheet.
Show a clear wind-up, strike, follow-through, and recovery.
Same character, same scale, same bounding box across frames.
Solid #FF00FF background.
Nothing may cross any cell edge.
```

#### 施法 + 飛行物 + 命中爆發

```text
Use $generate2dsprite to create a spell bundle for the character in the image just shown.
Character name: Akiro.
Keep the same identity, costume language, and weapon or casting style.
Create a cast animation, a projectile loop, and an impact burst in matching pixel-art style.
Use solid #FF00FF background for all raw sheets.
Keep every asset fully contained inside its cells.
```

這種情況下，skill 通常會自動拆成：

- cast
- projectile
- impact

也就是一組 `spell_bundle`。

### 流程 C：先做地圖，再把角色放進去

如果你想快速得到「角色可站上去的地圖」，建議從最輕量的地圖需求開始。

#### 你只要一張簡單可玩的地圖

```text
Use $generate2dmap to create a small fixed-screen pixel-art battle arena for the character named Akiro.
The map should match the visual style of the character image just shown.
Add simple collision only.
No UI, no text.
```

這會偏向：

- `baked_raster`
- `coarse_shapes`

適合：

- 戰鬥背景
- 單畫面 arena
- 先做 prototype

#### 你要的是 RPG 探索地圖

```text
Use $generate2dmap to create a top-down RPG shrine map for the character named Akiro.
Match the world style to the character image just shown.
Use a layered raster pipeline.
Add y-sorted props, precise collision, a rest point, and trigger zones.
The player must be able to walk in front of and behind tall props.
Create a flattened preview too.
```

這會偏向：

- `layered_raster`
- `y_sorted_props`
- `precise_shapes`
- `trigger_zones`

適合：

- 村莊
- 神社
- 野外場景
- 怪物養成 RPG 地圖

## 真正最快的實戰組合

如果你的需求是「我只有角色圖和角色名字，想快點得到角色 sprite 和一張能用的地圖」，直接照下面兩段丟給 agent 就好。

### Step 1: 先做角色四方向走路 sheet

```text
Use $generate2dsprite to create a top-down 4x4 player_sheet for the character in the image just shown.
Character name: fong-yi.
Keep the same identity, silhouette, palette, face, hair, outfit, and accessories.
Make a four-direction walk sprite sheet with 4 frames per direction.
Row order: down, left, right, up.
Same character, same proportions, same pixel scale in every frame.
Solid #FF00FF background.
Each frame must fit fully inside its cell, with clear margin on all sides.
Retro JRPG pixel-art style.
```

### Step 2: 再做一張角色專屬地圖

```text
Use $generate2dmap to create a top-down RPG starter area for the character named Akiro.
Match the world style to the character image just shown.
Use a layered raster pipeline.
Create a ground-only base map first, then generate props and a flattened preview.
Add y-sorted props, precise collision, one rest point, one entrance, and one encounter zone.
Keep the scene small and practical for a playable prototype.
```

這樣通常就能得到：

- 可用的角色 walk sheet
- 可用的地圖 base
- props placement
- collision / zones metadata
- preview 圖

## 什麼時候用哪個 sprite 模式

如果你不想自己猜，可以直接描述需求。但如果你想快一點，下面這張對照表夠用。

| 需求 | 建議模式 |
| --- | --- |
| 主角四方向行走 | `4x4 player_sheet` |
| 一般待機 | `2x2 idle` |
| 大型 Boss 待機 | `3x3 idle` |
| 施法 | `2x3 cast` |
| 投射物 | `1x4 projectile` |
| 爆炸 / 命中 | `2x2 impact` |
| 一整套法術 | `spell_bundle` |

## 什麼時候用哪種地圖

| 需求 | 建議 pipeline |
| --- | --- |
| 單畫面戰鬥場景 | `baked_raster + coarse_shapes` |
| RPG 探索地圖 | `layered_raster + y_sorted_props + precise_shapes` |
| 側視卷軸場景 | `parallax_layers` |
| 已經有 tilemap 編輯器流程 | `tilemap` 或 `layered_tilemap` |

如果你只是要「快點出一張可玩的 top-down 地圖」，直接選：

```text
layered_raster + y_sorted_props + precise_shapes + trigger_zones
```

## 角色圖片驅動的推薦 prompt 寫法

只要是 reference-driven 的生成，建議都沿用這個骨架。

```text
Use the image just shown as the visual reference.
Character name: <NAME>.
Keep the same silhouette, palette, face, outfit, accessories, and material language.
Only change the requested action, animation phase, or map/world context.
Keep the same pixel-art identity.
```

如果是 sprite，再補：

```text
Solid #FF00FF background.
Exact sheet shape only.
Same scale and bounding box across frames.
Nothing may cross any cell edge.
```

如果是地圖，再補：

```text
Match the world style to the character reference.
Keep the map practical for gameplay.
Add collision and zones only when needed.
```

## 你會拿到什麼輸出

### `$generate2dsprite` 常見輸出

- `raw-sheet.png`
- `raw-sheet-clean.png`
- `sheet-transparent.png`
- frame PNGs
- `animation.gif`
- `prompt-used.txt`
- `pipeline-meta.json`

如果是 `player_sheet`，通常還會有：

- 四個方向的 strip
- 四個方向的 GIF

### `$generate2dmap` 常見輸出

如果是 baked map，通常會有：

- 地圖 PNG
- prompt file
- collision JSON 或 zones JSON

如果是 layered raster map，通常會有：

- base map
- dressed reference
- props folders 或 prop pack extraction manifest
- props placement JSON
- collision JSON
- zones JSON
- layered preview

## 常見錯誤

### 1. 只給角色名，不給圖片，也不描述特徵

這樣可以生成，但不會長得像你心裡那個角色。

最少要給其中一種：

- 角色圖片
- 清楚的角色外觀描述

### 2. 把本機檔案路徑直接寫進 prompt

不穩。圖片要先出現在對話上下文。

### 3. 要角色行走 sheet，卻沒指定四方向

如果你想拿去做 top-down RPG，最好明確寫：

```text
Make a four-direction walk sprite sheet with 4 frames per direction.
Row order: down, left, right, up.
```

### 4. 要地圖，但沒說是戰鬥場景還是探索場景

這會直接影響 pipeline。

- 戰鬥圖：偏 baked
- 探索圖：偏 layered

### 5. 想把 tall props 做進 base map

如果角色要能走到物件前後，請不要把樹、門、燈籠、招牌這類 tall props 全烤進 base map。
應該用 layered raster 流程拆成透明 props。

## 建議你直接複製的兩組模板

### 模板 1：角色圖 -> RPG 主角 sprite

```text
Use $generate2dsprite to create a top-down 4x4 player_sheet for the character in the image just shown.
Character name: <NAME>.
Keep the same identity, silhouette, palette, face, hair, outfit, and accessories.
Make a four-direction walk sprite sheet with 4 frames per direction.
Row order: down, left, right, up.
Same character, same proportions, same pixel scale in every frame.
Solid #FF00FF background.
Each frame must fit fully inside its cell, with clear margin on all sides.
Retro JRPG pixel-art style.
```

### 模板 2：角色圖 -> 專屬 RPG 地圖

```text
Use $generate2dmap to create a top-down RPG map for the character named <NAME>.
Match the world style to the character image just shown.
Use a layered raster pipeline.
Create a ground-only base map first, then generate props and a flattened preview.
Add y-sorted props, precise collision, one spawn point, one entrance, and one trigger zone.
Keep the scene compact and practical for a playable prototype.
```

## 最後的建議

如果你是第一次用，先不要一口氣要求完整遊戲。

最快成功順序是：

1. 先用角色圖做 `4x4 player_sheet`。
2. 再做一張小型 `layered_raster` RPG 地圖。
3. 確認角色比例和地圖視角搭得上。
4. 最後才補 attack、cast、projectile、impact 這些戰鬥資產。

這樣最容易在短時間內拿到第一個能跑的 prototype。