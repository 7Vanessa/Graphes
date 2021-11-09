# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 01:19:13 2021

@author: thush
"""

import numpy as np
import pandas as pd
import math



##  ETAPE 1 : LECTURE / COPIE DU TEXTE

# On part du principe que l'ensemble des graphes seront nommés de la façon suivante : graphe1, graphe2,...

# Objectif :
# demander le numero du graph et l'entrer dans la variable num de type string
# num = str(input)
# graph = "graphe" + num +".txt"

# pour l'instant : 
graph = "graphe1.txt"

text = open(graph, "r")
s = text.read()
text.close()

s = s.split( )
#print(s)

#on crée une liste contenant toutes les arêtes
aretes = []
for i in range (2,len(s),3) :
    aretes.append((int(s[i]),int(s[i+1]),int(s[i+2])))
#print(aretes)





### ETAPE 2 : REPRESENTATION DE LA MATRICE 

#on part du principe que le fichier texte respecte la structure de l'énoncé


"""
def calculmatrices (s) : 
    databin = {}
    dataval = {}
    for x in range(int(s[0])):
        #print(x)
        listematricebin = np.zeros(int(s[0]))
        listematriceval = math.inf + np.zeros(int(s[0]))
        #s'il n'y a pas d'arête qui lie les sommets : inf dans la matrice de valeurs
        for i in range (len (aretes)):
            if aretes[i][1]==x : 
                listematricebin[aretes[i][0]]= 1
                listematriceval[aretes[i][0]]=aretes[i][2]
        databin[x] = listematricebin
        dataval[x]= listematriceval

    index = []
    for x in range (int(s[0])):
        index.append(x)

    matricebin = pd.DataFrame(databin,index)
    matriceval = pd.DataFrame(dataval,index)
    print( "La matrice d'adjacence binaire du graphe est: \n", matricebin, "\n")
    print( "La matrice de valeurs du graphe est: \n", matriceval, "\n")
    return matricebin, matriceval
"""
#print(calculmatrices(s)[0])

#--------------------------------

def listeAretesEntrantes (s) : 
    databin = {}
    dataval = {}
    for x in range(int(s[0])):
        #print(x)
        listematricebin = np.zeros(int(s[0]))
        listematriceval = math.inf + np.zeros(int(s[0]))
        #s'il n'y a pas d'arête qui lie les sommets : inf dans la matrice de valeurs
        for i in range (len (aretes)):
            if aretes[i][1]==x : 
                listematricebin[aretes[i][0]]= 1
                listematriceval[aretes[i][0]]=aretes[i][2]
        databin[x] = listematricebin
        dataval[x]= listematriceval
    return databin, dataval

def calculmatrices (s) : 
    index = np.arange(int(s[0]))
    matricebin = pd.DataFrame(listeAretesEntrantes(s)[0],index)
    matriceval = pd.DataFrame(listeAretesEntrantes(s)[1], index)
    return matricebin, matriceval

print( "La matrice d'adjacence binaire du graphe est: \n", calculmatrices(s)[0], "\n")
print( "La matrice de valeurs du graphe est: \n", calculmatrices(s)[1], "\n")
    




### ETAPE 3 : ALGORITHME DE FLOYD WARSHALL

#on suppose que l'on n'a pas besoin d'afficher les sommets dans L et P
def algoFloydWarshall (s) : 
    #print(listeAretesEntrantes(s)[1])
    L = []
    for x in listeAretesEntrantes(s)[1] :
        L.append(listeAretesEntrantes(s)[1][x])
    

print(algoFloydWarshall(s))