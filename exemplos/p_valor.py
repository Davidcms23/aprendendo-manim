"""
p-valor: O que é e o que não é
================================
Script Manim para vídeo explicativo.

Cenas:
  1. CenaContexto      — situação motivadora (ensaio clínico)
  2. CenaH0            — hipótese nula e distribuição de T sob H₀
  3. CenaTObs          — onde cai o t observado
  4. CenaArea          — p-valor é a área na cauda
  5. CenaMoveT         — área muda conforme t muda (slider manual)
  6. CenaAlpha         — comparação com α = 0,05 → decisão
  7. CenaMitosBustos   — o que o p-valor NÃO é

Execute uma cena por vez durante o desenvolvimento:
  manim -pql pvalor_video.py CenaContexto
  manim -pql pvalor_video.py CenaH0
  ... etc.

Para renderizar todas de uma vez em baixa qualidade:
  manim -pql pvalor_video.py --all

Para qualidade final:
  manim -pqh pvalor_video.py --all
"""

from manim import *
import numpy as np
from scipy.stats import norm


# ─────────────────────────────────────────────────────────────
# Paleta de cores consistente ao longo de todo o vídeo
# ─────────────────────────────────────────────────────────────
COR_H0        = BLUE_C       # distribuição sob H₀
COR_T_OBS     = RED_C        # linha do t observado
COR_AREA      = ORANGE       # área do p-valor (preenchimento)
COR_ALPHA     = GREEN_C      # limiar α
COR_TEXTO     = WHITE
COR_DESTAQUE  = YELLOW


# ─────────────────────────────────────────────────────────────
# Helpers reutilizáveis
# ─────────────────────────────────────────────────────────────

def curva_normal(axes, cor=COR_H0, x_min=-4, x_max=4):
    """Retorna o gráfico da densidade N(0,1) nos eixos dados."""
    return axes.plot(
        lambda x: norm.pdf(x),
        x_range=[x_min, x_max],
        color=cor,
        stroke_width=3,
    )


def area_cauda(axes, t_val, cor=COR_AREA, x_max=4.5):
    """
    Retorna a área sombreada à direita de t_val
    (cauda superior do teste unicaudal).
    """
    return axes.get_area(
        axes.plot(lambda x: norm.pdf(x), x_range=[t_val, x_max]),
        x_range=[t_val, x_max],
        color=cor,
        opacity=0.5,
    )


def eixos_padrao(x_range=(-4.5, 4.5, 1), y_range=(0, 0.45, 0.1)):
    """Cria o sistema de eixos padrão usado em todas as cenas."""
    return Axes(
        x_range=[*x_range],
        y_range=[*y_range],
        x_length=10,
        y_length=4.5,
        axis_config={"color": GREY_B, "stroke_width": 1.5},
        x_axis_config={"include_numbers": True, "numbers_to_include": range(-4, 5)},
        y_axis_config={"include_numbers": False},
    )


# ═══════════════════════════════════════════════════════════════
# CENA 1 — Contexto motivador
# ═══════════════════════════════════════════════════════════════

