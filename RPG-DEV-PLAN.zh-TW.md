# RPG 冒險遊戲開發計畫

## 技術選型

| 層級 | 選用技術 | 說明 |
|------|----------|------|
| 打包工具 | Vite | 快速開發伺服器、熱更新 |
| 遊戲框架 | Phaser 3 | 內建 spritesheet、tilemap、碰撞 |
| 語言 | JavaScript / TypeScript | 視團隊習慣選擇 |
| 地圖編輯 | Tiled Map Editor | 輸出 Phaser 相容的 JSON tilemap |
| Sprite 來源 | agent-sprite-forge | 本 repo 產出的角色與地圖素材 |

---

## 專案初始化

```bash
npm create vite@latest my-rpg -- --template vanilla
cd my-rpg
npm install phaser
npm run dev
```

---

## Sprite 規格對應

本計畫使用 `agent-sprite-forge` 產出的素材，規格如下：

| 素材類型 | Sheet 尺寸 | 用途 |
|----------|------------|------|
| 角色行走 | 4x4 | 四方向移動（下／左／右／上） |
| 角色閒置 | 3x3 | 站立呼吸、特殊動作（如進食） |
| 角色攻擊 | 2x2 | 戰鬥攻擊動畫 |
| 地圖 props | 透明 PNG | 場景裝飾物件 |

> 背景色為 `#FF00FF`（洋紅色），輸出後需去背或由後處理腳本轉透明。

---

## Phaser 3 核心實作

### 載入 Spritesheet

```js
// preload()
this.load.spritesheet('edward', 'assets/edward-walk.png', {
  frameWidth: 64,
  frameHeight: 64
});

this.load.spritesheet('edward-idle', 'assets/edward-idle.png', {
  frameWidth: 64,
  frameHeight: 64
});
```

### 定義行走動畫（4x4 sheet）

```js
// create()
// Row 0 = 往下（frame 0–3）
this.anims.create({
  key: 'walk-down',
  frames: this.anims.generateFrameNumbers('edward', { start: 0, end: 3 }),
  frameRate: 8,
  repeat: -1
});

// Row 1 = 往左（frame 4–7）
this.anims.create({
  key: 'walk-left',
  frames: this.anims.generateFrameNumbers('edward', { start: 4, end: 7 }),
  frameRate: 8,
  repeat: -1
});

// Row 2 = 往右（frame 8–11）
this.anims.create({
  key: 'walk-right',
  frames: this.anims.generateFrameNumbers('edward', { start: 8, end: 11 }),
  frameRate: 8,
  repeat: -1
});

// Row 3 = 往上（frame 12–15）
this.anims.create({
  key: 'walk-up',
  frames: this.anims.generateFrameNumbers('edward', { start: 12, end: 15 }),
  frameRate: 8,
  repeat: -1
});
```

### 定義閒置動畫（3x3 sheet）

```js
// 進食閒置（9 格循環）
this.anims.create({
  key: 'idle-eat',
  frames: this.anims.generateFrameNumbers('edward-idle', { start: 0, end: 8 }),
  frameRate: 6,
  repeat: -1
});
```

### 四方向移動控制

```js
// update()
const cursors = this.cursors;
const speed = 160;

if (cursors.left.isDown) {
  player.setVelocityX(-speed);
  player.anims.play('walk-left', true);
} else if (cursors.right.isDown) {
  player.setVelocityX(speed);
  player.anims.play('walk-right', true);
} else if (cursors.up.isDown) {
  player.setVelocityY(-speed);
  player.anims.play('walk-up', true);
} else if (cursors.down.isDown) {
  player.setVelocityY(speed);
  player.anims.play('walk-down', true);
} else {
  player.setVelocity(0);
  player.anims.play('idle-eat', true); // 停止移動時播放閒置
}
```

---

## 開發里程碑

### Phase 1 — 可動角色
- [ ] Vite + Phaser 3 環境建立
- [ ] 載入 Edward walk sheet
- [ ] 四方向行走動畫可切換
- [ ] 鍵盤輸入控制移動
- [ ] 停止時播放閒置動畫

### Phase 2 — 場景與地圖
- [ ] 用 Tiled 製作第一張室外地圖
- [ ] 載入 `agent-sprite-forge` 產出的 props
- [ ] 碰撞層設定（牆壁、物件不可穿越）
- [ ] 攝影機跟隨角色

