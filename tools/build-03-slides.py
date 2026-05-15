#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 03-agentic-tool-loop.pptx in the new visual style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "03-agentic-tool-loop.pptx"

TOTAL = 16


def build_cover(prs):
    s = _blank_slide(prs, BG_WHITE)
    _rect(s, 0.85, 0.55, 0.55, 0.07, VIOLET)
    _text(s, 0.85, 0.75, 12, 0.4, "MCP 入門工作坊  ·  第三講",
          font=FONT_BODY, size=15, color=MUTED, bold=True)
    _text(s, 0.85, 2.0, 12, 1.6, "Agentic Tool Loop",
          font=FONT_TITLE, size=72, color=INK, bold=True)
    _text(s, 0.85, 3.5, 12, 0.7,
          "LLM 如何自主決策、呼叫工具、迭代推理",
          font=FONT_BODY, size=26, color=VIOLET, bold=True)
    _text(s, 0.85, 6.3, 8, 0.4,
          "范耀中  Yao-Chung Fan",
          font=FONT_BODY, size=18, color=INK, bold=True)
    _text(s, 0.85, 6.75, 8, 0.4,
          "國立中興大學  ·  AI 學伴系統實務案例",
          font=FONT_BODY, size=14, color=MUTED)
    pastel_card(s, 8.8, 6.0, 4.3, 1.1, accent=VIOLET, fill=VIOLET_PASTEL)
    _text(s, 8.95, 6.05, 4.0, 0.5, "從一次回答 → 多輪迭代",
          font=FONT_TITLE, size=16, color=VIOLET_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 8.95, 6.5, 4.0, 0.5,
          "LLM 不只回答,還會自己選工具",
          font=FONT_BODY, size=13, color=INK, align=PP_ALIGN.CENTER)


def build_agenda(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "00", "A G E N D A", accent=VIOLET)
    slide_title(s, "本講四個段落", y=0.95, size=40)
    slide_subtitle(s, "Agentic 觀念 → 訊息機制 → 控制迴圈 → Live Demo", y=1.95)

    items = [
        ("①", "什麼是 Agentic Loop", "傳統 LLM vs 自主代理",         ORANGE, ORANGE_PASTEL),
        ("②", "tool_use / result",   "Claude API 訊息格式",            VIOLET, VIOLET_PASTEL),
        ("③", "迭代控制機制",         "maxIterations · 強制回覆\n· Metadata 追蹤",     TEAL,   TEAL_PASTEL),
        ("④", "Live Demo",           "Running Example 逐步解說",       PINK,   PINK_PASTEL),
    ]
    card_w, card_h = 2.95, 3.5
    for i, (num, title, body, accent, fill) in enumerate(items):
        x = 0.85 + i * (card_w + 0.20)
        _rounded(s, x, 2.85, card_w, card_h, fill, line_color=accent, line_w=2)
        circle_number(s, x + 0.5, 3.25, num, accent, r=0.32)
        _text(s, x + 0.25, 3.95, card_w - 0.5, 0.85, title,
              font=FONT_TITLE, size=18, color=INK, bold=True)
        _multi(s, x + 0.25, 4.85, card_w - 0.5, 1.5,
               [{"text": line, "font": FONT_BODY, "size": 14,
                 "color": INK_SOFT, "space_after": 3}
                for line in body.split("\n")])
    page_number(s, 2, TOTAL)


