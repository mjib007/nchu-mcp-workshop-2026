# YouTube 發佈素材 — 02-mcp-connection-video

影片：`02-mcp-connection-video-preview.mp4`（157.5 秒 ≈ 2:37，1920×1080）
用途：MCP 工作坊第二講「How MCP Works」課前預習版 — 父子程序握手流程

---

## 1. 標題（5 個版本）

| # | 標題 | 字數 | 風格 | 適用情境 |
|---|------|------|------|---------|
| **1** | **MCP 握手在做什麼？2 分半看懂父子程序對話** | 23 | 直白教學風 + 長度承諾 | **推薦單發** |
| 2 | spawn → initialize → tools/list → tools/call：MCP 完整握手流程 | 30 | 流程列舉式（搜尋友善）| 工程觀眾、技術 SEO |
| 3 | MCP 入門 #2｜父子程序怎麼開始講話（stdio + JSON-RPC）| 27 | 課程系列風 | 接 #01 Why MCP 系列 |
| 4 | ready ≠ isConnected：MCP 握手的微妙之處 | 22 | 痛點/反直覺式 | 已經懂 MCP 表面、想深入的觀眾 |
| 5 | 2 分半搞懂 MCP 連線：spawn 開子程序到 tool call | 25 | 直白 + 流程承諾 | 平衡型，社群分享適用 |

**推薦選 #1** 單發；若做系列改 #3。

---

## 2. 描述（複製貼上）

```
MCP Client 怎麼跟 MCP Server 講話？這支影片 2 分半帶你看完完整握手流程，從 spawn 開子程序、initialize 交換 capabilities、tools/list 取得工具清單，到實際 tools/call 執行工具。

▌ spawn 開子程序：stdio pipe 雙向 JSON-RPC，父寫 stdin、子回 stdout
▌ Handshake 兩階段：initialize 讓 ready=true，但要等 tools/list 才 isConnected=true
▌ Tool Call 機制：pendingRequests Map + 30 秒 timeout，resolve callback 收回結果

整支影片以中興大學 AI 學伴的 raw-mcp-client 程式碼為例，逐步示範 JSON-RPC 2.0 訊息的來回。

—

▌ 適合對象
・想自己實作 MCP Client 的工程師
・在 debug MCP 連線問題、看到 ready / isConnected 兩個 flag 搞不清楚的人
・教 MCP 工作坊、需要清楚架構圖的講師

▌ 你會學到
・child_process.spawn() 怎麼跟 Python MCP Server 用 stdio 串通
・JSON-RPC 2.0 的 request / response / notification 三種訊息差異
・pendingRequests Map + timeout + resolve 的 callback 機制

▌ 延伸閱讀
・MCP 官方規格：https://modelcontextprotocol.io
・興大 AI 學伴原始碼：https://github.com/UDICatNCHU/claude-mcp-project
・前一集 — Why MCP：（補上連結）

—

#MCP #ModelContextProtocol #JSONRPC #LLM #人工智慧 #Claude #AI教學 #大學課程 #工作坊 #SystemDesign
```

---

## 3. Hashtags

**前 3 個（影響曝光最大）**：

```
#MCP #ModelContextProtocol #JSONRPC
```

**完整清單**：

```
#MCP #ModelContextProtocol #JSONRPC #LLM #人工智慧 #Claude #AI教學 #大學課程 #工作坊 #SystemDesign
```

> 絕對不加 `#Shorts`。

---

## 4. 影片章節時間軸

```
0:00  片頭：MCP 握手
0:04  ACT 1｜spawn 父子程序建立
0:14  spawn() 開子程序 + stdio pipe
0:28  env ${VAR} 自動替換
0:36  ACT 2｜Handshake 三回合
0:39  送 initialize (id:1)
0:55  子程序回 capabilities → ready=true（但 isConnected 還是 false）
1:18  notifications/initialized + tools/list (id:3)
1:34  收到 8 個工具 → isConnected=true ✓
1:54  ACT 3｜Tool Call 真正動工
1:57  executeToolCall + pendingRequests Map + 30s timeout
2:14  子程序回 result → clearTimeout → resolve(content)
2:28  整個流程回顧：spawn → initialize → tools/list → tools/call
2:37  片尾：MCP 握手三件事
```

---

## 5. 置頂留言（3 版本）

**版本 A — 提問型**：
> 你在實作 MCP Client 時，遇過 ready 跟 isConnected 兩個 flag 分不清的問題嗎？
>
> 這個雙階段設計其實是為了確保「工具清單真的拿到了」才算連上 — 留言聊聊你自己的處理方式

**版本 B — 系列預告型**：
> 「三小時 MCP 工作坊」系列第 2 集。下一集會講 Agentic Tool Loop（LLM 怎麼自主選工具、串多輪迭代），訂閱看續集。

**版本 C — 教學補充型**：
> 影片裡所有 JSON-RPC 訊息範例都來自中興大學 AI 學伴的 raw-mcp-client，原始碼公開在：
> https://github.com/UDICatNCHU/claude-mcp-project
>
> 看 `MCPServerConnection.js` 對照影片流程，30 分鐘可以實作出自己的 MCP Client。

**推薦版本 A** — 互動率最高。

---

## 6. 縮圖建議

**主視覺**：
- **背景**：Ocean Gradient（Navy → Deep Blue）
- **左側**（畫面 40%）：超大字「MCP 握手」（白色 Serif Bold，~180pt）+ 副標小字「父子程序對話」（橘 `#E8793A`，48pt）
- **右側**（畫面 60%）：兩個盒（父 / 子）+ 中間水平箭頭 + JSON snippet `{"method":"initialize"}` 浮在上方
- **左上角**：標籤「2:37」（橘底白字）
- **右上角**：標籤「JSON-RPC 2.0」（小字白色）

**字級規則**：「MCP 握手」要佔縮圖 1/4 高度（手機看得清）。

**避免**：
- 不要塞太多技術名詞 — 縮圖 1 秒判斷
- 不要把整個 JSON 截圖貼上 — 看不清

---

## 7. 發佈時機建議

| 情境 | 建議發佈 |
|------|---------|
| 工作坊**前一天晚上** | **推薦**（21:00–22:00）|
| 配合 #01 Why MCP 發佈 | 前一集發佈後 2-3 天，建立系列節奏 |
| 系列連續發佈 | 每 3-5 天一集 |

---

## 8. 發佈前 checklist

- [ ] 標題從 5 版選定（推薦 #1 或 #3）
- [ ] 描述完整貼上（含章節時間軸）
- [ ] Hashtags 前 3 個置頂
- [ ] 縮圖製作（Ocean Gradient + 「MCP 握手」+ 父子盒 + JSON）
- [ ] 確認**沒加** `#Shorts`
- [ ] 置頂留言準備好（版本 A）
- [ ] **影片渲染為 1080p60**：`uv run --with manim manim -qh videos/02-mcp-connection-video.py MCPConnection`
- [ ] 字幕檔（中文 SRT — 從腳本 `show_subtitle` 抽出來）
- [ ] 加入「MCP 工作坊」播放清單（接 #01 Why MCP）

---

## 本機 render 1080p60 指令

```bash
# 在 repo root 執行（cd 到你 clone 下來的位置）
uv run --with manim manim -qh videos/02-mcp-connection-video.py MCPConnection
# 輸出在 media/videos/02-mcp-connection-video/1080p60/MCPConnection.mp4
```

當前交付是 1080p15 預覽（4.1 MB），正式發佈前請本機 render 1080p60。
