#!/usr/bin/env python3
"""推广站「项目介绍」栏目稿自检（纯标准库、只读 content/projects/ 与 data/invite.yaml，不联网）。

用法：python check_drafts.py
退出码：0 = 全绿；1 = 存在阻断项。

按总纲 #26（2026-11-08）：4 篇配套稿已从 drafts/ 升格为站点正式栏目页
content/projects/NN-*.md 并 push 上线，故扫描路径随之迁移；drafts/ 仍只保留
内部交付说明（继续在 .gitignore 中，不进公开仓库）。
只扫描 content/projects/NN-*.md；下划线开头的栏目 _index.md 不参与逐篇检查。

与 check_build.py 分工：后者管构建产物 public/（首页／关于页／栏目列表页按
#22/#23 加严不写收益数字；4 篇文章页按 #24 允许引用官网宣传数字，但须带
标注），本脚本管源稿——按 #24 允许引用官网宣传数字，但必须标注平台宣传口径、
核验日期与「不是收益承诺」，且诱导词仍一律拦。

按 #25（2026-11-08）：四篇稿件统一刊登同一个团队邀请链接与邀请码，
不再逐项目留占位。链接/邀请码的**唯一真源仍是 data/invite.yaml**；
本脚本从真源取值，逐篇校验逐字一致，换码漏改即阻断，脚本内不写死任何码。
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
PROJECTS = ROOT / "content" / "projects"
DRAFTS = ROOT / "drafts"
INVITE = ROOT / "data" / "invite.yaml"
POSTS = sorted(PROJECTS.glob("[0-9][0-9]-*.md"))

# 与站点 check_build.py 的 BANNED 保持同一套底线：否定式举例同样拦截。
BANNED = [
    "3%", "5%", "躺赚", "躺赢", "被动收入", "管道收入", "睡后收入",
    "日入", "月入", "保底", "包赚", "稳赚", "轻松赚", "零成本",
    "持续受益", "下级越多", "发展下线", "加盟费",
]

# 归因与泄露红线：官方投放入口、旧占位口径、本地草稿期表述、内部路径、
# 图片、互动引导。#26 后「挂载到站点时／挂载后」等未来时表述一律不得残留。
# 注意：tg.bd.cn 与邀请码不再列入禁止项（#25），改由下方真源一致性校验。
FORBIDDEN = [
    "66666600", "seo_rtb", "dt.bd.cn",
    "REPLACE_WITH_INVITE_URL", "【待景行在后台申请项目并生成后回填】",
    "本文不重复刊登", "本项目专属推广链接", "挂载", "draft: true",
    "![", "欢迎留言", "E:\\", "E:/", "Default Project", "workbuddy",
    "https://gdaox.top", "http://gdaox.top",
]

REQUIRED = [
    "广告｜推广链接",
    "推广合作信息 · 非招聘 · 非收益承诺",
    "不会增加你的费用",
    "不收取任何费用",
    "不代收费用、不代结算",
    "以平台当期官方说明为准",
    "平台宣传口径",
    "核验日期",
    "不是收益承诺",
    "## TL;DR",
    "## 参考阅读",
    "任推邦官网项目列表页",
    "统一团队邀请入口",
    "本站专属邀请码",
    "共用这一个入口",
    "手动填入",
    "不得直接引用",
]

rows = []


def chk(label, ok, note=""):
    rows.append((label, bool(ok), note))


def load_invite():
    """从 data/invite.yaml 的 cta 块读 url / code；本脚本不写死任何邀请码。"""
    txt = INVITE.read_text(encoding="utf-8")
    block = txt.split("\nsections:", 1)[0]
    u = re.search(r'(?m)^\s*url:\s*"([^"]+)"', block)
    c = re.search(r'(?m)^\s*code:\s*"([^"]+)"', block)
    return (u.group(1) if u else ""), (c.group(1) if c else "")


if not POSTS:
    print("BLOCK  content/projects/ 下未找到 NN-*.md 稿件")
    sys.exit(1)

INVITE_URL, INVITE_CODE = load_invite()
chk("唯一真源 data/invite.yaml 可读（cta.url / cta.code）",
    bool(INVITE_URL) and bool(INVITE_CODE))
chk("真源域名在白名单且为团队自助邀请",
    INVITE_URL.startswith("https://tg.bd.cn/")
    and "qd=self_team_android" in INVITE_URL
    and "dt.bd.cn" not in INVITE_URL)
chk("真源 URL 内邀请码 = cta.code",
    "invite_code=" + INVITE_CODE in INVITE_URL
    and bool(re.fullmatch(r"\d{4,12}", INVITE_CODE)))

titles = []
slugs = []
for p in POSTS:
    name = p.name
    text = p.read_text(encoding="utf-8")
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    chk(name + "：front matter 且已转为正式页（draft: false）",
        bool(fm) and "draft: false" in fm.group(1))

    slug_m = re.search(r'(?m)^slug:\s*"([^"]+)"', text)
    slug = slug_m.group(1) if slug_m else ""
    slugs.append(slug)
    chk(name + "：英文 slug 已设置",
        bool(slug) and bool(re.fullmatch(r"[a-z0-9-]+", slug)), slug)

    m = re.search(r'(?m)^title:\s*"([^"]+)"', text)
    title = m.group(1) if m else ""
    titles.append(title)
    chk(name + "：标题有落点", bool(title) and len(title) >= 12 and ("：" in title or "，" in title))

    miss = [s for s in REQUIRED if s not in text]
    chk(name + "：必备声明/结构齐全", not miss, "缺：" + "、".join(miss) if miss else "")

    hits = [w for w in BANNED if w in text]
    chk(name + "：无诱导性收益话术", not hits, "命中：" + "、".join(hits) if hits else "")

    leaks = [w for w in FORBIDDEN if w in text]
    chk(name + "：无官方码/旧占位/草稿期表述/内部路径/图片/互动引导", not leaks,
        "命中：" + "、".join(leaks) if leaks else "")

    # #24 有限放宽的代价：凡引用官网金额，必须同篇带宣传口径与免责。
    has_money = "￥" in text or "单笔最高收益" in text
    chk(name + "：宣传数字已标注口径",
        (not has_money) or all(s in text for s in
                               ("平台宣传口径", "不是收益承诺", "以平台当期官方说明为准")))

    # #25：统一入口与真源逐字一致，防止换码漏改或误挂官方投放链接。
    chk(name + "：统一入口链接与真源逐字一致且只出现一次",
        text.count(INVITE_URL) == 1, "实际 %d 次" % text.count(INVITE_URL))
    body_codes = set(re.findall(r"invite_code=(\d+)", text))
    chk(name + "：URL 邀请码无错码/异码",
        body_codes == {INVITE_CODE}, "实际 %s" % (sorted(body_codes) or "无"))
    chk(name + "：展示邀请码与真源一致",
        "`" + INVITE_CODE + "`" in text)
    bd_links = [u for u in re.findall(r"https?://[^\s`)]+", text) if "bd.cn" in u]
    chk(name + "：推广域名链接唯一且非官方入口",
        bd_links == [INVITE_URL], "实际 %s" % (bd_links or "无"))
    chk(name + "：邀请码手填兜底说明", "手动填入 `" + INVITE_CODE + "`" in text)

    chars = len(re.sub(r"\s", "", text))
    chk(name + "：篇幅 ≥800 字（非空壳）", chars >= 800, "%d 字" % chars)

gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
chk("稿件数量 = 4", len(POSTS) == 4, "实际 %d" % len(POSTS))
chk("标题互不重复", len(set(titles)) == len(titles))
chk("slug 互不重复", len(set(slugs)) == len(slugs))
chk("栏目 _index.md 存在", (PROJECTS / "_index.md").is_file())
chk("内部交付说明仍在 drafts/", (DRAFTS / "_选题与交付说明.md").is_file())
chk("drafts/ 仍被忽略（内部说明不进公开仓库）", "drafts/" in gi)
chk("content/projects/ 未进忽略名单（随 #26 上线）",
    not any(line.strip().startswith("content") for line in gi.splitlines()))

failed = [r for r in rows if not r[1]]
for label, ok, note in rows:
    print(("  OK   " if ok else " BLOCK ") + label + (("  | " + str(note)) if note else ""))

print("\n%d 篇栏目稿；%d/%d 通过；阻断 %d 项" % (
    len(POSTS), len(rows) - len(failed), len(rows), len(failed)))
sys.exit(1 if failed else 0)