### Phase 3 — 互動與內容
- [ ] NPC 角色放置與對話框
- [ ] 場景切換（室內↔室外）
- [ ] 物品拾取系統
- [ ] 簡單戰鬥或事件觸發

---

## 最小可玩移動版任務清單（建議先完成）

> 目標：只完成「角色可在地圖上順暢移動」的可玩版本，不含生命值、技能、飛行物與戰鬥邏輯。

### Task A — 專案與素材佈局
- [ ] 建立前端專案（Vite + Phaser 3）
- [ ] 建立素材路徑結構：
  - `public/assets/sprites/{CHARACTER-NAME}/walk.png`
  - `public/assets/sprites/{CHARACTER-NAME}/idle.png`
  - `public/assets/maps/{map-name}/`
- [ ] 將 `output/{CHARACTER-NAME}/action/walk` 與 `output/{CHARACTER-NAME}/action/idle` 的最終圖整理進上述路徑
- [ ] 建立 `src/scenes/MainScene.js`（或 `.ts`）並完成基本 `preload/create/update` 骨架

### Task B — 動畫命名規則與實作
- [ ] 統一動畫 key 規則：`<角色>-<狀態>-<方向>`
- [ ] 行走動畫 key：
  - `{CHARACTER-NAME}-walk-down`
  - `{CHARACTER-NAME}-walk-left`
  - `{CHARACTER-NAME}-walk-right`
  - `{CHARACTER-NAME}-walk-up`
- [ ] 閒置動畫 key：
  - `{CHARACTER-NAME}-idle-down`
  - `{CHARACTER-NAME}-idle-left`
  - `{CHARACTER-NAME}-idle-right`
  - `{CHARACTER-NAME}-idle-up`
- [ ] 設定 row 對應（4x4 walk）：
  - Row 0 = down, Row 1 = left, Row 2 = right, Row 3 = up
- [ ] 設定移動速度與動畫播放速率（建議：speed 140~180、walk frameRate 8）

### Task C — 地圖、碰撞與鏡頭
- [ ] 載入地圖底圖（先用你剛產生的空白地圖）
- [ ] 建立 `collision` 圖層或碰撞區塊資料（可先用簡易矩形區塊）
- [ ] 角色加入 Arcade Physics，並啟用與碰撞層的 collision
- [ ] 設定攝影機跟隨角色：`camera.startFollow(player)`
- [ ] 限制攝影機邊界與世界邊界一致，避免看到地圖外區域

### Task D — 輸入與狀態切換
- [ ] 鍵盤輸入：方向鍵 + WASD（擇一或同時支援）
- [ ] 支援斜向移動時速度正規化（避免斜向比直向快）
- [ ] 無輸入時播放最後朝向對應的 idle 動畫
- [ ] 切換場景或重載後，角色預設朝向一致（建議 down）

### Task E — 驗收標準（Definition of Done）
- [ ] 可在地圖上連續移動 3 分鐘，無卡頓與無明顯掉幀
- [ ] 四方向 walk/idle 均能正確切換，無錯誤 frame 對應
- [ ] 角色無法穿越碰撞區域
- [ ] 攝影機全程平滑跟隨，且不超出地圖邊界
- [ ] 重新整理頁面後，遊戲可正常進入並操作（無 console error）

### Task F — 時間建議（1~2 週）
- [ ] Day 1~2：Task A（專案與素材路徑）
- [ ] Day 3~4：Task B（動畫定義與命名統一）
- [ ] Day 5~6：Task C（碰撞與鏡頭）
- [ ] Day 7：Task D（輸入細節與 idle 朝向）
- [ ] Day 8：Task E（驗收、修正、整理）

---

## 何時考慮遷移至 Unity

以下條件成立時可評估遷移：

- 地圖規模超過 5 個場景且邏輯複雜
- 需要物理引擎（跳躍平台、投擲）
- 計畫發布為桌面執行檔或手機 App
- 需要 3D 元素

---

## 參考資源

- [Phaser 3 官方文件](https://newdocs.phaser.io/)
- [Tiled Map Editor](https://www.mapeditor.org/)
- [Phaser 3 + Tiled 教學](https://phaser.io/tutorials/making-your-first-phaser-3-game)
- 本 repo sprite 產出：`src/` 目錄下各角色資料夾
