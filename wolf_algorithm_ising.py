import numpy as np
from numpy.random.mtrand import rand
from matplotlib import pyplot as plt
from matplotlib import animation
from numba import njit
from matplotlib.widgets import Slider
import sys


sys.setrecursionlimit(100000)
@njit
def cord(a, b):
    return L * a + b
@njit
def recursiveFindGeitones(a, b, L, latt, cluster, beta):
    s = latt[a, b]  # brisko ti einai to simio a,b

    panoGeitonas = latt[(a - 1) % L, b]
    panoGeitonasCord = cord((a - 1) % L, b)
    katoGeitonas = latt[(a + 1) % L, b]
    katoGeitonasCord = cord((a + 1) % L, b)
    deksiaGeiotons = latt[a, (b + 1) % L]
    deksiaGeiotonsCord = cord(a, (b + 1) % L)
    aristeraGeitonas = latt[a, (b - 1) % L]
    aristeraGeitonasCord = cord(a, (b - 1) % L)

    listofneighbors = [panoGeitonas, katoGeitonas, deksiaGeiotons, aristeraGeitonas]
    listofneighborsCords = [panoGeitonasCord, katoGeitonasCord, deksiaGeiotonsCord, aristeraGeitonasCord]

    i = 0
    for neighbor in listofneighbors:
        if neighbor == s and listofneighborsCords[i] not in cluster and rand() < 1 - np.exp(-float(beta) * 2):

            if i == 0:
                cluster.add(listofneighborsCords[i])

                recursiveFindGeitones((a - 1) % L, b, L, latt, cluster, beta)
            elif i == 1:

                cluster.add(listofneighborsCords[i])
                recursiveFindGeitones((a + 1) % L, b, L, latt, cluster, beta)
            elif i == 2:

                cluster.add(listofneighborsCords[i])
                recursiveFindGeitones(a, (b + 1) % L, L, latt, cluster, beta)
            else:

                cluster.add(listofneighborsCords[i])
                recursiveFindGeitones(a, (b - 1) % L, L, latt, cluster, beta)

        i += 1
    return

@njit
def wolff(n,beta,latt1):
    lst =[]
    for i in range(0, n):
        lst.append(i+1)

    a = np.random.randint(0, L)
    b = np.random.randint(0, L)
    s = latt1[a, b]
    p = cord(a,b)
    cluster = set()
    cluster.add(p)
    recursiveFindGeitones(a, b, L, latt1, cluster, beta)

    lst.remove(s)

    rngNumber = lst[np.random.randint(0,n-1)]
    for point in cluster:
        pointA = point // L
        pointB = point % L
        latt1[pointA, pointB] = rngNumber
    return latt1


L=int(input('give me the number of sites L:'))

shape = (L, L)
list_of_spin_orientations = []
#q = int(input("Enter number of elements for potts : "))

for i in range(0, 2):
    elements = int(input("Give orientation : "))
    list_of_spin_orientations.append(elements)

latt = np.random.choice(list_of_spin_orientations, size=shape)

