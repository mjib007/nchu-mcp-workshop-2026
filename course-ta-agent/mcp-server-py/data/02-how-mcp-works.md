# 02-how-mcp-works.pptx


## Slide 1

MCP 入門工作坊  ·  第二講
How MCP Works
把 LLM 接到真實工具的標準協定
范耀中  Yao-Chung Fan
國立中興大學  ·  AI 學伴系統實務案例
LLM 不執行任何東西
所有「執行」都發生在 harness 程式裡

---

## Slide 2

00   A G E N D A
本講四個段落 + 附錄
從 function calling 底層 → MCP 標準化 → 整體架構
①
Function Calling 怎麼運作
LLM 只吐字串
harness 才是執行者
②
從一個查詢開始
場景 → spawn → 兩階段握手
→ 工具呼叫
③
Tool 與 Client 機制
JSON Schema · description
注入 LLM 的 tools 參數
④
整體架構與附錄
四層分工 · 一句話總結
+ REST vs JSON-RPC
2 / 24

---

## Slide 3

01   F U N C T I O N   C A L L I N G
用一個具體例子搞懂
—— 從使用者輸入 一路追到 真正執行 的程式碼
使用者輸入
我家目錄底下有幾個 .py 檔？
LLM 從頭到尾只做一件事 —— 吐字串
▶  所有「真的執行」都發生在外面的程式 —— 我們叫它 harness
3 / 24

---

## Slide 4

01 · ①   F U N C T I O N   C A L L I N G   ·   S T A G E   1 + 2
Stage 1+2:開發者準備 schema,送出 API call
tools 只是個 Python dict —— 最終會被 SDK 序列化成 JSON
# 開發者寫的 Python
import anthropic
client = anthropic.Anthropic()
tools = [{
"name": "execute_bash",
"description": "Execute a bash command. Returns stdout.",
"input_schema": {
"type": "object",
"properties": {"command": {"type": "string"}},
"required": ["command"]
}
}]
response = client.messages.create(
model="claude-opus-4-7",
tools=tools,        ← 把工具 schema 一起送
messages=[{'role':'user',
'content':'我家目錄底下有幾個 .py 檔？'}]
)
關鍵觀察
tools 只是一個 dict。
它沒有任何「綁定的函式指標」。
模型看到什麼
「有一個叫 execute_bash 的東西,
描述是這樣,參數長這樣 …」
→ 跟讀到任何自然語言沒差別。
4 / 24

---

## Slide 5

01 · ②   F U N C T I O N   C A L L I N G   ·   S T A G E   3
Stage 3:LLM 回了一段 JSON
它就是吐了一段字串 —— 沒有「呼叫」任何東西
{
"id": "msg_abc123",
"stop_reason": "tool_use",       ← 旗號
"content": [
{ "type": "text",
"text": "讓我用 find 幫你數一下。" },
{ "type": "tool_use",
"id": "toolu_01XYZ",
"name": "execute_bash",
"input": {
"command": "find ~ -name '*.py' -type f | wc -l"
}
}
]
}
stop_reason
tool_use ←→ end_turn
前者:harness 接手執行。
後者:迴圈結束,印出。
command 這串字
是 LLM token-by-token 生出來的。
Constrained decoding 確保 JSON 一定合法。
LLM 從來沒有「呼叫」過任何工具 —— 它就是吐了一段 JSON 字串
5 / 24

---

## Slide 6

01 · ③   F U N C T I O N   C A L L I N G   ·   S T A G E   4
Stage 4:Harness 真的執行
subprocess.run() —— 字串穿越文字宇宙、進入真實電腦的那一刻
# Harness 拿到 LLM 的 tool_use 後
for block in response.content:
if block.type == "tool_use":
cmd = block.input["command"]
# ↓↓↓  這一行才是真的執行 ↓↓↓
result = subprocess.run(
cmd,
shell=True,
capture_output=True,
text=True,
timeout=30,
)
tool_output = result.stdout.strip()  # "42"
信任邊界
subprocess.run(cmd, shell=True)
把 LLM 的字串交給 OS shell。從這一刻起,跟你親手打 100% 一樣。
OS 在這一刻做的事
/bin/bash 解析字串
→ fork 出 find / wc processes
→ stdout 回傳 "42"
⚠   subprocess.run(LLM 輸出) 本質上就是 eval(LLM 輸出)
若 prompt injection 攻擊,LLM 會生出 rm -rf ~,harness 不長眼就會照跑。
6 / 24

---

## Slide 7

