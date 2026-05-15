# 01-why-mcp.pptx


## Slide 1

MCP 入門工作坊  ·  第一講
Why MCP
從 LLM 的局限 到 Model Context Protocol
范耀中  Yao-Chung Fan
國立中興大學  ·  AI 學伴系統實務案例
為什麼需要 MCP?
LLM 摸不到外部世界 — MCP 是橋

---

## Slide 2

00   A G E N D A
本講四個段落
從 LLM 的局限 → 三種延伸策略 → MCP → 興大案例
①
LLM 能 / 不能做什麼
理解大型語言模型的能力邊界
②
三種延伸策略
RAG / Tool Use / MCP 深入比較
③
MCP 核心概念
Host / Client / Server / Tool
④
實際案例
興大 AI 學伴 33 個 MCP 工具
2 / 20

---

## Slide 3

01 · ①   L L M   能 做 什 麼
LLM 擅長什麼?
—— 訓練階段學到的「靜態知識」
語言理解與生成
翻譯、摘要、改寫、多語言對話
推理與分析
邏輯推導、比較分析、結構化輸出
程式碼生成
撰寫、除錯、解釋多種程式語言
知識回答
基於訓練資料的常識與專業知識
▶  這些能力來自訓練階段學到的靜態知識 —— 用一次,模型不會更新
3 / 20

---

## Slide 4

01 · ②   L L M   不 能 做 什 麼
LLM 的天花板
—— 訓練階段沒看過的、無法執行的事情
✗  知識截止日
訓練資料有日期上限
無法回答「今天」的事
✗  沒有私有資料
不知道你的課表、
圖書館藏書、校內公告
✗  無法執行動作
不能幫你查詢系統、
預約空間、操作 API
✗  會幻覺
不確定時仍自信回答
編造看起來合理的資訊
?  核心問題:如何讓 LLM 存取「外部世界」的資訊與功能?
4 / 20

---

## Slide 5

02 · A   S T R A T E G Y   ·   R A G
策略 A:RAG (Retrieval-Augmented Generation)
把外部文件「檢索 + 注入 prompt」交給 LLM
使用者提問
→
Embedding
向量化
→
向量資料庫
相似度搜尋
→
取回相關
文件片段
→
注入 Prompt
+ LLM 回答
優點
✓  降低幻覺 — 有引用來源
✓  存取私有資料(文件、知識庫)
✓  不需重新訓練模型
局限
✗  只能「讀」 — 無法執行動作
✗  檢索品質依賴 embedding 與切塊
✗  結構化查詢(如 SQL)支援差
5 / 20

---

## Slide 6

02 · A   R A G   ·   C O D E
RAG 概念程式碼
三步驟:embed query → 向量檢索 → 拼到 prompt
# 1. 使用者提問
query = "中興大學圖書館有什麼 AI 相關的書？"
# 2. 轉成向量,在資料庫中搜尋最相似的文件片段
embedding = embed_model.encode(query)
relevant_docs = vector_db.search(embedding, top_k=5)
# 3. 把搜尋結果塞進 prompt,交給 LLM
prompt = f"根據以下資料回答問題:\n{relevant_docs}\n\n問題：{query}"
response = llm.generate(prompt)
6 / 20

---

## Slide 7

02 · B   S T R A T E G Y   ·   T O O L   U S E
策略 B:Tool Use (Function Calling)
LLM 自己決定要不要呼叫工具、呼叫哪一個
使用者
提問
→
LLM 分析
選擇工具
→
呼叫外部
API / 函式
→
取得執行
結果
→
LLM 整合
回覆
優點
✓  能「做事」 — 查詢、計算、操作
✓  結構化輸入輸出(JSON Schema)
局限
✗  每家 API 格式不同(vendor lock-in)
✗  工具要寫死在應用程式裡
7 / 20

---

## Slide 8

02 · B   T O O L   U S E   ·   C L A U D E   v s   C H A T G P T
同一支工具,兩家 API 寫法不同
—— 這就是「vendor lock-in」的具體例子
Claude API
tools: [{
name: "search_books",
description: "搜尋館藏",
input_schema: {
type: "object",
properties: {
keyword:
{ type: "string" }
}
}
}]
ChatGPT API
tools: [{
type: "function",   ← 多包一層
function: {
name: "search_books",
description: "搜尋館藏",
parameters: {  ← 名稱不同
type: "object",
properties: { ... }
}
}
}]
8 / 20

---

## Slide 9

