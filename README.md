# promo-site｜推广二级域名 · 团队邀请说明页

独立 Hugo + PaperMod 静态站，域名 `nav.gdaox.top`，托管于 Cloudflare Pages（项目 `nav-gdaox-top`）。

> **主题已于 2026-11-08 转向**：由「网盘 & AI 工具推广导航」改为**任推邦团队邀请说明页**（参照 `https://www.rentuiapp.com/team/`）。
> 当前为**阶段二「正式版」并已上线**：2026-11-08 景行本人提供专属邀请链接与邀请码，已回填 `data/invite.yaml`；主按钮为可点链接，页面另展示邀请码兜底。合作方式说明、推广标识、合规声明、关于页齐全，无任何坏链。
> **✅ 2026-11-08 景行令「push」→ 提交 `4832d95` 并推送 `origin/main`，CF Pages 自动重建，线上 `https://nav.gdaox.top/` 已切换为团队邀请说明页**；首页／CSS／`/about/`／`/sitemap.xml`／`/robots.txt` 验收全绿（详见方案 v1.11 §9.9）。
> **✅ 2026-11-08 景行再令「推送至 https://nav.gdaox.top/」→ 4 篇项目介绍配套稿挂载为 `/projects/` 正式栏目并上线**（总纲 **#26**，方案 **v1.12 §9.10**）：栏目列表页 `/projects/` ＋ 4 篇文章页，首页与菜单均加入链，sitemap 7 条；两套门禁 **62/62 与 93/93**。`drafts/` 现只留内部交付说明（继续 `.gitignore`），4 篇成稿在 `content/projects/`。
> **P8 配套稿口径（2026-11-08，现行按总纲 #27）**：4 篇分别覆盖网盘拉新／AI 工具／电商活动／内容社区，现路径 `content/projects/NN-*.md`。**#27 起不再引用官网宣传数字**（删全部金额／最高收益／推广人数与「平台宣传口径」标注；#24 有限放宽保留但闲置，以后若恢复引用仍须按 #24 逐篇标注平台宣传口径＋核验日期＋不是收益承诺＋以后台当期为准）；**首页／关于页／栏目列表页仍按 #22/#23 加严，不写收益数字**。4 篇与文章页按钮统一用 `data/invite.yaml` 的同一个团队邀请链接与邀请码（总纲 #25），机检做真源一致性校验；不逐项目申请项目级链接。**未排期、不占 A 档槽位、不进博客九栏与公众号产线**。
> **★ 2026-11-08 再令（总纲 #27，方案 v1.14 §9.12）**：景行令「调整四篇推广博文尽量写简单些，重点引导用户加入团队，下载 app 熟悉」→ 4 篇改为简版（正文约 600–800 字），重心＝加入团队 → 下载 App → 熟悉规则；**官网宣传数字全部移除**（#24 放宽保留但闲置）、CTA 前置到正文前；官网 `/app/` 下载页含官方投放码 66666600，不引用，下载 App 只做纯文字引导。两套门禁 **62/62 与 103/103**。**本轮改动仅本地，未提交／未 push／未上线，线上 `/projects/` 仍为 #26 长稿版。**

---

## 一、归因：只有一个入口，且必须是你自己的邀请码

团队邀请的归因载体是**景行本人在任推邦后台【团队 → 我的团队】生成的专属邀请海报 / 推广链接 / 邀请码**。有效动作是「访客用该邀请码注册成为团队成员」，之后平台在成员结算时按当期规则向邀请方发放额外补贴。

> **★ 最大坑**：任推邦官网 `/team/` 页上所有「立即注册 / 立即邀请」按钮都指向
> `https://dt.bd.cn/#/pages/login/register?invite_code=66666600&ly=seo_rtb_syqm1`，
> 其中 `66666600` 是**任推邦官网自己的 SEO 投放码**。照搬这个链接，注册关系归官方，本站拿不到任何团队邀请补贴。
> `check_build.py` 已把该邀请码与 `seo_rtb` 参数列为**阻断项**，误填会直接门禁失败。

