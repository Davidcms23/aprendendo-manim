from manim import *
import numpy as np

class SValor(Scene):
    def construct(self):
        # ---------- Título ----------
        titulo = Text("O s-valor: uma medida de evidência alternativa", font_size=36)
        subtitulo = Text("Patriota (2018)", font_size=24, color=GRAY_B)
        subtitulo.next_to(titulo, DOWN, buff=0.2)
        self.play(Write(titulo), FadeIn(subtitulo))
        self.wait(1)
        self.play(FadeOut(titulo), FadeOut(subtitulo))

        # ---------- Eixos: espaço paramétrico Theta ----------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=7,
            axis_config={"include_tip": True, "color": GRAY_B},
        ).shift(LEFT * 2.2)

        theta1_label = MathTex(r"\theta_1", font_size=32).next_to(axes.x_axis.get_end(), RIGHT)
        theta2_label = MathTex(r"\theta_2", font_size=32).next_to(axes.y_axis.get_end(), UP)
        theta_space_label = MathTex(r"\Theta", font_size=40).move_to(axes.c2p(-2.6, 2.6))

        self.play(Create(axes), Write(theta1_label), Write(theta2_label), Write(theta_space_label))

        # ---------- EMV (theta hat) ----------
        theta_hat_point = axes.c2p(-0.8, -0.6)
        theta_hat_dot = Dot(theta_hat_point, color=YELLOW, radius=0.08)
        theta_hat_label = MathTex(r"\hat{\theta}", font_size=32, color=YELLOW).next_to(theta_hat_dot, DOWN, buff=0.15)

        self.play(FadeIn(theta_hat_dot, scale=0.5), Write(theta_hat_label))
        self.wait(0.3)

        # ---------- Hipótese nula: Theta_0 como uma curva (reta) ----------
        # H0: theta1 = theta2  -> reta diagonal, distante do EMV
        # Definida em coordenadas do "mundo" (não em pixels) para permitir geometria exata
        p_theta_hat = np.array([-0.8, -0.6])
        p_line_a = np.array([1.0, 2.6])
        p_line_b = np.array([2.6, 1.0])

        line_start = axes.c2p(*p_line_a)
        line_end = axes.c2p(*p_line_b)
        theta0_curve = Line(line_start, line_end, color=RED, stroke_width=6)
        theta0_label = MathTex(r"\Theta_0", font_size=36, color=RED).next_to(theta0_curve, UR, buff=0.1)

        info_h0 = Text("H₀ : θ ∈ Θ₀  (por exemplo, θ₁ = θ₂ = valores altos)", font_size=24).to_edge(DOWN)
        self.play(Create(theta0_curve), Write(theta0_label), FadeIn(info_h0))
        self.wait(1.5)
        self.play(FadeOut(info_h0))

        # ---------- Geometria exata: ponto mais próximo de theta_hat na reta ----------
        d = p_line_b - p_line_a
        t = np.dot(p_theta_hat - p_line_a, d) / np.dot(d, d)
        t_clamped = np.clip(t, 0, 1)
        p_touch = p_line_a + t_clamped * d
        max_radius_world = np.linalg.norm(p_touch - p_theta_hat)  # distância = raio de toque

        # converte o raio (em unidades do eixo) para o comprimento em pixels da cena
        radius_end_point = axes.c2p(p_theta_hat[0] + max_radius_world, p_theta_hat[1])
        max_radius_scene = np.linalg.norm(np.array(radius_end_point) - np.array(theta_hat_point))

        # ---------- Região de confiança crescente (círculo, geometria exata) ----------
        def make_circle(radius_scene):
            circle = Circle(
                radius=max(radius_scene, 0.02),
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.25,
                stroke_width=3,
            )
            circle.move_to(theta_hat_point)
            return circle

        conf_label = MathTex(r"\Lambda_\alpha", font_size=32, color=BLUE)

        circle = make_circle(0.02)
        conf_label.next_to(circle, LEFT, buff=0.15)
        self.play(Create(circle), Write(conf_label))

        # Crescimento gradual EXATO até tocar Theta_0
        n_steps = 40
        for i in range(1, n_steps + 1):
            frac = i / n_steps
            new_circle = make_circle(max_radius_scene * frac)
            new_label = MathTex(r"\Lambda_\alpha", font_size=32, color=BLUE)
            new_label.next_to(new_circle, LEFT, buff=0.15)
            self.play(
                Transform(circle, new_circle),
                Transform(conf_label, new_label),
                run_time=0.06,
            )

        self.play(FadeOut(info_growing))

        # ---------- Momento do toque: destaque (ponto exato calculado) ----------
        touch_point = axes.c2p(*p_touch)
        touch_dot = Dot(touch_point, color=GREEN, radius=0.09)
        touch_flash = Flash(touch_dot, color=GREEN, line_length=0.3, num_lines=12)

        self.play(FadeIn(touch_dot), touch_flash, FadeIn(info_touch))
        self.wait(1.5)

        # ---------- Fórmula do s-valor ----------
        formula = MathTex(
            r"s(X,\Theta_0) = \max\{0,\ \sup\{\alpha \in (0,1) : \Lambda_\alpha \cap \Theta_0 \neq \varnothing\}\}",
            font_size=30,
        ).to_edge(DOWN).shift(UP * 0.1)

        self.play(FadeOut(info_touch), Write(formula))
        self.wait(3)

        self.play(
            FadeOut(formula), FadeOut(touch_dot), FadeOut(circle), FadeOut(conf_label),
        )


        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)
