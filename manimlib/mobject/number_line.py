from manimlib.constants import *
from manimlib.mobject.geometry import Line
from manimlib.mobject.numbers import DecimalNumber
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.utils.bezier import interpolate
from manimlib.utils.config_ops import digest_config
from manimlib.utils.config_ops import merge_dicts_recursively
from manimlib.utils.iterables import list_difference_update
from manimlib.utils.simple_functions import fdiv
from manimlib.utils.space_ops import normalize


class NumberLine(Line):
    CONFIG = {
        "color": GREY_B,
        "stroke_width": 2,
        # List of 2 or 3 elements, x_min, x_max, step_size
        "x_range": [-8, 8, 1],
        # How big is one one unit of this number line in terms of absolute spacial distance
        "unit_size": 1,
        "width": None,
        "include_ticks": True,
        "tick_size": 0.1,
        "longer_tick_multiple": 1.5,
        "tick_offset": 0,
        # Change name
        "numbers_with_elongated_ticks": [],
        "include_numbers": False,
        "line_to_number_direction": DOWN,
        "line_to_number_buff": MED_SMALL_BUFF,
        "include_tip": False,
        "tip_config": {
            "width": 0.25,
            "length": 0.25,
        },
        "decimal_number_config": {
            "num_decimal_places": 0,
            "height": 0.25,
        },
        "exclude_zero_from_default_numbers": False,
    }

    def __init__(self, x_range=None, **kwargs):
        digest_config(self, kwargs)
        if x_range is None:
            x_range = self.x_range
        if len(x_range) == 2:
            x_range = [*x_range, 1]

        x_min, x_max, x_step = x_range
        # A lot of old scenes pass in x_min or x_max explicitly,
        # so this is just here to keep those workin
        self.x_min = kwargs.get("x_min", x_min)
        self.x_max = kwargs.get("x_max", x_max)
        self.x_step = kwargs.get("x_step", x_step)

        super().__init__(self.x_min * RIGHT, self.x_max * RIGHT, **kwargs)
        if self.width:
            self.set_width(self.width)
        else:
            self.scale(self.unit_size)
        self.center()

        if self.include_tip:
            self.add_tip()
            self.tip.set_stroke(
                self.stroke_color,
                self.stroke_width,
            )
        if self.include_ticks:
            self.add_ticks()
        if self.include_numbers:
            self.add_numbers()

    def get_tick_range(self):
        if self.include_tip:
            x_max = self.x_max
        else:
            x_max = self.x_max + self.x_step
        return np.arange(self.x_min, x_max, self.x_step)

    def add_ticks(self):
        ticks = VGroup()
        for x in self.get_tick_range():
            size = self.tick_size
            if x in self.numbers_with_elongated_ticks:
                size *= self.longer_tick_multiple
            ticks.add(self.get_tick(x, size))
        self.add(ticks)
        self.ticks = ticks

    def get_tick(self, x, size=None):
        if size is None:
            size = self.tick_size
        result = Line(size * DOWN, size * UP)
        result.rotate(self.get_angle())
        result.move_to(self.number_to_point(x))
        result.match_style(self)
        return result

    def get_tick_marks(self):
        return self.tick_marks

    def number_to_point(self, number):
        alpha = float(number - self.x_min) / (self.x_max - self.x_min)
        return interpolate(self.get_start(), self.get_end(), alpha)

    def point_to_number(self, point):
        start, end = self.get_start_and_end()
        unit_vect = normalize(end - start)
        proportion = fdiv(
            np.dot(point - start, unit_vect),
            np.dot(end - start, unit_vect),
        )
        return interpolate(self.x_min, self.x_max, proportion)

    def n2p(self, number):
        """Abbreviation for number_to_point"""
        return self.number_to_point(number)

    def p2n(self, point):
        """Abbreviation for point_to_number"""
        return self.point_to_number(point)

    def get_unit_size(self):
        return (self.x_max - self.x_min) / self.get_length()

    def get_number_mobject(self, x,
                           number_config=None,
                           direction=None,
                           buff=None):
        if number_config is None:
            number_config = {}
        number_config = merge_dicts_recursively(
            self.decimal_number_config, number_config
        )
        if direction is None:
            direction = self.line_to_number_direction
        if buff is None:
            buff = self.line_to_number_buff

        num_mob = DecimalNumber(x, **number_config)
        num_mob.next_to(
            self.number_to_point(x),
            direction=direction,
            buff=buff
        )
        if x < 0 and self.line_to_number_direction[0] == 0:
            # Align without the minus sign
            num_mob.shift(num_mob[0].get_width() * LEFT / 2)
        return num_mob

    def add_numbers(self, x_values=None, excluding=None, **kwargs):
        if x_values is None:
            x_values = self.get_tick_range()
        if excluding is not None:
            x_values = list_difference_update(x_values, excluding)

        self.numbers = VGroup()
        for x in x_values:
            self.numbers.add(self.get_number_mobject(x, **kwargs))
        self.add(self.numbers)
        return self.numbers


class UnitInterval(NumberLine):
    CONFIG = {
        "x_range": [0, 1, 0.1],
        "unit_size": 10,
        "numbers_with_elongated_ticks": [0, 1],
        "decimal_number_config": {
            "num_decimal_places": 1,
        }
    }
