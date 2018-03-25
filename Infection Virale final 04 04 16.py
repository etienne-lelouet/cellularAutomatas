import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
#import math

#Variables du programme
#size=int(input("Taille de la matrice : "))
#c=int(input("Nombre de cellules : "))
#nbStepInput =int(input("Duree d'incubation d'un virus : "))
#nbStep=nbStepInput+2
#nb_lympho=int(input("Nombre de lymphocytes : "))
#trigger=int(input("Nombre de cellules detruties pour declencher l'arrivee des lymphocytes : "))
size=30
c=35
nbStep=7
nb_lympho=120
trigger=50

nbDetruits=0
nbVirusDetruits=0
#Initialisation
def init(size,c):
    infection = np.zeros([size,size])
    x=random.randint(0,size-1)
    y=random.randint(0,size-1)
    infection[x,y] = 2      
    i=0    
    while i<c :
        j=random.randint(0,size-1)
        k=random.randint(0,size-1)
        if infection[j,k]!=0:
            continue  
        else :
            i=i+1
            infection[j,k]=1
    return infection

#Initialisation de la matrice des lymphocytes           
def init_lympho(size,nb_lympho):
    lymphocyte=np.zeros([size,size])
    i=0
    while i<nb_lympho:
        x=random.randint(0,size-1)
        y=random.randint(0,size-1)
        if infection[x,y]!=0:
            continue
        else:
            lymphocyte[x,y]=1
            i=i+1
    return lymphocyte
    
infection = init(size,c)
lymphocyte = init_lympho(size,nb_lympho)

#print(infection)

#print(infection.shape)

#Propagation du virus
def iteration (infection,lymphocyte):     
    x = infection.shape[0]
    infection2=np.copy(infection)
    global nbDetruits
    for i in range (0,x):
        for j in range(0,x):
            
            if(infection2[i,j]==2):
                r=random.randint(0,3)
                if(r==0) and infection2[(i-1)%x,j]==0:
                    infection2[(i-1)%x,j] = 2 
                    infection2[i,j] = 0
               
                    
                if(r==1) and infection2[i,(j+1)%x] ==0:
                    infection2[i,(j+1)%x] = 2 
                    infection2[i,j] = 0
                
                if(r==2) and infection2[(i+1)%x,j] ==0:
                    infection2[(i+1)%x,j] = 2 
                    infection2[i,j] = 0
                
                    
                if(r==3) and infection2[i,(j-1)%x] ==0 :
                    infection2[i,(j-1)%x] = 2 
                    infection2[i,j] = 0
                    
            if (infection2[i,j] == 1) and ((infection2[(i-1)%x,j]==2) or (infection2[(i+1)%x,j]==2) or (infection2[i,(j-1)%x]==2) or (infection2[i,(j+1)%x]==2)):
                infection2[i,j]=nbStep
                nbDetruits=nbDetruits+1
                if infection2[(i-1)%x,j]==2:
                    infection2[(i-1)%x,j]=nbStep 
                elif infection2[(i+1)%x,j]==2:
                    infection2[(i+1)%x,j]=nbStep
                elif infection2[i,(j-1)%x]==2:
                    infection2[i,(j-1)%x]=nbStep                   
                elif infection2[i,(j+1)%x]==2:
                    infection2[i,(j+1)%x]=nbStep
                    
            if infection2[i,j] in range (3,nbStep+1):
                infection2[i,j]=infection2[i,j]-1
            
    if nbDetruits>trigger:
        lymphocyte,infection2= iteration_lympho(lymphocyte, infection2)    
    return infection2,lymphocyte

