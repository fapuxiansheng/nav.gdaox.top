# promo-site｜推广二级域名导航站

独立 Hugo + PaperMod 静态站，域名 `nav.gdaox.top`，部署目标 Cloudflare Pages。
当前为**阶段一「空链版」**：工具介绍、广告标识、佣金声明、关于页齐全，卡片按钮自动渲染为不可点的「入口待开放」，用于任推邦报备截图，无任何坏链。

**本地状态（2026-11-07）**

- **主题**：PaperMod 官方 GitHub master HEAD `118119693d8b5ac211b939775678310973bcb232`（2026-10-25），直接拉取后 vendored 进仓库，**零补丁**；主题 `min_version = 0.158.0`。旧版主博客主题副本已弃用。
- **构建**：Hugo v0.166.0 `hugo --gc --minify` exit 0、**0 条 WARN**；`python check_build.py` **19/19 通过、阻断 0**；public 仅 6 个文件（首页／关于／CSS／404／robots／sitemap），sitemap 2 条，canonical 指向 `https://nav.gdaox.top/`。
- **仓库**：本地独立 git 仓库（分支 `main`，首次提交 `4f2b9fd`，134 个文件）；**2026-11-07 13:40 已推送到 `https://github.com/fapuxiansheng/nav.gdaox.top`**（空仓库首次推送，远端 HEAD = 本地 `01df2cd0e591380fffabb9d35cd6271d0859b352`，`main` 已设 upstream）。提交作者沿用本机全局配置 `LiuChuan <oysq95@163.com>`。
- **口径定案（13:04）**：景行令「按建议执行」→ 首期 4 个项目（3 网盘＋1 AI）、挂链扩口径已按 `AGENTS.md` 第 5 条记入总纲变更台账 **#21**、关于页主体沿用株洲观道行文化科技有限公司、短链点击统计层不启用。站点代码未因此改动。
- **预览链接（13:15，仅预览）**：已把构建产物 `public/` 通过 WorkBuddy 应用发布成在线预览 `https://netdisk-ai-tools-nav.app.workbuddy.host/?sharecode=HSD6UYHMRP`（首页 200、4 张卡片／广告标识齐全，CSS 与 `/about/` 经分享鉴权后 200）。**这不是 `nav.gdaox.top` 正式上线**：canonical／sitemap／robots 仍指向正式域名；分享链接的子路径需带 cookie 或 sharecode，匿名请求会返回 403「链接不完整」，属平台鉴权行为、非站点故障。重建 `public/` 后须重新发布才会同步线上预览。
- **未执行（账号侧，仍由景行本人操作）**：CF Pages Connect to Git、`nav.gdaox.top` 自定义域名绑定 / DNS / SSL、正式上线、任推邦报备。当前 `nav.gdaox.top` 解析返回 NXDOMAIN，GitHub Pages 未启用（API 404），**代码已上云但站点尚未对外可访问**。

## 目录

```
hugo.toml                      站点配置
data/tools.yaml                链接唯一真源（4 张卡片）
layouts/index.html             首页模板（覆盖 define "main"）
content/_index.md              首页对象（仅 front matter）
content/about.md               关于页（主体 / 广告声明 / 内容边界）
assets/css/extended/custom.css 卡片样式（PaperMod 官方扩展位）
themes/PaperMod/               官方最新版 PaperMod vendored 副本（非 submodule）
check_build.py                 构建产物自检（纯标准库、只读 public/）
.gitignore / README.md
```

## 关键约定

- 链接唯一真源 = `data/tools.yaml`。换推广链接**只改这一个文件**的 `url` 与 `verify`，不需要改模板、不需要 Worker。
- `url` 为 `REPLACE_WITH_RENTUIBANG_URL` 时，`layouts/index.html` 自动把按钮渲染为不可点的「入口待开放」并显示阶段提示；替换成真实链接后自动变为带 `rel="sponsored nofollow noopener"` 的可点按钮，**一次 push 即切正式版**，模板不用动。数据访问用 `hugo.Data`（`.Site.Data` 已弃用）。
- 主题是**官方最新版整目录副本**：从 GitHub 拉取、去掉嵌套 `.git`、不改任何主题源码。新版用 `layouts/_partials/`（Hugo 0.146+ 新布局结构），与旧版主博客主题的 `layouts/partials/` 不通用，**不要再复制主博客主题目录**。vendored 而非 submodule 的原因：CF Pages 不需要递归子模块，离线可构建，版本可锁死在一个 commit。
- `disableKinds = ["RSS","taxonomy","term"]` + `taxonomies = {}` 是**主动瘦身**（本站只有首页＋关于页，sitemap 只保留 2 条），**不是兼容补丁**；已验证去掉这些项、用官方最新版主题也能在 Hugo 0.166 原生构建通过。
- 首页由 `layouts/index.html` 的 `define "main"` 渲染，PaperMod 的 head/footer/menu 仍由主题 `baseof.html` 提供。**不要**把卡片写回 `content/_index.md` 的内联 HTML（Goldmark 默认会丢弃）。
- `locale = "zh-cn"`（不是已弃用的 `languageCode`）；`[markup.goldmark.renderer] unsafe = false` 保持默认，不开放注入面。

## 本地构建与门禁

