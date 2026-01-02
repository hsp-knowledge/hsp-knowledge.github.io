---
layout: post
title: HSPPP (Hot Soup Processor Plus Plus) — HSPユーザーのためのC++移行ライブラリ 完全ガイド
date: 2026-01-03 01:43:53 +09:00
author: Velgail + Opus 4.5(Copilot)
tags: [HSP3, ライブラリ, Tips, 応用, C++, C++23, HSPPP]
summary: ついに登場！　HSPPP Libを作りきったのでご紹介です！（なおデバッグがしっかりできてないからアルファ版でございます）
---

{% include toc.html %}

## HspppLib とは

**HSPPP (Hot Soup Processor Plus Plus)** は、HSP (Hot Soup Processor) 互換の C++23 ライブラリです。

HSPで培った知識とコーディングスタイルを活かしながら、C++の型安全性、パフォーマンス、拡張性を手に入れることができます。

**GitHub**: https://github.com/Velgail/HSPPP_Lib

### 特徴

| 機能 | 説明 |
| --- | --- |
| 🎮 **HSP互換API** | `screen`, `color`, `boxf`, `mes` などお馴染みの命令をそのまま使用可能 |
| 📦 **モダンC++** | C++23 の機能を活用した型安全・メモリ安全な設計 |
| 🔧 **デュアルスタイル** | HSP風のグローバル関数とOOP風のメソッドチェーン、お好みで選択 |
| 🖼️ **Direct2D描画** | 高品質なハードウェアアクセラレーション描画 |
| ⚡ **ゼロオーバーヘッド** | C++の哲学「使わないものにコストを払わない」 |
| 🛡️ **安全性重視** | 生ポインタ禁止、RAII、例外によるエラー処理 |

### なぜHspppなのか

HSPは素晴らしい言語ですが、以下のような限界があります：

* 大規模プロジェクトでの保守性
* 型チェックの欠如によるバグ
* 外部ライブラリとの連携の難しさ
* パフォーマンスの上限

HspppはこれらをC++の力で解決しつつ、HSPの「書きやすさ」を維持します。

***

## 設計思想: Pragmatic Hybrid

Hspppの設計思想は **「Pragmatic Hybrid（実用主義的ハイブリッド）」** です。

### 設計目標

1. **HSP再現性**: `hspMain` 内ではHSPとほぼ同じロジックで記述できる
2. **安全性**: C++の型システムとRAII（自動リソース管理）により、メモリリークや型エラーを防ぐ
3. **拡張性**: ユーザーはいつでも「HSPの皮」を破り、DirectXやWin32 APIの深層へアクセスできる

### ターゲットユーザー

* HSPでの開発に限界を感じ、C++へ移行したい
* しかし、Javaのような過度な儀式（ボイラープレート）は嫌う
* 「手軽さ」と「パワー」の両立を求める

***

## 環境要件とセットアップ

### 必須環境

| 項目 | 要件 |
| --- | --- |
| **OS** | Windows 11 (64-bit) |
| **コンパイラ** | Visual Studio 2026 (VS 18) |
| **C++標準** | C++23 (`/std:c++latest`) |
| **必須ライブラリ** | Direct2D, DirectWrite (Windows SDK に含まれる) |

> ⚠️ **重要**: Visual Studio 2022 (VS 17) ではビルドできません。必ずVS 2026を使用してください。

### ビルド手順

#### Visual Studio から

1. HspppLib.slnx を Visual Studio 2026 で開く
2. プラットフォームを x64 に設定
3. ビルド (`F7` または `Ctrl+Shift+B`)

#### コマンドライン (MSBuild) から

```powershell
# 文字化け防止（必須）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Debug ビルド
& "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe" `
    HspppLib.slnx /p:Configuration=Debug /p:Platform=x64 /m

# Release ビルド
& "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe" `
    HspppLib.slnx /p:Configuration=Release /p:Platform=x64 /m
```

### 実行

```powershell
& "x64\Debug\HspppSample.exe"
```

***

## プロジェクト構成

```
HspppLib/
├── HspppLib/              # ライブラリ本体（静的ライブラリ）
│   ├── module/            # C++23 モジュール (.ixx)
│   │   ├── hsppp.ixx           # メインモジュール（これだけimportすればOK）
│   │   ├── hsppp_types.ixx     # 型定義（OptInt, Screen, Quad等）
│   │   ├── hsppp_screen.ixx    # 画面制御（screen, buffer, gsel等）
│   │   ├── hsppp_drawing.ixx   # 描画命令（mes, boxf, line等）
│   │   ├── hsppp_input.ixx     # 入力処理（stick, getkey, mouse等）
│   │   ├── hsppp_math.ixx      # 数学関数（sin, cos, rnd等）
│   │   ├── hsppp_string.ixx    # 文字列操作（strmid, instr, NotePad等）
│   │   ├── hsppp_file.ixx      # ファイル/GUI（exist, bload, button等）
│   │   ├── hsppp_interrupt.ixx # 割り込み（onclick, onerror等）
│   │   └── hsppp_media.ixx     # メディア（mmplay, mmstop等）
│   └── src/
│       ├── boot/          # エントリポイント（WinMain）
│       └── core/          # 内部実装
│
├── HspppSample/           # サンプルアプリケーション（.exe）
│   ├── UserApp.cpp            # ユーザーコード（hspMainを記述）
│   ├── DemoDrawBasic.cpp      # 基本描画デモ
│   ├── DemoDrawExtended.cpp   # 拡張描画デモ
│   ├── DemoDrawGUI.cpp        # GUIデモ
│   └── ...
│
├── HspppTest/             # 単体テスト
└── docs/                  # ドキュメント（GitHub Pages用）
```

