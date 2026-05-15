#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build haiku-alignment-report.pptx in the new visual style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "haiku-alignment-report.pptx"

TOTAL = 9


def build_cover(prs):
    s = _blank_slide(prs, BG_WHITE)
    _rect(s, 0.85, 0.55, 0.55, 0.07, VIOLET)
    _text(s, 0.85, 0.75, 12, 0.4, "NCHU Claude MCP Client  ·  優化報告",
          font=FONT_BODY, size=15, color=MUTED, bold=True)
    _text(s, 0.85, 2.0, 12, 1.6, "Haiku Alignment",
          font=FONT_TITLE, size=72, color=INK, bold=True)
    _text(s, 0.85, 3.5, 12, 0.7,
          "從 Sonnet 切到 Haiku — Few-shot Alignment 降 73% 成本",
          font=FONT_BODY, size=22, color=VIOLET, bold=True)
    pastel_card(s, 8.8, 6.0, 4.3, 1.1, accent=ORANGE, fill=ORANGE_PASTEL)
    _text(s, 8.95, 6.05, 4.0, 0.5, "73%",
          font=FONT_TITLE, size=32, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 8.95, 6.6, 4.0, 0.4, "input token 成本節省",
          font=FONT_BODY, size=13, color=INK_SOFT, align=PP_ALIGN.CENTER)


def build_goal(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01", "G O A L", accent=VIOLET)
    slide_title(s, "優化目標", y=0.95)
    slide_subtitle(s, "將基底模型從 Sonnet 切換至 Haiku,同時透過 few-shot alignment 維持品質", y=1.85)

    items = [
        ("$0.80",     "vs $3.00 / 1M tokens",    "降低成本",
         "Haiku input token 價格僅 Sonnet 27%",      ORANGE, ORANGE_PASTEL),
        ("3,200+",    "筆歷史 Trace 檢索",       "維持品質",
         "Few-shot 範例引導工具選擇與回覆格式",       VIOLET, VIOLET_PASTEL),
        ("5",         "類回覆格式規範",           "結構化輸出",
         "五大分類模板,確保 Markdown 回覆一致",      TEAL,   TEAL_PASTEL),
    ]
    card_w = 3.95
    for i, (big, sub, name, body, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 3.7, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.9, card_w - 0.5, 0.8, big,
              font=FONT_TITLE, size=36, color=accent, bold=True)
        _text(s, x + 0.25, 3.75, card_w - 0.5, 0.4, sub,
              font=FONT_BODY, size=12, color=MUTED)
        _text(s, x + 0.25, 4.25, card_w - 0.5, 0.5, name,
              font=FONT_TITLE, size=15, color=INK, bold=True)
        _text(s, x + 0.25, 5.0, card_w - 0.5, 1.3, body,
              font=FONT_BODY, size=13, color=INK_SOFT)
    page_number(s, 2, TOTAL)


def build_flow_compare(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02", "F L O W   C O M P A R E", accent=VIOLET)
    slide_title(s, "請求處理流程對比", y=0.95)
    slide_subtitle(s, "綠色 = 新增或變更的元件", y=1.85)

    # Left: 原始
    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=MUTED, fill=SLATE_PASTEL,
                title="原始流程")
    _multi(s, 1.1, 3.3, 5.5, 3.3, [
        {"text": "User Query",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True, "space_after": 4},
        {"text": "ChatController (注入時間 + 登入狀態)",
         "font": FONT_BODY, "size": 13, "color": INK, "space_after": 4},
        {"text": "raw-mcp-client.js",
         "font": FONT_CODE, "size": 12, "color": INK, "space_after": 4},
        {"text": "ClaudeClient (claude-client.js)",
         "font": FONT_CODE, "size": 12, "color": INK, "space_after": 4},
        {"text": "System Prompt = 靜態 config",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "space_after": 8},
        {"text": "⬤ Claude Sonnet API",
         "font": FONT_BODY, "size": 14, "color": ORANGE, "bold": True, "space_after": 4},
        {"text": "回覆直接串流給用戶",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "space_after": 0},
    ])

    # Right: 新流程
    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=TEAL, fill=TEAL_PASTEL,
                title="新流程")
    _multi(s, 7.3, 3.3, 5.4, 3.3, [
        {"text": "User Query",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True, "space_after": 4},
        {"text": "ChatController (注入時間 + 登入狀態)",
         "font": FONT_BODY, "size": 13, "color": INK, "space_after": 4},
        {"text": "raw-mcp-client.js",
         "font": FONT_CODE, "size": 12, "color": INK, "space_after": 4},
        {"text": "claude-client-aligned.js",
         "font": FONT_CODE, "size": 12, "color": TEAL_DEEP, "bold": True, "space_after": 4},
        {"text": "AlignmentMiddleware.enrichSystemPrompt()",
         "font": FONT_CODE, "size": 11, "color": TEAL_DEEP, "bold": True, "space_after": 8},
        {"text": "⬤ Claude Haiku API",
         "font": FONT_BODY, "size": 14, "color": TEAL, "bold": True, "space_after": 4},
        {"text": "回覆直接串流給用戶",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "space_after": 0},
    ])
    page_number(s, 3, TOTAL)


