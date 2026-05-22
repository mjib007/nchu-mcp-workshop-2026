# YouTube 發佈素材 — 01-why-mcp-video

影片：`01-why-mcp-video-preview.mp4`（172.6 秒，1920×1080）
用途：MCP 工作坊第一講「Why MCP」課前預習版

---

## 1. 標題（5 個版本，依頻道調性挑）

| # | 標題 | 字數 | 風格 | 適用情境 |
|---|------|------|------|---------|
| **1** | **三分鐘看懂 Why MCP：從 LLM 局限到統一協定** | 22 | 直白教學風 + 長度承諾 | **推薦單發**（清楚說出主題與長度）|
| 2 | LLM 為什麼需要 MCP？三分鐘從 RAG/Tool Use 講起 | 24 | 直白 + 比較式 | 主打「我想了解三選一」的觀眾 |
| 3 | MCP 入門 #1｜為何 LLM 需要一個統一協定（3 min） | 25 | 課程系列風 | 適合做工作坊系列影片 |
| 4 | RAG、Tool Use、MCP 差在哪？三分鐘搞懂 | 20 | 比較式 | 對搜尋「RAG vs MCP」的觀眾有效 |
| 5 | N×M 還是 N+M？三分鐘看懂 MCP 解耦 LLM 整合的痛 | 25 | 痛點式（適合 LinkedIn 推廣）| 已知聽眾有 Tool Use 經驗者 |

**推薦選 #1 單發**；若會出第二、第三講，改用 #3 建立系列識別。

---

## 2. 描述（複製貼上）

```
LLM 很強，但有些事它做不到。MCP（Model Context Protocol）就是為了補上這塊空白而生。
這支影片三分鐘帶你看完 LLM 的三道牆、RAG 與 Tool Use 的解法與痛點，最後到 MCP 統一協定如何把 N×M 解耦成 N+M。

▌ LLM 的三道牆 — 知識截止、沒有私有資料、不能執行動作
▌ RAG 解知識問題，Tool Use 解動作問題，但每個 App × 每個資料源都要重寫整合
▌ MCP = LLM 世界的 USB-C：一個協定，接所有 App 與所有資料源

實際案例：中興大學「AI 學伴」基於 MCP 串接 33 個工具、9 大分類，1 套統一協定撐起整套系統。

—

▌ 適合對象
・大專院校教師：想知道學校系統能怎麼接上 LLM
・研究者／碩博生：在評估自己的研究流程要走 RAG、Tool Use、還是 MCP
・對 ChatGPT/Claude 已熟悉、想了解「應用怎麼接資料源」的人

▌ 你會學到
・LLM 三種延伸策略（RAG / Tool Use / MCP）的本質差異
・為什麼 Tool Use 在多應用場景下會撞 N×M 牆
・MCP 的四個角色：Host / Client / Server / Tool

▌ 延伸閱讀
・MCP 官方規格：https://modelcontextprotocol.io
・興大 AI 學伴（線上版）：https://eduxplore.nlpnchu.org
・後續工作坊段落會帶你動手做一個 MCP server

—

#MCP #LLM #人工智慧 #ModelContextProtocol #Claude #AI教學 #大學課程 #工作坊
```

---

## 3. Hashtags

**前 3 個（顯示在標題上方，影響曝光最大）**：

```
#MCP #LLM #人工智慧
```

**完整清單（複製到描述末尾）**：

```
#MCP #LLM #人工智慧 #ModelContextProtocol #Claude #AI教學 #大學課程 #工作坊 #RAG #ToolUse
```

> **絕對不加 `#Shorts`** — 這支是長片，加了會被 YouTube 誤判為短片、影響搜尋排序。

---

## 4. 影片章節時間軸（複製到描述）

```
0:00  片頭：Why MCP
0:04  ACT 1｜LLM 的三道牆
0:36  ACT 2｜策略 A：RAG 把私有文件塞進 prompt
1:00  策略 B：Tool Use 給 LLM 工具呼叫
1:25  痛點：N × M 整合爆炸
1:51  ACT 3｜MCP 解耦：N×M → N+M
2:08  MCP 的四個角色
2:23  譬喻：MCP = LLM 世界的 USB-C
2:32  實際案例：興大 AI 學伴 33 工具
2:42  片尾：今天我們看到三件事
```