02 · B   T O O L   U S E   ·   T H E   N × M   P A I N
Tool Use 的痛點:每個應用都要重做
4 個 AI 應用 × 4 個資料源 = 16 個 connector,而且格式各不相同
ChatGPT App
Claude App
Gemini App
自建 Agent
N × M
個別整合
✕  ✕  ✕  ✕
✕  ✕  ✕  ✕
✕  ✕  ✕  ✕
✕  ✕  ✕  ✕
圖書館 DB
課程系統
教師資料
校內公告
!  每加一個 AI 應用或一個資料源,connector 數量爆炸成長
9 / 20

---

## Slide 10

02 · C   S T R A T E G Y   ·   M C P
策略 C:MCP — 統一協定解耦
寫一次 MCP Server,所有 AI 應用都能用 — 像 USB-C 一樣的標準介面
ChatGPT App
Claude App
Gemini App
自建 Agent
MCP
統一協定
JSON-RPC 2.0
N + M
(而非 N × M)
圖書館 DB
課程系統
教師資料
校內公告
10 / 20

---

## Slide 11

02 · ★   C O M P A R E   ·   R A G   v s   T O O L   v s   M C P
三者比較總覽
從核心能力到維護成本,看哪個適合你的情境
面向
RAG
Tool Use
MCP
核心能力
檢索文件
執行功能
檢索 + 執行 + 標準化
LLM 角色
讀 prompt 資訊
決定呼叫哪個函式
透過 Client 調度 Server
整合方式
Embedding + 向量
各家 API 各寫
統一 JSON-RPC 協定
可重用性
綁定單一應用
綁定單一應用
Server 跨應用共用
執行動作
✗
✓
✓
維護成本
中
高(N×M)
低(N+M)
▶  MCP 不是「取代」前兩者 —— MCP Server 內部可以同時放 RAG 檢索 + Tool Use 函式
11 / 20

---

## Slide 12

02 · ★   W H E N   T O   U S E   W H I C H
什麼時候用哪一種?
適用場景判斷指南
RAG
適用場景:
• 內部知識庫問答
• 文件搜尋與摘要
• 客服 FAQ 系統
★  最適合大量非結構化文本
Tool Use
適用場景:
• 呼叫特定 API
• 資料庫查詢
• 計算或產生圖表
★  最適合少量、固定的工具
MCP
適用場景:
• 多系統整合平台
• 校園/企業助手
• 跨應用共享工具
★  工具多、需跨應用重用
12 / 20

---

## Slide 13

03   M C P   ·   核 心 概 念
MCP 架構四大角色
Host → Client → Server → Tool —— 每層只看下一層
Host
使用者介面
Claude Desktop / 自建 Web App
Client
MCP 協定客戶端
負責與 Server 建立連線、傳遞訊息
Server
MCP 服務端
包裝外部資源為標準化工具
Tool
具體功能定義
search_books / get_courses
13 / 20

---

## Slide 14

03 · ①   M C P   ·   J S O N - R P C   2 . 0
MCP 如何溝通?— JSON-RPC 2.0
Client / Server 雙向訊息,所有 MCP 通訊用同一格式
Client → Server (Request)
{
"jsonrpc": "2.0",
"method": "tools/call",
"params": {
"name": "search_books",
"arguments": {
"keyword": "AI"
}
},
"id": 1
}
Server → Client (Response)
{
"jsonrpc": "2.0",
"result": {
"content": [{
"type": "text",
"text": "找到 3 本..."
}]
},
"id": 1
}
▶  標準化 · 雙向 · 傳輸無關(支援 stdio、HTTP+SSE、WebSocket)
14 / 20

---

## Slide 15

04   C A S E   S T U D Y   ·   N C H U   A I   學 伴
33 個 MCP 工具,九大分類
—— 用 Python 寫,透過 stdio 與 Node.js Client 通訊
課程查詢
8
search_courses
get_department_courses
圖書資源
5
search_library_books
get_loan_history
教師研究
7
search_teachers
get_research_projects
學術規劃
5
get_cross_program_courses
get_dual_degrees
校園資源
5
get_activities
book_space
行政法規
3
search_regulations
get_faqs
15 / 20

---

## Slide 16

—  一  句  話  總  結  —
MCP 把 N×M 變成 N+M
—— 寫一次 Server,所有 AI 應用都能用。
搭配教學影片:
「01-why-mcp-video.mp4 —— ~3 min」
16 / 20

---

## Slide 17

★   R E C A P
本講重點回顧
下一講預告:How MCP Works —— 架構與連線機制實作
1
LLM 有知識截止、無法存取外部系統的先天限制
2
RAG 解決「讀」的問題,Tool Use 解決「做」的問題
3
但 Tool Use 有 N×M 整合爆炸的痛點
4
MCP 用統一協定解耦 AI 應用與資料源,實現 N+M 整合
5
興大 AI 學伴用 33 個 MCP 工具服務真實校園需求
17 / 20

---