***

## はじめてのHsppp

### 最小限のプログラム

```cpp
// UserApp.cpp
import hsppp;
using namespace hsppp;

// エントリポイント: hspMain() を定義（main/WinMain は書かない）
void hspMain() {
    // ウィンドウ作成
    screen(0, 640, 480);
    title("Hello HSPPP!");
    
    // 描画
    color(255, 0, 0);       // 赤色を設定
    boxf(100, 100, 200, 200);  // 矩形を塗りつぶし
    
    color(255, 255, 255);   // 白色を設定
    pos(120, 140);          // 描画位置を設定
    mes("Hello, HSPPP!");   // 文字列を描画
    
    // hspMain を抜けると stop() と同等（ウィンドウは閉じずに待機）
    return;
}
```

### HSPとの対比

| HSP | HSPPP |
| --- | ----- |
| (自動実行) | `void hspMain() { ... }` |
| `screen 0, 640, 480` | `screen(0, 640, 480);` |
| `title "Hello"` | `title("Hello");` |
| `color 255, 0, 0` | `color(255, 0, 0);` |
| `boxf 100, 100, 200, 200` | `boxf(100, 100, 200, 200);` |
| `stop` | `stop();` |

### 重要な違い

1. **main/WinMain は書かない**: ライブラリ側が提供
2. **行末にセミコロン `;`**: C++の文法
3. **命令は関数呼び出し**: カッコ `()` で引数を囲む
4. **文字列はダブルクォート**: `"..."` のみ（シングルクォート `'...'` は文字1つ）
5. **変数は型を宣言**: `int x = 0;` のように書く

***

## HSP互換スタイル vs OOPスタイル

Hspppは2つのコーディングスタイルをサポートします。

### HSP互換スタイル（グローバル関数）

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    // HSPとほぼ同じ書き方
    screen(0, 640, 480);
    color(255, 0, 0);
    boxf(100, 100, 200, 200);
    
    color(255, 255, 255);
    pos(120, 140);
    mes("Hello!");
    
    return;
}
```

### OOPスタイル（メソッドチェーン）

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    // 構造体による初期化（Designated Initializers）
    auto win = screen({.width = 640, .height = 480, .title = "OOP Style"});
    
    // メソッドチェーンで連続描画
    win.color(255, 0, 0)
       .boxf(100, 100, 200, 200)
       .color(255, 255, 255)
       .pos(120, 140)
       .mes("Method Chaining!");
    
    return;
}
```

### どちらを使うべきか？

| スタイル | 適したケース |
| ---- | ------ |
| **HSP互換** | HSPからの移行初期、シンプルなプログラム |
| **OOP** | 複数ウィンドウの管理、大規模プロジェクト |

両方を混在させることも可能です。

***

## パラメータ省略の仕組み

HSPでは `screen , 800, 600` のように任意の位置でパラメータを省略できます。Hspppでもこれを実現しています。

### 省略の方法

```cpp
// 方法1: omit キーワード
screen(omit, 800, 600);        // ID=0(省略), 800x600
screen(1, omit, omit, screen_hide);  // サイズ省略、非表示モード

// 方法2: 空の波括弧 {}
screen({}, 800, 600);          // ID=0(省略), 800x600
```

### なぜ `omit` なのか

C++26 では `_`（アンダースコア）が「名前独立宣言」として特別な意味を持つようになります。将来の互換性のため、`omit` キーワードを採用しています。

### 内部の仕組み: OptInt / OptDouble

```cpp
// 省略可能なint型
struct OptInt {
    std::optional<int> value_;
    
    constexpr OptInt() noexcept : value_(std::nullopt) {}  // 省略
    constexpr OptInt(int v) noexcept : value_(v) {}        // 値指定
    
    bool is_default() const noexcept { return !value_.has_value(); }
    int value_or(int def) const noexcept { return value_.value_or(def); }
};
```

***

## 型システムの理解

### 基本型の対応

| HSP | HSPPP (C++) | 説明 |
| --- | ----------- | --- |
| 整数 | `int` | 32bit整数 |
| 実数 | `double` | 64bit浮動小数点 |
| 文字列 | `std::string` | UTF-8文字列 |
| 配列 | `std::vector<T>` | 動的配列 |

### Hsppp独自の型