现状（2026-11-08 回填后）：
- `data/invite.yaml` 的 `cta.url`／`cta.code` 已由景行本人提供的**专属**链接与邀请码替换占位符，模板自动切为可点主按钮；链接域名 `tg.bd.cn`、参数 `qd=self_team_android`，与官方投放链接 `dt.bd.cn` ＋ `66666600` 不同。
- 换链接只改 `cta.url`／`cta.code`／`cta.verify` 三处；`check_build.py` 会校验按钮域名白名单、URL 邀请码与 `cta.code` 一致、页面展示码一致，**换码漏改会直接门禁失败**。**（总纲 #26 后）还须同步 `content/projects/NN-*.md` 4 篇稿件、重新构建并复跑两套门禁**，否则源稿门禁会因链接／码与真源不一致而阻断。
- 邀请码**只落在 `data/invite.yaml` 这一处真源**；模板通过 `$cta.code` 渲染，CSS、关于页、方案文档一律不写死邀请码或链接。4 篇项目介绍稿属**受控例外**（正文刊登同一链接与码，由 `check_drafts.py` 做真源一致性校验）；文章页／栏目列表页的可点按钮由 `layouts/partials/invite_cta.html` 从同一真源渲染。
- 链接为 hash 路由（`#/pages/login/register?...`），部分内置 WebView 可能丢失参数，故页面显示邀请码供访客手填兜底。

## 二、合规红线（比工具推广更严，已固化成机检）

团队邀请属于「发展团队成员、按成员业绩计酬」形态，2025-02 新浪财经／银柿财经等公开报道对该模式存在传销合规质疑，并引用《禁止传销条例》第七条第(三)项。**对外文案一律从严**：

| 必须写 | 禁止写 |
|---|---|
| 「广告｜推广链接」显著标识 | 补贴比例（3%／5% 等任何数字） |
| 「推广合作信息 · 非招聘 · 非收益承诺」 | 躺赚／被动收入／管道收入／日入／月入 |
| 「不会增加你的费用」「不收取任何费用」 | 保底／包赚／稳赚／轻松赚／零成本 |
| 「规则以平台当期官方说明为准」 | 收益案例、收益承诺、加盟费 |
| 非官方声明、主体与联系入口 | 「发展下线」「下级越多」等拉人头话术 |

`check_build.py` 用 `BANNED` 词表扫描首页、关于页、栏目列表页与 4 篇文章页，**连否定式用词也会拦截**（例：「不提供*保底*」曾被拦，已改写成「不提供任何形式的收益保证」）。另按口径分工：栏目列表页加查「不列收益数字」，4 篇文章页加查「宣传数字已标注平台口径」（总纲 #24／#26）。理由：平台与搜索引擎的机器审核同样按字面判定，否定语境也可能被误伤。

首页与关于页均明确：不是招聘／不是兼职岗位／不是加盟或培训招生；注册与入驻免费；本站不代收费用、不代结算、不提供收益保证；推广需投入时间与渠道资源、结果存在不确定性。

## 三、目录

```
hugo.toml                      站点配置（标题 / 描述 / 首页信息）
data/invite.yaml               唯一真源：cta（邀请入口）+ sections（4 张说明卡片）
layouts/index.html             首页模板（覆盖 define "main"）
layouts/projects/list.html      /projects/ 栏目列表页模板
layouts/projects/single.html    项目介绍文章页模板
layouts/partials/invite_cta.html 统一团队邀请入口块（从 hugo.Data 真源渲染）
content/_index.md              首页对象（仅 front matter）
content/about.md               关于页（非官方声明 / 推广声明 / 合作性质 / 内容边界 / 主体）
content/projects/_index.md      项目介绍栏目说明（按 #22/#23 加严，不列收益数字）
content/projects/NN-*.md        4 篇项目介绍正式稿（draft: false + slug）
assets/css/extended/custom.css 样式（PaperMod 官方扩展位）
themes/PaperMod/               官方最新版 PaperMod vendored 副本（非 submodule）
check_build.py                 构建产物自检（纯标准库、只读 public/，103 项）
check_drafts.py                栏目稿自检（纯标准库、只读 content/projects/ 与 data/invite.yaml，62 项）
drafts/                        仅内部交付说明（.gitignore 忽略，不进公开仓库）
.gitignore / README.md
```

