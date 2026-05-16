"""
01-why-mcp-video.py

3-min long video adapted from 01-why-mcp.pptx (21 slides).
Three-act structure for course pre-class viewing.

Render:
  manim -ql --disable_caching 01-why-mcp-video.py WhyMCP    # draft
  manim -qh 01-why-mcp-video.py WhyMCP                       # final 1080p60
"""

from manim import *
import numpy as np

# ============================================================
# Violet-primary design system (aligned with 2026 slide deck + V3 video)
# ============================================================
BG          = "#0a0a10"   # 3B1B-style near-black
DEEP_BLUE   = "#065A82"   # Deep blue — secondary panels (legacy, kept)
TEAL        = "#1C7293"   # Teal — tertiary elements
INK         = "#FFFFFF"   # Primary text
NEUTRAL     = "#B4BED2"   # Secondary text, borders
BLUE        = "#5B8DE8"   # Subject / user / secondary entity (aligned w/ V2, V3)
VIOLET      = "#7B5CF5"   # LLM main subject (aligned w/ V3, slide deck)
VIOLET_SOFT = "#9D85F7"
VIOLET_DEEP = "#5B3ED9"
ORANGE      = "#E8793A"   # Accent / accumulator / tool call / breakthrough
GREEN       = "#5CB85C"   # Success / completion
RED         = "#D9534F"   # Error / warning
DIM         = "#3A4A6A"   # Dim borders

CN_FONT     = "Noto Sans CJK TC"
SERIF_FONT  = "Noto Serif CJK TC"
MONO_FONT   = "DejaVu Sans Mono"


def F(*parts, color=INK, size=64):
    return MathTex(*parts, font_size=size, color=color)


config.frame_width  = 16
config.frame_height = 9
config.pixel_width  = 1920
config.pixel_height = 1080


