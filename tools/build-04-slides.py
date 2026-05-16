#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 04-hands-on-lab.pptx in the new visual style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "04-hands-on-lab.pptx"

TOTAL = 13


def build_cover(prs):
    s = _blank_slide(prs, BG_WHITE)
    _rect(s, 0.85, 0.55, 0.55, 0.07, VIOLET)
    _text(s, 0.85, 0.75, 12, 0.4, "MCP 入門工作坊  ·  第四講",
          font=FONT_BODY, size=15, color=MUTED, bold=True)
    _text(s, 0.85, 2.0, 12, 1.6, "動手做",
          font=FONT_TITLE, size=84, color=INK, bold=True)
    _text(s, 0.85, 3.5, 12, 0.7,
          "Hands-on Lab  ·  50 minutes",
          font=FONT_BODY, size=26, color=VIOLET, bold=True)
    _text(s, 0.85, 4.3, 12, 0.5,
          "mini-project 實作主場 — 現場跑起你自己領域的 AI agent",
          font=FONT_BODY, size=18, color=INK_SOFT)
    _text(s, 0.85, 6.3, 8, 0.4,
          "范耀中  Yao-Chung Fan",
          font=FONT_BODY, size=18, color=INK, bold=True)
    _text(s, 0.85, 6.75, 8, 0.4,
          "github.com/UDICatNCHU/nchu-mcp-workshop-2026",
          font=FONT_CODE, size=14, color=MUTED)


def build_outcomes(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "00", "O U T C O M E S", accent=VIOLET)
    slide_title(s, "本節產出物", y=0.95)
    slide_subtitle(s, "50 分鐘後,你將親手擁有", y=1.85)

    items = [
        ("跑起來的 MCP agent",
         "Node.js + Python FastMCP + 極簡 HTML chat\n三層完整可運作",
         VIOLET, VIOLET_PASTEL),
        ("一支「你領域」的工具",
         "換 JSON 就好,0 行 Python\n實驗室介紹 / 課程大綱 / 研究成果清單都行",
         ORANGE, ORANGE_PASTEL),
        ("Agent 資料流的脈動感",
         "工具選擇 → 參數綁定 → LLM 摘要\n在 terminal 看它一次跑通",
         TEAL, TEAL_PASTEL),
        ("L2 / L3 挑戰路徑",
         "帶回去繼續深入:加搜尋工具、呼叫外部 API",
         PINK, PINK_PASTEL),
    ]
    card_w = 2.95
    for i, (title, body, accent, fill) in enumerate(items):
        x = 0.85 + i * (card_w + 0.20)
        _rounded(s, x, 2.85, card_w, 3.5, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 3.05, card_w - 0.5, 0.55, "✓",
              font=FONT_TITLE, size=22, color=accent, bold=True)
        _text(s, x + 0.25, 3.6, card_w - 0.5, 0.7, title,
              font=FONT_TITLE, size=15, color=INK, bold=True)
        _multi(s, x + 0.25, 4.4, card_w - 0.5, 2.0,
               [{"text": line, "font": FONT_BODY, "size": 13,
                 "color": INK_SOFT, "space_after": 4}
                for line in body.split("\n")])
    page_number(s, 2, TOTAL)


