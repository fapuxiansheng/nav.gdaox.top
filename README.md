# promo-site｜推广二级域名导航站

独立 Hugo + PaperMod 静态站，域名 `nav.gdaox.top`，部署目标 Cloudflare Pages。
当前为**阶段一「空链版」**：工具介绍、广告标识、关于页齐全，卡片按钮自动渲染为「入口待开放」，用于任推邦报备截图，无任何坏链。

**本地状态（2026-11-07）**：Hugo v0.166.0 `hugo --gc --minify --cleanDestinationDir` exit 0；`python check_build.py` **19/19 通过、阻断 0**；public 仅 6 个文件（首页／关于／CSS／404／robots／sitemap，sitemap 2 条 URL）。**尚未建 GitHub 仓库、未 push、未绑域名、未上线、未提交报备。**

## 目录

```
hugo.toml                     站点配置
data/tools.yaml               链接唯一真源（4 张卡片）
layouts/index.html            首页模板（覆盖 define "main"）
content/_index.md             首页对象（仅 front matter）
content/about.md              关于页（主体 / 广告声明 / 内容边界）
assets/css/extended/custom.css 卡片样式（PaperMod 官方扩展位）
themes/PaperMod/              主博客同版 vendored 主题副本
check_build.py                构建产物自检（纯标准库、只读 public/）
.gitignore / README.md
```

## 关键约定

- 链接唯一真源 = `data/tools.yaml`。换推广链接**只改这一个文件**的 `url` 与 `verify`，不需要改模板、不需要 Worker。
- `url` 为 `REPLACE_WITH_RENTUIBANG_URL` 时，`layouts/index.html` 自动把按钮渲染为不可点的「入口待开放」，并显示「资料入口准备中」提示；替换成真实链接后按钮自动变为可点击（带 `rel="sponsored nofollow noopener"`），**一次 push 即切正式版**，模板不用动。
- 主题 `themes/PaperMod` 是**从主博客同版复制的 vendored 副本**（非 submodule）：与主博客风格严格一致、离线可构建、CF Pages 不需要递归子模块。更新主题时从主博客仓库同步，或重新拉取官方版本覆盖。
- 主题副本已做 Hugo 0.166 兼容修复（3 处 `partial "partials/…"` 前缀去掉；`opengraph.html` / `twitter_cards.html` 移除已废弃的 `site.Social` 分支）。配合 `disableKinds` + `taxonomies = {}` 关掉 RSS 与空分类页，避开旧主题对 `site.Author` 等已移除字段的引用。
- 首页由 `layouts/index.html` 的 `define "main"` 渲染，PaperMod 的 head/footer/menu 仍由主题 `baseof.html` 提供。**不要**把卡片写回 `content/_index.md` 的内联 HTML（Goldmark 默认会丢弃）。
- 构建只剩 1 条主题自身的 `.Language.LanguageDirection` deprecated WARN，不阻断；CF Pages 固定同一 Hugo 版本，不会漂移。

## 本地构建与门禁

```bash
cd "E:/我的文档/文档/Default Project/15_项目/promo-site"
hugo version                                    # v0.166.0 → CF Pages 的 HUGO_VERSION 填 0.166.0
hugo server -D                                  # 本地预览 http://localhost:1313
hugo --gc --minify --cleanDestinationDir        # 复现线上构建（本地反复构建务必带 cleanDestinationDir）
python check_build.py                           # 产物自检；0=全绿，1=阻断
```

`check_build.py` 自动识别阶段一/阶段二：阶段一校验 4 个按钮全部禁用且无坏链；阶段二校验 4 个可点按钮的 `rel/target` 合规且无占位符。同时检查 canonical、广告标识、佣金声明、sitemap 域名、CSS 注入、本地路径泄漏。

## 部署（以下动作由景行本人在账号下执行，AI 不碰凭据、不推送）

1. 在 GitHub 新建**独立**仓库（不并入主博客仓库），然后：

```bash
cd "E:/我的文档/文档/Default Project/15_项目/promo-site"
git init
git add .
git commit -m "init: 推广导航站空链版"
git branch -M main
git remote add origin <你的 GitHub 仓库 URL>
git push -u origin main
```

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

5. 审核通过后，把 `data/tools.yaml` 的占位符换成真实分享链接/口令，改 `verify` 日期，复跑 `hugo …` + `python check_build.py`（应自动切到「正式版」判定），再 commit + push，CF 自动重建。

## 上线验收

- `python check_build.py` 19/19 通过、exit 0
- canonical / sitemap.xml / robots.txt 均指向 `https://nav.gdaox.top/`，不是 `pages.dev`
- `/about/`、`/sitemap.xml`、`/robots.txt` 线上 200；首页可见「广告｜推广链接」与佣金声明
- 归因自测：无痕窗口点卡片 → 落地 URL 参数完整 → 完成一次注册+转存 → 任推邦后台 T+2 看回传。**归因不通不扩量。**

## 红线

不自动发布上线；不上传资源文件到本站；不堆项目（首期 4 个）；不放佣金数字、不承诺收益；仅公版/授权/自产资源；不与主博客互链；不碰 `.env` 等凭据文件。
