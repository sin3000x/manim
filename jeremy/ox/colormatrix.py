from manimlib import *

import matplotlib.pyplot as plt
import matplotlib.cm as cm

f = lambda x,y: x**2+y**2

x = np.linspace(-1,1,10)
y = np.linspace(-1,1,10)
x, y = np.meshgrid(x, y)
z = f(x, y)

c = plt.contour(x, y, z, 20)

CMAP = cm.jet(np.linspace(0, 1, 10))

rgbas = cm.jet(np.linspace(0, 1, 10))

colors = [rgba_to_color(i) for i in rgbas]

class ColorMatrix(Scene):
    def construct(self):
        mat = Matrix(
            z, 
            element_to_mobject=lambda i: Tex("%.2f" % i), 
            h_buff=1.1, 
            v_buff=1.1,
            bracket_h_buff=0.2,
            bracket_v_buff=0.25,
            ).set_color(BLACK).scale(.7)
        color_array = (z/1.8).flatten().astype(object)
        cmap = dict(zip(np.linspace(0.1,1.9, 19).round(1), colors))
        cmap.update({1.1: rgba_to_color(cm.jet(1.0)), 0.0: rgba_to_color(cm.jet(0.0))})
        for i in range(len(color_array)):
            # print(round(color_array[i], 1))
            color_array[i] = cmap.get(round(color_array[i], 1), WHITE)
        # color_array = color_array.reshape(z.shape)
        for ele, color in zip(mat.get_entries(), color_array):
            ele.set_color(color)

        self.add(mat)
        self.wait()