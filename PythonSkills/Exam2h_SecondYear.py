#LU2ME103-CC1
#CROZETIERE
#Etienne
#21304820
#G1B
#08/04/2025

import numpy as np
import matplotlib.pyplot as plt
#%%

#Mis en Jambe

#1
N = 20
s = 0
a = 0
for i in range(1,N,2):
    s += i
    a +=1
    print('S_'+str(a)+' = '+str(s))
    
#2

v1 = np.arange(11,60,2)
M = np.reshape(v1,(5,5))
v = np.transpose(M)
w = v[0,:]
print(v)
print(w)
print(M)

#3

x = np.linspace(-np.pi,np.pi,100)
plt.figure(1)
plt.plot(x,np.sin(x),'-k')
plt.grid()
plt.xlabel('Abcsisse x')
plt.ylabel('Ordonnée y = sin(x)')
plt.xlim(-4,4)
plt.ylim(-1.5,1.5)
plt.show()

#%%

#Paramètres physiques
m = 0.1 # en kg
R = 0.1 # en m
g = 9.81 # en m/s²
theta = np.linspace(10,30,3)
print(theta)
t = np.linspace(0,2,201)

#%%
# Valeur de x
x = g*((t**2)/2)*np.sin(theta[0]*np.pi/180)
# Valeur de la dérivée de x
x_d= g*t*np.sin(theta[0]*np.pi/180)


plt.figure(20,figsize=(8,4))
plt.subplot(1,2,1) # Graphique de la position
plt.plot(t,x,'-k',label='theta = 10 degrés')
plt.xlabel('Temps t[s]')
plt.ylabel('Position x[m]')
plt.legend()
plt.title('Position')
plt.grid()
plt.ylim(0.0,3.5)

plt.subplot(1,2,2)# Graphique de la vitesse
plt.plot(t,x_d,'-k',label='theta = 10 degrés')
plt.grid()
plt.xlabel('Temps t[s]')
plt.ylabel('Vitesse v [m/s]')
plt.title('Vitesse')

plt.tight_layout()
plt.legend()
plt.show()

#%%
#3

#Tableaux permettant de stockr les valeurs de x et x_d
tab_x = []
tab_x_d = []
for i in range(len(theta)):
    tab_x.append(g*((t**2)/2)*np.sin(theta[i]*np.pi/180))
    tab_x_d.append(g*t*np.sin(theta[i]*np.pi/180))

styles = ['-k','-b','-r']

plt.figure(30,figsize=(8,4))

plt.subplot(1,2,1)
for i in range(len(theta)):
    plt.plot(t,tab_x[i],styles[i],label='Theta ='+str(int(theta[i]))+' degrés')
    plt.grid()
    plt.ylim(0.0,3.5)
    plt.legend()
    plt.title('Position')
    plt.xlabel('Temps t[s]')
    plt.ylabel('Position x[m]')


plt.subplot(1,2,2)
for i in range(len(theta)):
    plt.plot(t,tab_x_d[i],styles[i],label='Theta ='+str(int(theta[i]))+' degrés')
    plt.grid()
    plt.ylim(0.0,3.5)
    plt.legend()
    plt.title('Vitesse')
    plt.xlabel('Temps t[s]')
    plt.ylabel('Vitesse v [m/s]')

plt.show()
plt.tight_layout()

#%%

#4

alpha = (np.pi/2) - ((g*t**2)/2*R)*np.sin(theta[0])
xC = tab_x[i]*np.cos(theta[0])
yC = -tab_x[i]*np.sin(theta[0])
xA = xC + R*np.cos(alpha)
yA = yC + R*np.sin(alpha)

plt.plot(xA,yA,'-k',label='xA, yA')
plt.plot(xC,yC,'-r',label='xC, yC')
plt.grid()
plt.xlabel('valeur de x')
plt.ylabel('valeur de y')
plt.title('Trajectoires')
plt.legend()
plt.show()


