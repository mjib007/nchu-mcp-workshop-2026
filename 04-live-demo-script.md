# Segment 4 · Hands-on Live 講師手冊

**用途**:50 min hands-on 主場的講師現場執行劇本 — 預檢、時間管理、卡點救援、Q&A 預案。

**對應投影片**:`04-hands-on-lab.pptx`(12+ 張) + `04-hands-on-lab.md`(學員 landing) + `mini-project/` 可跑 code。
**搭配影片**:目前無 — Segment 4 的「視覺主菜」是學員自己的螢幕。

---

## ① Pre-flight 5 件事檢查清單(開場前 10 分鐘)

| # | 檢查項 | 怎麼確認 | 失敗時 Plan B |
|---|--------|---------|---------------|
| 1 | 教室網路:可連 GitHub + Anthropic | `curl -sI https://api.anthropic.com \| head -1` | 改用 NCHU vLLM 端點(infra/serve-*.sh)|
| 2 | API Key 額度:本月帳上至少 $5 | 開 Anthropic Console → Usage | 切到 Haiku(成本 1/12)+ 提醒學員別狂測 |
| 3 | 自己機器 setup.sh 全綠 | 在投影機那台跑 `./setup.sh` | 用前一晚做好的 docker image / VM snapshot |
| 4 | port 3000 跟 3001 都沒被佔 | `lsof -i :3000` `lsof -i :3001` | 改 `backend-node/server.js` 的 PORT |
| 5 | 投影機 + 學員螢幕分屏可切換 | 講師桌跑 demo + 學員自己跑 | 講師桌準備好 2 個視窗(自己 vs 學員視角) |

---

## ② 50 分鐘時間配置

> 來源:`CLAUDE.md` 已給的官方時間配置。本節照表操課。

| 時段 | 內容 | 學員 / 講師動作 | 風險點 |
|-----|------|-----------------|--------|
| 0–10 min | **講師 demo + 學員同步 setup.sh** | 學員邊聽邊跑 setup.sh,看到 5/5 ✅ 才能進下一段 | 網路慢/uv 沒裝/API key 沒填 — **這 10 min 救人比講還重要** |
| 10–20 min | **L1 Step 1–2(觀察 + 換 JSON)** | 學員問現有問題、看 trace → 改 `english_center.json` 換成自己領域資料 | 不知道用什麼資料(課表? 實驗室介紹?)|
| 20–35 min | **L1 Step 3–4(改 docstring + 重啟驗證)** | 學員改工具 description → 重啟 server → 確認 LLM 拿新資料回答 | docstring 太抽象 LLM 不選/快取沒重新讀 |
| 35–45 min | **交叉展示** | 點 3–5 位老師示範各自的助理 | 害羞、demo 失敗、想多展示 |
| 45–50 min | **Q&A + 鋪陳 Segment 5** | 收尾 L2/L3 自修路徑、銜接實務考量 | 時間爆 → 砍交叉展示 |

**時間爆掉的砍法(順序)**:
1. 交叉展示從 10 min → 5 min(只點 2 位)
2. L1 Step 4 驗證口頭講過,讓學員回家做
3. 跳過 L2/L3 preview,直接 Q&A

---

## ③ 5 個 Setup 常見卡點 + 救援動作

### 卡點 1 · uv 未安裝(中高機率)

**症狀**:`./setup.sh` 跑到 1/5 顯示 `❌ uv 未安裝`。

