#!/usr/bin/env python3
"""推广站「项目介绍」栏目稿自检（纯标准库、只读 content/projects/ 与 data/invite.yaml，不联网）。

用法：python check_drafts.py
退出码：0 = 全绿；1 = 存在阻断项。

按总纲 #27（2026-11-08）：栏目稿改为简版（正文约 600–800 字，含固定
声明与链接的文件约 1300 字），重心从「项目科普」
转为「引导加入团队 → 下载 App → 熟悉规则」；不再引用官网宣传数字，
#24/#26 的放宽条款保留但闲置。官网 /app/ 下载页整页带官方投放码
66666600，故稿件不挂任何第三方下载／注册链接，只做文字引导。
按总纲 #28（2026-11-08）：栏目由 4 篇扩为 10 篇，骨架与全部合规声明
逐字保留，只把 TL;DR、「项目是什么」、「几条提醒」写成生活化切口；
新增「10 篇开头与项目说明互不重复」检查，防止扩篇时套模板。
按总纲 #29（2026-11-08，现行）：10 篇统一改为「简洁版」——场景开头、
结论前置、加粗锚点、三步清单、双互动钩；**删参考阅读区、官网链接与
核验日期**，全稿只保留 1 个邀请 URL ＋邀请码，三步编号由「第一步～第三步」
改为「一、二、三」。新增：全稿 URL 唯一、无 markdown 外链与官网域名、
结论前置、10 篇专属提醒互不重复；合规声明与真源校验一字未松。

与 check_build.py 分工：后者管构建产物 public/（首页／关于页／栏目列表页
按 #22/#23 加严；10 篇文章页按 #29 校验三步引导、无官网数字、CTA 前置、
正文无站外链接）。本脚本管源稿。链接与邀请码的唯一真源仍是
data/invite.yaml，换码漏改即拦。
P12（2026-11-08，执行动作）：列表页表述精简后加护栏——10 篇卡片描述
互不重复且不超过 36 字、不回潮旧模板尾巴；栏目引导区不含内部归因口径、
篇幅有上限；合规引用块逐字保留。
P13（2026-11-08，执行动作）：同页合规声明去重——每篇只留开头 FLAG 块一处
完整声明，正文末尾不再复述；新增「关键合规短语全稿各恰 1 次」与「FLAG 块外
不得再出现合规短语」断言，防止重复声明回潮。
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
# 图片、互动引导。#27 追加：官网宣传数字、官网 APP 下载页／镜像域、
# 应用商店等未经核实的下载入口，一律不得回到简版稿件。
FORBIDDEN = [
    "66666600", "seo_rtb", "dt.bd.cn",
    "REPLACE_WITH_INVITE_URL", "【待景行在后台申请项目并生成后回填】",
    "本文不重复刊登", "本项目专属推广链接", "挂载", "draft: true",
    "![", "欢迎留言", "E:\\", "E:/", "Default Project", "workbuddy",
    "https://gdaox.top", "http://gdaox.top",
    "￥", "单笔最高收益", "每单可赚", "正在推广人数", "推广人数",
    "rentuiapp.com/app", "rentuibang.top", "qr-app-download", "应用商店",
    # #29：旧结构不得回流；全稿只留一个邀请链接，官网域名一律不进源稿。
    "rentuiapp.com", "## 参考阅读", "核验日期", "## TL;DR",
    "第一步", "第二步", "第三步", "统一团队邀请入口", "共用这一个入口",
    "](",
]

REQUIRED = [
    "广告｜推广链接",
    "推广合作信息 · 非招聘 · 非收益承诺",
    "不会增加你的费用",
    "不收取任何费用",
    "不代收费用、不代结算",
    "以平台当期官方说明为准",
    "本站专属邀请码",
    "手动填入",
    "不得直接引用",
    # #29 简洁版：加入团队 / 下载 App / 熟悉规则三步（编号「一、二、三」）
    "加入团队",
    "下载 App",
    "熟悉规则",
    "先把顺序摆对",
    "任推邦 App",
    "本站不提供安装包",
    "结果存在不确定性",
    # #29 唯一入口与爆款骨架
    "团队邀请入口",
    "邀请入口只有一个",
    "这个项目的第一件事不是发链接",
    "三步，照着走就行",
    "几件得说在前面的事",
    "你会先花十分钟把规则看完",
    "一、",
    "二、",
    "三、",
]

# --- P13（2026-11-08）：同页合规声明唯一性 ---
# 每篇稿件的完整合规声明只放在开头 FLAG 块（引用块）一处；正文任何位置
# 不得再复述这些短语。下列短语全稿各恰 1 次，出现 0 次或 >1 次都判回潮。
P13_ONCE = [
    "广告｜推广链接",
    "推广合作信息 · 非招聘 · 非收益承诺",
    "不会增加你的费用",
    "不收取任何费用",
    "不代收费用、不代结算",
    "本站不设兼职岗位",
    "以平台当期官方说明为准",
]
# 「结果存在不确定性」是正文风险提示（「几件得说在前面的事」段），
# 不是 FLAG 块声明词，单独要求全稿恰 1 次。
P13_RISK = ["结果存在不确定性"]
# 只允许出现在开头 FLAG 引用块里的声明词（正文区必须为 0 次）。
P13_FLAG_ONLY = [
    "广告｜推广链接",
    "推广合作信息 · 非招聘 · 非收益承诺",
    "不会增加你的费用",
    "不收取任何费用",
    "不代收费用、不代结算",
    "本站不设兼职岗位",
    "以平台当期官方说明为准",
]
# 旧版正文末尾的复述句（整句），已删除，不得回流。
P13_ZERO = [
    "本页不是招聘，也不是兼职岗位；规则、活动状态与结算口径一律以平台当期官方说明为准。",
    "本页不是招聘，也不是兼职岗位",
]


def plain_body(text):
    """去掉 front matter 与引用块，只留正文（供去重锚点定位）。"""
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    body = text[m.end():] if m else text
    return "\n".join(l for l in body.splitlines()
                     if l.strip() and not l.startswith(">"))


def flag_block(text):
    """取开头 FLAG 引用块（含 '>' 行的连续段落）。"""
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    body = text[m.end():] if m else text
    lines, on = [], True
    for ln in body.splitlines():
        if on and ln.startswith(">"):
            lines.append(ln)
        elif on and not ln.strip():
            continue
        else:
            break
    return "\n".join(lines)

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
    chk(name + "：必备声明/结构与三步引导齐全", not miss, "缺：" + "、".join(miss) if miss else "")

    chk(name + "：三步引导顺序正确（#29：一、二、三）",
        text.find("一、") < text.find("二、") < text.find("三、")
        and all(k in text for k in ("一、", "二、", "三、")))

    hits = [w for w in BANNED if w in text]
    chk(name + "：无诱导性收益话术", not hits, "命中：" + "、".join(hits) if hits else "")

    leaks = [w for w in FORBIDDEN if w in text]
    chk(name + "：无官方码/官网宣传数字/第三方下载入口/内部路径", not leaks,
        "命中：" + "、".join(leaks) if leaks else "")

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

    # #29：全稿只留一个 URL（真源邀请链接），不附官网／参考／任何其它链接。
    all_urls = re.findall(r"https?://[^\s`)]+", text)
    chk(name + "：全稿仅 1 个 URL 且为邀请真源（#29）",
        all_urls == [INVITE_URL], "实际 %s" % (all_urls or "无"))
    chk(name + "：无 markdown 外链与官网域名（#29）",
        "](" not in text and "rentuiapp.com" not in text)
    chk(name + "：结论前置在首个小标题之前（#29）",
        text.find("这个项目的第一件事不是发链接") < text.find("## "))

    chars = len(re.sub(r"\s", "", text))
    # 含固定推广声明、统一邀请链接与 front matter；正文观感约 950–1050 字。
    chk(name + "：简洁版篇幅 1050–1350 字（#29）", 1050 <= chars <= 1350, "%d 字" % chars)

    # P13：完整合规声明全稿各恰 1 次，且只出现在开头 FLAG 引用块里。
    cnt_bad = [(k, text.count(k)) for k in P13_ONCE if text.count(k) != 1]
    chk(name + "：关键合规短语全稿各恰 1 次（P13 去重）", not cnt_bad,
        "；".join("%s×%d" % (k, n) for k, n in cnt_bad))
    r_bad = [(k, text.count(k)) for k in P13_RISK if text.count(k) != 1]
    chk(name + "：正文风险提示恰 1 次（P13 去重）", not r_bad,
        "；".join("%s×%d" % (k, n) for k, n in r_bad))
    z_bad = [(k, text.count(k)) for k in P13_ZERO if text.count(k) != 0]
    chk(name + "：正文末尾合规复述句已删除（P13 去重）", not z_bad,
        "；".join("%s×%d" % (k, n) for k, n in z_bad))
    _plain_txt = plain_body(text)
    f_bad = [(k, _plain_txt.count(k)) for k in P13_FLAG_ONLY if _plain_txt.count(k) != 0]
    chk(name + "：FLAG 块外无合规声明复述（P13 去重）", not f_bad,
        "；".join("%s×%d" % (k, n) for k, n in f_bad))
    _flag_txt = flag_block(text)
    fb_bad = [(k, _flag_txt.count(k)) for k in P13_FLAG_ONLY if _flag_txt.count(k) != 1]
    chk(name + "：声明词集中在开头 FLAG 块（P13 去重）", not fb_bad,
        "；".join("%s×%d" % (k, n) for k, n in fb_bad))

# #29：10 篇不得套模板，场景开头／项目说明／专属提醒逐篇互异。
def section_text(text, start, end):
    a = text.find(start)
    b = text.find(end, a + 1) if a >= 0 else -1
    return text[a:b].strip() if a >= 0 and b > a else ""


texts = [p.read_text(encoding="utf-8") for p in POSTS]
plains = [plain_body(t) for t in texts]
ledes = [p.split("## ", 1)[0].strip().splitlines()[0] if "## " in p else ""
         for p in plains]
whats = [section_text(p, "## ", "## 三步，照着走就行") for p in plains]
notices = [section_text(p, "## 几件得说在前面的事", "**团队邀请入口**") for p in plains]

# --- P12（2026-11-08）：列表页内容表述精简的防回潮护栏 ---
DESC_RE = re.compile(r'(?m)^description:\s*"([^"]+)"')
descs = []
for _t in texts:
    _m = DESC_RE.search(_t)
    descs.append(_m.group(1) if _m else "")
chk("10 篇均有卡片描述（P12）", all(descs))
chk("10 篇卡片描述互不重复（P12）", len(set(descs)) == len(POSTS),
    "重复 %d 条" % (len(descs) - len(set(descs))))
chk("卡片描述 12–36 字（P12）",
    all(12 <= len(d) <= 36 for d in descs),
    "最长 %d 字" % (max((len(d) for d in descs), default=0)))
chk("卡片描述无旧模板尾巴（P12）",
    not any(x in d for d in descs for x in
            ("类项目；", "先加入团队、下载 App", "推广合作信息，含推广链接")))

_idx = (PROJECTS / "_index.md").read_text(encoding="utf-8")
_idx_body = re.sub(r"(?m)^---\s*\n.*?\n---\s*\n", "", _idx, flags=re.S)
_idx_body = "\n".join(l for l in _idx_body.splitlines()
                       if l.strip() and not l.strip().startswith(">"))
_internal = [w for w in ("归因不归本站", "立即推广", "不逐项目申请",
                         "撤下或改写", "本站会撤下") if w in _idx_body]
chk("栏目引导区无内部归因口径（P12）", not _internal,
    "命中：" + "、".join(_internal) if _internal else "")
_idx_chars = len(re.sub(r"\s", "", _idx_body))
chk("栏目引导区精简 ≤ 280 字（P12）", 0 < _idx_chars <= 280,
    "%d 字" % _idx_chars)
chk("栏目合规引用块逐字保留（P12）",
    all(x in _idx for x in ("广告｜推广链接", "推广合作信息 · 非招聘 · 非收益承诺",
                            "不会增加你的费用", "不收取任何费用",
                            "不代收费用、不代结算", "以平台当期官方说明为准")))

# P13：栏目页声明同样只留引用块一处，关键短语各恰 1 次。
_idx_cnt_bad = [(k, _idx.count(k)) for k in P13_ONCE if _idx.count(k) != 1]
chk("栏目页关键合规短语各恰 1 次（P13 去重）", not _idx_cnt_bad,
    "；".join("%s×%d" % (k, n) for k, n in _idx_cnt_bad))
_idx_r_bad = [(k, _idx.count(k)) for k in P13_RISK if _idx.count(k) != 1]
chk("栏目页正文风险提示恰 1 次（P13 去重）", not _idx_r_bad,
    "；".join("%s×%d" % (k, n) for k, n in _idx_r_bad))
_idx_z_bad = [(k, _idx.count(k)) for k in P13_ZERO if _idx.count(k) != 0]
chk("栏目页无正文末尾合规复述句（P13 去重）", not _idx_z_bad,
    "；".join("%s×%d" % (k, n) for k, n in _idx_z_bad))
_idx_plain = plain_body(_idx)
_idx_f_bad = [(k, _idx_plain.count(k)) for k in P13_FLAG_ONLY if _idx_plain.count(k) != 0]
chk("栏目页 FLAG 块外无合规声明复述（P13 去重）", not _idx_f_bad,
    "；".join("%s×%d" % (k, n) for k, n in _idx_f_bad))

gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
chk("稿件数量 = 10（#28/#29）", len(POSTS) == 10, "实际 %d" % len(POSTS))
chk("10 篇场景开头互不重复（#29）",
    all(ledes) and len(set(ledes)) == len(POSTS))
chk("10 篇项目说明互不重复（#29）",
    all(whats) and len(set(whats)) == len(POSTS))
chk("10 篇专属提醒互不重复（#29）",
    all(notices) and len(set(notices)) == len(POSTS))
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
