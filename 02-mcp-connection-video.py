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
    TOTAL_SECONDS = 157.5

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
        self.scene_act1()         # 0:04–0:39
        self.scene_act2()         # 0:39–1:54
        self.scene_act3()         # 1:54–2:49
        self.scene_outro()        # 2:49–3:00

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
        self.wait(8.0)

        # Beat 1.3 — env substitution + setupEventHandlers (10s)
        env_snip = self.make_json_snippet([
            ('"env": {',                         NEUTRAL),
            ('  "MODULES_PATH":',                BLUE),
            ('    "${NCHU_MODULES_PATH}"',       ORANGE),
            ('}',                                NEUTRAL),
            ('# → "/opt/nchu-library"',          GREEN),
        ], width=5.5, size=18)
        env_snip.move_to(DOWN * 1.5)

        self.play(FadeIn(env_snip, shift=UP * 0.2), run_time=0.6)
        self.show_subtitle("env 內 ${VAR} 自動替換成真實環境變數")
        self.wait(10.0)

        # cleanup act 1 visuals, keep parent/child + pipes for act 2
        self.play(
            FadeOut(spawn_call), FadeOut(env_snip),
            FadeOut(pipe_lbl_top), FadeOut(pipe_lbl_bot),
            run_time=0.5,
        )
        if self._cur_subtitle is not None:
            self.play(FadeOut(self._cur_subtitle), run_time=0.3)
            self._cur_subtitle = None
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(32)

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

        # === Beat 2.1 — send initialize (id:1) (25s) ===
        self.show_subtitle("等 1 秒 → 送出 initialize (id:1)")

        init_snip = self.make_json_snippet([
            ('{',                                       NEUTRAL),
            ('  "method": "initialize",',               BLUE),
            ('  "id": 1,',                              ORANGE),
            ('  "params": {',                           NEUTRAL),
            ('    "protocolVersion": "2024-11-05"',     GREEN),
            ('  }',                                     NEUTRAL),
            ('}',                                       NEUTRAL),
        ], width=5.5, size=18)
        init_snip.move_to(UP * 2.8 + LEFT * 4.5)

        self.play(FadeIn(init_snip, shift=DOWN * 0.2), run_time=0.6)
        self.wait(4.5)

        # send arrow right
        arrow_init = self.message_arrow('right', ORANGE, y_offset=0.0)
        arrow_init_lbl = Text("REQUEST  initialize", font=MONO_FONT,
                              font_size=18, color=ORANGE,
                              weight=BOLD).next_to(arrow_init, UP, buff=0.1)
        self.play(GrowArrow(arrow_init), FadeIn(arrow_init_lbl), run_time=0.8)
        self.wait(5.0)

        # === Beat 2.2 — child responds (25s) ===
        self.show_subtitle("子程序回 capabilities → ready=true")

        # response arrow left
        arrow_cap = self.message_arrow('left', GREEN, y_offset=-1.0)
        arrow_cap_lbl = Text("RESPONSE  capabilities", font=MONO_FONT,
                             font_size=18, color=GREEN,
                             weight=BOLD).next_to(arrow_cap, DOWN, buff=0.1)
        self.play(GrowArrow(arrow_cap), FadeIn(arrow_cap_lbl), run_time=0.8)

        cap_snip = self.make_json_snippet([
            ('{',                                       NEUTRAL),
            ('  "id": 1,',                              ORANGE),
            ('  "result": {',                           NEUTRAL),
            ('    "capabilities": {"tools":{}}',        GREEN),
            ('  }',                                     NEUTRAL),
            ('}',                                       NEUTRAL),
        ], width=5.5, size=18)
        cap_snip.move_to(UP * 2.8 + RIGHT * 4.5)
        self.play(FadeIn(cap_snip, shift=DOWN * 0.2), run_time=0.6)
        self.wait(3.5)

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
        self.wait(10.0)

        # cleanup snippets before beat 2.3
        self.play(FadeOut(init_snip), FadeOut(cap_snip),
                  FadeOut(arrow_init), FadeOut(arrow_init_lbl),
                  FadeOut(arrow_cap), FadeOut(arrow_cap_lbl),
                  FadeOut(note),
                  run_time=0.6)

        # === Beat 2.3 — notifications/initialized + tools/list (25s) ===
        self.show_subtitle("送 notifications/initialized（單向，無 id）")

        # notify arrow (no id, grey)
        arrow_notify = self.message_arrow('right', NEUTRAL, y_offset=0.3)
        arrow_notify_lbl = Text("NOTIFY  notifications/initialized",
                                font=MONO_FONT, font_size=18,
                                color=NEUTRAL,
                                weight=BOLD).next_to(arrow_notify, UP, buff=0.1)
        self.play(GrowArrow(arrow_notify), FadeIn(arrow_notify_lbl),
                  run_time=0.7)
        self.wait(4.0)

        # tools/list request (right)
        self.show_subtitle("送 tools/list (id:3) → 子程序列舉工具")
        arrow_tl = self.message_arrow('right', ORANGE, y_offset=-0.3)
        arrow_tl_lbl = Text("REQUEST  tools/list  id:3", font=MONO_FONT,
                            font_size=18, color=ORANGE,
                            weight=BOLD).next_to(arrow_tl, UP, buff=0.05)
        self.play(GrowArrow(arrow_tl), FadeIn(arrow_tl_lbl), run_time=0.7)
        self.wait(3.5)

        # tools/list response (left, green)
        arrow_tl_res = self.message_arrow('left', GREEN, y_offset=-1.0)
        arrow_tl_res_lbl = Text("RESPONSE  8 個工具", font=MONO_FONT,
                                font_size=18, color=GREEN,
                                weight=BOLD).next_to(arrow_tl_res, DOWN,
                                                     buff=0.1)
        tools_snip = self.make_json_snippet([
            ('"tools": [',                              NEUTRAL),
            ('  {"name":"search_new_books"},',          GREEN),
            ('  {"name":"search_courses"},',            GREEN),
            ('  ...（共 8 個）',                          NEUTRAL),
            (']',                                       NEUTRAL),
        ], width=5.2, size=18)
        tools_snip.move_to(UP * 2.8 + RIGHT * 4.5)
        self.play(GrowArrow(arrow_tl_res), FadeIn(arrow_tl_res_lbl),
                  FadeIn(tools_snip), run_time=0.8)
        self.wait(3.5)

        # update isConnected=true
        self.show_subtitle("收到工具清單後 → isConnected=true 才算真正連上")
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
        self.wait(8.5)

        # cleanup act 2 (keep parent/child/pipes/state panel for act 3)
        self.play(FadeOut(arrow_notify), FadeOut(arrow_notify_lbl),
                  FadeOut(arrow_tl), FadeOut(arrow_tl_lbl),
                  FadeOut(arrow_tl_res), FadeOut(arrow_tl_res_lbl),
                  FadeOut(tools_snip), FadeOut(check),
                  run_time=0.5)
        self.play(FadeOut(act_badge), run_time=0.3)
        self.advance_progress(95)

    # ============================================================
    # ACT 3 — tool call (55s)
    # ============================================================
    def scene_act3(self):
        act_badge = self._make_act_badge("ACT 3")
        self.play(FadeIn(act_badge), run_time=0.3)

        # === Beat 3.1 — executeToolCall + pendingRequests (20s) ===
        self.show_subtitle("Sonnet 決定呼叫 → executeToolCall()")

        call_snip = self.make_json_snippet([
            ('{',                                       NEUTRAL),
            ('  "method": "tools/call",',               BLUE),
            ('  "id": 4,',                              ORANGE),
            ('  "params": {',                           NEUTRAL),
            ('    "name": "search_new_books",',         GREEN),
            ('    "arguments": {"query":"新書"}',         GREEN),
            ('  }',                                     NEUTRAL),
            ('}',                                       NEUTRAL),
        ], width=5.8, size=18)
        call_snip.move_to(UP * 2.8)
        self.play(FadeIn(call_snip, shift=DOWN * 0.2), run_time=0.6)
        self.wait(3.5)

        # pendingRequests map — compact label below parent_box (no overlap with call_snip)
        pmap_box = RoundedRectangle(width=4.0, height=0.85, corner_radius=0.10,
                                    stroke_color=BLUE, stroke_width=2,
                                    fill_color=BLUE, fill_opacity=0.15)
        pmap_box.move_to(self.parent_box.get_bottom() + DOWN * 0.55)
        pmap_lbl = Text("pendingRequests.set(4, {resolve, 30s})",
                        font=MONO_FONT, font_size=15,
                        color=INK).move_to(pmap_box.get_center())
        if pmap_lbl.width > pmap_box.width - 0.3:
            pmap_lbl.scale_to_fit_width(pmap_box.width - 0.3)
        pmap = VGroup(pmap_box, pmap_lbl)
        self.play(FadeIn(pmap, shift=UP * 0.2), run_time=0.5)
        self.wait(3.5)

        # send arrow right (tools/call)
        arrow_call = self.message_arrow('right', ORANGE, y_offset=0.0)
        arrow_call_lbl = Text("REQUEST  tools/call  id:4", font=MONO_FONT,
                              font_size=18, color=ORANGE,
                              weight=BOLD).next_to(arrow_call, UP, buff=0.1)
        self.play(GrowArrow(arrow_call), FadeIn(arrow_call_lbl), run_time=0.8)
        self.wait(6.0)

        # === Beat 3.2 — child returns result, resolve callback (20s) ===
        # Fade out call_snip first so result_snip can take the centre spot
        self.play(FadeOut(call_snip), run_time=0.4)
        self.show_subtitle("子程序執行完 → 回傳 result")

        arrow_res = self.message_arrow('left', GREEN, y_offset=-1.0)
        arrow_res_lbl = Text("RESPONSE  result.content", font=MONO_FONT,
                             font_size=18, color=GREEN,
                             weight=BOLD).next_to(arrow_res, DOWN, buff=0.1)
        result_snip = self.make_json_snippet([
            ('"result": {',                             NEUTRAL),
            ('  "content": [{',                         NEUTRAL),
            ('    "type": "text",',                     BLUE),
            ('    "text": "...10 筆新書"',              GREEN),
            ('  }]',                                    NEUTRAL),
            ('}',                                       NEUTRAL),
        ], width=5.8, size=18)
        result_snip.move_to(UP * 2.8)
        self.play(GrowArrow(arrow_res), FadeIn(arrow_res_lbl),
                  FadeIn(result_snip), run_time=0.8)
        self.wait(4.5)

        # resolve callback — from pmap (below parent_box) UP into parent_box
        self.show_subtitle("clearTimeout → resolve(content) → 結果回 client")
        resolve_arrow = Arrow(start=pmap_box.get_top() + UP * 0.02,
                              end=self.parent_box.get_bottom() + DOWN * 0.05,
                              color=GREEN, stroke_width=4, buff=0.05,
                              max_tip_length_to_length_ratio=0.20)
        resolve_lbl = Text("resolve(content)", font=MONO_FONT,
                           font_size=18, color=GREEN, weight=BOLD)
        resolve_lbl.next_to(resolve_arrow, RIGHT, buff=0.2)
        self.play(GrowArrow(resolve_arrow), FadeIn(resolve_lbl), run_time=0.6)
        self.wait(7.0)

        # cleanup before beat 3.3
        self.play(FadeOut(call_snip), FadeOut(result_snip),
                  FadeOut(arrow_call), FadeOut(arrow_call_lbl),
                  FadeOut(arrow_res), FadeOut(arrow_res_lbl),
                  FadeOut(pmap), FadeOut(resolve_arrow), FadeOut(resolve_lbl),
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
        self.advance_progress(145)

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