> 旧文件 `data/tools.yaml`（4 个网盘/AI 工具卡片）已删除；CSS 类名由 `.tool-*` 改为 `.info-*`／`.invite-*`。

## 四、关键约定

- **链接唯一真源** = `data/invite.yaml`。换邀请链接只改这一个文件的 `cta.url`／`cta.code`／`cta.verify`，不需要改模板、不需要 Worker；但按 #26 须同步 4 篇 `content/projects/` 稿件并重新构建＋复跑两套门禁。数据访问用 `hugo.Data`（`.Site.Data` 已弃用）。
- `cta.url` 为占位符时，`layouts/index.html` 自动把主按钮渲染为不可点的「入口待开放」并显示阶段提示；替换为真实链接后自动变为带 `rel="sponsored nofollow noopener"` 的可点按钮，并展示 `cta.code` 供手填兜底。**阶段一／阶段二均已实测通过**。
- 主题是**官方最新版整目录副本**：GitHub master HEAD `118119693d8b5ac211b939775678310973bcb232`（2026-10-25，`min_version = 0.158.0`），去掉嵌套 `.git`、不改任何主题源码、零兼容补丁。新版用 `layouts/_partials/`（Hugo 0.146+），与旧版主博客主题的 `layouts/partials/` 不通用，**不要复制主博客主题目录**。
- `disableKinds = ["RSS","taxonomy","term"]` + `taxonomies = {}` 是**主动瘦身**（不生成 RSS 与空分类／标签页；sitemap 现为首页＋关于页＋项目介绍栏目＋4 篇文章共 **7 条**），不是兼容补丁。
- 首页由 `layouts/index.html` 的 `define "main"` 渲染；**不要**把内容写回 `content/_index.md` 的内联 HTML（Goldmark 默认会丢弃）。`locale = "zh-cn"`，`unsafe = false` 保持默认。

## 五、本地构建与门禁

以下命令在**站点根目录**执行：

```bash
hugo version                              # v0.166.0 → CF Pages 的 HUGO_VERSION 填 0.166.0
hugo server -D                            # 本地预览 http://localhost:1313
rm -rf public && hugo --gc --minify       # 复现线上构建
python check_build.py                     # 产物自检；0=全绿，1=阻断
```

> **坑 1**：`--cleanDestinationDir` 并**不清理**上一轮遗留文件。换主题、改 `disableKinds` 或 CSS 后必须 `rm -rf public` 再构建，否则 public 会残留旧空分类页与旧 fingerprint CSS。
> **坑 2**：Hugo `--minify` 输出的**属性不带引号**、且会把 URL 里的 `&` 转义成 `&amp;`；门禁先用 `html.unescape` 还原再取 `href`，并用 `r"<a[^>]*invite-btn[^>]*>"` 匹配无引号属性。
> **坑 3（2026-11-08 实测）**：`hugo server` 输出「Serving pages from disk」会**把开发版写进 `public/`**，把 canonical 改成 `http://localhost:1313/`，此时跑门禁会误报 canonical 失败。**复现线上构建／跑门禁前必须先停 dev server**；本地预览改用只读静态服务：`python -m http.server 1313 --bind 127.0.0.1 --directory public`。

`check_build.py` 当前 **阶段一 30 项／阶段二 103 项**（#26 挂载后 93 项，#27 简版改写后 103 项），阶段二实测 **103/103、exit 0**：除 canonical、sitemap、robots、CSS 注入、本地路径泄漏外，还检查 4 张说明卡片、推广标识、非招聘／非收益承诺／不收费声明、无官方 SEO 邀请码、无补贴比例与收益诱导词、阶段一主按钮禁用 / 阶段二按钮 `rel/target` 合规、关于页三类声明、data 邀请码有效性与真源一致性。**#26 新增**：首页 `/projects/` 入链、栏目列表页、4 篇文章页各一组（广告与合规定性、无官方码与投放域、无诱导词、canonical、1 个合规 CTA、按钮域名／码／展示码与真源一致）、sitemap 7 条。**#27 新增**：列表页含加入团队／下载 App 引导且不挂官网下载入口；4 篇文章页各 5 项——三步引导齐全且顺序正确、CTA 前置到正文之前、无官网宣传数字、无第三方下载／注册入口与官方投放域。

