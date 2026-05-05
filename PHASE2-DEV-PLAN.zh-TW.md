# Phase 2：地圖物件、傳送系統、角色腳下效果

## 整體架構

### 系統互動流程

```
MainScene.update()
├─ 更新角色位置（WASD 輸入）
├─ 同步角色腳下 effect 位置與深度
├─ 檢測角色與 map colliders 碰撞
│  └─ 若碰撞，角色停止移動（走不動）
├─ 檢測角色進入 trigger zones（傳送門）
│  └─ 若進入，觸發 warp 到下一張地圖
└─ 若地圖切換，重新載入新地圖與物件佈置
```

---

## 需求分解

### Phase 2 範圍鎖定（本階段必做）

1. 地圖物件擺放與碰撞：不可穿透物件必須限制角色行動範圍。
2. 邊界傳送：角色碰到邊界傳送門後，切到下一張地圖的鏡像邊界，且落點需在傳送門前方一小段，避免立即回傳。
3. 腳下效果：角色預設使用 shadow，並可切換成 aura（例如 `aura-tidal-ripple`）。

本階段先不納入打擊特效（hit effect）驗收，打擊特效移至後續擴充。

### 1. 地圖物件掛載與碰撞（Blocking Objects）

**目標：** 角色無法穿過 rock、fence 等可阻擋物件

**實作步驟：**

1. 在地圖檔（例如 `data/shrine-props.json`）中標記 `isBlocking: true` 的物件
2. 在 preload 時載入所有物件圖片
3. 在 create 時根據 placement JSON 逐個產生 sprite：
   - 位置（x, y）
   - 尺寸（w, h）
   - 碰撞 footprint（底部橢圓或矩形）
4. 將碰撞 footprint 加入 physics group，設為 immovable
5. 角色與該 group 啟用 collide

**資料結構參考：**

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
      "isBlocking": true,
      "collision": {
        "type": "ellipse",
        "x": 420,
        "y": 520,
        "rx": 30,
        "ry": 14
      }
    }
  ]
}
```

**代碼參考框架：**

```js
// MainScene.create()
this.mapColliders = this.physics.add.staticGroup();
const placements = mapData.placements;
placements.forEach(p => {
  if (p.isBlocking && p.collision) {
    const blocker = this.add.zone(
      p.collision.x,
      p.collision.y,
      p.collision.rx * 2,
      p.collision.ry * 2
    );
    this.physics.add.existing(blocker, true);
    this.mapColliders.add(blocker);
  }
});

// 角色與地圖碰撞
this.physics.add.collider(this.player, this.mapColliders);
```

---

### 2. 傳送系統（Warp Triggers）

**目標：** 角色踩到傳送門 → 傳送到下一張地圖的鏡像邊界，且落在傳送門前方安全位置（避免無限回傳）

**座標對應規則：**

- 角色在當前地圖 `(x, y)` 處進入 warp trigger
- warp trigger 指向 targetMap 與 targetSpawn
- 在 targetMap 中尋找同名 spawn point，取其位置
- 角色在 targetMap 中出現在 spawn point 前方偏移位置（entryOffset）
- 傳送後啟用短暫保護時間（warpCooldownMs），保護期間忽略 warp overlap

**特例 - 邊界鏡像傳送：**

若 trigger 位置在地圖邊界，則在 targetMap 對邊出現：

```
當前地圖 right edge (x=1680, y=500)
  ↓ 鏡像 ↓
下一張地圖 left edge (x=20, y=500)
```

為避免切圖後立刻踩回傳送門，落點採「鏡像邊界 + 前方偏移」：

```
targetSpawn = mirrorEdgeSpawn + entryOffset
例：left edge spawn (x=20, y=500), entryOffsetX=+36
最終落點：(x=56, y=500)
```

**資料結構參考：**

```json
{
  "placements": [
    {
      "instanceId": "warp-circle-01",
      "objectId": "warp-circle",
      "x": 860,
      "y": 488,
      "w": 120,
      "h": 120,
      "sortY": 488,
      "isBlocking": false,
      "isInteractable": true,
      "triggerType": "warp",
      "trigger": {
        "type": "circle",
        "x": 860,
        "y": 488,
        "radius": 28
      },
      "warpData": {
        "targetMap": "shrine-02",
        "targetSpawn": "entrance-south",
        "entryOffset": { "x": 36, "y": 0 },
        "warpCooldownMs": 350
      }
    }
  ]
}
```

**代碼參考框架：**

```js
// MainScene.create()
this.warpTriggers = this.physics.add.group();
const placements = mapData.placements;
placements.forEach(p => {
  if (p.triggerType === 'warp' && p.trigger) {
    const triggerZone = this.physics.add.zone(
      p.trigger.x,
      p.trigger.y,
      p.trigger.radius * 2,
      p.trigger.radius * 2
    );
    triggerZone.warpData = p.warpData;
    this.warpTriggers.add(triggerZone);
  }
});

