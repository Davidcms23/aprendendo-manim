from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(WHITE, opacity=.2)
        self.play(Create(circle))
