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
graph = "graphe2.txt"

text = open(graph, "r")
s = text.read()
text.close()

s = s.split( )
#print(s)

#on crée une liste contenant toutes les arêtes
aretes = []
for i in range (2,len(s),3) :
    aretes.append((int(s[i]),int(s[i+1]),int(s[i+2])))
print(aretes)






### ETAPE 2 : REPRESENTATION DE LA MATRICE 

#on part du principe que le fichier texte respecte la structure de l'énoncé


def listeAretesEntrantes (s) : 
    databin = {}
    dataval = {}
    # x = un sommet
    for x in range(int(s[0])):
        #print(x)
        listematricebin = np.zeros(int(s[0]))
        listematriceval = math.inf + np.zeros(int(s[0]))
        #s'il n'y a pas d'arête qui lie les sommets : inf dans la matrice de valeurs
        for i in range (len (aretes)):
            if aretes[i][1]==x : 
                listematricebin[aretes[i][0]]= 1
                listematriceval[aretes[i][0]]=aretes[i][2]
            if ((aretes[i][1]==x) and (aretes[i][0] == x))==False:
                listematriceval[x]= 0
        #print (x)
        #print(listematriceval)
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
    
#print(calculmatrices(s))






## ETAPE 3 : EXECUTION DE L'ALGORITHME DE FLOYD WARSHALL

def algoFloydWarshall (s) : 
    
    #initialisation
    L = calculmatrices(s)[1]
    #L = pd.DataFrame((listesAretesEntrantes))
    #print("\n", L)
    listesP = []
    for x in range (int(s[0])): 
        l = x * np.ones(int(s[0]))
        listesP.append(l)
    P = pd.DataFrame((listesP))
     #print("\n", P)
    
    #itérations
    for k in range (int(s[0])) : 
        for i in range (int(s[0])) :
            for j in range (int(s[0])) :
                if L[k][i] + L[j][k] < L[j][i] : 
                    L[j][i] = L[k][i] + L[j][k]
                    P[j][i] = P[j][k]
        print("\nk = ",k)
        print(L)
        print("\n", P)

print(algoFloydWarshall(s)) 




## ETAPE 4 : CIRCUIT ABSORBANT ?

"""circuit absorbant si dans le dernier L : présence de nb négatifs dans la diagonale"""

