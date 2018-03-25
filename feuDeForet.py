# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 08:42:53 2016

@author: 3520287
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation


x=int(input("taille de la foret ? "))
d=int(input("densité forestière ? "))

def init(d,x):
    foret = np.zeros([x,x])
    for i in range (1,x-1):
        for j in range (1,x-1):
            if(random.random() < d ):
                foret[i,j]=1
            if foret[i,j]==1:
                continue      
    n = random.randint(1,x-2)
    m = random.randint(1,x-2)    
    foret[n,m]=2
    return foret


#definition des regles d'iteration
def iteration (foret):
    foret2=np.copy(foret)
    for k in range (1,foret2.shape[0]-1):
        for l in range(1,foret2.shape[1]-1):
            if (foret[k,l]==1) and ((foret[k+1,l]==2) or (foret [k-1,l]==2) or (foret[k,l-1]==2) or (foret[k,l+1]==2)):
                foret2[k,l]=2
            if foret[k,l]==2:
                foret2[k,l]=3
    return foret2

def comptage(foret):
    nb_brules=0
    while 2 in foret :
        foret=iteration(foret)
    for i in range (1,foret.shape[0]-1):
        for j in range (1,foret.shape[1]-1):
            if foret[i,j]==3:
               nb_brules=nb_brules+1
    return nb_brules 


def repetition(d,size,n):
    i=0
    resultats_vecteurs = np.zeros([n])
    while i<n:
        foret = init(d,size)
      
        resultats_vecteurs[i] = comptage(foret)
       
        i = i + 1
    
    m=np.average(resultats_vecteurs)
    v=np.var(resultats_vecteurs)
    ec=math.sqrt(v) 
    print(d)
    print(m)
    return(v,m) 

    

#x=np.linspace(0,1,10)
#y=[repetition(d,100,5)[1] for d in x]
#plt.plot(x,y,'ro')
#plt.show()

foret=init(d, x)

cmap = colors.ListedColormap(['black','green','orange','gray'])
                      
import matplotlib.pyplot as plt
size = np.array(foret.shape)
dpi = 72
figsize= size[1]/float(dpi),size[0]/float(dpi)
fig = plt.figure(figsize = (100,100), dpi = dpi, facecolor = "white")
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
im=plt.imshow(foret, interpolation = 'nearest', cmap=cmap,vmin=0,vmax=3)
plt.xticks([]), plt.yticks([])

def update(*args):
   global foret
   foret = iteration(foret)
   im.set_array(foret)
   return im,

ani = animation.FuncAnimation(fig, update, frames=range(20), interval=500)
plt.show()



        