**栏目稿机检（2026-11-08 新增；#25 升 55 项；#26 升 62 项；#27 改口径后仍 62 项）**：`python check_drafts.py` 只扫 `content/projects/NN-*.md`，从 `data/invite.yaml` 读 `cta.url`／`cta.code` 作唯一真源，**62 项**：必备推广声明块／TL;DR／参考区／核验日期／**三步引导（加入团队／下载 App／先熟悉）齐全且有序**；禁诱导性收益话术（连否定式也拦）、禁官方投放码与 `dt.bd.cn`、**禁官网宣传数字（`￥`／单笔最高收益／每单可赚／推广人数）与第三方下载入口（`rentuiapp.com/app`／镜像域／二维码／应用商店）**、禁旧占位与草稿期未来时表述、禁内部路径／图片／互动引导；逐篇校验统一入口链接逐字一致且只出现一次、URL 邀请码／展示码／手填兜底码与真源一致、推广域名链接唯一且非官方入口；另查 `draft: false`、英文 slug 唯一、`_index.md` 存在、`drafts/` 忽略而 `content/projects/` 不忽略、**简版篇幅 700–1400 字（含固定声明与链接）**、标题不重复。与 `check_build.py` 分工互不替代：后者管 `public/` 产物。4 篇实测 **62/62、exit 0**；负向「真源换码／塞回官网数字／挂官网 APP 下载页」均被拦并恢复。

## 六、部署与上线状态

| 步骤 | 状态 |
|---|---|
| GitHub 独立仓库 `fapuxiansheng/nav.gdaox.top`（公开、`main`） | ✅ 已推送 |
| CF **Pages 项目** `nav-gdaox-top`：构建 `hugo --gc --minify` / 输出 `public` / Root 空 / 分支 `main` / `HUGO_VERSION=0.166.0` | ✅ 已配置 |
| 自定义域 `nav.gdaox.top` → `CNAME nav → nav-gdaox-top.pages.dev`（已代理） | ✅ 已生效 |
| 阶段一「空链版」（旧主题：网盘 & AI 工具）线上验收全绿 | ✅ 2026-11-07 |
| **团队邀请主题改造 push 上线** | ✅ 2026-11-08 景行令「push」→ `4832d95` 已推送、CF 自动重建、线上验收全绿（方案 v1.11 §9.9） |
| 景行提供专属邀请链接／邀请码 → 回填 `cta.url`＋`cta.code`、模板补邀请码兜底、门禁升 35 项 | ✅ 2026-11-08 完成（35/35），已随 `4832d95` 上线 |
| 本地阶段二预览（只读静态服务 1313；首页／关于页 200、CTA 可点、邀请码与 canonical 正确） | ✅ 2026-11-08 |
| 任推邦渠道报备（自有网站 + 落地页 URL + 首页/关于页截图） | ⏸ 待景行本人提交 |
| 归因自测：无痕窗口点主按钮 → 核对邀请码参数 → 后台看团队人数回传 | ⏸ 真实链接已上线，待景行本人执行 |
| **P8 首批 4 篇项目介绍配套稿** | ✅ 2026-11-08：4 篇稿＋内部交付说明，统一刊登同一个团队邀请链接与邀请码（总纲 #25），`check_leak` 全绿；**未排期、不占 A 档槽位**，未动 `11_本周排期/` 与 `12_本周稿件/` |
| **4 篇挂载为 `/projects/` 正式栏目并 push 上线** | ✅ 2026-11-08 景行令「推送至 https://nav.gdaox.top/」→ 迁 `content/projects/`、新增栏目页／模板／统一入口 partial／首页与菜单入链，门禁 **62/62 与 93/93**，记总纲 **#26**（方案 v1.12 §9.10）；扩篇待另行下令 |
| **4 篇改简版、转向加入团队＋下载 App（#27）** | ✅ 2026-11-08 景行令「push」→ 提交 `c4611aa` 并上线：四节简版、三步引导、CTA 前置、栏目页与首页文案同步，门禁 **62/62 与 103/103**；线上 9 URL＋CSS 全 200、内容与本地构建一致（方案 v1.15 §9.13） |