// 角色與 warp trigger 的 overlap（不碰撞，只觸發）
this.physics.add.overlap(
  this.player,
  this.warpTriggers,
  (player, trigger) => {
    if (!this.warpLockUntil || this.time.now >= this.warpLockUntil) {
      this.handleWarp(trigger.warpData);
    }
  }
);

handleWarp(warpData) {
  const {
    targetMap,
    targetSpawn,
    entryOffset = { x: 0, y: 0 },
    warpCooldownMs = 350
  } = warpData;
  const spawnPoint = this.getSpawnPointFromMap(targetMap, targetSpawn);
  const safeSpawn = {
    x: spawnPoint.x + entryOffset.x,
    y: spawnPoint.y + entryOffset.y
  };
  this.warpLockUntil = this.time.now + warpCooldownMs;
  
  // 場景切換
  this.scene.start('MainScene', {
    mapName: targetMap,
    spawnPoint: safeSpawn,
    warpLockUntil: this.warpLockUntil
  });
}
```

**鏡像邊界落點函式（四方向最小版）：**

```js
function getMirrorEdgeSpawn({
  exitEdge,           // 'left' | 'right' | 'top' | 'bottom'
  sourceX,
  sourceY,
  targetMapWidth,
  targetMapHeight,
  margin = 20,
  entryOffset = 36
}) {
  // 先保留另一軸座標，避免超出地圖範圍
  const clamp = (v, min, max) => Math.max(min, Math.min(max, v));
  const y = clamp(sourceY, margin, targetMapHeight - margin);
  const x = clamp(sourceX, margin, targetMapWidth - margin);

  switch (exitEdge) {
    case 'right':
      // 從右邊出去 -> 下一張圖左邊進來，並前移避免連續回傳
      return { x: margin + entryOffset, y };
    case 'left':
      return { x: targetMapWidth - margin - entryOffset, y };
    case 'top':
      return { x, y: targetMapHeight - margin - entryOffset };
    case 'bottom':
      return { x, y: margin + entryOffset };
    default:
      return { x, y };
  }
}
```

**使用方式（示意）：**

```js
const safeSpawn = getMirrorEdgeSpawn({
  exitEdge: warpData.exitEdge,
  sourceX: this.player.x,
  sourceY: this.player.y,
  targetMapWidth: nextMapMeta.width,
  targetMapHeight: nextMapMeta.height,
  margin: 20,
  entryOffset: 36
});
```

---

### 3. 角色腳下影子（Shadow Effect）

**目標：** shadow 固定在角色腳底，隨著角色移動，深度永遠在角色下方

**設計原則：**

- shadow 是角色的 footFx child object，但不綁定為 displayList child
- 每幀在 update 中同步 shadow 位置與深度
- shadow 不參與碰撞
- 預設模式是 `shadow`，未來可擴充成 `aura`、`poison-cloud` 等

**代碼參考框架（已在 SHADOW-AURA-SETUP.zh-TW.md）：**

```js
create() {
  this.player = this.physics.add.sprite(320, 240, 'player', 0);
  this.playerFootFx = this.createFootFx(this.player, { mode: 'shadow' });
}

update() {
  // ... 移動邏輯 ...
  this.syncFootFx(this.player, this.playerFootFx);
}