#%%

#5

# Dans 3 graphiques différents

plt.figure(40,figsize=(12,5))
for i in range(len(theta)):
    plt.subplot(1,3,i+1)
    alpha = (np.pi/2) - ((g*t**2)/2*R)*np.sin(theta[i])
    xC = tab_x[i]*np.cos(theta[i])
    yC = -tab_x[i]*np.sin(theta[i])
    xA = xC + R*np.cos(alpha)
    yA = yC + R*np.sin(alpha)
    plt.plot(xA,yA,'-k',label='xA, yA pour'+str(int(theta[i]))+' degrés')
    plt.plot(xC,yC,'-r',label='xC, yC pour'+str(int(theta[i]))+' degrés')
    plt.xlabel('valeur de x')
    if i == 0:
        plt.ylabel('valeur de y')
    plt.title('Trajectoires')
    plt.grid()
    plt.legend()

plt.show()

#%%

# Dans un unique graphique 
stylesA = ['-k','-b','-g']
stylesC= ['--k','--b','--g']
plt.figure(40,figsize=(12,5))
for i in range(len(theta)):

     alpha = (np.pi/2) - ((g*t**2)/2*R)*np.sin(theta[i])
     xC = tab_x[i]*np.cos(theta[i])
     yC = -tab_x[i]*np.sin(theta[i])
     xA = xC + R*np.cos(alpha)
     yA = yC + R*np.sin(alpha)
     plt.plot(xA,yA,stylesA[i],label='xA, yA pour'+str(int(theta[i]))+' degrés')
     plt.plot(xC,yC,stylesC[i],label='xC, yC pour'+str(int(theta[i]))+' degrés')
     plt.xlabel('valeur de x')
     if i == 0:
         plt.ylabel('valeur de y')
     plt.title('Trajectoires')
     plt.grid()
     plt.legend()
plt.show()
#%%
#Exercice 4

#Debug

import numpy as np
import matplotlib.pyplot as plt # 1 ajout de .pyplot

# Figure principale (taille imposée (12,4))
plt.figure(30,figsize=(12,4)) # 2 figure pas fig

# Fonction tangente et DL
eps = 0.01 # Petit écart pour éviter de calculer tan(+-pi/2) = +-inf
x = np.linspace((-np.pi/2)+eps,(np.pi/2)-eps,201) # 4 on utilise la biblio numpy donc np.pi pas juste pi
y = np.tan(x)
DL1_1 = x
DL1_2 = x + x**3/3
DL1_3 = x + x**3/3 + 2*(x**5)/15 # 3 ajout de * entre 2 et x

plt.subplot(1,3,1)               
plt.plot(x,y,"-k")
plt.xlim(-np.pi/2,np.pi/2)
plt.xlabel("Abscisse x")
plt.ylim(-50,50) # 6 ylim pas xlim
plt.ylabel("tan(x)") 
plt.grid()                       
plt.title("Fonction tangente")                

plt.subplot(1,3,2)               
plt.plot(x,y,"-k",label="tan(x)")
plt.plot(x,DL1_1,'--k',label="ordre 1") #5 DL1_1 pas DL1
plt.plot(x,DL1_2,"--b",label="ordre 3") #5 DL2_1 pas DL2        
plt.plot(x,DL1_3,"--r",label="ordre 5") #5 DL3_1 pas DL3           
plt.xlim(-np.pi/2,np.pi/2)
plt.xlabel("Abscisse x")       
plt.ylim(-5,5)
plt.ylabel("tan(x) et ses DL") 
plt.grid()
plt.legend() #7 ajout de légende                    
plt.title("Zoom : Tangente et ses DL")       

# Fonction arctangente et DL
x3 = np.linspace(-5,5,201) # 9 on remplace le arange par un linspace
y3 = np.arctan(x3) # 8 on remplace x par x3
DL2_1 = x3
DL2_2 = x3 - x3**3/3
DL2_3 = x3 - x3**3/3 + x3**5/5