def build_new_components(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ①", "N E W   C O M P O N E N T S", accent=VIOLET)
    slide_title(s, "新增元件", y=0.95)
    slide_subtitle(s, "在不改變既有架構的前提下,增加三層品質保護", y=1.85)

    items = [
        ("AlignmentMiddleware",      "api/alignment-middleware.js",
         "從歷史 trace 檢索相似範例 — keyword / embedding / hybrid",          VIOLET, VIOLET_PASTEL),
        ("Aligned ClaudeClient",     "api/claude-client-aligned.js",
         "每次 API 呼叫前透過 middleware 動態豐富 system prompt",              ORANGE, ORANGE_PASTEL),
        ("格式規範",                  "config/response-format-rules.js",
         "書籍/課程/活動/人員/法規 五大分類 Markdown 模板",                    TEAL,   TEAL_PASTEL),
        ("Trace 資料",                "data/nchu_traces/*.jsonl",
         "3,207 筆正例 + 876 筆負例,作為 few-shot 檢索來源",                    PINK,   PINK_PASTEL),
    ]
    rh = 0.95
    y0 = 2.65
    for i, (name, path, desc, accent, fill) in enumerate(items):
        y = y0 + i * (rh + 0.10)
        _rounded(s, 0.85, y, 12, rh, fill, line_color=accent, line_w=2)
        _rect(s, 0.95, y + 0.15, 0.20, rh - 0.30, accent)
        _text(s, 1.4, y + 0.12, 4.0, 0.4, name,
              font=FONT_TITLE, size=14, color=accent, bold=True)
        _text(s, 1.4, y + 0.5, 4.0, 0.4, path,
              font=FONT_CODE, size=11, color=MUTED)
        _text(s, 5.6, y, 7.2, rh, desc,
              font=FONT_BODY, size=13, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    page_number(s, 4, TOTAL)


def build_quality_protection(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ②", "Q U A L I T Y   P R O T E C T I O N", accent=VIOLET)
    slide_title(s, "Enriched Prompt 三層結構", y=0.95)
    slide_subtitle(s, "Query → Retrieval → Enriched Prompt → Haiku Loop", y=1.85)

    items = [
        ("ALIGNMENT_RULES",         "工具選擇正確性",  "選對工具、填對參數",     VIOLET, VIOLET_PASTEL),
        ("RESPONSE_FORMAT_RULES",   "回覆格式品質",    "Markdown 標題/列表/圖片", ORANGE, ORANGE_PASTEL),
        ("Top-9 Few-shot Examples", "具體示範",        "query → tool_calls 配對", TEAL,   TEAL_PASTEL),
    ]
    card_w = 3.95
    for i, (name, role, body, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 3.7, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.95, card_w - 0.5, 0.55, name,
              font=FONT_CODE, size=15, color=accent, bold=True)
        _text(s, x + 0.25, 3.7, card_w - 0.5, 0.5, role,
              font=FONT_TITLE, size=15, color=INK, bold=True)
        _text(s, x + 0.25, 4.3, card_w - 0.5, 1.8, body,
              font=FONT_BODY, size=14, color=INK_SOFT)

    callout_box(s, 0.85, 6.45, 12, 0.55,
                "Query → Embedding/Keyword (3,200+ traces) → Enriched Prompt → Haiku Loop (≤7) → Markdown",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=12)
    page_number(s, 5, TOTAL)


def build_cost(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03", "C O S T   I M P A C T", accent=ORANGE)
    slide_title(s, "成本影響分析", y=0.95)
    slide_subtitle(s, "節省 73% input token 費用,額外開銷可忽略不計", y=1.85)

    pastel_card(s, 0.85, 2.7, 5.95, 4.0, accent=ORANGE, fill=ORANGE_PASTEL,
                title="模型成本比較")
    _text(s, 1.1, 3.3, 5.5, 0.7, "73 %",
          font=FONT_TITLE, size=64, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 1.1, 4.4, 5.5, 0.4, "input token 費用",
          font=FONT_BODY, size=14, color=INK_SOFT, italic=True,
          align=PP_ALIGN.CENTER)
    _multi(s, 1.5, 5.0, 4.7, 1.6, [
        {"text": "Sonnet:   $3.00 / 1M tokens",
         "font": FONT_CODE, "size": 13, "color": MUTED, "space_after": 4},
        {"text": "Haiku:    $0.80 / 1M tokens",
         "font": FONT_CODE, "size": 13, "color": TEAL_DEEP, "bold": True,
         "space_after": 0},
    ])

    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=VIOLET, fill=VIOLET_PASTEL,
                title="額外開銷")
    _multi(s, 7.3, 3.3, 5.4, 3.3, [
        {"text": "格式規範額外 token",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True, "space_after": 2},
        {"text": "~300 tokens/request — 五大分類模板",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "space_after": 10},
        {"text": "Few-shot 範例額外 token",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True, "space_after": 2},
        {"text": "~1,200 tokens/request — Top-9 相似範例",
         "font": FONT_BODY, "size": 12, "color": INK_SOFT, "space_after": 14},
        {"text": "每次請求額外成本",
         "font": FONT_BODY, "size": 13, "color": INK, "bold": True, "space_after": 2},
        {"text": "~ $0.0012 可忽略不計",
         "font": FONT_CODE, "size": 13, "color": TEAL_DEEP, "bold": True,
         "space_after": 0},
    ])
    page_number(s, 6, TOTAL)


def build_fallback(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "03 · ①", "M O D E L S   &   F A L L B A C K", accent=ORANGE)
    slide_title(s, "模型與備援配置", y=0.95)
    slide_subtitle(s, "最後一輪格式化提示也跟著改", y=1.85)

    headers = ["項目", "原始", "新流程"]
    cols_x = [0.85, 4.2, 8.5]
    cols_w = [3.2, 4.2, 4.4]
    fills  = [SLATE_PASTEL, ORANGE_PASTEL, TEAL_PASTEL]
    colors = [INK, ORANGE, TEAL_DEEP]

    rh = 0.55
    table_y = 2.7
    for i, h in enumerate(headers):
        _rect(s, cols_x[i], table_y, cols_w[i], rh, fills[i])
        _text(s, cols_x[i], table_y, cols_w[i], rh, h,
              font=FONT_TITLE, size=14, color=colors[i], bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    rows = [
        ("主要模型",     "Claude Sonnet",                  "Claude Haiku"),
        ("備援順序",     "ollama → claude",                "claude → ollama"),
        ("Controllers", "硬編碼 claude-sonnet-4",         "config.claudeModel[0] 統一控管"),
    ]
    for ri, row in enumerate(rows):
        y = table_y + (ri + 1) * rh
        if ri % 2:
            _rect(s, 0.85, y, 12.1, rh, SLATE_PASTEL)
        for i, cell in enumerate(row):
            _text(s, cols_x[i] + 0.15, y, cols_w[i] - 0.3, rh, cell,
                  font=FONT_BODY, size=12, color=INK,
                  bold=(i == 0),
                  anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 5.3, 12, 1.5, "", accent=VIOLET, fill=VIOLET_PASTEL,
                icon="")
    _multi(s, 1.0, 5.4, 11.7, 1.3, [
        {"text": "最後一輪提示對比",
         "font": FONT_TITLE, "size": 14, "color": VIOLET_DEEP, "bold": True,
         "space_after": 6},
        {"text": "原始:「不要用工具,直接回覆」",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT, "space_after": 4},
        {"text": "新流程:「不要用工具,整理出結構化 Markdown 回覆」+ 5 點格式要求",
         "font": FONT_BODY, "size": 13, "color": VIOLET_DEEP, "bold": True,
         "space_after": 0},
    ])
    page_number(s, 7, TOTAL)


def build_limits(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "04", "L I M I T A T I O N S", accent=PINK)
    slide_title(s, "已知限制", y=0.95)
    slide_subtitle(s, "整體成效正面,但仍有三項限制需注意", y=1.85)

    items = [
        ("中", "多語系影響",
         "Trace 與規則皆為中文,非中文使用者 few-shot 匹配率較低", PINK, PINK_PASTEL),
        ("低", "工具選擇差異",
         "Haiku 選擇的工具與 Sonnet 不完全一致,但方向通常正確",   ORANGE, ORANGE_PASTEL),
        ("低", "部分 Controller 未套用",
         "AdminController / QuickQuestionController 仍用原版",       TEAL, TEAL_PASTEL),
    ]
    card_w = 3.95
    for i, (severity, name, body, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 3.7, fill, line_color=accent, line_w=2)
        # Severity badge
        _rounded(s, x + 0.25, 2.9, 1.0, 0.45, accent, line_color=accent, line_w=0)
        _text(s, x + 0.25, 2.9, 1.0, 0.45, severity,
              font=FONT_TITLE, size=15, color=BG_WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, x + 0.25, 3.55, card_w - 0.5, 0.55, name,
              font=FONT_TITLE, size=16, color=accent, bold=True)
        _text(s, x + 0.25, 4.3, card_w - 0.5, 2.0, body,
              font=FONT_BODY, size=13, color=INK_SOFT)
    page_number(s, 8, TOTAL)


def build_summary(prs):
    s = _blank_slide(prs, MIDNIGHT)
    _text(s, 0.85, 1.0, 12, 0.5, "—  總  結  —",
          font=FONT_BODY, size=14, color=MUTED, italic=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 1.7, 12, 0.7, "NCHU Claude MCP Client — Haiku Alignment 優化",
          font=FONT_TITLE, size=24, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)

    items = [
        ("73%",    "成本節省",       "Input token 費用大幅降低",         ORANGE),
        ("3,200+", "Trace 範例",     "Few-shot alignment 品質基礎",      VIOLET),
        ("5 類",   "格式規範",       "書籍/課程/活動/人員/法規",          TEAL),
        ("7 輪",   "Agentic Loop",   "最大工具呼叫迭代次數",              PINK),
    ]
    card_w = 2.95
    for i, (big, name, body, accent) in enumerate(items):
        x = 0.85 + i * (card_w + 0.20)
        _rounded(s, x, 2.8, card_w, 3.5, RGBColor(0x1E, 0x20, 0x3A),
                 line_color=accent, line_w=2)
        _text(s, x + 0.25, 3.05, card_w - 0.5, 1.0, big,
              font=FONT_TITLE, size=42, color=accent, bold=True,
              align=PP_ALIGN.CENTER)
        _text(s, x + 0.25, 4.2, card_w - 0.5, 0.5, name,
              font=FONT_TITLE, size=16, color=BG_WHITE, bold=True,
              align=PP_ALIGN.CENTER)
        _text(s, x + 0.25, 4.85, card_w - 0.5, 1.3, body,
              font=FONT_BODY, size=13, color=MUTED,
              align=PP_ALIGN.CENTER)
    page_number(s, 9, TOTAL)


def main():
    prs = make_presentation()
    build_cover(prs)              # 1
    build_goal(prs)               # 2
    build_flow_compare(prs)       # 3
    build_new_components(prs)     # 4
    build_quality_protection(prs) # 5
    build_cost(prs)               # 6
    build_fallback(prs)           # 7
    build_limits(prs)             # 8
    build_summary(prs)            # 9
    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
