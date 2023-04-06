from __future__ import annotations

from colour import Color

from manimlib.constants import BLACK, RED, YELLOW, WHITE, GOLD
from manimlib.constants import DL, DOWN, DR, LEFT, RIGHT, UL, UR
from manimlib.constants import SMALL_BUFF
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle, RoundedRectangle, Ellipse
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.customization import get_customization

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import ManimColor, Self


class SurroundingRectangle(Rectangle):
    def __init__(
        self,
        mobject: Mobject,
        buff: float = SMALL_BUFF,
        color: ManimColor = YELLOW,
        **kwargs
    ):
        super().__init__(
            width=mobject.get_width() + 2 * buff,
            height=mobject.get_height() + 2 * buff,
            color=color,
            **kwargs
        )
        self.move_to(mobject)

class SurroundingRoundedRectangle(RoundedRectangle):
    CONFIG = {
        "color": YELLOW,
        "buff": SMALL_BUFF,
        "corner_radius": 0.5,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        kwargs["width"] = mobject.get_width() + 2 * self.buff
        kwargs["height"] = mobject.get_height() + 2 * self.buff
        RoundedRectangle.__init__(self, **kwargs)
        self.move_to(mobject)


class BackgroundRectangle(SurroundingRectangle):
    def __init__(
        self,
        mobject: Mobject,
        color: ManimColor = None,
        stroke_width: float = 0,
        stroke_opacity: float = 0,
        fill_opacity: float = 0.75,
        buff: float = 0,
        **kwargs
    ):
        if color is None:
            color = get_customization()['style']['background_color']
        super().__init__(
            mobject,
            color=color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            fill_opacity=fill_opacity,
            buff=buff,
            **kwargs
        )
        self.original_fill_opacity = fill_opacity

    def pointwise_become_partial(self, mobject: Mobject, a: float, b: float) -> Self:
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style(
        self,
        stroke_color: ManimColor | None = None,
        stroke_width: float | None = None,
        fill_color: ManimColor | None = None,
        fill_opacity: float | None = None,
        family: bool = True
    ) -> Self:
        # Unchangeable style, except for fill_opacity
        VMobject.set_style(
            self,
            stroke_color=BLACK,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=fill_opacity
        )
        return self

    def get_fill_color(self) -> Color:
        return Color(self.color)

class BackgroundRoundedRectangle(SurroundingRoundedRectangle):
    CONFIG = {
        "color": GOLD,
        "stroke_width": 0,
        "stroke_opacity": 0,
        "fill_opacity": 0.15,
        "buff": 0.2,
        "corner_radius": 0.5
    }

    def __init__(self, mobject, **kwargs):
        SurroundingRoundedRectangle.__init__(self, mobject, **kwargs)
        self.original_fill_opacity = self.fill_opacity

    def pointwise_become_partial(self, mobject, a, b):
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style_data(self,
                       stroke_color=None,
                       stroke_width=None,
                       fill_color=None,
                       fill_opacity=None,
                       family=True
                       ):
        # Unchangable style, except for fill_opacity
        VMobject.set_style_data(
            self,
            stroke_color=BLACK,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=fill_opacity
        )
        return self

    def get_fill_color(self):
        return Color(self.color)

class Cross(VGroup):
    def __init__(
        self,
        mobject: Mobject,
        stroke_color: ManimColor = RED,
        stroke_width: float | Sequence[float] = [0, 6, 0],
        **kwargs
    ):
        super().__init__(
            Line(UL, DR),
            Line(UR, DL),
        )
        self.insert_n_curves(20)
        self.replace(mobject, stretch=True)
        self.set_stroke(stroke_color, width=stroke_width)


class Underline(Line):
    def __init__(
        self,
        mobject: Mobject,
        buff: float = SMALL_BUFF,
        stroke_color=WHITE,
        stroke_width: float | Sequence[float] = [0, 3, 3, 0],
        **kwargs
    ):
        super().__init__(
            LEFT, RIGHT,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            **kwargs
        )
        self.insert_n_curves(30)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=buff)
