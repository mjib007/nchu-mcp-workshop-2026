#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 03-agentic-tool-loop.pptx in the new visual style."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_newstyle import *  # noqa: E402,F401,F403

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "slides" / "03-agentic-tool-loop.pptx"

TOTAL = 13


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
    # Hook card moved from floating right-bottom to under the hero subtitle,
    # creating a clean title → subtitle → hook vertical anchor in the
    # left column. Width matches hero (0.85, w=7) so it visually belongs
    # to the title group instead of orphan-floating near the author block.
    pastel_card(s, 0.85, 4.3, 7.0, 1.15, accent=VIOLET, fill=VIOLET_PASTEL)
    _text(s, 1.1, 4.4, 6.5, 0.55, "從一次回答  →  多輪迭代",
          font=FONT_TITLE, size=22, color=VIOLET_DEEP, bold=True)
    _text(s, 1.1, 4.95, 6.5, 0.45,
          "LLM 不只回答,還會自己選工具",
          font=FONT_BODY, size=15, color=INK)


def build_agenda(prs):
    """Slide 2 — A2-Standard 3-section agenda."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "00", "A G E N D A", accent=VIOLET)
    slide_title(s, "本講三段路", y=0.95, size=40)
    slide_subtitle(s, "為什麼要 → 怎麼運作 → Live Demo + 收尾", y=1.95)

    items = [
        ("①", "概念與解法",
         "single-turn 解不了複合請求\n→ Agentic 4 步走解法",
         "~10 min",  ORANGE, ORANGE_PASTEL),
        ("②", "迴圈機制",
         "Loop 視覺圖\n+ maxIterations 安全閥",
         "~8 min",   VIOLET, VIOLET_PASTEL),
        ("③", "Live Demo + 收尾",
         "5 個示範問題實機操作\n+ 三策略對比 / Segment 4 鋪陳",
         "~30 min",  TEAL,   TEAL_PASTEL),
    ]
    card_w, card_h = 4.0, 3.85
    for i, (num, title, body, time_hint, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.18)
        _rounded(s, x, 2.85, card_w, card_h, fill, line_color=accent, line_w=2)
        circle_number(s, x + 0.55, 3.30, num, accent, r=0.36)
        _text(s, x + 0.30, 4.15, card_w - 0.6, 0.6, title,
              font=FONT_TITLE, size=20, color=INK, bold=True)
        _multi(s, x + 0.30, 4.95, card_w - 0.6, 1.5,
               [{"text": line, "font": FONT_BODY, "size": 14,
                 "color": INK_SOFT, "space_after": 4}
                for line in body.split("\n")])
        # Time hint demoted from accent color to INK_SOFT so it doesn't
        # compete with title for attention; time is metadata not headline.
        _text(s, x + 0.30, 6.30, card_w - 0.6, 0.4, time_hint,
              font=FONT_CODE, size=13, color=INK_SOFT, bold=True)
    page_number(s, 2, TOTAL)


def build_loop_diagram(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ①", "A G E N T I C   L O O P · 概念圖", accent=ORANGE)
    slide_title(s, "Agentic Tool Loop 概念圖", y=0.95)
    slide_subtitle(s, "每一輪稱為一個 iteration,最多 maxIterations(預設 5)輪", y=1.85)

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
            # Arrow color follows the destination node color so the data
            # flow reads as "violet → violet → orange → orange → teal".
            arrow_color = nodes[i + 1][1]
            _text(s, x + card_w, 2.85, gap + 0.2, 1.1, "→",
                  font=FONT_TITLE, size=22, color=arrow_color, bold=True,
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
    page_number(s, 5, TOTAL)


def build_loop_trace(prs):
    """Concrete walk-through: one composite query through the rounds.
    Makes the abstract loop_diagram tangible with real tool names + data."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ②", "A G E N T I C   L O O P · 實 例 走 查", accent=ORANGE)
    slide_title(s, "走一遍:一個查詢跑完整個 loop", y=0.95, size=32)
    slide_subtitle(s, "「資工系深度學習的課,授課老師最近有什麼論文?」", y=1.85)

    rounds = [
        ("Round 1", VIOLET,
         "「先查課」  + tool_use  search_courses(深度學習, 系所=資工)",
         "→  tool_result:5 門課,授課老師:范、林、王…"),
        ("Round 2", ORANGE,
         "「查老師論文」  + tool_use  search_arxiv(范教授)",
         "→  tool_result:近期 3 篇論文(LLM 評測、低資源生成…)"),
        ("Round 3", TEAL,
         "「整合 5 個結果」  ✓ stop_reason = end_turn",
         "→  「你可修這門,范教授近期在做 LLM 評測,最對你胃口…」"),
    ]
    y0 = 2.55
    rh = 1.25
    for i, (label, color, action, result) in enumerate(rounds):
        y = y0 + i * (rh + 0.18)
        _rounded(s, 0.85, y, 12, rh, pastel_for(color), line_color=color, line_w=2)
        # round label chip on the left
        _rounded(s, 1.05, y + 0.20, 1.5, rh - 0.40, color, line_color=color)
        _text(s, 1.05, y + 0.20, 1.5, rh - 0.40, label,
              font=FONT_TITLE, size=15, color=BG_WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 2.8, y + 0.16, 9.9, 0.5, action,
              font=FONT_BODY, size=15, color=INK, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 2.8, y + 0.66, 9.9, 0.45, result,
              font=FONT_BODY, size=13, color=INK_SOFT, italic=True,
              anchor=MSO_ANCHOR.MIDDLE)
    callout_box(s, 0.85, 6.95, 12, 0.4,
                "每一輪 LLM 都看著上一輪的 tool_result,自己決定下一步 —— 你沒寫任何流程控制",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 6, TOTAL)