#### OptInt / OptDouble / OptInt64

省略可能なパラメータを表現

```cpp
void screen(int id, OptInt width = {}, OptInt height = {});
```

#### Screen

ウィンドウへの軽量ハンドル。内部ではIDのみを保持。

```cpp
Screen win = screen(0, 640, 480);
win.color(255, 0, 0).boxf(0, 0, 100, 100);
```

#### Cel

画像素材（スプライト）へのハンドル

```cpp
Cel sprite = loadCel("player.png");
sprite.divide(4, 4);  // 4x4分割
sprite.put(0, 100, 100);  // セル0を描画
```

#### Quad / QuadUV / QuadColors

gsquare用の4頂点座標

```cpp
Quad dst(0, 0, 100, 0, 100, 100, 0, 100);  // 左上, 右上, 右下, 左下
gsquare(-1, dst);  // 単色塗りつぶし
```

#### DialogResult

dialog命令の戻り値（intとstringの両方に変換可能）

```cpp
DialogResult result = dialog("OK?", dialog_yesno);
if (result) {  // int への変換（stat相当）
    std::string path = result;  // string への変換（refstr相当）
}
```

#### NotePad

OOP版メモリノートパッド

```cpp
NotePad note;
note.load("data.txt");
std::string line = note.get(0);  // 1行目を取得
note.add("新しい行").save("data.txt");
```

#### HspError / HspErrorRecoverable

例外クラス（onerrorで捕捉可能）

***

## API リファレンス

### 画面制御

#### screen / buffer / bgscr

```cpp
// HSP互換
Screen screen(int id, OptInt width = {}, OptInt height = {}, OptInt mode = {}, ...);
Screen buffer(int id, OptInt width = {}, OptInt height = {}, OptInt mode = {});
Screen bgscr(int id, OptInt width = {}, OptInt height = {}, OptInt mode = {}, ...);

// OOP（ID自動採番）
Screen screen(const ScreenParams& params);
Screen screen();  // デフォルト設定

// パラメータ構造体
struct ScreenParams {
    int width = 640;
    int height = 480;
    int mode = 0;
    int pos_x = -1;
    int pos_y = -1;
    std::string_view title = "HSPPP Window";
};
```

**modeフラグ:**

* `screen_normal (0)`: フルカラーモード
* `screen_hide (2)`: 非表示
* `screen_fixedsize (4)`: サイズ固定
* `screen_tool (8)`: ツールウィンドウ
* `screen_fullscreen (256)`: フルスクリーン（bgscr用）

#### gsel

```cpp
void gsel(OptInt id = {}, OptInt mode = {});
// mode: -1=非表示, 0=影響なし, 1=アクティブ, 2=アクティブ+最前面
```

#### gmode

```cpp
void gmode(OptInt mode = {}, OptInt size_x = {}, OptInt size_y = {}, OptInt blend_rate = {});
// mode: 0=通常, 1=透明色, 2=半透明, 3=透明色+半透明, 4=加算, 5=減算, 6=乗算
// blend_rate: 0~256（256で不透明）
```

#### gcopy / gzoom / grotate

```cpp
void gcopy(OptInt src_id = {}, OptInt src_x = {}, OptInt src_y = {}, OptInt size_x = {}, OptInt size_y = {});
void gzoom(OptInt dest_w = {}, OptInt dest_h = {}, OptInt src_id = {}, OptInt src_x = {}, OptInt src_y = {}, OptInt src_w = {}, OptInt src_h = {}, OptInt mode = {});
void grotate(OptInt srcId = {}, OptInt srcX = {}, OptInt srcY = {}, OptDouble angle = {}, OptInt dstW = {}, OptInt dstH = {});
```

#### redraw / await / cls

```cpp
void redraw(int p1 = 1);  // 0=描画予約, 1=画面反映
void await(int time_ms);  // 待機（ミリ秒）
void cls(OptInt p1 = {}); // 0=白, 1=明灰, 2=灰, 3=暗灰, 4=黒
```

#### picload / bmpsave / celload

```cpp
void picload(std::string_view filename, OptInt mode = {});
void bmpsave(std::string_view filename);
int celload(std::string_view filename, OptInt id = {});
void celdiv(int id, int divX, int divY);
void celput(int id, int cellIndex, OptInt x = {}, OptInt y = {});

// OOP版
Cel loadCel(std::string_view filename);
```

***

### 描画命令

#### color / pos / mes

```cpp
void color(int r, int g, int b);
void pos(int x, int y);
void mes(std::string_view text, OptInt sw = {});
// sw: 1=改行しない, 2=影, 4=縁取り, 8=簡易描画, 16=gmode設定

void print(std::string_view text, OptInt sw = {});  // mesの別名
```

#### boxf / line / circle / pset / pget