> **★ CF 项目类型坑**：CF 新的「创建应用程序」默认建 **Workers 项目**（`npx wrangler deploy`），Hugo 静态站在 CI 里会被 wrangler 卡在交互式确认而构建失败，手动部署只得到 `Hello world`。必须点创建页底部「**继续前往 Pages**」旧版工作流。旧 Workers 项目 `nav-gdaox-top` 的 Git 构建自 11-07 `445c2c1` 起已停触发（11-08 两次 push 均只有 `Cloudflare Pages success`，无失败构建）；**CF 账号内该项目对象是否已删除待景行在已登录面板确认**，详见方案 v1.13 §9.11。
> **★ 推送网络坑**：WorkBuddy 运行期注入的 `HTTPS_PROXY` 对 GitHub 返回 `CONNECT tunnel 502`，**直连可用**。用推送脚本时须 `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy python git_push.py --repo "$(pwd)"`；直接 `git push` 同理。凭据助手路径报错不影响推送，若报认证失败需景行本人修 helper，AI 不碰凭据。

## 七、上线验收清单

- `python check_drafts.py` **62/62**、`python check_build.py` 阶段二 **103/103**，均 exit 0（须先停 `hugo server` 再干净重建）
- canonical `https://nav.gdaox.top/`、sitemap **7 条**（首页／关于／栏目／4 篇）均指向正式域名，不是 `pages.dev`／`localhost:1313`
- 首页 200：推广标识／非招聘定性／主按钮**可点且指向专属邀请域**／邀请码展示与 URL 参数一致／4 张说明卡片／补贴声明／`/projects/` 入链齐全；CSS 200
- `/projects/` 列表页 200：4 篇入链、推广标识与合规定性、**不列收益数字**、1 个合规 CTA
- 4 篇文章页各 200：广告标识／非招聘／非收益承诺／平台宣传口径标注／1 个合规 CTA／邀请码与真源一致，无官方 SEO 码与诱导词
- `/about/`、`/sitemap.xml`、`/robots.txt` 线上 200
- 主按钮落地 URL 的**邀请码是本站专属码**（与 `cta.code`、页面展示码三者一致），不是 `66666600`，域名在 `tg.bd.cn` 白名单内
- 归因自测通过后再考虑扩量；**归因不通不扩量**

## 八、红线

上线／push 按景行**逐次下令**执行；AI 不碰凭据（仅复用浏览器已有登录态）、不代点任推邦报备提交；不写补贴比例、不承诺收益、不写诱导性收益话术；不使用官方 SEO 邀请码；**邀请码／邀请链接只落 `data/invite.yaml` 唯一真源，不写死到模板、CSS、关于页或方案文档**（总纲 #25 的 4 篇项目介绍稿属受控例外，须经 `check_drafts.py` 真源一致性校验；文章页／列表页按钮由 partial 从真源渲染）；不收任何费用；不上传资源文件到本站；不与主博客互链；不碰 `.env` 等凭据文件。**（总纲 #27／#24）4 篇简版起不再引用官网宣传数字**，#24 放宽保留但闲置（恢复引用须按 #24 逐篇标注）；首页／关于页／栏目列表页仍不写收益数字，诱导性话术与收益承诺在任何页面都不放开；官网 `/app/` 下载页含官方投放码 66666600，不引用、不挂二维码／镜像域，下载 App 只做纯文字引导**；`drafts/` 只剩内部交付说明且不进公开仓库；**换邀请链接／码须同步 4 篇＋真源、重新构建并复跑两套门禁**；官网宣传数字与活动状态须定期回查，链接失效即撤下。
