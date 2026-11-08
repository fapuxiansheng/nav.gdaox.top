#!/usr/bin/env python3
"""推广导航站（团队邀请主题）构建产物自检（纯标准库、只读 public/ 与 data/，不联网）。

用法：python check_build.py
退出码：0 = 全绿；1 = 存在阻断项。
自动识别阶段一「空链版」与阶段二「正式版」，回填专属邀请链接后可反复复跑。
阶段二额外校验：主按钮域名在专属邀请域白名单、URL 邀请码与 data/invite.yaml
的 cta.code 一致、页面展示的邀请码与 data 一致（防误填官方 SEO 码 / 换码漏改）。

按总纲 #26（2026-11-08）：4 篇项目介绍配套稿挂载为 /projects/ 正式栏目，
新增首页入链、栏目列表页、4 篇文章页、sitemap 条数与文章页 CTA 校验。
按总纲 #27（2026-11-08）：栏目稿改为简版（正文约 600–800 字），重心为「加入团队 →
下载 App → 熟悉规则」；CTA 由页尾前置到正文开头；不再引用官网宣传数字
（#24/#26 放宽保留但闲置），改校验三步引导、无官网数字、无第三方下载入口。
按总纲 #28（2026-11-08）：栏目由 4 篇扩为 10 篇，文章页、列表页入链与 sitemap
断言同步改为 10 篇与 13 条；合规红线与真源校验强度不降低。
按总纲 #29（2026-11-08，现行）：10 篇换「简洁版」——三步编号改「一、二、三」，
删参考阅读区、官网链接与核验日期；文章页新增断言：正文无站外链接、正文仅
1 个邀请 URL 文本、无官网项目页链接与旧结构残留。合规红线一字未松。
口径分工：首页／关于页／栏目列表页按 #22/#23 加严（不写收益数字、不列诱导词）；
链接与邀请码只以 data/invite.yaml 为唯一真源，任何页面换码漏改均被阻断。
"""
from pathlib import Path
import html
import re
import sys
from urllib.parse import urlparse

PUB = Path(__file__).resolve().parent / "public"
DATA = Path(__file__).resolve().parent / "data" / "invite.yaml"
DOMAIN = "https://nav.gdaox.top"
PLACEHOLDER = "REPLACE_WITH_INVITE_URL"
# 景行后台【团队 → 我的团队】生成的专属邀请链接域名；官方 SEO 投放链接
# 用的是 dt.bd.cn + 66666600，不在白名单内。换域名须同步改这里与 data。
ALLOWED_HOSTS = ("tg.bd.cn",)
SECTIONS = ["任推邦是什么", "团队邀请是做什么", "适合谁", "加入前先确认"]

# 团队邀请主题的对外文案红线：不得出现补贴比例、收益数字与诱导性收益话术。
# 任推邦官方 /team/ 页含 3%/5% 补贴说明，但对外落地页列比例即构成收益诱导；
# 且 2025-02 公开报道对该「发展下线按业绩计酬」模式存在合规质疑，故机检从严。
BANNED = [
    "3%", "5%", "躺赚", "躺赢", "被动收入", "管道收入", "睡后收入",
    "日入", "月入", "保底", "包赚", "稳赚", "轻松赚", "零成本",
    "持续受益", "下级越多", "发展下线", "加盟费",
]

rows = []


def chk(label, ok, note=""):
    rows.append((label, bool(ok), note))