**救援**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.cargo/env   # 或重開 terminal
./setup.sh             # 重跑
```
講師台前對全班講一次,讓**所有人邊聽邊裝**(40 秒內完成)。

---

### 卡點 2 · API Key 沒填 / 填錯

**症狀**:`./setup.sh` 跑到 3/5 顯示 `❌ .env 的 ANTHROPIC_API_KEY 還是範例 placeholder`。

**救援**:
```bash
# 在 mini-project/ 內:
nano .env                # 或 vim、code、subl
# 把 ANTHROPIC_API_KEY=sk-ant-... 改成真正的 key
./setup.sh
```

**講解重點**:「key 是字串 `sk-ant-` 開頭 + 一串長英數。**注意空白跟引號**:`ANTHROPIC_API_KEY="sk-ant-..."` 加引號會壞,不要加。」

---

### 卡點 3 · port 3000 被佔(中機率,Mac 上常見)

**症狀**:`./setup.sh` 跑到 5/5 顯示 `❌ port 3000 已被其他程式佔用`。

**救援**:
```bash
lsof -i :3000              # 找 PID
kill -9 <PID>              # 殺掉
# 或改用其他 port:
PORT=3010 npm start        # 在 backend-node/ 內
```

---

### 卡點 4 · `npm install` 失敗(低機率,網路問題)

**症狀**:`./setup.sh` 跑到 4/5 顯示 `❌ npm install 失敗`。

**救援**:
```bash
cat /tmp/mini-npm.log | tail -30
# 常見:
# - ENOTFOUND registry.npmjs.org → 網路問題,切手機熱點
# - EACCES → 權限,改 npm 全域路徑 OR 用 nvm
# - peer deps 衝突 → npm install --legacy-peer-deps
```

---

### 卡點 5 · L1 改完 docstring 後 LLM 還是答錯(高機率,L1 主要卡點)

**症狀**:學員改了 `english_center.json` + `hello_tool.py` 的 docstring,但問問題 LLM 仍走原 tool 或答錯。

**救援**(逐個排除):
1. **server 真的重啟了嗎?** Ctrl+C 後 `npm start`(MCP server 是 subprocess,Node restart 才會重新 spawn Python)
2. **docstring 寫得夠具體嗎?** 寫「`查實驗室介紹` — 學生問實驗室主題、成員、研究方向時用此工具」比「`查資料`」好 10 倍
3. **JSON 結構有沒有壞?** `python3 -c "import json; json.load(open('data/your_file.json'))"` 一行驗
4. **Claude API 真的有收到新 tool description?** 看 `backend-node` log,搜尋 `tool_use` 看實際送了什麼

**講師現場教學重點**:「**docstring 是 tool 對 LLM 的說明書**。寫不好,LLM 不會選你的 tool — Segment 5 會深入這個品質陷阱。」

---

## ④ L1 Step-by-Step 講師指引

### Step 1(5 min)— 先觀察

學員動作:啟動 server → 問「英文中心幾點開門?」→ 看 terminal 印出 `[tool_use] get_english_center_info`。

**講師台詞**:「**這就是 Segment 3 講的 tool_use 在你自己機器上發生**。terminal 印出的那行,就是 LLM 對 Claude API 說『我要呼叫 get_english_center_info』。」

### Step 2(5 min)— 換 JSON

學員動作:複製 `data/english_center.json` 改檔名 → 改成自己領域資料 → 重啟。

**講師台詞**:「**一行 Python 都不用改**。tool 怎麼讀資料寫死在 hello_tool.py,你只負責**換 JSON**。」

**check-in**:走 2 圈看哪些學員還在 Step 1。如果超過 1/3 卡 Step 1 → 額外 2 min 統一處理。

### Step 3(8 min)— 改 docstring

學員動作:改 `hello_tool.py` 裡 `@mcp.tool()` 的 docstring。

**講師台詞**:「現在 LLM 看到的工具名稱還叫 `get_english_center_info`。我們把它改成符合你領域的名字 + 寫更精準的 description。」

**現場示範**:
```python
@mcp.tool()
def get_lab_info(query: str) -> dict:
    """查詢 X 實驗室的研究方向、成員、近期論文。
    
    當學生問「實驗室在做什麼」「指導老師是誰」「最近發了什麼」時呼叫此工具。
    """
    ...
```

### Step 4(7 min)— 重啟驗證

學員動作:Ctrl+C 重啟 → 問新領域問題 → 看 LLM 是否走新 tool 名稱。

**講師台詞**:「**如果 LLM 沒走你新的 tool 名稱,就是 docstring 沒寫好**。Segment 5 會講『docstring quality 陷阱』,現在你已經親身體驗了。」

---

## ⑤ 交叉展示段(35–45 min)— 怎麼帶

### 點人原則

- **挑 3 位**:研究方向差異大的(理工 + 文 + 社科一位最好)
- **避免**:看起來還在 setup 卡的、明顯害羞的、坐角落的(會緊張)
- **告訴他們**:「就問你領域的一個典型問題,看 AI 怎麼回答」

### 5 分鐘 demo 模板(給每位)

> 「我是 X 系 X 老師,我做 X 領域。
>  我把 JSON 改成我實驗室的介紹,改了 docstring 叫 search_lab_info。
>  我問:『X 實驗室有什麼研究主題?』」

### 預期翻車與救援

- **AI 答錯**:「這就是 docstring 沒寫好的真實案例 — 我們現場一起 debug」(教學機會)
- **完全 setup 沒過**:不要逼,跳下一位,「等一下 Q&A 時我幫您看」

---

## ⑥ 學員可能問的 5 個問題

1. **「我可以用 OpenAI / Gemini 嗎?」**
   → 可以但需要小改:換 `backend-node/llm-client.js` 的 client init。**Segment 5 會講 multi-provider adapter**。

2. **「上線真的用這個架構嗎?」**
   → 教學用刻意極簡。**production 需要加** rate limit、cache、auth、observability。看 `course-ta-agent/` 是中等規模版本,興大 AI 學伴是大規模版本(~239 tools)。

3. **「我用我課程的 PDF/Word 可以嗎?」**
   → mini-project 用 JSON 是教學簡化。**production 通常先 parse 成 JSON**(用 LLM 或 unstructured.io)。L3 lab 會做 arXiv API 直連,L2 lab 會做關鍵字搜尋。

4. **「會不會被 prompt injection?」**
   → 會。**Segment 5 §2 會深入講 tool-calling 邊界防禦**。教學版沒做防禦,production 一定要做。

5. **「我下課可以拿回去當研究助理嗎?」**
   → 可以!MIT-license,改一改就是你的。**L2 / L3 lab 帶你做進階版**(加搜尋 / 接外部 API)。

---

## ⑦ 鋪陳 Segment 5(45–50 min)

「OK 你已經親手做出一個會自己選 tool、用你資料回答的 AI 助理。
 接下來 10 分鐘 Segment 5,我們講**從這個 mini-project 到 production 中間還缺什麼**:
 - **Scale**:你的 1 個 tool vs 興大 AI 學伴 239 tools
 - **Quality**:你剛剛踩到的 docstring 陷阱怎麼系統化解
 - **Model**:什麼時候用 Sonnet、什麼時候用 Haiku
 - **Cost**:剛剛你問那 3 個問題大概花了 $0.001,放大到 10 人 3 hr 是多少
 ↓ 進 Segment 5」

→ 自然進到 Segment 5 開場。
