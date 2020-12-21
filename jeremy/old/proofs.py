from manimlib.imports import *


class main(Scene):
    def title(self, i, text):
        t = TextMobject(r"\textbf{\heiti {%d.%s}}" % (i, text), color=YELLOW).to_edge(UP)
        line = Line(color=YELLOW).set_width(FRAME_WIDTH - 2).next_to(t, DOWN)
        self.play(Write(t), GrowFromCenter(line))
        self.wait()

    def proof(self, *texts, time=None):
        v = VGroup(*[TextMobject(text) for text in texts]).arrange(DOWN).scale(1.5)
        if time is not None:
            for text, t in zip(v, time):
                self.play(Write(text), run_time=t)
        else:
            for text in v:
                self.play(Write(text))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def construct(self):
        for i, (title, texts) in enumerate(zip(
                ["矛盾证明法",
                 "拖延证明法",
                 "循环拖延假装证过了法",
                 "无限期拖延证明法",
                 "恐吓证明法",
                 "手势证明法",
                 "个人信念证明法",
                 "无法想象证明法",
                 "责任外包证明法",
                 "不作为证明法",
                 "难以辨认符号证明法",
                 "权威证明法",
                 "模糊权威证明法",
                 "赌咒证明法",
                 "旁征博引证明法",
                 "归结为错误问题证明法",
                 "~$404$证明法",
                 ],
                [("这个命题与莱昂纳多·牛顿·轩兔", "的一个著名结果矛盾."),
                 ("我们下节课再证明这个.",),
                 ("正如我们上节课证明的......",),
                 ("正如我上节课说的，", "我们下节课再证明这个.",),
                 ("傻子都知道，", "这个证明是显而易见的.",),
                 ("【拉手风琴】","没有人，","比我，","更懂，","这个证明！"),
                 ("我深深地相信，",r"$\pi+\e$是个无理数."),
                 (r"我无法想象$\pi+\e$是个有理数，","所以它一定是无理数."),
                 (r"细节留给读者.",),
                 (r"还剩$397$种情况，", r"不过证明是类似的."),
                 (r"如果你研读接下来定义的500页符号，","就知道它是对的了."),
                 (r"欧拉托梦给我了，",r"告诉我$\pi+\e$是无理数."),
                 (r"众所周知，",r"$\pi+\e$是个无理数."),
                 (r"如果$\pi+\e$不是无理数，","我当场跪下来叫你爸爸."),
                 (r"$\pi+\e$的无理性可以通过",r"在特征数大于11的","非交换域上的非紧致无穷维拟流形","上应用接触数第三定理得证."),
                 (r"要证明$\pi+\e$是无理数，",r"我们先把它归结为勾股定理."),
                 (r"$\pi+\e$是无理数的证明，",r"能容易地在Pzxxwohccnd个人出版的",r"论文集第$1\frac 23$卷$-6$页找到."),
                 ]
        )):
            if i in (3,7,9,15) :
                self.title(i + 1, title)
                self.proof(*texts, time=[2,2])
            else:
                self.title(i+1, title)
                self.proof(*texts)