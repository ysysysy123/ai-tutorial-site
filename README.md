# 秋招算法与 AI 教程阅读站模板

这是一个独立的 MkDocs 网站项目。教程取自 [Akun-python/autumn-recruitment](https://github.com/Akun-python/autumn-recruitment) 的 `main` 分支，个人 Obsidian 笔记继续保存在原学习库。

模板提供章节导航、中文与英文搜索、Markdown 和 Notebook 阅读、公式、Mermaid 图、深浅色切换和 Notebook 下载。网站展示 Notebook 已保存的输出，构建时不运行 Python。没有保存输出的 Notebook 仍然只有文字和代码。

## 1. 本地预览

进入这个模板目录，在终端执行：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
git clone --depth 1 --branch main https://github.com/Akun-python/autumn-recruitment.git _source
.venv/bin/python scripts/prepare_docs.py
.venv/bin/python -m mkdocs serve -f mkdocs.generated.yml
```

打开终端显示的本地地址，通常为 `http://127.0.0.1:8000/`。用 `Ctrl+C` 停止预览。

命令明确使用本项目的虚拟环境，避免误调用系统 MkDocs。依赖和教程已经下载、导航已经生成时，直接执行最后一条启动命令。

Windows PowerShell 中，将 `.venv/bin/python` 替换为 `.venv\Scripts\python.exe`。

## 2. 新建 GitHub 仓库并上传模板

在 GitHub 创建名为 `ai-tutorial-site` 的 **Public** 仓库。保持空仓库，不额外生成 README、许可证或 `.gitignore`。

回到模板目录执行以下命令，将 `YOUR_USERNAME` 改成自己的 GitHub 用户名：

```bash
git init -b main
git add .gitignore README.md requirements.txt mkdocs.yml scripts overrides .github
git commit -m "Add tutorial reading site"
git remote add origin https://github.com/YOUR_USERNAME/ai-tutorial-site.git
```

如果终端尚未登录 GitHub，可先执行 `gh auth login`，再执行 `gh auth setup-git`。按交互提示登录即可，无需把凭据写进模板。

教程下载目录 `_source/` 和生成网页 `site/` 已被忽略，自己的仓库只保存网站配置。

## 3. 启用 GitHub Pages，再推送

进入新仓库的 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。然后执行：

```bash
git push -u origin main
```

进入仓库的 **Actions** 标签页，等待 `Build and deploy tutorial site` 成功。部署地址可以在工作流结果或 **Settings → Pages** 中查看。

如果之前已推送并触发了失败的构建，在启用 Pages 后进入 **Actions → Build and deploy tutorial site → Run workflow** 手动重跑即可。

通常地址为 `https://YOUR_USERNAME.github.io/ai-tutorial-site/`，以 GitHub 实际显示的地址为准。模板在 Actions 中自动读取 Pages 地址，无需在配置文件中手填用户名。

首次发布后，用手机打开部署地址，检查章节目录、搜索、公式和图片，再使用浏览器的“添加到主屏幕”。添加到主屏幕只提供入口，不代表已经支持离线阅读。

## 4. 更新教程

线上工作流每周一 UTC 06:23 读取上游最新 `main` 并重新构建；修改自己的配置或手动 **Run workflow** 也会更新。上游推送不会直接触发本仓库，更新发生在下次运行时。

GitHub 对连续 60 天没有仓库活动的公开仓库会停用定时工作流。如果自动更新停了，在 **Actions** 中重新启用该工作流。已有网站仍可访问。

本地更新时执行：

```bash
git -C _source pull --ff-only
.venv/bin/python scripts/prepare_docs.py
.venv/bin/python -m mkdocs serve -f mkdocs.generated.yml
```

## 目录说明

| 文件 | 用途 |
|---|---|
| `mkdocs.yml` | 阅读界面、搜索、Notebook 和公式配置 |
| `scripts/prepare_docs.py` | 从上游目录自动生成章节导航 |
| `scripts/notebook_links.py` | 避免同名教程覆盖，转换 Notebook 内站内链接并统一图表加载 |
| `overrides/` | Notebook 下载、署名、手机样式与 Mermaid 渲染 |
| `.github/workflows/pages.yml` | 读取上游、构建、部署和每周更新 |

模板保留上游完整目录，减少图片路径变动；Markdown 网页使用 `.html` 路径，Notebook 使用 `.notebook.html` 路径，避免同名 Markdown 和 Notebook 相互覆盖，也让 Notebook 内的相对图片路径保持有效。源仓库不存在的链接仍需在上游或本站单独修正。

## 内容来源与许可

教程版权归原贡献者所有。原仓库的 MIT 许可证及版权声明随下载目录保留，并作为 `LICENSE` 文件发布；每篇页面都提供来源和许可证链接。教程中引用的第三方图片仍保留各自的来源与许可说明，仓库 MIT 许可不能替代第三方素材的许可。

此模板没有配置离线缓存、跨设备学习进度或浏览器运行 Python。公式和 Mermaid 从公共 CDN 加载，阅读时需要能访问这些地址。

## 本次验证

2026-10-10：本地成功生成 232 篇 Notebook 网页和 68 篇 Markdown 网页；同名文档使用独立地址。抽查 PPO/GRPO 教程的公式、Mermaid、图片与下载入口；搜索 `RoPE` 返回 19 个结果；390 像素手机、820 像素平板和默认电脑视口通过抽查，手机与平板正文没有整页横向溢出。

原文仍有少量过时锚点；语音模块中指向深度学习“模型笔记”目录的链接没有对应网页首页，可从侧边导航进入该目录中的教程。全文搜索索引约 23 MB，首次加载搜索在手机网络下可能较慢。

本项目仓库为 [ysysysy123/ai-tutorial-site](https://github.com/ysysysy123/ai-tutorial-site)。在线阅读地址为 [秋招算法与 AI 学习教程](https://ysysysy123.github.io/ai-tutorial-site/)，构建与部署状态可在 [Actions](https://github.com/ysysysy123/ai-tutorial-site/actions) 中查看。

参考：[GitHub Pages 工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter)、[Material 公式配置](https://squidfunk.github.io/mkdocs-material/reference/math/)、[定时工作流停用规则](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)。
