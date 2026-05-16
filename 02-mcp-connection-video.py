"""
02-mcp-connection-video.py

3-min long video adapted from mcp-connection-animation.html.
Topic: MCP handshake — how parent (Node.js) and child (Python MCP server) talk.

Three phases:
  Act 1: spawn — fork child process + stdio pipe + env substitution
  Act 2: handshake — initialize → capabilities → tools/list (ready vs isConnected)
  Act 3: tool call — executeToolCall + pendingRequests Map + resolve

Render:
  manim -ql --disable_caching 02-mcp-connection-video.py MCPConnection
  manim -qh 02-mcp-connection-video.py MCPConnection       # final 1080p60
"""

from manim import *
import numpy as np

# Violet-primary palette (aligned with 2026 slide deck + V3 video)
BG          = "#0a0a10"   # 3B1B-style near-black
DEEP_BLUE   = "#065A82"
TEAL        = "#2DB5C9"   # was #1C7293 — pushed toward cyan for box-vs-box contrast
INK         = "#FFFFFF"
NEUTRAL     = "#B4BED2"
BLUE        = "#5B8DE8"   # Subject / user / secondary entity
VIOLET      = "#7B5CF5"   # LLM main subject (aligned w/ V1, V3, slide deck)
VIOLET_SOFT = "#9D85F7"
VIOLET_DEEP = "#5B3ED9"
ORANGE      = "#E8793A"   # tool call / accumulator / breakthrough
GREEN       = "#5CB85C"
RED         = "#D9534F"
DIM         = "#3A4A6A"
SHADOW      = "#000000"

CN_FONT     = "Noto Sans CJK TC"
SERIF_FONT  = "Noto Serif CJK TC"
MONO_FONT   = "DejaVu Sans Mono"

config.frame_width  = 16
config.frame_height = 9
config.pixel_width  = 1920
config.pixel_height = 1080


