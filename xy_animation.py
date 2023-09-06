import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy.random.mtrand import rand
import math
from numba import njit
from matplotlib.widgets import Slider



@njit
def Energy(latt,s,i,j):
    energ = -(math.cos(latt[(i-1)%L, j] - s)+ math.cos(latt[(i+1)%L, j]-s) + math.cos(latt[i, (j+1)%L]-s )+math.cos( latt[i, (j-1)%L]-s))
    return energ
@njit
def metropolis(latt, beta):
  for i in range(L**2):
    a = np.random.randint(0, L)
    b = np.random.randint(0, L)
    s = latt[a, b]
    s_new = latt[a, b]+np.random.uniform(-np.pi,np.pi)
    denerg= Energy(latt,s_new,a,b)-Energy(latt,s,a,b)

    if denerg <= 0:
        s = s_new
    elif np.random.uniform(0.0 , 1.0) < np.exp(-beta*denerg):
        s = s_new
    latt[a, b] = s
  return latt

def update_quiver(val):
    T = s_T.val
    beta = 1/T

    k = metropolis(latt1, beta)

    U = np.cos(k)
    V = np.sin(k)
    M = np.cos(k) + np.sin(k)

    Q.set_UVC(U, V, M)
    time.set_text(str(val))
    return Q
L=int(input('give me the number of sites L:'))
#beta =float(input('give the beta factor:'))

latt1 = np.random.random([L,L])*2*np.pi - np.pi*np.ones([L,L])

X, Y = np.meshgrid(np.arange(0, L), np.arange(0, L))
U = np.cos(latt1)
V = np.sin(latt1)
M = np.cos(latt1) + np.sin(latt1)
fig, ax = plt.subplots(1, 1)

axtext = fig.add_axes([0.0,0.95,0.1,0.05])
axtext.axis("off")
time = axtext.text(0.5,0.5, str(0), ha="left", va="top")

ax_T = fig.add_axes([0.3, 0.92, 0.4, 0.05])
Q = ax.quiver(X, Y, U, V, M, pivot='tail', units='inches', scale_units='xy', cmap='viridis')
s_T = Slider(ax=ax_T, label='Temperature ', valmin=0.001, valmax=2, valinit=100, valfmt='%0.1f K', facecolor='#cc7000')
s_T.on_changed(update_quiver)
anim = animation.FuncAnimation(fig, update_quiver,  interval=16, blit=False)
#fig.tight_layout()

plt.show()