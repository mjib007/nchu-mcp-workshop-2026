# NCHU MCP Workshop 2026

三小時 MCP 入門工作坊教材，受眾為大專院校教師（非必要為資工背景）。

所有內容以 [NCHU AI 學伴](https://github.com/UDICatNCHU/claude-mcp-project) 作為實際案例。

## 課程結構（180 min = 3 小時）

| 段落 | 時間 | 主題 | 檔案 |
|------|------|------|------|
| 1 | 40 min | Why MCP | `01-why-mcp.pptx`（21 張）+ Why MCP 概念長片（2:35, Manim → YouTube） |
| 2 | 40 min | How MCP Works | `02-how-mcp-works.pptx`（24 張，附錄含 REST vs JSON-RPC）+ handshake 影片（2:14, YouTube）|
| — | 10 min | 休息 | |
| 3 | 35 min | Agentic Tool Loop | `03-agentic-tool-loop.pptx`（8 張，A2 cut）+ Agentic Loop 影片（1:07, YouTube） |
| 4 | 45 min | 動手做（mini-project 實作） | `04-hands-on-lab.pptx`（12 張）+ `04-hands-on-lab.md` + `mini-project/`（含 Colab）+ `infra/` |
| 5 | 10 min | 實務考量（收尾） | `05-practical-considerations.md` + `haiku-alignment-report.pptx` |

## Repo 結構

```
├── 01–03-*.pptx                       # 講課用投影片
├── 01-why-mcp-video.mp4               # Segment 1 概念長片（3 min, Manim）
├── 02-mcp-connection-video.mp4        # Segment 2 handshake 影片（2:17, Manim）
├── 04-hands-on-lab.md / .pptx         # 第四段動手做 landing page + 講師開場 15 張
├── 05-practical-considerations.md     # 第五段收尾（規模／品質／模型／成本）
├── mini-project/                      # 學員端 hands-on：Express + FastMCP + 極簡 UI
│   ├── backend-node/, mcp-server-py/, web/
│   ├── colab/workshop.ipynb           # 零安裝 Colab 版（雲端跑完整 3 層 + L1/L3）
│   ├── docs/labs/                     # L1–L3 實作手冊
│   ├── docs/benchmarks/               # 2026-04-24 Claude vs Gemma4 實驗記錄
│   ├── scripts/                       # Claude vs 本地模型 對比腳本
│   └── setup.sh                       # 環境預檢
├── infra/                             # 工作坊主辦端：vLLM 啟動腳本
└── tools/
    ├── lib_newstyle.py                # 共用設計系統（violet 色票、版面 primitives）
    ├── build-0X-slides.py             # 各段 .pptx 程式化產生（皆 import lib_newstyle）
    ├── build-haiku-slides.py          # haiku-alignment-report.pptx 產生
    ├── build-sonnet-slides.py         # sonnet-running-example.pptx 產生
    ├── extract-pptx-to-md.py          # 把 pptx 抽成 md，餵 TA agent（private repo）
    └── sync-to-drive.sh               # rclone 同步教材到 Google Drive（需先 rclone config）
```

> **課程 TA agent** 已獨立成 private repo `UDICatNCHU/nchu-mcp-ta-agent`（線上問答 bot，不公開）。本 repo 只含教材。

> **動畫展示**：早期版本以單檔 `*.html` 互動動畫呈現；目前改為 Manim 渲染的 `.mp4` 影片（更穩定、可重複播放、能直接上 YouTube）。HTML 動畫已全部移除。

## 可跑的 hands-on：`mini-project/`

學員在 Segment 4 跟著做的 demo：Express + Claude + FastMCP + 極簡 chat UI。4 支教學工具（hello / teachers / weather / library）+ 1 支 L3 練習 stub（arxiv）。`library` 即時查圖書館館藏（Ex Libris Primo，免 key），是「呼叫外部 API」的可用範例。

**最簡單：零安裝用 Colab**（課堂推薦）
[▶ Open in Colab](https://colab.research.google.com/github/UDICatNCHU/nchu-mcp-workshop-2026/blob/main/mini-project/colab/workshop.ipynb) — 瀏覽器裡一步步跑完整 3 層 + L1/L3，Mac/Windows 體驗一致。

**在自己電腦跑：**
```bash
cd mini-project
cp .env.example .env && vim .env       # 填 ANTHROPIC_API_KEY
./setup.sh                             # 5/5 ✅
cd backend-node && npm start           # → http://localhost:3000
```

詳見 [`mini-project/README.md`](mini-project/README.md)。

## 課程 TA agent（獨立 private repo）

工作坊現場讓學員直接問問題的線上 bot（「Segment 2 在講什麼？」「L1 Step 3 怎麼改 docstring？」）已搬到 private repo **`UDICatNCHU/nchu-mcp-ta-agent`**，架構刻意 mirror `mini-project/`。不公開，預計部署 Google Cloud Run。本教材 repo 不含其程式碼。

## 風格規範

- 配色：Violet primary `#7B5CF5` + Orange / Teal / Pink / Blue accents，搭配 pastel card 底色（`*_PASTEL`）；finale / transition 頁使用 Midnight `#0F1429`
- 字型：Arial Black（重粗體標題）／ Calibri（內文，附 italic muted 副標）／ Consolas（程式碼，柔化的 syntax highlighting）
- 設計系統集中於 `tools/lib_newstyle.py`（色票 + `metadata_bar` / `pastel_card` / `circle_number` / `code_block` / `callout_box` 等版面 primitives），各段 `tools/build-0X-slides.py` 共用
- 動畫展示以 Manim 渲染為 `.mp4`（取代早期的 `.html` 互動動畫，已全數移除）
- 第四、五段以 `.md` 產出；動手部分以可跑的 `mini-project/`（含 Colab 版）呈現

## 目前進度

- 第一段：`01-why-mcp.pptx`（21 張）+ Why MCP 概念長片（2:35 Manim → YouTube）
- 第二段：`02-how-mcp-works.pptx`（**24 張**，含附錄 REST vs JSON-RPC）+ handshake 影片（2:14 → YouTube）
- 第三段：`03-agentic-tool-loop.pptx`（8 張，A2 cut）+ Agentic Loop 影片（1:07 Manim → YouTube）
- 第四段（動手做）：`04-hands-on-lab.pptx`（**12 張**，code-truth 對齊 mini-project）+ `04-hands-on-lab.md` + 完整可跑 `mini-project/`（含 Colab 版 + 三關 Lab 手冊）
- 第五段（實務考量收尾）：`05-practical-considerations.md` 完成（四大支柱：規模／品質／模型／成本）
- **TA agent**：已獨立成 private repo `nchu-mcp-ta-agent`，待部署 Cloud Run
- `infra/`：Gemma 4 / Qwen 2.5-Coder vLLM 啟動腳本完成
