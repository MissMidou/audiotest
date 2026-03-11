# Implementation Plan: 微信扫码听音频二维码

**Branch**: `001-wechat-audio-qrcode` | **Date**: 2026-03-11 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/001-wechat-audio-qrcode/spec.md`

## Summary

- **需求要点**：生成标准二维码（二维彩虹），微信扫码后打开 H5 目录页，页面展示音频列表（如 孤勇者.flac、06. 最伟大的作品.flac），用户选择一项在页内播放；本方案交付可部署的静态 H5 站点与音频托管方式，部署后得到 URL 用于生成二维码。
- **技术路线**：静态站点（单页 HTML + CSS + JS），构建时扫描指定文件夹生成目录数据并打包音频；部署至任意公网静态托管；二维码由用户将 H5 页面 URL 填入二维彩虹生成。

## Technical Context

**Language/Version**: HTML/CSS/JavaScript（前端）；构建脚本 Python 3.10+ 或 Node 18+（二选一，见 research.md）  
**Primary Dependencies**: 无框架依赖；可选轻量构建工具（如脚本内联列表或生成 manifest.json）  
**Storage**: N/A（源音频来自本地文件夹；部署后为静态文件）  
**Testing**: 本地浏览器 + 微信扫码验收；构建脚本可加单元/集成测试  
**Target Platform**: 任意可托管静态文件的公网环境；用户端为微信内置浏览器  
**Project Type**: 静态站点 + 小型构建/打包工具  
**Performance Goals**: 目录页加载与列表展示在 10–15 秒内完成（与 FR-007 一致）；1 分钟内完成选择并开始播放（SC-001）  
**Constraints**: 纯静态、无服务端逻辑；需兼容微信内置浏览器；支持 FLAC 播放（若环境不支持则 research 中记录备选）  
**Scale/Scope**: 单文件夹内多首音频、单二维码入口；无多租户或动态目录需求  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- 当前仓库 `.specify/memory/constitution.md` 仍为模板占位，未定义具体原则与门禁。
- **结论**：无强制门禁，按本 plan 与 spec 执行即可；若后续订立 Constitution 再补检。

## Project Structure

### Documentation (this feature)

```text
specs/001-wechat-audio-qrcode/
├── plan.md              # 本文件
├── research.md          # Phase 0 调研结论
├── data-model.md        # Phase 1 数据与状态
├── quickstart.md        # Phase 1 构建与部署指引
├── contracts/           # Phase 1 页面/目录契约（可选）
└── tasks.md             # Phase 2 由 /speckit.tasks 生成
```

### Source Code (repository root)

```text
# 静态站点 + 构建脚本（单仓库）
static/                  # 或 frontend/ — 静态 H5 源码
├── index.html           # 目录页入口，内嵌或加载目录数据
├── app.js               # 列表渲染、播放、loading/错误处理
├── styles.css           # 样式
└── assets/              # 可选图标等

build/                   # 构建脚本与配置
├── build.py             # 或 build.js：扫描文件夹、生成目录、复制音频到输出目录
└── config.example.json  # 示例：源文件夹路径、输出路径等

dist/                    # 构建产物（可 gitignore），部署此目录
├── index.html
├── app.js
├── styles.css
└── audio/               # 拷贝后的音频文件（如 孤勇者.flac, 06. 最伟大的作品.flac）
```

**Structure Decision**: 采用单项目“静态站点 + 构建脚本”结构；无后端、无数据库，部署 `dist/` 至任意静态托管即可，二维码由用户在二维彩虹填写 H5 页面 URL 生成。

## Complexity Tracking

> 当前无 Constitution 违规项；若后续引入原则冲突再在此表说明。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| —         | —          | —                                   |