def read(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def data_scalar(text, key):
    """从 data/invite.yaml 取简单字符串标量；纯标准库，不引入 YAML 依赖。"""
    m = re.search(r"(?m)^\s*" + re.escape(key) + r':\s*"([^"]+)"', text)
    return m.group(1) if m else ""


invite_data = read(DATA)
expected_code = data_scalar(invite_data, "code")
expected_url = data_scalar(invite_data, "url")

idx = read(PUB / "index.html")
chk("index.html 已生成", bool(idx))
if not idx:
    print("BLOCK  未找到 public/index.html，请先跑 rm -rf public && hugo --gc --minify")
    sys.exit(1)

for section in SECTIONS:
    chk("说明卡片 " + section, section in idx)
chk("广告标识", "广告｜推广链接" in idx)
chk("推广合作信息定性", "推广合作信息" in idx)
chk("非招聘声明", "非招聘" in idx)
chk("非收益承诺", "不构成任何收益承诺" in idx)
chk("不增加费用声明", "不会增加你的费用" in idx)
chk("不收费声明", "不收取任何费用" in idx)
chk("关于页入口", "关于本站" in idx)

canon = re.search(r'rel=["\']?canonical["\']?\s+href=["\']?([^"\'>\s]+)', idx)
chk("canonical 指向最终域名", bool(canon and canon.group(1).startswith(DOMAIN)),
    canon.group(1) if canon else "未找到 canonical")
chk("无 pages.dev 残留", "pages.dev" not in idx)
chk("无 /5ZY/ 子路径残留", "/5ZY/" not in idx)
chk("无本地绝对路径泄漏", not re.search(r"[A-Za-z]:[\\/]我的文档|Default Project", idx))

# 归因硬伤：绝不能把任推邦官网 /team/ 页的官方 SEO 邀请码写进本站，
# 否则注册关系归官方、本站拿不到任何团队邀请补贴。
chk("无官方 SEO 邀请码 66666600", "66666600" not in idx and "seo_rtb" not in idx)
chk("无官方 team 页邀请链接", "rentuiapp.com/team/" not in idx)

hits = [w for w in BANNED if w in idx]
chk("首页无补贴比例与收益诱导词", not hits, "命中：" + "、".join(hits) if hits else "")

pending = idx.count("入口待开放")
anchors = re.findall(r"<a[^>]*invite-btn[^>]*>", idx)
if pending:
    chk("阶段一：主按钮禁用", pending == 1, "实际 %d" % pending)
    chk("阶段一：无可点邀请链接", not anchors)
    chk("阶段一：页面无占位符", PLACEHOLDER not in idx)
else:
    chk("阶段二：1 个可点邀请按钮", len(anchors) == 1, "实际 %d" % len(anchors))
    chk("阶段二：data 邀请码有效且非官方码",
        bool(re.fullmatch(r"\d{6,10}", expected_code)) and expected_code != "66666600",
        expected_code or "data 未取到 code")
    for i, anchor in enumerate(anchors, 1):
        chk("阶段二：按钮 %d rel/target 合规" % i,
            "sponsored" in anchor and "nofollow" in anchor and "noopener" in anchor
            and "_blank" in anchor and PLACEHOLDER not in anchor)
        # Hugo --minify 输出无引号属性且会把 & 转义成 &amp;，先还原来取真实 URL。
        plain = html.unescape(anchor)
        href = re.search(r"href=[\"']?([^\"'\s>]+)", plain)
        href_val = href.group(1) if href else ""
        host = urlparse(href_val).hostname or ""
        chk("阶段二：按钮 %d 域名为专属邀请域" % i, host in ALLOWED_HOSTS,
            host or "未取到 href")
        chk("阶段二：按钮 %d 邀请码与 data 一致" % i,
            bool(expected_code) and ("invite_code=" + expected_code) in href_val,
            href_val or "未取到 href")
    chk("阶段二：页面展示邀请码与 data 一致",
        bool(expected_code) and "本站专属邀请码：" in idx
        and ("<strong>" + expected_code + "</strong>") in idx,
        expected_code or "data 未取到 code")
    chk("阶段二：data 链接与按钮一致",
        bool(expected_url) and expected_url in html.unescape(idx))
    chk("阶段二：页面无占位符", PLACEHOLDER not in idx)

about = read(PUB / "about" / "index.html")
chk("about/index.html 已生成", bool(about))
chk("关于页含非官方声明", "非官方声明" in about)
chk("关于页含广告与推广声明", "广告与推广声明" in about)
chk("关于页含合作性质边界", "不是招聘" in about)
about_hits = [w for w in BANNED if w in about]
chk("关于页无补贴比例与收益诱导词", not about_hits,
    "命中：" + "、".join(about_hits) if about_hits else "")

# --- 项目介绍栏目（总纲 #26 挂载为正式栏目 / #28 扩为 10 篇）---
PROJ_DIR = PUB / "projects"
PROJ_PAGES = sorted(PROJ_DIR.glob("*/index.html")) if PROJ_DIR.is_dir() else []
proj_list = read(PROJ_DIR / "index.html")

# Hugo --minify 输出无引号属性，须兼容 href=/projects/ 与 href="/projects/" 两种写法。
chk("首页含 /projects/ 栏目入链",
    bool(re.search(r'href=["\']?/projects/["\']?', idx)))
chk("栏目列表页已生成", bool(proj_list))
chk("10 篇文章页已生成（#28）", len(PROJ_PAGES) == 10, "实际 %d" % len(PROJ_PAGES))

list_hits = [w for w in BANNED if w in proj_list]
chk("列表页无补贴比例与收益诱导词", not list_hits,
    "命中：" + "、".join(list_hits) if list_hits else "")
chk("列表页不列收益数字（#22/#23 加严）",
    "￥" not in proj_list and "单笔最高收益" not in proj_list)
chk("列表页含推广标识与合规定性",
    all(x in proj_list for x in ("广告｜推广链接", "推广合作信息", "非招聘", "非收益承诺")))
list_slugs = sorted(set(re.findall(r"/projects/([a-z0-9-]+)/", proj_list)))
chk("列表页收录 10 篇文章入链（#28）", len(list_slugs) == 10, "实际 %s" % list_slugs)
# Hugo --minify 输出属性不带引号，须兼容 class=project-card 与 class="project-card"。
chk("列表页渲染 10 篇文章卡片（#28）",
    len(re.findall(r"class=[\"']?project-card[\"']?", proj_list)) == 10)
chk("列表页有 1 个可点团队邀请按钮",
    len(re.findall(r"<a[^>]*invite-btn[^>]*>", proj_list)) == 1)
chk("列表页含先加入团队/下载 App 引导（#27）",
    all(x in proj_list for x in ("加入团队", "下载 App")))
chk("列表页不挂官网下载入口（#27）",
    not any(x in proj_list for x in ("rentuiapp.com/app", "rentuibang.top")))
chk("列表页不挂官网项目页链接（#29）", "rentuiapp.com/xiangmu/" not in proj_list)

for page in PROJ_PAGES:
    name = page.parent.name
    s = read(page)
    chk(name + "：广告标识与合规定性",
        all(x in s for x in ("广告｜推广链接", "推广合作信息", "非招聘", "非收益承诺")))
    chk(name + "：简版不引用官网宣传数字（#27）",
        not any(x in s for x in ("￥", "单笔最高收益", "每单可赚", "正在推广人数")))
    chk(name + "：三步引导齐全且顺序正确（#29：一、二、三）",
        all(x in s for x in ("加入团队", "下载 App", "熟悉规则", "一、", "二、", "三、"))
        and s.find("一、") < s.find("二、") < s.find("三、"))
    chk(name + "：CTA 已前置到正文之前（#27）",
        "invite-cta" in s and "project-content" in s
        and s.find("invite-cta") < s.find("project-content"))
    chk(name + "：无官网下载/注册入口与官方投放域",
        not any(x in s for x in ("rentuiapp.com/app", "rentuibang.top",
                                 "dt.bd.cn", "66666600", "seo_rtb")))
    # #29：只留一个邀请链接，正文不附官网／参考／任何站外链接。
    chk(name + "：无官网项目页链接与参考阅读区（#29）",
        not any(x in s for x in ("rentuiapp.com/xiangmu/", "参考阅读", "核验日期")))
    pc = re.search(r'<article class=["\']?project-content["\']?>(.*?)</article>', s, re.S)
    pc_body = html.unescape(pc.group(1)) if pc else ""
    chk(name + "：正文无站外链接（#29）",
        bool(pc) and not re.search(r'<a[^>]+href=["\']?https?://', pc_body))
    chk(name + "：正文仅含 1 个邀请 URL 文本（#29）",
        bool(expected_url) and pc_body.count(expected_url) == 1)
    hits = [w for w in BANNED if w in s]
    chk(name + "：无诱导性收益话术", not hits,
        "命中：" + "、".join(hits) if hits else "")
    chk(name + "：无本地绝对路径泄漏",
        not re.search(r"[A-Za-z]:[\\/]我的文档|Default Project", s))
    c = re.search(r'rel=["\']?canonical["\']?\s+href=["\']?([^"\'>\s]+)', s)
    chk(name + "：canonical 指向最终域名", bool(c and c.group(1).startswith(DOMAIN)),
        c.group(1) if c else "未找到 canonical")

    anchors = re.findall(r"<a[^>]*invite-btn[^>]*>", s)
    chk(name + "：1 个可点团队邀请按钮", len(anchors) == 1, "实际 %d" % len(anchors))
    if anchors:
        chk(name + "：按钮 rel/target 合规",
            all(k in anchors[0] for k in ("sponsored", "nofollow", "noopener", "_blank")))
        h = re.search(r"href=[\"']?([^\"'\s>]+)", html.unescape(anchors[0]))
        hv = h.group(1) if h else ""
        chk(name + "：按钮域名为专属邀请域",
            (urlparse(hv).hostname or "") in ALLOWED_HOSTS, hv or "未取到 href")
        chk(name + "：按钮邀请码与 data 一致",
            bool(expected_code) and ("invite_code=" + expected_code) in hv)
    chk(name + "：展示邀请码与 data 一致",
        bool(expected_code) and ("<strong>" + expected_code + "</strong>") in s)
    chk(name + "：data 链接与页面一致",
        bool(expected_url) and expected_url in html.unescape(s))

robots = read(PUB / "robots.txt")
chk("robots.txt 含 Sitemap 行", "Sitemap" in robots and DOMAIN in robots)

sitemap = read(PUB / "sitemap.xml")
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
chk("sitemap 指向最终域名", bool(urls) and all(u.startswith(DOMAIN) for u in urls),
    "%d 条" % len(urls))
proj_urls = sum("/projects/" in u for u in urls)
chk("sitemap 含栏目页与 10 篇文章（#28）", proj_urls == 11, "实际 %d 条" % proj_urls)
chk("sitemap 条数 = 13（首页/关于/栏目/10 篇）（#28）", len(urls) == 13, "%d 条" % len(urls))

css_dir = PUB / "assets" / "css"
css_files = list(css_dir.glob("*.css")) if css_dir.is_dir() else []
chk("extended 样式已注入", any(".info-grid" in read(p) for p in css_files))

failed = [r for r in rows if not r[1]]
for label, ok, note in rows:
    print(("  OK   " if ok else " BLOCK ") + label + (("  | " + str(note)) if note else ""))

tax_urls = [u for u in urls if "/categories/" in u or "/tags/" in u]
if tax_urls:
    print("  WARN  sitemap 含 taxonomy 空页：%d 条（不影响功能，可择机清理）" % len(tax_urls))

print("\n阶段：%s；%d/%d 通过；阻断 %d 项" % (
    "空链版" if pending else "正式版", len(rows) - len(failed), len(rows), len(failed)))
sys.exit(1 if failed else 0)