class CenaContexto(Scene):
    """
    Apresenta a pergunta motivadora:
    'Um novo remédio funciona melhor que o placebo?'
    """

    def construct(self):
        # ── Título ──────────────────────────────────────────
        titulo = Text(
            "O que é o p-valor?",
            font_size=52,
            color=COR_DESTAQUE,
        ).to_edge(UP, buff=0.6)

        self.play(Write(titulo))
        self.wait(0.5)

        # ── Situação ────────────────────────────────────────
        situacao = VGroup(
            Text("Situação:", font_size=32, color=COR_DESTAQUE),
            Text(
                "Um ensaio clínico testa um novo remédio.",
                font_size=28,
                color=COR_TEXTO,
            ),
            Text(
                "Grupo A: remédio  |  Grupo B: placebo",
                font_size=26,
                color=GREY_A,
            ),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)

        situacao.next_to(titulo, DOWN, buff=0.8).shift(LEFT * 0.5)

        for linha in situacao:
            self.play(FadeIn(linha, shift=RIGHT * 0.3), run_time=0.7)
        self.wait(0.5)

        # ── Pergunta ────────────────────────────────────────
        pergunta_box = SurroundingRectangle(
            Text(""), buff=0.3, color=COR_H0, corner_radius=0.15
        )

        pergunta = VGroup(
            Text("Pergunta:", font_size=32, color=COR_H0),
            Text(
                "A diferença observada é real",
                font_size=30,
                color=COR_TEXTO,
            ),
            Text(
                "ou poderia ter ocorrido por acaso?",
                font_size=30,
                color=COR_TEXTO,
            ),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        pergunta.next_to(situacao, DOWN, buff=0.7)

        caixa = SurroundingRectangle(
            pergunta, buff=0.3, color=COR_H0, corner_radius=0.15
        )

        self.play(FadeIn(pergunta, shift=UP * 0.2), run_time=0.8)
        self.play(Create(caixa), run_time=0.6)
        self.wait(0.8)

        # ── Gancho ─────────────────────────────────────────
        gancho = Text(
            "O p-valor ajuda a responder isso.",
            font_size=30,
            color=COR_DESTAQUE,
        ).next_to(caixa, DOWN, buff=0.6)

        self.play(Write(gancho), run_time=0.9)
        self.wait(1.5)

        self.play(FadeOut(VGroup(titulo, situacao, caixa, pergunta, gancho)))


# ═══════════════════════════════════════════════════════════════
# CENA 2 — Hipótese nula e distribuição de T sob H₀
# ═══════════════════════════════════════════════════════════════

class CenaH0(Scene):
    """
    Mostra a hipótese nula e a distribuição da estatística de teste T
    assumindo que H₀ é verdadeira.
    """

    def construct(self):
        # ── Hipótese nula ───────────────────────────────────
        h0_texto = MathTex(
            r"H_0 : \text{O remédio não faz diferença}",
            font_size=38,
            color=COR_TEXTO,
        ).to_edge(UP, buff=0.6)

        self.play(Write(h0_texto), run_time=1.0)
        self.wait(0.5)

        # ── Lógica do teste ─────────────────────────────────
        logica = Text(
            "Se H₀ for verdadeira, como seria a estatística de teste T?",
            font_size=26,
            color=GREY_A,
        ).next_to(h0_texto, DOWN, buff=0.4)

        self.play(FadeIn(logica), run_time=0.7)
        self.wait(0.5)

        # ── Eixos e curva ───────────────────────────────────
        axes = eixos_padrao().shift(DOWN * 0.8)
        curva = curva_normal(axes)

        self.play(Create(axes), run_time=0.8)
        self.play(Create(curva), run_time=1.2)

        # ── Rótulo da curva ─────────────────────────────────
        label_curva = MathTex(
            r"T \sim N(0,1) \text{ sob } H_0",
            font_size=30,
            color=COR_H0,
        ).next_to(axes, RIGHT, buff=0.3).shift(UP * 1.5)

        seta_curva = CurvedArrow(
            label_curva.get_bottom(),
            axes.c2p(0, 0.4),
            color=COR_H0,
            angle=-TAU / 8,
        )

        self.play(Write(label_curva), Create(seta_curva), run_time=0.8)
        self.wait(1.0)

        # ── Interpretação: centro = 0 ────────────────────────
        ponto_zero = Dot(axes.c2p(0, 0), color=COR_DESTAQUE, radius=0.08)
        label_zero = Text("T = 0: sem efeito", font_size=22, color=COR_DESTAQUE)
        label_zero.next_to(axes.c2p(0, 0), DOWN, buff=0.2)

        self.play(FadeIn(ponto_zero), Write(label_zero), run_time=0.7)
        self.wait(1.2)

        # Guarda elementos para a próxima cena via self
        self.axes  = axes
        self.curva = curva

        self.wait(0.8)
        self.play(
            FadeOut(VGroup(h0_texto, logica, label_curva, seta_curva,
                           label_zero, ponto_zero))
        )


# ═══════════════════════════════════════════════════════════════
# CENA 3 — O valor observado t*
# ═══════════════════════════════════════════════════════════════

class CenaTObs(Scene):
    """
    Mostra o t* observado caindo na distribuição.
    Valor fixo: t* = 2,1.
    """

    T_OBS = 2.1  # valor fixo desta cena

    def construct(self):
        axes  = eixos_padrao().shift(DOWN * 0.8)
        curva = curva_normal(axes)

        self.add(axes, curva)

        # ── Título ──────────────────────────────────────────
        titulo = Text(
            "O experimento produziu um valor observado:",
            font_size=30,
            color=COR_TEXTO,
        ).to_edge(UP, buff=0.5)

        t_obs_label = MathTex(
            r"t^* = 2{,}1",
            font_size=44,
            color=COR_T_OBS,
        ).next_to(titulo, DOWN, buff=0.2)

        self.play(FadeIn(titulo), Write(t_obs_label), run_time=0.8)
        self.wait(0.4)

        # ── Linha vertical em t* ─────────────────────────────
        t_pos = axes.c2p(self.T_OBS, 0)
        t_top = axes.c2p(self.T_OBS, norm.pdf(self.T_OBS))

        linha_t = DashedLine(
            start=t_pos,
            end=t_top + UP * 2.5,
            color=COR_T_OBS,
            stroke_width=2.5,
        )

        # A linha "cai" de cima para baixo
        self.play(GrowFromPoint(linha_t, linha_t.get_top()), run_time=0.9)

        label_linha = MathTex(
            r"t^* = 2{,}1",
            font_size=28,
            color=COR_T_OBS,
        ).next_to(linha_t.get_top(), UP, buff=0.1)

        self.play(FadeIn(label_linha), run_time=0.5)
        self.wait(0.5)

        # ── Pergunta visual ──────────────────────────────────
        pergunta = Text(
            "Quão improvável é obter t ≥ 2,1 se H₀ for verdadeira?",
            font_size=25,
            color=COR_DESTAQUE,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(pergunta), run_time=0.9)
        self.wait(1.5)

        self.play(FadeOut(VGroup(titulo, t_obs_label, pergunta, label_linha, linha_t)))


# ═══════════════════════════════════════════════════════════════
# CENA 4 — p-valor como área
# ═══════════════════════════════════════════════════════════════

class CenaArea(Scene):
    """
    Revela que o p-valor é a área à direita de t*.
    Mostra o valor numérico e a fórmula formal.
    """

    T_OBS  = 2.1
    P_VAL  = round(1 - norm.cdf(2.1), 4)  # ≈ 0.0179

    def construct(self):
        axes  = eixos_padrao().shift(DOWN * 0.8)
        curva = curva_normal(axes)

        self.add(axes, curva)

        # ── Linha t* (já presente) ───────────────────────────
        t_pos = axes.c2p(self.T_OBS, 0)
        t_top = axes.c2p(self.T_OBS, norm.pdf(self.T_OBS) + 0.02)

        linha_t = DashedLine(
            start=t_pos, end=t_top + UP * 0.5,
            color=COR_T_OBS, stroke_width=2.5
        )
        self.add(linha_t)

        # ── Área da cauda ────────────────────────────────────
        area = area_cauda(axes, self.T_OBS)
        self.play(FadeIn(area), run_time=1.0)

        # ── Chave visual na área ─────────────────────────────
        # (seta apontando para o interior da área sombreada)
        meio_area_x = (self.T_OBS + 4.5) / 2
        ponto_area  = axes.c2p(meio_area_x, norm.pdf(meio_area_x) / 2)

        seta_area = Arrow(
            start=ponto_area + UP * 1.2 + RIGHT * 0.5,
            end=ponto_area,
            color=COR_AREA,
            buff=0.1,
            stroke_width=2,
        )

        label_pvalor = MathTex(
            rf"p = {self.P_VAL}",
            font_size=34,
            color=COR_AREA,
        ).next_to(seta_area.get_start(), UP, buff=0.1)

        self.play(GrowArrow(seta_area), Write(label_pvalor), run_time=0.9)
        self.wait(0.6)

        # ── Definição formal ────────────────────────────────
        definicao = MathTex(
            r"p\text{-valor} = P(T \geq t^* \mid H_0 \text{ verdadeira})",
            font_size=30,
            color=COR_TEXTO,
        ).to_edge(UP, buff=0.5)

        self.play(Write(definicao), run_time=1.0)
        self.wait(0.8)

        # ── Leitura em português ────────────────────────────
        leitura = Text(
            '"Probabilidade de ver um resultado tão extremo\n'
            'ou mais, assumindo que H₀ é verdade."',
            font_size=24,
            color=GREY_A,
            line_spacing=1.2,
        ).next_to(definicao, DOWN, buff=0.3)

        self.play(FadeIn(leitura), run_time=0.8)
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            definicao, leitura, seta_area, label_pvalor, area, linha_t
        )))