def build_json_anatomy(prs):
    """What tool_use / tool_result literally look like — links Seg 2's
    'LLM only emits strings' to Seg 3's loop. Three-card journey:
    LLM 吐 tool_use → 你的程式跑 → 塞 tool_result 回去 = 一輪 loop。"""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ③", "T O O L _ U S E   /   T O O L _ R E S U L T", accent=TEAL)
    slide_title(s, "tool_use / tool_result 長什麼樣", y=0.95)
    slide_subtitle(s, "Segment 2 說「LLM 只吐字串」—— 跟著一輪 loop 走一次:LLM 吐 → 你跑 → 塞回去",
                   y=1.85, size=17)

    cw, gap, cy, ch = 3.5, 0.65, 2.55, 3.15
    c1x = 0.85
    c2x = c1x + cw + gap
    c3x = c2x + cw + gap

    def card_body(x, lines):
        paras = []
        for txt, col, bold in lines:
            paras.append({"text": txt if txt else " ", "font": FONT_CODE,
                          "size": 12.5, "color": col, "bold": bold,
                          "space_after": 3})
        _multi(s, x + 0.28, cy + 1.0, cw - 0.5, ch - 1.2, paras)

    # ① LLM 吐出 (assistant content) — VIOLET
    pastel_card(s, c1x, cy, cw, ch, accent=VIOLET, fill=VIOLET_PASTEL,
                title="① LLM 吐出", title_size=20)
    _text(s, c1x + 0.28, cy + 0.62, cw - 0.5, 0.35, "assistant 的 content",
          font=FONT_BODY, size=12, color=MUTED, italic=True)
    card_body(c1x, [
        ('type: tool_use',        INK_SOFT, False),
        ('id: "toolu_01"',        PINK,     True),
        ('name:',                 INK_SOFT, False),
        ('  search_courses',      INK,      False),
        ('input:',                INK_SOFT, False),
        ('  {keyword:"深度學習"}', INK,      False),
    ])

    # ② 你的程式執行 — ORANGE
    pastel_card(s, c2x, cy, cw, ch, accent=ORANGE, fill=ORANGE_PASTEL,
                title="② 你的程式跑", title_size=20)
    _text(s, c2x + 0.28, cy + 0.62, cw - 0.5, 0.35, "harness / 你的 code",
          font=FONT_BODY, size=12, color=MUTED, italic=True)
    card_body(c2x, [
        ('讀 name + input', INK_SOFT, False),
        ('↓ 真的去呼叫',    MUTED,    False),
        ('search_courses(', INK_SOFT, False),
        ('  "深度學習")',    INK,      False),
        ('↓',               MUTED,    False),
        ('查資料庫 / API',  INK_SOFT, False),
    ])

    # ③ 塞回去 (next user message) — TEAL
    pastel_card(s, c3x, cy, cw, ch, accent=TEAL, fill=TEAL_PASTEL,
                title="③ 塞回去", title_size=20)
    _text(s, c3x + 0.28, cy + 0.62, cw - 0.5, 0.35, "下一則 user 訊息",
          font=FONT_BODY, size=12, color=MUTED, italic=True)
    card_body(c3x, [
        ('type:',                   INK_SOFT, False),
        ('  tool_result',           INK,      False),
        ('tool_use_id: "toolu_01"', PINK,     True),
        ('content:',                INK_SOFT, False),
        ('  "5 門課,范、林…"',       INK,      False),
    ])

    # arrows between cards (vertical centre of cards)
    ay = cy + ch / 2 - 0.28
    _text(s, c1x + cw - 0.05, ay, gap + 0.1, 0.55, "▶",
          font=FONT_BODY, size=26, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _text(s, c2x + cw - 0.05, ay, gap + 0.1, 0.55, "▶",
          font=FONT_BODY, size=26, color=ORANGE, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.5, 12, 0.55,
                "① 的 id 和 ③ 的 tool_use_id 必須相同 —— LLM 靠這個配對,才知道結果是回應哪一次呼叫",
                accent=PINK, fill=PINK_PASTEL, icon="▶", size=14)
    page_number(s, 7, TOTAL)


def build_loop_code(prs):
    """The 20-line loop — demystify 'agent = for-loop + if-else'."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ⑥", "A G E N T   =   2 0   行 迴 圈", accent=ORANGE)
    slide_title(s, "拆穿魔法:agent 就是一個 while 迴圈", y=0.95, size=32)
    slide_subtitle(s, "llm-client.js 的核心 —— 沒有黑魔法,就是 for-loop + if-else", y=1.85)

    code_block(s, 0.85, 2.5, 12, 3.8, [
        ("for (let i = 0; i < maxIterations; i++) {        // ← 護欄",       CODE_ORANGE),
        ("  const resp = await llm.create({ messages, tools });",            CODE_FG),
        ("",                                                                 CODE_FG),
        ("  // 沒有要呼叫工具 → 收工,回最終文字",                            CODE_COMMENT),
        ("  if (resp.stop_reason !== 'tool_use') return resp.text;",         CODE_FG),
        ("",                                                                 CODE_FG),
        ("  // 有 tool_use → 全部並行執行",                                  CODE_COMMENT),
        ("  const toolUses = resp.content.filter(b => b.type==='tool_use');", CODE_FG),
        ("  const results = await Promise.all(",                             CODE_FG),
        ("    toolUses.map(t => callTool(t.name, t.input)));",               CODE_FG),
        ("",                                                                 CODE_FG),
        ("  // 結果接回 messages → 下一輪 LLM 看得到",                       CODE_COMMENT),
        ("  messages.push(assistantMsg, { role:'user', content: results });", CODE_FG),
        ("}",                                                                CODE_FG),
    ], size=13)

    callout_box(s, 0.85, 6.5, 12, 0.5,
                "整個「自主 agent」= for-loop + if-else + 一個一直長大的 messages 陣列",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=14)
    page_number(s, 10, TOTAL)


def build_messages_growth(prs):
    """The messages[] array accumulating across rounds — the loop's memory."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ④", "M E S S A G E S   陣 列", accent=VIOLET)
    slide_title(s, "messages 陣列怎麼長大", y=0.95)
    slide_subtitle(s, "loop 的「記憶」就在這個一直變長的陣列 —— LLM 每輪都看到完整脈絡", y=1.85)

    rows = [
        ("[0]", "user",       "「資工系深度學習的課,老師論文?」", BLUE),
        ("[1]", "assistant",  "tool_use  search_courses(...)",     VIOLET),
        ("[2]", "user",       "tool_result  「5 門課,老師:范…」",  TEAL),
        ("[3]", "assistant",  "tool_use  search_arxiv(范)",        VIOLET),
        ("[4]", "user",       "tool_result  「3 篇論文…」",         TEAL),
        ("[5]", "assistant",  "text  「你可修這門…」  ✓ end_turn",  ORANGE),
    ]
    y0 = 2.55
    rh = 0.56
    for i, (idx, role, content, color) in enumerate(rows):
        y = y0 + i * (rh + 0.06)
        _rounded(s, 0.85, y, 12, rh, pastel_for(color), line_color=color, line_w=1.5)
        _text(s, 1.05, y, 0.9, rh, idx,
              font=FONT_CODE, size=14, color=color, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 2.0, y, 2.2, rh, role,
              font=FONT_CODE, size=14, color=color, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 4.3, y, 8.4, rh, content,
              font=FONT_BODY, size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)

    callout_box(s, 0.85, 6.95, 12, 0.4,
                "每輪把上一輪結果接在後面 → 陣列越來越長 → 這就是「多輪記憶」的全部祕密",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=13)
    page_number(s, 7, TOTAL)


def build_parallel_calls(prs):
    """Parallel tool calls — multiple tool_use in one turn, run concurrently."""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ⑤", "P A R A L L E L   T O O L   C A L L S", accent=TEAL)
    slide_title(s, "一回合可以同時開多支工具", y=0.95)
    slide_subtitle(s, "parallel tool calls —— 用 Promise.all 並行,不是一個接一個", y=1.85)

    # assistant box (top)
    _rounded(s, 4.5, 2.6, 4.3, 0.9, VIOLET_PASTEL, line_color=VIOLET, line_w=2)
    _text(s, 4.5, 2.6, 4.3, 0.9, "assistant:一次吐 5 個 tool_use",
          font=FONT_BODY, size=15, color=VIOLET, bold=True,
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # 5 parallel tool boxes
    names = ["arxiv(張)", "arxiv(李)", "arxiv(范)", "arxiv(林)", "arxiv(王)"]
    bw = 2.2
    for i, n in enumerate(names):
        x = 0.65 + i * (bw + 0.18)
        _rounded(s, x, 4.3, bw, 0.85, ORANGE_PASTEL, line_color=ORANGE, line_w=2)
        _text(s, x, 4.3, bw, 0.85, n,
              font=FONT_CODE, size=14, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # connector
        _text(s, x, 3.55, bw, 0.6, "↓",
              font=FONT_TITLE, size=20, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER)

    _text(s, 0.85, 5.35, 12, 0.5, "5 個查詢 並行執行(Promise.all)",
          font=FONT_BODY, size=16, color=TEAL_DEEP, bold=True,
          align=PP_ALIGN.CENTER)
    callout_box(s, 0.85, 6.4, 12, 0.55,
                "並行 → 1 秒搞定 5 個查詢,不用等 5 倍時間;5 個 tool_result 一起回給 LLM",
                accent=TEAL, fill=TEAL_PASTEL, icon="▶", size=14)
    page_number(s, 9, TOTAL)


def build_max_iter(prs):
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "02 · ⑦", "M A X _ I T E R A T I O N S · 強制回覆", accent=TEAL)
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
         "font": FONT_BODY, "size": 14, "color": PINK_DEEP, "space_after": 18},
        {"text": "情境:LLM 一直查課 → 查老師 → 查論文 →",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT,
         "italic": True, "space_after": 2},
        {"text": "再查… 30 秒過去,使用者還沒等到任何回答。",
         "font": FONT_BODY, "size": 13, "color": INK_SOFT,
         "italic": True, "space_after": 0},
    ])

    pastel_card(s, 7.05, 2.7, 5.85, 4.0, accent=TEAL, fill=TEAL_PASTEL,
                title="解法:maxIterations = 5")
    _multi(s, 7.3, 3.3, 5.4, 3.3, [
        {"text": "✓  設定最大迭代次數上限",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 6},
        {"text": "✓  第 5 輪(最後一輪)時注入臨時",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 2},
        {"text": "    user message 強制模型停止使用",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 2},
        {"text": "    工具,直接整理回覆",
         "font": FONT_BODY, "size": 14, "color": INK, "space_after": 14},
        # Quoted "強制 user message" — was 3-emphasis stacked (italic +
        # bold + FONT_CODE) which paradoxically diluted the emphasis.
        # Now: FONT_BODY + italic only, reads as actual user-text quote
        # rather than a code comment.
        {"text": "「請不要再使用任何工具,",
         "font": FONT_BODY, "size": 13, "color": TEAL_DEEP,
         "italic": True, "space_after": 2},
        {"text": "  直接根據工具回傳的資料整理 Markdown 回覆。」",
         "font": FONT_BODY, "size": 13, "color": TEAL_DEEP,
         "italic": True, "space_after": 0},
    ])
    page_number(s, 11, TOTAL)


