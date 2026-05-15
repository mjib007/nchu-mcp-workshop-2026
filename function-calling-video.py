"""
function-calling-video.py

~2-min long video visualizing how function calling works mechanically.
Topic: LLM only emits strings; the real execution happens in the harness.

Six scenes:
  Scenario: user query → harness
  Stage 1+2: developer prepares tools schema + sends API call
  Stage 3: LLM returns JSON (tool_use block, stop_reason flag)
  Stage 4: harness actually executes — subprocess.run is the eval moment
  Stage 5+6: tool_result fed back, LLM produces final answer
  Takeaway: LLM ↔ Harness responsibility split

Render:
  manim -ql --disable_caching function-calling-video.py FunctionCalling
  manim -qh function-calling-video.py FunctionCalling      # final 1080p60
"""

from manim import *
import numpy as np

# Violet-primary palette (matches 2026 slide deck)
BG            = "#0a0a10"
VIOLET        = "#7B5CF5"
VIOLET_DEEP   = "#5B3ED9"
VIOLET_SOFT   = "#9D85F7"
BLUE          = "#5B8DE8"
ORANGE        = "#FB7048"
TEAL          = "#0EA594"
TEAL_BRIGHT   = "#2DD4BF"
PINK          = "#EF4444"
PINK_DEEP     = "#B91C1C"
GREEN         = "#5CB85C"
INK           = "#FFFFFF"
NEUTRAL       = "#B4BED2"
DIM           = "#3A4A6A"
CODE_FG       = "#E5E7EB"
CODE_GREEN    = "#A8E1B4"
CODE_VIOLET   = "#C8B6FF"
CODE_COMMENT  = "#9CA3AF"
CODE_ORANGE   = "#FB924D"

CN_FONT     = "Noto Sans CJK TC"
SERIF_FONT  = "Noto Serif CJK TC"
MONO_FONT   = "DejaVu Sans Mono"

config.frame_width  = 16
config.frame_height = 9
config.pixel_width  = 1920
config.pixel_height = 1080


