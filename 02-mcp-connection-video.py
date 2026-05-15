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

# Ocean Gradient palette (per repo style guide)
BG          = "#0a0a10"   # 3B1B-style near-black (was Ocean Navy #1E2761)
DEEP_BLUE   = "#065A82"
TEAL        = "#1C7293"
INK         = "#FFFFFF"
NEUTRAL     = "#B4BED2"
BLUE        = "#4A90D9"
ORANGE      = "#E8793A"
GREEN       = "#5CB85C"
RED         = "#D9534F"
DIM         = "#3A4A6A"

CN_FONT     = "Noto Sans CJK TC"
SERIF_FONT  = "Noto Serif CJK TC"
MONO_FONT   = "DejaVu Sans Mono"

config.frame_width  = 16
config.frame_height = 9
config.pixel_width  = 1920
config.pixel_height = 1080


class MCPConnection(Scene):
    SUBTITLE_MAX_WIDTH = 14.0
    TOTAL_SECONDS = 129.0

    TITLE     = "MCP 握手"
    SUBTITLE  = "父子程序怎麼開始講話"

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
        self.scene_act1()         # 0:04–0:25
        self.scene_act2()         # 0:25–1:13
        self.scene_act3()         # 1:13–1:51
        self.scene_outro()        # 1:51–2:09

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
    # Helper: process box
    # ============================================================
    def make_process_box(self, label_top, label_bot, color, pos):
        """Process box with two-line label."""
        box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.18,
                               stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=0.18)
        top = Text(label_top, font=CN_FONT, font_size=26, color=INK,
                   weight=BOLD).move_to(box.get_top() + DOWN * 0.45)
        bot = Text(label_bot, font=MONO_FONT, font_size=18,
                   color=NEUTRAL).move_to(box.get_center() + DOWN * 0.25)
        group = VGroup(box, top, bot).move_to(pos)
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
    # INTRO (4s)
    # ============================================================
    def scene_intro(self):
        title = Text(self.TITLE, font=SERIF_FONT, font_size=120,
                     color=INK, weight=BOLD).move_to(UP * 0.6)
        subtitle = Text(self.SUBTITLE, font=CN_FONT, font_size=38,
                        color=NEUTRAL).move_to(DOWN * 0.9)
        accent = Line(start=LEFT * 1.5, end=RIGHT * 1.5,
                      color=ORANGE, stroke_width=3).move_to(DOWN * 0.2)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.9)
        self.play(GrowFromCenter(accent), run_time=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.5)
        self.wait(1.7)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(accent),
                  run_time=0.5)
        self.advance_progress(4)

    # ============================================================
    # ACT 1 — spawn (35s)
    # ============================================================
    def scene_act1(self):
        act_badge = self._make_act_badge("ACT 1")
        self.play(FadeIn(act_badge), run_time=0.3)

        # Beat 1.1 — Hook: 父子兩個程序怎麼開始講話？(10s)
        question = Text("父程序怎麼跟子程序講話？",
                        font=CN_FONT, font_size=44, color=ORANGE, weight=BOLD)
        question.move_to(UP * 0.5)
        self.show_subtitle("Host 端的 Node.js × MCP Server 的 Python")
        self.play(Write(question), run_time=1.2)
        self.wait(7.5)
        self.play(FadeOut(question), run_time=0.4)

        # Beat 1.2 — spawn + stdio pipe (15s)
        self.parent_box = self.make_process_box(
            "父程序", "Node.js", BLUE, LEFT * 4.5 + UP * 0.8)
        self.child_box = self.make_process_box(
            "子程序", "Python MCP Server", TEAL, RIGHT * 4.5 + UP * 0.8)

        spawn_call = Text("spawn(config.command, config.args)",
                          font=MONO_FONT, font_size=20,
                          color=ORANGE).move_to(UP * 2.7)

        self.play(FadeIn(self.parent_box, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(spawn_call, shift=DOWN * 0.2), run_time=0.4)
        self.show_subtitle("父程序用 spawn() 開一個子程序")
        self.wait(3.5)

        # child box appears
        self.play(FadeIn(self.child_box, shift=LEFT * 0.3), run_time=0.6)

        # stdio pipe (two lines)
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
        pipe_lbl_top = Text("stdout", font=MONO_FONT, font_size=16,
                            color=NEUTRAL).move_to(
            (self.parent_box.get_right() + self.child_box.get_left()) / 2 + UP * 0.55
        )
        pipe_lbl_bot = Text("stdin", font=MONO_FONT, font_size=16,
                            color=NEUTRAL).move_to(
            (self.parent_box.get_right() + self.child_box.get_left()) / 2 + DOWN * 0.55
        )

        self.play(Create(self.pipe_top), Create(self.pipe_bot), run_time=0.7)
        self.play(FadeIn(pipe_lbl_top), FadeIn(pipe_lbl_bot), run_time=0.4)
        self.show_subtitle("stdio 用 pipe 串通：父寫 stdin，子回 stdout")
        self.wait(7.5)

        # cleanup act 1 visuals, keep parent/child + pipes for act 2
        self.play(
            FadeOut(spawn_call),
            FadeOut(pipe_lbl_top), FadeOut(pipe_lbl_bot),
            run_time=0.5,
        )
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=0.3)
            self._cur_subtitle = None
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(25)

    # ============================================================
    # ACT 2 — handshake (75s)
    # ============================================================
    def scene_act2(self):
        act_badge = self._make_act_badge("ACT 2")
        self.play(FadeIn(act_badge), run_time=0.3)

        # State panel — shows ready / isConnected flags
        state_box = RoundedRectangle(width=4.0, height=1.1, corner_radius=0.12,
                                     stroke_color=DIM, stroke_width=1.5,
                                     fill_color=BG, fill_opacity=0.5)
        state_box.move_to(DOWN * 1.6)

        ready_lbl = Text("ready", font=MONO_FONT, font_size=20,
                         color=NEUTRAL)
        ready_val = Text("false", font=MONO_FONT, font_size=20,
                         color=RED, weight=BOLD)
        ready_row = VGroup(ready_lbl, ready_val).arrange(RIGHT, buff=0.4)
        ready_row.move_to(state_box.get_center() + UP * 0.22)

        conn_lbl = Text("isConnected", font=MONO_FONT, font_size=20,
                        color=NEUTRAL)
        conn_val = Text("false", font=MONO_FONT, font_size=20,
                        color=RED, weight=BOLD)
        conn_row = VGroup(conn_lbl, conn_val).arrange(RIGHT, buff=0.4)
        conn_row.move_to(state_box.get_center() + DOWN * 0.22)

        self.state_panel = VGroup(state_box, ready_row, conn_row)
        self.state_ready = ready_val
        self.state_conn = conn_val

        self.play(FadeIn(self.state_panel), run_time=0.5)
        self.wait(0.3)

        # === Beat 2.1 — send initialize (id:1) ===
        self.show_subtitle("等 1 秒 → 父程序送出 initialize")

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
        self.show_subtitle("子程序回報能力 → ready=true")

        arrow_cap = self.message_arrow('left', GREEN, y_offset=-1.0)
        self.play(GrowArrow(arrow_cap), run_time=0.5)

        cap_pill = self._make_pill("能力清單 · ok", GREEN)
        cap_pill.move_to(self.child_box.get_left() + LEFT * 0.55 + DOWN * 1.0)
        self.play(FadeIn(cap_pill, scale=0.6), run_time=0.4)
        self.play(
            cap_pill.animate.move_to(
                self.parent_box.get_right() + RIGHT * 0.55 + DOWN * 1.0
            ),
            run_time=1.4,
        )
        self.wait(1.5)
        self.play(FadeOut(cap_pill), run_time=0.3)

        # update ready=true
        new_ready = Text("true", font=MONO_FONT, font_size=20,
                         color=GREEN, weight=BOLD)
        new_ready.next_to(ready_lbl, RIGHT, buff=0.4)
        self.play(ReplacementTransform(self.state_ready, new_ready),
                  run_time=0.6)
        self.state_ready = new_ready
        # Re-link group reference
        self.state_panel[1].submobjects[1] = new_ready

        # Highlight the asymmetry
        note = Text("但 isConnected 還是 false ←重點",
                    font=CN_FONT, font_size=22, color=RED,
                    weight=BOLD).next_to(state_box, RIGHT, buff=0.4)
        self.play(FadeIn(note, shift=LEFT * 0.2), run_time=0.5)
        self.wait(9.5)

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
        self.show_subtitle("再問子程序有哪些工具")
        arrow_tl = self.message_arrow('right', ORANGE, y_offset=0.0)
        ask_lbl = Text("要工具清單", font=CN_FONT, font_size=22,
                       color=ORANGE,
                       weight=BOLD).next_to(arrow_tl, UP, buff=0.15)
        self.play(GrowArrow(arrow_tl), FadeIn(ask_lbl), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(arrow_tl), FadeOut(ask_lbl), run_time=0.4)

        # 3. response: green arrow + 8 dots flying back to parent
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

        # update isConnected=true
        self.show_subtitle("收到工具清單後 → 才算真正連上")
        new_conn = Text("true", font=MONO_FONT, font_size=20,
                        color=GREEN, weight=BOLD)
        new_conn.next_to(conn_lbl, RIGHT, buff=0.4)
        self.play(ReplacementTransform(self.state_conn, new_conn),
                  run_time=0.6)
        self.state_conn = new_conn
        self.state_panel[2].submobjects[1] = new_conn

        # green checkmark on state panel
        check = Text("✓ 連上", font=CN_FONT, font_size=22, color=GREEN,
                     weight=BOLD).next_to(state_box, RIGHT, buff=0.4)
        self.play(Write(check), run_time=0.4)
        self.wait(6.0)

        # cleanup act 2 (notify/tl arrows already faded above)
        self.play(FadeOut(arrow_tl_res),
                  FadeOut(tool_dots), FadeOut(count_lbl),
                  FadeOut(check),
                  run_time=0.5)
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(73)

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
        self.play(call_pill.animate.shift(UP * 1.15), run_time=0.4)
        self.wait(2.5)

        # 等候名單 icon — yellow, with id and timeout
        self.show_subtitle("父程序記下這個請求，等結果回來再回呼")
        wait_box = RoundedRectangle(
            width=2.4, height=0.65, corner_radius=0.14,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.20,
        )
        wait_lbl = Text("等候 id:4 · 30s 內", font=MONO_FONT,
                        font_size=18, color=ORANGE, weight=BOLD)
        wait_lbl.move_to(wait_box.get_center())
        wait_group = VGroup(wait_box, wait_lbl)
        wait_group.next_to(self.parent_box, DOWN, buff=0.3)
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
        self.show_subtitle("子程序執行完 → 回傳結果")

        arrow_res = self.message_arrow('left', GREEN, y_offset=-1.0)
        self.play(GrowArrow(arrow_res), run_time=0.4)

        result_pill = self._make_pill("結果 · 10 筆新書", GREEN)
        result_pill.move_to(
            self.child_box.get_left() + LEFT * 0.55 + DOWN * 1.0
        )
        self.play(FadeIn(result_pill, scale=0.7), run_time=0.4)
        self.play(
            result_pill.animate.move_to(
                self.parent_box.get_right() + RIGHT * 0.55 + DOWN * 1.0
            ),
            run_time=1.4,
        )
        self.wait(1.5)

        # 等候名單 yellow → green ✓
        self.show_subtitle("找到等候中的請求 → 把結果回給呼叫端")
        done_box = RoundedRectangle(
            width=2.4, height=0.65, corner_radius=0.14,
            stroke_color=GREEN, stroke_width=2,
            fill_color=GREEN, fill_opacity=0.20,
        )
        done_lbl = Text("id:4  ✓ 完成", font=MONO_FONT,
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
        self.show_subtitle("整個流程：stdio pipe + JSON-RPC 2.0")
        flow_text = VGroup(
            Text("spawn", font=MONO_FONT, font_size=30, color=BLUE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("initialize", font=MONO_FONT, font_size=30, color=ORANGE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("tools/list", font=MONO_FONT, font_size=30, color=ORANGE,
                 weight=BOLD),
            Text("→", font=MONO_FONT, font_size=30, color=NEUTRAL),
            Text("tools/call", font=MONO_FONT, font_size=30, color=GREEN,
                 weight=BOLD),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.8)
        self.play(FadeIn(flow_text, shift=DOWN * 0.2), run_time=0.7)
        self.wait(13.0)

        # cleanup act 3 (and persistent visuals)
        cleanup = [self.parent_box, self.child_box, self.pipe_top, self.pipe_bot,
                   self.state_panel, flow_text, act_badge]
        if self._cur_subtitle is not None:
            cleanup.append(self._cur_subtitle)
            self._cur_subtitle = None
        self.play(*[FadeOut(m) for m in cleanup], run_time=0.7)
        self.advance_progress(111)

    # ============================================================
    # OUTRO — three points (11s)
    # ============================================================
    def scene_outro(self):
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
                       "spawn 開子程序 + stdio pipe 雙向 JSON-RPC"),
            make_point("②", "兩階段狀態",
                       "ready ≠ isConnected：要等 tools/list 才算連上"),
            make_point("③", "Tool Call 機制",
                       "pendingRequests Map + 30s timeout + resolve"),
        ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(DOWN * 0.3)

        self.play(FadeIn(outro_title, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.5)
        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(2.5)

        self.wait(6.5)
        self.advance_progress(self.TOTAL_SECONDS)
        self.wait(0.4)