YouTube 看到這個格式會自動把章節點顯示在進度條上，學生可以跳段複習。

---

## 5. 置頂留言（3 版本選一）

**版本 A — 提問型（互動率最高）**：
> 你在用 ChatGPT / Claude 時，最希望它能接上哪個系統？
>
> （我們在中興大學試的是「AI 學伴」串了選課、圖書館、教師資料 — 但每間學校的需求都不一樣，歡迎留言聊聊）

**版本 B — 系列預告型**：
> 這是「三小時 MCP 工作坊」系列的第一講。下一講會深入 JSON-RPC 通訊協定（How MCP Works），訂閱看續集。
>
> 完整課程資料：https://github.com/...

**版本 C — 教學補充型**：
> 影片裡的「33 工具」案例是中興大學 AI 學伴系統（線上版：https://eduxplore.nlpnchu.org）。
>
> 如果你也想做一個自己學校 / 領域的 MCP 助理，可以從本工作坊的 mini-project 開始改：
> https://github.com/UDICatNCHU/nchu-mcp-workshop-2026

**推薦版本 A** — 互動率最高，能帶起留言區討論。

---

## 6. 縮圖建議

**主視覺**（建議在 Canva / Figma 做）：
- **背景**：Ocean Gradient（Navy `#1E2761` → Deep Blue `#065A82`）漸層
- **左半邊**（畫面 60%）：超大字「Why MCP」（白色 Serif Bold，~180pt）+ 副標小字「LLM × 統一協定」（橘 `#E8793A`，48pt）
- **右半邊**（畫面 40%）：N×M 蜘蛛網 → N+M 整齊圖（紅 → 綠 對比）
- **左上角**：小標籤「3 分鐘」（橘底白字圓角矩形）

**字級規則**：手機縮圖只有 ~200px 寬，主標題必須**手機上能看清** — 「Why MCP」要佔縮圖至少 1/3 高度。

**避免**：
- 不要把講師頭像放上去（這支是概念講解、不是 talking head）
- 不要塞超過 6 個字的中文 — 縮圖看不清
- 不要用截圖當縮圖 — 太雜

---

## 7. 發佈時機建議

**對齊課程節奏，不是流量熱門時段**：

| 情境 | 建議發佈時間 |
|------|------------|
| 工作坊**前一天晚上**（21:00–22:00）| **推薦** — 學員回家路上 / 睡前剛好看完 |
| 工作坊**當天早上**（8:00–9:00）| 次推薦 — 進教室前 catch up |
| 工作坊結束後當天（複習版）| 對沒到場的人 / 課堂太快沒消化的人 |

**避開**：
- 週末早晨（教師多半在備課，不會看 YouTube）
- 學期初開學週（資訊太多會被淹沒）

---

## 8. 發佈前 checklist

- [ ] 標題從 5 版中選定（推薦 #1）
- [ ] 描述完整貼上（含章節時間軸、適合對象、你會學到、延伸閱讀）
- [ ] Hashtags 前 3 個放描述首行
- [ ] 縮圖製作完成（Ocean Gradient + 「Why MCP」+ N×M→N+M 對比）
- [ ] 章節時間軸格式正確（YouTube 自動偵測）
- [ ] 確認**沒加 `#Shorts`**
- [ ] 置頂留言準備好（版本 A）
- [ ] 影片渲染為 1080p60（本機跑 `manim -qh videos/01-why-mcp-video.py WhyMCP`）
- [ ] 上字幕檔（中文 SRT — 從腳本內 `show_subtitle` 抽出來）
- [ ] 設定播放清單（若做系列）

---

## 本機 render 1080p60 指令

當前交付的是 1080p15 預覽（5.4 MB）。**正式發佈前**請本機 render 1080p60：

```bash
# 在 repo root 執行（cd 到你 clone 下來的位置）
uv run --with manim manim -qh videos/01-why-mcp-video.py WhyMCP
# 輸出在 media/videos/01-why-mcp-video/1080p60/WhyMCP.mp4
```

`-qh` = 1080p60，比 `-ql` 慢 5–10×，但畫面品質提升明顯（特別是文字邊緣與動畫流暢度）。