class MCPConnection(Scene):
    SUBTITLE_MAX_WIDTH = 14.0
    TOTAL_SECONDS = 136.3   # ~2:16 — R6 fixes net effect

    TITLE     = "MCP 握手"
    SUBTITLE  = "Parent / Child Process 怎麼開始講話"

    def construct(self):
        self.camera.background_color = BG
        self._cur_subtitle = None
        self._init_progress_bar()

        # Persistent across acts: parent / child boxes + pipe line
        self.parent_box = None
        self.child_box = None
        self.parent_label = None
        self.child_label = None
        self.pipe_top = None
        self.pipe_bot = None
        self.state_panel = None
        self.state_ready = None
        self.state_conn = None

        self.scene_intro()        # 0:00–0:04
        self.scene_scenario()     # 0:04–0:17  (NEW: user query → LLM decides)
        self.scene_act1()         # 0:17–0:30
        self.scene_act2()         # 0:30–1:18
        self.scene_act3()         # 1:18–1:56
        self.scene_outro()        # 1:56–2:14

    # ============================================================
    # Progress bar
    # ============================================================
    def _init_progress_bar(self):
        self._bar_total_width = config.frame_width - 1.6
        self._bar_height = 0.05
        self._bar_y = -config.frame_height / 2 + 0.25
        self._bar_left = -self._bar_total_width / 2

        self.progress_bg = Rectangle(
            width=self._bar_total_width, height=self._bar_height,
            stroke_width=0, fill_color=NEUTRAL, fill_opacity=0.55,
        ).move_to([0, self._bar_y, 0])

        self.progress_fill = Rectangle(
            width=0.001, height=self._bar_height,
            stroke_width=0, fill_color=ORANGE, fill_opacity=1.0
        )
        self._set_fill_width(0.001)
        self.add(self.progress_bg, self.progress_fill)

    def _set_fill_width(self, w):
        w = max(w, 0.001)
        self.progress_fill.stretch_to_fit_width(w)
        self.progress_fill.move_to([self._bar_left + w / 2, self._bar_y, 0])

    def advance_progress(self, target_seconds):
        target_w = self._bar_total_width * (target_seconds / self.TOTAL_SECONDS)
        self._set_fill_width(target_w)

    # ============================================================
    # Subtitle
    # ============================================================
    def _build_subtitle(self, text):
        sub = Text(text, font=CN_FONT, font_size=30, color=INK, weight=MEDIUM)
        if sub.width > self.SUBTITLE_MAX_WIDTH:
            sub.scale_to_fit_width(self.SUBTITLE_MAX_WIDTH)
        sub.to_edge(DOWN, buff=0.7)
        return sub

    def show_subtitle(self, text, run_time=0.35):
        # Sequential fade — out fully before in, prevents the ~0.15s visual
        # ghost of two subtitles overlaying during cross-fade.
        new_sub = self._build_subtitle(text)
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=run_time * 0.45)
            self._cur_subtitle = None
        self.play(FadeIn(new_sub), run_time=run_time * 0.55)
        self._cur_subtitle = new_sub

    def clear_subtitle(self, run_time=0.3):
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=run_time)
            self._cur_subtitle = None

    # ============================================================
    # ACT badge
    # ============================================================
    def _make_act_badge(self, text):
        box = RoundedRectangle(width=1.6, height=0.55, corner_radius=0.10,
                               stroke_color=ORANGE, stroke_width=2,
                               fill_color=ORANGE, fill_opacity=0.20)
        lbl = Text(text, font=MONO_FONT, font_size=22,
                   color=ORANGE, weight=BOLD).move_to(box.get_center())
        badge = VGroup(box, lbl).move_to([6.8, 3.9, 0])
        badge.set_z_index(100)
        return badge

    # ============================================================
    # Helper: process box (header bar + drop shadow + content area)
    # ============================================================
    def make_process_box(self, label_top, label_bot, color, pos):
        width = 2.8
        height = 1.7
        corner = 0.20

        # Drop shadow (slightly offset, dark fill, no stroke)
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=corner,
            stroke_width=0,
            fill_color=SHADOW, fill_opacity=0.55,
        ).shift(RIGHT * 0.10 + DOWN * 0.10)

        # Main box: solid BG fill so shadow doesn't bleed through
        box = RoundedRectangle(
            width=width, height=height, corner_radius=corner,
            stroke_color=color, stroke_width=3,
            fill_color=BG, fill_opacity=1.0,
        )

        # Header bar (filled band at top, inset slightly to respect rounded corners)
        header_h = 0.52
        header_pad = 0.06
        header = Rectangle(
            width=width - 2 * header_pad,
            height=header_h,
            stroke_width=0,
            fill_color=color, fill_opacity=0.55,
        )
        header.move_to(box.get_top() + DOWN * (header_h / 2 + header_pad))

        # Thin separator line under header for extra crispness
        sep = Line(
            start=header.get_bottom() + LEFT * (width / 2 - header_pad - 0.02),
            end=header.get_bottom() + RIGHT * (width / 2 - header_pad - 0.02),
            color=color, stroke_width=1.2,
        )

        # Title in header
        top = Text(label_top, font=CN_FONT, font_size=24, color=INK,
                   weight=BOLD).move_to(header.get_center())

        # Body label centered in lower content area
        body_top_y = header.get_bottom()[1]
        body_bot_y = box.get_bottom()[1]
        body_center_y = (body_top_y + body_bot_y) / 2
        bot = Text(label_bot, font=MONO_FONT, font_size=20,
                   color=INK).move_to([0, body_center_y, 0])

        group = VGroup(shadow, box, header, sep, top, bot).move_to(pos)
        return group

    # ============================================================
    # Helper: JSON snippet (rounded box with mono text)
    # ============================================================
    def make_json_snippet(self, lines, color=NEUTRAL, width=5.5, height=None,
                         size=18):
        text = VGroup()
        for line, line_color in lines:
            t = Text(line, font=MONO_FONT, font_size=size,
                     color=line_color, weight=MEDIUM)
            text.add(t)
        text.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        h = height if height else text.height + 0.5
        box = RoundedRectangle(width=width, height=h, corner_radius=0.12,
                               stroke_color=color, stroke_width=1.5,
                               fill_color=BG, fill_opacity=0.85)
        text.move_to(box.get_center())
        return VGroup(box, text)

    # ============================================================
    # Helper: pill capsule (flying token along an arrow)
    # ============================================================
    def _make_pill(self, label, color, size=18):
        txt = Text(label, font=MONO_FONT, font_size=size,
                   color=INK, weight=BOLD)
        pad_w = txt.width + 0.5
        pad_h = txt.height + 0.28
        pill = RoundedRectangle(
            width=pad_w, height=pad_h, corner_radius=pad_h / 2,
            stroke_color=color, stroke_width=2.5,
            fill_color=color, fill_opacity=0.85,
        )
        txt.move_to(pill.get_center())
        return VGroup(pill, txt)

    # ============================================================
    # Helper: arrow message between parent and child
    # ============================================================
    def message_arrow(self, direction, color, y_offset=0.0):
        """direction: 'right' = parent→child, 'left' = child→parent."""
        if direction == 'right':
            start = self.parent_box.get_right() + RIGHT * 0.15 + UP * y_offset
            end = self.child_box.get_left() + LEFT * 0.15 + UP * y_offset
        else:
            start = self.child_box.get_left() + LEFT * 0.15 + UP * y_offset
            end = self.parent_box.get_right() + RIGHT * 0.15 + UP * y_offset
        arrow = Arrow(start=start, end=end, color=color, stroke_width=4,
                      buff=0.05, max_tip_length_to_length_ratio=0.10)
        return arrow

    # ============================================================
    # SCENARIO (12s) — frame the whole video around one user query
    # ============================================================
    def scene_scenario(self):
        # User query bubble (right side, blue)
        user_query = Text("幫我查最近圖書館有什麼新書",
                          font=CN_FONT, font_size=26, color=INK,
                          weight=MEDIUM)
        user_pad_w = user_query.width + 0.7
        user_pad_h = user_query.height + 0.55
        user_bubble = RoundedRectangle(
            width=user_pad_w, height=user_pad_h, corner_radius=0.22,
            stroke_color=BLUE, stroke_width=2.5,
            fill_color=BLUE, fill_opacity=0.22,
        )
        user_query.move_to(user_bubble.get_center())
        user_group = VGroup(user_bubble, user_query)
        user_group.move_to(RIGHT * 1.6 + UP * 1.8)

        user_lbl = Text("使用者", font=CN_FONT, font_size=20,
                        color=NEUTRAL)
        user_lbl.next_to(user_group, UP, buff=0.18)
        user_lbl.align_to(user_group, RIGHT)

        self.show_subtitle("使用者問 AI 學伴一個問題")
        self.play(FadeIn(user_lbl, shift=DOWN * 0.1),
                  FadeIn(user_group, shift=DOWN * 0.2),
                  run_time=0.6)
        self.wait(2.5)

        # LLM thinking box (left side — violet for main subject;
        # tool-call line stays ORANGE for "action/tool" semantic)
        line1 = Text("嗯…需要查新書資料庫",
                     font=CN_FONT, font_size=22, color=INK)
        line2 = Text("→ 呼叫 search_new_books 工具",
                     font=MONO_FONT, font_size=22, color=ORANGE,
                     weight=BOLD)
        llm_text = VGroup(line1, line2).arrange(DOWN, buff=0.18,
                                                aligned_edge=LEFT)
        llm_pad_w = llm_text.width + 0.8
        llm_pad_h = llm_text.height + 0.55
        llm_box = RoundedRectangle(
            width=llm_pad_w, height=llm_pad_h, corner_radius=0.20,
            stroke_color=VIOLET, stroke_width=2.5,
            fill_color=VIOLET, fill_opacity=0.15,
        )
        llm_text.move_to(llm_box.get_center())
        llm_group = VGroup(llm_box, llm_text)
        llm_group.move_to(LEFT * 2.2 + DOWN * 0.8)

        llm_lbl = Text("LLM (Sonnet)", font=MONO_FONT, font_size=20,
                       color=NEUTRAL)
        llm_lbl.next_to(llm_group, DOWN, buff=0.18)
        llm_lbl.align_to(llm_group, LEFT)

        # Soft connector arrow user → LLM
        connector = Arrow(
            start=user_group.get_bottom() + DOWN * 0.05 + LEFT * 0.6,
            end=llm_group.get_top() + UP * 0.05 + RIGHT * 0.8,
            color=NEUTRAL, stroke_width=2.5, buff=0.1,
            max_tip_length_to_length_ratio=0.08,
        )

        self.show_subtitle("LLM 判斷：這題我得呼叫工具")
        self.play(GrowArrow(connector), run_time=0.4)
        self.play(FadeIn(llm_group, shift=UP * 0.2),
                  FadeIn(llm_lbl, shift=UP * 0.1),
                  run_time=0.6)
        self.wait(3.5)

        # Transition hook — highlight the tool name, change subtitle
        self.show_subtitle("但 LLM 自己不會呼叫 —— 要靠 Parent 去跟 Child 講話")
        self.play(Indicate(line2, scale_factor=1.12, color=ORANGE),
                  run_time=1.2)
        self.wait(4.5)

        # cleanup
        self.play(FadeOut(user_lbl), FadeOut(user_group),
                  FadeOut(connector),
                  FadeOut(llm_group), FadeOut(llm_lbl),
                  run_time=0.6)
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=0.3)
            self._cur_subtitle = None
        self.advance_progress(17)

    # ============================================================
    # INTRO (5s) — magazine-style cover: undraw illustration + title
    # ============================================================
    def scene_intro(self):
        # ── Right side: hero illustration (undraw "building-blocks") ──
        hero = SVGMobject(
            "intro-assets/undraw_building-blocks.svg",
        ).scale_to_fit_height(5.6)
        hero.move_to(RIGHT * 3.6 + DOWN * 0.1)

        # ── Left side: title stack ──
        title_lines = VGroup(
            Text("MCP", font=SERIF_FONT, font_size=110,
                 color=INK, weight=BOLD),
            Text("握手", font=SERIF_FONT, font_size=110,
                 color=INK, weight=BOLD),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        kicker = Text("章節 02", font=MONO_FONT, font_size=18,
                      color=VIOLET, weight=BOLD).next_to(
                          title_lines, UP, buff=0.30, aligned_edge=LEFT)
        accent = Line(start=LEFT * 0.0, end=RIGHT * 1.8,
                      color=VIOLET, stroke_width=5).next_to(
                          title_lines, DOWN, buff=0.30, aligned_edge=LEFT)
        sub = Text("Parent / Child Process\n怎麼開始講話",
                   font=CN_FONT, font_size=26, color=NEUTRAL,
                   line_spacing=1.1).next_to(
                       accent, DOWN, buff=0.30, aligned_edge=LEFT)
        title_stack = VGroup(kicker, title_lines, accent, sub).move_to(
            LEFT * 4.2 + UP * 0.1)

        # Phase 1: hero fades in with slight scale (0–0.9s)
        hero.scale(0.95)
        self.play(FadeIn(hero), run_time=0.9)

        # Phase 2: title stack (kicker → title → accent → sub)
        self.play(FadeIn(kicker, shift=DOWN * 0.1), run_time=0.3)
        self.play(FadeIn(title_lines, shift=UP * 0.15), run_time=0.6)
        self.play(GrowFromEdge(accent, LEFT), run_time=0.3)
        self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)

        # Phase 3: Ken Burns + hold
        self.play(hero.animate.scale(1.05 / 0.95).shift(LEFT * 0.15),
                  rate_func=linear, run_time=1.8)

        # Phase 4: fade out
        self.wait(0.8)
        self.play(FadeOut(hero), FadeOut(title_stack), run_time=0.5)
        self.advance_progress(5.6)

    # ============================================================
    # ACT 1 — spawn (35s)
    # ============================================================
    def scene_act1(self):
        act_badge = self._make_act_badge("ACT 1")
        # Bundle badge + subtitle so transition from scenario lands tighter
        self.show_subtitle("Node.js (Parent) × Python (Child)")
        self.play(FadeIn(act_badge), run_time=0.3)
        self.wait(1.5)

        # Beat 1.2 — spawn + stdio pipe (15s)
        # Boxes aligned to same y so pipe is horizontal, not slanting down
        self.parent_box = self.make_process_box(
            "Parent Process", "Node.js", BLUE, LEFT * 5.3 + UP * 0.8)
        self.child_box = self.make_process_box(
            "Child Process", "Python MCP Server", TEAL, RIGHT * 5.3 + UP * 0.8)

        spawn_call = Text("▶ 開出 Child",
                          font=CN_FONT, font_size=22,
                          color=ORANGE, weight=BOLD).move_to(UP * 3.2)

        self.play(FadeIn(self.parent_box, shift=RIGHT * 0.3), run_time=0.6)

        # Sonnet badge — visual bridge from scenario LLM box to parent_box
        # (violet — LLM main-subject color, aligned across all 3 videos)
        self.sonnet_badge = self._make_pill("LLM · Sonnet", VIOLET, size=13)
        self.sonnet_badge.scale(0.80)
        self.sonnet_badge.move_to(
            self.parent_box.get_corner(DR) + LEFT * 1.00 + UP * 0.32
        )
        self.sonnet_badge.set_z_index(20)
        self.play(FadeIn(self.sonnet_badge, scale=0.7), run_time=0.5)
        self.show_subtitle("Parent 裡跑著剛剛那個 LLM (Sonnet)")
        self.wait(3.0)

        self.play(FadeIn(spawn_call, shift=DOWN * 0.2), run_time=0.4)
        self.show_subtitle("Parent 開出一個 Child")
        self.wait(2.0)

        # child box appears
        self.play(FadeIn(self.child_box, shift=LEFT * 0.3), run_time=0.6)

        # Two parallel pipes — bidirectional channel, no jargon labels
        self.pipe_top = Line(
            start=self.parent_box.get_right() + RIGHT * 0.15 + UP * 0.3,
            end=self.child_box.get_left() + LEFT * 0.15 + UP * 0.3,
            color=NEUTRAL, stroke_width=2.5,
        )
        self.pipe_bot = Line(
            start=self.parent_box.get_right() + RIGHT * 0.15 + DOWN * 0.3,
            end=self.child_box.get_left() + LEFT * 0.15 + DOWN * 0.3,
            color=NEUTRAL, stroke_width=2.5,
        )

        self.play(Create(self.pipe_top), Create(self.pipe_bot), run_time=0.7)
        self.show_subtitle("兩條管道 → Parent ⇄ Child 可以雙向講話")
        self.wait(5.0)

        # cleanup act 1 visuals, keep parent/child + pipes + sonnet badge for act 2/3
        self.play(
            FadeOut(spawn_call),
            run_time=0.5,
        )
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=0.3)
            self._cur_subtitle = None
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(30)

    # ============================================================
    # ACT 2 — handshake (75s)
    # ============================================================
    def scene_act2(self):
        act_badge = self._make_act_badge("ACT 2")
        self.play(FadeIn(act_badge), run_time=0.3)

        # State panel — handshake progress as two checkboxes
        state_box = RoundedRectangle(width=3.5, height=1.05, corner_radius=0.12,
                                     stroke_color=DIM, stroke_width=1.5,
                                     fill_color=BG, fill_opacity=0.7)
        state_box.move_to(LEFT * 3.2 + DOWN * 2.6)

        def _make_checkbox():
            return Square(side_length=0.32, stroke_color=DIM, stroke_width=2,
                          fill_opacity=0)

        ready_box = _make_checkbox()
        ready_lbl = Text("打過招呼", font=CN_FONT, font_size=20,
                        color=NEUTRAL)
        ready_row = VGroup(ready_box, ready_lbl).arrange(RIGHT, buff=0.25)

        conn_box = _make_checkbox()
        conn_lbl = Text("拿到工具清單", font=CN_FONT, font_size=20,
                       color=NEUTRAL)
        conn_row = VGroup(conn_box, conn_lbl).arrange(RIGHT, buff=0.25)

        inner = VGroup(ready_row, conn_row).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT
        )
        inner.move_to(state_box.get_center())

        self.state_panel = VGroup(state_box, ready_row, conn_row)
        self.state_ready_box = ready_box
        self.state_ready_lbl = ready_lbl
        self.state_conn_box = conn_box
        self.state_conn_lbl = conn_lbl

        self.play(FadeIn(self.state_panel), run_time=0.5)
        self.wait(0.3)

        # === Beat 2.1 — send initialize (id:1) ===
        self.show_subtitle("Parent 先送一個「我來了」")

        arrow_init = self.message_arrow('right', ORANGE, y_offset=0.0)
        self.play(GrowArrow(arrow_init), run_time=0.5)

        init_pill = self._make_pill("initialize · id:1", ORANGE)
        init_pill.move_to(self.parent_box.get_right() + RIGHT * 0.55)
        self.play(FadeIn(init_pill, scale=0.6), run_time=0.4)
        self.wait(2.5)
        self.play(
            init_pill.animate.move_to(self.child_box.get_left() + LEFT * 0.55),
            run_time=1.4,
        )
        self.wait(3.0)
        self.play(FadeOut(init_pill), run_time=0.3)
        self.wait(1.5)

        # === Beat 2.2 — child responds ===
        self.show_subtitle("Child 回說「我能做什麼」")

        arrow_cap = self.message_arrow('left', GREEN, y_offset=-1.4)
        self.play(GrowArrow(arrow_cap), run_time=0.5)

        cap_pill = self._make_pill("能力清單 · ok", GREEN)
        cap_pill.move_to(self.child_box.get_left() + LEFT * 0.55 + DOWN * 1.4)
        self.play(FadeIn(cap_pill, scale=0.6), run_time=0.4)
        self.play(
            cap_pill.animate.move_to(
                self.parent_box.get_right() + RIGHT * 0.55 + DOWN * 1.4
            ),
            run_time=1.4,
        )
        self.wait(1.5)
        self.play(FadeOut(cap_pill), run_time=0.3)

        # Check the first checkbox (打過招呼 ✓)
        self.ready_check = Text("✓", font=MONO_FONT, font_size=26,
                                color=INK, weight=BOLD)
        self.ready_check.move_to(self.state_ready_box.get_center())
        self.play(
            self.state_ready_box.animate.set_stroke(
                GREEN, width=2
            ).set_fill(GREEN, opacity=0.7),
            self.state_ready_lbl.animate.set_color(GREEN),
            FadeIn(self.ready_check, scale=0.6),
            run_time=0.6,
        )

        # Highlight that second step is still pending
        note = Text("還沒拿到工具清單 → LLM 不知道能用哪些工具",
                    font=CN_FONT, font_size=20, color=RED,
                    weight=BOLD).next_to(state_box, RIGHT, buff=0.4)
        self.play(FadeIn(note, shift=LEFT * 0.2), run_time=0.5)
        self.wait(4.0)

        # cleanup snippets before beat 2.3
        self.play(FadeOut(arrow_init), FadeOut(arrow_cap),
                  FadeOut(note),
                  run_time=0.5)

        # === Beat 2.3 — notify + tools/list (3 arrows shown SEQUENTIALLY) ===

        # 1. notify arrow (grey)
        self.show_subtitle("先告知已就緒")
        arrow_notify = self.message_arrow('right', NEUTRAL, y_offset=0.0)
        notify_lbl = Text("告知已就緒", font=CN_FONT, font_size=22,
                          color=NEUTRAL).next_to(arrow_notify, UP, buff=0.15)
        self.play(GrowArrow(arrow_notify), FadeIn(notify_lbl), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(arrow_notify), FadeOut(notify_lbl), run_time=0.4)

        # 2. ask for tools (orange)
        self.show_subtitle("再問 Child 有哪些工具")
        arrow_tl = self.message_arrow('right', ORANGE, y_offset=0.0)
        ask_lbl = Text("要工具清單", font=CN_FONT, font_size=22,
                       color=ORANGE,
                       weight=BOLD).next_to(arrow_tl, UP, buff=0.15)
        self.play(GrowArrow(arrow_tl), FadeIn(ask_lbl), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(arrow_tl), FadeOut(ask_lbl), run_time=0.4)

        # 3. response: green arrow + 8 dots flying back to parent
        # Update subtitle so it matches what's now on screen (was previously
        # stuck on "再問 Child 有哪些工具" while the response was already playing).
        self.show_subtitle("Child 回傳工具清單")
        arrow_tl_res = self.message_arrow('left', GREEN, y_offset=0.0)
        self.play(GrowArrow(arrow_tl_res), run_time=0.5)

        start_pos = self.child_box.get_left() + LEFT * 0.3
        tool_dots = VGroup()
        for _ in range(8):
            d = Dot(radius=0.10, color=GREEN, fill_opacity=0.9,
                    stroke_width=0)
            d.move_to(start_pos)
            tool_dots.add(d)

        target_y = self.parent_box.get_top()[1] + 0.6
        target_x_left = self.parent_box.get_left()[0] + 0.3
        target_x_right = self.parent_box.get_right()[0] - 0.3
        target_xs = np.linspace(target_x_left, target_x_right, 8)

        self.play(FadeIn(tool_dots, scale=0.5), run_time=0.4)
        move_anims = [
            d.animate.move_to(np.array([target_xs[i], target_y, 0]))
            for i, d in enumerate(tool_dots)
        ]
        self.play(LaggedStart(*move_anims, lag_ratio=0.12), run_time=1.8)

        count_lbl = Text("tools: 8", font=MONO_FONT, font_size=22,
                         color=GREEN, weight=BOLD)
        count_lbl.next_to(tool_dots, UP, buff=0.18)
        self.play(FadeIn(count_lbl, shift=DOWN * 0.1), run_time=0.4)
        self.wait(1.5)

        # Check the second checkbox (拿到工具清單 ✓)
        self.show_subtitle("收到工具清單後 → 才算真正連上")
        self.conn_check = Text("✓", font=MONO_FONT, font_size=26,
                               color=INK, weight=BOLD)
        self.conn_check.move_to(self.state_conn_box.get_center())
        self.play(
            self.state_conn_box.animate.set_stroke(
                GREEN, width=2
            ).set_fill(GREEN, opacity=0.7),
            self.state_conn_lbl.animate.set_color(GREEN),
            FadeIn(self.conn_check, scale=0.6),
            run_time=0.6,
        )
        self.wait(6.5)

        # cleanup act 2 (notify/tl arrows already faded above)
        self.play(FadeOut(arrow_tl_res),
                  FadeOut(tool_dots), FadeOut(count_lbl),
                  run_time=0.5)
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(78)

    # ============================================================
    # ACT 3 — tool call (55s)
    # ============================================================
    def scene_act3(self):
        act_badge = self._make_act_badge("ACT 3")
        self.play(FadeIn(act_badge), run_time=0.3)

        # === Beat 3.1 — LLM 決定呼叫 + 等候名單 ===
        self.show_subtitle("Sonnet 決定呼叫工具")

        # Token inside parent representing the function call concept
        call_pill = self._make_pill('search_new_books("新書")', ORANGE)
        call_pill.move_to(self.parent_box.get_center())
        self.play(FadeIn(call_pill, scale=0.7), run_time=0.5)
        # Lift further above Parent box so the pill doesn't graze the box header
        self.play(call_pill.animate.shift(UP * 1.5), run_time=0.4)
        self.wait(2.5)

        # 等候名單 icon — yellow, with id and timeout
        self.show_subtitle("Parent 記下這個請求，等 Child 回應")
        wait_box = RoundedRectangle(
            width=4.0, height=0.65, corner_radius=0.14,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.20,
        )
        wait_lbl = Text("等候 search_new_books 回應 · 30s 內", font=CN_FONT,
                        font_size=18, color=ORANGE, weight=BOLD)
        wait_lbl.move_to(wait_box.get_center())
        wait_group = VGroup(wait_box, wait_lbl)
        # aligned_edge + right shift keeps the group inside the frame.
        # buff bumped 0.3 → 1.0 so wait_group sits well below the message
        # arrow track (cap_pill / result_pill at DOWN*1.4 from box edge);
        # earlier buff=0.3 caused result_pill on its way back to collide with
        # the wait_box at the same y level.
        wait_group.next_to(self.parent_box, DOWN, buff=1.0, aligned_edge=LEFT)
        wait_group.shift(RIGHT * 0.5)
        self.play(FadeIn(wait_group, shift=UP * 0.15), run_time=0.5)
        self.wait(2.0)

        # arrow + token flies along it to child
        arrow_call = self.message_arrow('right', ORANGE, y_offset=0.0)
        self.play(GrowArrow(arrow_call), run_time=0.4)
        self.play(
            call_pill.animate.move_to(
                self.child_box.get_center() + UP * 1.15
            ),
            run_time=1.4,
        )
        self.wait(2.0)
        self.play(FadeOut(call_pill), run_time=0.3)

        # === Beat 3.2 — child returns, waiting list resolves ===
        self.show_subtitle("Child 執行完 → 回傳結果")

        arrow_res = self.message_arrow('left', GREEN, y_offset=-1.4)
        self.play(GrowArrow(arrow_res), run_time=0.4)

        result_pill = self._make_pill("結果 · 10 筆新書", GREEN)
        result_pill.move_to(
            self.child_box.get_left() + LEFT * 0.55 + DOWN * 1.4
        )
        self.play(FadeIn(result_pill, scale=0.7), run_time=0.4)
        self.play(
            result_pill.animate.move_to(
                self.parent_box.get_right() + RIGHT * 0.55 + DOWN * 1.4
            ),
            run_time=1.4,
        )
        self.wait(1.5)

        # 等候名單 yellow → green ✓
        self.show_subtitle("找到對應的請求 → 把結果回給使用者")
        done_box = RoundedRectangle(
            width=4.0, height=0.65, corner_radius=0.14,
            stroke_color=GREEN, stroke_width=2,
            fill_color=GREEN, fill_opacity=0.20,
        )
        done_lbl = Text("search_new_books ✓ 回應完成", font=CN_FONT,
                        font_size=18, color=GREEN, weight=BOLD)
        done_lbl.move_to(done_box.get_center())
        done_group = VGroup(done_box, done_lbl)
        done_group.move_to(wait_group.get_center())
        self.play(ReplacementTransform(wait_group, done_group), run_time=0.6)
        self.wait(3.0)

        # cleanup before beat 3.3
        self.play(FadeOut(result_pill), FadeOut(done_group),
                  FadeOut(arrow_call), FadeOut(arrow_res),
                  run_time=0.5)

        # === Beat 3.3 — recap (15s) ===
        self.show_subtitle("整個流程：管道 + 訊息往返")
        flow_text = VGroup(
            Text("開 Child", font=CN_FONT, font_size=30, color=BLUE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("打招呼", font=CN_FONT, font_size=30, color=ORANGE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("拿工具", font=CN_FONT, font_size=30, color=ORANGE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("呼叫工具", font=CN_FONT, font_size=30, color=GREEN,
                 weight=BOLD),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.8)
        self.play(FadeIn(flow_text, shift=DOWN * 0.2), run_time=0.7)
        self.wait(13.0)

        # cleanup act 3 (and persistent visuals)
        cleanup = [self.parent_box, self.child_box, self.pipe_top, self.pipe_bot,
                   self.state_panel, self.ready_check, self.conn_check,
                   self.sonnet_badge, flow_text, act_badge]
        if self._cur_subtitle is not None:
            cleanup.append(self._cur_subtitle)
            self._cur_subtitle = None
        self.play(*[FadeOut(m) for m in cleanup], run_time=0.7)
        self.advance_progress(110)

    # ============================================================
    # OUTRO — frame closure + three things + closing card
    # ============================================================
    def scene_outro(self):
        # ----- Frame closure (~6s): close the loop started in scene_scenario
        closure_title = Text("剛剛使用者問的「新書」呢？",
                             font=CN_FONT, font_size=34,
                             color=ORANGE, weight=BOLD).move_to(UP * 2.5)

        chain_q = self._make_pill("查新書", BLUE)
        chain_arrow1 = Text("→", font=MONO_FONT, font_size=32, color=NEUTRAL)
        chain_child = self._make_pill("Child 執行", TEAL)
        chain_arrow2 = Text("→", font=MONO_FONT, font_size=32, color=NEUTRAL)
        chain_result = self._make_pill("10 筆新書", GREEN)
        chain_arrow3 = Text("→", font=MONO_FONT, font_size=32, color=NEUTRAL)
        chain_back = self._make_pill("使用者", BLUE)

        journey = VGroup(
            chain_q, chain_arrow1, chain_child, chain_arrow2,
            chain_result, chain_arrow3, chain_back,
        ).arrange(RIGHT, buff=0.28).move_to(UP * 0.5)

        self.play(FadeIn(closure_title, shift=DOWN * 0.2), run_time=0.6)
        for elem in journey:
            self.play(FadeIn(elem, shift=LEFT * 0.15), run_time=0.30)
        self.wait(2.0)
        self.play(FadeOut(closure_title), FadeOut(journey), run_time=0.5)

        # ----- Recap (~12s): MCP 握手三件事
        outro_title = Text("MCP 握手三件事",
                           font=CN_FONT, font_size=42,
                           color=INK, weight=BOLD).move_to(UP * 3.0)

        def make_point(num_str, label_str, content_str, content_color=ORANGE):
            num = Text(num_str, font=MONO_FONT, font_size=56,
                       color=BLUE, weight=BOLD)
            label = Text(label_str, font=CN_FONT, font_size=30,
                         color=INK, weight=BOLD)
            content = Text(content_str, font=CN_FONT, font_size=26,
                           color=content_color, weight=BOLD)
            return VGroup(num, label, content).arrange(RIGHT, buff=0.5)

        points = VGroup(
            make_point("①", "通訊管道",
                       "Parent 開出 Child + 雙向通訊管道"),
            make_point("②", "兩階段握手",
                       "先互換能力，再拿到工具清單，才算真的連上"),
            make_point("③", "工具呼叫機制",
                       "Parent 記下請求，等 Child 回應"),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(DOWN * 0.3)

        self.play(FadeIn(outro_title, shift=DOWN * 0.2), run_time=0.6)
        self.wait(0.3)
        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(1.8)
        self.wait(2.0)
        self.play(FadeOut(outro_title), FadeOut(points), run_time=0.5)

        # ----- Closing card (~5s): mirrors intro, teases next episode
        close_title = Text("MCP 握手 ✓", font=SERIF_FONT, font_size=90,
                           color=INK, weight=BOLD).move_to(UP * 0.6)
        close_sub_line1 = Text("下集",
                               font=CN_FONT, font_size=24, color=NEUTRAL)
        close_sub_line2 = Text("LLM 怎麼自主決定該呼叫哪個工具",
                               font=CN_FONT, font_size=30,
                               color=INK, weight=MEDIUM)
        close_sub = VGroup(close_sub_line1, close_sub_line2).arrange(
            DOWN, buff=0.18
        ).move_to(DOWN * 1.0)
        close_accent = Line(start=LEFT * 1.5, end=RIGHT * 1.5,
                            color=ORANGE, stroke_width=3).move_to(DOWN * 0.2)

        self.play(FadeIn(close_title, shift=DOWN * 0.2), run_time=0.8)
        self.play(GrowFromCenter(close_accent), run_time=0.3)
        self.play(FadeIn(close_sub, shift=UP * 0.15), run_time=0.5)
        self.advance_progress(self.TOTAL_SECONDS)
        self.wait(2.8)
        self.play(FadeOut(close_title), FadeOut(close_sub),
                  FadeOut(close_accent), run_time=0.6)
        self.wait(0.4)