def build_traditional_vs_agentic(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01", "A G E N T I C   L O O P   ·   觀 念", accent=ORANGE)
    slide_title(s, "傳統 LLM vs Agentic LLM", y=0.95)
    slide_subtitle(s, "從「單輪問答」到「多輪迭代」", y=1.85)

    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=MUTED, fill=SLATE_PASTEL,
                title="傳統 LLM — 單輪問答")
    _multi(s, 1.1, 3.4, 5.5, 3.2, [
        {"text": "使用者  →  提問",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 6},
        {"text": "LLM     →  回答(僅根據訓練資料)",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 6},
        {"text": "結束",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 18},
        {"text": "✗  無法存取外部資料",
         "font": FONT_BODY, "size": 13, "color": PINK_DEEP, "space_after": 4},
        {"text": "✗  無法執行動作",
         "font": FONT_BODY, "size": 13, "color": PINK_DEEP, "space_after": 4},
        {"text": "✗  一次互動就結束",
         "font": FONT_BODY, "size": 13, "color": PINK_DEEP, "space_after": 0},
    ])

    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=VIOLET, fill=VIOLET_PASTEL,
                title="Agentic LLM — 多輪迭代")
    _multi(s, 7.3, 3.4, 5.4, 3.2, [
        {"text": "使用者  →  提問",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 4},
        {"text": "LLM     →  分析 → 選工具 → 呼叫",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 4},
        {"text": "工具    →  回傳結果",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 4},
        {"text": "LLM     →  再分析 → 可能再呼叫…",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 4},
        {"text": "LLM     →  整合回覆",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 12},
        {"text": "✓  自主決策、多輪迭代",
         "font": FONT_BODY, "size": 13, "color": TEAL_DEEP, "space_after": 4},
        {"text": "✓  存取外部系統、執行動作",
         "font": FONT_BODY, "size": 13, "color": TEAL_DEEP, "space_after": 0},
    ])
    page_number(s, 3, TOTAL)


