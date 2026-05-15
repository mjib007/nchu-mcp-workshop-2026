# sonnet-running-example.pptx


## Slide 1

NCHU Claude MCP Client  ·  Running Example
Running Example
原始 Sonnet 流程  ·  逐步走過 9 個 Step
查詢範例
「中興大學圖書館有什麼新書?」
以下逐步走過從使用者送出到收到回覆的完整流程
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶

---

## Slide 2

STEP 1/9   R U N N I N G   E X A M P L E
Step 1:使用者送出查詢
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
瀏覽器透過 POST /api/chat/stream 送出訊息
• 需攜帶 Chat Token(經 Turnstile 驗證)
• API messages 陣列尚未建立
2 / 11

---

## Slide 3

STEP 2/9   R U N N I N G   E X A M P L E
Step 2:ChatController 接收
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
後端 controller 把 chat token 解開、確認登入狀態
• 注入「當前時間」與「登入狀態」進 system prompt
• 把 user 訊息 push 進空的 messages 陣列
3 / 11

---

## Slide 4

STEP 3/9   R U N N I N G   E X A M P L E
Step 3:raw-mcp-client 準備
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
建立 ClaudeClient 並收集所有 MCP server 的工具清單
• mcp.getAnthropicTools() → 把 33 個工具的 schema 收齊
• 把工具 schema 與 messages 一起準備好
4 / 11

---

## Slide 5

STEP 4/9   R U N N I N G   E X A M P L E
Step 4:第 1 輪 — 送往 Sonnet
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
ClaudeClient 呼叫 Anthropic API,messages + tools 一起送
• model: claude-sonnet-4 · max_tokens: 4096
• 等待 API 回傳 response.content
5 / 11

---

## Slide 6

STEP 5/9   R U N N I N G   E X A M P L E
Step 5:Sonnet 回傳 tool_use
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
Sonnet 判斷需要呼叫工具,回傳 tool_use block
• stop_reason: "tool_use"
• content[0]: { type: "tool_use", name: "search_new_books", input: {...} }
6 / 11

---

## Slide 7

STEP 6/9   R U N N I N G   E X A M P L E
Step 6:執行 MCP 工具
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
raw-mcp-client 從 tool_use 抽出 name + input,呼叫對應 MCP server
• mcp.callTool('search_new_books', { keyword: '新書' })
• Python MCP server 跑 SQL 查詢 → 回傳 10 筆新書
• auto-inject user_id(若工具需要)
7 / 11

---

## Slide 8

STEP 7/9   R U N N I N G   E X A M P L E
Step 7:第 2 輪 — 帶工具結果回 Sonnet
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
把 tool_result 以 role: user 追加到 messages,再叫一次 Sonnet
• tool_result.tool_use_id 必須對應第 1 輪的 id
• Sonnet 看 messages + 工具結果,生成最終文字
8 / 11

---

## Slide 9

STEP 8/9   R U N N I N G   E X A M P L E
Step 8:Sonnet 產生最終回覆
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
Sonnet 整合工具結果,生成自然語言 Markdown 回覆
• stop_reason: "end_turn"  ← 迴圈結束
• response.content[0].text 是 Markdown 格式的回覆
9 / 11

---

## Slide 10

STEP 9/9   R U N N I N G   E X A M P L E
Step 9:SSE 串流回覆給用戶
中興大學圖書館有什麼新書?
Browser
ChatController
raw-mcp-client.js
ClaudeClient
Claude Sonnet API
MCP Tools
SSE 串流回用戶
說明
把最終文字透過 Server-Sent Events 逐字推給瀏覽器
• 前端逐字渲染,使用者看到「打字機效果」
• 同時推送中繼事件:tool_executing / tool_completed / text_chunk / done
10 / 11

---

## Slide 11

—  原  始  流  程  回  顧  —
靜態 prompt + Sonnet + 2 輪 agentic loop
沒有工具選擇規則、沒有回覆格式規範、沒有 few-shot
靜態 System Prompt
config.json 固定角色 + 時間/登入狀態
Sonnet 模型
claude-sonnet-4 · $3.00 / 1M tokens
2 輪 Agentic Loop
Step 4 送出 → Step 7 回 result → Step 8 end_turn
→ 對照 Haiku Alignment 報告,看新流程如何在不犧牲品質下降成本
11 / 11

---