import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.style.use('ggplot')

x = np.linspace(0, 10, 500)

x = 2.5478 * x

plt.plot(x, np.sin(x))
plt.show()
