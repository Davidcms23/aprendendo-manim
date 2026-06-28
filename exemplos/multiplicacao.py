"""
Multiplicação: propriedades e exemplos
========================================
Só álgebra — sem texto, tudo via fórmulas e animações.

Cenas:
  CenaDefinicao       — a × b como fórmula
  CenaComutativa      — a × b = b × a
  CenaAssociativa     — (a × b) × c = a × (b × c)
  CenaDistributiva    — a × (b + c) = a×b + a×c
  CenaElementoNeutro  — a × 1 = a
  CenaElementoNulo    — a × 0 = 0
  CenaExemplo         — substitui números e resolve passo a passo

Rodar:
  manim -pql multiplicacao.py CenaComutativa
  manim -pql multiplicacao.py --write_all
"""

from manim import *


# ── Paleta ────────────────────────────────────────────────────
CA  = BLUE_C       # variável  a
CB  = ORANGE       # variável  b
CC  = GREEN_C      # variável  c
CEQ = WHITE        # sinal de =
CDT = YELLOW       # destaque / resultado


# ── Helper: cria MathTex com cores por substring ──────────────
def fml(*args, size=52, **kwargs):
    return MathTex(*args, font_size=size, **kwargs)


# ═══════════════════════════════════════════════════════════════
# CENA 1 — Definição: a × b
# ═══════════════════════════════════════════════════════════════
class CenaDefinicao(Scene):
    def construct(self):

        # Mostra  a  ×  b  surgindo da esquerda e direita
        a    = fml(r"a", size=72, color=CA).shift(LEFT * 2)
        vezes = fml(r"\times", size=72, color=CEQ)
        b    = fml(r"b", size=72, color=CB).shift(RIGHT * 2)

        self.play(FadeIn(a, shift=RIGHT * 0.4), run_time=0.8)
        self.play(Write(vezes), run_time=0.6)
        self.play(FadeIn(b, shift=LEFT * 0.4), run_time=0.8)
        self.wait(1.0)

        # Agrupa e centraliza
        grupo = VGroup(a, vezes, b)
        self.play(grupo.animate.arrange(RIGHT, buff=0.35).move_to(ORIGIN),
                  run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(grupo))


# ═══════════════════════════════════════════════════════════════
# CENA 2 — Comutativa: a × b = b × a
# ═══════════════════════════════════════════════════════════════
class CenaComutativa(Scene):
    def construct(self):

        # Estado inicial: a × b
        p0 = fml(r"a", r"\times", r"b", size=60)
        p0[0].set_color(CA)
        p0[2].set_color(CB)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.2)
        self.wait(1.0)

        # Adiciona  =  b × a  à direita
        p1 = fml(r"a", r"\times", r"b", r"=", r"b", r"\times", r"a", size=60)
        p1[0].set_color(CA)
        p1[2].set_color(CB)
        p1[4].set_color(CB)
        p1[6].set_color(CA)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=2.0, rate_func=smooth)
        self.wait(1.5)

        # Destaca: o  a  e o  b  do lado esquerdo migram para os lados trocados
        # Arco indicando a troca
        arco_a = CurvedArrow(
            p1[0].get_top() + UP * 0.1,
            p1[6].get_top() + UP * 0.1,
            angle=-TAU / 5,
            color=CA,
            stroke_width=2,
        )
        arco_b = CurvedArrow(
            p1[4].get_bottom() + DOWN * 0.1,
            p1[2].get_bottom() + DOWN * 0.1,
            angle=-TAU / 5,
            color=CB,
            stroke_width=2,
        )

        self.play(Create(arco_a), Create(arco_b), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(VGroup(p1, arco_a, arco_b)))


# ═══════════════════════════════════════════════════════════════
# CENA 3 — Associativa: (a × b) × c = a × (b × c)
# ═══════════════════════════════════════════════════════════════
class CenaAssociativa(Scene):
    def construct(self):

        # Lado esquerdo: (a × b) × c
        p0 = fml(
            r"(", r"a", r"\times", r"b", r")", r"\times", r"c",
            size=54,
        )
        p0[1].set_color(CA)
        p0[3].set_color(CB)
        p0[6].set_color(CC)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.5)
        self.wait(1.2)

        # Fórmula completa com igualdade
        p1 = fml(
            r"(", r"a", r"\times", r"b", r")", r"\times", r"c",
            r"=",
            r"a", r"\times", r"(", r"b", r"\times", r"c", r")",
            size=48,
        )
        p1[1].set_color(CA)
        p1[3].set_color(CB)
        p1[6].set_color(CC)
        p1[8].set_color(CA)
        p1[11].set_color(CB)
        p1[13].set_color(CC)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=2.2, rate_func=smooth)
        self.wait(1.5)

        # Destaca os parênteses alternando
        braces_esq = VGroup(p1[0], p1[4])
        braces_dir = VGroup(p1[10], p1[14])

        self.play(braces_esq.animate.set_color(YELLOW), run_time=0.5)
        self.wait(0.5)
        self.play(braces_esq.animate.set_color(WHITE), run_time=0.4)
        self.play(braces_dir.animate.set_color(YELLOW), run_time=0.5)
        self.wait(0.5)
        self.play(braces_dir.animate.set_color(WHITE), run_time=0.4)
        self.wait(1.5)

        self.play(FadeOut(p1))


