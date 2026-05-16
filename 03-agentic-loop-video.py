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
    TOTAL_SECONDS = 67.5   # D-plan measured (after #1 #2 #3 polish)

    TITLE     = "Agentic Loop"
    SUBTITLE  = "LLM 多輪迭代怎麼運作"

    def construct(self):
        self.camera.background_color = BG
        self._cur_subtitle = None
        self._init_progress_bar()

        self.scene_intro()             # 0:00 – 0:05  magazine cover
        self.scene_single_turn_pain()  # 0:05 – 0:13  why agentic — single-turn fails
        self.scene_scenario()          # 0:13 – 0:19  pivot to multi-turn
        self.scene_loop()              # 0:19 – 0:46  3-round walkthrough + stop_reason
        self.scene_maxiter()           # 0:46 – 0:55  safety guard
        self.scene_recap()             # 0:55 – 1:00  compressed loop replay
        self.scene_takeaway()          # 1:00 – 1:15  3 insights (longer dwell)
        self.scene_closing()           # 1:15 – 1:18  closing hero shot

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
    # SCENE — SINGLE-TURN PAIN (8s) — motivates why we need a loop
    # ============================================================
    def scene_single_turn_pain(self):
        """Demo what single-turn Function Calling does on a composite query:
        fires one tool, answers half the question, hits a dead end."""
        badge = self._stage_badge("SINGLE-TURN", PINK)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("如果只用單輪 Function Calling …")

        # User query (smaller, top)
        u_chip = self._role_chip("user", BLUE, width=1.4).scale(0.85)
        u_bub = self._bubble(
            "「下學期能修哪些 AI 課?這些老師最近有什麼論文?」",
            BLUE, fill_opacity=0.30, width=11.0, height=0.90, size=20,
        )
        u_chip.move_to(LEFT * 6.5 + UP * 2.5)
        u_bub.move_to(RIGHT * 0.4 + UP * 2.5)
        self.play(FadeIn(u_chip), FadeIn(u_bub, shift=DOWN * 0.1),
                  run_time=0.5)

        # Single tool fires
        a_chip = self._role_chip("assistant", VIOLET).scale(0.85)
        a_bub = self._bubble(
            "「先查 AI 課程…」", VIOLET, fill_opacity=0.18,
            width=11.0, height=0.78, size=18,
        )
        a_chip.move_to(LEFT * 6.5 + UP * 1.05)
        a_bub.move_to(RIGHT * 0.4 + UP * 1.05)
        single_tool = self._pill('search_courses("AI")', ORANGE, size=14)
        single_tool.scale(0.85).move_to(UP * 0.1)
        self.play(FadeIn(a_chip), FadeIn(a_bub, shift=DOWN * 0.1),
                  run_time=0.4)
        self.play(FadeIn(single_tool, scale=0.8), run_time=0.4)
        self.wait(0.5)

        # tool_result
        r_chip = self._role_chip("tool_result", TEAL_BRIGHT, width=1.7).scale(0.85)
        r_bub = self._bubble(
            "5 門 AI 課,老師:張、李、范、林、王",
            TEAL_BRIGHT, fill_opacity=0.18,
            width=11.0, height=0.78, size=18,
        )
        r_chip.move_to(LEFT * 6.4 + DOWN * 0.7)
        r_bub.move_to(RIGHT * 0.4 + DOWN * 0.7)
        self.play(FadeOut(single_tool), run_time=0.2)
        self.play(FadeIn(r_chip), FadeIn(r_bub, shift=DOWN * 0.1),
                  run_time=0.5)
        self.wait(0.4)

        # Assistant gives partial answer
        f_chip = self._role_chip("assistant", VIOLET).scale(0.85)
        f_bub = self._bubble(
            "「這些是 AI 課程。但老師論文我無法繼續查…」",
            PINK, fill_opacity=0.25, stroke_width=2,
            width=11.0, height=0.85, size=19,
        )
        f_chip.move_to(LEFT * 6.5 + DOWN * 2.3)
        f_bub.move_to(RIGHT * 0.4 + DOWN * 2.3)
        self.play(FadeIn(f_chip), FadeIn(f_bub, shift=DOWN * 0.1),
                  run_time=0.5)

        # Failure indicator
        fail_box = self._pill("△  第二題卡住 · 單輪只能交一次", PINK, size=15)
        fail_box.scale(0.95).move_to(DOWN * 3.3)
        self.play(FadeIn(fail_box, scale=0.85), run_time=0.5)
        self.wait(1.8)

        cleanup = VGroup(badge, u_chip, u_bub, a_chip, a_bub,
                         r_chip, r_bub, f_chip, f_bub, fail_box)
        self.play(FadeOut(cleanup), run_time=0.5)
        self.clear_subtitle(run_time=0.3)
        self.advance_progress(13)

    # ============================================================
    # SCENE — SCENARIO (6s) — pivot to multi-turn
    # ============================================================
    def scene_scenario(self):
        self.show_subtitle("→ 讓 LLM 看到結果,再決定下一步")

        u_chip = self._role_chip("user", BLUE)
        u_bub = self._bubble(
            "「我下學期能修哪些 AI 課?這些老師最近有什麼論文?」",
            BLUE, fill_opacity=0.32, width=11.5, height=1.0, size=22,
        )
        u_chip.move_to(LEFT * 6.5 + UP * 1.5)
        u_bub.move_to(RIGHT * 0.4 + UP * 1.5)

        self.play(FadeIn(u_chip, shift=RIGHT * 0.15),
                  FadeIn(u_bub, shift=DOWN * 0.15),
                  run_time=0.5)
        self.wait(0.5)

        pivot = Text("→ 同一個問題 · 給 LLM 多輪機會看 tool_result",
                     font=CN_FONT, font_size=22,
                     color=TEAL_BRIGHT, weight=BOLD).move_to(DOWN * 0.4)
        self.play(FadeIn(pivot, shift=UP * 0.15), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(pivot), run_time=0.4)
        self.user_chip = u_chip
        self.user_bub = u_bub
        self.advance_progress(19)

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
        # Narrower bubble (was 11.5) — make room for tool_use badge outside,
        # right of the bubble. Reviewer flagged the "sticker glued onto
        # bubble" look in the previous layout.
        r1_assistant_bub = self._bubble(
            "「先查 AI 課程」", VIOLET, fill_opacity=0.18,
            width=10.3, height=0.85, size=20,
        )
        r1_assistant_chip.move_to(LEFT * 6.5 + UP * 2.0)
        # Keep bubble center at x=-0.2 so it sits visually closer to the chip
        # on the left and leaves clean room for the badge on the right
        r1_assistant_bub.move_to(LEFT * 0.2 + UP * 2.0)
        self.play(FadeIn(r1_label), run_time=0.25)

        r1_tool_use = RoundedRectangle(
            width=2.4, height=0.50, corner_radius=0.22,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.30,
        )
        r1_tool_use_text = Text("+ tool_use", font=MONO_FONT, font_size=14,
                                color=ORANGE, weight=BOLD).move_to(
                                    r1_tool_use.get_center())
        # Badge sits OUTSIDE the bubble's right edge — symmetric to the
        # assistant chip on the left. Clean violet ellipse + clear orange
        # side-effect label.
        r1_tool_badge = VGroup(r1_tool_use, r1_tool_use_text)
        r1_tool_badge.next_to(r1_assistant_bub, RIGHT, buff=0.22)

        self.play(FadeIn(r1_assistant_chip, shift=RIGHT * 0.15),
                  FadeIn(r1_assistant_bub, shift=DOWN * 0.15),
                  run_time=0.4)
        self.play(FadeIn(r1_tool_badge, shift=LEFT * 0.10), run_time=0.3)

        # tool call as a pill (was floating bare text — felt homeless)
        r1_tool_call = self._pill(
            'search_courses(keyword="AI")', ORANGE, size=15
        )
        r1_tool_call.move_to(UP * 1.15)
        self.play(FadeIn(r1_tool_call, scale=0.85), run_time=0.5)
        self.wait(1.2)

        # ----- Round 1 result back ---------------------------------
        self.show_subtitle("Round 1 · 結果回來:5 門課、5 位老師")

        r1_result_chip = self._role_chip("tool_result", TEAL_BRIGHT, width=1.8)
        r1_result_bub = self._bubble(
            "5 門 AI 課,老師:張、李、范、林、王",
            TEAL_BRIGHT, fill_opacity=0.18,
            width=10.3, height=0.85, size=20,
        )
        r1_result_chip.move_to(LEFT * 6.4 + UP * 0.4)
        r1_result_bub.move_to(LEFT * 0.2 + UP * 0.4)

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
            width=10.3, height=0.85, size=20,
        )
        r2_assistant_chip.move_to(LEFT * 6.5 + DOWN * 1.1)
        r2_assistant_bub.move_to(LEFT * 0.2 + DOWN * 1.1)
        self.play(FadeIn(r2_label), run_time=0.25)

        r2_tool_use = RoundedRectangle(
            width=2.6, height=0.50, corner_radius=0.22,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.30,
        )
        r2_tool_use_text = Text("+ 5× tool_use", font=MONO_FONT, font_size=13,
                                color=ORANGE, weight=BOLD).move_to(
                                    r2_tool_use.get_center())
        # Badge sits OUTSIDE bubble's right edge — symmetric to assistant chip
        r2_tool_badge = VGroup(r2_tool_use, r2_tool_use_text)
        r2_tool_badge.next_to(r2_assistant_bub, RIGHT, buff=0.22)

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
            width=10.3, height=0.85, size=20,
        )
        r2_result_chip.move_to(LEFT * 6.2 + DOWN * 2.4)
        r2_result_bub.move_to(LEFT * 0.2 + DOWN * 2.4)
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
        # Dim the accumulated stack further (was 0.18 → still visually
        # competed with the final bubble). 0.08 lets final stand out cleanly.
        self.play(loop_so_far.animate.set_opacity(0.08), run_time=0.5)
        self.show_subtitle("Round 3 · LLM 整合 5 個結果 → 最終回覆")

        final_chip = self._role_chip("assistant", VIOLET)
        final_chip.scale(1.15)
        final_bub = self._bubble(
            "「你下學期可修這 5 門,范教授論文最對胃口…」",
            VIOLET, fill_opacity=0.55, stroke_width=4,
            width=12.5, height=1.2, size=24,
        )
        final_chip.move_to(LEFT * 6.2 + ORIGIN)
        final_bub.move_to(RIGHT * 0.5 + ORIGIN)
        final_chip.set_z_index(10)
        final_bub.set_z_index(10)

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

        # B-plan enhancement: bring up explicit stop_reason verdict so the
        # audience walks away with the vocabulary
        sr_verdict = self._pill("stop_reason = end_turn  →  loop 收工",
                                GREEN, size=16)
        sr_verdict.move_to(DOWN * 3.0)
        self.play(FadeIn(sr_verdict, shift=UP * 0.1), run_time=0.4)
        self.wait(2.5)

        cleanups = [
            self.user_chip, self.user_bub,
            loop_so_far,
            final_chip, final_bub, end_turn_chip,
            sr_verdict, badge,
        ]
        self.play(*[FadeOut(m) for m in cleanups], run_time=0.5)
        self.clear_subtitle(run_time=0.3)
        self.advance_progress(46)

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
        self.advance_progress(55)

    # ============================================================
    # SCENE — RECAP (5s) — compressed loop replay
    # ============================================================
    def scene_recap(self):
        """5s compressed visual of the 3-round loop ─ for audience to lock
        the pattern before takeaway cards roll in."""
        badge = self._stage_badge("RECAP", VIOLET_SOFT)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("一條 loop 的全貌 · 從 query 到 final answer")

        # User query (compressed)
        u_pill = self._pill("USER · 複合 query", BLUE, size=15)
        u_pill.move_to(LEFT * 5.5 + UP * 0.3)
        # 3 round circles — all ORANGE (iteration phase),
        # GREEN reserved for end_turn terminal state only
        rounds_data = [
            ("R1", "search_courses", ORANGE),
            ("R2", "arxiv × 5", ORANGE),
            ("R3", "integrate", ORANGE),
        ]
        round_pills = VGroup()
        for i, (rid, label, c) in enumerate(rounds_data):
            x = -1.5 + i * 2.0
            ring = Circle(radius=0.42, color=c, stroke_width=3,
                          fill_color=c, fill_opacity=0.15)
            ring.move_to([x, 0.3, 0])
            rid_text = Text(rid, font=MONO_FONT, font_size=18,
                            color=c, weight=BOLD).move_to(ring.get_center())
            sub_text = Text(label, font=MONO_FONT, font_size=13,
                            color=NEUTRAL).next_to(ring, DOWN, buff=0.25)
            round_pills.add(VGroup(ring, rid_text, sub_text))

        final_pill = self._pill("✓ end_turn", GREEN, size=15)
        final_pill.move_to(RIGHT * 5.5 + UP * 0.3)

        # Arrows
        arr1 = Arrow(u_pill.get_right() + RIGHT * 0.05,
                     round_pills[0][0].get_left() + LEFT * 0.05,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
                     color=NEUTRAL, buff=0.05)
        arr2 = Arrow(round_pills[0][0].get_right() + RIGHT * 0.05,
                     round_pills[1][0].get_left() + LEFT * 0.05,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
                     color=NEUTRAL, buff=0.05)
        arr3 = Arrow(round_pills[1][0].get_right() + RIGHT * 0.05,
                     round_pills[2][0].get_left() + LEFT * 0.05,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
                     color=NEUTRAL, buff=0.05)
        arr4 = Arrow(round_pills[2][0].get_right() + RIGHT * 0.05,
                     final_pill.get_left() + LEFT * 0.05,
                     stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
                     color=GREEN, buff=0.05)

        self.play(FadeIn(u_pill, shift=RIGHT * 0.15),
                  GrowArrow(arr1), run_time=0.5)
        for i, r in enumerate(round_pills):
            arr = [arr2, arr3][i] if i < 2 else None
            self.play(FadeIn(r, scale=0.8), run_time=0.3)
            if arr is not None:
                self.play(GrowArrow(arr), run_time=0.25)
        self.play(GrowArrow(arr4),
                  FadeIn(final_pill, shift=LEFT * 0.15), run_time=0.5)

        # stop_reason pill between chain and caption — anchors the
        # terminal-state vocabulary in the recap. Pushed further down so
        # it doesn't collide with the sub_text labels under each round ring.
        sr_pill = self._pill("stop_reason = end_turn  →  loop 收工", GREEN, size=14)
        sr_pill.scale(0.85).move_to(DOWN * 1.15)
        self.play(FadeIn(sr_pill, shift=UP * 0.10), run_time=0.4)

        # Caption — moved further down to balance vertical composition
        caption = Text("關鍵:LLM 自己看 tool_result 再決定下一輪 · loop 一定收得回來",
                       font=CN_FONT, font_size=20,
                       color=VIOLET_SOFT, weight=BOLD).move_to(DOWN * 1.95)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.4)
        self.wait(1.2)

        cleanup = VGroup(badge, u_pill, round_pills,
                         arr1, arr2, arr3, arr4, final_pill,
                         sr_pill, caption)
        self.play(FadeOut(cleanup), run_time=0.5)
        self.clear_subtitle(run_time=0.3)
        self.advance_progress(60)

    # ============================================================
    # SCENE — TAKEAWAY (15s) — D-plan: stagger cards, mini-icons, longer dwell
    # ============================================================
    def scene_takeaway(self):
        # Hero title uses SERIF_FONT to match V1/V2 channel convention
        # (intro "Agentic / Loop" + closing "Decide · Iterate · Closure"
        # are both SERIF). The mixed "三件事" Chinese fragment renders fine
        # in Noto Serif CJK TC.
        outro_title = Text("Agentic Loop = 三件事",
                           font=SERIF_FONT, font_size=42,
                           color=INK, weight=BOLD).move_to(UP * 3.0)

        cards_data = [
            ("①", "Decide", "拆解問題 + 選 tool",
             "LLM 自己決定要不要、要呼叫哪個", VIOLET, "?"),
            ("②", "Iterate", "多輪迭代 + 結果驅動",
             "看 tool_result 再決定下一輪", ORANGE, "↻"),
            ("③", "Closure", "end_turn / maxIterations",
             "loop 一定收得回來,不無限跑", TEAL_BRIGHT, "✓"),
        ]

        card_w = 4.4
        cards = VGroup()         # whole card groups (box + content)
        contents = []            # per-card content sub-group (texts + icon)
        icons = []
        for i, (num, eng, cn, desc, color, icon_char) in enumerate(cards_data):
            x = -4.6 + i * 4.6
            box = RoundedRectangle(width=card_w, height=4.2, corner_radius=0.22,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=color, fill_opacity=0.12)
            box.move_to([x, -0.4, 0])

            num_text = Text(num, font=MONO_FONT, font_size=42,
                            color=color, weight=BOLD).move_to(
                                box.get_top() + DOWN * 0.55)
            # mini-icon ring
            icon_ring = Circle(radius=0.36, color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.18)
            icon_ring.move_to(box.get_top() + DOWN * 1.45)
            icon_glyph = Text(icon_char, font=SERIF_FONT, font_size=36,
                              color=color, weight=BOLD).move_to(icon_ring.get_center())
            icon = VGroup(icon_ring, icon_glyph)
            eng_text = Text(eng, font=SERIF_FONT, font_size=28,
                            color=INK, weight=BOLD).move_to(
                                box.get_top() + DOWN * 2.25)
            cn_text = Text(cn, font=CN_FONT, font_size=16,
                           color=color, weight=BOLD).move_to(
                               box.get_top() + DOWN * 2.85)
            desc_text = Text(desc, font=CN_FONT, font_size=14,
                             color=INK).move_to(
                                 box.get_top() + DOWN * 3.55)
            # IMPORTANT — box stays separate so opacity animations on the
            # content do NOT change the box fill (else fill_opacity 0.12 → 1.0
            # turns the card into a solid color block that swallows the text)
            content = VGroup(num_text, icon, eng_text, cn_text, desc_text)
            card = VGroup(box, content)  # card[0]=box, card[1]=content
            cards.add(card)
            contents.append(content)
            icons.append(icon)

        self.play(FadeIn(outro_title, shift=DOWN * 0.2), run_time=0.6)

        # All 3 cards appear together; their CONTENT starts at 0.25 opacity
        # so the 3-column layout is complete from t=0 but only hero focus
        # shifts ① → ② → ③ over time. Box stays at fill_opacity 0.12 always.
        for content in contents:
            content.set_opacity(0.25)
        self.play(FadeIn(cards, shift=UP * 0.15), run_time=0.7)

        for i in range(len(cards)):
            self.play(
                contents[i].animate.set_opacity(1.0),
                Indicate(icons[i], scale_factor=1.35,
                         color=cards_data[i][4]),
                run_time=0.7,
            )
            self.wait(1.8)
            if i < len(cards) - 1:
                self.play(contents[i].animate.set_opacity(0.55), run_time=0.3)

        self.wait(0.6)
        self.play(FadeOut(outro_title), FadeOut(cards), run_time=0.5)
        self.advance_progress(75)

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
