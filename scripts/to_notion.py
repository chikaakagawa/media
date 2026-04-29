#!/usr/bin/env python3
"""
to_notion.py  — ~/home/02_AI_Education/media/content/articles/ のMarkdownをNotionへ送信
Usage:
  python3 ~/home/02_AI_Education/media/scripts/to_notion.py <markdown_file> [--status 下書き] [--category 軸B] [--tag AI,自動化]
"""

import sys, os, re, json, argparse
from datetime import date
import urllib.request, urllib.error

TOKEN = os.environ.get("NOTION_TOKEN", "")
DB_ID = os.environ.get("NOTION_DB_ID", "e965ba3617004f35b17c8a890ca5adf1")
NOTION_VERSION = "2022-06-28"

# ── Markdown → Notion blocks ──────────────────────────────────────────────────

def text_obj(content: str) -> dict:
    return {"type": "text", "text": {"content": content[:2000]}}

def parse_inline(line: str) -> list:
    """太字・コードのインライン装飾を簡易パース"""
    parts = []
    # **bold**
    segments = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', line)
    for seg in segments:
        if seg.startswith('**') and seg.endswith('**'):
            parts.append({"type": "text", "text": {"content": seg[2:-2]},
                          "annotations": {"bold": True}})
        elif seg.startswith('`') and seg.endswith('`'):
            parts.append({"type": "text", "text": {"content": seg[1:-1]},
                          "annotations": {"code": True}})
        elif seg:
            parts.append(text_obj(seg))
    return parts or [text_obj(line)]

def md_to_blocks(md: str) -> list:
    blocks = []
    for line in md.splitlines():
        stripped = line.rstrip()
        if not stripped:
            continue
        if stripped.startswith('### '):
            blocks.append({"object":"block","type":"heading_3",
                "heading_3":{"rich_text":[text_obj(stripped[4:])]}})
        elif stripped.startswith('## '):
            blocks.append({"object":"block","type":"heading_2",
                "heading_2":{"rich_text":[text_obj(stripped[3:])]}})
        elif stripped.startswith('# '):
            blocks.append({"object":"block","type":"heading_1",
                "heading_1":{"rich_text":[text_obj(stripped[2:])]}})
        elif re.match(r'^[-*] ', stripped):
            blocks.append({"object":"block","type":"bulleted_list_item",
                "bulleted_list_item":{"rich_text":parse_inline(stripped[2:])}})
        elif re.match(r'^\d+\. ', stripped):
            content = re.sub(r'^\d+\. ', '', stripped)
            blocks.append({"object":"block","type":"numbered_list_item",
                "numbered_list_item":{"rich_text":parse_inline(content)}})
        elif stripped.startswith('> '):
            blocks.append({"object":"block","type":"quote",
                "quote":{"rich_text":[text_obj(stripped[2:])]}})
        elif stripped.startswith('---'):
            blocks.append({"object":"block","type":"divider","divider":{}})
        else:
            blocks.append({"object":"block","type":"paragraph",
                "paragraph":{"rich_text":parse_inline(stripped)}})
    return blocks

# ── Notion API ────────────────────────────────────────────────────────────────

def notion_request(method: str, path: str, body: dict = None):
    url = f"https://api.notion.com/v1{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Notion-Version", NOTION_VERSION)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        sys.exit(1)

def create_page(title: str, status: str, category: str, tags: list, blocks_first: list) -> str:
    properties = {
        "タイトル": {"title": [{"text": {"content": title}}]},
        "ステータス": {"status": {"name": status}},
    }
    if category:
        properties["カテゴリ"] = {"select": {"name": category}}
    if tags:
        properties["タグ"] = {"multi_select": [{"name": t} for t in tags]}
    properties["公開先"] = {"select": {"name": "note"}}

    body = {
        "parent": {"database_id": DB_ID},
        "properties": properties,
        "children": blocks_first[:100],
    }
    res = notion_request("POST", "/pages", body)
    return res["id"]

def append_blocks(page_id: str, blocks: list):
    for i in range(0, len(blocks), 100):
        notion_request("PATCH", f"/blocks/{page_id}/children",
                       {"children": blocks[i:i+100]})

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--status", default="下書き")
    parser.add_argument("--category", default="")
    parser.add_argument("--tag", default="")
    args = parser.parse_args()

    path = os.path.expanduser(args.file)
    if not os.path.exists(path):
        print(f"ファイルが見つかりません: {path}")
        sys.exit(1)

    md = open(path).read()

    # タイトル抽出（最初の # 行 or ファイル名）
    title_match = re.search(r'^# (.+)', md, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.splitext(os.path.basename(path))[0]

    # # 行はブロックから除外（ページタイトルに使うため）
    body_md = re.sub(r'^# .+\n?', '', md, count=1)

    blocks = md_to_blocks(body_md)
    tags = [t.strip() for t in args.tag.split(',')] if args.tag else []

    print(f"送信中: {title} ({len(blocks)} blocks)")
    page_id = create_page(title, args.status, args.category, tags, blocks[:100])
    if len(blocks) > 100:
        append_blocks(page_id, blocks[100:])

    print(f"完了: https://www.notion.so/{page_id.replace('-', '')}")

if __name__ == "__main__":
    main()