# ═══════════════════════════════════════════════════════════════
# CENA 4 — Distributiva: a × (b + c) = a×b + a×c
# ═══════════════════════════════════════════════════════════════
class CenaDistributiva(Scene):
    def construct(self):

        # Passo 0: a × (b + c)
        p0 = fml(
            r"a", r"\times", r"(", r"b", r"+", r"c", r")",
            size=56,
        )
        p0[0].set_color(CA)
        p0[3].set_color(CB)
        p0[5].set_color(CC)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.3)
        self.wait(1.2)

        # Passo 1: = a×b + a×c
        p1 = fml(
            r"a", r"\times", r"(", r"b", r"+", r"c", r")",
            r"=",
            r"a", r"\times", r"b",
            r"+",
            r"a", r"\times", r"c",
            size=50,
        )
        p1[0].set_color(CA)
        p1[3].set_color(CB)
        p1[5].set_color(CC)
        p1[8].set_color(CA)
        p1[10].set_color(CB)
        p1[12].set_color(CA)
        p1[14].set_color(CC)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=2.2, rate_func=smooth)
        self.wait(1.2)

        # Arcos mostrando o  a  "se distribuindo"
        arco1 = CurvedArrow(
            p1[0].get_top() + UP * 0.05,
            p1[8].get_top() + UP * 0.05,
            angle=-TAU / 6,
            color=CA,
            stroke_width=2,
        )
        arco2 = CurvedArrow(
            p1[0].get_top() + UP * 0.05,
            p1[12].get_top() + UP * 0.05,
            angle=-TAU / 8,
            color=CA,
            stroke_width=2,
        )

        self.play(Create(arco1), run_time=0.8)
        self.play(Create(arco2), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(VGroup(p1, arco1, arco2)))


# ═══════════════════════════════════════════════════════════════
# CENA 5 — Elemento neutro: a × 1 = a
# ═══════════════════════════════════════════════════════════════
class CenaElementoNeutro(Scene):
    def construct(self):

        p0 = fml(r"a", r"\times", r"1", size=64)
        p0[0].set_color(CA)
        p0[2].set_color(CDT)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.0)
        self.wait(1.0)

        p1 = fml(r"a", r"\times", r"1", r"=", r"a", size=64)
        p1[0].set_color(CA)
        p1[2].set_color(CDT)
        p1[4].set_color(CA)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=1.8, rate_func=smooth)
        self.wait(1.0)

        # O  ×1  some, fica só o  a
        p2 = fml(r"a", size=80, color=CA)
        p2.move_to(ORIGIN)

        self.play(TransformMatchingTex(p1, p2), run_time=1.8, rate_func=smooth)
        self.wait(2.0)
        self.play(FadeOut(p2))


# ═══════════════════════════════════════════════════════════════
# CENA 6 — Elemento nulo: a × 0 = 0
# ═══════════════════════════════════════════════════════════════
class CenaElementoNulo(Scene):
    def construct(self):

        p0 = fml(r"a", r"\times", r"0", size=64)
        p0[0].set_color(CA)
        p0[2].set_color(RED_C)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.0)
        self.wait(1.0)

        p1 = fml(r"a", r"\times", r"0", r"=", r"0", size=64)
        p1[0].set_color(CA)
        p1[2].set_color(RED_C)
        p1[4].set_color(RED_C)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=1.8, rate_func=smooth)
        self.wait(1.0)

        # Tudo some — só o 0 fica
        p2 = fml(r"0", size=90, color=RED_C)
        p2.move_to(ORIGIN)

        self.play(TransformMatchingTex(p1, p2), run_time=1.8, rate_func=smooth)
        self.wait(2.0)
        self.play(FadeOut(p2))


# ═══════════════════════════════════════════════════════════════
# CENA 7 — Exemplo numérico: 3 × (4 + 2)
#           usando a distributiva passo a passo
# ═══════════════════════════════════════════════════════════════
class CenaExemplo(Scene):
    def construct(self):

        # Passo 0: expressão inicial
        p0 = fml(r"3", r"\times", r"(", r"4", r"+", r"2", r")", size=60)
        p0[0].set_color(CA)
        p0[3].set_color(CB)
        p0[5].set_color(CC)
        p0.move_to(ORIGIN)

        self.play(Write(p0), run_time=1.2)
        self.wait(1.5)

        # Passo 1: distribui → 3×4 + 3×2
        p1 = fml(
            r"3", r"\times", r"4",
            r"+",
            r"3", r"\times", r"2",
            size=60,
        )
        p1[0].set_color(CA)
        p1[2].set_color(CB)
        p1[4].set_color(CA)
        p1[6].set_color(CC)
        p1.move_to(ORIGIN)

        self.play(TransformMatchingTex(p0, p1), run_time=2.2, rate_func=smooth)
        self.wait(1.5)

        # Passo 2: 3×4 = 12, 3×2 = 6  →  12 + 6
        p2 = fml(r"12", r"+", r"6", size=64)
        p2[0].set_color(CB)
        p2[2].set_color(CC)
        p2.move_to(ORIGIN)

        self.play(TransformMatchingTex(p1, p2), run_time=2.0, rate_func=smooth)
        self.wait(1.5)

        # Passo 3: 12 + 6 = 18
        p3 = fml(r"12", r"+", r"6", r"=", r"18", size=64)
        p3[0].set_color(CB)
        p3[2].set_color(CC)
        p3[4].set_color(CDT)
        p3.move_to(ORIGIN)

        self.play(TransformMatchingTex(p2, p3), run_time=1.8, rate_func=smooth)
        self.wait(1.2)

        # Passo 4: só o resultado
        p4 = fml(r"18", size=90, color=CDT)
        p4.move_to(ORIGIN)

        self.play(TransformMatchingTex(p3, p4), run_time=1.8, rate_func=smooth)

        caixa = SurroundingRectangle(p4, color=CDT, corner_radius=0.15, buff=0.3)
        self.play(Create(caixa), run_time=0.6)
        self.wait(2.5)

        self.play(FadeOut(VGroup(p4, caixa)))