```cpp
void boxf(int x1, int y1, int x2, int y2);
void boxf();  // 画面全体

void line(OptInt x2 = {}, OptInt y2 = {}, OptInt x1 = {}, OptInt y1 = {});
void circle(OptInt x1 = {}, OptInt y1 = {}, OptInt x2 = {}, OptInt y2 = {}, OptInt fillMode = {});
// fillMode: 0=線, 1=塗りつぶし

void pset(OptInt x = {}, OptInt y = {});
void pget(OptInt x = {}, OptInt y = {});  // 色を取得して選択色に設定
```

#### gradf / grect / gsquare

```cpp
void gradf(OptInt x = {}, OptInt y = {}, OptInt w = {}, OptInt h = {}, OptInt mode = {}, OptInt color1 = {}, OptInt color2 = {});
// mode: 0=上→下, 1=左→右, 2=左上→右下

void grect(OptInt cx = {}, OptInt cy = {}, OptDouble angle = {}, OptInt w = {}, OptInt h = {});

void gsquare(int srcId, const Quad& dst);  // 単色
void gsquare(int srcId, const Quad& dst, const QuadUV& src);  // 画像
void gsquare(int srcId, const Quad& dst, const QuadColors& colors);  // グラデーション
```

#### font / sysfont

```cpp
int font(std::string_view fontName, OptInt size = {}, OptInt style = {}, OptInt decorationWidth = {});
// style: 0=通常, 1=太字, 2=斜体, 3=太字+斜体

void sysfont(OptInt type = {});
// type: 0=HSP標準, 17=デフォルトGUI
```

#### hsvcolor / rgbcolor / syscolor

```cpp
void hsvcolor(int h, int s, int v);  // HSV形式（h: 0-191, s: 0-255, v: 0-255）
void rgbcolor(int rgb);  // 0xRRGGBB形式
void syscolor(int id);   // システムカラー
```

***

### 入力処理

#### stick

```cpp
int stick(OptInt nonTrigger = {}, OptInt checkActive = {});
```

**ビットマスク定数:**

```cpp
stick_left    = 1;       // ←
stick_up      = 2;       // ↑
stick_right   = 4;       // →
stick_down    = 8;       // ↓
stick_space   = 16;      // Space
stick_enter   = 32;      // Enter
stick_ctrl    = 64;      // Ctrl
stick_esc     = 128;     // ESC
stick_lbutton = 256;     // マウス左
stick_rbutton = 512;     // マウス右
stick_tab     = 1024;    // Tab
stick_z       = 2048;    // Z
stick_x       = 4096;    // X
stick_c       = 8192;    // C
stick_a       = 16384;   // A
stick_w       = 32768;   // W
stick_d       = 65536;   // D
stick_s       = 131072;  // S
```

**使用例:**

```cpp
int key = stick(15);  // 方向キーは押しっぱなしでも検出
if (key & stick_left)  x -= 5;
if (key & stick_right) x += 5;
if (key & stick_space) fire();
```

#### getkey

```cpp
int getkey(int keycode);  // 押されていれば1
```

#### mouse / mousex / mousey / mousew

```cpp
void mouse(OptInt x = {}, OptInt y = {}, OptInt mode = {});
// mode: 0=負値で非表示, -1=移動+非表示, 1=移動のみ, 2=移動+表示

int mousex();  // X座標
int mousey();  // Y座標
int mousew();  // ホイール移動量
```

***

### 数学関数

#### 三角関数（ラジアン）

```cpp
// <cmath>の関数をそのまま再エクスポート
using std::sin, std::cos, std::tan;
using std::asin, std::acos, std::atan, std::atan2;
using std::sinh, std::cosh, std::tanh;
```

#### 角度変換

```cpp
double deg2rad(double degrees);  // 度→ラジアン
double rad2deg(double radians);  // ラジアン→度
```

#### 乱数

```cpp
int rnd(int max);  // 0〜max-1の乱数（HSP互換のLCG）
void randomize(OptInt seed = {});  // シード設定（省略時は時刻ベース）
```

#### 範囲制限

```cpp
int limit(int value, OptInt min = {}, OptInt max = {});
double limitf(double value, OptDouble min = {}, OptDouble max = {});
```

#### イージング

```cpp
void setease(double start, double end, OptInt type = {});
int getease(int progress, OptInt max = {});
double geteasef(double progress, OptDouble max = {});
```

**イージングタイプ:**

```cpp
ease_linear = 0;
ease_quad_in = 1;
ease_quad_out = 2;
ease_quad_inout = 3;
ease_cubic_in = 4;
// ... (bounce, shake等もあり)
ease_loop = 0x100;  // ループフラグ
```

#### ソート

```cpp
void sortval(std::vector<int>& arr, OptInt order = {});
void sortval(std::vector<double>& arr, OptInt order = {});
void sortstr(std::vector<std::string>& arr, OptInt order = {});
void sortnote(std::string& note, OptInt order = {});
int sortget(int index);  // ソート前のインデックスを取得
```

#### 数学定数

```cpp
M_PI;      // π
M_PI_2;    // π/2
M_PI_4;    // π/4
M_E;       // e（自然対数の底）
M_LOG2E;   // log₂(e)
M_LN2;     // ln(2)
// ...
```

