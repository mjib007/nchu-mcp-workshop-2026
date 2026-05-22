# Segment 3 · Live Demo 腳本

**用途**：講師現場操作興大 AI 學伴系統，向學員示範 multi-turn agentic loop 怎麼運作。

**對應投影片**：`03-agentic-tool-loop.pptx` § 4「Live Demo」段落（slides 13–14）。
**搭配影片**：`function-calling-video.mp4`（single-turn 機制複習）+ 待製作的 multi-turn loop 影片。

---

## ① Demo 前 4 件事檢查清單（開場前 5 分鐘）

| # | 檢查項 | 怎麼確認 | 失敗時的 plan B |
|---|--------|---------|----------------|
| 1 | 興大 AI 學伴 web 服務在線 | 瀏覽器開站名連得進 chat 介面 | 改用本地 mini-project 開 vLLM endpoint |
| 2 | 後端 Claude API key 有額度 | 任意問一個問題，能正常回應 | 換 OpenAI / 本地 Qwen / Gemma endpoint |
| 3 | 至少 5 個 MCP server 接得上 | 開系統儀表板看 server 狀態 | 至少要 search_library / search_courses 兩個能用 |
| 4 | 投影機解析度跟字級 OK | 把 chat 介面字級調到平時 1.5 倍，後排能讀 | 改用「逐句念出來」模式 |

---

## ② 5 個 Demo 問題（漸進難度）

### 問題 1 · 暖身 · single tool

> **「興大圖書館有幾本 AI 相關的書？」**

**預期 trajectory**：

```
Turn 1: LLM 看到問題 → tool_use(name="search_library_books", input={"query": "AI"})
Turn 1: tool_result = {"count": 247, "samples": [...]}
Turn 2: LLM 整合 → "圖書館共有 247 本 AI 相關的書..." → end_turn
```

**現場講解重點**：「LLM 看到問題,自己決定呼叫一個工具,拿到結果,回答你。**沒有人寫 if-else 告訴它要呼叫哪個工具**。」

**時間**：~30 秒（LLM 回應時間佔大部分）

---

### 問題 2 · 條件查詢 · single tool 加參數

> **「資工系有沒有教深度學習的老師？」**

**預期 trajectory**：

```
Turn 1: LLM → tool_use(name="search_teachers",
                       input={"department": "資工", "expertise": "深度學習"})
Turn 1: tool_result = [{name: "范耀中", ...}, {name: "李教授", ...}]
Turn 2: LLM → "資工系有 X 位老師教深度學習,分別是..." → end_turn
```

**現場講解重點**：「跟問題 1 不一樣的是,**LLM 知道要塞兩個參數**(department + expertise),這是從工具的 schema 學到的——回到 Segment 2 講的 `input_schema`。」

**時間**：~30 秒

---

### 問題 3 · 多輪迭代 · 一個 query 觸發 2-3 個 tool call

> **「我下學期想選一堂 AI 相關的課,看看哪些教授有開,簡單介紹一下他們」**

**預期 trajectory**：

```
Turn 1: LLM → tool_use(name="search_courses",
                       input={"keyword": "AI", "semester": "2025-spring"})
Turn 1: tool_result = [
  {course: "AI 概論", teacher: "張教授"},
  {course: "深度學習", teacher: "李教授"},
  {course: "自然語言處理", teacher: "范教授"}
]

Turn 2: LLM 看到三個教授,各自不認識
        → tool_use(name="get_teacher_info", input={"name": "張教授"})
        → 或 parallel tool_use 一次呼叫三個
Turn 2: tool_result × 3

Turn 3: LLM 整合三個教授資訊,加上課程資訊 → 完整回覆 → end_turn
```

**現場講解重點**：
- 「**這就是多輪 loop 的核心**:LLM 拿到第一個 tool 結果後,**自己判斷還需要更多資訊**,所以又呼叫第二、三個工具。」
- 「**現代的 LLM 還會 parallel tool calling**——一次呼叫三個 `get_teacher_info` 而不是一個一個來,大幅省時間。」
- 切換到開發者工具的 network tab 或 chat 介面下方的 tool trace,**讓學員看到實際的 tool_use 記錄**。

**時間**：~60-90 秒（最重要的一題,值得多停留)

---

### 問題 4 · 複合請求 · 跨領域兩個 tool

> **「我要找最近圖書館有什麼新書,順便看看星期一台中的天氣」**

**預期 trajectory**：

```
Turn 1: LLM → tool_use(name="search_library_recent_books", input={"days": 7})
            + tool_use(name="weather", input={"city": "台中", "day": "Monday"})
            (parallel)
Turn 1: tool_result × 2
Turn 2: LLM 整合 → "圖書館最近 7 天新到了 X 本書...台中星期一天氣..." → end_turn
```

**現場講解重點**：
- 「**這兩個工具完全不相關**(圖書館 + 天氣),但 LLM 自動知道要兩個都呼叫,而且**可以同時呼叫**。」
- 「對比 RAG (Segment 1):RAG 只能查文件,沒辦法同時做 retrieval + 執行 API 動作。**這就是 agentic 比 RAG 強的地方**。」

**時間**：~45 秒

---

### 問題 5 · 挑戰 · 可能撞 maxIterations

> **「我下學期能修哪些 AI 相關的選修課?這些課的老師最近發了哪些論文?幫我找出研究方向最對胃口的那位。」**

**預期 trajectory**：

```
Turn 1: search_courses (AI) → 拿到 N 門課
Turn 2: get_teacher_info × N (parallel)
Turn 3: arxiv_search × N (parallel) → 拿到每位老師最近論文
Turn 4: LLM 分析 → 整合回覆「最對胃口的是范教授,因為他做 LLM 推理...」→ end_turn
```

