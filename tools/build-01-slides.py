#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 01-why-mcp.pptx in the new visual style (violet primary)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "01-why-mcp.pptx"

TOTAL = 21


def build_cover(prs):
    s = _blank_slide(prs, BG_WHITE)
    _rect(s, 0.85, 0.55, 0.55, 0.07, VIOLET)
    _text(s, 0.85, 0.75, 12, 0.4, "MCP 入門工作坊  ·  第一講",
          font=FONT_BODY, size=15, color=MUTED, bold=True)
    _text(s, 0.85, 2.0, 12, 1.6, "Why MCP",
          font=FONT_TITLE, size=88, color=INK, bold=True)
    _text(s, 0.85, 3.5, 12, 0.7,
          "從 LLM 的局限 到 Model Context Protocol",
          font=FONT_BODY, size=28, color=VIOLET, bold=True)
    _text(s, 0.85, 6.3, 8, 0.4,
          "范耀中  Yao-Chung Fan",
          font=FONT_BODY, size=18, color=INK, bold=True)
    _text(s, 0.85, 6.75, 8, 0.4,
          "國立中興大學  ·  AI 學伴系統實務案例",
          font=FONT_BODY, size=14, color=MUTED)

    pastel_card(s, 8.8, 6.0, 4.3, 1.1, accent=VIOLET, fill=VIOLET_PASTEL)
    _text(s, 8.95, 6.05, 4.0, 0.5, "為什麼需要 MCP?",
          font=FONT_TITLE, size=16, color=VIOLET_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 8.95, 6.5, 4.0, 0.5,
          "LLM 摸不到外部世界 — MCP 是橋",
          font=FONT_BODY, size=13, color=INK, align=PP_ALIGN.CENTER)


def build_agenda(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "00", "A G E N D A", accent=VIOLET)
    slide_title(s, "本講四個段落", y=0.95, size=40)
    slide_subtitle(s, "從 LLM 的局限 → 三種延伸策略 → MCP → 興大案例", y=1.95)

    items = [
        ("①", "LLM 能 / 不能做什麼", "理解大型語言模型的能力邊界",          ORANGE, ORANGE_PASTEL),
        ("②", "三種延伸策略",       "RAG / Tool Use / MCP 深入比較",      VIOLET, VIOLET_PASTEL),
        ("③", "MCP 核心概念",       "Host / Client / Server / Tool",     TEAL,   TEAL_PASTEL),
        ("④", "實際案例",           "興大 AI 學伴 33 個 MCP 工具",         PINK,   PINK_PASTEL),
    ]
    card_w, card_h = 2.95, 3.5
    gap = 0.20
    for i, (num, title, body, accent, fill) in enumerate(items):
        x = 0.85 + i * (card_w + gap)
        _rounded(s, x, 2.85, card_w, card_h, fill,
                 line_color=accent, line_w=2)
        circle_number(s, x + 0.5, 3.25, num, accent, r=0.32)
        _text(s, x + 0.25, 3.95, card_w - 0.5, 0.85, title,
              font=FONT_TITLE, size=18, color=INK, bold=True)
        _text(s, x + 0.25, 4.85, card_w - 0.5, 1.5, body,
              font=FONT_BODY, size=14, color=INK_SOFT)
    page_number(s, 2, TOTAL)