#Propagation des lymphocytes
def iteration_lympho(lymphocyte,infection):
    global nbVirusDetruits
    
    lymphocyte2=np.copy(lymphocyte)
    size = infection.shape[0]

    #On teste si un lymphocyte est a proximite d'une cellule infectee ou d'un virus
    #Quand un lymphocyte est sur une cellule contaminee ou un virus, la cellule est detruite
    #Sinon,le virus se deplace aleatoirement
    for i in range (0,size):
        for j in range (0,size):
            if lymphocyte[i,j]==1 :
                if infection[i,j] in range (2,nbStep+1):
                    infection[i,j]=0
                    nbVirusDetruits=nbVirusDetruits+1
                else :
                    hasMoved = False 
                    
                    for m in range(-2,3):
                        for n in range (-2,3):
                            if hasMoved == False:
                                if (infection[(i+m)%size,(j+n)%size] in range (2,nbStep+1)) and (infection[(i+m)%size,(j+n)%size]!=1) :
                                    x=max(min(m,1),-1)
                                    y=max(min(n,1),-1)
                                    lymphocyte2[i,j]=0
                                    lymphocyte2[(i+x)%size,(j+y)%size]=1
                                    hasMoved = True
                                else:
                                    hasMoved=False
                               
                    if hasMoved == False:
                        r=random.randint(0,3)
                        if(r==0) and lymphocyte[(i-1)%size,j]==0:
                            lymphocyte2[(i-1)%size,j] = 1 
                            lymphocyte2[i,j] = 0
                        if(r==1) and lymphocyte[i,(j+1)%size] ==0:
                            lymphocyte2[i,(j+1)%size] = 1 
                            lymphocyte2[i,j] = 0    
                        if(r==2) and lymphocyte[(i+1)%size,j] ==0:
                            lymphocyte2[(i+1)%size,j] = 1 
                            lymphocyte2[i,j] = 0                
                        if(r==3) and lymphocyte[i,(j-1)%size] ==0 :
                            lymphocyte2[i,(j-1)%size] = 1 
                            lymphocyte2[i,j] = 0
                                    
    return lymphocyte2,infection


#Affichage matrice
def fusion(infection, lymphocyte):
    global nbDetruits
    size = infection.shape[0]
    affichage = np.copy(infection)
    for i in range(0,size):
        for j in range (0,size):
            if lymphocyte[i,j]==1 and nbDetruits>trigger:
                  affichage[i,j]= 4
            if infection[i,j] > 3:
                  affichage[i,j]= 3
    return affichage

affichageMatrice = fusion(infection,lymphocyte)


cmap = colors.ListedColormap(['white','red','purple','blue','yellow'])
size = np.array(affichageMatrice.shape)
dpi = 72
figsize= size[1]/float(dpi),size[0]/float(dpi)
fig = plt.figure(figsize = (100,100), dpi = dpi, facecolor = "white")
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
im=plt.imshow(affichageMatrice, interpolation = 'nearest', cmap=cmap,vmin=0,vmax=4)
plt.xticks([]), plt.yticks([])

def update(*args):
   global infection
   global lymphocyte
   
   infection,lymphocyte = iteration(infection,lymphocyte)
   
   
   
  
   affichageMatrice = fusion(infection,lymphocyte) 
   
   im.set_array(affichageMatrice)
   return im,

ani = animation.FuncAnimation(fig, update, frames=range(20), interval=500)
plt.show()




#def simulation(nbPas):
#   global infection
#   global lymphocyte
#   global nbDetruits
#   global nbVirusDetruits
#   for i in range (0,nbPas):
#      infection,lymphocyte = iteration(infection,lymphocyte)
#   return (nbDetruits,nbVirusDetruits)
#
#
#def repetition(n,nbPas):    
#    i=0
#    resultats_cellules = np.empty([n])
#    resultats_lymphos = np.empty([n])
#    while i<n:
#        x,y=simulation(1000)
#        resultats_cellules[i] = x
#        resultats_lymphos[i] = y
#        i = i + 1    
#    mc=int(np.average(resultats_cellules))
#    print("nombre moyen de cellules détruites sur", n, "répétitions = ",mc)
##    vc=int(np.var(resultats_cellules))
##    ecc=int(math.sqrt(vc))
#    mv=int(np.average(resultats_lymphos))
#    print("nombre moyen de virus détruits sur", n, "répétitions = ",mv)
##    vv=int(np.var(resultats_lymphhos))
##    ecv=int(math.sqrt(vv))
#    return()
#print(repetition(5,3000))