**現場講解重點**：
- 「這題如果 N=5 個老師,4 個 turn 就跑完 9-10 次 tool_use,**接近 maxIterations 上限(預設 7-10)**。」
- 「如果撞到上限,Claude API 會強制最後一輪不能再 tool_use,**只能用文字回覆已有的資訊**——這就是『**強制回覆機制**』。」
- 切換到投影片 § 3「迭代控制機制」,**讓學員看到 maxIterations 在 code 裡長什麼樣**。

**時間**：~90-120 秒（教學含量最高的一題,但時間風險也最大)

---

## ③ 5 個現場可能踩的坑 + 救援動作

### 坑 1 · 網路慢 / tool call timeout（高機率）

**症狀**：問題送出後 LLM 開始 tool_use,但 tool 回應超過 30 秒沒回來。

**救援**：
- 不要乾等。**邊等邊解釋**:「真實世界的 tool 不一定快,所以 maxIterations 跟 timeout 都是必要的護欄。」
- 如果完全卡住,**reload chat 介面重來,或換問題 1/2 那種單 tool 的題目**。

---

### 坑 2 · LLM 選錯 tool

**症狀**：問「資工系深度學習老師」,LLM 卻去 search_courses 而不是 search_teachers。

**救援**：
- **不要急著修**,反而是好教材:「**看到了嗎?LLM 也會選錯工具**——這是為什麼 Segment 2 講 tool 的 `description` 要寫清楚,description 寫不好 LLM 就選錯。」
- 接著切換到 § 2「Tool 註冊與描述」slide,**現場示範把 description 改清楚後重試**。

---

### 坑 3 · tool 回 error

**症狀**：tool 服務掛了,tool_result 回 `{"error": "service unavailable"}`。

**救援**：
- 看 LLM 如何反應。**好的 LLM 會直接告訴使用者:「這個工具暫時無法使用,請稍後再試」**,而不是無限重試。
- 講解:「**錯誤不該被偷偷吞掉,要當成資料傳回去給 LLM**——這在 Segment 5 實務考量會再深入。」

---

### 坑 4 · 達到 maxIterations

**症狀**：問題 5 那種複雜查詢,可能跑到 maxIterations=7 仍未 end_turn。

**救援**：
- **這是預設好的劇情**,不是 bug。
- 講解:「**最後一輪 Claude API 會強制 `tool_choice = none`,LLM 只能用已有的資訊回覆**,即使資訊不完整。這是為了防止無限迴圈。」
- 比較 maxIterations=7 vs maxIterations=15 的差異:後者比較貴但能處理更深的複合查詢。

---

### 坑 5 · 學員問奇怪的問題 / 沒有對應的 tool

**症狀**：學員試試看,問「台北市長是誰」之類沒有對應 MCP tool 的問題。

**救援**：
- 看 LLM 如何處理:**好的 LLM 會直接用訓練資料回答,不會去亂呼叫 search_teachers**。
- 講解:「**LLM 自己判斷是否需要 tool**——這是 agentic 的核心能力。**沒有人寫 if-else 說『遇到台北就用 tool A』**,是 LLM 看了 tool 清單後自己決定要不要用。」

---

## ④ Demo 段落時間配置(20 min 預算)

| 區塊 | 時間 | 內容 |
|------|------|------|
| 開場 | 2 min | 介紹我們要打開的系統,interface 走一遍 |
| 問題 1 | 2 min | 暖身,讓學員看完整流程一次 |
| 問題 2 | 2 min | 看 LLM 怎麼用 schema 帶參數 |
| 問題 3 | 5 min | **主菜——multi-turn loop。多停留,給學員問問題的空間** |
| 問題 4 | 3 min | 跨領域 parallel tool,呼應 Segment 1 RAG 對比 |
| 問題 5 | 4 min | 挑戰題 + maxIterations 講解 |
| 收尾 | 2 min | 帶回投影片 § 3 工程細節,鋪 Segment 4 hands-on |

如果 Demo 超時(網路慢、LLM 反應慢、學員提問多),**按順序砍掉問題 5 → 問題 4**,保住問題 1-3 是核心。

---

## ⑤ 學員可能會問的 5 個典型問題

1. **「LLM 知道有哪些 tool 可以用嗎?它怎麼選的?」**
   → 回到 Segment 2:每一輪 API call,**整份 tool 清單都會放在 system prompt 裡**,LLM 看完才決定要呼叫哪個或不呼叫。

2. **「如果工具回錯誤的資料怎麼辦?LLM 會發現嗎?」**
   → 不一定。**LLM 預設 trust tool 的回應**。要避免要靠 tool 自己做 validation,或在 prompt 上提醒 LLM 多檢查一次。

3. **「Loop 會不會跑太多次很貴?」**
   → 會。**Anthropic Console 可以設 token budget alarm**,Segment 5 會講 cost protection。

4. **「能不能讓 LLM 不要用 tool,只用訓練資料回答?」**
   → 可以,設 `tool_choice = "none"`。或者就不要在 API call 裡放 tools 清單。

5. **「興大這套系統的程式碼可以看嗎?」**
   → 原始碼是私有的,但線上版可以玩(eduxplore.nlpnchu.org)。我們 Segment 4 hands-on 跑的 `mini-project/` 就是它的公開精簡版,可以自由改。

---

## ⑥ Live Demo 後鋪陳到 Segment 4

「OK 看完了 agentic loop 怎麼運作。**接下來休息 10 分鐘,然後我們進到 hands-on——你自己的電腦上跑一個迷你版的 AI 學伴**。看完之後你會發現,做這套系統的程式碼比想像中少很多。」

→ 自然進到 Segment 4 開場。