def build_llm_can(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ①", "L L M   能 做 什 麼", accent=ORANGE)
    slide_title(s, "LLM 擅長什麼?", y=0.95)
    slide_subtitle(s, "—— 訓練階段學到的「靜態知識」", y=1.95)

    items = [
        ("語言理解與生成", "翻譯、摘要、改寫、多語言對話",        VIOLET,  VIOLET_PASTEL),
        ("推理與分析",     "邏輯推導、比較分析、結構化輸出",      TEAL,    TEAL_PASTEL),
        ("程式碼生成",     "撰寫、除錯、解釋多種程式語言",        ORANGE,  ORANGE_PASTEL),
        ("知識回答",       "基於訓練資料的常識與專業知識",        PINK,    PINK_PASTEL),
    ]
    card_w, card_h = 2.95, 3.2
    for i, (title, body, accent, fill) in enumerate(items):
        x = 0.85 + i * (card_w + 0.20)
        _rounded(s, x, 2.85, card_w, card_h, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 3.1, card_w - 0.5, 0.65, title,
              font=FONT_TITLE, size=17, color=accent, bold=True)
        _text(s, x + 0.25, 3.85, card_w - 0.5, 2.5, body,
              font=FONT_BODY, size=15, color=INK)
    callout_box(s, 0.85, 6.4, 12, 0.55,
                "這些能力來自訓練階段學到的靜態知識 —— 用一次,模型不會更新",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=14)
    page_number(s, 3, TOTAL)


def build_llm_cannot(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ②", "L L M   不 能 做 什 麼", accent=ORANGE)
    slide_title(s, "LLM 的天花板", y=0.95, accent=PINK)
    slide_subtitle(s, "—— 訓練階段沒看過的、無法執行的事情", y=1.95)

    items = [
        ("知識截止日",   "訓練資料有日期上限\n無法回答「今天」的事"),
        ("沒有私有資料", "不知道你的課表、\n圖書館藏書、校內公告"),
        ("無法執行動作", "不能幫你查詢系統、\n預約空間、操作 API"),
        ("會幻覺",       "不確定時仍自信回答\n編造看起來合理的資訊"),
    ]
    for i, (title, body) in enumerate(items):
        x = 0.85 + i * 3.15
        _rounded(s, x, 2.85, 2.95, 3.2, PINK_PASTEL, line_color=PINK, line_w=2)
        _text(s, x + 0.25, 3.05, 2.7, 0.55, f"✗  {title}",
              font=FONT_TITLE, size=17, color=PINK_DEEP, bold=True)
        _multi(s, x + 0.25, 3.7, 2.7, 2.3,
               [{"text": line, "font": FONT_BODY, "size": 14,
                 "color": INK, "space_after": 3}
                for line in body.split("\n")])
    callout_box(s, 0.85, 6.4, 12, 0.55,
                "核心問題:如何讓 LLM 存取「外部世界」的資訊與功能?",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="?", size=14)
    page_number(s, 4, TOTAL)


def build_strategy_overview(prs):
    """Slide 5 — 三條策略 overview before diving into each in detail.
    Bridges from 'LLM 天花板' (slide 4) to '策略 A RAG' (slide 6).
    Audience gets a roadmap before the deep dive."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · 0", "S T R A T E G I E S · 三 條 路 概 覽", accent=VIOLET)
    slide_title(s, "三條打破天花板的路", y=0.95, size=36)
    slide_subtitle(s, "接下來逐條深入比較,最後看哪條最適合你的情境", y=1.85)

    items = [
        ("A", "RAG",          "檢索增強生成",
         "把私有文件\n檢索後塞進 prompt",
         "解知識截止 + 私有資料",
         BLUE, BLUE_PASTEL),
        ("B", "Tool Use",     "工具呼叫",
         "LLM 自己決定\n呼叫哪個 API/函式",
         "解執行動作 + 即時資料",
         ORANGE, ORANGE_PASTEL),
        ("C", "MCP",          "統一協定解耦",
         "工具獨立於 LLM,\n協定當橋",
         "解整合爆炸 + 跨應用重用",
         VIOLET, VIOLET_PASTEL),
    ]
    card_w = 3.95
    for i, (tag, name, sub, method, solves, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 4.0, fill, line_color=accent, line_w=2)
        # 策略 tag (大字 A/B/C)
        _text(s, x + 0.25, 2.85, 0.7, 0.55, tag,
              font=FONT_TITLE, size=32, color=accent, bold=True)
        # name
        _text(s, x + 1.1, 2.95, card_w - 1.3, 0.55, name,
              font=FONT_TITLE, size=22, color=INK, bold=True)
        # subtitle (中文小字)
        _text(s, x + 1.1, 3.55, card_w - 1.3, 0.4, sub,
              font=FONT_BODY, size=13, color=MUTED, italic=True)
        # method
        _text(s, x + 0.25, 4.20, card_w - 0.5, 1.2, method,
              font=FONT_BODY, size=14, color=INK)
        # solves (bottom strip)
        _rect(s, x + 0.25, 5.85, card_w - 0.5, 0.55, BG_WHITE,
              line_color=accent, line_w=1)
        _text(s, x + 0.25, 5.85, card_w - 0.5, 0.55, solves,
              font=FONT_BODY, size=13, color=accent, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.95, 12, 0.50,
                "三者不互斥 — MCP server 內部可以放 RAG 檢索 + Tool Use 函式",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=14)
    page_number(s, 5, TOTAL)


def build_rag(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · A", "S T R A T E G Y   ·   R A G", accent=VIOLET)
    slide_title(s, "策略 A:RAG (Retrieval-Augmented Generation)", y=0.95, size=28)
    slide_subtitle(s, "把外部文件「檢索 + 注入 prompt」交給 LLM", y=1.85)

    flow = ["使用者提問", "Embedding\n向量化", "向量資料庫\n相似度搜尋", "取回相關\n文件片段", "注入 Prompt\n+ LLM 回答"]
    card_w = 2.30
    gap = 0.05
    for i, txt in enumerate(flow):
        x = 0.55 + i * (card_w + gap)
        _rounded(s, x, 2.6, card_w, 1.0, VIOLET_PASTEL,
                 line_color=VIOLET, line_w=2)
        _text(s, x, 2.6, card_w, 1.0, txt,
              font=FONT_BODY, size=12, color=VIOLET_DEEP, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(flow) - 1:
            _text(s, x + card_w, 2.6, gap + 0.1, 1.0, "→",
                  font=FONT_TITLE, size=18, color=MUTED, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    pastel_card(s, 0.85, 4.0, 5.9, 2.7, accent=TEAL, fill=TEAL_PASTEL,
                title="優點")
    _multi(s, 1.1, 4.55, 5.5, 2.0, [
        {"text": "✓  降低幻覺 — 有引用來源",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✓  存取私有資料(文件、知識庫)",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✓  不需重新訓練模型",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 0},
    ])
    pastel_card(s, 7.05, 4.0, 5.85, 2.7, accent=PINK, fill=PINK_PASTEL,
                title="局限")
    _multi(s, 7.3, 4.55, 5.4, 2.0, [
        {"text": "✗  只能「讀」 — 無法執行動作",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✗  檢索品質依賴 embedding 與切塊",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✗  結構化查詢(如 SQL)支援差",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 0},
    ])
    page_number(s, 6, TOTAL)


def build_rag_code(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · A", "R A G   ·   C O D E", accent=VIOLET)
    slide_title(s, "RAG 概念程式碼", y=0.95)
    slide_subtitle(s, "三步驟:embed query → 向量檢索 → 拼到 prompt", y=1.85)

    code_lines = [
        ("# 1. 使用者提問",                                                   CODE_COMMENT),
        ('query = "中興大學圖書館有什麼 AI 相關的書？"',                       CODE_FG),
        ("",                                                                   CODE_FG),
        ("# 2. 轉成向量,在資料庫中搜尋最相似的文件片段",                     CODE_COMMENT),
        ("embedding = embed_model.encode(query)",                              CODE_FG),
        ("relevant_docs = vector_db.search(embedding, top_k=5)",               CODE_ORANGE),
        ("",                                                                   CODE_FG),
        ("# 3. 把搜尋結果塞進 prompt,交給 LLM",                              CODE_COMMENT),
        ('prompt = f"根據以下資料回答問題:\\n{relevant_docs}\\n\\n問題：{query}"', CODE_FG),
        ("response = llm.generate(prompt)",                                    CODE_FG),
    ]
    code_block(s, 0.85, 2.7, 12, 3.6, code_lines, size=13)
    page_number(s, 7, TOTAL)


def build_tooluse(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · B", "S T R A T E G Y   ·   T O O L   U S E", accent=ORANGE)
    slide_title(s, "策略 B:Tool Use (Function Calling)", y=0.95, size=32)
    slide_subtitle(s, "LLM 自己決定要不要呼叫工具、呼叫哪一個", y=1.85)

    flow = ["使用者\n提問", "LLM 分析\n選擇工具", "呼叫外部\nAPI / 函式", "取得執行\n結果", "LLM 整合\n回覆"]
    card_w = 2.30
    gap = 0.05
    for i, txt in enumerate(flow):
        x = 0.55 + i * (card_w + gap)
        _rounded(s, x, 2.6, card_w, 1.0, ORANGE_PASTEL,
                 line_color=ORANGE, line_w=2)
        _text(s, x, 2.6, card_w, 1.0, txt,
              font=FONT_BODY, size=12, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < len(flow) - 1:
            _text(s, x + card_w, 2.6, gap + 0.1, 1.0, "→",
                  font=FONT_TITLE, size=18, color=MUTED, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    pastel_card(s, 0.85, 4.0, 5.9, 2.7, accent=TEAL, fill=TEAL_PASTEL,
                title="優點")
    _multi(s, 1.1, 4.55, 5.5, 2.0, [
        {"text": "✓  能「做事」 — 查詢、計算、操作",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✓  結構化輸入輸出(JSON Schema)",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 0},
    ])
    pastel_card(s, 7.05, 4.0, 5.85, 2.7, accent=PINK, fill=PINK_PASTEL,
                title="局限")
    _multi(s, 7.3, 4.55, 5.4, 2.0, [
        {"text": "✗  每家 API 格式不同(vendor lock-in)",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✗  工具要寫死在應用程式裡",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 0},
    ])
    page_number(s, 8, TOTAL)


def build_fc_picture(prs):
    """Slide 8 — Function Calling 具體例子(一張圖看懂)。
    Bridge between abstract flow (slide 7) and Claude/ChatGPT code (slide 9).
    Listeners get a mental anchor for HOW function calling works without
    diving into API code yet."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · B*", "F U N C T I O N   C A L L I N G   ·   一 圖 看 懂",
                 accent=ORANGE)
    slide_title(s, "Function Calling 一張圖看懂", y=0.95, size=32)
    slide_subtitle(s, '具體例子:「今天台中天氣?」→ LLM 看菜單 → 自己選工具', y=1.85)

    # ── Top row: User question → LLM (sees menu) → Tools menu ──
    # User box (left)
    pastel_card(s, 0.85, 2.65, 3.5, 1.3, accent=BLUE, fill=BLUE_PASTEL,
                title="使用者")
    _text(s, 1.0, 3.15, 3.2, 0.55, '"今天台中天氣?"',
          font=FONT_BODY, size=16, color=INK, italic=True,
          anchor=MSO_ANCHOR.MIDDLE)

    # LLM box (center)
    _rounded(s, 5.4, 2.65, 2.4, 1.3, VIOLET_PASTEL,
             line_color=VIOLET, line_w=3, adj=0.18)
    _text(s, 5.4, 2.78, 2.4, 0.5, "LLM",
          font=FONT_TITLE, size=28, color=VIOLET_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 5.4, 3.30, 2.4, 0.4, "(Claude / GPT-4)",
          font=FONT_BODY, size=11, color=VIOLET,
          align=PP_ALIGN.CENTER)

    # Tools menu (right) — 3 tools, highlight weather as "LLM picks this"
    pastel_card(s, 8.85, 2.65, 4.05, 1.3, accent=ORANGE, fill=ORANGE_PASTEL,
                title="LLM 看到的工具菜單")
    _multi(s, 9.0, 3.20, 3.85, 0.65, [
        {"text": "▶  weather(city)         —  查天氣",
         "font": FONT_CODE, "size": 10, "color": ORANGE, "bold": True,
         "space_after": 1},
        {"text": "    search_books(kw)     —  搜館藏",
         "font": FONT_CODE, "size": 10, "color": MUTED, "space_after": 1},
        {"text": "    get_course_info(id)  —  查課程",
         "font": FONT_CODE, "size": 10, "color": MUTED, "space_after": 0},
    ])

    # Arrows between top row pieces
    _text(s, 4.35, 2.65, 1.05, 1.3, "→",
          font=FONT_TITLE, size=28, color=MUTED, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 7.8, 2.65, 1.05, 1.3, "↔",
          font=FONT_TITLE, size=22, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ── Middle: decision line ──
    _text(s, 0.85, 4.20, 12, 0.45,
          "→  LLM 自己選擇  weather(city='台中')  ←  沒有人寫 if-else",
          font=FONT_BODY, size=18, color=VIOLET_DEEP, bold=True,
          align=PP_ALIGN.CENTER)

    # ── Bottom row: 3 steps ──
    pastel_card(s, 0.85, 4.95, 4.0, 1.9, accent=ORANGE, fill=ORANGE_PASTEL,
                title="① 呼叫")
    _text(s, 1.0, 5.55, 3.7, 0.5, 'tool_use:',
          font=FONT_CODE, size=12, color=MUTED, bold=True,
          anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 1.0, 5.92, 3.7, 0.5, 'weather("台中")',
          font=FONT_CODE, size=15, color=ORANGE, bold=True,
          anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 1.0, 6.35, 3.7, 0.4, "LLM 吐出名稱 + 參數",
          font=FONT_BODY, size=11, color=INK_SOFT, italic=True,
          anchor=MSO_ANCHOR.MIDDLE)

    pastel_card(s, 5.0, 4.95, 4.0, 1.9, accent=TEAL, fill=TEAL_PASTEL,
                title="② 結果")
    _text(s, 5.15, 5.55, 3.7, 0.5, 'tool_result:',
          font=FONT_CODE, size=12, color=MUTED, bold=True,
          anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 5.15, 5.92, 3.7, 0.5, '{ temp: 25, sky: "多雲" }',
          font=FONT_CODE, size=12, color=TEAL_DEEP, bold=True,
          anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 5.15, 6.35, 3.7, 0.4, "外部 API 跑完,回 JSON",
          font=FONT_BODY, size=11, color=INK_SOFT, italic=True,
          anchor=MSO_ANCHOR.MIDDLE)

    pastel_card(s, 9.1, 4.95, 3.85, 1.9, accent=VIOLET, fill=VIOLET_PASTEL,
                title="③ 整合回覆")
    _text(s, 9.25, 5.65, 3.55, 0.55, '"今天台中 25°C,多雲"',
          font=FONT_BODY, size=13, color=VIOLET_DEEP, bold=True,
          italic=True, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 9.25, 6.35, 3.55, 0.4, "LLM 把 JSON 用人話翻譯",
          font=FONT_BODY, size=11, color=INK_SOFT, italic=True,
          anchor=MSO_ANCHOR.MIDDLE)

    # Arrows between bottom 3 cards
    _text(s, 4.82, 5.0, 0.25, 1.85, "→",
          font=FONT_TITLE, size=22, color=MUTED, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, 8.92, 5.0, 0.25, 1.85, "→",
          font=FONT_TITLE, size=22, color=MUTED, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.95, 12, 0.45,
                "Segment 02 會深入 tool_use / tool_result 的 JSON 結構;這頁先建立直覺",
                accent=MUTED, fill=SLATE_PASTEL, icon="i", size=12)
    page_number(s, 9, TOTAL)


def build_fc_code(prs):
    """Slide 10 — Function Calling 概念程式碼 (對位 rag_code 的角色).
    After fc_picture (一張圖看懂), give the audience concept-level code
    before showing Claude vs ChatGPT API vendor lock-in next."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · B", "F U N C T I O N   C A L L I N G · C O D E",
                 accent=ORANGE)
    slide_title(s, "Function Calling 概念程式碼", y=0.95)
    slide_subtitle(s, "四步驟:定義 tool → API call → 執行 → 結果送回 LLM", y=1.85)

    code_lines = [
        ("# 1. 定義工具給 LLM 看(schema)",                                  CODE_COMMENT),
        ("tools = [{",                                                          CODE_FG),
        ('  "name": "get_weather",',                                            CODE_STRING),
        ('  "description": "查詢某城市的當前天氣",',                            CODE_STRING),
        ('  "input_schema": {"type": "object",',                                CODE_FG),
        ('                   "properties": {"city": {"type": "string"}}}',      CODE_FG),
        ("}]",                                                                  CODE_FG),
        ("",                                                                    CODE_FG),
        ("# 2. 帶 tools 呼叫 Claude API",                                       CODE_COMMENT),
        ("response = anthropic.messages.create(",                               CODE_FG),
        ('    model="claude-sonnet-4", tools=tools,',                           CODE_ORANGE),
        ('    messages=[{"role": "user", "content": "今天台中天氣?"}])',        CODE_FG),
        ("",                                                                    CODE_FG),
        ("# 3. LLM 決定呼叫 tool → 你執行它",                                   CODE_COMMENT),
        ('if response.stop_reason == "tool_use":',                              CODE_FG),
        ("    tool_use = response.content[-1]   # {name, input, id}",           CODE_FG),
        ('    result = weather_api(tool_use.input["city"])  # 你寫的 function', CODE_ORANGE),
        ("",                                                                    CODE_FG),
        ("    # 4. 結果送回 LLM,讓它整合成自然語言",                            CODE_COMMENT),
        ("    final = anthropic.messages.create(messages=[...prev,",            CODE_FG),
        ('        {"role": "user", "content": [{"type": "tool_result",',       CODE_FG),
        ('         "tool_use_id": tool_use.id, "content": str(result)}]}])',   CODE_FG),
    ]
    code_block(s, 0.85, 2.45, 12, 4.55, code_lines, size=10)

    callout_box(s, 0.85, 7.1, 12, 0.40,
                "RAG 是「拼字串給 LLM」;Function Calling 是「LLM 選工具叫你執行」",
                accent=ORANGE, fill=ORANGE_PASTEL, icon="▶", size=13)
    page_number(s, 10, TOTAL)


def build_tooluse_code(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · B", "T O O L   U S E   ·   C L A U D E   v s   C H A T G P T",
                 accent=ORANGE)
    slide_title(s, "同一支工具,兩家 API 寫法不同", y=0.95, size=30)
    slide_subtitle(s, "—— 這就是「vendor lock-in」的具體例子", y=1.85)

    # Claude
    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=ORANGE, fill=ORANGE_PASTEL,
                title="Claude API")
    code_block(s, 1.0, 3.4, 5.65, 3.1, [
        ('tools: [{',                       CODE_FG),
        ('  name: "search_books",',         CODE_STRING),
        ('  description: "搜尋館藏",',      CODE_STRING),
        ('  input_schema: {',               CODE_FG),
        ('    type: "object",',             CODE_FG),
        ('    properties: {',               CODE_FG),
        ('      keyword: ',                 CODE_FG),
        ('        { type: "string" }',      CODE_FG),
        ('    }',                           CODE_FG),
        ('  }',                             CODE_FG),
        ('}]',                              CODE_FG),
    ], size=10)

    # ChatGPT
    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=PINK, fill=PINK_PASTEL,
                title="ChatGPT API")
    code_block(s, 7.2, 3.4, 5.55, 3.1, [
        ('tools: [{',                       CODE_FG),
        ('  type: "function",   ← 多包一層', CODE_ORANGE),
        ('  function: {',                   CODE_FG),
        ('    name: "search_books",',       CODE_STRING),
        ('    description: "搜尋館藏",',    CODE_STRING),
        ('    parameters: {  ← 名稱不同',   CODE_ORANGE),
        ('      type: "object",',           CODE_FG),
        ('      properties: { ... }',       CODE_FG),
        ('    }',                           CODE_FG),
        ('  }',                             CODE_FG),
        ('}]',                              CODE_FG),
    ], size=10)
    page_number(s, 11, TOTAL)


def build_mcp_teaser(prs):
    """Slide 12 — 策略 C MCP 預告.
    Before pain_nxm deep dive, give audience the frame: 'There's a third
    option called MCP, and what you're about to see is the problem it
    solves.' Avoids the audience reading pain_nxm as 'another complaint'
    without knowing where it leads."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · C", "S T R A T E G Y · M C P 預 告", accent=VIOLET)
    slide_title(s, "等等 — 還有策略 C", y=0.95)
    slide_subtitle(s,
                   "Tool Use 看完了。在看它撞牆之前,先預告:MCP 就是來解這個的",
                   y=1.85)

    # Big violet card: MCP at a glance
    pastel_card(s, 0.85, 2.7, 12.1, 3.3, accent=VIOLET, fill=VIOLET_PASTEL)
    _text(s, 1.1, 2.95, 11.6, 0.6, "★  MCP — Model Context Protocol",
          font=FONT_TITLE, size=28, color=VIOLET_DEEP, bold=True)
    _text(s, 1.1, 3.65, 11.6, 0.5,
          "Anthropic 2024 推出的「LLM 端工具」統一協定",
          font=FONT_BODY, size=18, color=INK, italic=True)
    _multi(s, 1.1, 4.30, 11.6, 1.55, [
        {"text": "▸  寫一次 MCP server,所有支援 MCP 的 LLM 應用都能用",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 8},
        {"text": "▸  工具跟 LLM 之間用 JSON-RPC 標準訊息,跨 vendor 通用",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 8},
        {"text": "▸  類比:USB-C 之於外接周邊 — 一條協定打通所有設備",
         "font": FONT_BODY, "size": 15, "color": INK, "space_after": 0},
    ])

    # Bridge arrow into pain_nxm
    _text(s, 0.85, 6.25, 12, 0.55,
          "↓  在看 MCP 怎麼運作之前,先看看 Tool Use 為什麼會撞牆",
          font=FONT_BODY, size=16, color=ORANGE, bold=True, italic=True,
          align=PP_ALIGN.CENTER)

    callout_box(s, 0.85, 7.0, 12, 0.45,
                "把接下來「Tool Use 痛點」當成「MCP 要解的問題」來看",
                accent=ORANGE, fill=ORANGE_PASTEL, icon="▶", size=13)
    page_number(s, 12, TOTAL)


def build_pain_nxm(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · B", "T O O L   U S E   ·   T H E   N × M   P A I N",
                 accent=PINK)
    slide_title(s, "Tool Use 的痛點:每個應用都要重做", y=0.95, accent=PINK)
    slide_subtitle(s, "4 個 AI 應用 × 4 個資料源 = 16 個 connector,而且格式各不相同", y=1.85)

    # Left: AI apps
    apps = ["ChatGPT App", "Claude App", "Gemini App", "自建 Agent"]
    for i, name in enumerate(apps):
        y = 2.7 + i * 0.8
        _rounded(s, 0.85, y, 2.8, 0.6, ORANGE_PASTEL,
                 line_color=ORANGE, line_w=2)
        _text(s, 0.85, y, 2.8, 0.6, name,
              font=FONT_BODY, size=13, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Middle: tangle of arrows
    _text(s, 4.0, 2.5, 5, 0.5, "N × M",
          font=FONT_TITLE, size=22, color=PINK, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 4.0, 3.0, 5, 0.45, "個別整合",
          font=FONT_BODY, size=14, color=PINK_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    # Stylized mess
    _text(s, 4.0, 3.8, 5, 1.7,
          "✕  ✕  ✕  ✕\n✕  ✕  ✕  ✕\n✕  ✕  ✕  ✕\n✕  ✕  ✕  ✕",
          font=FONT_TITLE, size=20, color=PINK, bold=True,
          align=PP_ALIGN.CENTER)

    # Right: data sources
    sources = ["圖書館 DB", "課程系統", "教師資料", "校內公告"]
    for i, name in enumerate(sources):
        y = 2.7 + i * 0.8
        _rounded(s, 9.3, y, 3.0, 0.6, TEAL_PASTEL,
                 line_color=TEAL, line_w=2)
        _text(s, 9.3, y, 3.0, 0.6, name,
              font=FONT_BODY, size=13, color=TEAL_DEEP, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.3, 12, 0.65,
                "每加一個 AI 應用或一個資料源,connector 數量爆炸成長",
                accent=PINK, fill=PINK_PASTEL, icon="!", size=14)
    page_number(s, 13, TOTAL)


def build_mcp_intro(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · C", "S T R A T E G Y   ·   M C P", accent=VIOLET)
    slide_title(s, "策略 C:MCP — 統一協定解耦", y=0.95)
    slide_subtitle(s, "寫一次 MCP Server,所有 AI 應用都能用 — 像 USB-C 一樣的標準介面", y=1.85)

    apps = ["ChatGPT App", "Claude App", "Gemini App", "自建 Agent"]
    for i, name in enumerate(apps):
        y = 2.7 + i * 0.8
        _rounded(s, 0.85, y, 2.6, 0.6, ORANGE_PASTEL,
                 line_color=ORANGE, line_w=2)
        _text(s, 0.85, y, 2.6, 0.6, name,
              font=FONT_BODY, size=12, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # MCP hub (center)
    _rounded(s, 4.55, 2.85, 4.2, 3.1, VIOLET, line_color=VIOLET, line_w=0)
    _text(s, 4.55, 3.05, 4.2, 0.5, "MCP",
          font=FONT_TITLE, size=36, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 4.55, 3.65, 4.2, 0.45, "統一協定",
          font=FONT_BODY, size=18, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 4.55, 4.2, 4.2, 0.4, "JSON-RPC 2.0",
          font=FONT_CODE, size=15, color=BG_WHITE,
          align=PP_ALIGN.CENTER)
    _text(s, 4.55, 4.9, 4.2, 0.5, "N + M",
          font=FONT_TITLE, size=28, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 4.55, 5.4, 4.2, 0.4, "(而非 N × M)",
          font=FONT_BODY, size=13, color=BG_WHITE,
          italic=True, align=PP_ALIGN.CENTER)

    sources = ["圖書館 DB", "課程系統", "教師資料", "校內公告"]
    for i, name in enumerate(sources):
        y = 2.7 + i * 0.8
        _rounded(s, 9.85, y, 2.6, 0.6, TEAL_PASTEL,
                 line_color=TEAL, line_w=2)
        _text(s, 9.85, y, 2.6, 0.6, name,
              font=FONT_BODY, size=12, color=TEAL_DEEP, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    page_number(s, 14, TOTAL)


def build_compare(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ★", "C O M P A R E   ·   R A G   v s   T O O L   v s   M C P",
                 accent=VIOLET)
    slide_title(s, "三者比較總覽", y=0.95)
    slide_subtitle(s, "從核心能力到維護成本,看哪個適合你的情境", y=1.85)

    headers = ["面向", "RAG", "Tool Use", "MCP"]
    cols_x = [0.85, 3.5, 6.5, 9.5]
    cols_w = [2.55, 2.9, 2.9, 2.9]
    colors = [VIOLET, ORANGE, BLUE, TEAL]
    fills  = [VIOLET_PASTEL, ORANGE_PASTEL, BLUE_PASTEL, TEAL_PASTEL]

    row_h = 0.46
    table_y = 2.7
    # Header
    for i, h in enumerate(headers):
        _rect(s, cols_x[i], table_y, cols_w[i], row_h, fills[i])
        _text(s, cols_x[i], table_y, cols_w[i], row_h, h,
              font=FONT_TITLE, size=14, color=colors[i], bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    rows = [
        ("核心能力",   "檢索文件",         "執行功能",         "檢索 + 執行 + 標準化"),
        ("LLM 角色",   "讀 prompt 資訊",   "決定呼叫哪個函式", "透過 Client 調度 Server"),
        ("整合方式",   "Embedding + 向量",  "各家 API 各寫",    "統一 JSON-RPC 協定"),
        ("可重用性",   "綁定單一應用",      "綁定單一應用",      "Server 跨應用共用"),
        ("執行動作",   "✗",                "✓",                "✓"),
        ("維護成本",   "中",                "高(N×M)",          "低(N+M)"),
    ]
    for ri, row in enumerate(rows):
        y = table_y + (ri + 1) * row_h
        if ri % 2:
            _rect(s, 0.85, y, 12, row_h, SLATE_PASTEL)
        for i, cell in enumerate(row):
            _text(s, cols_x[i] + 0.1, y, cols_w[i] - 0.2, row_h, cell,
                  font=FONT_BODY, size=12,
                  color=INK if i == 0 else INK,
                  bold=(i == 0),
                  align=PP_ALIGN.CENTER if i > 0 else PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "MCP 不是「取代」前兩者 —— MCP Server 內部可以同時放 RAG 檢索 + Tool Use 函式",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 15, TOTAL)


def build_when_what(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ★", "W H E N   T O   U S E   W H I C H", accent=VIOLET)
    slide_title(s, "什麼時候用哪一種?", y=0.95)
    slide_subtitle(s, "適用場景判斷指南", y=1.85)

    items = [
        ("RAG", "適用場景:\n• 內部知識庫問答\n• 文件搜尋與摘要\n• 客服 FAQ 系統",
         "最適合大量非結構化文本",          VIOLET, VIOLET_PASTEL),
        ("Tool Use", "適用場景:\n• 呼叫特定 API\n• 資料庫查詢\n• 計算或產生圖表",
         "最適合少量、固定的工具",          ORANGE, ORANGE_PASTEL),
        ("MCP", "適用場景:\n• 多系統整合平台\n• 校園/企業助手\n• 跨應用共享工具",
         "工具多、需跨應用重用",             TEAL,   TEAL_PASTEL),
    ]
    card_w = 3.95
    for i, (name, scenarios, best, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 4.0, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.95, card_w - 0.5, 0.65, name,
              font=FONT_TITLE, size=24, color=accent, bold=True)
        _multi(s, x + 0.25, 3.7, card_w - 0.5, 2.5,
               [{"text": line, "font": FONT_BODY, "size": 14,
                 "color": INK, "space_after": 4}
                for line in scenarios.split("\n")])
        _text(s, x + 0.25, 5.95, card_w - 0.5, 0.6,
              f"★  {best}",
              font=FONT_BODY, size=13, color=accent, bold=True, italic=True)
    page_number(s, 16, TOTAL)


def build_mcp_roles(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03", "M C P   ·   核 心 概 念", accent=TEAL)
    slide_title(s, "MCP 架構四大角色", y=0.95)
    slide_subtitle(s, "Host → Client → Server → Tool —— 每層只看下一層", y=1.85)

    layers = [
        ("Host",   "使用者介面",         "Claude Desktop / 自建 Web App",         PINK,   PINK_PASTEL),
        ("Client", "MCP 協定客戶端",     "負責與 Server 建立連線、傳遞訊息",       VIOLET, VIOLET_PASTEL),
        ("Server", "MCP 服務端",         "包裝外部資源為標準化工具",                TEAL,   TEAL_PASTEL),
        ("Tool",   "具體功能定義",        "search_books / get_courses",            ORANGE, ORANGE_PASTEL),
    ]
    band_h = 0.85
    band_y0 = 2.65
    for i, (name, desc, ex, accent, fill) in enumerate(layers):
        y = band_y0 + i * (band_h + 0.18)
        _rounded(s, 0.85, y, 12, band_h, fill, line_color=accent, line_w=2)
        _rect(s, 0.95, y + 0.10, 0.20, band_h - 0.20, accent)
        _text(s, 1.4, y, 2.5, band_h, name,
              font=FONT_TITLE, size=20, color=accent, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 4.0, y, 3.5, band_h, desc,
              font=FONT_BODY, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 7.7, y, 5.1, band_h, ex,
              font=FONT_CODE, size=12, color=MUTED, italic=True,
              anchor=MSO_ANCHOR.MIDDLE)
    page_number(s, 17, TOTAL)


def build_jsonrpc(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ①", "M C P   ·   J S O N - R P C   2 . 0", accent=TEAL)
    slide_title(s, "MCP 如何溝通?— JSON-RPC 2.0", y=0.95)
    slide_subtitle(s, "Client / Server 雙向訊息,所有 MCP 通訊用同一格式", y=1.85)

    # Left: Client → Server
    pastel_card(s, 0.85, 2.7, 5.95, 3.6, accent=ORANGE, fill=ORANGE_PASTEL,
                title="Client → Server (Request)")
    code_block(s, 1.0, 3.4, 5.65, 2.8, [
        ('{',                              CODE_FG),
        ('  "jsonrpc": "2.0",',            CODE_FG),
        ('  "method": "tools/call",',      CODE_ORANGE),
        ('  "params": {',                  CODE_FG),
        ('    "name": "search_books",',    CODE_STRING),
        ('    "arguments": {',             CODE_FG),
        ('      "keyword": "AI"',          CODE_STRING),
        ('    }',                          CODE_FG),
        ('  },',                           CODE_FG),
        ('  "id": 1',                      CODE_FG),
        ('}',                              CODE_FG),
    ], size=11)

    # Right: Server → Client
    pastel_card(s, 7.05, 2.7, 5.85, 3.6, accent=TEAL, fill=TEAL_PASTEL,
                title="Server → Client (Response)")
    code_block(s, 7.2, 3.4, 5.55, 2.8, [
        ('{',                              CODE_FG),
        ('  "jsonrpc": "2.0",',            CODE_FG),
        ('  "result": {',                  CODE_ORANGE),
        ('    "content": [{',              CODE_FG),
        ('      "type": "text",',          CODE_FG),
        ('      "text": "找到 3 本..."',    CODE_STRING),
        ('    }]',                         CODE_FG),
        ('  },',                           CODE_FG),
        ('  "id": 1',                      CODE_FG),
        ('}',                              CODE_FG),
    ], size=11)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "標準化 · 雙向 · 傳輸無關(支援 stdio、HTTP+SSE、WebSocket)",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 18, TOTAL)


def build_nchu_case(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "04", "C A S E   S T U D Y   ·   N C H U   A I   學 伴", accent=PINK)
    slide_title(s, "33 個 MCP 工具,九大分類", y=0.95)
    slide_subtitle(s, "—— 用 Python 寫,透過 stdio 與 Node.js Client 通訊", y=1.85)

    cats = [
        ("課程查詢",   "8", "search_courses\nget_department_courses",       VIOLET, VIOLET_PASTEL),
        ("圖書資源",   "5", "search_library_books\nget_loan_history",       ORANGE, ORANGE_PASTEL),
        ("教師研究",   "7", "search_teachers\nget_research_projects",        TEAL,   TEAL_PASTEL),
        ("學術規劃",   "5", "get_cross_program_courses\nget_dual_degrees",   PINK,   PINK_PASTEL),
        ("校園資源",   "5", "get_activities\nbook_space",                    BLUE,   BLUE_PASTEL),
        ("行政法規",   "3", "search_regulations\nget_faqs",                  TEAL_DEEP, SLATE_PASTEL),
    ]
    card_w = 3.95
    card_h = 1.85
    gap_x = 0.20
    gap_y = 0.20
    for i, (name, count, tools, accent, fill) in enumerate(cats):
        col = i % 3
        row = i // 3
        x = 0.55 + col * (card_w + gap_x)
        y = 2.75 + row * (card_h + gap_y)
        _rounded(s, x, y, card_w, card_h, fill, line_color=accent, line_w=2)
        _text(s, x + 0.2, y + 0.12, card_w - 0.4, 0.5, name,
              font=FONT_TITLE, size=16, color=accent, bold=True)
        _text(s, x + card_w - 0.7, y + 0.08, 0.5, 0.5, count,
              font=FONT_TITLE, size=26, color=accent, bold=True,
              align=PP_ALIGN.RIGHT)
        _multi(s, x + 0.2, y + 0.75, card_w - 0.4, card_h - 0.9,
               [{"text": line, "font": FONT_CODE, "size": 11,
                 "color": INK_SOFT, "space_after": 2}
                for line in tools.split("\n")])
    page_number(s, 19, TOTAL)


def build_finale(prs):
    s = _blank_slide(prs, MIDNIGHT)
    _text(s, 0.85, 1.4, 12, 0.5, "—  一  句  話  總  結  —",
          font=FONT_BODY, size=14, color=MUTED, italic=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 2.6, 12, 1.2,
          "MCP 把 N×M 變成 N+M",
          font=FONT_TITLE, size=52, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 3.8, 12, 1.0,
          "—— 寫一次 Server,所有 AI 應用都能用。",
          font=FONT_TITLE, size=30, color=VIOLET, bold=True,
          align=PP_ALIGN.CENTER)
    pastel_card(s, 2.0, 5.4, 9.3, 1.2,
                accent=VIOLET, fill=RGBColor(0x1E, 0x20, 0x3A))
    _multi(s, 2.3, 5.5, 8.8, 1.05, [
        {"text": "搭配教學影片:",
         "font": FONT_BODY, "size": 14, "color": MUTED, "space_after": 4},
        {"text": "「01-why-mcp-video.mp4 —— ~3 min」",
         "font": FONT_CODE, "size": 14, "color": CODE_FG, "bold": True,
         "space_after": 0},
    ])
    page_number(s, 20, TOTAL)


def build_recap(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "★", "R E C A P", accent=VIOLET)
    slide_title(s, "本講重點回顧", y=0.95)
    slide_subtitle(s, "下一講預告:How MCP Works —— 架構與連線機制實作", y=1.85)

    points = [
        "LLM 有知識截止、無法存取外部系統的先天限制",
        "RAG 解決「讀」的問題,Tool Use 解決「做」的問題",
        "但 Tool Use 有 N×M 整合爆炸的痛點",
        "MCP 用統一協定解耦 AI 應用與資料源,實現 N+M 整合",
        "興大 AI 學伴用 33 個 MCP 工具服務真實校園需求",
    ]
    y = 2.8
    for i, txt in enumerate(points, 1):
        circle_number(s, 1.15, y + 0.25, str(i), VIOLET, r=0.26)
        _text(s, 1.7, y, 11.2, 0.55, txt,
              font=FONT_BODY, size=17, color=INK,
              anchor=MSO_ANCHOR.MIDDLE)
        y += 0.75
    page_number(s, 21, TOTAL)


# ── Main ───────────────────────────────────────────────────────────
def main():
    prs = make_presentation()
    build_cover(prs)             # 1
    build_agenda(prs)            # 2
    build_llm_can(prs)           # 3
    build_llm_cannot(prs)        # 4
    build_strategy_overview(prs) # 5  NEW — 三策略 overview
    build_rag(prs)               # 6
    build_rag_code(prs)          # 7
    build_tooluse(prs)           # 8
    build_fc_picture(prs)        # 9
    build_fc_code(prs)           # 10 NEW — Function Calling 概念程式碼
    build_tooluse_code(prs)      # 11
    build_mcp_teaser(prs)        # 12 NEW — MCP 預告 (frame next slide as MCP's problem)
    build_pain_nxm(prs)          # 13
    build_mcp_intro(prs)         # 14
    build_compare(prs)           # 15
    build_when_what(prs)         # 16
    build_mcp_roles(prs)         # 17
    build_jsonrpc(prs)           # 18
    build_nchu_case(prs)         # 19
    build_finale(prs)            # 20
    build_recap(prs)             # 21

    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