# ═══════════════════════════════════════════════════════════════
# CENA 5 — A área muda conforme t se move
# ═══════════════════════════════════════════════════════════════

class CenaMoveT(Scene):
    """
    Demonstra visualmente que quanto maior t*, menor o p-valor,
    animando o ponto t* se deslocando de 1.0 a 3.5.
    """

    def construct(self):
        axes  = eixos_padrao().shift(DOWN * 0.8)
        curva = curva_normal(axes)

        self.add(axes, curva)

        titulo = Text(
            "Quanto maior o t*, menor o p-valor",
            font_size=32, color=COR_TEXTO
        ).to_edge(UP, buff=0.5)
        self.play(Write(titulo), run_time=0.7)

        # ── Elementos dinâmicos (usamos ValueTracker) ────────
        t_tracker = ValueTracker(1.0)

        # Linha vertical
        linha_t = always_redraw(lambda: DashedLine(
            start=axes.c2p(t_tracker.get_value(), 0),
            end=axes.c2p(t_tracker.get_value(),
                         norm.pdf(t_tracker.get_value()) + 0.18),
            color=COR_T_OBS,
            stroke_width=2.5,
        ))

        # Label do t atual
        label_t = always_redraw(lambda: MathTex(
            rf"t^* = {t_tracker.get_value():.2f}",
            font_size=30, color=COR_T_OBS,
        ).next_to(
            axes.c2p(t_tracker.get_value(),
                     norm.pdf(t_tracker.get_value()) + 0.18),
            UP, buff=0.05
        ))

        # Área da cauda (recalculada a cada frame)
        area_mob = always_redraw(lambda: area_cauda(
            axes, t_tracker.get_value()
        ))

        # Label do p-valor atual
        p_label = always_redraw(lambda: MathTex(
            rf"p = {(1 - norm.cdf(t_tracker.get_value())):.4f}",
            font_size=36, color=COR_AREA,
        ).to_edge(DOWN, buff=0.6))

        self.add(area_mob, linha_t, label_t, p_label)

        # ── Animação: t desloca de 1.0 a 3.5 ────────────────
        self.play(
            t_tracker.animate.set_value(3.5),
            run_time=5,
            rate_func=linear,
        )
        self.wait(0.5)

        # ── Sentido inverso: de 3.5 a 1.0 ───────────────────
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=3,
            rate_func=linear,
        )
        self.wait(0.5)

        # ── Congela em t* = 2.1 para comparar com α ─────────
        self.play(
            t_tracker.animate.set_value(2.1),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(1.5)

        self.play(FadeOut(VGroup(titulo, linha_t, label_t, area_mob, p_label)))


# ═══════════════════════════════════════════════════════════════
# CENA 6 — Comparação com α e decisão
# ═══════════════════════════════════════════════════════════════

class CenaAlpha(Scene):
    """
    Introduz α = 0,05 como linha de corte e mostra
    a regra de decisão: p < α → rejeitar H₀.
    """

    T_OBS = 2.1
    ALPHA = 0.05
    T_ALPHA = round(norm.ppf(1 - 0.05), 4)  # ≈ 1.6449

    def construct(self):
        axes  = eixos_padrao().shift(DOWN * 0.9)
        curva = curva_normal(axes)

        self.add(axes, curva)

        # ── α = 0,05: linha vertical em t_α ─────────────────
        t_alpha_x = self.T_ALPHA

        linha_alpha = DashedLine(
            start=axes.c2p(t_alpha_x, 0),
            end=axes.c2p(t_alpha_x, 0.5),
            color=COR_ALPHA,
            stroke_width=2.5,
        )

        label_alpha = MathTex(
            r"\alpha = 0{,}05",
            font_size=28, color=COR_ALPHA
        ).next_to(axes.c2p(t_alpha_x, 0.5), UP, buff=0.1)

        self.play(Create(linha_alpha), Write(label_alpha), run_time=0.8)

        # ── Região de rejeição (sombreado verde) ─────────────
        regiao_rej = axes.get_area(
            axes.plot(lambda x: norm.pdf(x), x_range=[t_alpha_x, 4.5]),
            x_range=[t_alpha_x, 4.5],
            color=COR_ALPHA,
            opacity=0.15,
        )
        label_rej = Text("Região de rejeição", font_size=22, color=COR_ALPHA)
        label_rej.move_to(axes.c2p(2.8, 0.15))

        self.play(FadeIn(regiao_rej), Write(label_rej), run_time=0.7)

        # ── t* observado ────────────────────────────────────
        linha_t = DashedLine(
            start=axes.c2p(self.T_OBS, 0),
            end=axes.c2p(self.T_OBS, 0.5),
            color=COR_T_OBS, stroke_width=2.5,
        )
        label_t = MathTex(
            r"t^* = 2{,}1", font_size=28, color=COR_T_OBS
        ).next_to(axes.c2p(self.T_OBS, 0.5), UP + LEFT * 0.5, buff=0.1)

        self.play(Create(linha_t), Write(label_t), run_time=0.7)
        self.wait(0.5)

        # ── Comparação formal ────────────────────────────────
        pval_num = round(1 - norm.cdf(self.T_OBS), 4)

        comparacao = VGroup(
            MathTex(
                rf"p = {pval_num}", font_size=32, color=COR_AREA
            ),
            MathTex(r"<", font_size=32, color=COR_TEXTO),
            MathTex(r"\alpha = 0{,}05", font_size=32, color=COR_ALPHA),
        ).arrange(RIGHT, buff=0.3)

        comparacao.to_edge(UP, buff=0.5)

        self.play(Write(comparacao), run_time=0.8)

        # ── Caixa de decisão ────────────────────────────────
        decisao = Text(
            "→  Rejeitamos H₀",
            font_size=34,
            color=COR_DESTAQUE,
        ).next_to(comparacao, DOWN, buff=0.3)

        caixa = SurroundingRectangle(
            decisao, buff=0.25, color=COR_DESTAQUE, corner_radius=0.1
        )

        self.play(Write(decisao), Create(caixa), run_time=0.8)
        self.wait(1.0)

        # ── Nota cuidadosa ───────────────────────────────────
        nota = Text(
            "Isso não prova que o remédio funciona;\n"
            "diz que os dados seriam muito improváveis sob H₀.",
            font_size=22,
            color=GREY_A,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(nota), run_time=0.7)
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            comparacao, decisao, caixa, nota,
            linha_alpha, label_alpha, regiao_rej, label_rej,
            linha_t, label_t,
        )))


