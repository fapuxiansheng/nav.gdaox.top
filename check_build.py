#!/usr/bin/env python3
"""推广导航站构建产物自检（纯标准库、只读 public/，不联网）。

用法：python check_build.py
退出码：0 = 全绿；1 = 存在阻断项。
自动识别阶段一「空链版」与阶段二「正式版」，换链接后可反复复跑。
"""
from pathlib import Path
import re
import sys

PUB = Path(__file__).resolve().parent / "public"
DOMAIN = "https://nav.gdaox.top"
PLACEHOLDER = "REPLACE_WITH_RENTUIBANG_URL"
TOOLS = ["夸克网盘", "百度网盘", "迅雷网盘", "千问"]

rows = []


def chk(label, ok, note=""):
    rows.append((label, bool(ok), note))


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


idx = read(PUB / "index.html")
chk("index.html 已生成", bool(idx))
if not idx:
    print("BLOCK  未找到 public/index.html，请先跑 hugo --gc --minify --cleanDestinationDir")
    sys.exit(1)

for tool in TOOLS:
    chk("卡片 " + tool, tool in idx)
chk("广告标识", "广告｜推广链接" in idx)
chk("佣金声明", "不会增加你的费用" in idx)
chk("关于页入口", "关于本站" in idx)

canon = re.search(r'rel=["\']?canonical["\']?\s+href=["\']?([^"\'>\s]+)', idx)
chk("canonical 指向最终域名", bool(canon and canon.group(1).startswith(DOMAIN)),
    canon.group(1) if canon else "未找到 canonical")
chk("无 pages.dev 残留", "pages.dev" not in idx)
chk("无 /5ZY/ 子路径残留", "/5ZY/" not in idx)
chk("无本地绝对路径泄漏", not re.search(r"[A-Za-z]:[\\/]我的文档|Default Project", idx))

pending = idx.count("入口待开放")
anchors = re.findall(r"<a[^>]*tool-btn[^>]*>", idx)
if pending:
    chk("阶段一：4 个按钮全部禁用", pending == 4, "实际 %d" % pending)
    chk("阶段一：无占位符可点链接", PLACEHOLDER not in idx)
else:
    chk("阶段二：4 个可点按钮", len(anchors) == 4, "实际 %d" % len(anchors))
    for i, anchor in enumerate(anchors, 1):
        chk("阶段二：按钮 %d rel/target 合规" % i,
            "sponsored" in anchor and "nofollow" in anchor and "noopener" in anchor
            and "_blank" in anchor and PLACEHOLDER not in anchor)
    chk("阶段二：页面无占位符", PLACEHOLDER not in idx)

about = read(PUB / "about" / "index.html")
chk("about/index.html 已生成", bool(about))
chk("关于页含推广声明", "广告与推广声明" in about)

robots = read(PUB / "robots.txt")
chk("robots.txt 含 Sitemap 行", "Sitemap" in robots and DOMAIN in robots)

sitemap = read(PUB / "sitemap.xml")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
chk("sitemap 指向最终域名", bool(urls) and all(u.startswith(DOMAIN) for u in urls),
    "%d 条" % len(urls))

css_dir = PUB / "assets" / "css"
css_files = list(css_dir.glob("*.css")) if css_dir.is_dir() else []
chk("extended 卡片样式已注入", any(".tool-grid" in read(p) for p in css_files))

failed = [r for r in rows if not r[1]]
for label, ok, note in rows:
    print(("  OK   " if ok else " BLOCK ") + label + (("  | " + str(note)) if note else ""))

tax_urls = [u for u in urls if "/categories/" in u or "/tags/" in u]
if tax_urls:
    print("  WARN  sitemap 含 taxonomy 空页：%d 条（不影响功能，可择机清理）" % len(tax_urls))

print("\n阶段：%s；%d/%d 通过；阻断 %d 项" % (
    "空链版" if pending else "正式版", len(rows) - len(failed), len(rows), len(failed)))
sys.exit(1 if failed else 0)