01 · ④   F U N C T I O N   C A L L I N G   ·   S T A G E   5 + 6
Stage 5+6:結果塞回,LLM 給最終答案
messages 陣列繼續滾動,直到 stop_reason: end_turn
[user]
"我家目錄底下有幾個 .py 檔？"
[assistant]
"讓我用 find 幫你數一下。"
+ tool_use { execute_bash, find ~ ... }
[user]   ← 注意:role 是 user
tool_result { content="42" }
[assistant]   stop_reason: end_turn
"你家目錄底下總共有 42 個 .py 檔。"
tool_result 用 user 送回
從 model 角度,它中斷自己問了外面世界一個問題,外面回了一句。現在輪它繼續講。
完整 loop
tool_use
→ run → tool_result
→ … → end_turn
可能跑很多輪 —— LLM 可以連續呼叫多個工具,直到它覺得夠了。
7 / 24

---

## Slide 8

01 · ⑤   F U N C T I O N   C A L L I N G   ·   T A K E A W A Y
LLM ↔ Harness 職責分工
MCP 在這個機制上加了什麼?把 harness ↔ tool 標準化、抽到獨立 process
LLM 做的事
✓  生成 tool_use JSON
✓  讀 tool schema,生 input JSON
✓  Constrained decoding 確保 JSON 合法
✗  不知道工具真正做什麼
✗  碰不到 OS、檔案、網路
Harness 做的事
✓  解析 tool_use,真的執行
✓  維護 messages 陣列
✓  Loop 直到 stop_reason: end_turn
✓  處理 timeout / 錯誤 / 結果格式
✓  加 sandbox / 安全防護
▶  MCP = 把 harness ↔ tool 的協定標準化,抽到獨立 process
8 / 24

---

## Slide 9

02   F R O M   A   U S E R   Q U E R Y
場景:使用者問了一個問題
LLM 判斷該呼叫哪個工具 —— 但它自己不會呼叫
使用者
幫我查最近圖書館有什麼新書
LLM (Sonnet) 內心戲
「嗯…需要查新書資料庫」
→  呼叫 search_new_books 工具
!  但 LLM 自己不會呼叫 —— 要靠 Parent 程序去跟 Child 程序講話
9 / 24

---

## Slide 10

02 · ①   F R O M   A   U S E R   Q U E R Y   ·   A C T   1
Act 1:Parent 開出 Child
spawn 子程序 + 兩條 stdio pipe = 雙向通訊管道
Parent Process
Node.js
LLM · Sonnet
Child Process
Python MCP Server
stdout
stdin
①  Parent (Node.js) 用 spawn() 開出 Child (Python) 子程序
②  LLM (Sonnet) 是 Parent 內的 client component —— 不會自己出去呼叫工具
③  兩條 stdio pipe → Parent ⇄ Child 可以雙向講話
10 / 24

---

## Slide 11

02 · ②   F R O M   A   U S E R   Q U E R Y   ·   A C T   2
Act 2:兩階段握手
互換能力 → 拿到工具清單,兩步都過才算真的連上
訊息往返
①   Parent  →  Child
「我來了」  +  「給我能力清單」
②   Child  →  Parent
「我能做什麼」  +  「8 個工具清單」
→  雙向 JSON-RPC 訊息往返
握手進度
✓
Step 1:打過招呼
✓
Step 2:拿到工具清單
兩個都打勾 才算真的連上
中間時刻 (Step 1 ✓ 但 Step 2 ✗) Parent 還不知道工具清單,送 tool call 也沒用。
11 / 24

---

## Slide 12

02 · ③   F R O M   A   U S E R   Q U E R Y   ·   A C T   3
Act 3:工具呼叫
LLM 決定 → token 飛去 Child → 結果飛回 → 找對應請求
①
LLM 決定
search_new_books("新書")
②
Parent 記下
等候第 4 個請求 · 30s 內
③
Child 執行
Python MCP Server 跑 search_new_books()
④
結果飛回
10 筆新書
⑤
Parent 回呼
找到對應請求 → 回給使用者
▶  「第 4 個請求」是 JSON-RPC 給每個 request 的編號,讓 response 對得回來
12 / 24

---

## Slide 13

▶  切換到影片
02-mcp-connection-video.mp4   ·   2 : 1 7
影片重點
1. 場景開場 — 使用者問「新書」 → LLM 判斷要呼叫工具
2. Act 1 — Parent / Child 的 spawn 與 pipe
3. Act 2 — 兩階段握手 checkbox 視覺
4. Act 3 — token 飛去、等候第 4 個請求、結果飛回
5. Frame closure — 「新書」一路回到使用者
13 / 24

---

## Slide 14

03   T O O L   ·   註 冊 與 描 述
tools/list:Server 回傳工具定義
Client 一啟動就 list,把每個工具的 schema 收進來
# Client → Server
{ "method": "tools/list", "id": 2 }
# Server → Client  (興大系統共 33 個)
{ "result": { "tools": [{
"name": "search_library_books",
"description": "搜尋中興大學圖書館的館藏書籍,
支援關鍵字查詢",
"inputSchema": {
"type": "object",
"properties": {
"keyword": {"type": "string"}
}, "required": ["keyword"]
}
}, { "name": "get_department_courses", ... },
…共 33 個
] }, "id": 2 }
14 / 24

