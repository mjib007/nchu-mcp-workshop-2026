# haiku-alignment-report.pptx


## Slide 1

NCHU Claude MCP Client  ·  優化報告
Haiku Alignment
從 Sonnet 切到 Haiku — Few-shot Alignment 降 73% 成本
73%
input token 成本節省

---

## Slide 2

01   G O A L
優化目標
將基底模型從 Sonnet 切換至 Haiku,同時透過 few-shot alignment 維持品質
$0.80
vs $3.00 / 1M tokens
降低成本
Haiku input token 價格僅 Sonnet 27%
3,200+
筆歷史 Trace 檢索
維持品質
Few-shot 範例引導工具選擇與回覆格式
5
類回覆格式規範
結構化輸出
五大分類模板,確保 Markdown 回覆一致
2 / 9

---

## Slide 3

02   F L O W   C O M P A R E
請求處理流程對比
綠色 = 新增或變更的元件
原始流程
User Query
ChatController (注入時間 + 登入狀態)
raw-mcp-client.js
ClaudeClient (claude-client.js)
System Prompt = 靜態 config
⬤ Claude Sonnet API
回覆直接串流給用戶
新流程
User Query
ChatController (注入時間 + 登入狀態)
raw-mcp-client.js
claude-client-aligned.js
AlignmentMiddleware.enrichSystemPrompt()
⬤ Claude Haiku API
回覆直接串流給用戶
3 / 9

---

## Slide 4

02 · ①   N E W   C O M P O N E N T S
新增元件
在不改變既有架構的前提下,增加三層品質保護
AlignmentMiddleware
api/alignment-middleware.js
從歷史 trace 檢索相似範例 — keyword / embedding / hybrid
Aligned ClaudeClient
api/claude-client-aligned.js
每次 API 呼叫前透過 middleware 動態豐富 system prompt
格式規範
config/response-format-rules.js
書籍/課程/活動/人員/法規 五大分類 Markdown 模板
Trace 資料
data/nchu_traces/*.jsonl
3,207 筆正例 + 876 筆負例,作為 few-shot 檢索來源
4 / 9

---

## Slide 5

02 · ②   Q U A L I T Y   P R O T E C T I O N
Enriched Prompt 三層結構
Query → Retrieval → Enriched Prompt → Haiku Loop
ALIGNMENT_RULES
工具選擇正確性
選對工具、填對參數
RESPONSE_FORMAT_RULES
回覆格式品質
Markdown 標題/列表/圖片
Top-9 Few-shot Examples
具體示範
query → tool_calls 配對
▶  Query → Embedding/Keyword (3,200+ traces) → Enriched Prompt → Haiku Loop (≤7) → Markdown
5 / 9

---

## Slide 6

03   C O S T   I M P A C T
成本影響分析
節省 73% input token 費用,額外開銷可忽略不計
模型成本比較
73 %
input token 費用
Sonnet:   $3.00 / 1M tokens
Haiku:    $0.80 / 1M tokens
額外開銷
格式規範額外 token
~300 tokens/request — 五大分類模板
Few-shot 範例額外 token
~1,200 tokens/request — Top-9 相似範例
每次請求額外成本
~ $0.0012 可忽略不計
6 / 9

---

## Slide 7

03 · ①   M O D E L S   &   F A L L B A C K
模型與備援配置
最後一輪格式化提示也跟著改
項目
原始
新流程
主要模型
Claude Sonnet
Claude Haiku
備援順序
ollama → claude
claude → ollama
Controllers
硬編碼 claude-sonnet-4
config.claudeModel[0] 統一控管
最後一輪提示對比
原始:「不要用工具,直接回覆」
新流程:「不要用工具,整理出結構化 Markdown 回覆」+ 5 點格式要求
7 / 9

---

## Slide 8

04   L I M I T A T I O N S
已知限制
整體成效正面,但仍有三項限制需注意
中
多語系影響
Trace 與規則皆為中文,非中文使用者 few-shot 匹配率較低
低
工具選擇差異
Haiku 選擇的工具與 Sonnet 不完全一致,但方向通常正確
低
部分 Controller 未套用
AdminController / QuickQuestionController 仍用原版
8 / 9

---

## Slide 9

—  總  結  —
NCHU Claude MCP Client — Haiku Alignment 優化
73%
成本節省
Input token 費用大幅降低
3,200+
Trace 範例
Few-shot alignment 品質基礎
5 類
格式規範
書籍/課程/活動/人員/法規
7 輪
Agentic Loop
最大工具呼叫迭代次數
9 / 9

---