class WhyMCP(Scene):
    SUBTITLE_MAX_WIDTH = 14.0
    TOTAL_SECONDS = 157.6   # measured: intro hold +0.5s offset by Act transition tighten

    TITLE     = "Why MCP"
    SUBTITLE  = "LLM 為何需要一個統一協定"

    def construct(self):
        self.camera.background_color = BG
        self._cur_subtitle = None
        self._init_progress_bar()

        self.scene_intro()        # 0:00–0:04
        self.scene_act1()         # 0:04–0:39
        self.scene_act2()         # 0:39–1:59
        self.scene_act3()         # 1:59–2:54
        self.scene_outro()        # 2:54–3:05

    # ------------------------------------------------------------
    # Progress bar
    # ------------------------------------------------------------
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

    # ------------------------------------------------------------
    # Subtitle system
    # ------------------------------------------------------------
    def _build_subtitle(self, text):
        sub = Text(text, font=CN_FONT, font_size=30, color=INK, weight=MEDIUM)
        if sub.width > self.SUBTITLE_MAX_WIDTH:
            sub.scale_to_fit_width(self.SUBTITLE_MAX_WIDTH)
        sub.to_edge(DOWN, buff=0.7)
        return sub

    def show_subtitle(self, text, run_time=0.35):
        # Sequential fade — out fully before in, prevents 0.15s visual ghost
        # of two subtitles overlaying during cross-fade (R6-P0 fix).
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

    # ------------------------------------------------------------
    # Helper: act group cleanup
    # ------------------------------------------------------------
    def end_act(self, act_group, run_time=0.5):
        fade_targets = [act_group]
        if self._cur_subtitle is not None:
            fade_targets.append(self._cur_subtitle)
            self._cur_subtitle = None
        self.play(*[FadeOut(m) for m in fade_targets], run_time=run_time)
        self.remove(act_group)

    # ------------------------------------------------------------
    # Helper: L-arrow
    # ------------------------------------------------------------
    def make_l_arrow(self, start, end, bend='V', color=DIM,
                     stroke_width=2.0,
                     max_tip_length_to_length_ratio=0.10):
        s = np.array(start, dtype=float) if not isinstance(start, np.ndarray) else start
        e = np.array(end, dtype=float) if not isinstance(end, np.ndarray) else end
        if bend == 'V':
            corner = np.array([s[0], e[1], 0.0])
        else:
            corner = np.array([e[0], s[1], 0.0])
        seg1 = Line(start=s, end=corner, color=color, stroke_width=stroke_width)
        seg2 = Arrow(start=corner, end=e, color=color, stroke_width=stroke_width,
                     buff=0, max_tip_length_to_length_ratio=max_tip_length_to_length_ratio)
        return VGroup(seg1, seg2)

    # ------------------------------------------------------------
    # Helper: rounded box with centered label
    # ------------------------------------------------------------
    def make_box(self, label, width=2.0, height=0.9, color=BLUE,
                 fill_op=0.15, label_size=24, weight=MEDIUM, label_color=None):
        if label_color is None:
            label_color = INK
        box = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                               stroke_color=color, stroke_width=2.5,
                               fill_color=color, fill_opacity=fill_op)
        txt = Text(label, font=CN_FONT, font_size=label_size,
                   color=label_color, weight=weight)
        if txt.width > width - 0.3:
            txt.scale_to_fit_width(width - 0.3)
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    # ============================================================
    # INTRO (5s) — magazine-style cover: undraw illustration + title
    # ============================================================
    def scene_intro(self):
        # ── Right side: hero illustration (undraw "thought-process") ──
        hero = SVGMobject(
            "intro-assets/undraw_thought-process.svg",
        ).scale_to_fit_height(5.6)
        hero.move_to(RIGHT * 3.6 + DOWN * 0.1)

        # ── Left side: title stack ──
        title_lines = VGroup(
            Text("Why", font=SERIF_FONT, font_size=110,
                 color=INK, weight=BOLD),
            Text("MCP", font=SERIF_FONT, font_size=110,
                 color=INK, weight=BOLD),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        kicker = Text("章節 01", font=MONO_FONT, font_size=18,
                      color=VIOLET, weight=BOLD).next_to(
                          title_lines, UP, buff=0.30, aligned_edge=LEFT)
        accent = Line(start=LEFT * 0.0, end=RIGHT * 1.8,
                      color=VIOLET, stroke_width=5).next_to(
                          title_lines, DOWN, buff=0.30, aligned_edge=LEFT)
        sub = Text("LLM 為何需要\n一個統一協定",
                   font=CN_FONT, font_size=26, color=NEUTRAL,
                   line_spacing=1.1).next_to(
                       accent, DOWN, buff=0.30, aligned_edge=LEFT)
        title_stack = VGroup(kicker, title_lines, accent, sub).move_to(
            LEFT * 4.2 + UP * 0.1)

        # Phase 1: hero fades in with slight initial scale (0–0.9s)
        hero.scale(0.95)
        self.play(FadeIn(hero), run_time=0.9)

        # Phase 2: title stack appears (kicker → title → accent → sub)
        self.play(FadeIn(kicker, shift=DOWN * 0.1), run_time=0.3)
        self.play(FadeIn(title_lines, shift=UP * 0.15), run_time=0.6)
        self.play(GrowFromEdge(accent, LEFT), run_time=0.3)
        self.play(FadeIn(sub, shift=UP * 0.10), run_time=0.4)

        # Phase 3: slow Ken Burns + true hold so audience reads the stack
        self.play(hero.animate.scale(1.05 / 0.95).shift(LEFT * 0.15),
                  rate_func=linear, run_time=1.4)
        self.wait(1.0)

        # Phase 4: fade out
        self.play(FadeOut(hero), FadeOut(title_stack), run_time=0.5)
        self.advance_progress(5.6)

    # ============================================================
    # ACT 1 — LLM 的三道牆 (0:04–0:39, 35s)
    # ============================================================
    def scene_act1(self):
        act_badge = self._make_act_badge("ACT 1")

        # Beat 1.1 — Hook: 教師問 LLM，LLM 答不出 (10s)
        question_box = self.make_box("「興大圖書館有哪些 AI 相關的書？」",
                                     width=7.0, height=1.0,
                                     color=BLUE, fill_op=0.18, label_size=26)
        question_box.move_to(UP * 2.2)

        teacher_label = Text("教師", font=CN_FONT, font_size=22,
                             color=NEUTRAL).next_to(question_box, LEFT, buff=0.3)

        llm_circle = Circle(radius=0.7, color=VIOLET, fill_opacity=0.25,
                            stroke_width=3).move_to(DOWN * 0.3 + LEFT * 5.5)
        llm_label = Text("LLM", font=CN_FONT, font_size=28, color=INK,
                         weight=BOLD).move_to(llm_circle.get_center())

        # 編造書名（幻覺）—比「我不知道」更有教學張力
        answer_lines = VGroup(
            Text("《AI 概論導讀》", font=CN_FONT, font_size=24,
                 color=INK, weight=MEDIUM),
            Text("《機器學習入門》", font=CN_FONT, font_size=24,
                 color=INK, weight=MEDIUM),
            Text("《深度學習實作》...", font=CN_FONT, font_size=24,
                 color=INK, weight=MEDIUM),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        answer_box_outer = RoundedRectangle(
            width=6.0, height=answer_lines.height + 0.6,
            corner_radius=0.15, stroke_color=NEUTRAL, stroke_width=2,
            fill_color=NEUTRAL, fill_opacity=0.08,
        )
        answer_lines.move_to(answer_box_outer.get_center())
        answer_box = VGroup(answer_box_outer, answer_lines)
        answer_box.move_to(DOWN * 0.6 + RIGHT * 1.5)

        red_x = Cross(stroke_color=RED, stroke_width=8).scale(0.45).move_to(
            answer_box.get_right() + RIGHT * 0.6
        )
        hallucination_lbl = Text("← 這些書根本不存在（幻覺）",
                                 font=CN_FONT, font_size=22,
                                 color=RED, weight=BOLD)
        hallucination_lbl.next_to(answer_box, DOWN, buff=0.4)

        self.play(FadeIn(act_badge), run_time=0.3)
        self.show_subtitle("LLM 很強，但有些問題它會「編造」")
        self.play(FadeIn(teacher_label), FadeIn(question_box), run_time=0.7)
        self.wait(3.0)
        self.play(FadeIn(llm_circle), FadeIn(llm_label), run_time=0.5)
        self.play(FadeIn(answer_box), run_time=0.7)
        self.play(Write(red_x), run_time=0.4)
        self.play(FadeIn(hallucination_lbl, shift=UP * 0.15), run_time=0.5)
        self.wait(4.5)
        # 一次深出所有 hook 元素（不再 transform LLM 到頂部）
        self.play(FadeOut(question_box), FadeOut(teacher_label),
                  FadeOut(answer_box), FadeOut(red_x),
                  FadeOut(hallucination_lbl),
                  FadeOut(llm_circle), FadeOut(llm_label),
                  run_time=0.8)

        # Beat 1.2 — 三道紅牆 (15s)
        self.show_subtitle("這背後是 LLM 的三道牆")

        wall_data = [
            ("知識截止日", "訓練資料\n停在某個日期"),
            ("沒有私有資料", "不知道你的課表、\n圖書館藏書"),
            ("不能執行動作", "只能說話，\n不能幫你加退選"),
        ]
        walls = VGroup()
        for i, (head, body) in enumerate(wall_data):
            wall_box = RoundedRectangle(width=3.8, height=3.0, corner_radius=0.2,
                                        stroke_color=RED, stroke_width=3,
                                        fill_color=RED, fill_opacity=0.12)
            head_t = Text(head, font=CN_FONT, font_size=28,
                          color=INK, weight=BOLD).move_to(wall_box.get_top() + DOWN * 0.7)
            body_t = Text(body, font=CN_FONT, font_size=20,
                          color=NEUTRAL, weight=MEDIUM, line_spacing=0.8)
            body_t.move_to(wall_box.get_center() + DOWN * 0.4)
            wall = VGroup(wall_box, head_t, body_t)
            walls.add(wall)
        walls.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.4)

        for w in walls:
            self.play(FadeIn(w, shift=UP * 0.2), run_time=0.7)
        self.wait(13.0)

        # Beat 1.3 — 核心問句 (10s)
        question = Text("如何讓 LLM 接上外部世界？",
                        font=CN_FONT, font_size=58, color=ORANGE, weight=BOLD)
        question.move_to(ORIGIN)

        self.play(
            FadeOut(walls),
            FadeOut(llm_circle), FadeOut(llm_label),
            run_time=0.7,
        )
        self.show_subtitle("核心問題")
        self.play(Write(question), run_time=1.4)
        self.wait(8.5)

        # Cleanup act 1
        act1_group = VGroup(question, act_badge)
        self.end_act(act1_group, run_time=0.7)
        self.advance_progress(36)

    # ============================================================
    # ACT 2 — 兩條外掛 + N×M 撞牆 (0:39–1:59, 80s)
    # ============================================================
    def scene_act2(self):
        act_badge = self._make_act_badge("ACT 2")

        # === Beat 2.1 RAG (25s) ===
        # Bundle badge + title into one play to tighten Act 1→2 transition
        rag_title = Text("策略 A：RAG（檢索增強生成）",
                         font=CN_FONT, font_size=34,
                         color=INK, weight=BOLD).move_to(UP * 3.2)
        self.show_subtitle("先讓 LLM「讀文件」")
        self.play(FadeIn(act_badge),
                  FadeIn(rag_title, shift=DOWN * 0.2),
                  run_time=0.5)

        # RAG pipeline boxes
        doc_box = self.make_box("校內文件", width=2.0, height=1.0,
                                color=BLUE, fill_op=0.18, label_size=22)
        chunk_box = self.make_box("切片", width=1.5, height=1.0,
                                  color=BLUE, fill_op=0.18, label_size=22)
        embed_box = self.make_box("向量化", width=1.8, height=1.0,
                                  color=BLUE, fill_op=0.18, label_size=22)
        vdb_box = self.make_box("向量資料庫", width=2.4, height=1.0,
                                color=BLUE, fill_op=0.18, label_size=22)
        topk_box = self.make_box("Top-K 文件", width=2.2, height=1.0,
                                 color=ORANGE, fill_op=0.20, label_size=22)
        llm_box = self.make_box("LLM", width=1.6, height=1.0,
                                color=GREEN, fill_op=0.22, label_size=24,
                                weight=BOLD)

        pipeline = VGroup(doc_box, chunk_box, embed_box, vdb_box, topk_box, llm_box)
        pipeline.arrange(RIGHT, buff=0.35).move_to(UP * 0.8)

        arrows = VGroup()
        for i in range(len(pipeline) - 1):
            a = Arrow(start=pipeline[i].get_right(),
                      end=pipeline[i + 1].get_left(),
                      color=NEUTRAL, stroke_width=2,
                      buff=0.05,
                      max_tip_length_to_length_ratio=0.25)
            arrows.add(a)

        for i, box in enumerate(pipeline):
            self.play(FadeIn(box, shift=RIGHT * 0.2), run_time=0.35)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.25)

        # answer pops — anchor under the whole pipeline (not just llm_box)
        # so the group stays inside the frame.
        ans = Text("「圖書館有 12 本 AI 相關書」",
                   font=CN_FONT, font_size=26, color=GREEN, weight=BOLD)
        check = Text("✓", font=MONO_FONT, font_size=40, color=GREEN, weight=BOLD)
        ans_group = VGroup(ans, check).arrange(RIGHT, buff=0.3).next_to(
            pipeline, DOWN, buff=0.6
        )

        self.play(FadeIn(ans_group, shift=UP * 0.2), run_time=0.6)
        self.show_subtitle("RAG 把私有文件塞進 prompt，解了知識問題")
        self.wait(5.0)

        # but cannot execute action
        warn = Text("但不能幫你加退選", font=CN_FONT, font_size=28,
                    color=RED, weight=BOLD).next_to(ans_group, DOWN, buff=0.5)
        self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.5)
        self.wait(6.5)

        # cleanup RAG
        rag_group = VGroup(rag_title, pipeline, arrows, ans_group, warn)
        self.play(FadeOut(rag_group), run_time=0.6)

        # === Beat 2.2 Tool Use (30s) ===
        tu_title = Text("策略 B：Tool Use（工具呼叫）",
                        font=CN_FONT, font_size=34,
                        color=INK, weight=BOLD).move_to(UP * 3.2)
        self.show_subtitle("給 LLM 一組「工具」")
        self.play(FadeIn(tu_title, shift=DOWN * 0.2), run_time=0.5)

        # LLM in the middle (main subject — violet per design system)
        llm_circle = Circle(radius=1.0, color=VIOLET, fill_opacity=0.20,
                            stroke_width=3).move_to(ORIGIN)
        llm_lbl = Text("LLM", font=CN_FONT, font_size=34, color=INK,
                       weight=BOLD).move_to(llm_circle.get_center())

        # toolbox
        tool_data = [
            ("search_books()", LEFT * 4 + UP * 1.5),
            ("enroll_course()", LEFT * 4 + DOWN * 0.0),
            ("check_class()", LEFT * 4 + DOWN * 1.5),
        ]
        tools = VGroup()
        tool_lines = VGroup()
        for name, pos in tool_data:
            t = self.make_box(name, width=2.6, height=0.8,
                              color=TEAL, fill_op=0.22, label_size=20)
            t.move_to(pos)
            tools.add(t)
            line = Line(start=t.get_right(),
                        end=llm_circle.get_left() + LEFT * 0.05,
                        color=NEUTRAL, stroke_width=1.5)
            tool_lines.add(line)

        # data sources on right
        ds_data = [
            ("圖書館 DB", RIGHT * 4 + UP * 1.5),
            ("課程系統", RIGHT * 4 + DOWN * 0.0),
            ("教師資料", RIGHT * 4 + DOWN * 1.5),
        ]
        ds = VGroup()
        ds_lines = VGroup()
        for name, pos in ds_data:
            d = self.make_box(name, width=2.4, height=0.8,
                              color=BLUE, fill_op=0.22, label_size=20)
            d.move_to(pos)
            ds.add(d)
            line = Line(start=llm_circle.get_right() + RIGHT * 0.05,
                        end=d.get_left(),
                        color=NEUTRAL, stroke_width=1.5)
            ds_lines.add(line)

        self.play(FadeIn(llm_circle), FadeIn(llm_lbl), run_time=0.5)
        self.play(*[FadeIn(t, shift=RIGHT * 0.2) for t in tools], run_time=0.7)
        self.play(*[Create(l) for l in tool_lines], run_time=0.5)
        self.play(*[FadeIn(d, shift=LEFT * 0.2) for d in ds], run_time=0.7)
        self.play(*[Create(l) for l in ds_lines], run_time=0.5)

        self.show_subtitle("LLM 自主選工具、呼叫 API，能執行動作")
        self.wait(5.0)

        # highlight one path: enroll_course
        self.play(
            tools[1][0].animate.set_stroke(ORANGE, width=4).set_fill(ORANGE, opacity=0.35),
            tool_lines[1].animate.set_stroke(ORANGE, width=5),
            ds_lines[1].animate.set_stroke(ORANGE, width=5),
            ds[1][0].animate.set_stroke(ORANGE, width=4).set_fill(ORANGE, opacity=0.35),
            run_time=0.8,
        )
        ok_text = Text("✓ 動作完成", font=CN_FONT, font_size=24,
                       color=GREEN, weight=BOLD).move_to(llm_circle.get_top() + UP * 0.6)
        self.play(FadeIn(ok_text), run_time=0.4)
        self.wait(4.0)

        # but pain point coming — placed BELOW the diagram, not overlapping tools/ds
        self.play(FadeOut(ok_text), run_time=0.3)
        pain_q = Text("問題是：每個 App 都要重做一次整合",
                      font=CN_FONT, font_size=30, color=RED,
                      weight=BOLD)
        pain_q.move_to(DOWN * 3.0)   # 移到畫面底部，避開 check_class 與 教師資料
        self.play(FadeIn(pain_q, shift=UP * 0.15), run_time=0.6)
        self.show_subtitle("如果學校有 4 個 App、3 個資料源呢？")
        self.wait(7.5)

        # cleanup tool use
        tu_group = VGroup(tu_title, llm_circle, llm_lbl, tools, tool_lines,
                          ds, ds_lines, pain_q)
        self.play(FadeOut(tu_group), run_time=0.6)

        # === Beat 2.3 N×M 痛點 (25s) ===
        nm_title = Text("痛點：N × M 整合爆炸",
                        font=CN_FONT, font_size=36,
                        color=RED, weight=BOLD).move_to(UP * 3.2)
        self.show_subtitle("4 個 App × 3 個資料源 = 12 條整合工作")
        self.play(FadeIn(nm_title, shift=DOWN * 0.2), run_time=0.5)

        # 4 apps on left
        apps_data = ["ChatGPT", "Claude", "Gemini", "自建 Agent"]
        apps = VGroup()
        for i, name in enumerate(apps_data):
            a = self.make_box(name, width=2.4, height=0.8,
                              color=BLUE, fill_op=0.22, label_size=22)
            apps.add(a)
        apps.arrange(DOWN, buff=0.35).move_to(LEFT * 4.5 + DOWN * 0.3)

        # 3 sources on right
        srcs_data = ["圖書館 DB", "課程系統", "教師資料"]
        srcs = VGroup()
        for i, name in enumerate(srcs_data):
            s = self.make_box(name, width=2.4, height=0.8,
                              color=TEAL, fill_op=0.22, label_size=22)
            srcs.add(s)
        srcs.arrange(DOWN, buff=0.7).move_to(RIGHT * 4.5 + DOWN * 0.3)

        self.play(*[FadeIn(a, shift=RIGHT * 0.2) for a in apps], run_time=0.7)
        self.play(*[FadeIn(s, shift=LEFT * 0.2) for s in srcs], run_time=0.7)

        # 12 red lines (chaos)
        nm_lines = VGroup()
        for a in apps:
            for s in srcs:
                l = Line(start=a.get_right(), end=s.get_left(),
                         color=RED, stroke_width=2.0, stroke_opacity=0.6)
                nm_lines.add(l)

        # animate lines appearing in bursts
        for i in range(0, 12, 3):
            self.play(*[Create(nm_lines[j]) for j in range(i, min(i + 3, 12))],
                      run_time=0.4)

        # counter
        counter = Text("12 條整合", font=CN_FONT, font_size=44,
                       color=RED, weight=BOLD).move_to(DOWN * 2.4)
        self.play(FadeIn(counter, shift=UP * 0.2), run_time=0.4)
        self.show_subtitle("學校撐不住這麼多整合工作")
        self.wait(11.0)

        # cleanup act 2
        act2_group = VGroup(nm_title, apps, srcs, nm_lines, counter, act_badge)
        self.end_act(act2_group, run_time=0.7)
        self.advance_progress(111)

    # ============================================================
    # ACT 3 — MCP 解耦 (1:59–2:54, 55s)
    # ============================================================
    def scene_act3(self):
        act_badge = self._make_act_badge("ACT 3")

        # === Beat 3.1 N×M → N+M (15s) ===
        # Bundle badge + title into one play to tighten Act 2→3 transition
        title = Text("策略 C：MCP — 統一協定解耦",
                     font=CN_FONT, font_size=36,
                     color=ORANGE, weight=BOLD).move_to(UP * 3.2)
        self.show_subtitle("加一層 MCP，把 N×M 變成 N+M")
        self.play(FadeIn(act_badge),
                  FadeIn(title, shift=DOWN * 0.2),
                  run_time=0.5)

        # 4 apps left
        apps_data = ["ChatGPT", "Claude", "Gemini", "自建 Agent"]
        apps = VGroup()
        for name in apps_data:
            a = self.make_box(name, width=2.2, height=0.7,
                              color=BLUE, fill_op=0.22, label_size=20)
            apps.add(a)
        apps.arrange(DOWN, buff=0.3).move_to(LEFT * 5.0 + DOWN * 0.3)

        # MCP layer in middle
        mcp_layer = RoundedRectangle(width=2.4, height=4.5, corner_radius=0.25,
                                     stroke_color=ORANGE, stroke_width=4,
                                     fill_color=ORANGE, fill_opacity=0.18)
        mcp_layer.move_to(DOWN * 0.3)
        mcp_lbl_top = Text("MCP", font=CN_FONT, font_size=44,
                           color=INK, weight=BOLD).move_to(mcp_layer.get_top() + DOWN * 0.7)
        mcp_lbl_bot = Text("統一協定", font=CN_FONT, font_size=22,
                           color=NEUTRAL).move_to(mcp_lbl_top.get_center() + DOWN * 0.7)
        mcp_lbl_proto = Text("JSON-RPC 2.0", font=MONO_FONT, font_size=18,
                             color=NEUTRAL).move_to(mcp_layer.get_bottom() + UP * 0.5)

        # 3 sources right
        srcs_data = ["圖書館 DB", "課程系統", "教師資料"]
        srcs = VGroup()
        for name in srcs_data:
            s = self.make_box(name, width=2.2, height=0.7,
                              color=TEAL, fill_op=0.22, label_size=20)
            srcs.add(s)
        srcs.arrange(DOWN, buff=0.55).move_to(RIGHT * 5.0 + DOWN * 0.3)

        self.play(*[FadeIn(a, shift=RIGHT * 0.2) for a in apps],
                  *[FadeIn(s, shift=LEFT * 0.2) for s in srcs],
                  run_time=0.6)
        self.play(FadeIn(mcp_layer), FadeIn(mcp_lbl_top),
                  FadeIn(mcp_lbl_bot), FadeIn(mcp_lbl_proto), run_time=0.6)

        # 4 lines left + 3 lines right = 7 lines (clean)
        left_lines = VGroup()
        for a in apps:
            l = Line(start=a.get_right(), end=mcp_layer.get_left(),
                     color=GREEN, stroke_width=2.5, stroke_opacity=0.85)
            left_lines.add(l)
        right_lines = VGroup()
        for s in srcs:
            l = Line(start=mcp_layer.get_right(), end=s.get_left(),
                     color=GREEN, stroke_width=2.5, stroke_opacity=0.85)
            right_lines.add(l)

        self.play(*[Create(l) for l in left_lines], run_time=0.5)
        self.play(*[Create(l) for l in right_lines], run_time=0.5)

        contrast = Text("12 → 7（N×M → N+M）", font=CN_FONT, font_size=36,
                        color=GREEN, weight=BOLD).move_to(DOWN * 2.5)
        self.play(FadeIn(contrast, shift=UP * 0.2), run_time=0.5)
        self.wait(6.0)

        # cleanup — fade the whole decoupling figure including MCP layer.
        # (Earlier version shrank mcp_layer to top as a persistent anchor,
        # but the next beats never interacted with it so it ended up as
        # decoration debris distracting from the new hero visual.)
        decoupling_group = VGroup(title, apps, srcs, left_lines, right_lines,
                                  contrast, mcp_lbl_proto,
                                  mcp_layer, mcp_lbl_top, mcp_lbl_bot)
        self.play(FadeOut(decoupling_group), run_time=0.7)

        # === Beat 3.2 四大角色 (20s) ===
        title2 = Text("MCP 的四個角色",
                      font=CN_FONT, font_size=32,
                      color=INK, weight=BOLD).move_to(UP * 0.7)
        self.show_subtitle("四層分工：介面 → 協定 → 工具方 → 能力")
        self.play(FadeIn(title2), run_time=0.5)

        # P1 refine: 每個角色加具體例子，幫教師受眾建立心智模型
        role_data = [
            ("Host",   "Claude Desktop",   BLUE),
            ("Client", "Host 內部組件",     TEAL),
            ("Server", "MCP server",       ORANGE),
            ("Tool",   "search_books()",   GREEN),
        ]
        roles = VGroup()
        for name, desc, c in role_data:
            box = RoundedRectangle(width=2.95, height=1.85, corner_radius=0.18,
                                   stroke_color=c, stroke_width=3,
                                   fill_color=c, fill_opacity=0.18)
            n = Text(name, font=CN_FONT, font_size=28, color=INK,
                     weight=BOLD).move_to(box.get_top() + DOWN * 0.55)
            d_lbl = Text("如：", font=CN_FONT, font_size=20, color=INK,
                         weight=MEDIUM)
            d_val = Text(desc, font=MONO_FONT if "(" in desc else CN_FONT,
                         font_size=22, color=INK, weight=MEDIUM)
            d = VGroup(d_lbl, d_val).arrange(RIGHT, buff=0.15)
            d.move_to(box.get_center() + DOWN * 0.35)
            roles.add(VGroup(box, n, d))
        roles.arrange(RIGHT, buff=0.30).move_to(DOWN * 1.4)

        arrows_between = VGroup()
        for i in range(len(roles) - 1):
            ar = Arrow(start=roles[i].get_right() + LEFT * 0.05,
                       end=roles[i + 1].get_left() + RIGHT * 0.05,
                       color=NEUTRAL, stroke_width=2,
                       buff=0.05,
                       max_tip_length_to_length_ratio=0.25)
            arrows_between.add(ar)

        for i, r in enumerate(roles):
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.4)
            if i < len(arrows_between):
                self.play(GrowArrow(arrows_between[i]), run_time=0.25)
        self.wait(7.0)

        # cleanup roles
        roles_group = VGroup(title2, roles, arrows_between)
        self.play(FadeOut(roles_group), run_time=0.5)

        # === Beat 3.3 USB-C 譬喻 (10s) ===
        # Big icon: just a stylized "USB-C-like" shape with label
        usbc_box = RoundedRectangle(width=4.5, height=1.6, corner_radius=0.8,
                                    stroke_color=ORANGE, stroke_width=5,
                                    fill_color=ORANGE, fill_opacity=0.15)
        usbc_inner = RoundedRectangle(width=3.5, height=0.9, corner_radius=0.45,
                                      stroke_color=ORANGE, stroke_width=3,
                                      fill_color=BG, fill_opacity=1)
        usbc_inner.move_to(usbc_box.get_center())
        usbc_lbl = Text("USB-C", font=MONO_FONT, font_size=26,
                        color=ORANGE, weight=BOLD).move_to(usbc_inner.get_center())
        usbc_group = VGroup(usbc_box, usbc_inner, usbc_lbl).move_to(LEFT * 3.5 + DOWN * 0.3)

        arrow_eq = Text("≈", font=MONO_FONT, font_size=80, color=INK,
                        weight=BOLD).move_to(DOWN * 0.3)

        mcp_meta = Text("MCP\n（LLM 世界的統一介面）",
                        font=CN_FONT, font_size=36, color=ORANGE,
                        weight=BOLD, line_spacing=0.9)
        mcp_meta.move_to(RIGHT * 3.5 + DOWN * 0.3)

        self.show_subtitle("一個協定，接所有 App 與所有資料源")
        self.play(FadeIn(usbc_group, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(arrow_eq), run_time=0.3)
        self.play(FadeIn(mcp_meta, shift=LEFT * 0.3), run_time=0.6)
        self.wait(5.0)

        # cleanup usbc
        usbc_full = VGroup(usbc_group, arrow_eq, mcp_meta)
        self.play(FadeOut(usbc_full), run_time=0.5)

        # === Beat 3.4 興大 AI 學伴案例 (10s) ===
        case_title = Text("實際案例：興大 AI 學伴",
                          font=CN_FONT, font_size=36,
                          color=INK, weight=BOLD).move_to(DOWN * 0.3 + UP * 0.3)

        stats = VGroup(
            VGroup(
                Text("33", font=MONO_FONT, font_size=84, color=ORANGE, weight=BOLD),
                Text("個 MCP 工具", font=CN_FONT, font_size=24, color=NEUTRAL),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("9", font=MONO_FONT, font_size=84, color=ORANGE, weight=BOLD),
                Text("大分類", font=CN_FONT, font_size=24, color=NEUTRAL),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("1", font=MONO_FONT, font_size=84, color=GREEN, weight=BOLD),
                Text("套統一協定", font=CN_FONT, font_size=24, color=NEUTRAL),
            ).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.3).move_to(DOWN * 1.5)

        self.show_subtitle("33 個工具 × 1 套協定")
        self.play(FadeIn(case_title, shift=DOWN * 0.2), run_time=0.5)
        for s in stats:
            self.play(FadeIn(s, shift=UP * 0.2), run_time=0.4)
        self.wait(6.0)

        # cleanup act 3 — mcp_layer / mcp_lbl_* already faded in Beat 3.1
        act3_group = VGroup(case_title, stats, act_badge)
        self.end_act(act3_group, run_time=0.5)
        self.advance_progress(149)

    # ============================================================
    # OUTRO — 三點回顧 (2:54–3:05, 11s)
    # ============================================================
    def scene_outro(self):
        outro_title = Text("今天我們看到三件事",
                           font=CN_FONT, font_size=42,
                           color=INK, weight=BOLD).move_to(UP * 3.0)

        def make_point(num_str, label_str, content_str, content_color=ORANGE):
            num = Text(num_str, font=MONO_FONT, font_size=56,
                       color=BLUE, weight=BOLD)
            label = Text(label_str, font=CN_FONT, font_size=30,
                         color=INK, weight=BOLD)
            content = Text(content_str, font=CN_FONT, font_size=28,
                           color=content_color, weight=BOLD)
            return VGroup(num, label, content).arrange(RIGHT, buff=0.5)

        points = VGroup(
            make_point("①", "LLM 三道牆",
                       "知識截止 / 沒有私有資料 / 不能執行動作"),
            make_point("②", "三條延伸",
                       "RAG / Tool Use / MCP 三條路"),
            make_point("③", "MCP 的價值",
                       "N×M → N+M：把整合工作從爆炸變線性"),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(DOWN * 0.3)

        self.play(FadeIn(outro_title, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.5)
        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(2.2)

        self.wait(2.5)

        # Closing hero shot — give the audience one image to remember
        self.play(FadeOut(outro_title), FadeOut(points), run_time=0.5)
        hero_eq = Text("N × M    →    N + M",
                       font=SERIF_FONT, font_size=110,
                       color=INK, weight=BOLD).move_to(UP * 0.5)
        hero_line = Line(start=LEFT * 3.0, end=RIGHT * 3.0,
                         color=VIOLET, stroke_width=5).move_to(DOWN * 0.5)
        hero_sub = Text("MCP 把整合工作從爆炸變線性",
                        font=CN_FONT, font_size=32, color=VIOLET_SOFT,
                        weight=MEDIUM).move_to(DOWN * 1.2)
        self.play(FadeIn(hero_eq, shift=DOWN * 0.2), run_time=0.7)
        self.play(GrowFromCenter(hero_line), run_time=0.3)
        self.play(FadeIn(hero_sub, shift=UP * 0.15), run_time=0.5)
        self.wait(2.5)
        self.advance_progress(self.TOTAL_SECONDS)
        self.wait(0.5)

    # ============================================================
    # Helper: ACT N badge (top-right anchor)
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
