"""
author: kang.liu and jiabin.chen
date: 29/06/2017
Projet MAP311:  Determination du plus court chemin
Contact: jiabin.chen@polytechnique.edu

"""
import random
import math
from matplotlib import pyplot as plt
from matplotlib import animation
import copy

#classe de ville
class Ville(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __init__(self):
        self.x = random.uniform(-10, 10)
        a = math.sqrt(100-self.x**2)
        if random.randint(0,1) == 0:
            self.y = a
        else:
            self.y = -a

    def getVille(self):
        return (self.x, self.y)

    def distance(self, other):
        d = math.sqrt((self.y - other.y)**2+(self.x-other.x)**2)
        return d

#classe d'une liste des villes
class ListeVille(object):

    def __init__(self, unelistevilles):
        self.listevilles = unelistevilles

    def echangeAleatoire(self):
        i = random.randint(0, N-1)
        j = random.randint(0, N-1)
        autrelistevilles = copy.deepcopy(self.listevilles)
        tmp = autrelistevilles[i]
        autrelistevilles[i] = autrelistevilles[j]
        autrelistevilles[j] = tmp
        nouveaulisteville = ListeVille(autrelistevilles)
        return nouveaulisteville

    def echangeComplexe(self):
        i = random.randint(0, N-1)
        j = random.randint(0, N-1)
        if i==j :
            autrelistevilles = copy.deepcopy(self.listevilles)
            nouveaulisteville = ListeVille(autrelistevilles)
            return nouveaulisteville
        if i<j:
            min = i
            max = j
        else:
            min = j
            max = i
        autrelistevilles = copy.deepcopy(self.listevilles)
        for i in range(((max-min)/2)+1):
            tmp = autrelistevilles[min+i]
            autrelistevilles[min+i] = autrelistevilles[max-i]
            autrelistevilles[max-i] = tmp
        nouveaulisteville = ListeVille(autrelistevilles)
        return nouveaulisteville

    def calculDistanceTotale(self):
        i=0
        totale = 0
        while i<N-1:
            totale= totale+ dictVille[self.listevilles[i]].distance(dictVille[self.listevilles[i+1]])
            i=i+1
        totale = totale + dictVille[self.listevilles[0]].distance(dictVille[self.listevilles[-1]])
        return totale


# main function
def renouvelerLaTabListeVille(tableauDeListeVille, tableauDeDistance,  n):
    s0 = tableauDeListeVille[n-1] # s0 est une liste initiale des villes
    s1 = s0.echangeAleatoire()  # on fait une permutation aleatoire
    u = random.uniform(0,1)
    d0 =s0.calculDistanceTotale()
    d1 =s1.calculDistanceTotale()
    critere = d0- d1 - (1.0/(n+1))*math.log(u,math.e)
    if critere >= 0:
        tableauDeListeVille.append(s1) # on ajoute cette nouvelle liste des villes a la fin de tableau
        tableauDeDistance.append(d1)  # on ajoute cette nouvelle distance a la fin de tableau
    else:
        tableauDeListeVille.append(s0)
        tableauDeDistance.append(d0)

def renouvelerLaTabListeVilleComplex(tableauDeListeVille, tableauDeDistance, n):
        s0 = tableauDeListeVille[n - 1]  # s0 est une liste initiale des villes
        s1 = s0.echangeComplexe()  # on fait une permutation aleatoire
        u = random.uniform(0, 1)
        d0 = s0.calculDistanceTotale()
        d1 = s1.calculDistanceTotale()
        critere = d0 - d1 - (1.0 / (math.log(n,math.e) + 1)) * math.log(u, math.e)
        if critere >= 0:
            tableauDeListeVille.append(s1)  # on ajoute cette nouvelle liste des villes a la fin de tableau
            tableauDeDistance.append(d1)  # on ajoute cette nouvelle distance a la fin de tableau
        else:
            tableauDeListeVille.append(s0)
            tableauDeDistance.append(d0)


# on met un chiffre ici qui represente le nombre de ville
N=40
# on met le nombre de l'iteration
NombreDeIteration = 10000

# On cree un dictionnaire pour stoker tous les villes et construire une application bijective
# entre ces villes et chiffre entiers entre 0 et N-1
def creerDictVille():
    dictVille = {}
    j = 0;
    while j < N :
        unville = Ville()
        dictVille[j] = unville
        j = j+1
    return dictVille

# Ici on cree tous les villes par hazard, du coup il va creer chaque fois N villes aleatoires lorsque on demarre cette
# fonction. Si vous voulez etudier le cas que les N villes sont fixes, il faut utiliser l'autre constructeur de classe
# Ville qui est fournie dedans mais par contre vous devez enregistrer tous les points des villes
dictVille = creerDictVille()

# On initiale le premier parcours par un tableau de entiers entre
# 0 et N-1 qui represente N villes
unliste=[]
for i in range(N):
    unliste.append(i)

# On cree un objet de type ListeVille
premierList = ListeVille(unliste)

# On ajoute le premier element(parcours) dans une liste ou on va ajouter au fur et a mesure des nouvelles parcours.
tableauDeListeVille = [premierList]

# On ajoute aussi le premier distance du premier parcours et puis on va ajouter au fur et a mesure tous les distances
# de chaque parcours que l'on ajoute dans la tableauDeListeVille
tableauDeDistance = [premierList.calculDistanceTotale()]

# On demarre ici la processus d'iteration pour obtenir le plus court chemin
for i in range(1,NombreDeIteration+1):
    renouvelerLaTabListeVilleComplex(tableauDeListeVille, tableauDeDistance, i)

# A partir ici, on montre l'animation sur l'ecran
fig1 = plt.figure("figure1")
abscisse = []
for i in range(1, len(tableauDeDistance)+1):
    abscisse.append(i)
plt.scatter(abscisse, tableauDeDistance)
# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure("figure2")
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    unePermutation = tableauDeListeVille[i].listevilles
    x = []
    y = []
    for j in range(N):
        x.append(dictVille[unePermutation[j]].x)
        y.append(dictVille[unePermutation[j]].y)
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=NombreDeIteration, interval=500, repeat_delay= 1000000, blit=True)

plt.show()