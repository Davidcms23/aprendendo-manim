"""
Cenas algébricas com transformações fluidas
============================================
Usa TransformMatchingTex para animar cada símbolo
se transformando no próximo passo, em vez de
aparecer/desaparecer abruptamente.

Cenas:
  CenaSubstituicao  — substitui α=1, β=1 na fórmula geral
  CenaIntegralB     — calcula B(1,1) passo a passo

Rodar:
  manim -pql uniforme_beta.py CenaSubstituicao
  manim -pql uniforme_beta.py CenaIntegralB
  manim -pql uniforme_beta.py --write_all
"""

from manim import *


# ── Paleta ────────────────────────────────────────────────────
COR_NORM  = ORANGE    # normalizador  1/B(α,β)
COR_X     = YELLOW    # termo x^{α-1}
COR_1X    = BLUE_C    # termo (1-x)^{β-1}
COR_EQ    = WHITE
COR_DEST  = "#80FF80" # verde claro para resultados finais


# ═══════════════════════════════════════════════════════════════
# CENA 1 — Substituição α=1, β=1
# ═══════════════════════════════════════════════════════════════
class CenaSubstituicao(Scene):
    """
    Parte da fórmula geral e substitui α→1, β→1,
    com cada símbolo se transformando no seu substituto.
    """

    def construct(self):

        # ── Passo 0: fórmula geral ──────────────────────────
        # Escrevemos com substrings nomeadas para que o
        # TransformMatchingTex consiga rastrear cada pedaço.
        p0 = MathTex(
            r"\frac{1}{B(\alpha,\beta)}",
            r"x^{\alpha - 1}",
            r"(1-x)^{\beta - 1}",
            font_size=52,
        )
        # Colore cada parte
        p0[0].set_color(COR_NORM)
        p0[1].set_color(COR_X)
        p0[2].set_color(COR_1X)

        p0.move_to(ORIGIN)
        self.play(Write(p0), run_time=1.5)
        self.wait(1.5)

        # ── Passo 1: substitui α=1, β=1 ─────────────────────
        # Os símbolos "α" e "β" viram "1" — o resto fica igual
        p1 = MathTex(
            r"\frac{1}{B(1,1)}",
            r"x^{1 - 1}",
            r"(1-x)^{1 - 1}",
            font_size=52,
        )
        p1[0].set_color(COR_NORM)
        p1[1].set_color(COR_X)
        p1[2].set_color(COR_1X)

        # TransformMatchingTex: símbolos comuns deslizam,
        # símbolos novos aparecem (FadeIn), removidos somem (FadeOut)
        self.play(
            TransformMatchingTex(p0, p1),
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 2: 1 - 1 → 0 nos expoentes ───────────────
        p2 = MathTex(
            r"\frac{1}{B(1,1)}",
            r"x^{0}",
            r"(1-x)^{0}",
            font_size=52,
        )
        p2[0].set_color(COR_NORM)
        p2[1].set_color(COR_X)
        p2[2].set_color(COR_1X)

        self.play(
            TransformMatchingTex(p1, p2),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 3: x⁰ → 1, (1-x)⁰ → 1 ───────────────────
        p3 = MathTex(
            r"\frac{1}{B(1,1)}",
            r"\cdot 1",
            r"\cdot 1",
            font_size=52,
        )
        p3[0].set_color(COR_NORM)
        p3[1].set_color(COR_X)
        p3[2].set_color(COR_1X)

        self.play(
            TransformMatchingTex(p2, p3),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 4: · 1 · 1 some, fica só 1/B(1,1) ────────
        p4 = MathTex(
            r"\frac{1}{B(1,1)}",
            font_size=60,
            color=COR_NORM,
        )

        self.play(
            TransformMatchingTex(p3, p4),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(1.0)

        # Caixa de destaque no resultado parcial
        caixa = SurroundingRectangle(p4, color=COR_NORM,
                                      corner_radius=0.12, buff=0.25)
        self.play(Create(caixa), run_time=0.7)
        self.wait(2.0)

        self.play(FadeOut(VGroup(p4, caixa)))


# ═══════════════════════════════════════════════════════════════
# CENA 2 — Calculando B(1,1)
# ═══════════════════════════════════════════════════════════════
class CenaIntegralB(Scene):
    """
    Mostra o cálculo de B(1,1) com cada passo
    se transformando no seguinte.
    """

    def construct(self):

        # ── Passo 0: definição de B(1,1) ────────────────────
        p0 = MathTex(
            r"B(1,1)",
            r"=",
            r"\int_0^1 x^{1-1}(1-x)^{1-1}\,dx",
            font_size=46,
        )
        p0.move_to(ORIGIN)
        self.play(Write(p0), run_time=1.8)
        self.wait(1.5)

        # ── Passo 1: simplifica expoentes ───────────────────
        p1 = MathTex(
            r"B(1,1)",
            r"=",
            r"\int_0^1 x^{0}(1-x)^{0}\,dx",
            font_size=46,
        )

        self.play(
            TransformMatchingTex(p0, p1),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 2: x⁰ = 1, (1-x)⁰ = 1 ───────────────────
        p2 = MathTex(
            r"B(1,1)",
            r"=",
            r"\int_0^1 1 \,dx",
            font_size=46,
        )

        self.play(
            TransformMatchingTex(p1, p2),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 3: antiderivada ────────────────────────────
        p3 = MathTex(
            r"B(1,1)",
            r"=",
            r"\Big[ x \Big]_0^1",
            font_size=46,
        )

        self.play(
            TransformMatchingTex(p2, p3),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 4: substitui os limites ───────────────────
        p4 = MathTex(
            r"B(1,1)",
            r"=",
            r"1 - 0",
            font_size=46,
        )

        self.play(
            TransformMatchingTex(p3, p4),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.5)

        # ── Passo 5: 1 - 0 → 1 ──────────────────────────────
        p5 = MathTex(
            r"B(1,1)",
            r"=",
            r"1",
            font_size=60,
        )
        p5[2].set_color(COR_DEST)

        self.play(
            TransformMatchingTex(p4, p5),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(1.0)

        caixa = SurroundingRectangle(p5, color=COR_DEST,
                                      corner_radius=0.12, buff=0.3)
        self.play(Create(caixa), run_time=0.7)
        self.wait(1.5)

        # ── Consequência final ───────────────────────────────
        # Cada passo é um MathTex separado — único modo seguro
        # de usar TransformMatchingTex sem erro de tex_string.
        self.play(FadeOut(caixa))
        self.play(p5.animate.shift(UP * 1.5), run_time=0.8)

        # Passo A: f(x;1,1) = 1/B(1,1)
        c_a = MathTex(
            r"f(x;1,1)", r"=", r"\frac{1}{B(1,1)}",
            font_size=46, color=COR_NORM,
        )
        c_a[0].set_color(COR_EQ)
        c_a[1].set_color(COR_EQ)
        c_a.next_to(p5, DOWN, buff=0.7)
        self.play(Write(c_a), run_time=1.2)
        self.wait(0.8)

        # Passo B: f(x;1,1) = 1/1   (B(1,1) → 1 no denominador)
        c_b = MathTex(
            r"f(x;1,1)", r"=", r"\frac{1}{1}",
            font_size=46, color=COR_NORM,
        )
        c_b[0].set_color(COR_EQ)
        c_b[1].set_color(COR_EQ)
        c_b.next_to(p5, DOWN, buff=0.7)

        self.play(
            TransformMatchingTex(c_a, c_b),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(0.8)

        # Passo C: f(x;1,1) = 1
        c_c = MathTex(
            r"f(x;1,1)", r"=", r"1",
            font_size=52,
        )
        c_c[0].set_color(COR_EQ)
        c_c[1].set_color(COR_EQ)
        c_c[2].set_color(COR_DEST)
        c_c.next_to(p5, DOWN, buff=0.7)

        self.play(
            TransformMatchingTex(c_b, c_c),
            run_time=2.0, rate_func=smooth,
        )
        self.wait(0.8)

        # Caixa final em torno de f(x;1,1) = 1
        caixa_final = SurroundingRectangle(
            c_c, color=COR_DEST, corner_radius=0.12, buff=0.2,
        )
        self.play(Create(caixa_final), run_time=0.7)
        self.wait(3.0)

        self.play(FadeOut(VGroup(p5, c_c, caixa_final)))