def build_demo_cue(prs):
    """Slide 7 — Live Demo briefing with 5-question cheat sheet.
    Dual purpose: transition cue + 講師's running checklist during demo.
    Dark BG but follows the same family conventions as the other 7 slides
    (metadata bar top-left, left-aligned hero, page number bottom-right)
    so it doesn't read as 'visual orphan' from another deck."""
    s = _blank_slide(prs, MIDNIGHT)

    # Manual metadata bar in dark-BG-friendly colors. (lib metadata_bar's
    # default text color assumes light BG.)
    _oval(s, 0.85, 0.55, 0.20, ORANGE)
    _text(s, 1.2, 0.30, 12, 0.55,
          "03   L I V E   D E M O",
          font=FONT_BODY, size=14, color=RGBColor(0xCB, 0xD5, 0xE1), bold=True,
          anchor=MSO_ANCHOR.MIDDLE)

    # Hero — switched from align=CENTER to align=LEFT (default) so it
    # anchors to x=0.85 like every other slide's slide_title.
    _text(s, 0.85, 1.05, 12, 0.85, "▶  切換到 Live Demo",
          font=FONT_TITLE, size=44, color=ORANGE, bold=True)
    _text(s, 0.85, 2.05, 12, 0.45,
          "25 分鐘 · 興大 AI 學伴實機",
          font=FONT_BODY, size=18, color=RGBColor(0xCB, 0xD5, 0xE1), italic=True)

    # Section header
    _text(s, 0.85, 2.7, 12, 0.4,
          "5 個示範問題(從淺到深,完整腳本見 03-live-demo-script.md)",
          font=FONT_BODY, size=14, color=VIOLET_PASTEL, bold=True)

    # 5 question rows
    questions = [
        ("Q1", "圖書館 AI 書多少",      "single tool",         "★",      "~30s",   TEAL),
        ("Q2", "資工系深度學習老師",    "single tool + 參數",  "★",      "~30s",   TEAL),
        ("Q3", "AI 課程 + 教授介紹",    "multi-turn 主菜",     "★★",     "~60-90s", VIOLET),
        ("Q4", "新書 + 天氣",           "parallel call",       "★★",     "~45s",   ORANGE),
        ("Q5", "課程 + 論文 + 推薦",    "maxIter 挑戰",        "★★★",   "~90-120s", PINK),
    ]
    # Row dimensions tightened so we don't crash into page_number after
    # adding the metadata bar that pushed everything down ~0.4 unit.
    row_h = 0.65
    row_gap = 0.08
    for i, (num, q, tag, stars, dur, accent) in enumerate(questions):
        y = 3.20 + i * (row_h + row_gap)
        # Row bg lifted from #1E203A to #242A44 so the rounded outline
        # against the midnight BG is more readable on a projector.
        _rounded(s, 1.0, y, 11.85, row_h, RGBColor(0x24, 0x2A, 0x44),
                 line_color=accent, line_w=1.5)
        _text(s, 1.20, y, 0.70, row_h, num,
              font=FONT_CODE, size=14, color=accent, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 1.95, y, 4.50, row_h, q,
              font=FONT_BODY, size=15, color=CODE_FG, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 6.50, y, 3.40, row_h, tag,
              font=FONT_BODY, size=12.5, color=MUTED, italic=True,
              anchor=MSO_ANCHOR.MIDDLE)
        _text(s, 10.00, y, 1.55, row_h, stars,
              font=FONT_BODY, size=14, color=accent, bold=True,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        _text(s, 11.55, y, 1.25, row_h, dur,
              font=FONT_CODE, size=11, color=MUTED,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

    # Manual page number with light color so it doesn't disappear into the
    # midnight BG (lib's default uses MUTED which is ~3:1 here — WCAG fail).
    _text(s, 11.0, 7.0, 2.0, 0.4, "12 / 13",
          font=FONT_CODE, size=12, color=RGBColor(0xCB, 0xD5, 0xE1),
          align=PP_ALIGN.RIGHT)


def build_single_turn_pain(prs):
    """§1 · ① — Single-turn LLM 解不了的問題類型 (3 個例子)"""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ①", "S I N G L E - T U R N · 解不了", accent=PINK)
    slide_title(s, "為什麼需要 Agentic Loop?", y=0.95)
    slide_subtitle(s, "single-turn LLM(就算有 tool)解不了的三類問題", y=1.85)

    items = [
        ("跨領域複合查詢",
         "「找最近圖書館新書,順便看星期一台中天氣」",
         "需要兩個不相關的工具同時呼叫",
         ORANGE, ORANGE_PASTEL),
        ("結果驅動的後續查詢",
         "「資工系 AI 課的老師有什麼論文?」",
         "先要拿到老師清單,才能查論文",
         VIOLET, VIOLET_PASTEL),
        ("動態判斷要不要用 tool",
         "「圖書館有幾本 AI 書?順便比較 Claude vs GPT-4」",
         "第一部分要 tool,第二部分用訓練資料就好",
         TEAL, TEAL_PASTEL),
    ]
    card_w = 3.95
    for i, (title, example, why, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        # Card height 3.7 → 3.3 (was bottom-padding死白); callout y also up
        _rounded(s, x, 2.7, card_w, 3.3, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.9, card_w - 0.5, 0.5, title,
              font=FONT_TITLE, size=15, color=accent, bold=True)
        # example bumped 13→15 + bold (was italic) — hero in card hierarchy
        _text(s, x + 0.25, 3.55, card_w - 0.5, 1.4, example,
              font=FONT_BODY, size=15, color=INK, bold=True)
        # why dropped 13→12 + italic — clearly explanation tier
        _text(s, x + 0.25, 4.85, card_w - 0.5, 1.1, why,
              font=FONT_BODY, size=12, color=INK_SOFT, italic=True)

    # Callout y 6.6 → 6.25 to leave breathing room above page_number
    callout_box(s, 0.85, 6.25, 12, 0.55,
                "Agentic Loop = LLM 自己決定何時、用什麼工具,以及要重複幾輪",
                accent=VIOLET, fill=VIOLET_PASTEL, icon="▶", size=14)
    page_number(s, 3, TOTAL)


def build_agentic_walkthrough(prs):
    """§1 · ③ — 4-step preview of how agentic resolves a composite query"""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "01 · ②", "A G E N T I C · 解法預覽", accent=ORANGE)
    slide_title(s, "Agentic 怎麼解 — 4 步走法的骨架", y=0.95, size=30)
    slide_subtitle(s, "不管什麼複合問題,都是這 4 步;具體走一遍見下一頁", y=1.85)

    steps = [
        ("STEP 1", "拆解",
         "LLM 看問題 →\n拆成幾個子任務\n(自己想,你沒教)",
         "拆解能力 = 預訓練自帶",
         ORANGE),
        ("STEP 2", "第一輪 tool call",
         "呼叫第一個工具\n→ 拿到中間結果",
         'stop_reason = "tool_use"',
         VIOLET),
        ("STEP 3", "下一輪 tool call",
         "看上一輪結果\n→ 決定下一個工具\n(可多個並行)",
         "結果驅動的後續決定",
         TEAL),
        # STEP 4 was TEAL_DEEP (same family as STEP 3 TEAL) → cards looked
        # identical, lost the "endgame" signal. Switched to VIOLET_DEEP so
        # STEP 4 reads as "closure / return to LLM main color".
        ("STEP 4", "整合 + end_turn",
         "LLM 整合課 + 論文\n→ 完整自然語言回覆",
         'stop_reason = "end_turn"',
         VIOLET_DEEP),
    ]
    card_w = 2.95
    for i, (step, title, body, note, accent) in enumerate(steps):
        x = 0.55 + i * (card_w + 0.15)
        fill = pastel_for(accent)
        _rounded(s, x, 2.7, card_w, 3.85, fill, line_color=accent, line_w=2)
        # STEP badge bumped: rect 1.0×0.32 → 1.2×0.42, font 10 → 12
        # (was so small it looked like decoration not a progress indicator)
        _rect(s, x + 0.25, 2.85, 1.2, 0.42, accent)
        _text(s, x + 0.25, 2.85, 1.2, 0.42, step,
              font=FONT_CODE, size=12, color=BG_WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _text(s, x + 0.25, 3.30, card_w - 0.5, 0.5, title,
              font=FONT_TITLE, size=18, color=INK, bold=True)
        _text(s, x + 0.25, 3.90, card_w - 0.5, 1.9, body,
              font=FONT_BODY, size=12, color=INK)
        _text(s, x + 0.25, 6.05, card_w - 0.5, 0.45, note,
              font=FONT_CODE, size=10, color=accent, italic=True, bold=True)
    page_number(s, 4, TOTAL)


def build_strategy_callback(prs):
    """§5 · ① — 回頭跟 Segment 1 的 RAG / Tool Use / Agentic Loop 比較"""
    s = _blank_slide(prs, BG_WHITE)
    metadata_bar(s, "04 · ①", "S T R A T E G I E S · 回看", accent=VIOLET)
    slide_title(s, "回頭看三種策略 — Agentic Loop 站在哪", y=0.95, size=28)
    slide_subtitle(s, "Segment 1 介紹的三條路,Agentic Loop 是其中能力最完整的一條", y=1.85)

    items = [
        ("RAG", "檢索增強生成",
         "✓ 解知識截止\n✓ 讀私有文件",
         "✗ 不能執行動作\n✗ 單輪",
         BLUE, BLUE_PASTEL),
        ("Tool Use", "工具呼叫",
         "✓ 能執行動作\n✓ 接 API",
         "✗ 典型 1-2 輪\n✗ 不主動拆解",
         ORANGE, ORANGE_PASTEL),
        ("Agentic Loop", "多輪迭代",
         "✓ 自己拆解問題\n✓ 多輪 + 結果驅動\n✓ Tool Use 完整版",
         "△  成本最高、難 debug",
         VIOLET, VIOLET_PASTEL),
    ]
    card_w = 3.95
    for i, (name, subtitle, pros, cons, accent, fill) in enumerate(items):
        x = 0.55 + i * (card_w + 0.20)
        _rounded(s, x, 2.7, card_w, 4.0, fill, line_color=accent, line_w=2)
        _text(s, x + 0.25, 2.9, card_w - 0.5, 0.55, name,
              font=FONT_TITLE, size=22, color=accent, bold=True)
        _text(s, x + 0.25, 3.55, card_w - 0.5, 0.4, subtitle,
              font=FONT_BODY, size=13, color=MUTED, italic=True)
        _text(s, x + 0.25, 4.15, card_w - 0.5, 1.5, pros,
              font=FONT_BODY, size=13, color=INK)
        # Cons unified: ✗ red = hard limitation (RAG/Tool Use),
        # ⚠ orange = trade-off (Agentic Loop "成本最高、難 debug" is not
        # a hard wall, it's a cost). Symbol's color does the signaling now.
        _text(s, x + 0.25, 5.75, card_w - 0.5, 1.0, cons,
              font=FONT_BODY, size=13,
              color=(PINK_DEEP if i < 2 else ORANGE))

    # Bottom callout = recap + Segment 4 bridge (合併原 recap slide 進來)
    callout_box(s, 0.85, 6.95, 12, 0.55,
                "從『單輪答話』到『多輪自主』 —— Segment 4 你會親手跑一個 mini-project",
                accent=ORANGE, fill=ORANGE_PASTEL, icon="▶", size=14)
    page_number(s, 13, TOTAL)


def main():
    """A2-Standard: 8 slides, concept-light + demo-heavy.

    Cut from previous 18-slide build (all kept as dead-code functions in
    this file for reference; just no longer called):
      traditional_vs_agentic, stop_reasons, tool_use_block, tool_result,
      messages_growth, parallel_tools, core_loop_code,
      metadata_tracking, sse_streaming, engineering_footnotes,
      finale, recap
    """
    prs = make_presentation()
    build_cover(prs)                    # 1 — cover
    build_agenda(prs)                   # 2 — 3-section agenda
    build_single_turn_pain(prs)         # 3 — why agentic (problem)
    build_agentic_walkthrough(prs)      # 4 — agentic solution (4 steps)
    build_loop_diagram(prs)             # 5 — loop mechanism (abstract)
    build_loop_trace(prs)               # 6 — 一個查詢走完整 loop (具體)
    build_json_anatomy(prs)             # 7 — NEW: tool_use / tool_result JSON 長相
    build_messages_growth(prs)          # 8 — messages 陣列累積 (記憶)
    build_parallel_calls(prs)           # 9 — 並行呼叫多支工具
    build_loop_code(prs)                # 10 — NEW: 20 行 while 迴圈揭密
    build_max_iter(prs)                 # 11 — safety valve
    build_demo_cue(prs)                 # 12 — Live Demo + 5-question cheat sheet
    build_strategy_callback(prs)        # 13 — RAG/ToolUse/Agentic + Segment 4 bridge
    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