***

### 文字列操作

#### 基本操作

```cpp
int64_t strlen(const std::string& s);  // 長さ
std::string strmid(const std::string& s, int64_t start, int64_t length);  // 部分文字列
int64_t instr(const std::string& s, int64_t start, const std::string& search);  // 検索
int64_t strrep(std::string& s, const std::string& search, const std::string& replace);  // 置換
std::string strtrim(const std::string& s, int mode = 0, int char_code = 32);  // トリム
std::vector<std::string> split(const std::string& s, const std::string& delimiter);  // 分割
```

#### 型変換

```cpp
int toInt(double value);
int toInt(const std::string& s);
double toDouble(int value);
double toDouble(const std::string& s);
std::string str(int value);
std::string str(double value);
```

#### 書式付き文字列

```cpp
std::string strf(const std::string& format, ...);
// HSP互換のprintf風書式
// %d: 整数, %f: 実数, %s: 文字列, %x: 16進数
```

#### パス操作

```cpp
std::string getpath(const std::string& path, int type);
// type: 0=フルパス, 1=ディレクトリ名なし, 2=拡張子なし, 8=小文字変換, 16=ディレクトリのみ, 32=拡張子のみ
```

#### 文字コード変換

```cpp
std::u16string cnvstow(const std::string& utf8);  // UTF-8 → UTF-16
std::string cnvwtos(const std::u16string& utf16);  // UTF-16 → UTF-8
std::string cnvstoa(const std::string& utf8);  // UTF-8 → ShiftJIS
std::string cnvatos(const std::string& sjis);  // ShiftJIS → UTF-8
```

#### NotePad クラス（OOP版メモリノートパッド）

```cpp
class NotePad {
    size_t count() const;  // 行数
    size_t size() const;   // バイト数
    std::string get(size_t index) const;  // 行取得
    NotePad& add(std::string_view text, int index = -1, int overwrite = 0);  // 追加
    NotePad& del(size_t index);  // 削除
    NotePad& clear();  // クリア
    int find(std::string_view search, int mode = 0, size_t start = 0) const;  // 検索
    NotePad& load(std::string_view filename, size_t maxSize = 0);  // ロード
    bool save(std::string_view filename) const;  // セーブ
};
```

#### メモリノートパッド命令（HSP互換）

```cpp
void notesel(std::string& buffer);  // バッファ選択
void noteunsel();  // バッファ解除
void noteadd(std::string_view text, OptInt index = {}, OptInt overwrite = {});
void notedel(int index);
void noteget(std::string& dest, OptInt index = {});
void noteload(std::string_view filename, OptInt maxSize = {});
void notesave(std::string_view filename);
int notefind(std::string_view search, OptInt mode = {});
int noteinfo(int type);  // type: notemax(0)=行数, notesize(1)=バイト数
```

***

### ファイル操作

#### ファイル操作

```cpp
int64_t exist(const std::string& filename);  // サイズ取得（-1=存在しない）
void chdir(const std::string& dirname);  // ディレクトリ移動
void mkdir(const std::string& dirname);  // ディレクトリ作成
void deletefile(const std::string& filename);  // ファイル削除
void bcopy(const std::string& src, const std::string& dest);  // コピー

int64_t bload(const std::string& filename, std::string& buffer, OptInt64 size = {}, OptInt64 offset = {});
int64_t bload(const std::string& filename, std::vector<uint8_t>& buffer, OptInt64 size = {}, OptInt64 offset = {});
int64_t bsave(const std::string& filename, const std::string& buffer, OptInt64 size = {}, OptInt64 offset = {});
int64_t bsave(const std::string& filename, const std::vector<uint8_t>& buffer, OptInt64 size = {}, OptInt64 offset = {});

std::vector<std::string> dirlist(const std::string& filemask, OptInt mode = {});
```

#### ディレクトリ情報

```cpp
std::string dirinfo(int type);
// type: 0=カレント, 1=exe, 2=Windows, 3=System, 4=コマンドライン

// 便利関数
std::string dir_cur();      // カレントディレクトリ
std::string dir_exe();      // 実行ファイルのディレクトリ
std::string dir_win();      // Windowsディレクトリ
std::string dir_sys();      // Systemディレクトリ
std::string dir_cmdline();  // コマンドライン
std::string dir_desktop();  // デスクトップ
std::string dir_mydoc();    // マイドキュメント
```

#### exec

```cpp
int exec(const std::string& filename, OptInt mode = {}, const std::string& command = "");
// mode: exec_normal(0), exec_minimized(2), exec_shellexec(16), exec_print(32)
```

#### dialog

```cpp
DialogResult dialog(const std::string& message, OptInt type = {}, const std::string& option = "");
// type: dialog_info(0), dialog_warning(1), dialog_yesno(2), dialog_open(16), dialog_save(17), dialog_color(32)
```

***

### GUIオブジェクト

#### オブジェクト設定

