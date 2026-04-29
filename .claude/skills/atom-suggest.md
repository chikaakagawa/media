# atom-suggest

## 目的
直近7日間の queued 件数が 3 本未満になったら自動発動。
WebSearch で最新AIニュースをリサーチし、atoms.csv と pipeline.csv を補充する。

## トリガー条件
pipeline.csv の planned_date が今日〜7日後 かつ status=queued の行が 3 本未満

## リサーチ軸（毎回必ずこの3軸を検索）
1. `AI freelance designer news [今週の日付]` — 海外の最新動向
2. `フリーランス デザイナー AI 最新 [今月年月]` — 国内動向・調査データ
3. `AI design tool update [今週の日付]` — ツール・プロダクト情報

## atom 評価基準
| スコア | 条件 |
|---|---|
| 5 | ターゲットの痛みに直撃 or 日本のリアルデータ |
| 4 | 有力な反証・インサイト・信頼できる調査 |
| 3 | 話題性あるが読者への接続が弱い |

スコア 3 以下は原則 skip ルートへ。

## route 判定
- note+x+threads: 1,500字以上で展開できる・インサイト系・シリーズ化可能
- x+threads: 速報・データ単発・1スレッドで完結
- note: エバーグリーン・深掘り必須

## atom_id 採番ルール
`a[YYYYMMDD]-[連番2桁]` または `i[YYYYMMDD]-[連番2桁]`（iはインサイト系）

## 処理フロー
1. pipeline.csv の残数チェック
2. 残数 < 3 なら WebSearch で3軸リサーチ
3. 新atom を score 4 以上のもの 3〜5 件抽出
4. atoms.csv に追記（status=routed）
5. pipeline.csv に追記（planned_date は既存の最後の日付+2〜3日）
6. 追加したatomの一覧を出力
