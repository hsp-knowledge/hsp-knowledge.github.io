# HSP-Knowledge

**HSP (Hot Soup Processor) ユーザーのための、みんなで作るナレッジ共有サイト**

[🚀 サイトを見る](https://velgail.github.io/HSP-Knowledge/)

このプロジェクトは、Qiitaのような技術情報共有サービスを、GitHub Pages と Jekyll を用いてサーバー費用ゼロ・メンテナンスフリーで実現する実験的な試みです。
誰でも Markdown で記事を書いて Pull Request を送ることで、知識を共有できます。

## ✨ 特徴

- **Qiita風のモダンなデザイン**: 読みやすい記事レイアウト、タグ機能、検索機能を備えています。
- **HSP特化**: HSP3向けのシンタックスハイライトに対応しています。
- **維持費ゼロ**: GitHub Pages でホスティングされているため、サーバー代や管理の手間がかかりません。
- **🤖 自動レビュー & 承認システム**: Gemini Code Assist と GitHub Actions が投稿を自動的に検証。管理者が寝ていても、適切な記事なら自動でマージ・公開されます。

## 📝 記事を投稿する方法

GitHub アカウントがあれば誰でも投稿可能です。

1. **記事を作成**
   `_posts/` フォルダに `YYYY-MM-DD-タイトル.md` という形式でファイルを作成します。
   （テンプレート: `_posts/template.md`）

2. **Pull Request (PR) を送信**
   変更をコミットして PR を作成すると、自動検証システムが以下のチェックを行います。
   - ファイル名と Front Matter の形式チェック
   - 既存記事の更新権限チェック
   - AI (Gemini) によるスパム・品質判定

3. **自動マージ**
   検証に合格（✅）したら、PRのコメント欄に `/publish` と入力してください。
   自動的にマージされ、サイトに公開されます。

詳しくは [記事の投稿方法](https://hsp-knowledge.github.io/2000/01/01/how-to-post.html) を参照してください。

## 🛠️ システム構成

- **フレームワーク**: Jekyll
- **ホスティング**: GitHub Pages
- **CI/CD**: GitHub Actions
- **AIレビュー**: Gemini Code Assist

自動レビューシステムの詳細は [docs/AUTO_REVIEW_SYSTEM.md](docs/AUTO_REVIEW_SYSTEM.md) をご覧ください。

## 📜 ライセンス

本サイトのコンテンツは以下のライセンスで提供されます（詳細は [LICENSE](LICENSE) を参照）。

- **記事本文**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (クリエイティブ・コモンズ 表示 4.0)
- **コードスニペット**: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (パブリックドメイン)

---
*Happy Hacking with HSP!*
