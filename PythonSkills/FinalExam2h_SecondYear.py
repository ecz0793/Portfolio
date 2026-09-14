#CC2
#Etienne
#CROZETIERE
#21304820
#G1B
#21/05/2025

import numpy as np
import matplotlib.pyplot as plt

#%% Exercice 1

folder = "C:/Users/croze/OneDrive/Bureau/CC2/"
tab_N5 = np.load(folder +"CC2_N5.npy")
tab_N28 = np.load(folder +"CC2_N28.npy")
tab_zoom = np.load(folder  +"CC2_zoom.npy")

plt.figure(1,figsize=(10,4)) 
plt.subplot(1,3,1)
plt.imshow(tab_N5,cmap='gray')
plt.subplot(1,3,2)
plt.imshow(tab_N28,cmap='gray')
plt.subplot(1,3,3)
plt.imshow(tab_zoom,cmap='gray')
plt.show()

#%%Question 2

L_25=tab_N5[25,:]
L_75=tab_N5[75,:]
L_125=tab_N5[125,:]

plt.figure(2) 
plt.subplot(2,1,1)
plt.imshow(tab_N5,cmap='gray')
plt.plot([0,150],[25,25],'-r')
plt.plot([0,150],[75,75],'-r')
plt.plot([0,150],[125,125],'-r')
plt.title('5 disques')
plt.xlabel('Pixels')
plt.ylabel('Pixels')

plt.subplot(2,1,2)
x = np.linspace(0,150,150)
x2 = np.linspace(150,300,150)
x3 = np.linspace(300,450,150)

plt.plot(x,L_25,'-k')
plt.plot(x2,L_75,'-k')
plt.plot(x3,L_125,'-k')
plt.plot([150,150],[0,1],'--r')
plt.plot([300,300],[0,1],'--r')

print(tab_N5)
#%% Question 3

a =  np.sum(abs(np.diff(L_25)))
b =  np.sum(abs(np.diff(L_75)))
c =  np.sum(abs(np.diff(L_125)))

print("Le nombre de fibres comptées par cette méthode est",int(np.ceil(int(a+b+c)/2)))

#%% Question 4

L28_25=tab_N28[25,:]
L28_75=tab_N28[75,:]
L28_125=tab_N28[125,:]

plt.figure(3) 
plt.subplot(2,1,1)
plt.imshow(tab_N28,cmap='gray')
plt.plot([0,150],[25,25],'-r')
plt.plot([0,150],[75,75],'-r')
plt.plot([0,150],[125,125],'-r')
plt.title('5 disques')
plt.xlabel('Pixels')
plt.ylabel('Pixels')

plt.subplot(2,1,2)
x = np.linspace(0,150,150)
x2 = np.linspace(150,300,150)
x3 = np.linspace(300,450,150)

plt.plot(x,L28_25,'-k')
plt.plot(x2,L28_75,'-k')
plt.plot(x3,L28_125,'-k')
plt.plot([150,150],[0,1],'--r')
plt.plot([300,300],[0,1],'--r')

a2 =  np.sum(abs(np.diff(L28_25)))
b2 =  np.sum(abs(np.diff(L28_75)))
c2 =  np.sum(abs(np.diff(L28_125)))
print(np.diff(L28_25))
print("Le nombre de fibres comptées par cette méthode est",int(np.ceil(int(a2+b2+c2)/2)))

#%% Exercice 2 Q1

def oscillateur_CN(tmax, N, w=2*np.pi, ui=1., vi=0.):
    """ En entrée : tmax correspond au temps total, N a un pas de temps que l'on fixe, w
    la pulsation fixé, ui condition initiale de position, vi condition initiale de vitesse  
    
    En sortie : tvec le temps discrétisé, U la solution de l'équation du mouvement
    
    """       

    dt = tmax/N # pas de temps
    tvec = np.linspace(0,tmax,N+1) # N pas donc N+1 points 0 ... N

    A = np.array([[0, 1],
                  [-w**2, 0]]);
    I = np.eye(2)

    R = np.linalg.inv(2*I - dt*A)  @ (2*I + dt*A) # Calcule R une fois pour toutes
                                                  # puisque w et A sont constants

    # Initialisation : crée un tableau de 2 lignes et N+1 colonnes (une colonne par temps discret)
    U = np.zeros((2,N+1))
    U[0,0] = ui  # Initialise la première colonne avec les conditions initiales
    U[1,0] = vi

    # Schéma numérique 
    n = 0
    while n < N :
        U[:,n+1] = np.dot(R,U[:,n])
        n = n+1    

    return tvec, U

# Test de la fonction
w = 2*np.pi
tmax = 5
N = 50
tvec, U =  oscillateur_CN(tmax,N)
tvec
uvec_CN = U[0,:] # extrait la première ligne de U càd les valeurs approchées un

#%% Ex 2 q2

u = np.cos(w*tvec)

plt.figure(4)

N = 50
plt.subplot(1,2,1)
plt.plot(tvec,u,'-r',label='Solution exacte')
plt.plot(tvec,uvec_CN,'--k',label='Solution approchée')
plt.legend()
plt.xlabel('Temps tvec')
plt.ylabel('Fonction U')

plt.subplot(1,2,2)

en = abs(u-uvec_CN)
plt.plot(tvec , en)
plt.title('Erreur absolue')

#%%

def erreur_tot_CN(tmax,N):
    tvec, U =  oscillateur_CN(tmax,N)
    uvec_CN = U[0,:]
    u = np.cos(w*tvec)
    en = abs(u-uvec_CN)
    En = np.sum(en)/np.sum(abs(u))     
    return En

erreur_tot_CN(5,10)
erreur_tot_CN(5,100)

#%%

Nvec = np.array([20,50,100,200,500,1000])

F = []
E = []
for i in range(len(Nvec)):
    En = erreur_tot_CN(5,Nvec[i])
    Fn = En/erreur_tot_CN(5,100)
    print('Fn pour',Nvec[i],' est ',Fn)
    F.append(Fn)
    E.append(En)

N2 = np.linspace(0,Nvec,len(Nvec))
plt.figure(5)
plt.subplot(1,2,1)
plt.plot(F,N2,'--ok')
plt.title('Echelle linéaire')
plt.subplot(1,2,2)
plt.loglog(F,N2,'--ok')
plt.title('Echelle LogLog')

#%%
p = 1
Fnt = (100/N2)**p

plt.figure(6)
plt.loglog(N2,E,'--ob',label='Erreur')
plt.plot(N2,Fnt,'-r',label='Fn théorique')
plt.plot(N2,(100/N2)**5,'-r',label='p = 5')
plt.plot(N2,(100/N2)**20,'-r',label='p = 20')
plt.legend()
plt.grid()

#%%

def EMC_CN(p):
    N = np.array([20,50,100,200,500,1000])
    for i in range(len(N)):
        En = erreur_tot_CN(5,N[i])
        Fn = En/erreur_tot_CN(5,100)
        emc = np.sqrt(np.sum((Fn-(100/N)**p)**2))
    return emc
print(EMC_CN(1),EMC_CN(5),EMC_CN(10)) 

#%%
p0 = 20
pm = np.linspace(0.8*p0,1.2*p0,41)

plt.figure(7)
EM = []
for j in range(41):
    EM.append(EMC_CN(pm[j]))

plt.loglog(pm,EM)