```cpp
void objsize(OptInt sizeX = {}, OptInt sizeY = {}, OptInt spaceY = {});
void objmode(OptInt mode = {}, OptInt tabMove = {});
// mode: objmode_normal(0), objmode_guifont(1), objmode_usefont(2), objmode_usecolor(4)
void objcolor(OptInt r = {}, OptInt g = {}, OptInt b = {});
```

#### button

```cpp
// ラムダ式でコールバックを指定
int button(std::string_view name, std::function<int()> callback);

// 使用例
button("Click Me", []() {
    mes("Clicked!");
});
```

#### input / mesbox

```cpp
// ⚠️ 必ず shared_ptr を使用（ライフタイム安全性のため）
int input(std::shared_ptr<std::string> var, OptInt sizeX = {}, OptInt sizeY = {}, OptInt maxLen = {});
int mesbox(std::shared_ptr<std::string> var, OptInt sizeX = {}, OptInt sizeY = {}, OptInt style = {}, OptInt maxLen = {});

// 使用例
auto text = std::make_shared<std::string>("初期値");
input(text, 200, 24);
// 後で値を取得
mes(*text);
```

#### chkbox / combox / listbox

```cpp
// ⚠️ 必ず shared_ptr を使用
int chkbox(std::string_view label, std::shared_ptr<int> var);
int combox(std::shared_ptr<int> var, OptInt expandY, std::string_view items);
int listbox(std::shared_ptr<int> var, OptInt expandY, std::string_view items);

// 使用例
auto selected = std::make_shared<int>(0);
combox(selected, 100, "Option A\nOption B\nOption C");
// 後で値を取得
mes(strf("Selected: %d", *selected));
```

#### オブジェクト操作

```cpp
void clrobj(OptInt startId = {}, OptInt endId = {});  // オブジェクト削除
void objprm(int objectId, std::string_view value);    // 内容変更（文字列）
void objprm(int objectId, int value);                 // 内容変更（整数）
void objenable(int objectId, OptInt enable = {});     // 有効/無効
void objsel(int objectId);                            // フォーカス設定
```

***

### 割り込み・エラー処理

#### 割り込みハンドラ

```cpp
// グローバル版
void onclick(InterruptHandler handler);
void onkey(InterruptHandler handler);
void oncmd(InterruptHandler handler, int messageId);

// OOP版（Screenごと）
win.onclick([](){ /* クリック処理 */ });
win.onkey([](){ /* キー処理 */ });

// InterruptHandler = std::function<void()>
```

#### stop

```cpp
void stop();  // 割り込み待機（hspMainを抜けても同等）
```

#### onerror

```cpp
void onerror(ErrorHandler handler);
void onerror();  // 解除

// ErrorHandler = std::function<void(const HspError&)>
// 戻り値: 0=継続, 非0=終了

// 使用例
onerror([](const HspError& e) {
    mes(strf("Error %d: %s", e.error_code(), e.message().c_str()));
    mes(strf("at %s:%d", e.file_name().c_str(), e.line_number()));
});
```

#### HspError クラス

```cpp
class HspError : public std::runtime_error {
    int error_code() const;
    int line_number() const;
    const std::string& file_name() const;
    const std::string& function_name() const;
    const std::string& message() const;
};
```

#### エラーコード定数

```cpp
ERR_NONE = 0;
ERR_SYNTAX = 1;
ERR_ILLEGAL_FUNCTION = 2;
ERR_OUT_OF_MEMORY = 4;
ERR_TYPE_MISMATCH = 5;
ERR_OUT_OF_ARRAY = 6;
ERR_OUT_OF_RANGE = 7;
ERR_DIVIDE_BY_ZERO = 8;
ERR_FILE_IO = 12;
ERR_WINDOW_INIT = 13;
// ...
```

***

### メディア

```cpp
void mmload(std::string_view filename, int id, OptInt flag = {});
void mmplay(int id, OptInt flag = {});
void mmstop(OptInt id = {});
void mmvol(int id, int volume);  // 音量 (0-1000)
void mmpan(int id, int pan);     // パン (-1000 to 1000)
```

***

## HSPからの移行ガイド

### 基本的な違い

| 項目 | HSP | HSPPP (C++) |
| --- | --- | ----------- |
| エントリポイント | なし（自動実行） | `void hspMain()` |
| 変数宣言 | 不要 | 必須 `int x = 0;` |
| 行末 | 改行 | セミコロン `;` |
| 文字列 | `"..."` or `'...'` | `"..."` のみ |
| コメント | `//` or `;` | `//` or `/* */` |
| ラベル | `*label` | 関数/ラムダ |
| goto/gosub | サポート | 非推奨（関数を使用） |

### 変数宣言

```hsp
; HSP
a = 10
b = 3.14
s = "Hello"
dim arr, 10
```

```cpp
// HSPPP
int a = 10;
double b = 3.14;
std::string s = "Hello";
std::vector<int> arr(10);
```

### 制御構文

