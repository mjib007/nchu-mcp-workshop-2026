# 04-hands-on-lab.pptx


## Slide 1

MCP 入門工作坊  ·  第四講
動手做
Hands-on Lab  ·  50 minutes
mini-project 實作主場 — 現場跑起你自己領域的 AI agent
范耀中  Yao-Chung Fan
github.com/UDICatNCHU/nchu-mcp-workshop-2026

---

## Slide 2

00   O U T C O M E S
本節產出物
50 分鐘後,你將親手擁有
✓
跑起來的 MCP agent
Node.js + Python FastMCP + 極簡 HTML chat
三層完整可運作
✓
一支「你領域」的工具
換 JSON 就好,0 行 Python
實驗室介紹 / 課程大綱 / 研究成果清單都行
✓
Agent 資料流的脈動感
工具選擇 → 參數綁定 → LLM 摘要
在 terminal 看它一次跑通
✓
L2 / L3 挑戰路徑
帶回去繼續深入:加搜尋工具、呼叫外部 API
2 / 12

---

## Slide 3

00 · ②   S C H E D U L E
50 分鐘時間配置
講師 10 min 引導 + 40 min 巡場陪跑
時段 (min)
做什麼
產出
0–10
講師 demo + 學員同步 ./setup.sh
環境綠燈 5/5 ✅
10–20
L1 Step 1–2:觀察現況 + 換自己 JSON
data/your.json
20–35
L1 Step 3–4:改 docstring + 重啟驗證
問自己資料會答
35–45
交叉展示 — 3–4 位老師 demo 自己領域
見識不同落地方式
45–50
Q&A + 為 L2/L3 與 Segment 5 鋪陳
清楚下一步
▶  40 分鐘巡場預計 80% 在幫卡住的老師 — 開場預演越短,越多時間陪跑
3 / 12

---

## Slide 4

01   A R C H I T E C T U R E   R E C A P
架構快速回顧
不是單向 pipeline —— Node ⟷ LLM 多輪迭代才是 agent
Browser
web/index.html  ·  fetch POST /chat
Node Server
Express  ·  LLMClient  ·  MCPClient
Python FastMCP
@mcp.tool()  ·  stdio JSON-RPC
data/
你的 JSON  ·  外部 API
☁  LLM API
Claude · Gemma
· GPT · …
▶  Node ⟷ LLM 之間迭代「問 → tool_use → 跑 → 答 → 再問」直到 end_turn
4 / 12

---

## Slide 5

01 · ①   L L M - C L I E N T . J S   ·   2 0   L I N E S
agent loop 真實長這樣
backend-node/llm-client.js — 整個系統的 20 行核心
async chat(messages) {
const history = [...messages];
for (let i = 0; i < maxIterations; i++) {  // ← 護欄
const resp = await anthropic.messages.create({
model, tools: mcp.getAnthropicTools(),  // ① 餵 tools
messages: history,
});
history.push({ role: "assistant", content: resp.content });
if (resp.stop_reason !== "tool_use") {  // ② 結束
return { reply: extractText(resp) };
}
const toolUses = resp.content                  // ③ 跑工具
.filter(b => b.type === "tool_use");
const toolResults = await Promise.all(
toolUses.map(t => mcp.callTool(t.name, t.input))
);
history.push({ role: "user", content: toolResults });
}
}
🛑 maxIterations=10 是護欄;整個 agent 沒有 magic — 就是 for-loop + if-else
5 / 12

---

## Slide 6

02   P R E - W O R K S H O P
行前準備(請於上課前完成)
這幾步無關概念,但卡住會吃掉現場時間
1
git clone 教材
$ git clone github.com/UDICatNCHU/nchu-mcp-workshop-2026
$ cd nchu-mcp-workshop-2026/mini-project
2
取得 LLM 存取(二選一)
雲端:Anthropic Console 申請 API key(新帳號 $5 試用)
本地:確認你會走 NCHU vLLM 路線
3
建 .env 並填入金鑰
$ cp .env.example .env
$ vim .env  # 填 ANTHROPIC_API_KEY
4
跑環境預檢
$ ./setup.sh
→ 看到 5/5 ✅ 代表現場可以直接 npm start
6 / 12

---

## Slide 7

