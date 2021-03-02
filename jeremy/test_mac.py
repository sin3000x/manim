from manimlib import *


class Chang(Scene):
    def construct(self):
        hello = Text("妈妈")
        self.play(Write(hello))
        self.wait()
        self.embed()

class Tu(Scene):
    def construct(self):
        v = Vocabulary()
        self.add(v)


class Test(Scene):
    def construct(self):
        creature = BunnyEars()
        # for i in range(len(creature)):
        #     creature[i].set_stroke(width=2)
        creature.set_stroke(width=1)
        self.add(creature)