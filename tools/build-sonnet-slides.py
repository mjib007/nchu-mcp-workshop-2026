#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build sonnet-running-example.pptx in the new visual style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "sonnet-running-example.pptx"

TOTAL = 11

STAGES = [
    "Browser",
    "ChatController",
    "raw-mcp-client.js",
    "ClaudeClient",
    "Claude Sonnet API",
    "MCP Tools",
    "SSE 串流回用戶",
]


def stage_strip(slide, active_idx):
    """Top-area horizontal strip showing the 7-stage pipeline."""
    n = len(STAGES)
    total_w = 12
    gap = 0.05
    box_w = (total_w - gap * (n - 1)) / n
    x0 = 0.85
    y = 2.6
    h = 0.7
    for i, name in enumerate(STAGES):
        x = x0 + i * (box_w + gap)
        if i == active_idx:
            _rounded(slide, x, y, box_w, h, VIOLET, line_color=VIOLET, line_w=0)
            _text(slide, x, y, box_w, h, name,
                  font=FONT_BODY, size=10, color=BG_WHITE, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        else:
            _rounded(slide, x, y, box_w, h, SLATE_PASTEL,
                     line_color=HAIRLINE, line_w=1)
            _text(slide, x, y, box_w, h, name,
                  font=FONT_BODY, size=10, color=MUTED,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def build_cover(prs):
    s = _blank_slide(prs, BG_WHITE)
    _rect(s, 0.85, 0.55, 0.55, 0.07, VIOLET)
    _text(s, 0.85, 0.75, 12, 0.4, "NCHU Claude MCP Client  ·  Running Example",
          font=FONT_BODY, size=15, color=MUTED, bold=True)
    _text(s, 0.85, 1.7, 12, 1.6, "Running Example",
          font=FONT_TITLE, size=64, color=INK, bold=True)
    _text(s, 0.85, 3.0, 12, 0.6, "原始 Sonnet 流程  ·  逐步走過 9 個 Step",
          font=FONT_BODY, size=22, color=VIOLET, bold=True)

    # Query box
    pastel_card(s, 0.85, 4.2, 12, 1.5, accent=VIOLET, fill=VIOLET_PASTEL)
    _text(s, 0.85, 4.3, 12, 0.4, "查詢範例",
          font=FONT_BODY, size=14, color=MUTED, align=PP_ALIGN.CENTER)
    _text(s, 0.85, 4.7, 12, 0.7,
          "「中興大學圖書館有什麼新書?」",
          font=FONT_TITLE, size=24, color=VIOLET_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 5.4, 12, 0.4,
          "以下逐步走過從使用者送出到收到回覆的完整流程",
          font=FONT_BODY, size=14, color=INK_SOFT, italic=True,
          align=PP_ALIGN.CENTER)

    # Pipeline strip at bottom
    n = len(STAGES)
    total_w = 12
    gap = 0.05
    box_w = (total_w - gap * (n - 1)) / n
    for i, name in enumerate(STAGES):
        x = 0.85 + i * (box_w + gap)
        _rounded(s, x, 6.2, box_w, 0.65, VIOLET_PASTEL,
                 line_color=VIOLET, line_w=1)
        _text(s, x, 6.2, box_w, 0.65, name,
              font=FONT_BODY, size=9, color=VIOLET_DEEP, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def build_step(prs, n, active, title, body_paragraphs, page):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, f"STEP {n}/9", "R U N N I N G   E X A M P L E", accent=VIOLET)
    slide_title(s, title, y=0.95, size=30)
    slide_subtitle(s, "中興大學圖書館有什麼新書?", y=1.85)
    stage_strip(s, active)

    pastel_card(s, 0.85, 3.55, 12, 3.0, accent=VIOLET, fill=VIOLET_PASTEL,
                title="說明")
    _multi(s, 1.1, 4.15, 11.5, 2.3, body_paragraphs)
    page_number(s, page, TOTAL)


def main():
    prs = make_presentation()
    build_cover(prs)  # 1

    build_step(prs, 1, 0, "Step 1:使用者送出查詢", [
        {"text": "瀏覽器透過 POST /api/chat/stream 送出訊息",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• 需攜帶 Chat Token(經 Turnstile 驗證)",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• API messages 陣列尚未建立",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 2)

    build_step(prs, 2, 1, "Step 2:ChatController 接收", [
        {"text": "後端 controller 把 chat token 解開、確認登入狀態",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• 注入「當前時間」與「登入狀態」進 system prompt",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• 把 user 訊息 push 進空的 messages 陣列",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 3)

    build_step(prs, 3, 2, "Step 3:raw-mcp-client 準備", [
        {"text": "建立 ClaudeClient 並收集所有 MCP server 的工具清單",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• mcp.getAnthropicTools() → 把 33 個工具的 schema 收齊",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• 把工具 schema 與 messages 一起準備好",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 4)

    build_step(prs, 4, 3, "Step 4:第 1 輪 — 送往 Sonnet", [
        {"text": "ClaudeClient 呼叫 Anthropic API,messages + tools 一起送",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• model: claude-sonnet-4 · max_tokens: 4096",
         "font": FONT_CODE, "size": 13, "color": INK_SOFT, "space_after": 4},
        {"text": "• 等待 API 回傳 response.content",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 5)

    build_step(prs, 5, 4, "Step 5:Sonnet 回傳 tool_use", [
        {"text": "Sonnet 判斷需要呼叫工具,回傳 tool_use block",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": '• stop_reason: "tool_use"',
         "font": FONT_CODE, "size": 13, "color": ORANGE, "bold": True,
         "space_after": 4},
        {"text": '• content[0]: { type: "tool_use", name: "search_new_books", input: {...} }',
         "font": FONT_CODE, "size": 12, "color": INK_SOFT, "space_after": 0},
    ], 6)

    build_step(prs, 6, 5, "Step 6:執行 MCP 工具", [
        {"text": "raw-mcp-client 從 tool_use 抽出 name + input,呼叫對應 MCP server",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• mcp.callTool('search_new_books', { keyword: '新書' })",
         "font": FONT_CODE, "size": 13, "color": INK_SOFT, "space_after": 4},
        {"text": "• Python MCP server 跑 SQL 查詢 → 回傳 10 筆新書",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• auto-inject user_id(若工具需要)",
         "font": FONT_BODY, "size": 13, "color": MUTED, "italic": True,
         "space_after": 0},
    ], 7)

    build_step(prs, 7, 3, "Step 7:第 2 輪 — 帶工具結果回 Sonnet", [
        {"text": "把 tool_result 以 role: user 追加到 messages,再叫一次 Sonnet",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": '• tool_result.tool_use_id 必須對應第 1 輪的 id',
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• Sonnet 看 messages + 工具結果,生成最終文字",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 8)

    build_step(prs, 8, 4, "Step 8:Sonnet 產生最終回覆", [
        {"text": "Sonnet 整合工具結果,生成自然語言 Markdown 回覆",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": '• stop_reason: "end_turn"  ← 迴圈結束',
         "font": FONT_CODE, "size": 13, "color": TEAL_DEEP, "bold": True,
         "space_after": 4},
        {"text": "• response.content[0].text 是 Markdown 格式的回覆",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 0},
    ], 9)

    build_step(prs, 9, 6, "Step 9:SSE 串流回覆給用戶", [
        {"text": "把最終文字透過 Server-Sent Events 逐字推給瀏覽器",
         "font": FONT_BODY, "size": 16, "color": INK, "space_after": 8},
        {"text": "• 前端逐字渲染,使用者看到「打字機效果」",
         "font": FONT_BODY, "size": 14, "color": INK_SOFT, "space_after": 4},
        {"text": "• 同時推送中繼事件:tool_executing / tool_completed / text_chunk / done",
         "font": FONT_BODY, "size": 13, "color": MUTED, "italic": True,
         "space_after": 0},
    ], 10)

    # Final summary
    s = _blank_slide(prs, MIDNIGHT)
    _text(s, 0.85, 1.0, 12, 0.5, "—  原  始  流  程  回  顧  —",
          font=FONT_BODY, size=14, color=MUTED, italic=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 1.8, 12, 0.7,
          "靜態 prompt + Sonnet + 2 輪 agentic loop",
          font=FONT_TITLE, size=30, color=BG_WHITE, bold=True,
          align=PP_ALIGN.CENTER)
    _text(s, 0.85, 2.7, 12, 0.5,
          "沒有工具選擇規則、沒有回覆格式規範、沒有 few-shot",
          font=FONT_BODY, size=16, color=VIOLET, italic=True,
          align=PP_ALIGN.CENTER)

    items = [
        ("靜態 System Prompt", "config.json 固定角色 + 時間/登入狀態",       VIOLET),
        ("Sonnet 模型",        "claude-sonnet-4 · $3.00 / 1M tokens",        ORANGE),
        ("2 輪 Agentic Loop", "Step 4 送出 → Step 7 回 result → Step 8 end_turn", TEAL),
    ]
    card_w = 3.95
    for i, (name, body, accent) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 3.7, card_w, 2.6, RGBColor(0x1E, 0x20, 0x3A),
                 line_color=accent, line_w=2)
        _text(s, x + 0.25, 3.9, card_w - 0.5, 0.55, name,
              font=FONT_TITLE, size=15, color=accent, bold=True,
              align=PP_ALIGN.CENTER)
        _text(s, x + 0.25, 4.7, card_w - 0.5, 1.5, body,
              font=FONT_BODY, size=13, color=CODE_FG,
              align=PP_ALIGN.CENTER)

    callout_box(s, 2.0, 6.55, 9.3, 0.45,
                "→ 對照 Haiku Alignment 報告,看新流程如何在不犧牲品質下降成本",
                accent=VIOLET, fill=RGBColor(0x1E, 0x20, 0x3A), icon="", size=13)
    page_number(s, TOTAL, TOTAL)

    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