def build_loop_diagram(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ①", "A G E N T I C   L O O P   ·   概 念 圖", accent=ORANGE)
    slide_title(s, "Agentic Tool Loop 概念圖", y=0.95)
    slide_subtitle(s, "每一輪稱為一個 iteration,最多 maxIterations(預設 7)輪", y=1.85)

    nodes = [
        ("User\nQuery",     VIOLET),
        ("Build\nMessages", VIOLET),
        ("Call\nLLM API",   ORANGE),
        ("Check\nstop_reason", ORANGE),
        ("Execute\nMCP Tools", TEAL),
    ]
    card_w = 2.30
    gap = 0.05
    for i, (txt, color) in enumerate(nodes):
        x = 0.55 + i * (card_w + gap)
        fill = pastel_for(color)
        _rounded(s, x, 2.85, card_w, 1.1, fill, line_color=color, line_w=2)
        _text(s, x, 2.85, card_w, 1.1, txt,
              font=FONT_BODY, size=13, color=color, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(nodes) - 1:
            _text(s, x + card_w, 2.85, gap + 0.2, 1.1, "→",
                  font=FONT_TITLE, size=18, color=MUTED, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Return arrow + label
    _text(s, 0.85, 4.2, 12, 0.5, "↑   追加 tool_result 到 messages,回到 LLM",
          font=FONT_BODY, size=14, color=TEAL_DEEP, italic=True, bold=True,
          align=PP_ALIGN.CENTER)

    # stop_reason explanation
    pastel_card(s, 0.85, 4.95, 5.95, 1.85, accent=ORANGE, fill=ORANGE_PASTEL,
                title='stop_reason = "tool_use"')
    _text(s, 1.1, 5.55, 5.5, 1.15,
          "→  執行工具 → 追加 tool_result → 進入下一輪",
          font=FONT_BODY, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    pastel_card(s, 7.05, 4.95, 5.85, 1.85, accent=TEAL, fill=TEAL_PASTEL,
                title='stop_reason = "end_turn"')
    _text(s, 7.3, 5.55, 5.4, 1.15,
          "→  跳出迴圈,把最終文字回給使用者",
          font=FONT_BODY, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    page_number(s, 4, TOTAL)


def build_stop_reasons(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02", "S T O P   R E A S O N", accent=VIOLET)
    slide_title(s, "stop_reason — 迴圈的關鍵判斷", y=0.95)
    slide_subtitle(s, "Claude API 用這個欄位告訴 client 接下來該怎麼做", y=1.85)

    items = [
        ('"end_turn"',   "模型認為已可回覆",  "結束迴圈,回傳最終回覆給使用者", TEAL,   TEAL_PASTEL),
        ('"tool_use"',   "模型需要呼叫工具",  "執行工具 → 追加結果 → 進入下一輪", ORANGE, ORANGE_PASTEL),
        ('"max_tokens"', "回覆被截斷",       "視為完成或觸發錯誤處理", PINK,   PINK_PASTEL),
    ]
    card_w = 3.95
    for i, (name, desc, action, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 3.5, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.9, card_w - 0.5, 0.5, name,
              font=FONT_CODE, size=20, color=accent, bold=True)
        _text(s, x + 0.25, 3.7, card_w - 0.5, 0.6, desc,
              font=FONT_BODY, size=14, color=INK, bold=True)
        _text(s, x + 0.25, 4.5, card_w - 0.5, 1.5, action,
              font=FONT_BODY, size=14, color=INK_SOFT)

    _rounded(s, 0.85, 6.4, 12, 0.55, CODE_BG)
    _text(s, 1.1, 6.4, 11.5, 0.55,
          'while (stop_reason === "tool_use" && iteration < maxIterations) { … }',
          font=FONT_CODE, size=15, color=CODE_FG, bold=True,
          anchor=MSO_ANCHOR.MIDDLE)
    page_number(s, 5, TOTAL)


def build_tool_use_block(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ①", "T O O L _ U S E   B L O C K", accent=VIOLET)
    slide_title(s, "tool_use — LLM 的工具呼叫指令", y=0.95)
    slide_subtitle(s, "當 LLM 決定呼叫工具時,response.content 會含 tool_use block", y=1.85)

    code_lines = [
        ("// Claude API response.content 陣列中的一個 block", CODE_COMMENT),
        ("{",                                                  CODE_FG),
        ('  "type": "tool_use",',                              CODE_ORANGE),
        ('  "id": "toolu_01A09q90qw90lq917835lq9",',           CODE_FG),
        ('  "name": "search_library_books",  // MCP 工具名稱',  CODE_STRING),
        ('  "input": {                       // LLM 自動產生',  CODE_FG),
        ('    "keyword": "人工智慧",',                         CODE_STRING),
        ('    "limit": 10',                                    CODE_FG),
        ('  }',                                                CODE_FG),
        ("}",                                                  CODE_FG),
    ]
    code_block(s, 0.85, 2.5, 7.0, 3.5, code_lines, size=11)

    pastel_card(s, 8.1, 2.5, 4.8, 1.45, accent=ORANGE, fill=ORANGE_PASTEL,
                title="id", title_size=18)
    _text(s, 8.35, 3.0, 4.4, 0.95,
          "唯一識別碼,後續 tool_result 必須對應同一個 id",
          font=FONT_BODY, size=12, color=INK)

    pastel_card(s, 8.1, 4.1, 4.8, 1.45, accent=VIOLET, fill=VIOLET_PASTEL,
                title="name", title_size=18)
    _text(s, 8.35, 4.6, 4.4, 0.95,
          "對應 MCP Server 註冊的工具名稱",
          font=FONT_BODY, size=12, color=INK)

    pastel_card(s, 8.1, 5.7, 4.8, 1.45, accent=TEAL, fill=TEAL_PASTEL,
                title="input", title_size=18)
    _text(s, 8.35, 6.2, 4.4, 0.95,
          "LLM 根據 JSON Schema 自動生成的參數",
          font=FONT_BODY, size=12, color=INK)
    page_number(s, 6, TOTAL)


def build_tool_result(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ②", "T O O L _ R E S U L T", accent=VIOLET)
    slide_title(s, "tool_result — 工具執行結果回傳", y=0.95)
    slide_subtitle(s, "Client 執行 MCP 工具後,將結果以 user 角色追加到 messages", y=1.85)

    code_lines = [
        ("// 追加到 messages 陣列(role: user)",                CODE_COMMENT),
        ("{",                                                   CODE_FG),
        ('  "role": "user",                  ← 注意 role',     CODE_ORANGE),
        ('  "content": [{',                                     CODE_FG),
        ('    "type": "tool_result",',                          CODE_FG),
        ('    "tool_use_id": "toolu_01A09q...",  ← 同 id',     CODE_ORANGE),
        ('    "content": [{',                                   CODE_FG),
        ('      "type": "text",',                               CODE_FG),
        ('      "text": "[{\\"title\\":\\"深度學習入門\\"},…]"', CODE_STRING),
        ('    }],',                                             CODE_FG),
        ('    "is_error": false',                               CODE_FG),
        ('  }]',                                                CODE_FG),
        ("}",                                                   CODE_FG),
    ]
    code_block(s, 0.85, 2.5, 7.5, 3.7, code_lines, size=11)

    pastel_card(s, 8.6, 2.5, 4.3, 1.4, accent=ORANGE, fill=ORANGE_PASTEL,
                title="tool_use_id", title_size=16)
    _text(s, 8.85, 3.0, 4.0, 0.85,
          "必須與 tool_use 的 id 一致",
          font=FONT_BODY, size=12, color=INK)

    pastel_card(s, 8.6, 4.05, 4.3, 1.4, accent=TEAL, fill=TEAL_PASTEL,
                title="content", title_size=16)
    _text(s, 8.85, 4.55, 4.0, 0.85,
          "MCP 工具的實際回傳值(JSON 序列化為 text)",
          font=FONT_BODY, size=12, color=INK)

    pastel_card(s, 8.6, 5.6, 4.3, 1.4, accent=PINK, fill=PINK_PASTEL,
                title="is_error", title_size=16)
    _text(s, 8.85, 6.1, 4.0, 0.85,
          "true 時 LLM 會嘗試錯誤處理或換工具",
          font=FONT_BODY, size=12, color=INK)
    page_number(s, 7, TOTAL)


def build_messages_growth(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ③", "M E S S A G E S   G R O W T H", accent=VIOLET)
    slide_title(s, "Messages 陣列的成長過程", y=0.95)
    slide_subtitle(s, "每一輪迭代都追加 assistant + user(tool_result) —— 陣列持續增長", y=1.85)

    items = [
        ("system",    "System Prompt(角色設定 + 注入資訊)",                    BLUE),
        ("user",      "中興大學圖書館有什麼新書?",                              VIOLET),
        ("assistant", "我需要查詢…  + tool_use: search_new_books",              ORANGE),
        ("user",      "tool_result: [{\"title\":\"深度學習入門\",…}]",           TEAL),
        ("assistant", "以下是圖書館最新書籍:1.《深度學習入門》…",                 ORANGE),
    ]
    rh = 0.55
    y0 = 2.7
    for i, (role, txt, accent) in enumerate(items):
        y = y0 + i * (rh + 0.15)
        # Role pill
        _rounded(s, 0.85, y, 1.8, rh, accent, line_color=accent, line_w=0)
        _text(s, 0.85, y, 1.8, rh, role,
              font=FONT_CODE, size=14, color=BG_WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Text
        _text(s, 2.85, y, 10, rh, txt,
              font=FONT_BODY, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        # Iteration labels
        if i == 2:
            _text(s, 11.6, y + 0.3, 1.3, 0.4, "第 1 輪",
                  font=FONT_BODY, size=12, color=ORANGE, italic=True, bold=True)
        if i == 4:
            _text(s, 11.6, y + 0.3, 1.3, 0.4, "第 2 輪",
                  font=FONT_BODY, size=12, color=ORANGE, italic=True, bold=True)
    page_number(s, 8, TOTAL)


def build_parallel_tools(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ④", "P A R A L L E L   T O O L   C A L L S", accent=VIOLET)
    slide_title(s, "一輪中呼叫多個工具", y=0.95)
    slide_subtitle(s, "response.content 可以同時包含多個 tool_use block —— 平行執行", y=1.85)

    code_lines = [
        ("response.content = [",                                  CODE_FG),
        ('  { type: "text",',                                     CODE_FG),
        ('    text: "讓我同時查詢課程和圖書資訊..." },',          CODE_STRING),
        ('  { type: "tool_use", name: "search_courses",',         CODE_ORANGE),
        ('    id: "toolu_001", input: { keyword: "AI" } },',      CODE_FG),
        ('  { type: "tool_use", name: "search_library_books",',   CODE_ORANGE),
        ('    id: "toolu_002", input: { keyword: "AI" } }',       CODE_FG),
        ("]",                                                     CODE_FG),
        ("",                                                      CODE_FG),
        ("// Client 端收集所有 tool_use",                          CODE_COMMENT),
        ("const toolCalls = response.content",                    CODE_FG),
        ('  .filter(c => c.type === "tool_use");',                CODE_FG),
        ("// → 依序執行每個工具,收集結果",                       CODE_COMMENT),
    ]
    code_block(s, 0.85, 2.5, 12, 3.7, code_lines, size=11)

    callout_box(s, 0.85, 6.35, 12, 0.65,
                "興大 AI 學伴:「幫我查 AI 課程和相關書籍」→ 一輪同時呼叫 search_courses + search_library_books",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 9, TOTAL)


def build_core_loop_code(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03", "C O R E   L O O P", accent=TEAL)
    slide_title(s, "chatWithStreaming() —— 核心迴圈", y=0.95)
    slide_subtitle(s, "整個 agent 行為就是這 ~15 行 — while loop 加上 stop 條件", y=1.85)

    code_lines = [
        ("async chatWithStreaming(messages, options) {",                 CODE_FG),
        ("  const maxIterations = options.maxIterations || 7;",          CODE_FG),
        ("  let iteration = 0;",                                         CODE_FG),
        ("  while (iteration < maxIterations) {",                        CODE_ORANGE),
        ("    iteration++;",                                             CODE_FG),
        ("    // 最後一輪? 注入強制回覆提示",                            CODE_COMMENT),
        ("    if (iteration === maxIterations) {",                       CODE_FG),
        ('      messages.push({ role: "user",',                          CODE_FG),
        ('        content: "這是最後一輪,請直接回覆..." });',           CODE_STRING),
        ("    }",                                                        CODE_FG),
        ("    response = await callLLM(messages, tools);",               CODE_FG),
        ('    toolCalls = response.content.filter(c=>c.type==="tool_use");', CODE_FG),
        ("    if (toolCalls.length === 0) break;  // end_turn → 結束",   CODE_ORANGE),
        ("    results = await executeTools(toolCalls);",                 CODE_FG),
        ("    messages.push(assistantMsg, toolResultMsg);",              CODE_FG),
        ("  }",                                                          CODE_FG),
        ("}",                                                            CODE_FG),
    ]
    code_block(s, 0.85, 2.5, 12, 4.3, code_lines, size=11)
    page_number(s, 10, TOTAL)


def build_max_iter(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ①", "M A X _ I T E R A T I O N S   ·   強 制 回 覆", accent=TEAL)
    slide_title(s, "maxIterations 與強制回覆機制", y=0.95)
    slide_subtitle(s, "避免 LLM 無限呼叫工具 —— 設上限 + 最後一輪強制總結", y=1.85)

    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=PINK, fill=PINK_PASTEL,
                title="問題:無限迴圈風險")
    _multi(s, 1.1, 3.3, 5.5, 3.3, [
        {"text": "LLM 可能不斷呼叫工具而永遠不回覆使用者,造成:",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 10},
        {"text": "✗  Token 成本無限增長",
         "font": FONT_BODY, "size": 14, "color": PINK_DEEP, "space_after": 6},
        {"text": "✗  回應時間過長",
         "font": FONT_BODY, "size": 14, "color": PINK_DEEP, "space_after": 6},
        {"text": "✗  使用者體驗極差",
         "font": FONT_BODY, "size": 14, "color": PINK_DEEP, "space_after": 0},
    ])

    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=TEAL, fill=TEAL_PASTEL,
                title="解法:maxIterations = 7")
    _multi(s, 7.3, 3.3, 5.4, 3.3, [
        {"text": "✓  設定最大迭代次數上限",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✓  第 7 輪(最後一輪)時注入臨時",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 2},
        {"text": "    user message 強制模型停止使用",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 2},
        {"text": "    工具,直接整理回覆",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 14},
        {"text": "「請不要再使用任何工具,",
         "font": FONT_CODE, "size": 12, "color": TEAL_DEEP, "bold": True,
         "italic": True, "space_after": 2},
        {"text": "  直接根據工具回傳的資料整理 Markdown 回覆。」",
         "font": FONT_CODE, "size": 12, "color": TEAL_DEEP, "bold": True,
         "italic": True, "space_after": 0},
    ])
    page_number(s, 11, TOTAL)


def build_metadata_tracking(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ②", "M E T A D A T A   T R A C K I N G", accent=TEAL)
    slide_title(s, "Metadata 追蹤 —— 不污染 Messages", y=0.95, size=32)
    slide_subtitle(s, "每輪的 stop_reason 與 token usage 用「平行陣列」記錄,結構分離", y=1.85)

    cols = ["messages[]", "messageStopReasons[]", "messageUsages[]"]
    cols_x = [0.85, 5.45, 9.65]
    cols_w = [4.4, 4.0, 3.25]
    cols_color = [VIOLET, ORANGE, TEAL]
    cols_fill = [VIOLET_PASTEL, ORANGE_PASTEL, TEAL_PASTEL]

    for i, name in enumerate(cols):
        _rect(s, cols_x[i], 2.65, cols_w[i], 0.45, cols_fill[i])
        _text(s, cols_x[i], 2.65, cols_w[i], 0.45, name,
              font=FONT_CODE, size=14, color=cols_color[i], bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    rows = [
        ("assistant (tool_use)",   "tool_use",     "{ in: 850, out: 120 }"),
        ("user (tool_result)",     "null",         "null"),
        ("assistant (end_turn)",   "end_turn",     "{ in: 1200, out: 350 }"),
    ]
    rh = 0.7
    for ri, row in enumerate(rows):
        y = 3.15 + ri * (rh + 0.10)
        for i, cell in enumerate(row):
            _rounded(s, cols_x[i], y, cols_w[i], rh, BG_WHITE,
                     line_color=cols_color[i], line_w=1.5)
            _text(s, cols_x[i] + 0.1, y, cols_w[i] - 0.2, rh, cell,
                  font=FONT_CODE, size=12, color=INK,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.35, 12, 0.55,
                "索引對齊、結構分離 — 乾淨且不影響 API 呼叫格式",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=14)
    page_number(s, 12, TOTAL)


def build_sse_streaming(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ③", "S S E   S T R E A M I N G", accent=TEAL)
    slide_title(s, "SSE 串流 —— 即時回饋使用者", y=0.95)
    slide_subtitle(s, "整個 agentic loop 過程,透過 Server-Sent Events 逐步通知前端", y=1.85)

    events = [
        ("thinking_start",  "第 N 輪思考中…",                      "每輪開始",   VIOLET, VIOLET_PASTEL),
        ("tools_start",     "開始執行工具",                         "偵測 tool_use", ORANGE, ORANGE_PASTEL),
        ("tool_executing",  "正在執行 search_books…",               "每個工具",    PINK,   PINK_PASTEL),
        ("tool_completed",  "工具完成,取得結果",                    "工具完成",    TEAL,   TEAL_PASTEL),
        ("text_chunk",      "逐字回傳最終文字",                      "最後回覆",    BLUE,   BLUE_PASTEL),
        ("done",            "串流結束",                              "全部完成",    TEAL_DEEP, SLATE_PASTEL),
    ]
    card_w = 3.95
    for i, (event, desc, when, accent, fill) in enumerate(events):
        col = i % 3
        row = i // 3
        x = 0.55 + col * (card_w + 0.20)
        y = 2.7 + row * 1.7
        _rounded(s, x, y, card_w, 1.5, fill, line_color=accent, line_w=2)
        _text(s, x + 0.2, y + 0.10, card_w - 0.4, 0.45, event,
              font=FONT_CODE, size=14, color=accent, bold=True)
        _text(s, x + 0.2, y + 0.6, card_w - 0.4, 0.4, desc,
              font=FONT_BODY, size=12, color=INK)
        _text(s, x + 0.2, y + 1.05, card_w - 0.4, 0.4, when,
              font=FONT_BODY, size=11, color=MUTED, italic=True)
    page_number(s, 13, TOTAL)


def build_demo_cue(prs):
    s = _blank_slide(prs, MIDNIGHT)
    _text(s, 0.85, 1.5, 12, 0.8, "▶  切換到 Live Demo",
          font=FONT_TITLE, size=44, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 2.6, 12, 0.5,
          "sonnet-running-example.pptx",
          font=FONT_CODE, size=22, color=MUTED, align=PP_ALIGN.CENTER)

    pastel_card(s, 2.0, 3.6, 9.3, 3.0,
                accent=VIOLET, fill=RGBColor(0x1E, 0x20, 0x3A))
    _multi(s, 2.35, 3.85, 8.6, 2.6, [
        {"text": "展示重點",
         "font": FONT_TITLE, "size": 16, "color": VIOLET, "bold": True,
         "space_after": 8},
        {"text": "1.  使用者提問 → Controller → 建立 messages 陣列",
         "font": FONT_BODY, "size": 13, "color": CODE_FG, "space_after": 4},
        {"text": "2.  第 1 輪 — 送往 Sonnet → 回傳 tool_use block",
         "font": FONT_BODY, "size": 13, "color": CODE_FG, "space_after": 4},
        {"text": "3.  MCP 工具執行(auto-inject user_id)",
         "font": FONT_BODY, "size": 13, "color": CODE_FG, "space_after": 4},
        {"text": "4.  第 2 輪 — 帶結果回 Sonnet → end_turn",
         "font": FONT_BODY, "size": 13, "color": CODE_FG, "space_after": 4},
        {"text": "5.  SSE 串流回傳完整回覆",
         "font": FONT_BODY, "size": 13, "color": CODE_FG, "space_after": 0},
    ])
    page_number(s, 14, TOTAL)


def build_finale(prs):
    s = _blank_slide(prs, MIDNIGHT)
    _text(s, 0.85, 1.4, 12, 0.5, "—  一  句  話  總  結  —",
          font=FONT_BODY, size=14, color=MUTED, italic=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 2.6, 12, 1.2,
          "Agentic = stop_reason 驅動的 while 迴圈",
          font=FONT_TITLE, size=42, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 3.7, 12, 1.0,
          "—— 加上 maxIterations 安全閥 + 最後一輪強制回覆。",
          font=FONT_TITLE, size=26, color=VIOLET, bold=True,
          align=PP_ALIGN.CENTER)
    pastel_card(s, 2.0, 5.4, 9.3, 1.2,
                accent=VIOLET, fill=RGBColor(0x1E, 0x20, 0x3A))
    _multi(s, 2.3, 5.5, 8.8, 1.05, [
        {"text": "下一講:實務考量",
         "font": FONT_BODY, "size": 14, "color": MUTED, "space_after": 4},
        {"text": "「動手做 mini-project + 實務上的成本 / 模型 / 品質考量」",
         "font": FONT_BODY, "size": 14, "color": CODE_FG, "bold": True,
         "space_after": 0},
    ])
    page_number(s, 15, TOTAL)


def build_recap(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "★", "R E C A P", accent=VIOLET)
    slide_title(s, "本講回顧", y=0.95)
    slide_subtitle(s, "下一講預告:實務考量 —— 模型選擇、Haiku alignment、工具品質", y=1.85)

    points = [
        ("Agentic = 自主決策",
         "LLM 不只回答問題,還能判斷需要什麼資訊、主動呼叫工具取得"),
        ("tool_use / tool_result",
         "Claude API 的核心機制 — stop_reason 驅動整個迴圈"),
        ("maxIterations 安全閥",
         "預設 7 輪上限 + 最後一輪強制回覆,平衡能力與安全"),
        ("SSE 即時串流",
         "每個步驟(思考、執行工具、回覆)都即時通知前端"),
    ]
    y = 2.8
    for i, (title, body) in enumerate(points, 1):
        circle_number(s, 1.15, y + 0.4, str(i), VIOLET, r=0.28)
        _text(s, 1.7, y, 11.2, 0.4, title,
              font=FONT_TITLE, size=18, color=INK, bold=True)
        _text(s, 1.7, y + 0.4, 11.2, 0.5, body,
              font=FONT_BODY, size=14, color=INK_SOFT)
        y += 0.92
    page_number(s, 16, TOTAL)


def main():
    prs = make_presentation()
    build_cover(prs)                    # 1
    build_agenda(prs)                   # 2
    build_traditional_vs_agentic(prs)   # 3
    build_loop_diagram(prs)             # 4
    build_stop_reasons(prs)             # 5
    build_tool_use_block(prs)           # 6
    build_tool_result(prs)              # 7
    build_messages_growth(prs)          # 8
    build_parallel_tools(prs)           # 9
    build_core_loop_code(prs)           # 10
    build_max_iter(prs)                 # 11
    build_metadata_tracking(prs)        # 12
    build_sse_streaming(prs)            # 13
    build_demo_cue(prs)                 # 14
    build_finale(prs)                   # 15
    build_recap(prs)                    # 16
    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