plt.subplot(1,3,3)               
plt.plot(x3,y3,"-k",label="arctan(x)")
plt.plot(x3,DL2_1,'--k',label="ordre 1")
plt.plot(x3,DL2_2,"--b",label="ordre 3")            
plt.plot(x3,DL2_3,"--r",label="ordre 5")
          
plt.xlim(-5,5) # 10 Les limites sont -5; 5 pas -50; 50
plt.xlabel("Abscisse x")       
plt.ylim(-np.pi/2,np.pi/2)
plt.ylabel("arctan(x) et ses DL") 
plt.grid()    
plt.legend()#7 ajout de légende                   
plt.title("Zoom : Arctangente et ses DL")      


plt.tight_layout()
plt.show()
#%%

#Amélioration du code

#A Variables intermédiaires
xmin = -np.pi/2
xmax = np.pi/2
ymin = -50
ymax = 50
Nx = 201

 # Figure principale (taille imposée (12,4))
plt.figure(30,figsize=(12,4)) # 2 figure pas fig

# Fonction tangente et DL
eps = 0.01 # Petit écart pour éviter de calculer tan(+-pi/2) = +-inf
x = np.linspace((-np.pi/2)+eps,(np.pi/2)-eps,Nx) # 4 on utilise la biblio numpy donc np.pi pas juste pi
y = np.tan(x)

#B 2 tableaux DL1 et DL2
DL1 = np.zeros((3,Nx))

DL1[0,:] = x
DL1[1,:] = x + x**3/3
DL1[2,:] = x + x**3/3 + 2*(x**5)/15 # 3 ajout de * entre 2 et x

x3 = np.linspace(-5,5,Nx) # 9 on remplace le arange par un linspace
y3 = np.arctan(x3) # 8 on remplace x par x3

DL2 = np.zeros((3,Nx))
DL2[0,:] = x3
DL2[1,:] = x3 - x3**3/3
DL2[2,:] = x3 - x3**3/3 + x3**5/5

plt.subplot(1,3,1)               
plt.plot(x,y,"-k")
plt.xlim(xmin,xmax)
plt.xlabel("Abscisse x")
plt.ylim(ymin,ymax) # 6 ylim pas xlim
plt.ylabel("tan(x)") 
plt.grid()                       
plt.title("Fonction tangente")   

styles = ["--k","--b","--r"] 

#C Boucle pour tracer les 3 DL
plt.subplot(1,3,2)
for i in range(len(DL1)):
    plt.plot(x,DL1[i], styles[i],label='ordre '+str(i+1))          
            
plt.plot(x,y,"-k",label="tan(x)")       
plt.xlim(xmin,xmax)
plt.xlabel("Abscisse x")       
plt.ylim(ymin/10,ymax/10)
plt.ylabel("tan(x) et ses DL") 
plt.grid()
plt.legend() #7 ajout de légende                    
plt.title("Zoom : Tangente et ses DL")       


plt.subplot(1,3,3)               
plt.plot(x3,y3,"-k",label="arctan(x)")

ordre = [1,3,5]

#C Boucle pour tracer les 3 DL
for i in range(len(DL2)):
    plt.plot(x3,DL2[i],styles[i],label='ordre '+str(ordre[i]))
          
plt.xlim(ymin/10,ymax/10) # 10 Les limites sont -5; 5 pas -50; 50
plt.xlabel("Abscisse x")       
plt.ylim(xmin,xmax)
plt.ylabel("arctan(x) et ses DL") 
plt.grid()
plt.legend() #7 ajout de légende               
plt.title("Zoom : Arctangente et ses DL")      

plt.tight_layout()
plt.show()
#%%

#D Bonus
plt.figure(30,figsize=(12,4)) # 2 figure pas fig

ordre = [1,3,5]
styles = ["--k","--b","--r"] 