def build_schedule(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "00 · ②", "S C H E D U L E", accent=VIOLET)
    slide_title(s, "50 分鐘時間配置", y=0.95)
    slide_subtitle(s, "講師 10 min 引導 + 40 min 巡場陪跑", y=1.85)

    rows = [
        ("0–10",  "講師 demo + 學員同步 ./setup.sh",      "環境綠燈 5/5 ✅"),
        ("10–20", "L1 Step 1–2:觀察現況 + 換自己 JSON",  "data/your.json"),
        ("20–35", "L1 Step 3–4:改 docstring + 重啟驗證", "問自己資料會答"),
        ("35–45", "交叉展示 — 3–4 位老師 demo 自己領域",   "見識不同落地方式"),
        ("45–50", "Q&A + 為 L2/L3 與 Segment 5 鋪陳",     "清楚下一步"),
    ]

    # Header
    cols_x = [0.85, 2.4, 8.0]
    cols_w = [1.5, 5.5, 4.95]
    _rect(s, cols_x[0], 2.7, cols_w[0], 0.5, VIOLET_PASTEL)
    _rect(s, cols_x[1], 2.7, cols_w[1], 0.5, ORANGE_PASTEL)
    _rect(s, cols_x[2], 2.7, cols_w[2], 0.5, TEAL_PASTEL)
    _text(s, cols_x[0], 2.7, cols_w[0], 0.5, "時段 (min)",
          font=FONT_TITLE, size=13, color=VIOLET, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, cols_x[1], 2.7, cols_w[1], 0.5, "做什麼",
          font=FONT_TITLE, size=13, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, cols_x[2], 2.7, cols_w[2], 0.5, "產出",
          font=FONT_TITLE, size=13, color=TEAL_DEEP, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    rh = 0.55
    for ri, row in enumerate(rows):
        y = 3.2 + ri * rh
        if ri % 2:
            _rect(s, 0.85, y, 12.1, rh, SLATE_PASTEL)
        _text(s, cols_x[0], y, cols_w[0], rh, row[0],
              font=FONT_CODE, size=12, color=VIOLET, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, cols_x[1] + 0.2, y, cols_w[1] - 0.2, rh, row[1],
              font=FONT_BODY, size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, cols_x[2] + 0.2, y, cols_w[2] - 0.2, rh, row[2],
              font=FONT_BODY, size=13, color=INK_SOFT, italic=True,
              anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "40 分鐘巡場預計 80% 在幫卡住的老師 — 開場預演越短,越多時間陪跑",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 3, TOTAL)


def build_architecture(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01", "A R C H I T E C T U R E   R E C A P", accent=ORANGE)
    slide_title(s, "架構快速回顧", y=0.95)
    slide_subtitle(s, "不是單向 pipeline —— Node ⟷ LLM 多輪迭代才是 agent", y=1.85)

    layers = [
        ("Browser",          "web/index.html  ·  fetch POST /chat",          BLUE,   BLUE_PASTEL),
        ("Node Server",      "Express  ·  LLMClient  ·  MCPClient",          VIOLET, VIOLET_PASTEL),
        ("Python FastMCP",   "@mcp.tool()  ·  stdio JSON-RPC",                TEAL,   TEAL_PASTEL),
        ("data/",            "你的 JSON  ·  外部 API",                        ORANGE, ORANGE_PASTEL),
    ]
    band_h = 0.7
    band_y0 = 2.65
    for i, (name, desc, accent, fill) in enumerate(layers):
        y = band_y0 + i * (band_h + 0.15)
        _rounded(s, 0.85, y, 9.0, band_h, fill, line_color=accent, line_w=2)
        _rect(s, 0.95, y + 0.10, 0.20, band_h - 0.20, accent)
        _text(s, 1.4, y, 2.5, band_h, name,
              font=FONT_TITLE, size=16, color=accent, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 4.0, y, 5.8, band_h, desc,
              font=FONT_CODE, size=13, color=INK_SOFT, anchor=MSO_ANCHOR.MIDDLE)

    # LLM API on the right
    _rounded(s, 10.3, 3.5, 2.6, 1.7, MIDNIGHT, line_color=VIOLET, line_w=2)
    _text(s, 10.3, 3.65, 2.6, 0.5, "☁  LLM API",
          font=FONT_TITLE, size=15, color=VIOLET, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 10.3, 4.2, 2.6, 0.8,
          "Claude · Gemma\n· GPT · …",
          font=FONT_BODY, size=12, color=CODE_FG,
          align=PP_ALIGN.CENTER)

    callout_box(s, 0.85, 6.4, 12, 0.55,
                "Node ⟷ LLM 之間迭代「問 → tool_use → 跑 → 答 → 再問」直到 end_turn",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 4, TOTAL)


def build_agent_loop_code(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ①", "L L M - C L I E N T . J S   ·   2 0   L I N E S",
                 accent=ORANGE)
    slide_title(s, "agent loop 真實長這樣", y=0.95)
    slide_subtitle(s, "backend-node/llm-client.js — 整個系統的 20 行核心", y=1.85)

    code_lines = [
        ("async chat(messages) {",                                       CODE_FG),
        ("  const history = [...messages];",                             CODE_FG),
        ("  for (let i = 0; i < maxIterations; i++) {  // ← 護欄",       CODE_ORANGE),
        ("    const resp = await anthropic.messages.create({",           CODE_FG),
        ("      model, tools: mcp.getAnthropicTools(),  // ① 餵 tools",  CODE_FG),
        ("      messages: history,",                                     CODE_FG),
        ("    });",                                                      CODE_FG),
        ('    history.push({ role: "assistant", content: resp.content });', CODE_FG),
        ("",                                                             CODE_FG),
        ('    if (resp.stop_reason !== "tool_use") {  // ② 結束',        CODE_ORANGE),
        ("      return { reply: extractText(resp) };",                   CODE_FG),
        ("    }",                                                        CODE_FG),
        ("",                                                             CODE_FG),
        ("    const toolUses = resp.content                  // ③ 跑工具", CODE_FG),
        ('      .filter(b => b.type === "tool_use");',                   CODE_FG),
        ("    const toolResults = await Promise.all(",                   CODE_FG),
        ("      toolUses.map(t => mcp.callTool(t.name, t.input))",       CODE_FG),
        ("    );",                                                       CODE_FG),
        ('    history.push({ role: "user", content: toolResults });',    CODE_FG),
        ("  }",                                                          CODE_FG),
        ("}",                                                            CODE_FG),
    ]
    code_block(s, 0.85, 2.5, 12, 4.0, code_lines, size=11)

    callout_box(s, 0.85, 6.65, 12, 0.4,
                "🛑 maxIterations=10 是護欄;整個 agent 沒有 magic — 就是 for-loop + if-else",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="", size=12)
    page_number(s, 5, TOTAL)


def build_setup_steps(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02", "P R E - W O R K S H O P", accent=TEAL)
    slide_title(s, "行前準備(請於上課前完成)", y=0.95, size=32)
    slide_subtitle(s, "這幾步無關概念,但卡住會吃掉現場時間", y=1.85)

    steps = [
        ("1", "git clone 教材",
         "$ git clone github.com/UDICatNCHU/nchu-mcp-workshop-2026\n$ cd nchu-mcp-workshop-2026/mini-project"),
        ("2", "取得 LLM 存取(二選一)",
         "雲端:Anthropic Console 申請 API key(新帳號 $5 試用)\n本地:確認你會走 NCHU vLLM 路線"),
        ("3", "建 .env 並填入金鑰",
         "$ cp .env.example .env\n$ vim .env  # 填 ANTHROPIC_API_KEY"),
        ("4", "跑環境預檢",
         "$ ./setup.sh\n→ 看到 5/5 ✅ 代表現場可以直接 npm start"),
    ]
    y = 2.6
    for num, title, code in steps:
        _rounded(s, 0.85, y, 12, 0.85, TEAL_PASTEL,
                 line_color=TEAL, line_w=2)
        circle_number(s, 1.2, y + 0.42, num, TEAL, r=0.26)
        _text(s, 1.8, y, 4.5, 0.85, title,
              font=FONT_TITLE, size=15, color=TEAL_DEEP, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _multi(s, 6.5, y + 0.08, 6.3, 0.78,
               [{"text": line, "font": FONT_CODE, "size": 11,
                 "color": INK, "space_after": 2}
                for line in code.split("\n")])
        y += 1.0
    page_number(s, 6, TOTAL)


def build_quick_start(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ①", "Q U I C K   S T A R T", accent=TEAL)
    slide_title(s, "現場啟動 (5 分鐘)", y=0.95)
    slide_subtitle(s, "三條指令 + 對照「該長什麼樣」", y=1.85)

    pastel_card(s, 0.85, 2.7, 12, 1.7, accent=TEAL, fill=TEAL_PASTEL,
                title="▶  你輸入")
    code_block(s, 1.05, 3.3, 11.5, 1.05, [
        ("$ ./setup.sh                           # 1. sanity check 環境", CODE_FG),
        ("$ cd backend-node && npm start         # 2. 啟動 backend + MCP", CODE_FG),
        ("$ open http://localhost:3000           # 3. 瀏覽器",            CODE_FG),
    ], size=11)

    pastel_card(s, 0.85, 4.55, 12, 2.0, accent=VIOLET, fill=VIOLET_PASTEL,
                title="▶  你應該看到")
    code_block(s, 1.05, 5.15, 11.5, 1.35, [
        ("> mini-assistant@1.0.0 start",                              CODE_COMMENT),
        ("> node server.js",                                          CODE_COMMENT),
        ("",                                                          CODE_FG),
        ("✓ hello_tool → get_english_center_info",                    CODE_STRING),
        ("✓ teachers_tool → search_teachers, get_teacher_detail",     CODE_STRING),
        ("✓ weather_tool → get_weather",                              CODE_STRING),
        ("→ Mini AI Assistant: http://localhost:3000",                CODE_ORANGE),
    ], size=10)

    _text(s, 0.85, 6.65, 12, 0.3,
          "🎉 三行 ✓ + URL → MCP server 都連上了",
          font=FONT_BODY, size=13, color=TEAL_DEEP, italic=True,
          align=PP_ALIGN.CENTER)
    page_number(s, 7, TOTAL)


def build_troubleshooting(prs):
    """Slide 8 — 卡住了?5 個常見救援 cheat sheet.
    Inserted between quick_start (slide 7) and llm_routes (slide 9 was 8)
    to give 講師 + 學員 a single-screen reference when setup.sh fails."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ⚠", "S E T U P · 卡住怎麼辦", accent=PINK)
    slide_title(s, "卡住了?5 個常見救援", y=0.95, size=32)
    slide_subtitle(s, "Setup 失敗 90% 是這 5 種,先看這頁再舉手", y=1.85)

    items = [
        ("①", "uv 未安裝",
         "curl -LsSf https://astral.sh/uv/install.sh | sh",
         PINK,   PINK_PASTEL),
        ("②", "API key 沒填",
         "nano .env → 填入 sk-ant-...(不要加引號)",
         ORANGE, ORANGE_PASTEL),
        ("③", "Port 3000 被佔",
         "lsof -i :3000 → kill -9 <PID>",
         VIOLET, VIOLET_PASTEL),
        ("④", "npm install 失敗",
         "cat /tmp/mini-npm.log → 多半是 --legacy-peer-deps",
         TEAL,   TEAL_PASTEL),
        ("⑤", "LLM 答錯",
         "1) Ctrl+C 重啟 server   2) 把 docstring 寫更具體",
         BLUE,   BLUE_PASTEL),
    ]
    row_h = 0.72
    row_gap = 0.10
    for i, (num, title, fix, accent, fill) in enumerate(items):
        y = 2.55 + i * (row_h + row_gap)
        _rounded(s, 0.85, y, 12.1, row_h, fill, line_color=accent, line_w=2)
        _text(s, 1.0, y, 0.6, row_h, num,
              font=FONT_TITLE, size=22, color=accent, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 1.7, y, 3.5, row_h, title,
              font=FONT_TITLE, size=15, color=INK, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 5.3, y, 7.7, row_h, fix,
              font=FONT_CODE, size=12, color=INK_SOFT,
              anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.85, 12, 0.45,
                "完整故障排除見 04-live-demo-script.md(講師手冊)",
                accent=MUTED, fill=SLATE_PASTEL, icon="i", size=12)
    page_number(s, 8, TOTAL)


def build_llm_routes(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ②", "L L M   R O U T E   ·   1   L I N E   T O   S W I T C H",
                 accent=TEAL)
    slide_title(s, "選你的 LLM 路線", y=0.95)
    slide_subtitle(s, ".env 一行切換 —— 因為 MCP 工具兩家都認", y=1.85)

    pastel_card(s, 0.85, 2.7, 5.95, 3.7, accent=ORANGE, fill=ORANGE_PASTEL,
                title="☁  雲端 · Anthropic Claude")
    code_block(s, 1.0, 3.3, 5.65, 2.9, [
        ("# .env",                                CODE_COMMENT),
        ("LLM_PROVIDER=anthropic",                CODE_ORANGE),
        ("ANTHROPIC_API_KEY=sk-ant-...",          CODE_FG),
        ("ANTHROPIC_MODEL=claude-haiku-4-5",      CODE_FG),
        ("",                                      CODE_FG),
        ("# 優點",                                CODE_COMMENT),
        ("# • 工具呼叫品質最佳",                  CODE_COMMENT),
        ("# • 啟動快,$5 試用額",                 CODE_COMMENT),
    ], size=11)

    pastel_card(s, 7.05, 2.7, 5.85, 3.7, accent=TEAL, fill=TEAL_PASTEL,
                title="🏠  本地 · NCHU vLLM (Gemma 4)")
    code_block(s, 7.2, 3.3, 5.55, 2.9, [
        ("# .env",                                 CODE_COMMENT),
        ("LLM_PROVIDER=openai",                    CODE_ORANGE),
        ("OPENAI_BASE_URL=http://<ws>:8000/v1",    CODE_FG),
        ("OPENAI_API_KEY=dummy",                   CODE_FG),
        ("OPENAI_MODEL=gemma-4",                   CODE_FG),
        ("",                                       CODE_FG),
        ("# 優點",                                 CODE_COMMENT),
        ("# • 0 美金,無 token 限制",              CODE_COMMENT),
    ], size=11)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "💎  N+M 的甜蜜:你的工具一支不變,adapter 差別只在 mcp-client.js 幾行",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="", size=13)
    page_number(s, 9, TOTAL)


def build_l1_overview(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03", "L A B   1   ·   換   J S O N", accent=PINK)
    slide_title(s, "Lab 1 — 換 JSON 做你領域的助理", y=0.95)
    slide_subtitle(s, "0 行 Python · 40 分鐘 · 現場必做", y=1.85)

    steps = [
        ("①", "觀察",       "看 [tool_use] log\nAI 摘要 JSON",        "5 min",   VIOLET, VIOLET_PASTEL),
        ("②", "換資料",     "編輯 data/*.json\n放你的領域內容",      "15 min",  ORANGE, ORANGE_PASTEL),
        ("③", "改說明書",   "docstring 的使用情境\n決定工具呼叫率",  "10 min",  TEAL,   TEAL_PASTEL),
        ("④", "驗證",       "重啟 npm start\n問自己資料問題",         "5 min",   PINK,   PINK_PASTEL),
    ]
    card_w = 2.95
    for i, (num, title, body, dur, accent, fill) in enumerate(steps):
        x = 0.85 + i * (card_w + 0.20)
        _rounded(s, x, 2.85, card_w, 3.5, fill, line_color=accent, line_w=2)
        circle_number(s, x + 0.5, 3.25, num, accent, r=0.32)
        _text(s, x + 0.25, 3.95, card_w - 0.5, 0.55, title,
              font=FONT_TITLE, size=18, color=INK, bold=True)
        _multi(s, x + 0.25, 4.6, card_w - 0.5, 1.4,
               [{"text": line, "font": FONT_BODY, "size": 13,
                 "color": INK_SOFT, "space_after": 4}
                for line in body.split("\n")])
        _text(s, x + 0.25, 5.95, card_w - 0.5, 0.4, dur,
              font=FONT_CODE, size=14, color=accent, bold=True, italic=True)

    callout_box(s, 0.85, 6.5, 12, 0.5,
                "產出:你的 AI 助理會回答你自己放進去的資料 — 不是英文中心 demo 了",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 10, TOTAL)


def build_l1_step12(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ①②", "L A B   1   ·   S T E P S   1 - 2", accent=PINK)
    slide_title(s, "Step 1–2:觀察 → 換 JSON", y=0.95)
    slide_subtitle(s, "還沒動到 Python 一個字", y=1.85)

    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=VIOLET, fill=VIOLET_PASTEL,
                title="Step 1  觀察 (5 min)")
    _multi(s, 1.1, 3.3, 5.5, 3.3, [
        {"text": "在瀏覽器問:",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 4},
        {"text": "「英文中心幾點開門?」",
         "font": FONT_BODY, "size": 15, "color": VIOLET_DEEP, "bold": True,
         "space_after": 12},
        {"text": "在 terminal 觀察:",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 4},
        {"text": "[tool_use] get_english_center_info",
         "font": FONT_CODE, "size": 12, "color": ORANGE, "bold": True,
         "space_after": 14},
        {"text": "💡  關鍵觀察:",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True,
         "space_after": 4},
        {"text": "Claude 不會 dump 整份 JSON,挑出「開放時間」那一段。這是 LLM 對 tool result 的摘要 — agent 的靈魂。",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "italic": True,
         "space_after": 0},
    ])

    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=ORANGE, fill=ORANGE_PASTEL,
                title="Step 2  換 JSON (15 min)")
    _multi(s, 7.3, 3.3, 5.4, 3.3, [
        {"text": "編輯:",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 2},
        {"text": "mcp-server-py/data/english_center.json",
         "font": FONT_CODE, "size": 12, "color": ORANGE, "bold": True,
         "space_after": 12},
        {"text": "換成你自己的領域資料:",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True,
         "space_after": 4},
        {"text": "• 你的研究室介紹",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 2},
        {"text": "• 你教的一門課(大綱/作業/評分)",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 2},
        {"text": "• 你系所的 FAQ / 研究成果清單",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 12},
        {"text": "⚠ JSON 語法錯會卡住:",
         "font": FONT_BODY, "size": 12, "color": PINK_DEEP, "bold": True,
         "space_after": 2},
        {"text": "python3 -m json.tool data/xxx.json",
         "font": FONT_CODE, "size": 11, "color": PINK_DEEP, "space_after": 0},
    ])
    page_number(s, 11, TOTAL)


def build_l1_step3(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ③", "L A B   1   ·   S T E P   3   ·   D O C S T R I N G",
                 accent=PINK)
    slide_title(s, "Step 3:改 docstring (10 min)", y=0.95, size=30)
    slide_subtitle(s, "直接拿 repo 兩支真實工具對照 —— 同樣語法、教 LLM 不同事", y=1.85)

    # Left: minimal
    pastel_card(s, 0.85, 2.7, 5.95, 3.6, accent=ORANGE, fill=ORANGE_PASTEL,
                title="📝  minimal — hello_tool.py")
    code_block(s, 1.05, 3.3, 5.55, 2.9, [
        ("@mcp.tool()",                                  CODE_ORANGE),
        ("def get_english_center_info() -> str:",       CODE_FG),
        ('    """取得中興大學英語自學暨',                 CODE_STRING),
        ('    檢定中心的完整資訊。',                       CODE_STRING),
        ('',                                              CODE_FG),
        ('    回傳 JSON 字串,包含:',                    CODE_STRING),
        ('    名稱、開放時間、地點、設備…',                CODE_STRING),
        ('    使用情境:使用者詢問英語',                  CODE_STRING),
        ('    自學中心相關問題時呼叫。',                  CODE_STRING),
        ('    """',                                       CODE_STRING),
    ], size=10)

    # Right: rich
    pastel_card(s, 7.05, 2.7, 5.85, 3.6, accent=TEAL, fill=TEAL_PASTEL,
                title="📖  rich — teachers_tool.py")
    code_block(s, 7.2, 3.3, 5.55, 2.9, [
        ("@mcp.tool()",                                  CODE_ORANGE),
        ("def get_teacher_detail(name: str) -> str:",   CODE_FG),
        ('    """取得指定教授的完整資訊',                 CODE_STRING),
        ('    (email、辦公室、研究領域)。',              CODE_STRING),
        ('    使用情境:使用者問某位教授',                CODE_STRING),
        ('    的聯絡方式或完整資料時呼叫。',              CODE_STRING),
        ('    通常在 search_teachers 找到',              CODE_STRING),
        ('    候選名單後再呼叫。 ← 跨工具線索',          CODE_ORANGE),
        ('    Args:',                                    CODE_FG),
        ('        name: 教授姓名(完整中文)。',          CODE_STRING),
    ], size=10)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "影響 LLM 行為的 3 元素:使用情境(該不該叫) / Args 描述(怎麼填) / 跨工具線索(呼叫順序)",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 12, TOTAL)


def build_l2_l3_preview(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "★", "L 2 / L 3   P R E V I E W", accent=VIOLET)
    slide_title(s, "L2 / L3 — 帶回去繼續深入", y=0.95)
    slide_subtitle(s, "課後自修,參考 mini-project/docs/labs/", y=1.85)

    items = [
        ("L1", "換 JSON 做你領域的助理", "課堂現場必做\n0 行 Python", "完成", TEAL, TEAL_PASTEL),
        ("L2", "加一支有參數的搜尋工具",  "課後自修\n寫一個 @mcp.tool()",  "+1 hr", ORANGE, ORANGE_PASTEL),
        ("L3", "呼叫外部 API",            "課後自修\n串 arxiv/weather API", "+2 hr", PINK,   PINK_PASTEL),
    ]
    card_w = 3.95
    for i, (lab, title, body, badge, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 3.7, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.85, 1.0, 0.5, lab,
              font=FONT_TITLE, size=24, color=accent, bold=True)
        _rounded(s, x + card_w - 0.95, 2.95, 0.75, 0.4, BG_WHITE,
                 line_color=accent, line_w=1.5)
        _text(s, x + card_w - 0.95, 2.95, 0.75, 0.4, badge,
              font=FONT_CODE, size=10, color=accent, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, x + 0.25, 3.55, card_w - 0.5, 0.6, title,
              font=FONT_TITLE, size=15, color=INK, bold=True)
        _multi(s, x + 0.25, 4.3, card_w - 0.5, 2.0,
               [{"text": line, "font": FONT_BODY, "size": 14,
                 "color": INK_SOFT, "space_after": 6}
                for line in body.split("\n")])

    callout_box(s, 0.85, 6.5, 12, 0.5,
                "三關手冊:mini-project/docs/labs/L1-customize-your-data.md / L2 / L3",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 13, TOTAL)


def main():
    prs = make_presentation()
    build_cover(prs)            # 1
    build_outcomes(prs)         # 2
    build_schedule(prs)         # 3
    build_architecture(prs)     # 4
    build_agent_loop_code(prs)  # 5
    build_setup_steps(prs)      # 6
    build_quick_start(prs)      # 7
    build_troubleshooting(prs)  # 8 (NEW: 卡住怎麼辦 5 個救援)
    build_llm_routes(prs)       # 9
    build_l1_overview(prs)      # 10
    build_l1_step12(prs)        # 11
    build_l1_step3(prs)         # 12
    build_l2_l3_preview(prs)    # 13
    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
