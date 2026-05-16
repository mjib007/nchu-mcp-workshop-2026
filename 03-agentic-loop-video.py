"""
03-agentic-loop-video.py

~1:45 video visualizing multi-turn agentic tool loop for Segment 3.
Topic: LLM decides what to call, when to call, and when to stop —
across multiple iterations. Companion video to function-calling-video
(which covers a single tool call); this one stretches the same idea
across 3 rounds + maxIterations safety valve.

Six scenes:
  Intro:     magazine-cover (cli-coding-agent illustration + title)
  Scenario:  user asks a composite query
  Loop:      3-round walkthrough with chat-bubble stack growing
  MaxIter:   safety guard — maxIterations + forced final reply
  Takeaway:  3 cards summarizing agentic loop's contract
  Closing:   "Decide · Iterate · Closure" hero shot

Render:
  manim -ql --disable_caching 03-agentic-loop-video.py AgenticLoop
  manim -qh 03-agentic-loop-video.py AgenticLoop      # final 1080p60
"""

from manim import *
import numpy as np

# Violet-primary palette (matches V1 / V2 / V3 + slide deck)
BG            = "#0a0a10"
VIOLET        = "#7B5CF5"
VIOLET_DEEP   = "#5B3ED9"
VIOLET_SOFT   = "#9D85F7"
BLUE          = "#5B8DE8"
ORANGE        = "#FB7048"
TEAL          = "#0EA594"
TEAL_BRIGHT   = "#2DD4BF"
PINK          = "#EF4444"
GREEN         = "#5CB85C"
INK           = "#FFFFFF"
NEUTRAL       = "#B4BED2"
DIM           = "#3A4A6A"

CN_FONT     = "Noto Sans CJK TC"
SERIF_FONT  = "Noto Serif CJK TC"
MONO_FONT   = "DejaVu Sans Mono"

config.frame_width  = 16
config.frame_height = 9
config.pixel_width  = 1920
config.pixel_height = 1080


