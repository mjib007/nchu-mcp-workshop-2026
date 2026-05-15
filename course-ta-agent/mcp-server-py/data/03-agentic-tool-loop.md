# 03-agentic-tool-loop.pptx


## Slide 1

MCP 入門工作坊  ·  第三講
Agentic Tool Loop
LLM 如何自主決策、呼叫工具、迭代推理
范耀中  Yao-Chung Fan
國立中興大學  ·  AI 學伴系統實務案例
從一次回答 → 多輪迭代
LLM 不只回答,還會自己選工具

---

## Slide 2

00   A G E N D A
本講四個段落
Agentic 觀念 → 訊息機制 → 控制迴圈 → Live Demo
①
什麼是 Agentic Loop
傳統 LLM vs 自主代理
②
tool_use / result
Claude API 訊息格式
③
迭代控制機制
maxIterations · 強制回覆
· Metadata 追蹤
④
Live Demo
Running Example 逐步解說
2 / 16

---

## Slide 3

01   A G E N T I C   L O O P   ·   觀 念
傳統 LLM vs Agentic LLM
從「單輪問答」到「多輪迭代」
傳統 LLM — 單輪問答
使用者  →  提問
LLM     →  回答(僅根據訓練資料)
結束
✗  無法存取外部資料
✗  無法執行動作
✗  一次互動就結束
Agentic LLM — 多輪迭代
使用者  →  提問
LLM     →  分析 → 選工具 → 呼叫
工具    →  回傳結果
LLM     →  再分析 → 可能再呼叫…
LLM     →  整合回覆
✓  自主決策、多輪迭代
✓  存取外部系統、執行動作
3 / 16

---

## Slide 4

01 · ①   A G E N T I C   L O O P   ·   概 念 圖
Agentic Tool Loop 概念圖
每一輪稱為一個 iteration,最多 maxIterations(預設 7)輪
User
Query
→
Build
Messages
→
Call
LLM API
→
Check
stop_reason
→
Execute
MCP Tools
↑   追加 tool_result 到 messages,回到 LLM
stop_reason = "tool_use"
→  執行工具 → 追加 tool_result → 進入下一輪
stop_reason = "end_turn"
→  跳出迴圈,把最終文字回給使用者
4 / 16

---

## Slide 5

02   S T O P   R E A S O N
stop_reason — 迴圈的關鍵判斷
Claude API 用這個欄位告訴 client 接下來該怎麼做
"end_turn"
模型認為已可回覆
結束迴圈,回傳最終回覆給使用者
"tool_use"
模型需要呼叫工具
執行工具 → 追加結果 → 進入下一輪
"max_tokens"
回覆被截斷
視為完成或觸發錯誤處理
while (stop_reason === "tool_use" && iteration < maxIterations) { … }
5 / 16

---

## Slide 6

02 · ①   T O O L _ U S E   B L O C K
tool_use — LLM 的工具呼叫指令
當 LLM 決定呼叫工具時,response.content 會含 tool_use block
// Claude API response.content 陣列中的一個 block
{
"type": "tool_use",
"id": "toolu_01A09q90qw90lq917835lq9",
"name": "search_library_books",  // MCP 工具名稱
"input": {                       // LLM 自動產生
"keyword": "人工智慧",
"limit": 10
}
}
id
唯一識別碼,後續 tool_result 必須對應同一個 id
name
對應 MCP Server 註冊的工具名稱
input
LLM 根據 JSON Schema 自動生成的參數
6 / 16

---

## Slide 7

02 · ②   T O O L _ R E S U L T
tool_result — 工具執行結果回傳
Client 執行 MCP 工具後,將結果以 user 角色追加到 messages
// 追加到 messages 陣列(role: user)
{
"role": "user",                  ← 注意 role
"content": [{
"type": "tool_result",
"tool_use_id": "toolu_01A09q...",  ← 同 id
"content": [{
"type": "text",
"text": "[{\"title\":\"深度學習入門\"},…]"
}],
"is_error": false
}]
}
tool_use_id
必須與 tool_use 的 id 一致
content
MCP 工具的實際回傳值(JSON 序列化為 text)
is_error
true 時 LLM 會嘗試錯誤處理或換工具
7 / 16

---

## Slide 8

02 · ③   M E S S A G E S   G R O W T H
Messages 陣列的成長過程
每一輪迭代都追加 assistant + user(tool_result) —— 陣列持續增長
system
System Prompt(角色設定 + 注入資訊)
user
中興大學圖書館有什麼新書?
assistant
我需要查詢…  + tool_use: search_new_books
第 1 輪
user
tool_result: [{"title":"深度學習入門",…}]
assistant
以下是圖書館最新書籍:1.《深度學習入門》…
第 2 輪
8 / 16

