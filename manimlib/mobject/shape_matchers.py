from __future__ import annotations

from manimlib.constants import *
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle, RoundedRectangle, Ellipse
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.color import Color
from manimlib.utils.customization import get_customization
from manimlib.utils.config_ops import digest_config

<<<<<<< HEAD
class SurroundingEllipse(Ellipse):
    CONFIG = {
        "color": YELLOW,
        "buff": LARGE_BUFF,
    }
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        kwargs["width"] = mobject.get_width() + 2 * self.buff
        kwargs["height"] = mobject.get_height() + 2 * self.buff
        Ellipse.__init__(self, **kwargs)
        self.move_to(mobject)
=======
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union, Sequence
    from manimlib.mobject.mobject import Mobject
    ManimColor = Union[str, Color, Sequence[float]]

>>>>>>> 9d7db7aacd7116a8dbce0781f64ba44f065a7e39

class SurroundingRectangle(Rectangle):
    CONFIG = {
        "color": YELLOW,
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject: Mobject, **kwargs):
        digest_config(self, kwargs)
        kwargs["width"] = mobject.get_width() + 2 * self.buff
        kwargs["height"] = mobject.get_height() + 2 * self.buff
        Rectangle.__init__(self, **kwargs)
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
    CONFIG = {
        "stroke_width": 0,
        "stroke_opacity": 0,
        "fill_opacity": 0.75,
        "buff": 0
    }

    def __init__(self, mobject: Mobject, color: ManimColor = None, **kwargs):
        if color is None:
            color = get_customization()['style']['background_color']
        SurroundingRectangle.__init__(self, mobject, color=color, **kwargs)
        self.original_fill_opacity = self.fill_opacity

    def pointwise_become_partial(self, mobject: Mobject, a: float, b: float):
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style_data(
        self,
        stroke_color: ManimColor | None = None,
        stroke_width: float | None = None,
        fill_color: ManimColor | None = None,
        fill_opacity: float | None = None,
        family: bool = True
    ):
        # Unchangeable style, except for fill_opacity
        VMobject.set_style_data(
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
    CONFIG = {
        "stroke_color": RED,
        "stroke_width": [0, 6, 0],
    }

<<<<<<< HEAD
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
=======
    def __init__(self, mobject: Mobject, **kwargs):
>>>>>>> 9d7db7aacd7116a8dbce0781f64ba44f065a7e39
        super().__init__(
            Line(UL, DR),
            Line(UR, DL),
        )
        self.insert_n_curves(2)
        self.replace(mobject, stretch=True)
        self.set_stroke(self.stroke_color, width=self.stroke_width)


class Underline(Line):
    CONFIG = {
        "buff": SMALL_BUFF,
    }

    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(LEFT, RIGHT, **kwargs)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)
