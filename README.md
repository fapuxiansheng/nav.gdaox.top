# promo-site｜推广二级域名 · 团队邀请说明页

独立 Hugo + PaperMod 静态站，域名 `nav.gdaox.top`，托管于 Cloudflare Pages（项目 `nav-gdaox-top`）。

> **主题已于 2026-11-08 转向**：由「网盘 & AI 工具推广导航」改为**任推邦团队邀请说明页**（参照 `https://www.rentuiapp.com/team/`）。
> 当前为**阶段二「正式版」并已上线**：2026-11-08 景行本人提供专属邀请链接与邀请码，已回填 `data/invite.yaml`；主按钮为可点链接，页面另展示邀请码兜底。合作方式说明、推广标识、合规声明、关于页齐全，无任何坏链。
> **✅ 2026-11-08 景行令「push」→ 提交 `4832d95` 并推送 `origin/main`，CF Pages 自动重建，线上 `https://nav.gdaox.top/` 已切换为团队邀请说明页**；首页／CSS／`/about/`／`/sitemap.xml`／`/robots.txt` 验收全绿（详见方案 v1.11 §9.9）。`drafts/` 四篇配套稿仍为本地草稿，未进仓库、未挂站。
> **P8 配套稿（2026-11-08）**：`drafts/` 下 4 篇项目介绍稿＋交付说明，机检 **55/55**、`check_leak` 全绿；**`drafts/` 已进 `.gitignore`，不进公开仓库、不挂站、不发布**。宣传数字有限放宽只适用这 4 篇，口径见总纲 **#24**；4 篇统一刊登同一个团队邀请链接与邀请码（值见 `data/invite.yaml`，机检做真源一致性校验），不再逐项目申请项目级链接，见总纲 **#25**。

---

## 一、归因：只有一个入口，且必须是你自己的邀请码

团队邀请的归因载体是**景行本人在任推邦后台【团队 → 我的团队】生成的专属邀请海报 / 推广链接 / 邀请码**。有效动作是「访客用该邀请码注册成为团队成员」，之后平台在成员结算时按当期规则向邀请方发放额外补贴。

> **★ 最大坑**：任推邦官网 `/team/` 页上所有「立即注册 / 立即邀请」按钮都指向
> `https://dt.bd.cn/#/pages/login/register?invite_code=66666600&ly=seo_rtb_syqm1`，
> 其中 `66666600` 是**任推邦官网自己的 SEO 投放码**。照搬这个链接，注册关系归官方，本站拿不到任何团队邀请补贴。
> `check_build.py` 已把该邀请码与 `seo_rtb` 参数列为**阻断项**，误填会直接门禁失败。

现状（2026-11-08 回填后）：
- `data/invite.yaml` 的 `cta.url`／`cta.code` 已由景行本人提供的**专属**链接与邀请码替换占位符，模板自动切为可点主按钮；链接域名 `tg.bd.cn`、参数 `qd=self_team_android`，与官方投放链接 `dt.bd.cn` ＋ `66666600` 不同。
- 换链接只改 `cta.url`／`cta.code`／`cta.verify` 三处；`check_build.py` 会校验按钮域名白名单、URL 邀请码与 `cta.code` 一致、页面展示码一致，**换码漏改会直接门禁失败**。
- 邀请码**只落在 `data/invite.yaml` 这一处真源**；模板通过 `$cta.code` 渲染，CSS、关于页、其它文件一律不写死邀请码或链接。
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

`check_build.py` 用 `BANNED` 词表扫描首页与关于页，**连否定式用词也会拦截**（例：「不提供*保底*」曾被拦，已改写成「不提供任何形式的收益保证」）。理由：平台与搜索引擎的机器审核同样按字面判定，否定语境也可能被误伤。

首页与关于页均明确：不是招聘／不是兼职岗位／不是加盟或培训招生；注册与入驻免费；本站不代收费用、不代结算、不提供收益保证；推广需投入时间与渠道资源、结果存在不确定性。

## 三、目录

```
hugo.toml                      站点配置（标题 / 描述 / 首页信息）
data/invite.yaml               唯一真源：cta（邀请入口）+ sections（4 张说明卡片）
layouts/index.html             首页模板（覆盖 define "main"）
content/_index.md              首页对象（仅 front matter）
content/about.md               关于页（非官方声明 / 推广声明 / 合作性质 / 内容边界 / 主体）
assets/css/extended/custom.css 样式（PaperMod 官方扩展位）
themes/PaperMod/               官方最新版 PaperMod vendored 副本（非 submodule）
check_build.py                 构建产物自检（纯标准库、只读 public/）
check_drafts.py                配套稿自检（纯标准库、只读 drafts/NN-*.md 与 data/invite.yaml，55 项）
drafts/                        4 篇项目介绍配套稿＋_选题与交付说明（.gitignore 忽略，不挂站）
.gitignore / README.md
```

> 旧文件 `data/tools.yaml`（4 个网盘/AI 工具卡片）已删除；CSS 类名由 `.tool-*` 改为 `.info-*`／`.invite-*`。

## 四、关键约定

