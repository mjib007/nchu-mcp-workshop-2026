# 02-how-mcp-works.pptx


## Slide 1

How MCP Works
架構、協定與連線機制
MCP 入門工作坊  ｜  第二講（50 min）
國立中興大學  ·  AI 學伴系統實務案例

---

## Slide 2

本講大綱
01
從一個查詢開始
場景 → Parent 開出 Child → 兩階段握手 → 工具呼叫
02
Tool 註冊與描述
JSON Schema · description 如何影響 LLM 選擇
03
Client 整合機制
工具清單如何注入 LLM 的 system prompt
附錄
技術細節(時間夠就講,不夠就跳)
REST vs JSON-RPC · JSON-RPC 三種訊息類型

---

## Slide 3

01
從一個查詢開始
用 search_new_books 走一遍完整流程

---

## Slide 4

場景:使用者問了一個問題,LLM 決定要呼叫工具
使用者
幫我查最近圖書館有什麼新書
嗯…需要查新書資料庫
→ 呼叫 search_new_books 工具
LLM (Sonnet)
但 LLM 自己不會呼叫 — 要靠 Parent 去跟 Child 講話

---

## Slide 5

Act 1 — Parent 開出 Child
▶ 開出 Child
Parent Process
Node.js
LLM · Sonnet
Child Process
Python MCP Server
• Parent (Node.js) 用 spawn() 開出 Child (Python) 子程序
• LLM (Sonnet) 是 Parent 裡的一個 client component — 它住在 Parent 內,不會自己出去呼叫工具
• 兩條 stdio pipe 串通 → Parent ⇄ Child 可以雙向講話

---

## Slide 6

Act 2 — 兩階段握手
Parent
Node.js
Child
Python
→ 我來了 / 給我工具清單
← 我能做什麼 / 8 個工具
握手進度
✓
Step 1:打過招呼
✓
Step 2:拿到工具清單
兩個都打勾 才算真的連上
重點:中間時刻(Step 1 ✓ 但 Step 2 ✗)Parent 還不知道工具清單,送 tool call 也沒用

---

## Slide 7

Act 3 — 工具呼叫
Parent
Node.js
LLM · Sonnet
Child
Python
search_new_books("新書")
等候第 4 個請求 · 30s 內
結果 · 10 筆新書
第 4 個請求 ✓ 完成
完整流程:LLM 決定 → token 飛去 Child → Child 執行 → 結果飛回 → Parent 找到對應請求 → 回給使用者
「第 4 個請求」是 JSON-RPC 給每個 request 的編號,讓 response 能對得回來

---

## Slide 8

→  切換到影片
02-mcp-connection-video.mp4   ·   2:17
影片重點:
1. 場景開場 — 使用者問「新書」 → LLM 判斷要呼叫工具
2. Act 1 — Parent / Child 的 spawn 與 pipe;LLM (Sonnet) 住在 Parent 內
3. Act 2 — 兩階段握手:checkbox ☐打過招呼 → ✓打過招呼 → ☐拿工具 → ✓拿工具
4. Act 3 — 工具呼叫:token 飛去、等候第 4 個請求、結果飛回
5. Frame closure — 「查新書」→ Child 執行 → 10 筆新書 → 使用者

---

## Slide 9

03
Tool 註冊與描述
JSON Schema  ·  description  ·  LLM 的唯一線索

---

## Slide 10

tools/list — Server 回傳工具定義
// Client 發送 tools/list request
{ "method": "tools/list", "id": 2 }
// Server 回傳所有可用工具（興大系統共 33 個）
{ "result": { "tools": [{
"name": "search_library_books",
"description": "搜尋中興大學圖書館的館藏書籍，支援關鍵字查詢",
"inputSchema": {
"type": "object",
"properties": {
"keyword": { "type": "string", "description": "搜尋關鍵字" }
}, "required": ["keyword"]
}
}, { "name": "get_department_courses", ... }, // ...共 33 個
] }, "id": 2 }

---

## Slide 11

每個 Tool 的三個關鍵欄位
name
工具的唯一識別名稱
LLM 在 tool_use 回傳時引用這個名稱
"search_library_books"
description
自然語言描述工具的用途
這是 LLM 判斷「要不要用」的最重要依據
"搜尋中興大學圖書館的館藏書籍"
inputSchema
JSON Schema 定義參數格式
LLM 據此產生正確的 arguments
{ type: "object", properties: {...} }

---

## Slide 12

description 寫得好不好，決定 LLM 選不選得對
✕  模糊的 description
"搜尋課程"
問題：有 8 個課程相關工具
（關鍵字 / 系所 / 教師 / 類型…）
LLM 分不清楚要用哪一個
✓  精確的 description
"依系所代碼查詢該系所的
 所有課程，回傳課程名稱、
 學分數、授課教師"
