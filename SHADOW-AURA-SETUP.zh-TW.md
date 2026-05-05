# Phaser 2.5D 角色腳下 Shadow/Aura 最小實作

這份是可直接套用的最小骨架，目標：

1. 每個角色預設有共用影子（shadow）
2. 技能發動時可切成光圈（aura）
3. 技能結束後回到影子
4. 腳下效果永遠跟著角色，不參與碰撞

---

## 資產建議

請先準備兩張共用素材：

- `public/assets/effects/shadow.png`：橢圓形半透明黑影（建議 64x24）
- `public/assets/effects/aura.png`：技能光圈（建議 96x96，可做 1 張或動畫圖）

建議 shadow 初始參數：

- `alpha = 0.35`
- `scaleX = 1.0`
- `scaleY = 1.0`

---

## 最小骨架（JavaScript）

```js
// MainScene.js
export default class MainScene extends Phaser.Scene {
  constructor() {
    super('MainScene');
    this.player = null;
    this.playerFootFx = null;
    this.isCasting = false;
    this.castTimerMs = 0;
  }

  preload() {
    // 角色素材（請換成你的實際路徑）
    this.load.spritesheet('player', 'assets/sprites/edward/walk.png', {
      frameWidth: 64,
      frameHeight: 64
    });

    // 腳下效果素材（共用）
    this.load.image('fx-shadow', 'assets/effects/shadow.png');
    this.load.image('fx-aura', 'assets/effects/aura.png');
  }

  create() {
    // 角色
    this.player = this.physics.add.sprite(320, 240, 'player', 0);
    this.player.setCollideWorldBounds(true);

    // 建立腳下效果（預設 shadow）
    this.playerFootFx = this.createFootFx(this.player, {
      mode: 'shadow'
    });

    // 測試：按空白鍵切換技能光圈 800ms
    this.input.keyboard.on('keydown-SPACE', () => {
      this.startCast(800);
    });
  }

  update(time, delta) {
    // 這裡保留你原本的移動程式
    // ... WASD movement ...

    // 每幀同步腳下效果位置與深度
    this.syncFootFx(this.player, this.playerFootFx);

    // 技能計時，結束後回到 shadow
    if (this.isCasting) {
      this.castTimerMs -= delta;
      if (this.castTimerMs <= 0) {
        this.endCast();
      }
    }
  }

  createFootFx(actor, { mode = 'shadow' } = {}) {
    const x = actor.x;
    const y = actor.y + 14; // 視角色腳底位置微調

    const fx = this.add.sprite(x, y, mode === 'aura' ? 'fx-aura' : 'fx-shadow');

    // 影子/光圈都在角色下方
    fx.setDepth(actor.depth - 1);

    // 不參與碰撞；純視覺
    // 使用 add.sprite 即可，不用 physics

    if (mode === 'shadow') {
      fx.setAlpha(0.35);
      fx.setScale(1.0, 1.0);
    } else {
      fx.setAlpha(0.9);
      fx.setScale(1.0);
    }

    return fx;
  }

  syncFootFx(actor, fx) {
    fx.setPosition(actor.x, actor.y + 14);
    fx.setDepth(actor.depth - 1);
  }

  setFootFxMode(fx, mode) {
    if (mode === 'aura') {
      fx.setTexture('fx-aura');
      fx.setAlpha(0.9);
      fx.setScale(1.0);
    } else {
      fx.setTexture('fx-shadow');
      fx.setAlpha(0.35);
      fx.setScale(1.0, 1.0);
    }
  }

  startCast(durationMs = 800) {
    this.isCasting = true;
    this.castTimerMs = durationMs;
    this.setFootFxMode(this.playerFootFx, 'aura');
  }

  endCast() {
    this.isCasting = false;
    this.castTimerMs = 0;
    this.setFootFxMode(this.playerFootFx, 'shadow');
  }
}
```

---

## TypeScript 介面建議（可選）

```ts
type FootFxMode = 'shadow' | 'aura';

interface FootFxState {
  mode: FootFxMode;
  offsetY: number;
  shadowAlpha: number;
  auraAlpha: number;
}
```

---

## 之後擴充建議

1. 若角色會跳躍：跳越高，shadow 越小且越淡
2. 若技能有多種：把 aura 換成不同 key（例如 `fx-aura-fire`, `fx-aura-ice`）
3. 若多人角色：每個 actor 都綁一個 footFx，更新時一起同步
4. 若要性能更穩：可把腳下效果改成 Pool 管理，避免頻繁建立/刪除

---

## 驗收清單

- 角色移動時，腳下效果持續跟隨
- 腳下效果永遠在角色下方（depth 正確）
- 技能啟動時從 shadow 切到 aura
- 技能結束時回到 shadow
- 腳下效果不影響碰撞與移動
