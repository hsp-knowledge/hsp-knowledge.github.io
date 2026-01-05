---
layout: post
title: 【HSPPP v0.1.1】ティアリング防止のvwait()と型安全なステートマシンで、ゲーム開発がもっと快適に
date: 2026-01-05 20:08:35 +09:00
author: Velgail
tags: [HSP3, ゲーム制作, C++, C++23, HSPPP]
summary: HSPPP v0.1.1で追加された、VSync同期の`vwait()`とHSPの*label/gotoを型安全に実装できるStateMachineを紹介します。画面のちらつきを防ぎ、安全で分かりやすいゲームフロー管理を実現します。
---

HSPPP v0.1.1がリリースされました！今回は、ゲーム開発でよく使う2つの機能を大幅に強化しました。

1. **`vwait()` - ティアリング防止機能を内蔵したVSync同期待機**
2. **StateMachine - HSPの`*label`/`goto`を型安全に実装できるステート管理システム**

どちらもHSPユーザーなら「あったらいいな」と思っていた機能です。順番に見ていきましょう。

## vwait() - 画面のちらつきを防ぐ最強の武器

### HSPの問題点：await()だけでは画面がちらつく

HSPでゲームを作るとき、こんなコードを書いていませんか？

```hsp
; HSPの典型的なゲームループ
*mainloop
    redraw 0           ; 描画開始

    ; 描画処理
    color 0,0,0 : boxf
    color 255,255,255
    pos x, y : gcopy 1, 0, 0, 32, 32

    redraw 1           ; 描画終了
    await 16           ; 約60FPS
    goto *mainloop
```

このコードには**ティアリング**（画面のちらつき・ずれ）が発生する可能性があります。`await 16`は「だいたい16ミリ秒待つ」だけで、モニターの垂直同期（VSync）とは関係ないからです。

### HSPPP独自の拡張：vwait()

HSPPPの`vwait()`は、**HSPには存在しない独自の拡張機能**です。以下の特徴があります：

- **自動的にVSync同期Present** - モニターのリフレッシュレートに完全同期
- **ティアリング防止を保証** - 画面のちらつき・ずれが起きない
- **描画バッファを自動フラッシュ** - `redraw(1)`を書かなくても安全
- **フレームドロップ検出** - 戻り値で前回からの経過時間を取得可能

### 使い方：超シンプル！

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    screen(0, 640, 480);

    int x = 0;

    // ゲームループ
    while (true) {
        redraw(0);              // 描画開始

        // 描画処理
        color(0, 0, 0);
        boxf();
        color(255, 255, 255);
        circle(x, 240, x + 32, 272, 1);

        x = (x + 5) % 640;

        // ✅ vwait()だけでティアリング防止完了！
        vwait();  // redraw(1)は不要！VSync同期で自動Present

        if (getkey(VK_ESCAPE)) break;
    }
}
```

**ポイント:**
- `redraw(0)`で描画開始
- 描画処理を書く
- `vwait()`を呼ぶだけ
- `redraw(1)`は書かなくてOK！（書いても動きます）

### 従来の方法との比較

| 方法 | ティアリング防止 | フレームレート | 使いやすさ |
|------|-----------------|----------------|-----------|
| HSPの`await` | ❌ なし | 不安定 | 😐 普通 |
| HSPPPの`await()` | ❌ なし | 安定（高精度タイマー） | 😊 良い |
| HSPPPの`vwait()` | ✅ **完全保証** | **VSync同期** | 🤩 **最高** |

### フレームドロップの検出も簡単

```cpp
int fps = ginfo_fps();  // モニターの最大FPS（60 or 144等）
double expected_ms = 1000.0 / fps;

while (true) {
    redraw(0);
    // ... 描画処理 ...

    double elapsed = vwait();  // 戻り値で前回からの経過時間を取得

    // フレームドロップ検出
    if (elapsed > expected_ms * 1.5) {
        logmes(strf("FPS DROPPED: %dms", static_cast<int>(elapsed)));
    }
}
```

### いつ使う？

| シーン | 推奨 | 理由 |
|--------|------|------|
| アクションゲーム | `vwait()` | なめらかな動きが重要 |
| シューティング | `vwait()` | ティアリングは致命的 |
| RPG（フィールド） | `vwait()` | スクロールがなめらか |
| メニュー画面 | `stop()` | 入力待ち、CPU負荷を抑える |
| ノベルゲーム | `stop()` | イベント駆動、省電力 |

---

## StateMachine - *label/gotoの現代的な進化形

### HSPのgotoは便利だけど...

HSPで画面遷移を作るとき、こう書きますよね：

```hsp
; HSPのゲームフロー
*title
    cls
    mes "タイトル画面"
    button "スタート", *game
    button "終了", *exit
    stop
    goto *title