# ═══════════════════════════════════════════════════════════════
# CENA 7 — O que o p-valor NÃO é
# ═══════════════════════════════════════════════════════════════

class CenaMitos(Scene):
    """
    Desconstrói os três mitos mais comuns sobre o p-valor.
    Cada mito aparece com um ✗ vermelho e depois a versão correta.
    """

    MITOS = [
        {
            "errado": "p-valor = probabilidade de H₀ ser verdadeira",
            "certo":  "É P(dados tão extremos | H₀ verdadeira),\nnão P(H₀ | dados).",
        },
        {
            "errado": "p < 0,05 prova que o efeito é real",
            "certo":  "Rejeitar H₀ não elimina a chance de erro\n"
                      "do tipo I (falso positivo).",
        },
        {
            "errado": "p grande significa que H₀ é verdadeira",
            "certo":  "Não rejeitar H₀ não é o mesmo\n"
                      "que confirmar H₀.",
        },
    ]

    def construct(self):
        titulo = Text(
            "O que o p-valor NÃO é",
            font_size=40,
            color=COR_T_OBS,
        ).to_edge(UP, buff=0.5)

        self.play(Write(titulo), run_time=0.7)

        y_base = 1.8

        for i, mito in enumerate(self.MITOS):
            # ── Rótulo do mito ───────────────────────────────
            numero = Text(
                f"Mito {i+1}", font_size=24, color=GREY_B
            ).move_to(LEFT * 4.5 + UP * (y_base - i * 2.4))

            # ── Frase errada ─────────────────────────────────
            errado = Text(
                mito["errado"],
                font_size=24,
                color=COR_T_OBS,
            ).next_to(numero, RIGHT, buff=0.3)

            x_mark = Text("✗", font_size=30, color=COR_T_OBS)
            x_mark.next_to(errado, LEFT, buff=0.15)

            self.play(FadeIn(numero), FadeIn(x_mark), Write(errado), run_time=0.6)

            # ── Correção ─────────────────────────────────────
            certo = Text(
                mito["certo"],
                font_size=22,
                color=GREEN_B,
                line_spacing=1.1,
            ).next_to(errado, DOWN, buff=0.15, aligned_edge=LEFT)

            check = Text("✓", font_size=26, color=GREEN_B)
            check.next_to(certo, LEFT, buff=0.15)

            self.play(FadeIn(check), Write(certo), run_time=0.7)
            self.wait(0.8)

        self.wait(1.5)

        # ── Resumo final ─────────────────────────────────────
        self.play(FadeOut(*self.mobjects))

        resumo = VGroup(
            Text("Resumo", font_size=36, color=COR_DESTAQUE),
            Text(
                "O p-valor mede o quão compatíveis os dados são com H₀.",
                font_size=26, color=COR_TEXTO,
            ),
            Text(
                "Ele sozinho não diz nada sobre a importância prática do efeito.",
                font_size=26, color=GREY_A,
            ),
            MathTex(
                r"p\text{-valor} = P(T \geq t^* \mid H_0)",
                font_size=34, color=COR_H0,
            ),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)

        resumo.move_to(ORIGIN)

        self.play(FadeIn(resumo, shift=UP * 0.3), run_time=1.0)
        self.wait(3.0)

        self.play(FadeOut(resumo))


# ═══════════════════════════════════════════════════════════════
# Cena combinada — roda tudo em sequência (desenvolvimento rápido)
# ═══════════════════════════════════════════════════════════════

class VideoCompleto(Scene):
    """
    Renderiza todas as cenas em sequência num único arquivo.
    Use durante o desenvolvimento:  manim -pql pvalor_video.py VideoCompleto
    """

    def construct(self):
        for CenaClass in [
            CenaContexto,
            CenaH0,
            CenaTObs,
            CenaArea,
            CenaMoveT,
            CenaAlpha,
            CenaMitos,
        ]:
            cena = CenaClass()
            cena.renderer = self.renderer
            cena.camera   = self.camera
            cena.construct()
            self.wait(0.3)