02 · ①   Q U I C K   S T A R T
現場啟動 (5 分鐘)
三條指令 + 對照「該長什麼樣」
▶  你輸入
$ ./setup.sh                           # 1. sanity check 環境
$ cd backend-node && npm start         # 2. 啟動 backend + MCP
$ open http://localhost:3000           # 3. 瀏覽器
▶  你應該看到
> mini-assistant@1.0.0 start
> node server.js
✓ hello_tool → get_english_center_info
✓ teachers_tool → search_teachers, get_teacher_detail
✓ weather_tool → get_weather
→ Mini AI Assistant: http://localhost:3000
🎉 三行 ✓ + URL → MCP server 都連上了
7 / 12

---

## Slide 8

02 · ②   L L M   R O U T E   ·   1   L I N E   T O   S W I T C H
選你的 LLM 路線
.env 一行切換 —— 因為 MCP 工具兩家都認
☁  雲端 · Anthropic Claude
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-haiku-4-5
# 優點
# • 工具呼叫品質最佳
# • 啟動快,$5 試用額
🏠  本地 · NCHU vLLM (Gemma 4)
# .env
LLM_PROVIDER=openai
OPENAI_BASE_URL=http://<ws>:8000/v1
OPENAI_API_KEY=dummy
OPENAI_MODEL=gemma-4
# 優點
# • 0 美金,無 token 限制
💎  N+M 的甜蜜:你的工具一支不變,adapter 差別只在 mcp-client.js 幾行
8 / 12

---

## Slide 9

03   L A B   1   ·   換   J S O N
Lab 1 — 換 JSON 做你領域的助理
0 行 Python · 40 分鐘 · 現場必做
①
觀察
看 [tool_use] log
AI 摘要 JSON
5 min
②
換資料
編輯 data/*.json
放你的領域內容
15 min
③
改說明書
docstring 的使用情境
決定工具呼叫率
10 min
④
驗證
重啟 npm start
問自己資料問題
5 min
▶  產出:你的 AI 助理會回答你自己放進去的資料 — 不是英文中心 demo 了
9 / 12

---

## Slide 10

03 · ①②   L A B   1   ·   S T E P S   1 - 2
Step 1–2:觀察 → 換 JSON
還沒動到 Python 一個字
Step 1  觀察 (5 min)
在瀏覽器問:
「英文中心幾點開門?」
在 terminal 觀察:
[tool_use] get_english_center_info
💡  關鍵觀察:
Claude 不會 dump 整份 JSON,挑出「開放時間」那一段。這是 LLM 對 tool result 的摘要 — agent 的靈魂。
Step 2  換 JSON (15 min)
編輯:
mcp-server-py/data/english_center.json
換成你自己的領域資料:
• 你的研究室介紹
• 你教的一門課(大綱/作業/評分)
• 你系所的 FAQ / 研究成果清單
⚠ JSON 語法錯會卡住:
python3 -m json.tool data/xxx.json
10 / 12

---

## Slide 11

03 · ③   L A B   1   ·   S T E P   3   ·   D O C S T R I N G
Step 3:改 docstring (10 min)
直接拿 repo 兩支真實工具對照 —— 同樣語法、教 LLM 不同事
📝  minimal — hello_tool.py
@mcp.tool()
def get_english_center_info() -> str:
"""取得中興大學英語自學暨
檢定中心的完整資訊。
回傳 JSON 字串,包含:
名稱、開放時間、地點、設備…
使用情境:使用者詢問英語
自學中心相關問題時呼叫。
"""
📖  rich — teachers_tool.py
@mcp.tool()
def get_teacher_detail(name: str) -> str:
"""取得指定教授的完整資訊
(email、辦公室、研究領域)。
使用情境:使用者問某位教授
的聯絡方式或完整資料時呼叫。
通常在 search_teachers 找到
候選名單後再呼叫。 ← 跨工具線索
Args:
name: 教授姓名(完整中文)。
▶  影響 LLM 行為的 3 元素:使用情境(該不該叫) / Args 描述(怎麼填) / 跨工具線索(呼叫順序)
11 / 12

---

## Slide 12

★   L 2 / L 3   P R E V I E W
L2 / L3 — 帶回去繼續深入
課後自修,參考 mini-project/docs/labs/
L1
完成
換 JSON 做你領域的助理
課堂現場必做
0 行 Python
L2
+1 hr
加一支有參數的搜尋工具
課後自修
寫一個 @mcp.tool()
L3
+2 hr
呼叫外部 API
課後自修
串 arxiv/weather API
▶  三關手冊:mini-project/docs/labs/L1-customize-your-data.md / L2 / L3
12 / 12

---