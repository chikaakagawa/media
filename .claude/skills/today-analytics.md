# today-analytics

## 目的
公開した記事・投稿のパフォーマンス数値を outputs.csv に記録する。
手動入力ベース（noteとXのAPIは使わない）。

## outputs.csv のカラム
`date, atom_id, title, url, views_7d, likes, comments, notes`

- `date`: 公開日（YYYY-MM-DD）
- `views_7d`: 公開後7日間のビュー数
- `likes`: スキ / いいね数
- `comments`: コメント / リプライ数
- `notes`: 特記事項（バズった原因・炎上・キャンペーン施策など）

## 確認場所
| データ | 確認場所 |
|---|---|
| views_7d / likes / comments（note） | note管理画面 → 記事ページ |
| views_7d / likes / comments（X） | Xアナリティクス → 投稿詳細 |

## 実行手順
1. 数値を受け取る（または下記フォーマットで入力を促す）
2. outputs.csv に1行追記
3. 記録完了サマリーを返す

## 入力フォーマット（ユーザーへの確認テンプレ）
```
公開日:
atom_id:（不明な場合は記事タイトルで可）
title:
url:
views_7d:
likes:
comments:
notes:（任意）
```

## 出力
```
【記録完了】
「[title]」 / [date]
views_7d: N / likes: N / comments: N
→ outputs.csv に追記しました。
```