class FunctionCalling(Scene):
    SUBTITLE_MAX_WIDTH = 14.0
    TOTAL_SECONDS = 86.0

    TITLE     = "Function Calling 怎麼運作"
    SUBTITLE  = "LLM 只吐字串,真的執行的是外面的 harness"

    def construct(self):
        self.camera.background_color = BG
        self._cur_subtitle = None
        self._init_progress_bar()

        self.scene_intro()        # 0:00–0:04
        self.scene_scenario()     # 0:04–0:14
        self.scene_stage12()      # 0:14–0:32
        self.scene_stage3()       # 0:32–0:54
        self.scene_stage4()       # 0:54–1:20
        self.scene_stage56()      # 1:20–1:38
        self.scene_closure()      # 1:38–1:46  (frame story closes)
        self.scene_takeaway()     # 1:46–2:04

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
        self.progress_fill.move_to(
            [self._bar_left + w / 2, self._bar_y, 0]
        )

    def advance_progress(self, target_seconds):
        target_w = self._bar_total_width * (target_seconds / self.TOTAL_SECONDS)
        self._set_fill_width(target_w)

    # ============================================================
    # Subtitle helpers
    # ============================================================
    def _build_subtitle(self, text):
        sub = Text(text, font=CN_FONT, font_size=30, color=INK, weight=MEDIUM)
        if sub.width > self.SUBTITLE_MAX_WIDTH:
            sub.scale_to_fit_width(self.SUBTITLE_MAX_WIDTH)
        sub.to_edge(DOWN, buff=0.7)
        return sub

    def show_subtitle(self, text, run_time=0.35):
        new_sub = self._build_subtitle(text)
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), FadeIn(new_sub),
                      run_time=run_time)
        else:
            self.play(FadeIn(new_sub), run_time=run_time)
        self._cur_subtitle = new_sub

    def clear_subtitle(self, run_time=0.3):
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=run_time)
            self._cur_subtitle = None

    # ============================================================
    # Stage badge helper
    # ============================================================
    def _make_stage_badge(self, text, color=VIOLET):
        box = RoundedRectangle(width=2.0, height=0.48, corner_radius=0.09,
                               stroke_color=NEUTRAL, stroke_width=1.5,
                               fill_color=color, fill_opacity=0.0)
        lbl = Text(text, font=MONO_FONT, font_size=17,
                   color=color, weight=BOLD).move_to(box.get_center())
        badge = VGroup(box, lbl).move_to([6.7, 4.05, 0])
        badge.set_z_index(100)
        return badge

    # ============================================================
    # Pill helper (token flying along an arrow)
    # ============================================================
    def _pill(self, label, color, size=16):
        txt = Text(label, font=MONO_FONT, font_size=size,
                   color=INK, weight=BOLD)
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
    # Code block (rounded with mono lines)
    # ============================================================
    def _code_block(self, lines, width=8.0, line_h=0.30, size=16, color=None):
        """Dark code block. lines = list[(text, color)].
        - Empty/whitespace lines get a transparent space placeholder so they
          still occupy a row (Manim Text("") otherwise collapses to 0 height).
        - Leading ASCII spaces are replaced with U+2003 (em-space) so that
          indentation survives Manim Text's whitespace handling.
        - buff bumped to 0.22 — was 0.10, far too tight for CJK + Latin mixed.
        """
        if color is None:
            color = CODE_FG
        text_group = VGroup()
        for line, line_color in lines:
            stripped = line.strip()
            if not stripped:
                rendered = " "
                t = Text(rendered, font=MONO_FONT, font_size=size,
                         color=line_color, weight=MEDIUM)
                t.set_opacity(0)
            else:
                # Preserve leading indentation by swapping ASCII space → em-space
                lead = len(line) - len(line.lstrip(" "))
                rendered = (" " * lead) + line.lstrip(" ")
                t = Text(rendered, font=MONO_FONT, font_size=size,
                         color=line_color, weight=MEDIUM)
            text_group.add(t)
        # Explicit per-line y positioning — Manim's arrange() collapses
        # rows when mixing CJK + Latin at small sizes. Use fixed line step.
        line_step = size * 0.024 + 0.06   # at size 17 → 0.468 / size 16 → 0.444
        for i, m in enumerate(text_group):
            cur_x = float(m.get_center()[0])
            m.move_to(np.array([cur_x, -i * line_step, 0.0]))
        leftmost = float(min(float(m.get_left()[0]) for m in text_group))
        for m in text_group:
            m.shift(np.array([leftmost - float(m.get_left()[0]), 0.0, 0.0]))
        h = (len(lines) - 1) * line_step + size * 0.04 + 0.5
        box = RoundedRectangle(
            width=width, height=h, corner_radius=0.18,
            stroke_color=DIM, stroke_width=2.0,
            fill_color="#1A2440", fill_opacity=0.95,
        )
        text_group.move_to(box.get_center())
        return VGroup(box, text_group)

    # ============================================================
    # INTRO (4s)
    # ============================================================
    def scene_intro(self):
        title = Text(self.TITLE, font=SERIF_FONT, font_size=88,
                     color=INK, weight=BOLD).move_to(UP * 0.6)
        subtitle = Text(self.SUBTITLE, font=CN_FONT, font_size=32,
                        color=VIOLET_SOFT).move_to(DOWN * 0.6)
        accent = Line(start=LEFT * 1.5, end=RIGHT * 1.5,
                      color=VIOLET, stroke_width=4).move_to(DOWN * 0.05)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.9)
        self.play(GrowFromCenter(accent), run_time=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(accent),
                  run_time=0.5)
        self.advance_progress(4)

    # ============================================================
    # SCENARIO (10s)
    # ============================================================
    def scene_scenario(self):
        # User query bubble (top)
        bub = RoundedRectangle(width=9.0, height=1.2, corner_radius=0.30,
                               stroke_color=VIOLET, stroke_width=3,
                               fill_color=VIOLET, fill_opacity=0.35)
        bub_text = Text("我家目錄底下有幾個 .py 檔？",
                        font=CN_FONT, font_size=36,
                        color=INK, weight=BOLD).move_to(bub.get_center())
        bub_group = VGroup(bub, bub_text).move_to(UP * 1.5)
        bub_label = Text("使用者輸入", font=CN_FONT, font_size=22,
                         color=NEUTRAL).next_to(bub_group, UP, buff=0.18)

        self.show_subtitle("用一個具體例子搞懂")
        self.play(FadeIn(bub_label, shift=DOWN * 0.1),
                  FadeIn(bub_group, shift=DOWN * 0.2),
                  run_time=0.7)
        self.wait(2.0)

        # Big punchline
        punchline = Text("LLM 只做一件事 —— 吐字串",
                         font=CN_FONT, font_size=48, color=ORANGE,
                         weight=BOLD).move_to(DOWN * 0.5)
        self.play(Write(punchline), run_time=1.0)
        self.show_subtitle("想想看:這個查詢背後到底發生了什麼?")
        self.wait(4.0)

        self.play(FadeOut(bub_label), FadeOut(bub_group),
                  FadeOut(punchline), run_time=0.5)
        self.advance_progress(11)

    # ============================================================
    # STAGE 1+2 — developer prepares schema + API call (18s)
    # ============================================================
    def scene_stage12(self):
        badge = self._make_stage_badge("STAGE 1+2", VIOLET)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("想想看:這個查詢背後到底發生了什麼?")

        # Three pills representing the only fields the LLM sees
        title = Text("LLM 看到的,只有這三件事", font=CN_FONT, font_size=30,
                     color=INK, weight=BOLD).move_to(UP * 2.6)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.5)

        name_pill = self._pill("name : execute_bash", VIOLET, size=22)
        desc_pill = self._pill("description : 執行 bash 指令", ORANGE, size=22)
        sch_pill  = self._pill("input_schema : { command }", TEAL_BRIGHT, size=22)
        pills = VGroup(name_pill, desc_pill, sch_pill).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        ).move_to(LEFT * 3.0 + UP * 0.1)

        # All three pills together (slight stagger via LaggedStart)
        self.play(LaggedStart(
            FadeIn(name_pill, shift=RIGHT * 0.3),
            FadeIn(desc_pill, shift=RIGHT * 0.3),
            FadeIn(sch_pill, shift=RIGHT * 0.3),
            lag_ratio=0.25,
        ), run_time=1.0)
        self.wait(1.5)

        # Envelope on the right (tool schema packaged)
        env_box = RoundedRectangle(
            width=4.5, height=2.6, corner_radius=0.20,
            stroke_color=VIOLET, stroke_width=3,
            fill_color=VIOLET, fill_opacity=0.18,
        ).move_to(RIGHT * 3.5 + UP * 0.1)
        env_title = Text("tool schema", font=MONO_FONT, font_size=18,
                         color=VIOLET_SOFT, weight=BOLD).move_to(
                             env_box.get_top() + DOWN * 0.35)
        env_icon = Text("✉", font=CN_FONT, font_size=72, color=VIOLET).move_to(
            env_box.get_center() + UP * 0.05)
        env_caption = Text("送往  ☁ Claude API",
                           font=CN_FONT, font_size=16, color=ORANGE).move_to(
                               env_box.get_bottom() + UP * 0.4)
        envelope = VGroup(env_box, env_title, env_icon, env_caption)

        self.play(FadeIn(envelope, shift=LEFT * 0.3), run_time=0.6)
        self.wait(0.5)

        # Pulse the three pills as they "go in" to the envelope
        self.play(
            Indicate(name_pill, scale_factor=1.08, color=VIOLET),
            Indicate(desc_pill, scale_factor=1.08, color=ORANGE),
            Indicate(sch_pill,  scale_factor=1.08, color=TEAL_BRIGHT),
            Indicate(envelope, scale_factor=1.04, color=VIOLET_SOFT),
            run_time=1.0,
        )
        self.wait(2.0)

        # Bottom punchline
        pl = Text("這就是 LLM 端的全部 — 沒有「綁定 Python 函式」這回事",
                  font=CN_FONT, font_size=24,
                  color=VIOLET_SOFT, slant=ITALIC).move_to(DOWN * 2.6)
        self.play(FadeIn(pl, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(title), FadeOut(name_pill), FadeOut(desc_pill),
                  FadeOut(sch_pill), FadeOut(envelope), FadeOut(pl),
                  FadeOut(badge), run_time=0.5)
        self.advance_progress(26)

    # ============================================================
    # STAGE 3 — LLM returns JSON (22s) — KEY moment
    # ============================================================
    def scene_stage3(self):
        badge = self._make_stage_badge("STAGE 3", ORANGE)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("但 LLM 沒有手 — 它怎麼真的執行 find?")

        # LLM "brain" entity at top
        llm_box = RoundedRectangle(
            width=3.2, height=1.3, corner_radius=0.25,
            stroke_color=VIOLET_SOFT, stroke_width=3,
            fill_color=VIOLET, fill_opacity=0.35,
        ).move_to(UP * 2.5)
        llm_label = Text("LLM (Claude)", font=CN_FONT, font_size=24,
                         color=INK, weight=BOLD).move_to(llm_box.get_center())
        llm = VGroup(llm_box, llm_label)
        self.play(FadeIn(llm), run_time=0.5)
        self.wait(0.8)

        # stop_reason ribbon at very top
        flag_box = RoundedRectangle(
            width=5.5, height=0.55, corner_radius=0.15,
            stroke_color=ORANGE, stroke_width=2.5,
            fill_color=ORANGE, fill_opacity=0.85,
        )
        flag_text = Text('stop_reason : "tool_use"',
                         font=MONO_FONT, font_size=20,
                         color=INK, weight=BOLD).move_to(flag_box.get_center())
        flag = VGroup(flag_box, flag_text).move_to(UP * 3.55)
        self.play(FadeIn(flag, shift=DOWN * 0.15), run_time=0.6)
        self.wait(0.5)

        # Two emissions from LLM
        # 1) Text bubble (left)
        tb_box = RoundedRectangle(
            width=5.5, height=1.5, corner_radius=0.22,
            stroke_color=CODE_GREEN, stroke_width=2,
            fill_color=CODE_GREEN, fill_opacity=0.20,
        )
        tb_title = Text("① 文字回覆", font=CN_FONT, font_size=18,
                        color=CODE_GREEN, weight=BOLD).move_to(tb_box.get_top() + DOWN * 0.30)
        tb_body = Text("「讓我用 find 幫你數一下。」",
                       font=CN_FONT, font_size=22,
                       color=INK).move_to(tb_box.get_center() + DOWN * 0.10)
        text_bubble = VGroup(tb_box, tb_title, tb_body).move_to(LEFT * 3.6 + UP * 0.4)

        # 2) Tool call card (right)
        tc_box = RoundedRectangle(
            width=5.5, height=1.5, corner_radius=0.22,
            stroke_color=ORANGE, stroke_width=2.5,
            fill_color=ORANGE, fill_opacity=0.22,
        )
        tc_title = Text("② 工具呼叫", font=CN_FONT, font_size=18,
                        color=ORANGE, weight=BOLD).move_to(tc_box.get_top() + DOWN * 0.30)
        tc_name = Text("execute_bash", font=MONO_FONT, font_size=20,
                       color=INK, weight=BOLD).move_to(tc_box.get_center() + UP * 0.05)
        tc_cmd = Text('"find ~ -name \'*.py\'"',
                      font=MONO_FONT, font_size=15,
                      color=CODE_GREEN).move_to(tc_box.get_center() + DOWN * 0.32)
        tool_card = VGroup(tc_box, tc_title, tc_name, tc_cmd).move_to(RIGHT * 3.6 + UP * 0.4)

        # Arrows from LLM to both — use box corners so the diagonals visually
        # match the "射出兩個 emission" metaphor (was: nearly-horizontal centers)
        arr_left = Arrow(start=llm_box.get_corner(DL),
                         end=text_bubble.get_corner(UR),
                         color=CODE_GREEN, stroke_width=3,
                         buff=0.12, max_tip_length_to_length_ratio=0.10)
        arr_right = Arrow(start=llm_box.get_corner(DR),
                          end=tool_card.get_corner(UL),
                          color=ORANGE, stroke_width=3,
                          buff=0.12, max_tip_length_to_length_ratio=0.10)

        self.play(GrowArrow(arr_left), FadeIn(text_bubble, shift=DOWN * 0.3),
                  run_time=0.8)
        self.wait(2.0)
        self.play(GrowArrow(arr_right), FadeIn(tool_card, shift=DOWN * 0.3),
                  run_time=0.8)
        self.wait(2.5)

        # Bottom punchline
        pl_box = RoundedRectangle(width=14, height=0.85, corner_radius=0.18,
                                  stroke_color=ORANGE, stroke_width=2.5,
                                  fill_color=ORANGE, fill_opacity=0.20)
        pl_text = Text("LLM 沒「呼叫」任何東西 — 它就是吐了兩個字串卡片",
                       font=CN_FONT, font_size=26, color=ORANGE,
                       weight=BOLD).move_to(pl_box.get_center())
        pl = VGroup(pl_box, pl_text).move_to(DOWN * 2.6)
        self.play(FadeIn(pl, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(llm), FadeOut(flag),
                  FadeOut(text_bubble), FadeOut(tool_card),
                  FadeOut(arr_left), FadeOut(arr_right),
                  FadeOut(pl), FadeOut(badge), run_time=0.5)
        self.advance_progress(44)

    # ============================================================
    # STAGE 4 — harness executes (26s) — THE eval moment
    # ============================================================
    def scene_stage4(self):
        badge = self._make_stage_badge("STAGE 4", PINK)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("⚠ harness 不長眼 — LLM 給什麼字串它都會跑")

        # ── Top zone: 文字宇宙 (violet dashed box with the token inside) ──
        tw_box = DashedVMobject(
            Rectangle(width=10.0, height=1.6,
                      stroke_color=VIOLET_SOFT, stroke_width=2.5,
                      fill_opacity=0).move_to(UP * 2.3),
            num_dashes=40,
        )
        tw_title = Text("「文字宇宙」 — LLM 吐的字串",
                        font=CN_FONT, font_size=20,
                        color=VIOLET_SOFT, weight=BOLD)
        tw_title.next_to(tw_box, UP, buff=0.15)
        tw_token = self._pill('execute_bash  ·  "find ~ -name \'*.py\'"',
                              ORANGE, size=18)
        tw_token.move_to(UP * 2.3 + DOWN * 0.15)

        self.play(Create(tw_box), FadeIn(tw_title), run_time=0.6)
        self.play(FadeIn(tw_token, scale=0.7), run_time=0.4)
        self.wait(1.0)

        # ── Middle zone: the door (split arrow so door_label isn't pierced) ──
        door_label = Text("subprocess.run( … )",
                          font=MONO_FONT, font_size=28,
                          color=ORANGE, weight=BOLD).move_to(UP * 0.55)
        door_caption = Text("這道門 — 把 LLM 字串交給 shell",
                            font=CN_FONT, font_size=18,
                            color=NEUTRAL).next_to(door_label, DOWN, buff=0.10)
        arrow_in = Arrow(start=UP * 1.45, end=door_label.get_top() + UP * 0.05,
                         color=ORANGE, stroke_width=8,
                         buff=0.05, max_tip_length_to_length_ratio=0.22)
        arrow_out_down = Arrow(start=door_caption.get_bottom() + DOWN * 0.05,
                               end=DOWN * 0.85,
                               color=ORANGE, stroke_width=8,
                               buff=0.05, max_tip_length_to_length_ratio=0.22)

        self.play(GrowArrow(arrow_in), run_time=0.35)
        self.play(Write(door_label), FadeIn(door_caption), run_time=0.55)
        self.play(GrowArrow(arrow_out_down), run_time=0.35)
        self.wait(0.3)

        # ── Token flies through the door ──
        flying = tw_token.copy()
        self.add(flying)
        self.play(
            flying.animate.move_to(DOWN * 1.7).scale(0.7),
            run_time=1.4,
        )

        # ── Bottom zone: 真實電腦 (teal dashed box) ──
        rw_box = DashedVMobject(
            Rectangle(width=10.0, height=1.6,
                      stroke_color=TEAL_BRIGHT, stroke_width=2.5,
                      fill_opacity=0).move_to(DOWN * 1.7),
            num_dashes=40,
        )
        rw_title = Text("「真實電腦」 — shell 真的跑了",
                        font=CN_FONT, font_size=20,
                        color=TEAL_BRIGHT, weight=BOLD)
        rw_title.next_to(rw_box, UP, buff=0.15)

        # Shell prompt: $ find ~ ... → 42
        prompt = Text("$  find ~ -name '*.py' | wc -l",
                      font=MONO_FONT, font_size=20,
                      color=TEAL_BRIGHT).move_to(DOWN * 1.7 + DOWN * 0.05 + LEFT * 1.5)
        arrow_out = Text("→", font=MONO_FONT, font_size=24,
                         color=NEUTRAL, weight=BOLD).move_to(DOWN * 1.7 + DOWN * 0.05 + RIGHT * 2.4)
        result_42 = Text("42", font=MONO_FONT, font_size=32,
                         color=GREEN, weight=BOLD).move_to(DOWN * 1.7 + DOWN * 0.05 + RIGHT * 3.2)

        self.play(Create(rw_box), FadeIn(rw_title), run_time=0.5)
        self.play(FadeOut(flying), Write(prompt), run_time=0.9)
        self.play(FadeIn(arrow_out), FadeIn(result_42, scale=1.2), run_time=0.6)
        self.wait(2.0)

        # ── Bottom security warning ──
        warn_box = RoundedRectangle(width=13.5, height=0.95, corner_radius=0.18,
                                    stroke_color=PINK, stroke_width=2.5,
                                    fill_color=PINK, fill_opacity=0.20)
        warn_text = Text("⚠ 這就是 eval(LLM 輸出) — prompt injection 攻擊就能讓 harness 跑 rm -rf",
                         font=CN_FONT, font_size=20, color=PINK,
                         weight=BOLD).move_to(warn_box.get_center())
        warn = VGroup(warn_box, warn_text).move_to(DOWN * 3.15)
        self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)

        cleanups = [tw_box, tw_title, tw_token, arrow_in, arrow_out_down,
                    door_label, door_caption,
                    rw_box, rw_title, prompt, arrow_out, result_42,
                    warn, badge]
        self.play(*[FadeOut(m) for m in cleanups], run_time=0.5)
        self.advance_progress(66)

    # ============================================================
    # STAGE 5+6 — feedback loop + final answer (18s)
    # ============================================================
    def scene_stage56(self):
        badge = self._make_stage_badge("STAGE 5+6", TEAL)
        self.play(FadeIn(badge), run_time=0.3)
        self.show_subtitle("把 42 塞回對話 — LLM 看完再吐一段話")

        # Chat-style stack of 4 bubbles
        def _bubble(text, accent, fill_opacity=0.18, stroke_width=2,
                    role_text="", role_color=None):
            bub_w = 10.5
            bub_h = 0.95
            box = RoundedRectangle(
                width=bub_w, height=bub_h, corner_radius=0.25,
                stroke_color=accent, stroke_width=stroke_width,
                fill_color=accent, fill_opacity=fill_opacity,
            )
            t = Text(text, font=CN_FONT, font_size=22,
                     color=INK).move_to(box.get_center())
            return VGroup(box, t)

        def _role_chip(text, color):
            chip = RoundedRectangle(
                width=1.6, height=0.45, corner_radius=0.22,
                stroke_color=color, stroke_width=0,
                fill_color=color, fill_opacity=1.0,
            )
            t = Text(text, font=MONO_FONT, font_size=15,
                     color=INK, weight=BOLD).move_to(chip.get_center())
            return VGroup(chip, t)

        # All bubble positions (top to bottom)
        ys = [2.5, 1.3, -0.0, -1.6]

        bubbles = []
        chips = []

        # 1) User query (blue)
        u1_chip = _role_chip("user", BLUE)
        u1_bub = _bubble("我家目錄底下有幾個 .py 檔？", BLUE)
        u1_chip.move_to(LEFT * 5.4 + UP * ys[0])
        u1_bub.move_to(RIGHT * 0.5 + UP * ys[0])
        self.play(FadeIn(u1_chip, shift=RIGHT * 0.15),
                  FadeIn(u1_bub, shift=DOWN * 0.15), run_time=0.5)
        bubbles.append(u1_bub); chips.append(u1_chip)
        self.wait(0.6)

        # 2) Assistant text + tool_use marker (violet)
        # Split message into two visual lines for clarity
        a1_chip = _role_chip("assistant", VIOLET)
        a1_bub = _bubble("「讓我用 find 幫你數一下」",
                         VIOLET)
        a1_chip.move_to(LEFT * 5.4 + UP * ys[1])
        a1_bub.move_to(RIGHT * 0.5 + UP * ys[1])
        # Corner badge attached to the assistant bubble
        a1_badge_box = RoundedRectangle(
            width=2.0, height=0.42, corner_radius=0.20,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.30,
        )
        a1_badge_text = Text("+ tool_use", font=MONO_FONT, font_size=14,
                             color=ORANGE, weight=BOLD).move_to(a1_badge_box.get_center())
        a1_badge = VGroup(a1_badge_box, a1_badge_text)
        a1_badge.move_to(a1_bub.get_corner(UR) + DOWN * 0.05 + LEFT * 1.10)
        self.play(FadeIn(a1_chip, shift=RIGHT * 0.15),
                  FadeIn(a1_bub, shift=DOWN * 0.15),
                  FadeIn(a1_badge, shift=LEFT * 0.10),
                  run_time=0.5)
        bubbles.append(a1_bub); chips.append(a1_chip); chips.append(a1_badge)
        self.wait(1.2)

        # 3) Tool result (TEAL — note: this is role=user in API,
        #    but visually we mark it as "工具回傳" via color)
        t1_chip = _role_chip("tool_result", TEAL_BRIGHT)
        t1_bub = _bubble("42  (find 跑完的結果)", TEAL_BRIGHT)
        t1_chip.move_to(LEFT * 5.4 + UP * ys[2])
        t1_bub.move_to(RIGHT * 0.5 + UP * ys[2])
        self.play(FadeIn(t1_chip, shift=RIGHT * 0.15),
                  FadeIn(t1_bub, shift=DOWN * 0.15), run_time=0.5)
        bubbles.append(t1_bub); chips.append(t1_chip)

        # Sidenote about role being "user" under the hood
        side_note = Text("(API 上 role 其實是 user,但意義是工具回傳)",
                         font=CN_FONT, font_size=14, color=NEUTRAL,
                         slant=ITALIC).move_to(
                             RIGHT * 0.5 + UP * ys[2] + DOWN * 0.65)
        self.play(FadeIn(side_note), run_time=0.3)
        self.wait(0.9)

        # 4) Assistant final answer (violet + end_turn marker)
        # Punchline bubble: heavier fill + thicker stroke to break the visual flatline
        a2_chip = _role_chip("assistant", VIOLET)
        a2_bub = _bubble("「你家目錄底下總共有 42 個 .py 檔。」",
                         VIOLET, fill_opacity=0.42, stroke_width=3)
        a2_chip.move_to(LEFT * 5.4 + UP * ys[3])
        a2_bub.move_to(RIGHT * 0.5 + UP * ys[3])
        # ✓ end_turn corner chip — mirrors the orange +tool_use chip on bubble 2
        # (open ↔ close: tool_use opens the round-trip, end_turn closes it)
        end_turn_box = RoundedRectangle(
            width=2.0, height=0.42, corner_radius=0.20,
            stroke_color=GREEN, stroke_width=0,
            fill_color=GREEN, fill_opacity=1.0,
        )
        end_turn_text = Text("✓ end_turn", font=MONO_FONT, font_size=14,
                             color=BG, weight=BOLD).move_to(end_turn_box.get_center())
        end_turn_chip = VGroup(end_turn_box, end_turn_text)
        end_turn_chip.move_to(a2_bub.get_corner(UR) + DOWN * 0.05 + LEFT * 1.10)
        self.play(FadeIn(a2_chip, shift=RIGHT * 0.15),
                  FadeIn(a2_bub, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(end_turn_chip, shift=LEFT * 0.10), run_time=0.4)
        bubbles.append(a2_bub); chips.append(a2_chip); chips.append(end_turn_chip)
        self.wait(0.3)

        # Highlight the loop closure — pulse the green chip itself
        self.play(Indicate(end_turn_chip, scale_factor=1.25, color=GREEN),
                  run_time=0.7)
        self.wait(1.8)

        # Bottom takeaway
        bt = Text("整個對話只是一串卡片往下堆 —— 直到 LLM 說 end_turn",
                  font=CN_FONT, font_size=22,
                  color=VIOLET_SOFT, slant=ITALIC).move_to(DOWN * 2.8)
        self.play(FadeIn(bt, shift=UP * 0.2), run_time=0.6)
        self.wait(2.5)

        cleanups = bubbles + chips + [side_note, bt, badge]
        self.play(*[FadeOut(m) for m in cleanups], run_time=0.5)
        self.advance_progress(80)

    # ============================================================
    # CLOSURE — close the frame story started in scene_scenario (~8s)
    # ============================================================
    def scene_closure(self):
        self.show_subtitle("整個流程的目的 —— 答案回到使用者")

        # Top: user query bubble (mirrors the opener)
        user_bub = RoundedRectangle(
            width=8.5, height=1.05, corner_radius=0.28,
            stroke_color=VIOLET, stroke_width=2.5,
            fill_color=VIOLET, fill_opacity=0.32,
        )
        user_text = Text("我家目錄底下有幾個 .py 檔？",
                         font=CN_FONT, font_size=30,
                         color=INK, weight=BOLD).move_to(user_bub.get_center())
        user_group = VGroup(user_bub, user_text).move_to(UP * 1.8)
        user_label = Text("使用者", font=CN_FONT, font_size=20,
                          color=NEUTRAL).next_to(user_group, UP, buff=0.15)

        self.play(FadeIn(user_label, shift=DOWN * 0.1),
                  FadeIn(user_group, shift=DOWN * 0.2),
                  run_time=0.6)
        self.wait(0.8)

        # Build answer bubble first (positioned but not yet shown) so we can
        # aim the connector arrow exactly at its top edge.
        ans_bub = RoundedRectangle(
            width=9.0, height=1.05, corner_radius=0.28,
            stroke_color=TEAL_BRIGHT, stroke_width=2.5,
            fill_color=TEAL_BRIGHT, fill_opacity=0.30,
        )
        ans_text = Text("你家目錄底下總共有 42 個 .py 檔。",
                        font=CN_FONT, font_size=30,
                        color=INK, weight=BOLD).move_to(ans_bub.get_center())
        ans_group = VGroup(ans_bub, ans_text).move_to(DOWN * 1.6)

        # Connector arrow that actually reaches the answer bubble's top
        connector = Arrow(
            start=user_group.get_bottom() + DOWN * 0.08,
            end=ans_group.get_top() + UP * 0.05,
            color=VIOLET_SOFT, stroke_width=4,
            buff=0.05, max_tip_length_to_length_ratio=0.10,
        )
        self.play(GrowArrow(connector), run_time=0.6)
        ans_label = Text("最終回覆", font=CN_FONT, font_size=20,
                         color=NEUTRAL).next_to(ans_group, DOWN, buff=0.15)

        self.play(FadeIn(ans_group, shift=UP * 0.2),
                  FadeIn(ans_label, shift=UP * 0.1),
                  run_time=0.6)
        self.wait(2.5)

        # Subtle highlight: pulse both bubbles together to make the loop visible
        self.play(Indicate(user_group, scale_factor=1.04, color=VIOLET),
                  Indicate(ans_group, scale_factor=1.04, color=TEAL_BRIGHT),
                  run_time=0.9)
        self.wait(1.2)

        self.play(FadeOut(user_label), FadeOut(user_group),
                  FadeOut(connector),
                  FadeOut(ans_group), FadeOut(ans_label),
                  run_time=0.5)
        self.advance_progress(86)

    # ============================================================
    # TAKEAWAY — LLM ↔ Harness split (~18s)
    # ============================================================
    def scene_takeaway(self):
        title = Text("LLM ↔ Harness 職責分工",
                     font=CN_FONT, font_size=44, color=INK,
                     weight=BOLD).move_to(UP * 3.0)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.show_subtitle("兩邊各做各的事 —— 這是 function calling 的本質")

        # Left card — LLM
        llm_card_bg = RoundedRectangle(
            width=6.8, height=4.0, corner_radius=0.22,
            stroke_color=VIOLET, stroke_width=3,
            fill_color=VIOLET, fill_opacity=0.12,
        ).move_to(LEFT * 4.0 + DOWN * 0.3)
        llm_hdr = RoundedRectangle(
            width=6.4, height=0.7, corner_radius=0.10,
            stroke_color=VIOLET, stroke_width=0,
            fill_color=VIOLET, fill_opacity=1.0,
        ).move_to(LEFT * 4.0 + UP * 1.3)
        llm_hdr_text = Text("LLM 做的事", font=CN_FONT, font_size=28,
                            color=INK, weight=BOLD).move_to(llm_hdr.get_center())
        llm_lines = VGroup(
            Text("✓  生成 tool_use JSON",        font=CN_FONT, font_size=22, color=INK),
            Text("✓  讀 schema,生 input JSON",  font=CN_FONT, font_size=22, color=INK),
            Text("✓  Constrained decoding",      font=CN_FONT, font_size=22, color=INK),
            Text("✗  不知道工具真做什麼",         font=CN_FONT, font_size=22, color=NEUTRAL),
            Text("✗  碰不到 OS、檔案、網路",      font=CN_FONT, font_size=22, color=PINK, weight=BOLD),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        llm_lines.move_to(LEFT * 4.0 + DOWN * 0.7)

        # Right card — Harness
        h_card_bg = RoundedRectangle(
            width=6.8, height=4.0, corner_radius=0.22,
            stroke_color=TEAL, stroke_width=3,
            fill_color=TEAL, fill_opacity=0.12,
        ).move_to(RIGHT * 4.0 + DOWN * 0.3)
        h_hdr = RoundedRectangle(
            width=6.4, height=0.7, corner_radius=0.10,
            stroke_color=TEAL, stroke_width=0,
            fill_color=TEAL, fill_opacity=1.0,
        ).move_to(RIGHT * 4.0 + UP * 1.3)
        h_hdr_text = Text("Harness 做的事", font=CN_FONT, font_size=28,
                          color=INK, weight=BOLD).move_to(h_hdr.get_center())
        h_lines = VGroup(
            Text("✓  解析 tool_use,真的執行",     font=CN_FONT, font_size=22, color=INK),
            Text("✓  維護 messages 陣列",         font=CN_FONT, font_size=22, color=INK),
            Text("✓  Loop 直到 end_turn",         font=CN_FONT, font_size=22, color=INK),
            Text("✓  處理 timeout / 錯誤",        font=CN_FONT, font_size=22, color=INK),
            Text("✓  加 sandbox / 安全防護",      font=CN_FONT, font_size=22, color=TEAL_BRIGHT, weight=BOLD),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        h_lines.move_to(RIGHT * 4.0 + DOWN * 0.7)

        self.play(FadeIn(llm_card_bg), FadeIn(h_card_bg), run_time=0.5)
        self.play(FadeIn(llm_hdr), FadeIn(llm_hdr_text),
                  FadeIn(h_hdr), FadeIn(h_hdr_text), run_time=0.5)
        self.play(FadeIn(llm_lines, shift=UP * 0.15),
                  FadeIn(h_lines, shift=UP * 0.15), run_time=0.8)
        self.wait(7.0)

        # Clear subtitle first so it doesn't sit underneath the transition line
        self.clear_subtitle(run_time=0.3)

        # Bottom transition line (now owns the bottom strip alone)
        trans = Text("→ MCP 在這個機制上加了什麼?把 harness ↔ tool 的協定標準化",
                     font=CN_FONT, font_size=22, color=ORANGE,
                     weight=BOLD, slant=ITALIC).move_to(DOWN * 3.4)
        self.play(FadeIn(trans, shift=UP * 0.15), run_time=0.6)
        self.wait(3.5)

        # Final fadeout
        self.play(FadeOut(title), FadeOut(llm_card_bg), FadeOut(h_card_bg),
                  FadeOut(llm_hdr), FadeOut(llm_hdr_text),
                  FadeOut(h_hdr), FadeOut(h_hdr_text),
                  FadeOut(llm_lines), FadeOut(h_lines),
                  FadeOut(trans), run_time=0.7)
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=0.3)
            self._cur_subtitle = None
        self.advance_progress(self.TOTAL_SECONDS)
        self.wait(0.5)
