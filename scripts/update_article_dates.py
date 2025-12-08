#!/usr/bin/env python3
"""
HSP-Knowledge 記事のdateフィールド自動更新スクリプト

/publish コマンド実行時に、bot名義で記事のdateフィールドを自動設定します。

ロジック：
- 新記事（dateフィールドなし）: date フィールドを設定
- 既存記事（date フィールドあり）: date は保持し、lastupdate フィールドを更新
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple
import yaml


class ArticleDateUpdater:
    """記事のdateフィールドを更新するクラス"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.is_new_article = False

    def update(self) -> Dict:
        """記事のdateフィールドを更新"""
        result = {
            "success": False,
            "file": str(self.file_path),
            "is_new_article": False,
            "message": "",
            "old_date": None,
            "new_date": None,
            "old_lastupdate": None,
            "new_lastupdate": None
        }

        try:
            # ファイル読み込み
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            result["message"] = f"ファイル読み込みエラー: {str(e)}"
            return result

        # Front Matterを解析
        front_matter, body = self._parse_markdown()
        if front_matter is None:
            result["message"] = "Front Matterが見つかりません"
            return result

        # 現在の日時を取得（JST: UTC+9）
        jst = timezone(timedelta(hours=9))
        now = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S %z")
        # フォーマット調整: "+0900" を "+9:00" に（YAMLで標準的な形式）
        now = now[:-2] + ":" + now[-2:]

        # 古いdateを記録
        if 'date' in front_matter:
            result["old_date"] = front_matter['date']
            self.is_new_article = False
        else:
            # dateフィールドがない = 新記事
            self.is_new_article = True

        # 古いlastupdateを記録
        if 'lastupdate' in front_matter:
            result["old_lastupdate"] = front_matter['lastupdate']

        # 新記事 or 既存記事の処理
        if self.is_new_article:
            # 新記事: dateを設定
            front_matter['date'] = now
            result["new_date"] = now
            result["is_new_article"] = True
        else:
            # 既存記事: dateは保持、lastupdateのみ更新
            pass

        # lastupdateは常に更新（新記事・既存記事問わず）
        front_matter['lastupdate'] = now
        result["new_lastupdate"] = now

        # Front Matterを再構築
        new_content = self._rebuild_markdown(front_matter, body)
        if new_content is None:
            result["message"] = "Front Matter再構築エラー"
            return result

        # ファイルに書き込み
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            result["success"] = True
            if self.is_new_article:
                result["message"] = "新記事: date を設定、lastupdate を作成"
            else:
                result["message"] = "既存記事: lastupdate を更新"
        except Exception as e:
            result["message"] = f"ファイル書き込みエラー: {str(e)}"
            return result

        return result

    def _parse_markdown(self) -> Tuple[Optional[Dict], str]:
        """Markdownファイルを解析してFront Matterと本文に分離"""
        front_matter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(front_matter_pattern, self.content, re.DOTALL)

        if not match:
            return None, self.content

        try:
            front_matter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return front_matter, body
        except yaml.YAMLError as e:
            return None, match.group(2) if match else self.content

    def _rebuild_markdown(self, front_matter: Dict, body: str) -> Optional[str]:
        """Front Matterと本文を再構築"""
        try:
            # Front Matterを YAML に変換
            fm_yaml = yaml.dump(
                front_matter,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False
            )
            # 末尾の改行を削除
            fm_yaml = fm_yaml.rstrip('\n')
            return f"---\n{fm_yaml}\n---\n{body}"
        except Exception:
            return None


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("Usage: python update_article_dates.py <file_path> [file_path2] ...")
        sys.exit(1)

    all_results = []
    has_error = False

    for file_path in sys.argv[1:]:
        updater = ArticleDateUpdater(file_path)
        result = updater.update()
        all_results.append(result)

        if not result["success"]:
            has_error = True

    # 結果を JSON で出力
    print(json.dumps(all_results, ensure_ascii=False, indent=2))

    # 終了コード
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