*game
    cls
    mes "ゲーム中..."
    stick key
    if key & 128 : goto *result
    await 16
    goto *game

*result
    cls
    mes "リザルト"
    button "タイトルへ", *title
    stop
```

便利ですが、こんな問題もあります：

- **GUIオブジェクトの管理が難しい** - ボタンを毎回作り直すと重い
- **状態遷移が複雑になると破綻** - どこからどこに飛べるか分からない
- **C++では`goto`は非推奨** - モダンなコードスタイルに合わない

### StateMachine - 型安全で分かりやすい画面遷移

HSPPPのStateMachineは、HSPの`*label`/`goto`の**良いところはそのまま**に、**欠点を解消**します。

#### ステップ1：画面を定義する

```cpp
// HSPの *label に相当
enum class Screen {
    Title,      // *title
    Game,       // *game
    Result      // *result
};
```

#### ステップ2：各画面の処理を書く

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    screen(0, 640, 480);

    // StateMachineを作成
    auto sm = StateMachine<Screen>();

    int score = 0;

    // ═══════════════════════════════════════════
    // タイトル画面
    // ═══════════════════════════════════════════
    sm.state(Screen::Title)
      .on_enter([&]() {
          // ✅ ここは1回だけ実行：GUIを作る
          button("スタート", [&]() {
              score = 0;
              sm.jump(Screen::Game);
          });
          button("終了", [&]() { sm.quit(); });
      })
      .on_update([&](auto& sm) {
          // ✅ 毎フレーム実行：軽い処理だけ
          redraw(0);
          color(0, 0, 0);
          boxf();
          color(255, 255, 255);
          pos(250, 100);
          mes("タイトル画面");

          // キーボードショートカット
          if (getkey(' ')) {
              score = 0;
              sm.jump(Screen::Game);
          }

          redraw(1);
          stop();  // GUI画面：イベント待ち
      })
      .on_exit([&]() {
          // ✅ 画面を離れる時：GUIを削除
          clrobj();
      });

    // ═══════════════════════════════════════════
    // ゲーム画面
    // ═══════════════════════════════════════════
    sm.state(Screen::Game)
      .on_enter([&]() {
          // 初期化処理
          // 30秒後に自動的にリザルトへ
          sm.set_timer(Screen::Result, 30000);
      })
      .on_update([&](auto& sm) {
          redraw(0);
          color(0, 0, 0);
          boxf();

          color(255, 255, 255);
          pos(20, 20);
          mes(strf("スコア: %d", score));

          // ゲームロジック
          score++;

          if (getkey(VK_ESCAPE)) {
              sm.cancel_timer();
              sm.jump(Screen::Result);
          }

          vwait();  // ゲーム画面：60FPS
      });

    // ═══════════════════════════════════════════
    // リザルト画面
    // ═══════════════════════════════════════════
    sm.state(Screen::Result)
      .on_enter([&]() {
          button("もう一度", [&]() { sm.jump(Screen::Game); });
          button("タイトルへ", [&]() { sm.jump(Screen::Title); });
      })
      .on_update([&](auto& sm) {
          redraw(0);
          color(0, 0, 0);
          boxf();
          color(255, 255, 255);
          pos(200, 150);
          mes(strf("最終スコア: %d", score));

          redraw(1);
          stop();
      })
      .on_exit([&]() {
          clrobj();
      });

    // ゲーム開始
    sm.start(Screen::Title);
}
```

### StateMachineの3つのコールバック

| コールバック | 実行タイミング | 用途 |
|-------------|---------------|------|
| `on_enter()` | **画面に入った時（1回だけ）** | GUIオブジェクト作成、リソース読み込み |
| `on_update()` | **毎フレーム** | 描画、入力チェック、ゲームロジック |
| `on_exit()` | **画面を離れる時（1回だけ）** | GUIオブジェクト削除、後始末 |

