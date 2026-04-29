# pipeline

## 目的
atoms.csv の status=new を、note記事／X投稿／両方／スキップに仕分ける。

## 判定基準
- note: 文脈・解釈・実装Tipsを1,500字以上で展開できるネタ（score 5 優先）
- x: 速報性重視・1スレッドで完結するネタ（score 3-4）
- note+x: インパクト大。noteで深掘り→Xで要約リンク
- skip: 既出／冗長／ciroの読者に届かないネタ

## 優先度
1 = 今日書く
2 = 明日
3 = キュー保留（3日以内）

## 処理後
- atoms.csv の status を `routed` に更新
- pipeline.csv に1行追記