# Amélioration Bonus Ajout d'une boucle pour afficher les 3 graphiques
for j in range(len(DL1)):
    plt.subplot(1,3,j+1)
    if j == 0:
        plt.plot(x,y,'-k')
        plt.xlim(xmin,xmax)
        plt.xlabel("Abscisse x")
        plt.ylim(ymin,ymax) # 6 ylim pas xlim
        plt.ylabel("tan(x)") 
        plt.grid()                       
        plt.title("Fonction tangente")  
    elif j == 1:
        plt.plot(x,y,'-k',label='tan(x)')
        for i in range(len(DL1)):
            plt.plot(x,DL1[i], styles[i],label='ordre '+str(i+1))

        plt.xlim(xmin,xmax)
        plt.xlabel("Abscisse x")       
        plt.ylim(ymin/10,ymax/10)
        plt.ylabel("tan(x) et ses DL") 
        plt.grid()
        plt.legend() #7 ajout de légende                    
        plt.title("Zoom : Tangente et ses DL")       
    elif j == 2:
        plt.plot(x3,y3,"-k",label="arctan(x)")
        for i in range(len(DL2)):
            plt.plot(x3,DL2[i],styles[i],label='ordre '+str(ordre[i]))
        plt.xlim(ymin/10,ymax/10) # 10 Les limites sont -5; 5 pas -50; 50
        plt.xlabel("Abscisse x")       
        plt.ylim(xmin,xmax)
        plt.ylabel("arctan(x) et ses DL") 
        plt.grid()
        plt.legend() #7 ajout de légende               
        plt.title("Zoom : Arctangente et ses DL")  
   

plt.tight_layout()
plt.show()
#%%
#3

x = 0.9
N = 40
n = np.arange(0,41)

An = np.cumsum(((-1)**n) * (x**(2*n+1))/(2*n+1))
err = (abs(np.arctan(x)-An))/(abs(np.arctan(x)))


plt.figure(50)
plt.semilogy(n,err,':b',label='erreur An pour x = 0.9')
plt.xlabel('Nombre de terme N')
plt.ylabel('Erreur relative de An')
plt.legend()
plt.grid()
plt.title('Erreur en fonction du nombre de terme')

plt.show()
#%%
#4
err_1 = 0.01
N = 40
An = 0

x = 0.9

for n in range(0,N+1):
    An += (((-1)**n) * (x**(2*n+1))/(2*n+1))

    if ((abs(np.arctan(x)-An))/(abs(np.arctan(x)))) < err_1:
        print("L'erreur relative est inférieur à 1% pour N = ", n)
        break

#%%

#5
x = 1
N = 40
n = np.arange(0,41)

An = np.cumsum(((-1)**n) * (x**(2*n+1))/(2*n+1))
err = (abs(np.arctan(x)-An))/(abs(np.arctan(x)))

err2 = (abs(np.arctan(0.9)-np.cumsum(((-1)**n) * (0.9**(2*n+1))/(2*n+1))))/(abs(np.arctan(0.9)))

plt.figure(50)
plt.semilogy(n,err,'xr',label='erreur An pour x = 1')
plt.semilogy(n,err2,':b',label='erreur An pour x = 0.9')
plt.xlabel('Nombre de terme N')
plt.ylabel('Erreur relative de An')
plt.grid()
plt.title('Erreur en fonction du nombre de terme')

# Valeur pour lesquelles l'erreur relative est inférieur à 1%

plt.plot(n[err<0.01],err[err<0.01],'ok',label='Valeur < 1%')
plt.plot(n[err2<0.01],err2[err2<0.01],'ok',)
plt.legend()

An = 0
for n in range(0,N+1):
    An += (((-1)**n) * (x**(2*n+1))/(2*n+1))

    if ((abs(np.arctan(x)-An))/(abs(np.arctan(x)))) < err_1:
        print("L'erreur relative est inférieur à 1% pour N = ", n)
        break



plt.show()
