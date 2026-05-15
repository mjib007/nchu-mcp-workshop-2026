#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refactor 02-how-mcp-works.pptx to align with the polished v3 video.

Plan B + appendix demotion:

  * Old slides 8-11 (lifecycle section) deleted.
  * 6 new slides inserted between old slide 2 (outline) and old slide 12:
      - 01 從一個查詢開始 (section divider)
      - 場景: user query → LLM tool decision
      - Act 1: Parent / Child / Sonnet badge
      - Act 2: 兩階段握手 checkbox
      - Act 3: 工具呼叫 + 等候第 4 個請求
      - → 切換到影片
  * Old slides 3-7 (REST vs JSON-RPC) moved to end as appendix.
  * Slide 2 (outline) text refreshed to reflect new order.
  * Slide 20 (recap) vocab refreshed.

Run:
    uv run --with python-pptx python3 tools/refresh-02-slides.py

Output:
    ./02-how-mcp-works.pptx  (overwritten in place)
"""

from copy import deepcopy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parent.parent
PPTX = REPO / "02-how-mcp-works.pptx"

# ── Palette (Ocean Gradient + accents) ──────────────────────────────
NAVY    = RGBColor(0x1E, 0x27, 0x61)
DEEP    = RGBColor(0x06, 0x5A, 0x82)
TEAL    = RGBColor(0x1C, 0x72, 0x93)
ORANGE  = RGBColor(0xE8, 0x79, 0x3A)
BLUE    = RGBColor(0x5B, 0x8D, 0xE8)   # video v3 brighter blue
CYAN    = RGBColor(0x2D, 0xB5, 0xC9)   # video v3 brighter teal
GREEN   = RGBColor(0x5C, 0xB8, 0x5C)
RED     = RGBColor(0xD9, 0x53, 0x4F)
LIGHT_ORANGE = RGBColor(0xFC, 0xE5, 0xD1)   # faded fill for orange box + text
LIGHT_GREEN  = RGBColor(0xDB, 0xEE, 0xDB)
LIGHT_BLUE   = RGBColor(0xDD, 0xE7, 0xF9)
PAGE_BG = RGBColor(0xEF, 0xF2, 0xF7)        # light blue page background (matches kept slides)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DARK    = RGBColor(0x1A, 0x1A, 0x1A)
MUTED   = RGBColor(0x6B, 0x6B, 0x6B)
SOFT    = RGBColor(0xE8, 0xED, 0xF3)
DIM     = RGBColor(0xC0, 0xC0, 0xC8)
CODE_BG = RGBColor(0x10, 0x1A, 0x2E)
CODE_FG = RGBColor(0xDD, 0xE4, 0xEE)

FONT_TITLE = "Arial Black"
FONT_BODY  = "Calibri"
FONT_CODE  = "Consolas"

# The existing 02-how-mcp-works.pptx is 10.0 × 5.625 inches.
# My build helpers were originally drafted in 13.333 × 7.5 coords (gen-04 style)
# so we scale all inch values down by 0.75 to fit.
S = 0.75


def _I(v):
    """Scaled Inches — maps logical (gen-04 13.333x7.5) coords to actual 10x5.625."""
    return Inches(v * S)


def _P(v):
    """Scaled Pt — fonts scale with slide too."""
    return Pt(v * S)


# ── Build helpers (operate on a presentation's slides) ──────────────
def _add_rect(slide, x, y, w, h, color, line_color=None, line_w=None):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, _I(x), _I(y), _I(w), _I(h)
    )
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        if line_w is not None:
            sh.line.width = _P(line_w)
    sh.shadow.inherit = False
    return sh


def _add_rounded(slide, x, y, w, h, color, line_color=None, line_w=None,
                 transparency=None):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, _I(x), _I(y), _I(w), _I(h)
    )
    sh.adjustments[0] = 0.12
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
        if line_w is not None:
            sh.line.width = _P(line_w)
    sh.shadow.inherit = False
    return sh


def _add_text(slide, x, y, w, h, text, *,
              font=FONT_BODY, size=18, color=DARK,
              bold=False, italic=False, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(_I(x), _I(y), _I(w), _I(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = _I(0.05)
    tf.margin_top = tf.margin_bottom = _I(0.02)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = _P(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    return tb


def _add_multi(slide, x, y, w, h, paragraphs, *, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(_I(x), _I(y), _I(w), _I(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = _I(0.05)
    tf.vertical_anchor = anchor
    for i, spec in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec.get("align", PP_ALIGN.LEFT)
        if "space_after" in spec:
            p.space_after = _P(spec["space_after"])
        r = p.add_run()
        r.text = spec["text"]
        r.font.name = spec.get("font", FONT_BODY)
        r.font.size = _P(spec.get("size", 18))
        r.font.color.rgb = spec.get("color", DARK)
        r.font.bold = spec.get("bold", False)
        r.font.italic = spec.get("italic", False)
    return tb


def _blank_slide(prs, bg=WHITE):
    # Pick a blank-ish layout; fall back to layout 0 if only one exists
    layout = prs.slide_layouts[min(6, len(prs.slide_layouts) - 1)]
    s = prs.slides.add_slide(layout)
    rect = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    rect.fill.solid(); rect.fill.fore_color.rgb = bg
    rect.line.fill.background()
    sp_tree = s.shapes._spTree
    sp_tree.remove(rect._element); sp_tree.insert(2, rect._element)
    return s


def _chrome_slide(prs):
    """Standard content slide chrome: light-blue background + top orange strip.
    Matches the visual frame of the original kept slides so new + old read as
    one deck."""
    s = _blank_slide(prs, PAGE_BG)
    _add_rect(s, 0, 0, 13.333, 0.10, ORANGE)
    return s


def _apply_chrome(slide):
    """Apply the standard chrome (bg + top strip) to an existing/cleared slide."""
    _add_rect(slide, 0, 0, 13.333, 7.5, PAGE_BG)
    _add_rect(slide, 0, 0, 13.333, 0.10, ORANGE)


def _process_box(slide, x, y, w, h, header_color, header_label, body_label,
                 sonnet=False):
    """Draw a Parent/Child Process box matching the video's v3 aesthetic.

    header_label is the Chinese-or-English name shown on the colored header bar.
    body_label is the runtime name (e.g. Node.js / Python MCP Server).
    sonnet=True adds an orange LLM·Sonnet badge inside the box.
    """
    # Drop shadow (offset back-right)
    shadow = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        _I(x + 0.06), _I(y + 0.06), _I(w), _I(h)
    )
    shadow.adjustments[0] = 0.14
    shadow.fill.solid(); shadow.fill.fore_color.rgb = RGBColor(0, 0, 0)
    shadow.fill.transparency = 0
    shadow.line.fill.background()
    shadow.shadow.inherit = False

    # Main box (white fill + colored border)
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, _I(x), _I(y), _I(w), _I(h)
    )
    box.adjustments[0] = 0.14
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = header_color
    box.line.width = _P(2.5)
    box.shadow.inherit = False

    # Header band
    hdr_h = 0.6
    hdr = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, _I(x + 0.05), _I(y + 0.05),
        _I(w - 0.10), _I(hdr_h)
    )
    hdr.fill.solid(); hdr.fill.fore_color.rgb = header_color
    hdr.line.fill.background()
    hdr.shadow.inherit = False

    # Header text
    _add_text(slide, x + 0.05, y + 0.05, w - 0.10, hdr_h,
              header_label, font=FONT_TITLE, size=20,
              color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Body label centered in remaining area; if sonnet badge will sit at the
    # bottom-right, shorten body height so the middle-anchored label doesn't
    # drop onto the badge.
    badge_zone = 0.50 if sonnet else 0
    body_y = y + 0.05 + hdr_h + 0.10
    body_h = h - hdr_h - 0.30 - badge_zone
    _add_text(slide, x + 0.05, body_y, w - 0.10, body_h,
              body_label, font=FONT_CODE, size=14,
              color=MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Optional Sonnet badge at bottom-right inside box
    if sonnet:
        bw, bh = 1.5, 0.32
        bx = x + w - bw - 0.15
        by = y + h - bh - 0.15
        badge = _add_rounded(slide, bx, by, bw, bh, ORANGE,
                             line_color=ORANGE, line_w=1.5)
        _add_text(slide, bx, by, bw, bh, "LLM · Sonnet",
                  font=FONT_CODE, size=11, color=WHITE, bold=True,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def _arrow(slide, x1, y1, x2, y2, color, line_w=3):
    """Straight arrow from (x1,y1) to (x2,y2), inches."""
    conn = slide.shapes.add_connector(
        1,  # straight
        _I(x1), _I(y1), _I(x2), _I(y2)
    )
    conn.line.color.rgb = color
    conn.line.width = _P(line_w)
    # Add arrowhead via XML
    from pptx.oxml.ns import qn
    ln = conn.line._get_or_add_ln()
    # Remove any existing tailEnd / headEnd
    for tag in ("a:tailEnd", "a:headEnd"):
        for el in ln.findall(qn(tag)):
            ln.remove(el)
    from lxml import etree
    nsmap = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    tail = etree.SubElement(ln, qn("a:tailEnd"), nsmap=nsmap)
    tail.set("type", "triangle")
    tail.set("w", "med")
    tail.set("len", "med")
    return conn


def _pipe_pair(slide, x1, y1, x2, y2, color=MUTED, gap=0.18):
    """Two parallel lines representing bidirectional pipes."""
    for dy in (-gap, +gap):
        conn = slide.shapes.add_connector(
            1, _I(x1), _I(y1 + dy), _I(x2), _I(y2 + dy)
        )
        conn.line.color.rgb = color
        conn.line.width = _P(1.5)


# ── New slide content ───────────────────────────────────────────────
def build_slide_section_divider(prs, number, title, subtitle):
    """Section divider — compact style (matches original kept dividers).
    Teal bg + thin orange top strip + small number top-left + title below."""
    s = _blank_slide(prs, TEAL)
    _add_rect(s, 0, 0, 13.333, 0.10, ORANGE)
    # Number (orange, small upper-left)
    _add_text(s, 0.85, 2.0, 4.0, 1.0, number,
              font=FONT_TITLE, size=46, color=ORANGE, bold=True)
    # Title (white, large, below number; full width avoids overflow)
    _add_text(s, 0.85, 2.95, 12, 1.0, title,
              font=FONT_TITLE, size=42, color=WHITE, bold=True)
    # Subtitle (soft, below title)
    _add_text(s, 0.85, 4.05, 12, 0.7, subtitle,
              font=FONT_BODY, size=20, color=SOFT)
    return s


def build_slide_scenario(prs):
    """Scenario: user query → LLM tool decision."""
    s = _chrome_slide(prs)
    # Title
    _add_text(s, 0.75, 0.4, 12, 0.7, "場景:使用者問了一個問題,LLM 決定要呼叫工具",
              font=FONT_TITLE, size=26, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # User chat bubble (top-right area)
    bub_x, bub_y = 5.5, 1.8
    bub_w, bub_h = 7.0, 1.1
    _add_text(s, bub_x + bub_w - 1.5, bub_y - 0.45, 1.5, 0.35, "使用者",
              font=FONT_BODY, size=14, color=MUTED, align=PP_ALIGN.RIGHT)
    _add_rounded(s, bub_x, bub_y, bub_w, bub_h, BLUE,
                 line_color=BLUE, line_w=2.5)
    _add_text(s, bub_x, bub_y, bub_w, bub_h,
              "幫我查最近圖書館有什麼新書",
              font=FONT_BODY, size=22, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Diagonal arrow user → LLM
    _arrow(s, 6.5, 3.0, 4.5, 4.2, MUTED, line_w=2)

    # LLM thinking box (bottom-left) — faded orange fill so orange text stays visible
    llm_x, llm_y = 0.8, 4.3
    llm_w, llm_h = 7.5, 1.8
    _add_rounded(s, llm_x, llm_y, llm_w, llm_h, LIGHT_ORANGE,
                 line_color=ORANGE, line_w=2.5)
    # Fade orange fill (use line only with white fill)
    _add_multi(s, llm_x + 0.3, llm_y + 0.25, llm_w - 0.6, llm_h - 0.5, [
        {"text": "嗯…需要查新書資料庫",
         "font": FONT_BODY, "size": 20, "color": DARK},
        {"text": "→ 呼叫 search_new_books 工具",
         "font": FONT_CODE, "size": 20, "color": ORANGE, "bold": True,
         "space_after": 0},
    ])
    _add_text(s, llm_x, llm_y + llm_h + 0.05, 4, 0.35, "LLM (Sonnet)",
              font=FONT_CODE, size=14, color=MUTED)

    # Bottom hook
    _add_text(s, 0.75, 6.55, 12.5, 0.5,
              "但 LLM 自己不會呼叫 — 要靠 Parent 去跟 Child 講話",
              font=FONT_BODY, size=20, color=RED, bold=True, italic=True,
              align=PP_ALIGN.CENTER)
    return s


def build_slide_act1(prs):
    """Act 1: Parent / Child boxes + LLM Sonnet badge + pipes."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7, "Act 1 — Parent 開出 Child",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # Spawn cue at top
    _add_text(s, 4.5, 1.45, 6, 0.5, "▶ 開出 Child",
              font=FONT_CODE, size=22, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER)

    # Parent box (left)
    _process_box(s, 0.8, 2.1, 4.2, 2.5, BLUE,
                 "Parent Process", "Node.js", sonnet=True)
    # Child box (right)
    _process_box(s, 8.3, 2.1, 4.2, 2.5, CYAN,
                 "Child Process", "Python MCP Server", sonnet=False)

    # Two pipes between them
    _pipe_pair(s, 5.05, 3.35, 8.25, 3.35, MUTED, gap=0.20)

    # Bottom bullets
    _add_multi(s, 0.75, 5.0, 12.5, 2.2, [
        {"text": "• Parent (Node.js) 用 spawn() 開出 Child (Python) 子程序",
         "font": FONT_BODY, "size": 20, "color": DARK,
         "space_after": 8},
        {"text": "• LLM (Sonnet) 是 Parent 裡的一個 client component — 它住在 Parent 內,不會自己出去呼叫工具",
         "font": FONT_BODY, "size": 20, "color": DARK,
         "space_after": 8},
        {"text": "• 兩條 stdio pipe 串通 → Parent ⇄ Child 可以雙向講話",
         "font": FONT_BODY, "size": 20, "color": DARK,
         "space_after": 0},
    ])
    return s


