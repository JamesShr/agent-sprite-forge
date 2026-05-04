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