class AgenticLoop(Scene):
    SUBTITLE_MAX_WIDTH = 14.0
    TOTAL_SECONDS = 51.7   # measured: scenes ran tighter than the 105s estimate

    TITLE     = "Agentic Loop"
    SUBTITLE  = "LLM 多輪迭代怎麼運作"

    def construct(self):
        self.camera.background_color = BG
        self._cur_subtitle = None
        self._init_progress_bar()

        self.scene_intro()       # 0:00 – 0:05  magazine cover
        self.scene_scenario()    # 0:05 – 0:11  user query
        self.scene_loop()        # 0:11 – 0:36  3-round walkthrough
        self.scene_maxiter()     # 0:36 – 0:44  safety guard
        self.scene_takeaway()    # 0:44 – 0:50  3 insights
        self.scene_closing()     # 0:50 – 0:52  closing hero shot

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
            stroke_width=0, fill_color=VIOLET, fill_opacity=1.0
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
    # Subtitle helpers (sequential fade)
    # ============================================================
    def _build_subtitle(self, text):
        sub = Text(text, font=CN_FONT, font_size=28, color=INK, weight=MEDIUM)
        if sub.width > self.SUBTITLE_MAX_WIDTH:
            sub.scale_to_fit_width(self.SUBTITLE_MAX_WIDTH)
        sub.to_edge(DOWN, buff=0.7)
        return sub

    def show_subtitle(self, text, run_time=0.35):
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
    # Stage badge helper
    # ============================================================
    def _stage_badge(self, text, color=VIOLET):
        box = RoundedRectangle(width=2.2, height=0.48, corner_radius=0.09,
                               stroke_color=NEUTRAL, stroke_width=1.5,
                               fill_color=color, fill_opacity=0.0)
        lbl = Text(text, font=MONO_FONT, font_size=17,
                   color=color, weight=BOLD).move_to(box.get_center())
        badge = VGroup(box, lbl).move_to([6.7, 4.05, 0])
        badge.set_z_index(100)
        return badge

    # ============================================================
    # Pill helper
    # ============================================================
    def _pill(self, label, color, size=16, weight=BOLD):
        txt = Text(label, font=MONO_FONT, font_size=size,
                   color=INK, weight=weight)
        pad_w = txt.width + 0.4
        pad_h = txt.height + 0.22
        bg = RoundedRectangle(
            width=pad_w, height=pad_h, corner_radius=pad_h / 2,
            stroke_color=color, stroke_width=2.0,
            fill_color=color, fill_opacity=0.85,
        )
        txt.move_to(bg.get_center())
        return VGroup(bg, txt)

    # ============================================================
    # Chat bubble helper
    # ============================================================
    def _bubble(self, text, accent, fill_opacity=0.20, stroke_width=2,
                width=10.5, height=0.95, size=22):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.25,
            stroke_color=accent, stroke_width=stroke_width,
            fill_color=accent, fill_opacity=fill_opacity,
        )
        t = Text(text, font=CN_FONT, font_size=size,
                 color=INK).move_to(box.get_center())
        return VGroup(box, t)

    def _role_chip(self, text, color, width=1.6):
        chip = RoundedRectangle(
            width=width, height=0.45, corner_radius=0.22,
            stroke_color=color, stroke_width=0,
            fill_color=color, fill_opacity=1.0,
        )
        t = Text(text, font=MONO_FONT, font_size=15,
                 color=INK, weight=BOLD).move_to(chip.get_center())
        return VGroup(chip, t)

    # ============================================================
    # SCENE — INTRO (5s)
    # ============================================================
    def scene_intro(self):
        try:
            hero = SVGMobject(
                "intro-assets/undraw_cli-coding-agent.svg",
            ).scale_to_fit_height(5.6)
            hero.move_to(RIGHT * 3.6 + DOWN * 0.1)
        except Exception:
            hero = VGroup()

        title_lines = VGroup(
            Text("Agentic", font=SERIF_FONT, font_size=88,
                 color=INK, weight=BOLD),
            Text("Loop", font=SERIF_FONT, font_size=88,
                 color=INK, weight=BOLD),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        kicker = Text("章節 03", font=MONO_FONT, font_size=18,
                      color=VIOLET, weight=BOLD).next_to(
                          title_lines, UP, buff=0.30, aligned_edge=LEFT)
        accent = Line(start=LEFT * 0.0, end=RIGHT * 1.8,
                      color=VIOLET, stroke_width=5).next_to(
                          title_lines, DOWN, buff=0.30, aligned_edge=LEFT)
        sub = Text("LLM 多輪迭代怎麼運作\n自己決定何時呼叫工具",
                   font=CN_FONT, font_size=24, color=NEUTRAL,
                   line_spacing=1.15).next_to(
                       accent, DOWN, buff=0.30, aligned_edge=LEFT)
        title_stack = VGroup(kicker, title_lines, accent, sub).move_to(
            LEFT * 4.2 + UP * 0.1)

        if isinstance(hero, SVGMobject):
            hero.scale(0.95)
            self.play(FadeIn(hero), run_time=0.9)
        self.play(FadeIn(kicker, shift=DOWN * 0.1), run_time=0.3)
        self.play(FadeIn(title_lines, shift=UP * 0.15), run_time=0.6)
        self.play(GrowFromEdge(accent, LEFT), run_time=0.3)
        self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)

        if isinstance(hero, SVGMobject):
            self.play(hero.animate.scale(1.05 / 0.95).shift(LEFT * 0.15),
                      rate_func=linear, run_time=1.4)
        self.wait(0.8)

        cleanups = [title_stack]
        if isinstance(hero, SVGMobject):
            cleanups.append(hero)
        self.play(*[FadeOut(m) for m in cleanups], run_time=0.4)
        self.advance_progress(5.6)

    # ============================================================
    # SCENE — SCENARIO (9s)
    # ============================================================
    def scene_scenario(self):
        self.show_subtitle("從一個複合請求開始")

        u_chip = self._role_chip("user", BLUE)
        # Bubble width unified with the assistant/tool_result bubbles below
        # so the loop section reads as a consistent chat thread, not a mix
        # of wide top + narrow rows.
        u_bub = self._bubble(
            "「我下學期能修哪些 AI 課?這些老師最近有什麼論文?」",
            BLUE, fill_opacity=0.32, width=11.5, height=1.0, size=22,
        )
        u_chip.move_to(LEFT * 6.5 + UP * 1.5)
        u_bub.move_to(RIGHT * 0.4 + UP * 1.5)

        self.play(FadeIn(u_chip, shift=RIGHT * 0.15),
                  FadeIn(u_bub, shift=DOWN * 0.15),
                  run_time=0.6)
        self.wait(1.2)

        complexity = Text("→ single-turn 解不了:得分兩步驟",
                          font=CN_FONT, font_size=20,
                          color=ORANGE, weight=BOLD).move_to(DOWN * 0.5)
        self.play(FadeIn(complexity, shift=UP * 0.15), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(complexity), run_time=0.4)
        self.user_chip = u_chip
        self.user_bub = u_bub
        self.advance_progress(11)

    # ============================================================
    # SCENE — LOOP (~65s) — 3 rounds, chat bubbles accumulate
    # ============================================================
    def scene_loop(self):
        badge = self._stage_badge("THE LOOP", VIOLET)
        self.play(FadeIn(badge), run_time=0.3)

        # Shift user bubble up to make room for the loop stack
        # (lighter scale so user bubble stays a similar width to assistant/result)
        self.play(self.user_chip.animate.scale(0.75).move_to(LEFT * 6.5 + UP * 3.3),
                  self.user_bub.animate.scale(0.85).move_to(RIGHT * 0.4 + UP * 3.3),
                  run_time=0.5)

        # ----- Round 1: assistant decides + tool_use ---------------
        self.show_subtitle("Round 1 · LLM 拆解 → 第一個工具")

        # Round 1 label on left edge, shared by assistant + tool_result rows
        r1_label = Text("Round 1", font=MONO_FONT, font_size=15,
                        color=VIOLET_SOFT, weight=BOLD).move_to(
                            LEFT * 7.4 + UP * 1.2)

        r1_assistant_chip = self._role_chip("assistant", VIOLET)
        r1_assistant_bub = self._bubble(
            "「先查 AI 課程」", VIOLET, fill_opacity=0.18,
            width=11.5, height=0.85, size=20,
        )
        r1_assistant_chip.move_to(LEFT * 6.5 + UP * 2.0)
        r1_assistant_bub.move_to(RIGHT * 0.4 + UP * 2.0)
        self.play(FadeIn(r1_label), run_time=0.25)

        r1_tool_use = RoundedRectangle(
            width=2.4, height=0.40, corner_radius=0.20,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.30,
        )
        r1_tool_use_text = Text("+ tool_use", font=MONO_FONT, font_size=13,
                                color=ORANGE, weight=BOLD).move_to(
                                    r1_tool_use.get_center())
        # Place badge fully INSIDE the bubble, vertically centered, near
        # right edge — avoids the "sticker glued onto corner" look that
        # clipped the bubble's rounded corner outline.
        r1_tool_badge = VGroup(r1_tool_use, r1_tool_use_text).move_to(
            r1_assistant_bub.get_right() + LEFT * 1.35
        )

        self.play(FadeIn(r1_assistant_chip, shift=RIGHT * 0.15),
                  FadeIn(r1_assistant_bub, shift=DOWN * 0.15),
                  run_time=0.4)
        self.play(FadeIn(r1_tool_badge, shift=LEFT * 0.10), run_time=0.3)

        r1_tool_call = Text('search_courses(keyword="AI")',
                            font=MONO_FONT, font_size=20,
                            color=ORANGE, weight=BOLD).move_to(UP * 1.1)
        self.play(FadeIn(r1_tool_call, shift=UP * 0.15), run_time=0.5)
        self.wait(1.2)

        # ----- Round 1 result back ---------------------------------
        self.show_subtitle("Round 1 · 結果回來:5 門課、5 位老師")

        r1_result_chip = self._role_chip("tool_result", TEAL_BRIGHT, width=1.8)
        r1_result_bub = self._bubble(
            "5 門 AI 課,老師:張、李、范、林、王",
            TEAL_BRIGHT, fill_opacity=0.18,
            width=11.5, height=0.85, size=20,
        )
        r1_result_chip.move_to(LEFT * 6.4 + UP * 0.4)
        r1_result_bub.move_to(RIGHT * 0.4 + UP * 0.4)

        self.play(FadeOut(r1_tool_call), run_time=0.3)
        self.play(FadeIn(r1_result_chip, shift=RIGHT * 0.15),
                  FadeIn(r1_result_bub, shift=DOWN * 0.15),
                  run_time=0.5)
        self.wait(1.8)

        # ----- Round 2: LLM sees results, parallel tool_use --------
        self.show_subtitle("Round 2 · LLM 看清單 → 5 次 parallel tool call")

        r2_label = Text("Round 2", font=MONO_FONT, font_size=15,
                        color=VIOLET_SOFT, weight=BOLD).move_to(
                            LEFT * 7.4 + DOWN * 1.8)

        r2_assistant_chip = self._role_chip("assistant", VIOLET)
        r2_assistant_bub = self._bubble(
            "「查每位老師最近論文」", VIOLET, fill_opacity=0.18,
            width=11.5, height=0.85, size=20,
        )
        r2_assistant_chip.move_to(LEFT * 6.5 + DOWN * 1.1)
        r2_assistant_bub.move_to(RIGHT * 0.4 + DOWN * 1.1)
        self.play(FadeIn(r2_label), run_time=0.25)

        r2_tool_use = RoundedRectangle(
            width=3.0, height=0.40, corner_radius=0.20,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.30,
        )
        r2_tool_use_text = Text("+ 5× tool_use", font=MONO_FONT, font_size=13,
                                color=ORANGE, weight=BOLD).move_to(
                                    r2_tool_use.get_center())
        r2_tool_badge = VGroup(r2_tool_use, r2_tool_use_text).move_to(
            r2_assistant_bub.get_right() + LEFT * 1.65
        )

        self.play(FadeIn(r2_assistant_chip, shift=RIGHT * 0.15),
                  FadeIn(r2_assistant_bub, shift=DOWN * 0.15),
                  run_time=0.4)
        self.play(FadeIn(r2_tool_badge, shift=LEFT * 0.10), run_time=0.3)

        parallel_chips = VGroup()
        names = ["arxiv(張)", "arxiv(李)", "arxiv(范)", "arxiv(林)", "arxiv(王)"]
        for i, n in enumerate(names):
            ch = self._pill(n, ORANGE, size=13)
            ch.scale(0.85)
            x = -5.6 + i * 2.85
            ch.move_to([x, -2.15, 0])
            parallel_chips.add(ch)
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in parallel_chips],
                              lag_ratio=0.10, run_time=0.9))
        self.wait(0.6)

        parallel_note = Text("(同時呼叫 → 1 秒搞定 5 個查詢)",
                             font=CN_FONT, font_size=18, color=GREEN,
                             weight=BOLD).move_to(DOWN * 2.85)
        self.play(FadeIn(parallel_note, shift=UP * 0.15), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(parallel_chips), FadeOut(parallel_note), run_time=0.4)

        r2_result_chip = self._role_chip("tool_result × 5", TEAL_BRIGHT, width=2.4)
        r2_result_bub = self._bubble(
            "5 位老師最近論文清單(各 3-5 篇)",
            TEAL_BRIGHT, fill_opacity=0.18,
            width=11.5, height=0.85, size=20,
        )
        r2_result_chip.move_to(LEFT * 6.2 + DOWN * 2.4)
        r2_result_bub.move_to(RIGHT * 0.4 + DOWN * 2.4)
        self.play(FadeIn(r2_result_chip, shift=RIGHT * 0.15),
                  FadeIn(r2_result_bub, shift=DOWN * 0.15),
                  run_time=0.5)
        self.wait(2.0)

        # ----- Round 3: integrate + end_turn -----------------------
        loop_so_far = VGroup(
            r1_label, r2_label,
            r1_assistant_chip, r1_assistant_bub, r1_tool_badge,
            r1_result_chip, r1_result_bub,
            r2_assistant_chip, r2_assistant_bub, r2_tool_badge,
            r2_result_chip, r2_result_bub,
        )
        self.play(loop_so_far.animate.set_opacity(0.18), run_time=0.5)
        self.show_subtitle("Round 3 · LLM 整合 5 個結果 → 最終回覆")

        final_chip = self._role_chip("assistant", VIOLET)
        final_bub = self._bubble(
            "「你下學期可修這 5 門,范教授論文最對胃口…」",
            VIOLET, fill_opacity=0.42, stroke_width=3,
            width=12.0, height=1.0, size=22,
        )
        final_chip.move_to(LEFT * 6.0 + DOWN * 0.3)
        final_bub.move_to(RIGHT * 0.6 + DOWN * 0.3)

        end_turn_box = RoundedRectangle(
            width=2.0, height=0.42, corner_radius=0.20,
            stroke_color=GREEN, stroke_width=0,
            fill_color=GREEN, fill_opacity=1.0,
        )
        end_turn_text = Text("✓ end_turn", font=MONO_FONT, font_size=14,
                             color=BG, weight=BOLD).move_to(end_turn_box.get_center())
        end_turn_chip = VGroup(end_turn_box, end_turn_text).move_to(
            final_bub.get_right() + LEFT * 1.15
        )

        self.play(FadeIn(final_chip, shift=RIGHT * 0.15),
                  FadeIn(final_bub, shift=DOWN * 0.15),
                  run_time=0.6)
        self.play(FadeIn(end_turn_chip, shift=LEFT * 0.10), run_time=0.4)
        self.play(Indicate(end_turn_chip, scale_factor=1.25, color=GREEN),
                  run_time=0.7)
        self.wait(2.0)

        cleanups = [
            self.user_chip, self.user_bub,
            loop_so_far,
            final_chip, final_bub, end_turn_chip,
            badge,
        ]
        self.play(*[FadeOut(m) for m in cleanups], run_time=0.5)
        self.clear_subtitle(run_time=0.3)
        self.advance_progress(36)

    # ============================================================
    # SCENE — MAXITER (12s)
    # ============================================================
    def scene_maxiter(self):
        badge = self._stage_badge("SAFETY", ORANGE)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("如果 loop 跑到失控怎麼辦?")

        circles = VGroup()
        for i in range(8):
            c = Circle(radius=0.30, color=ORANGE, fill_opacity=0.25,
                       stroke_width=2)
            x = -5.6 + i * 1.6
            c.move_to([x, 0.5, 0])
            lbl = Text(str(i + 1), font=MONO_FONT, font_size=18,
                       color=ORANGE, weight=BOLD).move_to(c.get_center())
            circles.add(VGroup(c, lbl))
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in circles],
                              lag_ratio=0.08, run_time=1.2))

        x_mark = Cross(stroke_color=PINK, stroke_width=8).scale(0.45).move_to(
            circles[7].get_center())
        self.play(Write(x_mark), run_time=0.4)
        forced_lbl = Text("第 7 輪強制 tool_choice=none",
                          font=CN_FONT, font_size=18, color=TEAL_BRIGHT,
                          weight=BOLD).next_to(circles[6], DOWN, buff=0.5)
        self.play(FadeIn(forced_lbl, shift=UP * 0.1), run_time=0.5)
        self.wait(1.2)

        max_label = Text("maxIterations = 7", font=MONO_FONT, font_size=28,
                         color=ORANGE, weight=BOLD).move_to(UP * 2.0)
        self.play(Write(max_label), run_time=0.6)
        self.wait(2.5)

        cleanup = VGroup(circles, x_mark, forced_lbl, max_label, badge)
        self.play(FadeOut(cleanup), run_time=0.5)
        self.clear_subtitle(run_time=0.3)
        self.advance_progress(44)

    # ============================================================
    # SCENE — TAKEAWAY (12s)
    # ============================================================
    def scene_takeaway(self):
        outro_title = Text("Agentic Loop = 三件事",
                           font=CN_FONT, font_size=42,
                           color=INK, weight=BOLD).move_to(UP * 3.0)

        cards_data = [
            ("①", "Decide", "拆解問題 + 選 tool",
             "LLM 自己決定要不要、要呼叫哪個", VIOLET),
            ("②", "Iterate", "多輪迭代 + 結果驅動",
             "看 tool_result 再決定下一輪", ORANGE),
            ("③", "Closure", "end_turn / maxIterations",
             "loop 一定收得回來,不無限跑", TEAL_BRIGHT),
        ]

        card_w = 4.4
        cards = VGroup()
        for i, (num, eng, cn, desc, color) in enumerate(cards_data):
            x = -4.6 + i * 4.6
            box = RoundedRectangle(width=card_w, height=4.0, corner_radius=0.22,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=color, fill_opacity=0.12)
            box.move_to([x, -0.3, 0])

            num_text = Text(num, font=MONO_FONT, font_size=48,
                            color=color, weight=BOLD).move_to(
                                box.get_top() + DOWN * 0.7)
            eng_text = Text(eng, font=SERIF_FONT, font_size=32,
                            color=INK, weight=BOLD).move_to(
                                box.get_top() + DOWN * 1.5)
            cn_text = Text(cn, font=CN_FONT, font_size=17,
                           color=color, weight=BOLD).move_to(
                               box.get_top() + DOWN * 2.2)
            desc_text = Text(desc, font=CN_FONT, font_size=15,
                             color=INK).move_to(
                                 box.get_top() + DOWN * 3.0)
            card = VGroup(box, num_text, eng_text, cn_text, desc_text)
            cards.add(card)

        self.play(FadeIn(outro_title, shift=DOWN * 0.2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards],
                              lag_ratio=0.25, run_time=1.4))
        self.wait(6.5)

        self.play(FadeOut(outro_title), FadeOut(cards), run_time=0.5)
        self.advance_progress(50)

    # ============================================================
    # SCENE — CLOSING (5s)
    # ============================================================
    def scene_closing(self):
        hero = Text("Decide  ·  Iterate  ·  Closure",
                    font=SERIF_FONT, font_size=66,
                    color=INK, weight=BOLD).move_to(UP * 0.5)
        accent = Line(start=LEFT * 3.5, end=RIGHT * 3.5,
                      color=VIOLET, stroke_width=5).move_to(DOWN * 0.5)
        sub = Text("Agentic Loop 的契約",
                   font=CN_FONT, font_size=30, color=VIOLET_SOFT,
                   weight=MEDIUM).move_to(DOWN * 1.2)

        self.play(FadeIn(hero, shift=DOWN * 0.2), run_time=0.7)
        self.play(GrowFromCenter(accent), run_time=0.3)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.4)
        self.wait(2.5)
        self.play(FadeOut(hero), FadeOut(accent), FadeOut(sub), run_time=0.5)
        self.advance_progress(self.TOTAL_SECONDS)
        self.wait(0.3)
