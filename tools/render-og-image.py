"""
Render a 1200x630 OG image for social-share previews (LinkedIn / Twitter / FB).

Layout mirrors the magazine-cover intro of the videos:
  left  — kicker / serif title / violet accent / subtitle / credit
  right — undraw chat-with-ai illustration

Render:
  manim -s -ql --disable_caching tools/render-og-image.py OGImage
  → media/images/render-og-image/OGImage_ManimCE_v0.20.1.png
"""
from manim import *

# OG image standard: 1200x630 (aspect ~1.905). Keep frame at 16:8.4.
config.frame_width  = 16
config.frame_height = 8.4
config.pixel_width  = 1200
config.pixel_height = 630


class OGImage(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a10"

        # ── Background radial glows (mimic the landing hero) ───────────
        glow_v = Circle(radius=4.0, color="#7B5CF5", fill_opacity=0.10,
                        stroke_width=0).move_to([5.5, 3.5, 0])
        glow_o = Circle(radius=3.5, color="#FB7048", fill_opacity=0.06,
                        stroke_width=0).move_to([-5.5, -3.0, 0])
        self.add(glow_v, glow_o)

        # ── Right: hero illustration ───────────────────────────────────
        try:
            hero = SVGMobject(
                "intro-assets/undraw_chat-with-ai.svg",
            ).scale_to_fit_height(5.6)
            hero.move_to([4.2, -0.1, 0])
            self.add(hero)
        except Exception:
            pass

        # ── Left: magazine-cover title stack ───────────────────────────
        kicker = Text("章節 00  ·  國立中興大學",
                      font="DejaVu Sans Mono", font_size=18,
                      color="#9D85F7", weight=BOLD)

        title_lines = VGroup(
            Text("MCP 入門", font="Noto Serif CJK TC", font_size=84,
                 color="#FFFFFF", weight=BOLD),
            Text("工作坊", font="Noto Serif CJK TC", font_size=84,
                 color="#FFFFFF", weight=BOLD),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)

        accent = Line(start=LEFT * 0.0, end=RIGHT * 2.4,
                      color="#7B5CF5", stroke_width=6)

        sub = Text("讓 LLM 連上你的工具\n從 RAG 到 MCP 的完整路徑",
                   font="Noto Sans CJK TC", font_size=26,
                   color="#B4BED2", line_spacing=1.15)

        kicker.next_to(title_lines, UP, buff=0.35, aligned_edge=LEFT)
        accent.next_to(title_lines, DOWN, buff=0.32, aligned_edge=LEFT)
        sub.next_to(accent, DOWN, buff=0.32, aligned_edge=LEFT)

        title_stack = VGroup(kicker, title_lines, accent, sub)
        title_stack.move_to([-4.4, 0.4, 0])
        self.add(title_stack)

        # ── Bottom-right: credit ───────────────────────────────────────
        credit = Text(
            "Supported by  NAPAI · SIGAgent group",
            font="DejaVu Sans Mono", font_size=14,
            color="#9D85F7", weight=BOLD,
        )
        credit.move_to([5.2, -3.7, 0])
        self.add(credit)

        # Manim with -s flag captures the first frame. Need at least one wait.
        self.wait(0.01)
