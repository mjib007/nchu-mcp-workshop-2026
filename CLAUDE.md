# CLAUDE.md

This file provides guidance to Claude Code / Claude Agent SDK clients when working on this repository.

## 本 repo 目的

這是一份「三小時 MCP 入門工作坊」的教材集散地，受眾為大專院校教師（非必要為資工背景）。所有內容以 [NCHU AI 學伴（UDICatNCHU/claude-mcp-project）](https://github.com/UDICatNCHU/claude-mcp-project) 作為實際案例。

原始素材於 2026-04-24 從 `claude-mcp-project/teaching-materials/` 搬出、獨立成本 repo，便於獨立版控與分享。

## 受眾假設

- 聽眾熟悉 LLM 使用經驗，但對 RAG / Tool Use / MCP 的差異尚未建立清楚的心智模型
- 聽眾不一定每天寫程式，技術細節需「概念為主、關鍵程式片段佐證」，避免逐行解釋
- 期望聽眾課後能自行判斷：自己的研究／教學情境，該選 RAG、Tool Use 還是 MCP

## 課程結構（總 180 min = 3 小時，含 10 min 休息）

| 段落 | 時間 | 主題 | 主要檔案 | 狀態 |
|------|------|------|---------|------|
| 第一段 | 40 min | **Why MCP** | `01-why-mcp.pptx`、`01-why-mcp-video.mp4`（3 min Manim 長片） | ✅ 初稿完成（17 張 + v2 影片）|
| 第二段 | 40 min | **How MCP Works** | `02-how-mcp-works.pptx`（22 張，含附錄）、`02-mcp-connection-video.mp4`（2:17 Manim 影片） | ✅ v3 完成（pptx 與影片已對齊）|
| 休息 | 10 min | | | |
| 第三段 | 35 min | **Agentic Tool Loop** | `03-agentic-tool-loop.pptx`（8 張，A2 cut）、`03-agentic-loop-video.mp4`（1:07 Manim 影片）、`sonnet-running-example.pptx` | ✅ pptx + 影片 D 方案完成 |
| 第四段 | 45 min | **動手做（mini-project 實作）** | `04-hands-on-lab.pptx`（12 張）、`04-hands-on-lab.md` + `mini-project/` + `infra/` | ✅ 完成 |
| 第五段 | 10 min | **實務考量（收尾）** | `05-practical-considerations.md`、`haiku-alignment-report.pptx` | ✅ 完成（md 版本，HTML 動畫已移除） |

## 各段內容規劃

### 第一段：Why MCP（40 min）
- LLM 擅長的事（語言理解、推理、程式碼生成、知識回答）
- LLM 的天花板（知識截止、無私有資料、不能執行動作、幻覺）
- 策略 A：RAG — 概念 + 流程圖 + 概念程式碼 + 優缺點
- 策略 B：Tool Use — 概念 + 流程圖 + Claude API 範例 + 優缺點
- Tool Use 的 N×M 痛點（每個 App × 每個資料源都要個別整合）
- 策略 C：MCP — 統一協定解耦，N+M 模式
- **三者深入比較**（比較表 + 適用場景分析 + 可混用說明，5+ 頁）
- MCP 核心概念（Host / Client / Server / Tool 四大角色）
- MCP 通訊協定（JSON-RPC 2.0 範例）
- 興大 AI 學伴案例引子（33 工具、9 大分類）

### 第二段：How MCP Works（40 min）
- **結構（v4）**：先講 function calling 底層，再用 frame story 串 MCP
  - Section 01 Function Calling 怎麼運作（LLM 只吐字串、subprocess.run 那道門、安全警告、LLM ↔ Harness 職責分工）
  - Section 02 從一個查詢開始（場景 → Parent 開出 Child → 兩階段握手 → 工具呼叫）
  - Section 03 Tool 註冊與描述（JSON Schema、description 對 LLM 的重要性）
  - Section 04 Client 整合機制（工具清單如何餵給 LLM）
  - 附錄：REST vs JSON-RPC、JSON-RPC 三種訊息類型（給技術 curious 老師，可跳）
- 搭配影片：`02-mcp-connection-video.mp4`（2:17，Parent / Child / 兩階段握手 checkbox / 第 4 個請求 / frame closure）
- pptx 重生工具：`tools/build-02-slides.py`（程式化生成，import `lib_newstyle`，避免手動同步影片內容）

### 第三段：Agentic Tool Loop（35 min）
- 完整查詢流程 walk-through（使用者提問 → 最終回覆）
- LLM 自主選工具（`tool_use` block → `tool_result` → 多輪迭代）
- `maxIterations` 限制與最後一輪強制回覆機制
- Live Demo：現場操作系統
- 搭配素材：`sonnet-running-example.pptx`（HTML 動畫已移除，預計改 Manim 影片）

### 第四段：動手做（45 min，hands-on 主場）

現版 `04-hands-on-lab.md` 是學員端 landing page，指向可跑的 `mini-project/`。`04-hands-on-lab.pptx`（12 張）是**現場講師開場用**的投影片，涵蓋本節目標、時間配置、架構回顧、Quick Start、L1 四步驟分解、卡點速查、收尾鋪陳 Segment 5；由 `tools/build-04-slides.py` 以 python-pptx 自動生成（共用 `tools/lib_newstyle.py` 設計系統），視覺遵循 repo 的 violet primary + pastel cards 風格規範。

**作為工作坊的 hands-on 主場**，學員現場完成 L1（換自己領域的 JSON），讓 Segment 1–3 的概念在自己電腦上發生。

**45 分鐘時間配置**：
- 0–8 min：講師 demo + 學員同步 `setup.sh`
- 8–18 min：L1 Step 1–2（觀察 + 換 JSON）
- 18–32 min：L1 Step 3–4（改 docstring + 重啟驗證）
- 32–40 min：交叉展示 — 幾位老師用自己領域資料 demo
- 40–45 min：Q&A + 鋪陳 Segment 5

三關 Lab 路徑：
- **L1**：換 JSON 做你領域的助理（**課堂現場必做**）
- **L2**：加一支有參數的搜尋工具（課後自修）
- **L3**：呼叫外部 API（課後自修）

Workshop 現場可連 NCHU vLLM 端點（`infra/serve-*.sh` 提供 Gemma 4 / Qwen Coder）。

### 第五段：實務考量 收尾（10 min）

現版 `05-practical-considerations.md` 結構為「四大支柱」，**順序從剛做的 mini-project 往外擴**（Scale → Quality → Model → Cost）：

- **§1 Scale 質變**（3 tools → 239 tools 的五個質變：context 爆量 / 語意混淆 / 多輪 context / 安全 / observability）
- **§2 Tool-calling 品質陷阱**（docstring 設計、邊界防禦、錯誤當資料、Gemma 4 thinking marker strip）
- **§3 模型選擇**（Task-complexity gradient；引 benchmark 佐證 Gemma 4 在 tool-calling 任務打平 Claude；multi-provider adapter）
- **§4 成本**（10 人 3 小時 workshop 真實帳、prompt caching、失控情境、Anthropic Console 護欄、本地 vs 雲端長期帳）

**10 分鐘塞不下四支柱**。講師於現場依聽眾屬性**擇一深入 ~7 min**，其餘三節各一句帶過，最後 ~2 min Q&A。md 保留完整四節供課後閱讀。

搭配素材：`haiku-alignment-report.pptx`（可作為 §4 成本中 Haiku alignment 的延伸閱讀；HTML 動畫已移除）。

## 範圍：本 repo 只含教材

本 repo（public）只包含**工作坊教材**：投影片、md、mini-project hands-on、Manim 影片、landing page。

線上課程小助教（TA 問答服務）是**另一個獨立的非公開專案**，不在本 repo，相關開發請在該專案進行。

## 教材風格規範

- 配色：Violet primary `#7B5CF5`（+ `VIOLET_DEEP #5B3ED9`）搭 Orange / Teal / Pink / Blue accents，所有 card 用對應 `*_PASTEL` 底色；finale / transition 頁使用 Midnight `#0F1429`
- 字型：Arial Black（重粗體標題）／ Calibri（內文，副標常用 italic muted）／ Consolas（程式碼，柔化的 syntax highlighting）
- 設計系統集中於 `tools/lib_newstyle.py`（色票 + `metadata_bar` / `pastel_card` / `circle_number` / `code_block` / `callout_box` / `finale` 等版面 primitives）；所有 `tools/build-*-slides.py` 共用，確保跨段視覺一致
- 簡報以 `.pptx` 產出（由 `build-*-slides.py` 程式化重生，方便迭代）；動畫已全面改用 Manim 渲染為 `.mp4`（早期的 `.html` 互動動畫已全數移除）
- 技術深度：概念為主，穿插關鍵程式片段；RAG / Tool Use / MCP 比較做深入版（5+ 頁）
- 每段至少 1 個來自 NCHU AI 學伴 repo 的具體案例（例如 33 工具分類、Haiku alignment、agentic loop）
- 程式片段以說明「概念」為主，避免逐行解釋；複雜流程用動畫或圖示取代文字

## 檔案命名慣例 + 目錄歸類

頂層按產出類型分資料夾，root 只留少數入口 md：

- **`slides/`**：所有講課投影片 `.pptx`（`0X-主題.pptx` + haiku + sonnet）。由 `tools/build-*-slides.py` 程式化產生並寫入此。
- **`videos/`**：影片生產檔 —— Manim `*-video.py` + 渲染出的 `*-preview.mp4` + `*-youtube.md`（YouTube 發佈素材）
- **`scripts/`**：講師用 —— `*-live-demo-script.md` + `course-notes-draft.md`（草稿）
- **root 只留**：`04-hands-on-lab.md`、`05-practical-considerations.md`、`haiku-alignment-report.md`（學員/讀者入口）+ `README.md` / `CLAUDE.md`
- **`mini-project/`**：學員端可跑 code（含 `colab/` 零安裝版）；`setup.sh` 在其 root
- **`infra/`**：工作坊主辦端 vLLM，學員不碰
- **`docs/`**：GitHub Pages landing page

## Repo 結構

```
repo root/
├── 04-hands-on-lab.md                 第四段動手做 landing（學員入口）
├── 05-practical-considerations.md     第五段實務考量收尾
├── haiku-alignment-report.md          Haiku 優化報告（第五段延伸閱讀）
│
├── slides/                            所有 .pptx（01–05 + haiku + sonnet,由 tools/ 產出）
├── videos/                            Manim *.py + *-preview.mp4 + *-youtube.md
├── scripts/                           *-live-demo-script.md + course-notes-draft.md
│
├── tools/                             投影片生成腳本（共用 lib_newstyle.py）
│   ├── lib_newstyle.py                色票 + 版面 primitives（violet 主視覺）
│   ├── build-0X-slides.py             各段 .pptx 程式化產生 → 寫入 slides/
│   └── sync-to-drive.sh               rclone 同步教材到 Google Drive
├── mini-project/                      學員端 hands-on 可跑 code
│   ├── backend-node/                  Express + LLM client + MCP client
│   ├── mcp-server-py/                 5 支 FastMCP 工具（hello/teachers/weather/library/arxiv）
│   ├── web/                           極簡 vanilla JS chat UI
│   ├── colab/workshop.ipynb           零安裝 Colab 版
│   ├── docs/labs/                     L1–L3 Lab 手冊
│   └── setup.sh                       環境預檢
├── infra/                             工作坊主辦端 vLLM 啟動（serve-gemma/qwen.sh）
└── docs/                              GitHub Pages landing page
```

## 相關 repo

- 原始應用：[UDICatNCHU/claude-mcp-project](https://github.com/UDICatNCHU/claude-mcp-project) — 興大 AI 學伴（Claude + MCP 的 web chat 介面，~239 個 MCP 工具）

## 其他 CLAUDE.md（本機同步維護參考）

公開讀者可忽略本節。若您是 NCHU 內部開發者，本 repo 通常與 `AiLearningMate/` 並列為 sibling 目錄，本機會有另外兩份 CLAUDE.md 各司其職：

| 路徑（從本 repo 看） | 焦點 |
|------|------|
| `../AiLearningMate/CLAUDE.md` | NCHU AI 學伴 monorepo 總覽（claude-mcp-project + library + mini-project + qwen-coding）|
| `../AiLearningMate/library/CLAUDE.md` | `library/` sub-project 專屬：Python / uv / FastMCP 環境與工具分類，獨立於本 workshop 維護 |

三份 CLAUDE.md 各自作為其所在目錄的 Claude Code context；不互相衝突，只是工作 scope 不同。本機工作時可三份並讀，**公開發佈只有本檔**。
