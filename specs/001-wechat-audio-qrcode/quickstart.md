# Quickstart: 微信扫码听音频二维码

**Phase 1 产出** | 构建、部署与生成二维码的简要步骤。

---

## 前置条件

- 本地已安装 **Python 3.10+**（或 Node 18+，若采用 Node 版构建脚本）。
- 指定文件夹内准备好音频文件（如 `孤勇者.flac`、`06. 最伟大的作品.flac`）。
- 具备可部署静态站点的公网托管（如 GitHub 账号、Netlify/Vercel 账号，或自有服务器）。

---

## 1. 构建

1. 进入项目根目录，确认存在构建脚本（如 `build/build.py`）与静态页源码（如 `static/`）。
2. 复制配置模板（可选但推荐）：
   - 复制 `build/config.example.json` 为 `build/config.json`。
   - 若不复制，构建脚本会直接读取 `build/config.example.json`。
3. 配置源文件夹与输出目录（`build/config.json` 或 `build/config.example.json`）：
   - **源文件夹**：存放 `孤勇者.flac`、`06. 最伟大的作品.flac` 等文件的目录。
   - **输出目录**：构建产物目录（如 `dist/`），将包含 `index.html`、`app.js`、`styles.css` 及 `audio/` 下拷贝的音频文件。
4. 执行构建：
   - `python build/build.py`
5. 检查 `dist/`：应包含 `index.html`、`app.js`、`styles.css`、`manifest.json` 及 `audio/` 下所有音频文件。

---

## 2. 部署（公网）

将 `dist/` 整体部署到任意静态托管，获得 **H5 目录页的公网 URL**，例如：

- **GitHub Pages**：将 `dist/` 内容推送到 `gh-pages` 分支或 `docs/`，得到 `https://<user>.github.io/<repo>/`。
- **Netlify / Vercel**：将项目根目录指向仓库，构建命令为上述构建脚本，发布目录为 `dist/`，得到分配的域名或自定义域名。
- **自建**：将 `dist/` 拷贝到 Nginx/其他静态服务器配置的根目录，通过域名访问。

确认在浏览器中打开该 URL 能正常看到目录列表，并能在页内选择播放。

---

## 3. 生成二维码

1. 打开 [二维彩虹](https://www.erweicaihong.com/)（或 spec 约定的其他二维码服务）。
2. 选择“网址/URL”类二维码，将 **上一步得到的 H5 目录页公网 URL** 填入。
3. 生成并下载二维码图片。
4. 使用微信扫一扫测试：扫码后应打开 H5 目录页，列表展示与指定文件夹一致，可选择并播放音频。

---

## 4. 验收检查（与 Spec 对照）

- [ ] 二维码可被微信识别并跳转到 H5 目录页。
- [ ] 目录页展示音频列表（如 孤勇者、06. 最伟大的作品），与源文件夹一致。
- [ ] 点击某一项可正常播放，音质可接受。
- [ ] 加载中有 loading；超时或失败有错误提示；目录为空时有“暂无可播放音频”类提示。