---

## Slide 9

02 · ④   P A R A L L E L   T O O L   C A L L S
一輪中呼叫多個工具
response.content 可以同時包含多個 tool_use block —— 平行執行
response.content = [
{ type: "text",
text: "讓我同時查詢課程和圖書資訊..." },
{ type: "tool_use", name: "search_courses",
id: "toolu_001", input: { keyword: "AI" } },
{ type: "tool_use", name: "search_library_books",
id: "toolu_002", input: { keyword: "AI" } }
]
// Client 端收集所有 tool_use
const toolCalls = response.content
.filter(c => c.type === "tool_use");
// → 依序執行每個工具,收集結果
▶  興大 AI 學伴:「幫我查 AI 課程和相關書籍」→ 一輪同時呼叫 search_courses + search_library_books
9 / 16

---

## Slide 10

03   C O R E   L O O P
chatWithStreaming() —— 核心迴圈
整個 agent 行為就是這 ~15 行 — while loop 加上 stop 條件
async chatWithStreaming(messages, options) {
const maxIterations = options.maxIterations || 7;
let iteration = 0;
while (iteration < maxIterations) {
iteration++;
// 最後一輪? 注入強制回覆提示
if (iteration === maxIterations) {
messages.push({ role: "user",
content: "這是最後一輪,請直接回覆..." });
}
response = await callLLM(messages, tools);
toolCalls = response.content.filter(c=>c.type==="tool_use");
if (toolCalls.length === 0) break;  // end_turn → 結束
results = await executeTools(toolCalls);
messages.push(assistantMsg, toolResultMsg);
}
}
10 / 16

---

## Slide 11

03 · ①   M A X _ I T E R A T I O N S   ·   強 制 回 覆
maxIterations 與強制回覆機制
避免 LLM 無限呼叫工具 —— 設上限 + 最後一輪強制總結
問題:無限迴圈風險
LLM 可能不斷呼叫工具而永遠不回覆使用者,造成:
✗  Token 成本無限增長
✗  回應時間過長
✗  使用者體驗極差
解法:maxIterations = 7
✓  設定最大迭代次數上限
✓  第 7 輪(最後一輪)時注入臨時
user message 強制模型停止使用
工具,直接整理回覆
「請不要再使用任何工具,
直接根據工具回傳的資料整理 Markdown 回覆。」
11 / 16

---

## Slide 12

03 · ②   M E T A D A T A   T R A C K I N G
Metadata 追蹤 —— 不污染 Messages
每輪的 stop_reason 與 token usage 用「平行陣列」記錄,結構分離
messages[]
messageStopReasons[]
messageUsages[]
assistant (tool_use)
tool_use
{ in: 850, out: 120 }
user (tool_result)
null
null
assistant (end_turn)
end_turn
{ in: 1200, out: 350 }
▶  索引對齊、結構分離 — 乾淨且不影響 API 呼叫格式
12 / 16

---

## Slide 13

03 · ③   S S E   S T R E A M I N G
SSE 串流 —— 即時回饋使用者
整個 agentic loop 過程,透過 Server-Sent Events 逐步通知前端
thinking_start
第 N 輪思考中…
每輪開始
tools_start
開始執行工具
偵測 tool_use
tool_executing
正在執行 search_books…
每個工具
tool_completed
工具完成,取得結果
工具完成
text_chunk
逐字回傳最終文字
最後回覆
done
串流結束
全部完成
13 / 16

---

## Slide 14

▶  切換到 Live Demo
sonnet-running-example.pptx
展示重點
1.  使用者提問 → Controller → 建立 messages 陣列
2.  第 1 輪 — 送往 Sonnet → 回傳 tool_use block
3.  MCP 工具執行(auto-inject user_id)
4.  第 2 輪 — 帶結果回 Sonnet → end_turn
5.  SSE 串流回傳完整回覆
14 / 16

---

## Slide 15

—  一  句  話  總  結  —
Agentic = stop_reason 驅動的 while 迴圈
—— 加上 maxIterations 安全閥 + 最後一輪強制回覆。
下一講:實務考量
「動手做 mini-project + 實務上的成本 / 模型 / 品質考量」
15 / 16

---

## Slide 16

★   R E C A P
本講回顧
下一講預告:實務考量 —— 模型選擇、Haiku alignment、工具品質
1
Agentic = 自主決策
LLM 不只回答問題,還能判斷需要什麼資訊、主動呼叫工具取得
2
tool_use / tool_result
Claude API 的核心機制 — stop_reason 驅動整個迴圈
3
maxIterations 安全閥
預設 7 輪上限 + 最後一輪強制回覆,平衡能力與安全
4
SSE 即時串流
每個步驟(思考、執行工具、回覆)都即時通知前端
16 / 16

---