```hsp
; HSP if
if a > 10 {
    mes "big"
} else {
    mes "small"
}

; HSP repeat
repeat 10
    mes cnt
loop
```

```cpp
// HSPPP if
if (a > 10) {
    mes("big");
} else {
    mes("small");
}

// HSPPP for
for (int cnt = 0; cnt < 10; cnt++) {
    mes(std::to_string(cnt));
}
```

### goto/gosub → 関数

```hsp
; HSP
gosub *draw
stop

*draw
    color 255, 0, 0
    boxf 0, 0, 100, 100
    return
```

```cpp
// HSPPP
void draw() {
    color(255, 0, 0);
    boxf(0, 0, 100, 100);
}

void hspMain() {
    screen(0, 640, 480);
    draw();  // 関数呼び出し
    return;
}
```

### button の gosub → ラムダ

```hsp
; HSP
button gosub "Click", *onclick
stop

*onclick
    mes "Clicked!"
    return
```

```cpp
// HSPPP
button("Click", []() {
    mes("Clicked!");
});
```

### GUI変数の注意（shared\_ptr必須）

```hsp
; HSP（問題なし）
chk = 0
chkbox "Enable", chk
```

```cpp
// HSPPP（shared_ptr必須）
auto chk = std::make_shared<int>(0);
chkbox("Enable", chk);

// 値の取得
if (*chk) {
    mes("Enabled");
}
```

> ⚠️ **なぜshared\_ptrが必要か**: HSPでは変数がグローバルなので問題ありませんが、C++ではローカル変数は関数を抜けると破棄されます。GUIコントロールが参照している変数が消えると、未定義動作（クラッシュ等）になります。`shared_ptr`は参照カウントで変数の寿命を管理し、この問題を防ぎます。

### 移行チェックリスト

* [ ] `void hspMain()` を定義したか
* [ ] 変数はすべて型を指定して宣言したか
* [ ] 行末に `;` を付けたか
* [ ] `goto`/`gosub` を関数に置き換えたか
* [ ] `chkbox`/`combox`/`listbox` は `shared_ptr` を使用しているか
* [ ] ローカル変数を GUI コールバックで使用していないか

***

## 実践的なサンプル

### シンプルなゲームループ

```cpp
import hsppp;
using namespace hsppp;

int x = 320, y = 240;

void hspMain() {
    screen(0, 640, 480);
    title("Simple Game");
    
    while (true) {
        redraw(0);
        color(255, 255, 255);
        cls();
        
        // プレイヤー描画
        color(255, 0, 0);
        circle(x - 20, y - 20, x + 20, y + 20, 1);
        
        redraw(1);
        
        // 入力処理
        int key = stick(15);  // 方向キーは押しっぱなしOK
        if (key & stick_left)  x -= 5;
        if (key & stick_right) x += 5;
        if (key & stick_up)    y -= 5;
        if (key & stick_down)  y += 5;
        
        // ESCで終了
        if (key & stick_esc) break;
        
        await(16);  // 約60fps
    }
    
    return;
}
```

### メソッドチェーンを活用した描画

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    auto win = screen({.width = 800, .height = 600, .title = "Method Chain Demo"});
    
    // メソッドチェーンで一気に描画
    win.color(100, 100, 200)
       .boxf()  // 背景
       .color(255, 255, 0)
       .font("Arial", 48, 1)
       .pos(200, 100)
       .mes("HSPPP Demo")
       .color(255, 255, 255)
       .font("MS Gothic", 16, 0)
       .pos(200, 200)
       .mes("メソッドチェーンで")
       .mes("連続して描画できます");
    
}
```

### GUIフォーム

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    screen(0, 400, 300);
    title("GUI Form");
    
    // 入力フィールド（shared_ptr必須）
    auto name = std::make_shared<std::string>("");
    auto selected = std::make_shared<int>(0);
    auto checked = std::make_shared<int>(0);
    
    color(0, 0, 0);
    pos(20, 20);
    mes("名前:");
    pos(80, 18);
    input(name, 200, 24);
    
    pos(20, 60);
    mes("性別:");
    pos(80, 58);
    combox(selected, 60, "男性\n女性\nその他");
    
    pos(20, 100);
    chkbox("メルマガを受け取る", checked);
    
    pos(20, 150);
    button("送信", [&]() {
        mes("=== 入力内容 ===");
        mes("名前: " + *name);
        mes("性別: " + str(*selected));
        mes("メルマガ: " + (*checked ? std::string("はい") : std::string("いいえ")));
    });
    
    return;
}
```

### 画像の読み込みと表示

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    screen(0, 640, 480);
    title("Image Demo");
    
    // OOP版: Celオブジェクトで管理
    Cel player = loadCel("player.png");
    if (!player) {
        mes("画像の読み込みに失敗しました");
        return 1;
    }
    
    player.divide(4, 4);  // 4x4分割
    
    int frame = 0;
    while (true) {
        redraw(0);
        cls(4);
        
        // アニメーション
        player.put(frame % 16, 100, 100);
        
        redraw(1);
        
        frame++;
        if (getkey(VK_ESCAPE)) break;
        await(100);
    }
    
    return 0;
}
```

### エラーハンドリング

```cpp
import hsppp;
using namespace hsppp;

