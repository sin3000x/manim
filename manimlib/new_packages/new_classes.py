import os
import numpy as np
from manimlib import *


class Heiti(Text):
    CONFIG = {
        "underline": True,
        "color": YELLOW
    }

    def __init__(self, *tex_strings, **kwargs):
        digest_config(self, kwargs)
        if self.underline is True:
            tmp = [r"\underline{\textbf{\heiti %s}}" % string for string in tex_strings]
            super().__init__(*tmp, **kwargs)
        else:
            tmp = [r"\textbf{\heiti %s}" % string for string in tex_strings]
            super().__init__(self, *tmp, **kwargs)


class Logo(VMobject):
    CONFIG = {
        "pupil_radius": 1.0,
        "outer_radius": 2.0,
        "iris_background_blue": "#74C0E3",
        "iris_background_brown": "#8C6239",
        "blue_spike_colors": [
            "#528EA3",
            "#3E6576",
            "#224C5B",
            BLACK,
        ],
        "brown_spike_colors": [
            "#754C24",
            "#603813",
            "#42210b",
            BLACK,
        ],
        "n_spike_layers": 4,
        "n_spikes": 28,
        "spike_angle": TAU / 28,
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.add_iris_back()
        self.add_spikes()
        self.add_pupil()

    def add_iris_back(self):
        blue_iris_back = AnnularSector(
            inner_radius=self.pupil_radius,
            outer_radius=self.outer_radius,
            angle=270 * DEGREES,
            start_angle=180 * DEGREES,
            fill_color=self.iris_background_blue,
            fill_opacity=1,
            stroke_width=0,
        )
        brown_iris_back = AnnularSector(
            inner_radius=self.pupil_radius,
            outer_radius=self.outer_radius,
            angle=90 * DEGREES,
            start_angle=90 * DEGREES,
            fill_color=self.iris_background_brown,
            fill_opacity=1,
            stroke_width=0,
        )
        self.iris_background = VGroup(
            blue_iris_back,
            brown_iris_back,
        )
        self.add(self.iris_background)

    def add_spikes(self):
        layers = VGroup()
        radii = np.linspace(
            self.outer_radius,
            self.pupil_radius,
            self.n_spike_layers,
            endpoint=False,
        )
        radii[:2] = radii[1::-1]  # Swap first two
        if self.n_spike_layers > 2:
            radii[-1] = interpolate(
                radii[-1], self.pupil_radius, 0.25
            )

        for radius in radii:
            tip_angle = self.spike_angle
            half_base = radius * np.tan(tip_angle)
            triangle, right_half_triangle = [
                Polygon(
                    radius * UP,
                    half_base * RIGHT,
                    vertex3,
                    fill_opacity=1,
                    stroke_width=0,
                )
                for vertex3 in (half_base * LEFT, ORIGIN,)
            ]
            left_half_triangle = right_half_triangle.copy()
            left_half_triangle.flip(UP, about_point=ORIGIN)

            n_spikes = self.n_spikes
            full_spikes = [
                triangle.copy().rotate(
                    -angle,
                    about_point=ORIGIN
                )
                for angle in np.linspace(
                    0, TAU, n_spikes, endpoint=False
                )
            ]
            index = (3 * n_spikes) // 4
            if radius == radii[0]:
                layer = VGroup(*full_spikes)
                layer.rotate(
                    -TAU / n_spikes / 2,
                    about_point=ORIGIN
                )
                layer.brown_index = index
            else:
                half_spikes = [
                    right_half_triangle.copy(),
                    left_half_triangle.copy().rotate(
                        90 * DEGREES, about_point=ORIGIN,
                    ),
                    right_half_triangle.copy().rotate(
                        90 * DEGREES, about_point=ORIGIN,
                    ),
                    left_half_triangle.copy()
                ]
                layer = VGroup(*it.chain(
                    half_spikes[:1],
                    full_spikes[1:index],
                    half_spikes[1:3],
                    full_spikes[index + 1:],
                    half_spikes[3:],
                ))
                layer.brown_index = index + 1

            layers.add(layer)

        # Color spikes
        blues = self.blue_spike_colors
        browns = self.brown_spike_colors
        for layer, blue, brown in zip(layers, blues, browns):
            index = layer.brown_index
            layer[:index].set_color(blue)
            layer[index:].set_color(brown)

        self.spike_layers = layers
        self.add(layers)

    def add_pupil(self):
        self.pupil = Circle(
            radius=self.pupil_radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            sheen=0.0,
        )
        self.pupil.rotate(90 * DEGREES)
        self.add(self.pupil)

    def cut_pupil(self):
        pupil = self.pupil
        center = pupil.get_center()
        new_pupil = VGroup(*[
            pupil.copy().pointwise_become_partial(pupil, a, b)
            for (a, b) in [(0.25, 1), (0, 0.25)]
        ])
        for sector in new_pupil:
            sector.add_cubic_bezier_curve_to([
                sector.points[-1],
                *[center] * 3,
                *[sector.points[0]] * 2
            ])
        self.remove(pupil)
        self.add(new_pupil)
        self.pupil = new_pupil

    def get_blue_part_and_brown_part(self):
        if len(self.pupil) == 1:
            self.cut_pupil()
        # circle = Circle()
        # circle.set_stroke(width=0)
        # circle.set_fill(BLACK, opacity=1)
        # circle.match_width(self)
        # circle.move_to(self)
        blue_part = VGroup(
            self.iris_background[0],
            *[
                layer[:layer.brown_index]
                for layer in self.spike_layers
            ],
            self.pupil[0],
        )
        brown_part = VGroup(
            self.iris_background[1],
            *[
                layer[layer.brown_index:]
                for layer in self.spike_layers
            ],
            self.pupil[1],
        )
        return blue_part, brown_part


# Cards
class DeckOfCards(VGroup):
    def __init__(self, **kwargs):
        possible_values = list(map(str, list(range(1, 11)))) + ["J", "Q", "K"]
        possible_suits = ["hearts", "diamonds", "spades", "clubs"]
        VGroup.__init__(self, *[
            PlayingCard(value=value, suit=suit, **kwargs)
            for value in possible_values
            for suit in possible_suits
        ])


class PlayingCard(VGroup):
    CONFIG = {
        "value": None,
        "suit": None,
        "key": None,  # String like "8H" or "KS"
        "height": 2,
        "height_to_width": 3.5 / 2.5,
        "card_height_to_symbol_height": 7,
        "card_width_to_corner_num_width": 10,
        "card_height_to_corner_num_height": 10,
        "color": GREY,
        "turned_over": False,
        "possible_suits": ["hearts", "diamonds", "spades", "clubs"],
        "possible_values": list(map(str, list(range(2, 11)))) + ["J", "Q", "K", "A"],
    }

    def __init__(self, key=None, **kwargs):
        VGroup.__init__(self, key=key, **kwargs)

    def generate_points(self):
        self.add(Rectangle(
            height=self.height,
            width=self.height / self.height_to_width,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=self.color,
            fill_opacity=1,
        ))
        if self.turned_over:
            self.set_fill(DARK_GREY)
            self.set_stroke(LIGHT_GREY)
            contents = VectorizedPoint(self.get_center())
        else:
            value = self.get_value()
            symbol = self.get_symbol()
            design = self.get_design(value, symbol)
            corner_numbers = self.get_corner_numbers(value, symbol)
            contents = VGroup(design, corner_numbers)
            self.design = design
            self.corner_numbers = corner_numbers
        self.add(contents)

    def get_value(self):
        value = self.value
        if value is None:
            if self.key is not None:
                value = self.key[:-1]
            else:
                value = random.choice(self.possible_values)
        value = str(value).upper()
        if value == "1":
            value = "A"
        if value not in self.possible_values:
            raise Exception("Invalid card value")

        face_card_to_value = {
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        try:
            self.numerical_value = int(value)
        except:
            self.numerical_value = face_card_to_value[value]
        return value

    def get_symbol(self):
        suit = self.suit
        if suit is None:
            if self.key is not None:
                suit = dict([
                    (string.upper(s[0]), s)
                    for s in self.possible_suits
                ])[string.upper(self.key[-1])]
            else:
                suit = random.choice(self.possible_suits)
        if suit not in self.possible_suits:
            raise Exception("Invalud suit value")
        self.suit = suit
        symbol_height = float(self.height) / self.card_height_to_symbol_height
        symbol = SuitSymbol(suit, height=symbol_height)
        return symbol

    def get_design(self, value, symbol):
        if value == "A":
            return self.get_ace_design(symbol)
        if value in list(map(str, list(range(2, 11)))):
            return self.get_number_design(value, symbol)
        else:
            return self.get_face_card_design(value, symbol)

    def get_ace_design(self, symbol):
        design = symbol.copy().scale(1.5)
        design.move_to(self)
        return design

    def get_number_design(self, value, symbol):
        num = int(value)
        n_rows = {
            2: 2,
            3: 3,
            4: 2,
            5: 2,
            6: 3,
            7: 3,
            8: 3,
            9: 4,
            10: 4,
        }[num]
        n_cols = 1 if num in [2, 3] else 2
        insertion_indices = {
            5: [0],
            7: [0],
            8: [0, 1],
            9: [1],
            10: [0, 2],
        }.get(num, [])

        top = self.get_top() + symbol.get_height() * DOWN
        bottom = self.get_bottom() + symbol.get_height() * UP
        column_points = [
            interpolate(top, bottom, alpha)
            for alpha in np.linspace(0, 1, n_rows)
        ]

        design = VGroup(*[
            symbol.copy().move_to(point)
            for point in column_points
        ])
        if n_cols == 2:
            space = 0.2 * self.get_width()
            column_copy = design.copy().shift(space * RIGHT)
            design.shift(space * LEFT)
            design.add(*column_copy)
        design.add(*[
            symbol.copy().move_to(
                center_of_mass(column_points[i:i + 2])
            )
            for i in insertion_indices
        ])
        for symbol in design:
            if symbol.get_center()[1] < self.get_center()[1]:
                symbol.rotate_in_place(np.pi)
        return design

    def get_face_card_design(self, value, symbol):
        from for_3b1b_videos.pi_creature import PiCreature
        sub_rect = Rectangle(
            stroke_color=BLACK,
            fill_opacity=0,
            height=0.9 * self.get_height(),
            width=0.6 * self.get_width(),
        )
        sub_rect.move_to(self)

        # pi_color = average_color(symbol.get_color(), GREY)
        pi_color = symbol.get_color()
        pi_mode = {
            "J": "plain",
            "Q": "thinking",
            "K": "hooray"
        }[value]
        pi_creature = PiCreature(
            mode=pi_mode,
            color=pi_color,
        )
        pi_creature.set_width(0.8 * sub_rect.get_width())
        if value in ["Q", "K"]:
            prefix = "king" if value == "K" else "queen"
            crown = SVGMobject(file_name=prefix + "_crown")
            crown.set_stroke(width=0)
            crown.set_fill(YELLOW, 1)
            crown.stretch_to_fit_width(0.5 * sub_rect.get_width())
            crown.stretch_to_fit_height(0.17 * sub_rect.get_height())
            crown.move_to(pi_creature.eyes.get_center(), DOWN)
            pi_creature.add_to_back(crown)
            to_top_buff = 0
        else:
            to_top_buff = SMALL_BUFF * sub_rect.get_height()
        pi_creature.next_to(sub_rect.get_top(), DOWN, to_top_buff)
        # pi_creature.shift(0.05*sub_rect.get_width()*RIGHT)

        pi_copy = pi_creature.copy()
        pi_copy.rotate(np.pi, about_point=sub_rect.get_center())

        return VGroup(sub_rect, pi_creature, pi_copy)

    def get_corner_numbers(self, value, symbol):
        value_mob = TextMobject(value)
        width = self.get_width() / self.card_width_to_corner_num_width
        height = self.get_height() / self.card_height_to_corner_num_height
        value_mob.set_width(width)
        value_mob.stretch_to_fit_height(height)
        value_mob.next_to(
            self.get_corner(UP + LEFT), DOWN + RIGHT,
            buff=MED_LARGE_BUFF * width
        )
        value_mob.set_color(symbol.get_color())
        corner_symbol = symbol.copy()
        corner_symbol.set_width(width)
        corner_symbol.next_to(
            value_mob, DOWN,
            buff=MED_SMALL_BUFF * width
        )
        corner_group = VGroup(value_mob, corner_symbol)
        opposite_corner_group = corner_group.copy()
        opposite_corner_group.rotate(
            np.pi, about_point=self.get_center()
        )

        return VGroup(corner_group, opposite_corner_group)


class SuitSymbol(SVGMobject):
    CONFIG = {
        "height": 0.5,
        "fill_opacity": 1,
        "stroke_width": 0,
        "red": "#D02028",
        "black": BLACK,
    }

    def __init__(self, suit_name, **kwargs):
        digest_config(self, kwargs)
        suits_to_colors = {
            "hearts": self.red,
            "diamonds": self.red,
            "spades": self.black,
            "clubs": self.black,
        }
        if suit_name not in suits_to_colors:
            raise Exception("Invalid suit name")
        SVGMobject.__init__(self, file_name=suit_name, **kwargs)

        color = suits_to_colors[suit_name]
        self.set_stroke(width=0)
        self.set_fill(color, 1)
        self.set_height(self.height)


class Like(SVGMobject):
    CONFIG = {
        "color": "#fb7199"
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        SVGMobject.__init__(self, file_name="good", **kwargs)


class Coin(SVGMobject):
    CONFIG = {
        "color": "#03b5e5"
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        SVGMobject.__init__(self, file_name="coin", **kwargs)


class Favo(SVGMobject):
    CONFIG = {
        "color": "#f3a034"
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        SVGMobject.__init__(self, file_name="favo", **kwargs)


class BranchCut(VGroup):
    CONFIG = {
        "color": YELLOW,
        "num": 20,
        "angle": np.pi,
        "factor": .2
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        triag = VGroup(Line(DR, ORIGIN), Line(ORIGIN, DL))
        triag = VGroup(*[triag.copy() for _ in range(self.num)]).arrange(buff=0) \
            .scale(self.factor).next_to(ORIGIN, RIGHT, buff=0).set_color(self.color).rotate(self.angle, about_point=ORIGIN)
        VGroup.__init__(self, triag)


# 下面的仅仅是将它封装成类，或许可以便于操作
# 将数字的显示改成使用Integer，以避免生成过多的TextSVG
# widcardw

# 显示所有锚点的索引
class AllPointsIndex(VGroup):
    CONFIG = {
        "scale_factor": 0.5,
        "color": PURPLE,
    }

    def __init__(self, obj, **kwargs):
        # digest_config(self, kwargs)
        VGroup.__init__(self, **kwargs)
        for index, points in enumerate(obj.get_all_points()):
            point_id = Integer(index, background_stroke_width=2) \
                .scale(self.scale_factor).set_color(self.color)
            point_id.move_to(points)
            self.add(point_id)


# 显示单个vmobject的索引
class PointIndex(VGroup):
    CONFIG = {
        "scale_factor": 0.5,
        "color": PURPLE,
    }

    def __init__(self, obj, **kwargs):
        # digest_config(self, kwargs)
        VGroup.__init__(self, **kwargs)
        for index, points in enumerate(obj.get_points()):
            point_id = Integer(index, background_stroke_width=2) \
                .scale(self.scale_factor).set_color(self.color)
            point_id.move_to(points)
            self.add(point_id)


class TexIndex(VGroup):
    CONFIG = {
        "scale_factor": 0.5,
        "color": PURPLE,
    }

    def __init__(self, obj, **kwargs):
        VGroup.__init__(self, **kwargs)
        for index, single_tex in enumerate(obj):
            tex_index = Integer(index, background_stroke_width=2) \
                .scale(self.scale_factor).set_color(self.color)
            tex_index.move_to(single_tex.get_center())
            self.add(tex_index)


class CheckFormulaByTXT(Scene):
    CONFIG = {
        "camera_config": {"background_color": BLACK},
        "svg_type": "text",
        "text": Tex(""),
        "file": "",
        "svg_scale": 0.9,
        "angle": 0,
        "flip_svg": False,
        "fill_opacity": 1,
        "remove": [],
        "stroke_color": WHITE,
        "fill_color": WHITE,
        "stroke_width": 3,
        "numbers_scale": 0.5,
        "show_numbers": True,
        "animation": False,
        "direction_numbers": UP,
        "color_numbers": RED,
        "space_between_numbers": 0,
        "show_elements": [],
        "color_element": BLUE,
        "set_size": "width",
        "remove_stroke": [],
        "show_stroke": [],
        "warning_color": RED,
        "stroke_": 1
    }

    def construct(self):
        self.imagen = self.text
        self.imagen.set_width(FRAME_WIDTH)
        if self.imagen.get_height() > FRAME_HEIGHT:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.flip_svg == True:
            self.imagen.flip()
        if self.show_numbers == True:
            self.print_formula(self.imagen.copy(),
                               self.numbers_scale,
                               self.direction_numbers,
                               self.remove,
                               self.space_between_numbers,
                               self.color_numbers)

        self.return_elements(self.imagen.copy(), self.show_elements)
        for st in self.remove_stroke:
            self.imagen[st].set_stroke(None, 0)
        for st in self.show_stroke:
            self.imagen[st].set_stroke(None, self.stroke_)
        if self.animation == True:
            self.play(DrawBorderThenFill(self.imagen))
        else:
            c = 0
            for j in range(len(self.imagen)):
                permission_print = True
                for w in self.remove:
                    if j == w:
                        permission_print = False
                if permission_print:
                    self.add(self.imagen[j])
            c = c + 1
        self.personalize_image()
        self.wait()

    def personalize_image(self):
        pass

    def print_formula(self, text, inverse_scale, direction, exception, buff, color):
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print = True
            for w in exception:
                if j == w:
                    permission_print = False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c = 0
        for j in range(len(text)):
            permission_print = True
            element = TexMobject("%d" % c, color=color)
            element.scale(inverse_scale)
            element.next_to(text[j], direction, buff=buff)
            for w in exception:
                if j == w:
                    permission_print = False
            if permission_print:
                self.add_foreground_mobjects(element)
            c = c + 1

    def return_elements(self, formula, adds):
        for i in adds:
            self.add_foreground_mobjects(formula[i].set_color(self.color_element),
                                         TexMobject("%d" % i, color=self.color_element,
                                                    background_stroke_width=0).scale(self.numbers_scale).next_to(
                                             formula[i], self.direction_numbers, buff=self.space_between_numbers))


class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = TextMobject(f"{coord_point}", font="Arial", stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)
