# from manimlib import *

import numpy as np
import matplotlib.pyplot as plt

f = lambda x,y: x**2+y**2

x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)
x, y = np.meshgrid(x, y)
z = f(x, y)

# plt.figure(dpi=200)
c = plt.contour(x, y, z, 10)
cmap = c.get_cmap()
print(z)
plt.colorbar()
plt.savefig('contour.png', dpi=200)

