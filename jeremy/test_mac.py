from manimlib.imports import *
import matplotlib.pyplot as plt

class pi(TeacherStudentsScene):
    def construct(self):
        # you = self.pi_creature.move_to(ORIGIN)
        # a = [Coin().to_edge(i) for i in [LEFT, UP, RIGHT, DOWN]]
        # for i in a:
        #     self.play(FadeIn(i))
        #     self.wait()

        # self.play(you.change, "question")
        t = self.teacher_says("hello")
        self.wait(4)


class Cut(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        cut = BranchCut()
        self.play(ShowCreation(cut))
