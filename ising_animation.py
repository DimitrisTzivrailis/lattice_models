import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy.random.mtrand import rand
from matplotlib.widgets import Slider
import sys
sys.setrecursionlimit(100000)


def metropolis(latt, beta):
    for i in range(L):
        for j in range(L):
            a = np.random.randint(0, L)
            b = np.random.randint(0, L)
            s = latt[a, b]
            neighbours = (latt[(a - 1) % L, b] + latt[(a + 1) % L, b] + latt[a, (b + 1) % L] + latt[a, (b - 1) % L])
            denerg = 2 * s * neighbours

            if denerg <= 0:
                s *= -1
            elif rand() < np.exp(-beta * denerg):
                s *= -1
            latt[a, b] = s

    return latt

def update_quiver(val):
    T = s_T.val
    beta = 1 / T
    p = metropolis(latt1, beta)
    #p = wolff(n,latt1,beta)
    l = np.arcsin(p)
    U = np.cos(l)
    V = np.sin(l)
    M = np.cos(l) + np.sin(l)
    Q.set_UVC(U, V, M)

    return Q
L = int(input('give me the number of sites:'))
#beta = float(input('give me the beta factor:'))
#n = int(input('give number of spin orientations'))
latt1 = np.random.choice([-1,1], (L, L))
latt2 = np.arcsin(latt1)
X, Y = np.meshgrid(np.arange(0, L), np.arange(0, L))
U = np.cos(latt2)
V = np.sin(latt2)
M = np.cos(latt2) + np.sin(latt2)

fig, ax = plt.subplots(1, 1)
Q = ax.quiver(X, Y, U, V, M, pivot='mid', units='inches', scale_units='xy',cmap = 'viridis')

ax_T = fig.add_axes([0.3, 0.92, 0.4, 0.05])
s_T = Slider(ax=ax_T, label='Temperature ', valmin=0.001, valmax=4, valinit=100, valfmt='%0.1f K', facecolor='#cc7000')
s_T.on_changed(update_quiver)

anim = animation.FuncAnimation(fig, update_quiver, interval=16, blit=False)
#fig.tight_layout()
plt.show()