def build_slide_act2(prs):
    """Act 2: 兩階段握手 with checkbox visualization."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7, "Act 2 — 兩階段握手",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # Left side: Parent → Child message exchange
    _process_box(s, 0.8, 2.0, 4.0, 1.5, BLUE, "Parent", "Node.js",
                 sonnet=False)
    _process_box(s, 0.8, 4.3, 4.0, 1.5, CYAN, "Child", "Python",
                 sonnet=False)

    # Two arrows: Parent → Child (orange) and Child → Parent (green)
    _arrow(s, 2.8, 3.5, 2.8, 4.3, ORANGE, line_w=3)
    _arrow(s, 2.8, 5.8, 2.8, 6.5, GREEN, line_w=3)

    _add_text(s, 5.0, 3.65, 4, 0.4, "→ 我來了 / 給我工具清單",
              font=FONT_BODY, size=15, color=ORANGE, bold=True)
    _add_text(s, 5.0, 5.85, 4, 0.4, "← 我能做什麼 / 8 個工具",
              font=FONT_BODY, size=15, color=GREEN, bold=True)

    # Right side: Two-step checklist
    panel_x, panel_y, panel_w, panel_h = 8.0, 2.0, 4.7, 3.8
    _add_rounded(s, panel_x, panel_y, panel_w, panel_h, SOFT,
                 line_color=MUTED, line_w=1.5)
    _add_text(s, panel_x + 0.3, panel_y + 0.2, panel_w - 0.6, 0.5,
              "握手進度", font=FONT_TITLE, size=18, color=NAVY, bold=True)

    # Step 1: checked green
    sx = panel_x + 0.4
    sy1 = panel_y + 0.9
    _add_rounded(s, sx, sy1, 0.5, 0.5, GREEN, line_color=GREEN, line_w=2)
    _add_text(s, sx, sy1, 0.5, 0.5, "✓",
              font=FONT_TITLE, size=22, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_text(s, sx + 0.7, sy1, 3.5, 0.5, "Step 1:打過招呼",
              font=FONT_BODY, size=20, color=GREEN, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)

    # Step 2: checked green
    sy2 = sy1 + 0.95
    _add_rounded(s, sx, sy2, 0.5, 0.5, GREEN, line_color=GREEN, line_w=2)
    _add_text(s, sx, sy2, 0.5, 0.5, "✓",
              font=FONT_TITLE, size=22, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_text(s, sx + 0.7, sy2, 3.5, 0.5, "Step 2:拿到工具清單",
              font=FONT_BODY, size=20, color=GREEN, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)

    # Bottom note inside panel
    _add_text(s, panel_x + 0.3, panel_y + panel_h - 1.0, panel_w - 0.6, 0.6,
              "兩個都打勾 才算真的連上",
              font=FONT_BODY, size=18, color=NAVY, bold=True, italic=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Bottom takeaway
    _add_text(s, 0.75, 6.4, 12.5, 0.5,
              "重點:中間時刻(Step 1 ✓ 但 Step 2 ✗)Parent 還不知道工具清單,送 tool call 也沒用",
              font=FONT_BODY, size=18, color=MUTED, italic=True,
              align=PP_ALIGN.CENTER)
    return s


def build_slide_act3(prs):
    """Act 3: tool call + waiting list + result back."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7, "Act 3 — 工具呼叫",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # Parent + Child boxes
    _process_box(s, 0.8, 1.7, 3.6, 1.4, BLUE, "Parent", "Node.js",
                 sonnet=True)
    _process_box(s, 9.0, 1.7, 3.6, 1.4, CYAN, "Child", "Python",
                 sonnet=False)

    # Arrow Parent → Child (orange) with token
    _arrow(s, 4.4, 2.4, 9.0, 2.4, ORANGE, line_w=3)
    _add_rounded(s, 5.5, 2.05, 2.5, 0.55, ORANGE,
                 line_color=ORANGE, line_w=2)
    _add_text(s, 5.5, 2.05, 2.5, 0.55,
              'search_new_books("新書")',
              font=FONT_CODE, size=11, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Waiting list box below Parent — light orange so orange text reads
    _add_rounded(s, 0.8, 3.3, 3.6, 0.6, LIGHT_ORANGE,
                 line_color=ORANGE, line_w=2)
    _add_text(s, 0.8, 3.3, 3.6, 0.6,
              "等候第 4 個請求 · 30s 內",
              font=FONT_BODY, size=14, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Arrow Child → Parent (green) with result token
    _arrow(s, 9.0, 4.5, 4.4, 4.5, GREEN, line_w=3)
    _add_rounded(s, 5.5, 4.18, 2.5, 0.55, GREEN, line_color=GREEN, line_w=2)
    _add_text(s, 5.5, 4.18, 2.5, 0.55,
              "結果 · 10 筆新書",
              font=FONT_CODE, size=12, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Done waiting list (resolved) — light green so green text reads
    _add_rounded(s, 0.8, 5.0, 3.6, 0.6, LIGHT_GREEN,
                 line_color=GREEN, line_w=2)
    _add_text(s, 0.8, 5.0, 3.6, 0.6,
              "第 4 個請求 ✓ 完成",
              font=FONT_BODY, size=14, color=GREEN, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Bottom flow recap
    _add_text(s, 0.75, 5.95, 12.5, 0.5,
              "完整流程:LLM 決定 → token 飛去 Child → Child 執行 → "
              "結果飛回 → Parent 找到對應請求 → 回給使用者",
              font=FONT_BODY, size=16, color=DARK,
              align=PP_ALIGN.CENTER)

    _add_text(s, 0.75, 6.55, 12.5, 0.5,
              "「第 4 個請求」是 JSON-RPC 給每個 request 的編號,讓 response 能對得回來",
              font=FONT_BODY, size=14, color=MUTED, italic=True,
              align=PP_ALIGN.CENTER)
    return s


def build_slide_video_cue(prs):
    """Cue slide: switch to the polished video."""
    s = _blank_slide(prs, NAVY)
    _add_text(s, 0.75, 1.5, 12, 1.2, "→  切換到影片",
              font=FONT_TITLE, size=64, color=ORANGE, bold=True)
    _add_text(s, 0.75, 3.0, 12, 0.6,
              "02-mcp-connection-video.mp4   ·   2:17",
              font=FONT_CODE, size=22, color=WHITE)
    _add_rect(s, 0.75, 3.85, 2.5, 0.04, ORANGE)

    _add_multi(s, 0.75, 4.0, 12, 3.0, [
        {"text": "影片重點:",
         "font": FONT_BODY, "size": 22, "color": WHITE, "bold": True,
         "space_after": 14},
        {"text": "1. 場景開場 — 使用者問「新書」 → LLM 判斷要呼叫工具",
         "font": FONT_BODY, "size": 19, "color": SOFT, "space_after": 8},
        {"text": "2. Act 1 — Parent / Child 的 spawn 與 pipe;LLM (Sonnet) 住在 Parent 內",
         "font": FONT_BODY, "size": 19, "color": SOFT, "space_after": 8},
        {"text": "3. Act 2 — 兩階段握手:checkbox ☐打過招呼 → ✓打過招呼 → ☐拿工具 → ✓拿工具",
         "font": FONT_BODY, "size": 19, "color": SOFT, "space_after": 8},
        {"text": "4. Act 3 — 工具呼叫:token 飛去、等候第 4 個請求、結果飛回",
         "font": FONT_BODY, "size": 19, "color": SOFT, "space_after": 8},
        {"text": "5. Frame closure — 「查新書」→ Child 執行 → 10 筆新書 → 使用者",
         "font": FONT_BODY, "size": 19, "color": SOFT, "space_after": 0},
    ])
    return s


def build_appendix_divider(prs):
    """Appendix divider — same compact style as other section dividers."""
    s = _blank_slide(prs, TEAL)
    _add_rect(s, 0, 0, 13.333, 0.10, ORANGE)
    _add_text(s, 0.85, 2.0, 4.0, 1.0, "附錄",
              font=FONT_TITLE, size=46, color=ORANGE, bold=True)
    _add_text(s, 0.85, 2.95, 12, 1.0, "Appendix",
              font=FONT_TITLE, size=42, color=WHITE, bold=True)
    _add_multi(s, 0.85, 4.05, 12, 2.2, [
        {"text": "給技術 curious 老師的細節",
         "font": FONT_BODY, "size": 20, "color": SOFT, "space_after": 10},
        {"text": "• REST vs JSON-RPC 比較",
         "font": FONT_BODY, "size": 17, "color": SOFT, "space_after": 4},
        {"text": "• JSON-RPC 三種訊息類型 (Request / Response / Notification)",
         "font": FONT_BODY, "size": 17, "color": SOFT, "space_after": 0},
    ])
    return s


# ── Slide list manipulation (XML level) ─────────────────────────────
def _slides_xml(prs):
    return prs.slides._sldIdLst


def _slide_ids(prs):
    return list(_slides_xml(prs))


def _move_slide(prs, from_index, to_index):
    """Move slide currently at from_index to to_index."""
    xml = _slides_xml(prs)
    slides = list(xml)
    s = slides[from_index]
    xml.remove(s)
    # After removal, indices shift
    target = to_index if to_index < from_index else to_index - 1
    if target >= len(xml):
        xml.append(s)
    else:
        xml.insert(target, s)


def _delete_slide(prs, index):
    xml = _slides_xml(prs)
    slides = list(xml)
    xml.remove(slides[index])


# ── Slide 2 outline rewrite ─────────────────────────────────────────
def _clear_slide_shapes(slide):
    """Remove all shapes from a slide (used to rebuild slide 2 / 20)."""
    sp_tree = slide.shapes._spTree
    # Keep first 2 elements (nvGrpSpPr + grpSpPr) which are required
    children = list(sp_tree)
    for el in children:
        tag = el.tag.split("}")[-1]
        if tag in ("sp", "pic", "graphicFrame", "cxnSp", "grpSp"):
            sp_tree.remove(el)


def rebuild_slide_2(slide):
    """Rebuild slide 2 outline to reflect new structure."""
    _clear_slide_shapes(slide)
    _apply_chrome(slide)
    _add_text(slide, 0.75, 0.5, 12, 0.8, "本講大綱",
              font=FONT_TITLE, size=36, color=NAVY, bold=True)
    _add_rect(slide, 0.75, 1.40, 3, 0.04, ORANGE)

    items = [
        ("01", "Function Calling 怎麼運作",
         "LLM 只吐字串,真的執行的是外面的 harness"),
        ("02", "從一個查詢開始",
         "場景 → Parent 開出 Child → 兩階段握手 → 工具呼叫"),
        ("03", "Tool 註冊與描述",
         "JSON Schema · description 如何影響 LLM 選擇"),
        ("04", "Client 整合機制",
         "工具清單如何注入 LLM 的 system prompt"),
        ("附錄", "技術細節(時間夠就講,不夠就跳)",
         "REST vs JSON-RPC · JSON-RPC 三種訊息類型"),
    ]
    y = 1.7
    for num, title, sub in items:
        _add_text(slide, 0.8, y, 1.7, 0.7, num,
                  font=FONT_TITLE, size=36, color=ORANGE, bold=True,
                  anchor=MSO_ANCHOR.MIDDLE)
        _add_text(slide, 2.7, y, 10, 0.55, title,
                  font=FONT_TITLE, size=23, color=NAVY, bold=True,
                  anchor=MSO_ANCHOR.MIDDLE)
        _add_text(slide, 2.7, y + 0.55, 10, 0.45, sub,
                  font=FONT_BODY, size=15, color=MUTED,
                  anchor=MSO_ANCHOR.MIDDLE)
        y += 1.05


def _code_block(slide, x, y, w, h, lines, size=11, padding=0.18):
    """Dark code block; `lines` is list[str] or list[(text, color)]."""
    _add_rect(slide, x, y, w, h, CODE_BG)
    paragraphs = []
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text, color = line, CODE_FG
        paragraphs.append({
            "text": text if text else " ",
            "font": FONT_CODE,
            "size": size,
            "color": color,
            "space_after": 1,
        })
    _add_multi(slide, x + 0.25, y + padding, w - 0.45, h - padding * 2,
               paragraphs)


# ── Section 01 (new): Function Calling 怎麼運作 ──────────────────
def build_fc_setup(prs):
    """Setup slide: one concrete example + the core punchline."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "用一個具體例子搞懂",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # User query bubble
    bub_x, bub_y, bub_w, bub_h = 2.5, 1.9, 8.0, 1.0
    _add_text(s, bub_x, bub_y - 0.45, bub_w, 0.35, "使用者輸入",
              font=FONT_BODY, size=14, color=MUTED,
              align=PP_ALIGN.CENTER)
    _add_rounded(s, bub_x, bub_y, bub_w, bub_h, BLUE,
                 line_color=BLUE, line_w=2.5)
    _add_text(s, bub_x, bub_y, bub_w, bub_h,
              "我家目錄底下有幾個 .py 檔？",
              font=FONT_BODY, size=24, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Big punchline
    _add_text(s, 0.75, 3.5, 12, 0.9,
              "LLM 從頭到尾只做一件事 —— 吐字串",
              font=FONT_TITLE, size=32, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    _add_multi(s, 0.75, 4.9, 12, 2.0, [
        {"text": "所有「真的執行」的動作 —— 跑 find、發 HTTP request、改檔、開瀏覽器 —— 都發生在 LLM 外面的一段程式裡。",
         "font": FONT_BODY, "size": 18, "color": DARK,
         "align": PP_ALIGN.CENTER, "space_after": 14},
        {"text": "我們叫它 harness  (= agent runtime / agent loop runner)",
         "font": FONT_BODY, "size": 20, "color": NAVY, "bold": True,
         "align": PP_ALIGN.CENTER, "space_after": 0},
    ])
    return s


def build_fc_stage12(prs):
    """Stage 1+2: developer prepares schema + sends API call."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "Stage 1+2 — 開發者準備工具描述,送出 API call",
              font=FONT_TITLE, size=24, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    code_lines = [
        ("# 開發者寫的 Python", MUTED),
        ("tools = [{",                                                CODE_FG),
        ('  "name": "execute_bash",',                                 GREEN),
        ('  "description": "Execute a bash command. Returns stdout.",', GREEN),
        ('  "input_schema": {',                                       CODE_FG),
        ('    "type": "object",',                                     CODE_FG),
        ('    "properties": {',                                       CODE_FG),
        ('      "command": {"type": "string"}',                       CODE_FG),
        ("    },",                                                    CODE_FG),
        ('    "required": ["command"]',                               CODE_FG),
        ("  }",                                                       CODE_FG),
        ("}]",                                                        CODE_FG),
        ("",                                                          CODE_FG),
        ('messages = [{"role": "user",',                              CODE_FG),
        ('             "content": "我家目錄底下有幾個 .py 檔？"}]',     CODE_FG),
        ("",                                                          CODE_FG),
        ("response = client.messages.create(",                        CODE_FG),
        ('    model="claude-opus-4-7",',                              CODE_FG),
        ("    tools=tools,        ← 把工具 schema 一起送",             ORANGE),
        ("    messages=messages,",                                    CODE_FG),
        (")",                                                         CODE_FG),
    ]
    _code_block(s, 0.75, 1.55, 7.5, 5.3, code_lines)

    _add_multi(s, 8.6, 1.7, 4.5, 5.2, [
        {"text": "tools 只是一個 dict",
         "font": FONT_TITLE, "size": 17, "color": NAVY, "bold": True,
         "space_after": 4},
        {"text": "SDK 把它序列化成 JSON,塞進 API 的 request body。",
         "font": FONT_BODY, "size": 14, "color": DARK,
         "space_after": 16},

        {"text": "LLM 看到的是這段 JSON",
         "font": FONT_TITLE, "size": 17, "color": NAVY, "bold": True,
         "space_after": 4},
        {"text": "翻成 prompt 後 LLM 讀到「有一個叫 execute_bash 的東西,描述是這樣,參數長這樣」。",
         "font": FONT_BODY, "size": 14, "color": DARK,
         "space_after": 16},

        {"text": "✗ 沒有綁定真函式指標",
         "font": FONT_TITLE, "size": 17, "color": RED, "bold": True,
         "space_after": 4},
        {"text": "LLM 拿不到 Python 函式 reference,也碰不到 OS。它就是讀了一段文字。",
         "font": FONT_BODY, "size": 14, "color": DARK,
         "space_after": 0},
    ])
    return s


def build_fc_stage3(prs):
    """Stage 3: LLM returns JSON — the KEY teaching moment."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "Stage 3 — LLM 回了一段 JSON",
              font=FONT_TITLE, size=26, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    json_lines = [
        ("{",                                                         CODE_FG),
        ('  "id": "msg_abc123",',                                     CODE_FG),
        ('  "stop_reason": "tool_use",        ← 旗號:給 harness 看',  ORANGE),
        ('  "content": [',                                            CODE_FG),
        ('    {',                                                     CODE_FG),
        ('      "type": "text",',                                     CODE_FG),
        ('      "text": "讓我用 find 幫你數一下。"',                   GREEN),
        ('    },',                                                    CODE_FG),
        ('    {',                                                     CODE_FG),
        ('      "type": "tool_use",',                                 CODE_FG),
        ('      "id": "toolu_01XYZ",',                                CODE_FG),
        ('      "name": "execute_bash",',                             CODE_FG),
        ('      "input": {',                                          CODE_FG),
        ('        "command": "find ~ -name \'*.py\' -type f | wc -l"', GREEN),
        ('      }',                                                   CODE_FG),
        ('    }',                                                     CODE_FG),
        ('  ]',                                                       CODE_FG),
        ('}',                                                         CODE_FG),
    ]
    _code_block(s, 0.75, 1.55, 8.6, 4.3, json_lines)

    _add_multi(s, 9.6, 1.7, 3.6, 4.2, [
        {"text": "stop_reason: tool_use",
         "font": FONT_CODE, "size": 14, "color": ORANGE, "bold": True,
         "space_after": 4},
        {"text": "「我停下來了,因為產出了一個 tool_use,你接手。」",
         "font": FONT_BODY, "size": 13, "color": MUTED, "italic": True,
         "space_after": 16},

        {"text": "command 這串字",
         "font": FONT_TITLE, "size": 14, "color": GREEN, "bold": True,
         "space_after": 4},
        {"text": "是 LLM token-by-token 生出來的;constrained decoding 確保 JSON 一定合法。",
         "font": FONT_BODY, "size": 13, "color": DARK,
         "space_after": 0},
    ])

    # Big punchline at bottom
    _add_rounded(s, 0.75, 6.05, 12, 0.85, LIGHT_ORANGE,
                 line_color=ORANGE, line_w=2)
    _add_text(s, 0.75, 6.05, 12, 0.85,
              "LLM 沒有「呼叫」任何東西 —— 它就是吐了一段 JSON 字串。",
              font=FONT_TITLE, size=20, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return s


def build_fc_stage4(prs):
    """Stage 4: Harness actually executes — the 'eval LLM output' moment."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "Stage 4 — Harness 真的執行",
              font=FONT_TITLE, size=26, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    code_lines = [
        ("# Harness 拿到 LLM 的 tool_use 後,跑 dispatcher", MUTED),
        ("for block in response.content:",            CODE_FG),
        ('    if block.type == "tool_use":',          CODE_FG),
        ('        cmd = block.input["command"]',      CODE_FG),
        ("",                                          CODE_FG),
        ("        # 這一行才是「真的下去執行」",       MUTED),
        ("        result = subprocess.run(",          ORANGE),
        ("            cmd,",                          CODE_FG),
        ("            shell=True,         ← LLM 字串 → /bin/bash", ORANGE),
        ("            capture_output=True,",          CODE_FG),
        ("            text=True,",                    CODE_FG),
        ("            timeout=30,",                   CODE_FG),
        ("        )",                                 CODE_FG),
        ('        tool_output = result.stdout.strip()    # "42"', CODE_FG),
    ]
    _code_block(s, 0.75, 1.55, 8.2, 3.7, code_lines)

    # Right side: door metaphor
    _add_multi(s, 9.2, 1.7, 4.0, 3.5, [
        {"text": "「文字宇宙」",
         "font": FONT_TITLE, "size": 16, "color": BLUE, "bold": True,
         "align": PP_ALIGN.CENTER, "space_after": 2},
        {"text": "= LLM 吐的字串",
         "font": FONT_BODY, "size": 13, "color": MUTED,
         "align": PP_ALIGN.CENTER, "space_after": 14},

        {"text": "↓  這道門  ↓",
         "font": FONT_TITLE, "size": 20, "color": ORANGE, "bold": True,
         "align": PP_ALIGN.CENTER, "space_after": 4},
        {"text": "subprocess.run(...)",
         "font": FONT_CODE, "size": 13, "color": ORANGE, "bold": True,
         "align": PP_ALIGN.CENTER, "space_after": 14},

        {"text": "「真實電腦」",
         "font": FONT_TITLE, "size": 16, "color": NAVY, "bold": True,
         "align": PP_ALIGN.CENTER, "space_after": 2},
        {"text": "= shell fork + exec",
         "font": FONT_BODY, "size": 13, "color": MUTED,
         "align": PP_ALIGN.CENTER, "space_after": 0},
    ])

    # Bottom warning box
    _add_rounded(s, 0.75, 5.45, 12, 1.5,
                 RGBColor(0xFD, 0xE5, 0xE5),
                 line_color=RED, line_w=2)
    _add_multi(s, 1.0, 5.6, 11.5, 1.3, [
        {"text": "⚠  安全警告 — 本質上是 eval(LLM 輸出)",
         "font": FONT_TITLE, "size": 16, "color": RED, "bold": True,
         "space_after": 6},
        {"text": "若 prompt injection 攻擊,LLM 會生出 rm -rf ~,harness 不長眼就照跑。",
         "font": FONT_BODY, "size": 14, "color": DARK,
         "space_after": 4},
        {"text": "Production 系統必須加 sandbox / docker / allow-list / human-in-the-loop confirmation。",
         "font": FONT_BODY, "size": 14, "color": DARK, "italic": True,
         "space_after": 0},
    ])
    return s


def build_fc_stage56(prs):
    """Stage 5+6: tool_result fed back, LLM produces final answer."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "Stage 5+6 — 結果塞回,LLM 給最終答案",
              font=FONT_TITLE, size=24, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    _add_text(s, 0.75, 1.55, 8, 0.4, "messages 陣列現在長這樣:",
              font=FONT_TITLE, size=14, color=NAVY, bold=True)

    msg_lines = [
        ("[user]",                                                BLUE),
        ('    "我家目錄底下有幾個 .py 檔？"',                       CODE_FG),
        ("",                                                       CODE_FG),
        ("[assistant]",                                            ORANGE),
        ('    "讓我用 find 幫你數一下。"',                          CODE_FG),
        ('    + tool_use { execute_bash, "find ~ ..." }',          CODE_FG),
        ("",                                                       CODE_FG),
        ("[user]   ← 注意:role 是 user!",                         GREEN),
        ('    tool_result { id=toolu_01XYZ, content="42" }',       CODE_FG),
        ("",                                                       CODE_FG),
        ("[assistant]   stop_reason: end_turn",                    ORANGE),
        ('    "你家目錄底下總共有 42 個 .py 檔。"',                  CODE_FG),
    ]
    _code_block(s, 0.75, 2.0, 7.8, 4.4, msg_lines)

    _add_multi(s, 8.9, 2.0, 4.2, 4.4, [
        {"text": "tool_result 用 role: user 送回",
         "font": FONT_TITLE, "size": 15, "color": GREEN, "bold": True,
         "space_after": 4},
        {"text": "從 model 的角度,它中斷自己去問了外面的世界,外面的世界回了一句,現在輪到 model 繼續講。",
         "font": FONT_BODY, "size": 13, "color": DARK,
         "space_after": 18},

        {"text": "stop_reason: end_turn",
         "font": FONT_CODE, "size": 14, "color": ORANGE, "bold": True,
         "space_after": 4},
        {"text": "harness 看到這個(不是 tool_use)就知道:迴圈結束了。",
         "font": FONT_BODY, "size": 13, "color": DARK,
         "space_after": 18},

        {"text": "完整 loop",
         "font": FONT_TITLE, "size": 14, "color": NAVY, "bold": True,
         "space_after": 4},
        {"text": "tool_use → run → tool_result → … → end_turn",
         "font": FONT_CODE, "size": 12, "color": MUTED,
         "space_after": 0},
    ])

    _add_text(s, 0.75, 6.6, 12, 0.4,
              "可能要跑很多輪 —— LLM 可以連續呼叫多個工具,直到它覺得夠了 (end_turn)。",
              font=FONT_BODY, size=15, color=MUTED, italic=True,
              align=PP_ALIGN.CENTER)
    return s


def build_fc_takeaway(prs):
    """Takeaway: LLM ↔ Harness responsibility split + transition to MCP."""
    s = _chrome_slide(prs)
    _add_text(s, 0.75, 0.4, 12, 0.7,
              "重點:LLM ↔ Harness 職責分工",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(s, 0.75, 1.20, 3, 0.04, ORANGE)

    # Left: LLM card
    llm_x, llm_w = 0.75, 5.9
    _add_rounded(s, llm_x, 1.7, llm_w, 4.5, WHITE,
                 line_color=BLUE, line_w=2.5)
    _add_rect(s, llm_x + 0.08, 1.78, llm_w - 0.16, 0.55, BLUE)
    _add_text(s, llm_x + 0.08, 1.78, llm_w - 0.16, 0.55, "LLM 做的",
              font=FONT_TITLE, size=22, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_multi(s, llm_x + 0.4, 2.6, llm_w - 0.7, 3.4, [
        {"text": "• 純粹吐字串 (text + tool_use JSON)",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• 讀 tool schema,生 input JSON",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• Constrained decoding 確保 JSON 合法",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• 不知道工具真正做什麼",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "✗ 碰不到 OS、檔案、網路",
         "font": FONT_BODY, "size": 17, "color": RED, "bold": True,
         "space_after": 0},
    ])

    # Right: Harness card
    h_x, h_w = 6.95, 5.9
    _add_rounded(s, h_x, 1.7, h_w, 4.5, WHITE,
                 line_color=ORANGE, line_w=2.5)
    _add_rect(s, h_x + 0.08, 1.78, h_w - 0.16, 0.55, ORANGE)
    _add_text(s, h_x + 0.08, 1.78, h_w - 0.16, 0.55, "Harness 做的",
              font=FONT_TITLE, size=22, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_multi(s, h_x + 0.4, 2.6, h_w - 0.7, 3.4, [
        {"text": "• 真的執行 (subprocess、HTTP、DB…)",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• 維護 messages 陣列",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• Loop 直到 stop_reason: end_turn",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "• 處理 timeout / 錯誤 / 結果格式",
         "font": FONT_BODY, "size": 17, "color": DARK, "space_after": 8},
        {"text": "✓ 加 sandbox / 安全防護",
         "font": FONT_BODY, "size": 17, "color": GREEN, "bold": True,
         "space_after": 0},
    ])

    # Bottom transition to next section
    _add_text(s, 0.75, 6.5, 12, 0.5,
              "→ MCP 在這個機制上加了什麼?把 harness ↔ tool 的協定標準化、抽到獨立 process。",
              font=FONT_BODY, size=17, color=NAVY, bold=True, italic=True,
              align=PP_ALIGN.CENTER)
    return s


def _replace_exact_text(slide, old, new):
    """Replace any text run whose entire text == old, in place."""
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if run.text == old:
                    run.text = new


def rebuild_architecture_slide(slide):
    """Replace the old HTML-demo cue with a static 4-layer diagram."""
    _clear_slide_shapes(slide)
    _apply_chrome(slide)
    _add_text(slide, 0.75, 0.4, 12, 0.7,
              "MCP 整體架構:四層分工",
              font=FONT_TITLE, size=28, color=NAVY, bold=True)
    _add_rect(slide, 0.75, 1.20, 3, 0.04, ORANGE)

    layers = [
        ("Host",   "應用程式 / 入口",
         "興大 AI 學伴 web UI",                                  NAVY),
        ("Client", "包含 LLM + MCP client 邏輯",
         "Node.js + Sonnet  (= 影片裡的 Parent)",                 BLUE),
        ("Server", "個別 MCP server 子程序",
         "Python MCP Server  (= 影片裡的 Child)",                 CYAN),
        ("Tool",   "個別工具函式",
         "search_new_books / search_courses / search_teachers …", GREEN),
    ]

    band_h = 1.00
    band_y = 1.7
    gap = 0.20
    for i, (name, desc, ex, color) in enumerate(layers):
        y = band_y + i * (band_h + gap)
        _add_rounded(slide, 0.8, y, 12, band_h, WHITE,
                     line_color=color, line_w=2.5)
        # Colored left strip
        _add_rect(slide, 0.85, y + 0.06, 0.2, band_h - 0.12, color)
        # Layer name
        _add_text(slide, 1.2, y, 2.5, band_h, name,
                  font=FONT_TITLE, size=24, color=color, bold=True,
                  anchor=MSO_ANCHOR.MIDDLE)
        # Description (middle)
        _add_text(slide, 4.0, y, 4.3, band_h, desc,
                  font=FONT_BODY, size=18, color=DARK,
                  anchor=MSO_ANCHOR.MIDDLE)
        # Example (right)
        _add_text(slide, 8.5, y, 4.3, band_h, ex,
                  font=FONT_CODE, size=14, color=MUTED, italic=True,
                  anchor=MSO_ANCHOR.MIDDLE)

        # Arrow indicator below each band (except last)
        if i < len(layers) - 1:
            ay = y + band_h + 0.03
            _add_text(slide, 6.4, ay, 0.6, gap - 0.04, "▼",
                      font=FONT_BODY, size=16, color=MUTED,
                      align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    _add_text(slide, 0.75, 6.95, 12, 0.4,
              "Host 看不到 JSON-RPC · Client 看不到 Server 實作 · LLM 只看 name + description + inputSchema",
              font=FONT_BODY, size=14, color=MUTED, italic=True,
              align=PP_ALIGN.CENTER)


def rebuild_recap(slide):
    """Rebuild final recap slide with refreshed vocab."""
    _clear_slide_shapes(slide)
    _apply_chrome(slide)
    _add_text(slide, 0.75, 0.5, 12, 0.8, "本講重點回顧",
              font=FONT_TITLE, size=36, color=NAVY, bold=True)
    _add_rect(slide, 0.75, 1.40, 3, 0.04, ORANGE)

    items = [
        "Function calling:LLM 只吐 tool_use JSON,真的執行的是外面的 harness;harness 跨越「文字宇宙 → 真實電腦」",
        "MCP 把 LLM ⇄ 工具的通訊抽出來,變成 Parent / Child 兩個 process 之間的雙向管道",
        "兩階段握手:① 互換能力 → ② 拿到工具清單;兩步都過才算真的連上",
        "工具呼叫:LLM 決定 → token 飛去 Child → Child 執行 → 結果飛回 → 找到對應請求回給使用者",
        "每個工具由 name / description / inputSchema 三個欄位定義;description 的品質直接決定 LLM 選不選得對",
        "Client 把所有工具定義轉換後,注入 LLM API 的 tools 參數 — LLM 只看得到 name + description + inputSchema",
    ]
    y = 1.65
    for i, txt in enumerate(items, 1):
        _add_text(slide, 0.9, y, 0.8, 0.5, str(i),
                  font=FONT_TITLE, size=22, color=ORANGE, bold=True,
                  anchor=MSO_ANCHOR.MIDDLE)
        _add_text(slide, 1.8, y, 11.3, 0.5, txt,
                  font=FONT_BODY, size=16, color=DARK,
                  anchor=MSO_ANCHOR.MIDDLE)
        y += 0.78

    _add_text(slide, 0.75, 6.8, 12, 0.4,
              "下一講預告:Agentic Tool Loop — LLM 怎麼自主決定該呼叫哪個工具",
              font=FONT_BODY, size=16, color=TEAL, italic=True)


# ── Main flow ───────────────────────────────────────────────────────
def main():
    prs = Presentation(str(PPTX))
    n_orig = len(prs.slides)
    print(f"opened {PPTX.name}: {n_orig} slides")

    # Build new slides — appended at end first
    new_indices = {}

    # Section 01: Function Calling 怎麼運作 (new)
    new_indices["fc_divider"]  = len(prs.slides); build_slide_section_divider(
        prs, "01", "Function Calling 怎麼運作",
        "LLM 只吐字串,真的執行的是外面的 harness")
    new_indices["fc_setup"]    = len(prs.slides); build_fc_setup(prs)
    new_indices["fc_stage12"]  = len(prs.slides); build_fc_stage12(prs)
    new_indices["fc_stage3"]   = len(prs.slides); build_fc_stage3(prs)
    new_indices["fc_stage4"]   = len(prs.slides); build_fc_stage4(prs)
    new_indices["fc_stage56"]  = len(prs.slides); build_fc_stage56(prs)
    new_indices["fc_takeaway"] = len(prs.slides); build_fc_takeaway(prs)

    # Section 02: 從一個查詢開始 (renumbered from previous 01)
    new_indices["divider"]  = len(prs.slides); build_slide_section_divider(
        prs, "02", "從一個查詢開始",
        "用 search_new_books 走一遍完整流程")
    new_indices["scenario"] = len(prs.slides); build_slide_scenario(prs)
    new_indices["act1"]     = len(prs.slides); build_slide_act1(prs)
    new_indices["act2"]     = len(prs.slides); build_slide_act2(prs)
    new_indices["act3"]     = len(prs.slides); build_slide_act3(prs)
    new_indices["video"]    = len(prs.slides); build_slide_video_cue(prs)

    # Appendix divider
    new_indices["appendix"] = len(prs.slides); build_appendix_divider(prs)

    print(f"appended 14 new slides; total now {len(prs.slides)}")

    # Reorder. Goal final order:
    #   1: orig slide 1 (title)
    #   2: orig slide 2 (outline, REBUILT)
    #   3: new section divider
    #   4: new scenario
    #   5: new act1
    #   6: new act2
    #   7: new act3
    #   8: new video cue
    #   9-12: orig slide 12-15 (Tool description)
    #   13-16: orig slide 16-19 (Client integration)
    #   17: orig slide 20 (recap, REBUILT)
    #   18: new appendix divider
    #   19-23: orig slide 3-7 (REST vs JSON-RPC content)
    # DELETE: orig slide 8-11 (lifecycle)

    # Use sldId-element references to be safe across reorders
    xml = _slides_xml(prs)
    all_slides = list(xml)
    orig_3_to_7   = all_slides[2:7]
    orig_8_to_11  = all_slides[7:11]
    orig_12_to_19 = all_slides[11:19]
    orig_20       = all_slides[19]

    # New FC section (7 slides, indices 20..26 in the appended order)
    new_fc_divider  = all_slides[20]
    new_fc_setup    = all_slides[21]
    new_fc_stage12  = all_slides[22]
    new_fc_stage3   = all_slides[23]
    new_fc_stage4   = all_slides[24]
    new_fc_stage56  = all_slides[25]
    new_fc_takeaway = all_slides[26]

    # New query section (6 slides, indices 27..32)
    new_divider  = all_slides[27]
    new_scenario = all_slides[28]
    new_act1     = all_slides[29]
    new_act2     = all_slides[30]
    new_act3     = all_slides[31]
    new_video    = all_slides[32]

    # Appendix divider (index 33)
    new_appendix = all_slides[33]

    # Remove all from XML; then re-append in desired order
    for el in list(xml):
        xml.remove(el)

    final = [
        all_slides[0],     # 1: title (kept)
        all_slides[1],     # 2: outline (REBUILT)

        # Section 01 — Function Calling 怎麼運作 (new)
        new_fc_divider,
        new_fc_setup,
        new_fc_stage12,
        new_fc_stage3,
        new_fc_stage4,
        new_fc_stage56,
        new_fc_takeaway,

        # Section 02 — 從一個查詢開始 (renumbered)
        new_divider,
        new_scenario,
        new_act1,
        new_act2,
        new_act3,
        new_video,

        # Sections 03 + 04 — Tool 註冊與描述 / Client 整合機制 (kept original)
        *orig_12_to_19,

        # Recap
        orig_20,           # REBUILT

        # Appendix
        new_appendix,
        *orig_3_to_7,
    ]
    # orig_8_to_11 (lifecycle) dropped

    for el in final:
        xml.append(el)
    print(f"reordered to {len(final)} slides (dropped 4 lifecycle slides)")

    # NOTE on deletion: removing the sldId reference unhooks the slide from
    # the deck but the underlying slide part still lives in the package. Good
    # enough for our purposes — file is slightly larger but no broken refs.

    # Rebuild outline slide (slide 2 → index 1)
    rebuild_slide_2(prs.slides[1])
    # Recap is now at index 23 (24th slide, 0-based) after the FC + query
    # sections + 8 kept slides above it
    rebuild_recap(prs.slides[23])
    print("rebuilt outline (slide 2) and recap (slide 24)")

    # Kept section dividers already have correct numbers (03 Tool / 04 Client)
    # from the original pptx — no renumbering needed in this revision.

    # Replace the old "→ 切換到 mcp-architecture-animation.html" demo cue
    # (originally orig slide 19, now at index 22) with a static 4-layer diagram.
    rebuild_architecture_slide(prs.slides[22])
    print("rebuilt architecture slide (slide 23) — no more HTML demo cue")

    prs.save(str(PPTX))
    print(f"saved → {PPTX.name} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
