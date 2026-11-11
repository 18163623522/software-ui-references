#!/usr/bin/env python3
"""从 ignoredone.space 设计导航页同步资源数据。

该页面的条目由前端 JS 动态渲染，常规抓取只能看到分类标签。
完整数据内嵌在 WordPress 渲染后的 HTML 里（一个 JSON 数组），
因此走 WP REST API 取渲染结果，再正则提取内嵌数组。

同步内容：
  data/sites.json   原始数据，全字段原样保存
  assets/icons/     每条资源的图标镜像
  CATALOG.md        按分类的完整清单（自动生成，勿手改）

用法: python scripts/fetch.py [--skip-icons]
"""

import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

API = "https://www.ignoredone.space/index.php/wp-json/wp/v2/pages/4730"
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ICONS = ROOT / "assets" / "icons"

# JSON categories 键 -> 站点页面上的分类名（按站内条目数降序）
CATEGORY_NAMES = {
    "tool": "设计工具",
    "font": "字体资源",
    "inspiration": "灵感收集",
    "illustration": "图片素材",
    "resource": "设计资源",
    "ui": "UI 参考",
    "mockup": "样机素材",
}


def fetch_sites():
    req = urllib.request.Request(API, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    # 只在 content.rendered 内搜索：整个 JSON 响应的 _links 字段里
    # 也有 [{"name":...}] 结构，会抢先命中正则
    rendered = json.loads(resp)["content"]["rendered"]
    m = re.search(r'\[\{"name".*?\}\]', rendered, re.S)
    if not m:
        sys.exit("未找到内嵌数据数组，页面结构可能已变化")
    return json.loads(m.group(0))


def slugify(name, i):
    s = re.sub(r"[^0-9A-Za-z]+", "-", name).strip("-").lower()
    return f"{i:02d}-{s or 'site'}"


def download(url, dest):
    if dest.exists():
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        dest.write_bytes(urllib.request.urlopen(req, timeout=30).read())
        return True
    except Exception as e:
        print(f"  [warn] {url}: {e}")
        return False


def gen_catalog(sites):
    lines = [
        "# 完整清单",
        "",
        f"> 由 `scripts/fetch.py` 自动生成，勿手改。共 {len(sites)} 条，"
        f"同步自 [ignoredone.space 设计导航](https://www.ignoredone.space/index.php/designwebsite/)。",
        "",
    ]
    first_seen = {}  # url -> 首次出现的条目名，用于标注重复条目
    for key, label in CATEGORY_NAMES.items():
        items = [s for s in sites if key in s.get("categories", [])]
        lines += [f"## {label}（{len(items)} 条）", "", "| 名称 | 说明 | 备注 |", "|---|---|---|"]
        for s in items:
            notes = []
            if s.get("broken"):
                notes.append("站方标记失效")
            if s["url"] in first_seen:
                notes.append(f"与「{first_seen[s['url']]}」同址")
            else:
                first_seen[s["url"]] = s["name"]
            sub = s.get("subtitle", "")
            lines.append(f"| [{s['name']}]({s['url']}) | {sub} | {'；'.join(notes)} |")
        lines.append("")
    (ROOT / "CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    skip_icons = "--skip-icons" in sys.argv
    sites = fetch_sites()
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "sites.json").write_text(
        json.dumps(sites, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"sites.json: {len(sites)} 条")

    gen_catalog(sites)
    print("CATALOG.md: 已生成")

    if not skip_icons:
        ICONS.mkdir(parents=True, exist_ok=True)
        ok = 0
        for i, s in enumerate(sites):
            icon = s.get("icon")
            if not icon:
                continue
            ext = Path(urlparse(icon).path).suffix or ".svg"
            if download(icon, ICONS / f"{slugify(s['name'], i)}{ext}"):
                ok += 1
        print(f"icons: {ok}/{sum(1 for s in sites if s.get('icon'))} 个已就位")


if __name__ == "__main__":
    main()