### HSPのgotoとの対応表

| HSP | HSPPP StateMachine |
|-----|-------------------|
| `*title` | `sm.state(Screen::Title)` |
| `goto *game` | `sm.jump(Screen::Game)` |
| ラベル内のループ | `on_update()` 内で `await()`/`vwait()`/`stop()` |
| ボタンの `goto` | ボタンのラムダ式内で `sm.jump()` |

### 便利な機能

#### 1. タイマー自動遷移

```cpp
sm.state(Screen::Splash)
  .on_enter([&]() {
      // 3秒後に自動的にタイトルへ
      sm.set_timer(Screen::Title, 3000);
  })
  .on_update([&](auto& sm) {
      // ローディング画面の表示
      vwait();
  });
```

#### 2. 履歴機能（戻るボタン）

```cpp
sm.enable_history(5);  // 最大5画面まで履歴を保持

sm.state(Screen::Options)
  .on_enter([&]() {
      button("戻る", [&]() { sm.back(); });  // 前の画面に戻る
  });
```

#### 3. デバッグログ

```cpp
sm.enable_debug_log(true);

// コンソールに出力：
// [StateMachine] Enter state: Title
// [StateMachine] Transition: Title -> Game (frame: 120)
```

#### 4. 状態遷移グラフの可視化

```cpp
sm.export_graph("state_graph.dot");
// Graphviz でPNG化: dot -Tpng state_graph.dot -o graph.png
```

### 実践：クリックゲームのサンプル

完全なサンプルコードは[HspppStateSample](https://github.com/Velgail/HspppLib/tree/main/HspppStateSample)にあります。

以下の画面遷移を実装しています：

```
Splash（2秒自動遷移）
  ↓
Title ←────────┐
  ↓            │
Game ⇄ Pause   │
  ↓            │
GameOver（3秒自動遷移）
  ↓            │
Result ────────┘
```

特徴：
- スプラッシュ画面は2秒で自動遷移
- ゲーム画面は30秒のタイマー付き
- ポーズ画面からゲームに戻れる
- ゲームオーバー後は3秒でリザルトへ
- 履歴機能で「戻る」ボタンが使える

---

## まとめ

HSPPP v0.1.1では、ゲーム開発で重要な2つの機能を追加しました：

### vwait() - ティアリング防止の決定版

✅ VSync同期で画面のちらつきを完全防止
✅ `redraw(1)`不要で簡潔に書ける
✅ フレームドロップ検出も簡単
✅ **HSPPP独自の拡張機能**

### StateMachine - 型安全な画面遷移

✅ HSPの`*label`/`goto`と同じ感覚で書ける
✅ GUIオブジェクトの管理が自動化
✅ タイマー遷移、履歴機能など便利な機能満載
✅ デバッグ支援（ログ、グラフ可視化）

どちらも**HSPユーザーが求めていた機能**を、**モダンなC++の安全性**で実現しています。

「C++は難しそう」と思っていた方も、HSPPPなら慣れ親しんだHSPの書き方で、より高度なゲーム開発ができます。

## リンク

- [HSPPP GitHub](https://github.com/Velgail/HspppLib)
- [公式ドキュメント](https://velgail.github.io/HspppLib/)
- [ステートマシンAPIリファレンス](https://velgail.github.io/HspppLib/api/statemachine.html)
- [vwait() APIリファレンス](https://velgail.github.io/HspppLib/api/interrupt.html#vwait)
- [サンプルコード（StateMachine）](https://github.com/Velgail/HspppLib/tree/main/HspppStateSample)

### ライセンスについて

HSPPPは **Boost Software License 1.0** で提供されています。

**つまり、あなたが自由にできること：**

✅ **HSPPPを使って作ったゲームやアプリは完全にあなたのもの**
✅ **exe配布時にライセンス表記は不要** - クレジット表記もライセンスファイルの同梱も必要ありません
✅ **商用利用も完全に自由** - ゲームを販売してもOK、業務アプリに使ってもOK
✅ **ソースコードを公開する義務なし** - あなたが書いたコードは秘密にできます

HSPと同じ感覚で、気軽に使ってください！
