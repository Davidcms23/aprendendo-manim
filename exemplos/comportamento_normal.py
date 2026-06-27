from manim import *
import math

class EvolucaoNormal(Scene):
    def construct(self):
        # 1. Apresentação da Função de Densidade
        formula = MathTex(
            r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}"
        )
        self.play(Write(formula), run_time=2)
        self.wait(1)
        # Realoca a fórmula para o topo da tela para liberar espaço cartesiano
        self.play(formula.animate.to_edge(UP).scale(0.8))

        # 2. Configuração do Plano Cartesiano (Corrigida)
        ax = Axes(
            x_range=[-7, 7, 1],
            y_range=[0, 0.6, 0.1],
            x_length=10,  # Define a largura física máxima na tela
            y_length=4,   # Restringe a altura para evitar sobreposição
            axis_config={"color": BLUE, "include_numbers": False},
        ).shift(DOWN * 1.2) # Ancara o sistema de coordenadas na metade inferior

        # 3. Inicialização dos Rastreadores de Parâmetros
        mu_tracker = ValueTracker(3.0)
        sigma_tracker = ValueTracker(2.0)

        # 4. Construção da Lógica da Curva Atualizável
        def get_normal_curve():
            m = mu_tracker.get_value()
            s = sigma_tracker.get_value()
            return ax.plot(
                lambda x: math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi)),
                color=YELLOW
            )

        curva = always_redraw(get_normal_curve)

        # 5. Configuração dos Rótulos Dinâmicos (DecimalNumber evita gargalos de compilação)
        mu_label = MathTex(r"\mu = ")
        mu_value = DecimalNumber(3.0, num_decimal_places=1)
        mu_value.add_updater(lambda m: m.set_value(mu_tracker.get_value()))

        sigma_label = MathTex(r",\quad \sigma = ")
        sigma_value = DecimalNumber(2.0, num_decimal_places=1)
        sigma_value.add_updater(lambda s: s.set_value(sigma_tracker.get_value()))

        # Agrupamento e posicionamento dos rótulos
        parametros = VGroup(mu_label, mu_value, sigma_label, sigma_value).arrange(RIGHT, buff=0.1)
        parametros.next_to(ax, UP, buff=0.5)

        # 6. Execução Visual: Setup Inicial
        self.play(Create(ax))
        self.play(Create(curva), Write(parametros))
        self.wait(1)

        # 7. Execução Visual: Interpolação da Média (Translação espacial)
        self.play(mu_tracker.animate.set_value(0.0), run_time=3)
        self.wait(1)

        # 8. Execução Visual: Interpolação do Desvio Padrão (Achatamento/Dispersão)
        self.play(sigma_tracker.animate.set_value(1.0), run_time=3)
        self.wait(1)

        # 9. Conclusão da Normal Padrão
        padrao_label = Text("Distribuição Normal Padrão (Z)", color=GREEN).scale(0.8)
        padrao_label.next_to(parametros, UP)

        area_z = always_redraw(lambda: ax.get_area(curva, color=GREEN, opacity=0.3))

        self.play(Write(padrao_label), FadeIn(area_z))
        self.wait(3)
