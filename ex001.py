from manim import *

class PrimeiraCena(Scene):
    def construct(self):
        formula = MathTex(r"P(A|B) = \frac{P(B|A)P(A)}{P(B)} = \text{Seu Otário}")

        self.play(Write(formula))
        self.wait(1)

        caixa = SurroundingRectangle(formula, color=BLUE)
        self.play(Create(caixa))
        self.wait(2)
