# 微信扫码音频目录页

扫码后打开一个 H5 页面，显示音频目录（如 `孤勇者.flac`、`06. 最伟大的作品.flac`），用户可选择并播放。

## 构建

1. 复制 `build/config.example.json` 为 `build/config.json`（可选，不复制则使用示例配置）。
2. 执行：

```powershell
python build/build.py
```

构建产物输出到 `dist/`，包括：

- `dist/index.html`
- `dist/app.js`
- `dist/styles.css`
- `dist/manifest.json`
- `dist/audio/*`

## 部署与二维码

部署 `dist/` 到任意公网静态托管，拿到页面 URL 后，按 `specs/001-wechat-audio-qrcode/quickstart.md` 中步骤粘贴到二维彩虹生成二维码。