- **链接唯一真源** = `data/invite.yaml`。换邀请链接只改这一个文件的 `cta.url` 与 `cta.verify`，不需要改模板、不需要 Worker。数据访问用 `hugo.Data`（`.Site.Data` 已弃用）。
- `cta.url` 为占位符时，`layouts/index.html` 自动把主按钮渲染为不可点的「入口待开放」并显示阶段提示；替换为真实链接后自动变为带 `rel="sponsored nofollow noopener"` 的可点按钮，并展示 `cta.code` 供手填兜底。**阶段一／阶段二均已实测通过**。
- 主题是**官方最新版整目录副本**：GitHub master HEAD `118119693d8b5ac211b939775678310973bcb232`（2026-10-25，`min_version = 0.158.0`），去掉嵌套 `.git`、不改任何主题源码、零兼容补丁。新版用 `layouts/_partials/`（Hugo 0.146+），与旧版主博客主题的 `layouts/partials/` 不通用，**不要复制主博客主题目录**。
- `disableKinds = ["RSS","taxonomy","term"]` + `taxonomies = {}` 是**主动瘦身**（只有首页＋关于页，sitemap 只留 2 条），不是兼容补丁。
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

`check_build.py` 当前 **阶段一 30 项／阶段二 35 项**，阶段二实测 **35/35、exit 0**：除 canonical、sitemap、robots、CSS 注入、本地路径泄漏外，还检查 4 张说明卡片、推广标识、非招聘／非收益承诺／不收费声明、**无官方 SEO 邀请码**、**无补贴比例与收益诱导词**、阶段一主按钮禁用 / 阶段二按钮 `rel/target` 合规、关于页三类声明；阶段二另加 5 项：data 邀请码有效性、按钮域名白名单 `tg.bd.cn`、URL 邀请码与 `cta.code` 一致、页面展示码一致、data 链接与按钮一致。**负向实测**：把 `cta.code` 改成错码后降到 33/35 并阻断「换码漏改」。

**配套稿机检（2026-11-08 新增，总纲 #24；同日按 #25 升级）**：`python check_drafts.py` 只扫 `drafts/NN-*.md`，并从 `data/invite.yaml` 读 `cta.url`／`cta.code` 作唯一真源，**55 项**：必备声明块／TL;DR／参考区／核验日期／宣传口径联动标注；禁诱导性收益话术（连否定式举例也拦）、禁官方投放码与 `dt.bd.cn`、禁旧占位与「只指向首页入口」旧写法、禁内部路径／图片／互动引导；**逐篇校验统一入口链接逐字一致且只出现一次、URL 邀请码／展示码／手填兜底码与真源一致、推广域名链接唯一且非官方入口**；另查篇幅 ≥800 字、标题不重复、`drafts/` 进 `.gitignore`。与 `check_build.py` **分工互不替代**：后者仍只管 `public/` 首页＋关于页，按 #22/#23 加严不写收益数字。4 篇实测 **55/55、exit 0**；负向测试「真源换码未同步」「稿件挂错码」均被阻断并已恢复；4 篇另过 `check_leak.py scan` 全绿。

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
| **后续更新项目介绍博文（P8）** | ✅ 2026-11-08 启动：4 篇配套稿＋交付说明落 `drafts/`，机检 **55/55**、`check_leak` 全绿；同日按景行令统一刊登同一个团队邀请链接与邀请码（总纲 #25），不再逐项目申请项目级链接；**未挂站、未发布、未排期**，未动 `11_本周排期/` 与 `12_本周稿件/`；挂载方式待另行下令 |

> **★ CF 项目类型坑**：CF 新的「创建应用程序」默认建 **Workers 项目**（`npx wrangler deploy`），Hugo 静态站在 CI 里会被 wrangler 卡在交互式确认而构建失败，手动部署只得到 `Hello world`。必须点创建页底部「**继续前往 Pages**」旧版工作流。旧 Workers 项目未删除、仍连着本仓库，每次 push 会多一条失败构建；清理需景行另行下令。
> **★ 推送网络坑**：WorkBuddy 运行期注入的 `HTTPS_PROXY` 对 GitHub 返回 `CONNECT tunnel 502`，**直连可用**。用推送脚本时须 `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy python git_push.py --repo "$(pwd)"`；直接 `git push` 同理。凭据助手路径报错不影响推送，若报认证失败需景行本人修 helper，AI 不碰凭据。

## 七、上线验收清单

- `python check_build.py` 阶段二 **35/35**、exit 0（须先停 `hugo server` 再干净重建）
- canonical `https://nav.gdaox.top/`、sitemap 2 条均指向正式域名，不是 `pages.dev`／`localhost:1313`
- 首页 200：推广标识／非招聘定性／主按钮**可点且指向专属邀请域**／邀请码展示与 URL 参数一致／4 张说明卡片／补贴声明齐全；CSS 200
- `/about/`、`/sitemap.xml`、`/robots.txt` 线上 200
- 主按钮落地 URL 的**邀请码是本站专属码**（与 `cta.code`、页面展示码三者一致），不是 `66666600`，域名在 `tg.bd.cn` 白名单内
- 归因自测通过后再考虑扩量；**归因不通不扩量**

## 八、红线

上线／push 按景行**逐次下令**执行；AI 不碰凭据（仅复用浏览器已有登录态）、不代点任推邦报备提交；不写补贴比例、不承诺收益、不写诱导性收益话术；不使用官方 SEO 邀请码；**邀请码／邀请链接只落 `data/invite.yaml` 唯一真源，不写死到模板、CSS、关于页或方案文档**（总纲 #25 的 `drafts/` 四篇配套稿属受控例外，须经 `check_drafts.py` 真源一致性校验）；不收任何费用；不上传资源文件到本站；不与主博客互链；不碰 `.env` 等凭据文件。**（总纲 #24）「允许引用官网宣传数字」仅限 `drafts/` 四篇配套稿且须逐篇标注平台宣传口径＋核验日期＋不是收益承诺＋以后台当期为准；首页／关于页仍不写收益数字，诱导性话术与收益承诺在任何页面都不放开**；`drafts/` 不进公开仓库，不挂站需另行下令。
