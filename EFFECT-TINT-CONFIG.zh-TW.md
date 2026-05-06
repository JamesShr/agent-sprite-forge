# Phaser 攻擊特效配色與範圍參數化設定指南

本文件說明如何把灰白基底特效（例如 `output/effect/vertical-arc-slash`）做成可調參數，讓遊戲在執行時可依屬性、方向、範圍大小動態調整。

## 目標

- 同一張灰白特效圖，支援多種屬性配色（火、冰、雷等）
- 不重做素材即可調整特效範圍大小
- 可依角色面向方向掛載（偏移、角度）
- 使用資料設定檔（JSON）讓企劃/美術可直接微調

## 建議參數結構

建議拆成 4 個區塊：

1. `effects`
2. `elements`
3. `mounts`
4. `ranges`

### 1) effects（特效本體）

- `textureKey`: Phaser 資源 key
- `animKey`: Phaser 動畫 key
- `baseScale`: 預設縮放
- `defaultAlpha`: 預設透明度
- `defaultBlendMode`: 預設混色模式
- `rangeProfile`: 套用哪一組範圍大小設定

### 2) elements（屬性配色）

- `tint`: 套色顏色（十六進位）
- `alpha`: 屬性專屬透明度
- `blendMode`: 屬性專屬混色模式

### 3) mounts（掛載方向）

- `ox`, `oy`: 特效相對角色偏移
- `angle`: 特效旋轉角度
- `flipX`: 是否水平翻轉

### 4) ranges（範圍大小）

- `scale`: 視覺範圍倍率（控制 sprite 大小）
- `hitRadius`: 命中半徑（若你有碰撞/判定系統）
- `length`: 前伸長度（刺擊、弧形可用）
- `durationMs`: 持續時間（可選）

## JSON 範例

```json
{
  "effects": {
    "verticalArcSlash": {
      "textureKey": "fx-vertical-arc-slash",
      "animKey": "fx-vertical-arc-slash-play",
      "baseScale": 1.0,
      "defaultAlpha": 0.95,
      "defaultBlendMode": "ADD",
      "rangeProfile": "melee_medium"
    }
  },
  "elements": {
    "neutral": { "tint": "#FFFFFF", "alpha": 0.95, "blendMode": "ADD" },
    "fire":    { "tint": "#FF5A2A", "alpha": 0.95, "blendMode": "ADD" },
    "ice":     { "tint": "#63D8FF", "alpha": 0.90, "blendMode": "ADD" },
    "thunder": { "tint": "#FFD84A", "alpha": 0.95, "blendMode": "ADD" },
    "poison":  { "tint": "#8DFF66", "alpha": 0.90, "blendMode": "ADD" },
    "dark":    { "tint": "#8F6BFF", "alpha": 0.92, "blendMode": "ADD" }
  },
  "mounts": {
    "down":      { "ox": 0,   "oy": 12,  "angle": 0,    "flipX": false },
    "up":        { "ox": 0,   "oy": -14, "angle": 180,  "flipX": false },
    "left":      { "ox": -14, "oy": 2,   "angle": -90,  "flipX": false },
    "right":     { "ox": 14,  "oy": 2,   "angle": 90,   "flipX": false },
    "downLeft":  { "ox": -10, "oy": 10,  "angle": -35,  "flipX": false },
    "downRight": { "ox": 10,  "oy": 10,  "angle": 35,   "flipX": false },
    "upLeft":    { "ox": -10, "oy": -10, "angle": -145, "flipX": false },
    "upRight":   { "ox": 10,  "oy": -10, "angle": 145,  "flipX": false }
  },
  "ranges": {
    "melee_small": {
      "scale": 0.85,
      "hitRadius": 28,
      "length": 34,
      "durationMs": 120
    },
    "melee_medium": {
      "scale": 1.00,
      "hitRadius": 36,
      "length": 44,
      "durationMs": 140
    },
    "melee_large": {
      "scale": 1.20,
      "hitRadius": 46,
      "length": 56,
      "durationMs": 170
    }
  }
}
```

## Phaser 使用方式（簡化版）

```ts
function playAttackEffect(scene, attacker, config, opts) {
  const fxDef = config.effects[opts.effectId];
  const ele = config.elements[opts.element] || config.elements.neutral;
  const mount = config.mounts[opts.facing] || config.mounts.down;
  const range = config.ranges[opts.rangeKey || fxDef.rangeProfile];

  const fx = scene.add.sprite(
    attacker.x + mount.ox,
    attacker.y + mount.oy,
    fxDef.textureKey,
    0
  );

  // 屬性配色
  fx.setTint(Phaser.Display.Color.HexStringToColor(ele.tint).color);
  fx.setAlpha(ele.alpha ?? fxDef.defaultAlpha);
  fx.setBlendMode(Phaser.BlendModes[ele.blendMode] ?? Phaser.BlendModes.ADD);

  // 方向與範圍
  fx.setAngle(mount.angle);
  fx.setFlipX(!!mount.flipX);
  fx.setScale((fxDef.baseScale ?? 1) * (range?.scale ?? 1));

  fx.play(fxDef.animKey);
  fx.once(Phaser.Animations.Events.ANIMATION_COMPLETE, () => fx.destroy());

  // 若有判定系統，可使用 range.hitRadius / range.length 做命中範圍
  return { fx, hitRadius: range?.hitRadius, length: range?.length };
}
```

## 調參建議

- 先固定 `mounts`，再調 `ranges.scale`，避免視覺位置飄移
- 近戰短武器先用 `melee_small`，大劍或重擊改 `melee_large`
- 若特效過亮：降低 `elements.*.alpha` 或改 `blendMode` 為 `NORMAL`
- 若特效範圍看起來正確但命中不合理，只調 `hitRadius/length`，不要先動 sprite

## 最小落地流程

1. 生成灰白基底特效（你目前已完成）
2. 建立 JSON 設定檔
3. 實作統一播放函式讀取 JSON
4. 戰鬥系統呼叫時傳入 `effectId + element + facing + rangeKey`
5. 進遊戲逐項微調 `elements` 與 `ranges`