---

## Slide 15

03 · ①   T O O L   ·   三 個 關 鍵 欄 位
每個 Tool 的三個關鍵欄位
LLM 看到的就只有這三個,所以 description 決定一切
name
工具的唯一識別名稱
"search_library_books"
LLM 在 tool_use 回傳時引用這個名稱
description
自然語言描述工具的用途
"搜尋中興大學圖書館的館藏書籍"
這是 LLM 判斷「要不要用」的最重要依據
inputSchema
JSON Schema 定義參數格式
{ "type": "object",
  "properties": {…} }
LLM 據此產生正確的 arguments
15 / 24

---

## Slide 16

03 · ②   T O O L   ·   D E S C R I P T I O N
description 寫得好不好,決定 LLM 選不選得對
LLM 從來不會直接接觸 MCP Server,只看 name + description + inputSchema
✗   模糊的 description
"搜尋課程"
問題:8 個課程相關工具
(關鍵字 / 系所 / 教師 / 類型…)
LLM 分不清楚要用哪一個。
✓   精確的 description
"依系所代碼查詢該系所的
所有課程,回傳課程名稱、
學分數、授課教師"
LLM 一看就知道:「電機系有哪些課」→ 用這個
關鍵洞察
description 的品質  =  工具被正確使用的機率
16 / 24

---

## Slide 17

04   C L I E N T   ·   整 合 機 制
工具清單 → LLM 的 tools 參數
Client 把所有 MCP Server 的工具收齊,轉成 LLM API 的 tools 欄位
33 個 MCP
Servers
→
Client 收集
→
轉換
→
LLM API
呼叫
// raw-mcp-client.js  —  注入工具到 Claude API
const response = await anthropic.messages.create({
model: "claude-sonnet-4-20250514",
messages: conversationHistory,
tools: allMcpTools.map(t => ({
name: t.name,             // 來自 MCP Server
description: t.description, // 來自 MCP Server
input_schema: t.inputSchema // 來自 MCP Server
}))
});
17 / 24

---

## Slide 18

04 · ①   C L I E N T   ·   L L M 眼中的世界
LLM 眼中的世界 —— 只看到工具描述
Server 怎麼跑、語言、資料庫,LLM 都看不到。它只有文字。
LLM 看到的
Available tools:
1.  search_library_books
搜尋圖書館館藏書籍
2.  get_department_courses
依系所代碼查詢課程
3.  search_teachers
搜尋教師資訊與研究
…共 33 個
LLM 看不到的
✗  Server 怎麼啟動的
✗  Server 用什麼語言
✗  資料庫連線方式
✗  網路拓撲
✗  認證機制
✗  JSON-RPC 細節
18 / 24

---

## Slide 19

04 · ②   M C P   ·   整 體 架 構
MCP 整體架構:四層分工
Host → Client → Server → Tool —— 每層只看下一層,LLM 只看文字
Host
應用程式 / 入口
興大 AI 學伴 web UI
Client
包含 LLM + MCP client
Node.js + Sonnet  (= 影片裡的 Parent)
Server
個別 MCP server 子程序
Python MCP Server  (= 影片裡的 Child)
Tool
個別工具函式
search_new_books / search_courses / …
19 / 24

---

## Slide 20

—  一  句  話  總  結  —
MCP 把 function calling 標準化
—— LLM ↔ Tool 中間多了一個獨立 process。
搭配教學影片:
「02-mcp-connection-video.mp4 — 2:17」
20 / 24

---

## Slide 21

附錄   A P P E N D I X   ·   R E S T   v s   J S O N - R P C
為什麼 MCP 選 JSON-RPC 不選 REST?
給技術 curious 老師 —— 不講也不影響理解 MCP 的核心
面向
REST
JSON-RPC
核心概念
資源(URL + HTTP 動詞)
動作(method 欄位)
端點
每個資源一個 URL
單一入口,靠 method 區分
傳輸層
綁定 HTTP
不綁定(stdio / HTTP / WS)
語意
CRUD 操作
呼叫函式
範例
GET /books?keyword=AI
{ method: "search_books" }
▶  MCP 選 JSON-RPC:傳輸層不綁 HTTP(可用 stdio),語意是「呼叫工具」而非「操作資源」
21 / 24

---

## Slide 22

附錄 · ①   J S O N - R P C   ·   三 種 訊 息 類 型
JSON-RPC 2.0 的三種訊息類型
Request / Response / Notification —— 用 id 欄位區分
Request
Client → Server
帶有 id 欄位 · 期待回應
{ method: "tools/call",
params: {...},
id: 1 }
Response
Server → Client
帶有相同 id · 回 result 或 error
{ result: {...},
id: 1 }
Notification
任一方向
沒有 id · 不期待回應
{ method:
"notifications/
initialized" }
22 / 24

---