void hspMain() {
    screen(0, 640, 480);
    
    // エラーハンドラを設定
    onerror([](const HspError& e) {
        color(255, 0, 0);
        mes("=== エラー発生 ===");
        mes(strf("コード: %d", e.error_code()));
        mes("メッセージ: " + e.message());
        mes(strf("場所: %s:%d", e.file_name().c_str(), e.line_number()));
    });
    
    // わざとエラーを発生させる
    button("エラーを発生させる", []() {
        color(-1, 0, 0);  // 不正な色値 → HspError
    });
}
```

***

## 内部アーキテクチャ

### エントリポイントの隠蔽

ユーザーは `main` / `WinMain` を記述しません。ライブラリ側がブートストラップを提供します。

```
起動フロー:
1. [System Boot] ライブラリ内の WinMain が起動
2. [Init] COM, Direct2D Factory, システムフォント等の初期化
3. [User Code] hspMain() をコール
4. [Persistence] hspMain終了後もメッセージループ継続（stopと同等）
```

### 描画システム（Surface Architecture）

すべての描画対象を「Surface」として抽象化し、IDマップで管理します。

```
HspSurface (基底クラス)
├── HspWindow (screen/bgscr) - HWND + SwapChain
└── HspBuffer (buffer) - BitmapRenderTarget

ID管理: std::map<int, std::shared_ptr<HspSurface>>
- gsel(id): current_surface を切り替え
- gcopy(id, ...): ポリモーフィズムで画像転送
```

### 描画パイプライン（保持モード）

DirectXのImmediate Modeではなく、HSPのCanvas挙動を再現しています。

```
1. [Offscreen First] 描画命令はバックバッファへ
2. [Redraw Command]
   - redraw(0): 描画バッチ開始
   - redraw(1): バックバッファ → スワップチェーン転送 + VSync
3. [Auto-Repaint] WM_PAINTでバックバッファを自動再転送
```

### Screen クラスの軽量ハンドル方式

`Screen` クラスは `shared_ptr<HspSurface>` を保持せず、ID のみを保持します。

```cpp
class Screen {
    int m_id;       // ウィンドウID
    bool m_valid;   // 有効フラグ
    // ...
};
```

これにより：

* モジュール境界の型問題を回避
* コピーコストを最小化（軽量コピー可能）
* HSPのウィンドウID概念と一致

***

## トラブルシューティング

### ビルドエラー

#### Q: `import hsppp;` でエラーになる

**A:** Visual Studio 2026 (VS 18) を使用していますか？VS 2022以前ではC++23 Modulesのサポートが不十分です。

#### Q: リンクエラーが発生する

**A:** プラットフォームが x64 になっているか確認してください。Win32 (x86) はサポートしていません。

### 実行時エラー

#### Q: ウィンドウが表示されない

**A:** `screen_hide` フラグが設定されていないか確認してください。また、`hspMain` 内でループせずにすぐ `return` していませんか？

#### Q: GUIコントロールをクリックするとクラッシュする

**A:** 変数に `shared_ptr` を使用していますか？ローカル変数をそのまま渡していると、関数を抜けた時点で破棄されます。

```cpp
// NG
void setup() {
    int chk = 0;
    chkbox("Enable", &chk);  // コンパイルエラーになるはず
}

// OK
auto chk = std::make_shared<int>(0);
chkbox("Enable", chk);
```

#### Q: 文字化けする

**A:** Hspppは UTF-8 を使用しています。ソースファイルが UTF-8 で保存されているか確認してください。Visual Studioでは「ファイル」→「名前を付けて保存」→「エンコード付きで保存」から設定できます。

### パフォーマンス

#### Q: 描画が遅い

**A:**

1. `redraw(0)` で描画開始、`redraw(1)` で画面更新をしていますか？
2. 毎フレーム大量の `mes` を呼んでいませんか？フォント切り替えはコストがかかります。

***

## ライセンスとリンク

### ライセンス

**Boost Software License 1.0**

非常に寛容なオープンソースライセンスです。商用利用、改変、再配布が自由にできます。著作権表示の保持のみが必要です。

### リンク

* **GitHub リポジトリ**: https://github.com/Velgail/HSPPP_Lib
* **HSP公式サイト**: https://hsp.tv/

### バージョン情報

```cpp
// プログラムからバージョンを取得
auto ver = hsppp::get_version();
mes(strf("HSPPP v%d.%d.%d", ver.major, ver.minor, ver.patch));
mes(strf("Build: %s / %s", ver.build_type, ver.platform));

// または簡易版
mes(hsppp::version());  // "0.1.0"
```

現在のバージョン: **0.1.0** (2026-01-02)

***

以上が **HSPPP** の完全ガイドです。HSPユーザーがC++の世界へスムーズに移行できることを願っています。
