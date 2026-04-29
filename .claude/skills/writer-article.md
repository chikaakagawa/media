# writer-article

## 目的
pipeline.csv の priority=1 のネタから note 初稿を生成する。

## 前提
- CLAUDE.md の文体ルール・読者定義・NGワードを必ず参照する
- 読者: フリーランスデザイナー／クリエイター

## 記事構成テンプレ
1. リード文（2-3行）: 「今日これを読むと何が分かるか」を端的に
2. H2 何が起きたか（事実を1段落で）
3. H2 なぜデザイナーに関係あるか（現場視点）
4. H2 明日からできる一歩（具体アクション3つ）
5. H2 私（ciro）の視点（主観）
6. 締め／CTA

## 制約
- 1,500〜2,500字
- 見出しは H2 中心
- 数値・日付・固有名詞に出典リンク必須
- タイトル32字以内

## 保存先
`~/home/02_AI_Education/media/content/articles/YYYYMMDD_[atom_id].md`

## 保存後の自動処理
以下を必ず実行する：
```
python3 ~/home/02_AI_Education/media/scripts/to_notion.py \
  ~/home/02_AI_Education/media/content/articles/YYYYMMDD_[atom_id].md \
  --status 下書き --category 軸B
```
完了後、`/post-social` スキルに従い X・Threads の投稿文を各1案生成して出力する。
ターゲットの痛みに刺さる最良案のみ。