```bash
cd "E:/我的文档/文档/Default Project/15_项目/promo-site"
hugo version                              # v0.166.0 → CF Pages 的 HUGO_VERSION 填 0.166.0
hugo server -D                            # 本地预览 http://localhost:1313
rm -rf public && hugo --gc --minify       # 复现线上构建
python check_build.py                     # 产物自检；0=全绿，1=阻断
```

> **坑**：`--cleanDestinationDir` 并**不清理**上一轮遗留的文件。换主题、改 `disableKinds` 或 CSS 后必须 `rm -rf public` 再构建，否则 public 里会残留旧的空分类页与旧 fingerprint CSS，导致产物清单误判。

`check_build.py` 自动识别阶段一/阶段二：阶段一校验 4 个按钮全部禁用且无坏链；阶段二校验 4 个可点按钮的 `rel/target` 合规且无占位符。同时检查 canonical、广告标识、佣金声明、sitemap 域名、CSS 注入、本地路径泄漏。

## 主题升级（可选）

```bash
TMP=../_papermod_latest_tmp
git clone --depth 1 https://github.com/adityatelange/hugo-PaperMod.git "$TMP"
git -C "$TMP" log -1 --format="%H %ci %s"     # 记录新 commit sha，写进本文件「本地状态」
mv themes/PaperMod ../_改前备份/推广导航站_20261107/PaperMod_backup
cp -r "$TMP" themes/PaperMod && rm -rf themes/PaperMod/.git "$TMP"
rm -rf public && hugo --gc --minify && python check_build.py
```

升级后必须复跑门禁；若新版主题抬高 `min_version`，CF Pages 的 `HUGO_VERSION` 要同步上调。

## 部署（步骤 1 已完成；步骤 2–5 由景行本人在账号下执行）

1. **已完成（2026-11-07 13:40）**：景行新建空的独立 GitHub 仓库 `fapuxiansheng/nav.gdaox.top`（公开、默认分支 `main`）并给出 URL，按逐次下令完成首次推送：

```bash
cd "E:/我的文档/文档/Default Project/15_项目/promo-site"
git remote add origin https://github.com/fapuxiansheng/nav.gdaox.top.git
git fetch origin --quiet                       # 项目纪律：push 前必先 fetch
python "E:/我的文档/文档/Default Project/WorkBuddy-OC/06_脚本/根目录/git_push.py" \
  --repo "E:/我的文档/文档/Default Project/15_项目/promo-site" --max-attempts 3 --max-seconds 150
git branch --set-upstream-to=origin/main main  # 脚本 push 不带 -u，补设 upstream
```

后续改文件只需正常 `git add` → `git commit` → `git push`（已设 upstream）；走项目脚本时记得带 `--repo` 指向本目录。

> **★ 推送网络坑（本机环境）**：WorkBuddy 运行期注入的 `HTTPS_PROXY=http://127.0.0.1:<端口>` 对 GitHub 会返回 `CONNECT tunnel failed, response 502`，而**直连可用**。可靠推送脚本会自动读取该代理，所以必须临时去掉它：`env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy python git_push.py --repo …`（脚本随即走「直连 + 钉 IPv4 + HTTP/1.1」策略，实测第一次即成功）。同理，直接 `git push` 也要 `env -u … git push`。脚本本次另报 `git-credential-manager.exe store: No such file or directory`（凭据助手路径配置有误）但**推送本身成功**；若日后报认证失败，需景行本人修 credential helper 或重新登录，AI 不碰凭据。

2. Cloudflare → Workers & Pages → 创建 → Pages → Connect to Git，选该仓库：

| 设置 | 值 |
|---|---|
| Framework preset | Hugo |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| Root directory | 留空 |
| Production branch | `main` |
| 环境变量 | `HUGO_VERSION` = `0.166.0` |

3. Custom domains → Set up a custom domain → 填 **`nav.gdaox.top`**（主机名，不带路径）。域名 NS 在 CF，CNAME 会自动添加；等 SSL 签发完成后访问 `https://nav.gdaox.top/`。

4. 任推邦逐项目绑定服务商 → 拿 UID/UK 码与绑定截图 → 「申请推广」填「自有网站 + 落地页 URL + 首页/关于页截图」→ 等审核。**逐项目核对当期「有效动作定义」**（网盘类＝注册＋首次转存，AI 类机制不同）。

5. 审核通过后，把 `data/tools.yaml` 的占位符换成真实分享链接/口令，改 `verify` 日期，复跑 `rm -rf public && hugo --gc --minify` + `python check_build.py`（应自动切到「正式版」判定），再 commit + push，CF 自动重建。

## 上线验收

- `python check_build.py` 19/19 通过、exit 0
- canonical / sitemap.xml / robots.txt 均指向 `https://nav.gdaox.top/`，不是 `pages.dev`
- `/about/`、`/sitemap.xml`、`/robots.txt` 线上 200；首页可见「广告｜推广链接」与佣金声明
- 归因自测：无痕窗口点卡片 → 落地 URL 参数完整 → 完成一次注册+转存 → 任推邦后台 T+2 看回传。**归因不通不扩量。**

## 红线

不自动发布上线；不上传资源文件到本站；不堆项目（首期 4 个）；不放佣金数字、不承诺收益；仅公版/授权/自产资源；不与主博客互链；不碰 `.env` 等凭据文件。
