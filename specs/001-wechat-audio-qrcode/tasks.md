# Tasks: 微信扫码听音频二维码

**Input**: Design documents from `specs/001-wechat-audio-qrcode/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Spec 未要求自动化测试；验收以本地浏览器 + 微信扫码为主（见 quickstart.md）。

**Organization**: 按用户故事分组，便于独立实现与验收。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行（不同文件、无未完成依赖）
- **[Story]**: 所属用户故事（US1, US2），仅 Phase 3/4 任务带此标签
- 描述中含明确文件路径

---

## Phase 1: Setup（项目初始化）

**Purpose**: 创建仓库目录与配置，供后续构建与静态页使用

- [X] T001 Create project structure per plan: `static/`, `build/`, and `dist/` at repo root (static=H5 source, build=scripts, dist=output)
- [X] T002 Create `build/config.example.json` with `sourceDir` and `outputDir` (or equivalent) for build script config
- [X] T003 [P] Add `dist/` to `.gitignore` and document in README or quickstart that dist is build output

---

## Phase 2: Foundational（阻塞性前置）

**Purpose**: 构建脚本与静态页骨架就绪，所有用户故事依赖此阶段

**⚠️ CRITICAL**: 未完成本阶段前不得开始 US1/US2 实现

- [X] T004 Implement build script in `build/build.py` (or `build/build.js`): read config, scan sourceDir for audio (e.g. .flac, .mp3), generate `manifest.json` per data-model.md (items with id, label, url), copy audio to output `audio/`, copy static files to output; fail or warn when no audio files found
- [X] T005 Create `static/index.html`: minimal shell with container for list and loading/error area, load `app.js`
- [X] T006 Create `static/app.js`: fetch `manifest.json` with timeout (10–15s), manage loading and error states per `contracts/directory-page.md`
- [X] T007 [P] Create `static/styles.css`: base layout and styles for list, loading, and error states

**Checkpoint**: 可运行构建得到 `dist/`，打开 `dist/index.html` 能发起 manifest 请求并显示 loading/error；可开始 US1

---

## Phase 3: User Story 1 - 扫码进入目录页并选择播放 (Priority: P1) 🎯 MVP

**Goal**: 用户扫码打开 H5 页，看到音频目录列表，点击一项即可在页内播放；加载有 loading，超时/失败有错误提示，空列表有“暂无可播放音频”。

**Independent Test**: 部署 dist 到公网 URL，用微信扫该 URL 的二维码（或直接打开 URL），能在一分钟内看到列表并选择播放其中一首。

### Implementation for User Story 1

- [X] T008 [US1] In `static/app.js` render manifest `items` as clickable list (display `label`, attach click handler per item)
- [X] T009 [US1] In `static/app.js` implement single `<audio>` playback: on item click set `src` to item `url` and play; stop previous track when switching per data-model and contract
- [X] T010 [US1] In `static/app.js` show loading state while fetching manifest; on timeout (10–15s) or network error show error message per FR-007 and contracts/directory-page.md
- [X] T011 [US1] In `static/app.js` when manifest `items` is empty show "暂无可播放音频" (or equivalent) per contract
- [X] T012 [US1] In `static/app.js` handle per-track playback/load error: show message for that track without white screen per contract

**Checkpoint**: User Story 1 可独立验收：扫码或打开 URL → 见列表 → 点击播放 → 听到音频；异常与空列表有提示

---

## Phase 4: User Story 2 - 二维码为标准制式、微信可扫 (Priority: P2)

**Goal**: 交付物可部署为公网 URL，且该 URL 填入二维彩虹后生成的二维码可被微信稳定识别并跳转到 H5 目录页。

**Independent Test**: 将 H5 公网 URL 填入二维彩虹生成二维码，微信扫一扫能识别并打开目录页，列表与播放正常。

### Implementation for User Story 2

- [X] T013 [US2] Ensure build script outputs to `dist/` using relative paths only (no localhost or absolute paths) so deployment to any static host works
- [X] T014 [US2] Document in `specs/001-wechat-audio-qrcode/quickstart.md` (or README) the step to paste H5 URL into 二维彩虹 to generate WeChat-scannable QR; verify quickstart flow matches current build and deploy steps

**Checkpoint**: User Story 2 可验收：部署 dist → 获得 URL → 二维彩虹生成二维码 → 微信扫码进入目录页并可选播

---

## Phase 5: Polish & Cross-Cutting

**Purpose**: 文档与整体验收

- [X] T015 Update project README with purpose, build command, and deploy pointer (or link to quickstart.md)
- [ ] T016 Run quickstart.md validation: execute build, deploy dist to a test public URL (e.g. GitHub Pages or local tunnel), paste URL into 二维彩虹, scan with WeChat and verify list + play and error/empty states

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 无依赖，可立即开始
- **Phase 2 (Foundational)**: 依赖 Phase 1；完成前不得开始 Phase 3/4
- **Phase 3 (US1)**: 依赖 Phase 2；可与 Phase 4 顺序或并行（若多人）
- **Phase 4 (US2)**: 依赖 Phase 2；可与 Phase 3 顺序或并行
- **Phase 5 (Polish)**: 依赖 Phase 3、4 完成（至少 US1 完成即可做 T016 最小验收）

### User Story Dependencies

- **US1 (P1)**: 仅依赖 Phase 2；无 US2 依赖
- **US2 (P2)**: 仅依赖 Phase 2；实现上依赖“可部署的 dist”，与 US1 共享构建与静态页

### Within Each Phase

- Phase 2: T004 构建脚本应先于 T005–T007（或并行 T005/T007 与 T004，只要 T006 能消费 manifest 格式）
- Phase 3: T008 列表渲染 → T009 播放；T010/T011/T012 可与 T008/T009 穿插或紧随

### Parallel Opportunities

- T003 可与 T001/T002 并行
- T007 可与 T005/T006 并行（不同文件）
- Phase 2 完成后，T008–T012 (US1) 与 T013–T014 (US2) 可由不同人并行
- T015 与 T016 可顺序；T016 依赖可部署的 dist

---

## Parallel Example: User Story 1

```text
# 先完成 T008 列表渲染，再 T009 播放（同文件 app.js，顺序）
# T010 / T011 / T012 可在 T008 后并行（均为 app.js 内不同逻辑块）
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup
2. Phase 2: Foundational
3. Phase 3: User Story 1
4. **STOP and VALIDATE**: 部署 dist，浏览器或微信打开 URL，验证列表 + 选择播放 + loading/错误/空列表
5. 需要时再做 Phase 4（文档与二维码流程）和 Phase 5

### Incremental Delivery

1. Setup + Foundational → 可构建、可打开静态页
2. 完成 US1 → 独立验收（列表 + 播放 + 异常处理）→ 即 MVP
3. 完成 US2 → 文档与部署友好、二维彩虹流程清晰
4. Polish → README + quickstart 全流程验收