syncFootFx(actor, fx) {
  fx.setPosition(actor.x, actor.y + 14);
  fx.setDepth(actor.depth - 1);
}
```

---

### 4. Effect 層可擴充系統

**目標：** shadow 只是第一個 effect，未來可直接加其他 footFx（aura、治療圈、毒圈等）

**設計層級：**

```
Player
├─ sprite（角色動畫）
├─ footFxController（管理腳下所有 effect）
│  ├─ currentFootFx（當前 effect sprite）
│  ├─ mode（'shadow' | 'aura-fire' | 'aura-ice' | ...）
│  └─ overrideDuration（計時、持續時間）
└─ colliders
```

**Future footFx 類型規劃：**

- `shadow`：預設黑影
- `aura-fire`：火焰光圈（技能 casting）
- `aura-ice`：冰霜光圈（技能 casting）
- `poison-cloud`：毒雲持續效果
- `heal-glow`：治療光圈
- ...

**代碼設計：**

```js
class FootFxController {
  constructor(actor, modes = {}) {
    this.actor = actor;
    this.modes = modes; // { shadow: {...}, aura: {...} }
    this.currentMode = 'shadow';
    this.sprite = null;
    this.overrideDuration = 0;
  }

  setMode(mode, durationMs = 0) {
    if (this.modes[mode]) {
      const config = this.modes[mode];
      if (this.sprite) this.sprite.setTexture(config.texture);
      else this.sprite = /* create new sprite */;
      
      this.sprite.setAlpha(config.alpha || 1);
      this.currentMode = mode;
      this.overrideDuration = durationMs;
    }
  }

  update(delta) {
    // 同步位置
    this.sprite.setPosition(
      this.actor.x,
      this.actor.y + 14
    );
    this.sprite.setDepth(this.actor.depth - 1);

    // 計時：若 override 時間到，回到 shadow
    if (this.overrideDuration > 0) {
      this.overrideDuration -= delta;
      if (this.overrideDuration <= 0) {
        this.setMode('shadow');
      }
    }
  }
}
```

---

## 驗收清單

### Phase 2 必完成項目

- [ ] 地圖物件（rock、fence 等）正確載入並顯示
- [ ] 角色無法穿過可阻擋物件（碰撞正常運作）
- [ ] 角色踩到傳送門時觸發場景切換
- [ ] 傳送後角色出現在正確的鏡像邊界落點
- [ ] 邊界鏡像傳送：從地圖右邊界進入 → 下一張地圖左邊界出現
- [ ] 傳送落點會前移（entryOffset），不會一出生就碰到傳送門
- [ ] 傳送保護時間生效（warpCooldownMs），不會無限來回切圖
- [ ] Shadow 隨著角色移動
- [ ] Shadow 永遠在角色下方（depth 正確）
- [ ] 玩家可手動測試：按指定鍵觸發光圈（例如 aura-tidal-ripple）→ 腳下 shadow 變成 aura → 計時後回到 shadow
- [ ] 無 console error 與 warning

### 效能檢查

- [ ] 連續移動 5 分鐘無掉幀、無記憶體洩漏
- [ ] 地圖切換後舊地圖資源正確釋放

---

## 檔案結構建議

```text
project-root/
├─ src/
│  └─ scenes/
│     └─ MainScene.js （含碰撞、傳送、shadow 邏輯）
├─ data/
│  ├─ shrine-props.json （shrine 地圖物件擺放）
│  ├─ shrine-02-props.json （shrine-02 地圖物件擺放）
│  └─ spawn-points.json （全地圖 spawn point 定義）
├─ public/assets/
│  ├─ sprites/
│  │  ├─ edward/
│  │  │  ├─ walk.png
│  │  │  └─ idle.png
│  │  └─ ...
│  ├─ objects/
│  │  ├─ rock-mossy.png
│  │  ├─ fence-wood.png
│  │  ├─ warp-circle.png
│  │  └─ ...
│  └─ effects/
│     ├─ shadow.png
│     └─ aura-tidal-ripple.png
└─ ...
```

---

## 開發順序建議

1. **Day 1-2：** 實裝碰撞與地圖物件載入
   - 測試角色能否被 rock、fence 阻擋

2. **Day 3：** 實裝傳送系統
   - 測試場景切換
   - 測試 spawn point 座標正確性

3. **Day 4：** 整合 shadow 效果
   - 影子隨角色移動
   - 測試 shadow/aura 切換

4. **Day 5：** 整體測試與優化
   - 驗收清單逐項確認
   - 效能測試

---

## 後續擴充點

- [ ] 多個傳送目標（不同出口）
- [ ] 條件式傳送（需要鑰匙、等級等）
- [ ] 傳送動畫（淡出淡入、傳送特效）
- [ ] Aura 多種類型與層級系統
- [ ] 狀態效果光圈（中毒、冰凍等）
- [ ] 打擊特效（hit effect）與命中方向鏡像