LLM 一看就知道：
「電機系有哪些課」→ 用這個
關鍵洞察
LLM 從來不會直接接觸 MCP Server。
它看到的就只有 name + description + inputSchema 這三個欄位的文字。
→ description 的品質 = 工具被正確使用的機率

---

## Slide 13

04
Client 整合機制
工具清單如何餵給 LLM

---

## Slide 14

工具清單 → LLM 的 tools 參數
33 個
MCP Servers
→
Client
收集工具清單
→
轉換 →
LLM API 呼叫
// raw-mcp-client.js — 呼叫 Claude API 時注入工具
const response = await anthropic.messages.create({
model: "claude-sonnet-4-20250514",
messages: conversationHistory,
tools: allMcpTools.map(t => ({
name: t.name,              // 來自 MCP Server
description: t.description, // 來自 MCP Server
input_schema: t.inputSchema // 來自 MCP Server
}))
});

---

## Slide 15

LLM 眼中的世界 — 只看到工具描述
LLM 看到的
Available tools:

1. search_library_books
   搜尋圖書館館藏書籍

2. get_department_courses
   依系所代碼查詢課程

3. search_teachers
   搜尋教師資訊與研究

... 共 33 個
LLM 看不到的
✕ Server 怎麼啟動的

✕ Server 用什麼語言

✕ 資料庫連線方式

✕ 網路拓撲

✕ 認證機制

✕ JSON-RPC 細節

---

## Slide 16

→  切換到互動動畫 Demo
mcp-architecture-animation.html
展示重點：
1. Host → Client → Server → Tool 四層架構的完整互動
2. 使用者提問後，LLM 如何透過 Client 呼叫 Server 的工具
3. 工具執行結果如何回傳給 LLM 整合成最終回覆
4. 對照剛剛學到的 JSON-RPC 格式，看實際訊息往返

---

## Slide 17

本講重點回顧
1
MCP 把 LLM ⇄ 工具的通訊抽出來,變成 Parent / Child 兩個 process 之間的雙向管道
2
兩階段握手:① 互換能力 → ② 拿到工具清單;兩步都過才算真的連上
3
工具呼叫:LLM 決定 → token 飛去 Child → Child 執行 → 結果飛回 → 找到對應請求回給使用者
4
每個工具由 name / description / inputSchema 三個欄位定義;description 的品質直接決定 LLM 選不選得對
5
Client 把所有工具定義轉換後,注入 LLM API 的 tools 參數 — LLM 只看得到 name + description + inputSchema
下一講預告:Agentic Tool Loop — LLM 怎麼自主決定該呼叫哪個工具

---

## Slide 18

附錄
Appendix
給技術 curious 老師的細節
• REST vs JSON-RPC 比較
• JSON-RPC 三種訊息類型(Request / Response / Notification)

---

## Slide 19

01
通訊協定
REST  vs  JSON-RPC

---

## Slide 20

REST vs JSON-RPC — 一張表看懂差異
面向 | REST | JSON-RPC
核心概念 | 資源（URL + HTTP 動詞） | 動作（method 欄位）
端點 | 每個資源一個 URL | 單一入口，靠 method 區分
傳輸層 | 綁定 HTTP | 不綁定（stdio / HTTP / WS）
語意 | CRUD 操作 | 呼叫函式
範例 | GET /books?keyword=AI | { method: "search_books" }
MCP 選 JSON-RPC 的原因：  傳輸層不綁 HTTP（可用 stdio），語意是「呼叫工具」而非「操作資源」

---

## Slide 21

REST — 每個資源有自己的路徑
// 搜尋書籍
GET /api/books?keyword=AI
Host: library.nchu.edu.tw
// 新增一本書
POST /api/books
Content-Type: application/json
{ "title": "深度學習入門", "author": "..." }
// 刪除
DELETE /api/books/123
// → 三個不同的 URL path + 三個不同的 HTTP method，必須透過 HTTP

---

## Slide 22

JSON-RPC — 單一入口，靠 method 區分
// 搜尋書籍
{ "jsonrpc": "2.0",
"method": "search_books",
"params": { "keyword": "AI" },
"id": 1 }
// 新增一本書 — 同一個入口，換 method 就好
{ "jsonrpc": "2.0",
"method": "create_book",
"params": { "title": "深度學習入門" },
"id": 2 }
// → 不需要 HTTP、不需要 URL — 可以透過 stdio 傳送！

---

## Slide 23

JSON-RPC 2.0 的三種訊息類型
Request
Client → Server
帶有 id 欄位
期待回應
{ method: "tools/call",
params: {...},
id: 1 }
Response
Server → Client
帶有相同 id
回傳 result 或 error
{ result: {
content: [...]
},
id: 1 }
Notification
任一方向
沒有 id 欄位
不期待回應（fire & forget）
{ method:
"notifications/
initialized" }

---