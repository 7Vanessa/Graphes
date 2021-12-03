import copy

import numpy as np
import pandas as pd
import math
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# demande à l'utilisateur si oui ou non il souhaite analyser un nouveau graphe
def nouvelleAnalyse(root, presence):
    if presence:
        res = messagebox.askquestion("Présence d'un circuit absorbant", "Souhaitez-vous analyser un nouveau graphe ?", icon='question')
    else:
        res = messagebox.askquestion("Fin de l'algorithme", "Souhaitez-vous analyser un nouveau graphe ?", icon='question')
    if res == 'yes':
        root.destroy()
    elif res == 'no':
        exit()
    else:
        print("ok")

# pour chaque sommet, en fonction des arêtes entrantes, on constitue 2 listes :
#     * l'une avec des valeurs binaires : présence(1) ou non(0) d'arêtes entrantes
#     * l'autre avec des nombres entiers naturels : nombre d'arêtes entrantes
# a partir de ces listes on construit 2 dictionnaires qui contiendront les colonnes des 2 matrices (la matrice d'adjacence binaire et la matrice de valeurs)
def listeAretesEntrantes(graphe, aretes):
    databin = {}
    dataval = {}

    # x est un sommet
    for x in range(int(graphe[0])):
        listematricebin = np.zeros(int(graphe[0]))

        # s'il n'y a pas d'arête qui lie les sommets : inf dans la matrice de valeurs
        listematriceval = math.inf + np.zeros(int(graphe[0]))

        for i in range(len(aretes)):
            if aretes[i][1] == x:
                listematricebin[aretes[i][0]] = 1
                listematriceval[aretes[i][0]] = aretes[i][2]
            if((aretes[i][1] == x) and (aretes[i][0] == x)) == False:
                listematriceval[x] = 0

        # on stock ces listes (valeur), et leur sommet correspondant (indice) dans 2 dictionnaires
        databin[x] = listematricebin
        dataval[x] = listematriceval
    return databin, dataval

# detection de circuit absorbant dans le graphe
def circuitAbsorbant(matrice):
    for i in range(len(matrice)):
        if matrice[i][i] < 0:
            return True
    return False

# a partir des dictionnaires précédemment établis on peut construire nos matrices sous forme de DataFrames
# on utilise l'index pour retrouver les sommets à partir desquels les arêtes sortent
def calculmatrices(graphe, aretes):
    index = np.arange(int(graphe[0]))
    matricebin = pd.DataFrame(listeAretesEntrantes(graphe, aretes)[0], index)
    matriceval = pd.DataFrame(listeAretesEntrantes(graphe, aretes)[1], index)
    return matricebin, matriceval

def chemin(root, P, depart, arrivee) :
    listChemin = []
    listChemin.append(arrivee)
    predCourant = int(P[arrivee][depart])
    listChemin.append(predCourant)

    while(predCourant != depart) :
        predCourant = int(P[predCourant][depart])
        listChemin.append(predCourant)


    cheminReversed = []
    for i in range(len(listChemin)):
        cheminReversed.append(listChemin.pop())

    label_chemin = Label(root, text=str(cheminReversed), font=("Courrier", 30),
                         bg='#ffeeee', fg='black',
                         justify=RIGHT)
    label_chemin.pack()

    return cheminReversed

# on applique l'algorithme de Floyd Warshall
def floydWarshall(root, graphe, frame_trace):

    # creation d'une liste contenant toutes les aretes du graphe
    aretes = []
    for i in range(2, len(graphe), 3):
        aretes.append((int(graphe[i]), int(graphe[i + 1]), int(graphe[i + 2])))
    # affichage console
    print(aretes)

    # initialisation matrice L
    L = calculmatrices(graphe, aretes)[1]
    listesP = []

    # initialisation matrice P
    for x in range(int(graphe[0])):
        l = x * np.ones(int(graphe[0]))
        listesP.append(l)
    P = pd.DataFrame((listesP))

    # initialisation de la matrice d'adjacence
    A = calculmatrices(graphe, aretes)[0]

    # variable booleene de detection de circuit absorbant
    circuit_absorbant = False

    # affichage console
    print("Deroulement de l'algorithme : ")
    print("La matrice d'adjacence binaire du graphe est: \n", calculmatrices(graphe, aretes)[0], "\n")
    print("La matrice de valeurs du graphe est: \n", calculmatrices(graphe, aretes)[1], "\n")

    # initialisation de l'affichage des matrices d'adjacence et de valeurs
    adj = ttk.Treeview(frame_trace)
    vals = ttk.Treeview(frame_trace)

    # ajout d'une case vide a l'indice 0 pour que les indices des lignes ne se retouvent pas dans la colonne d'indice 0
    listeSommets = [" "]

    # on recupere la liste contenant les indices (sommets du graphe)
    for i in range(int(graphe[0])):
        listeSommets.append(str(i))

    # on convertit les colonnes en ligne pour pouvoir l'utiliser dans 'insert'
    adjTrans = A.transpose()
    valsTrans = L.transpose()

    # on convertit en tuple car 'insert' ne prend que des tuples
    adj["columns"] = tuple(listeSommets)
    vals["columns"] = tuple(listeSommets)

    # configuration du Treeview
    adj.column("#0", width=0, stretch=NO)
    adj.heading("#0", text="", anchor=CENTER)
    vals.column("#0", width=0, stretch=NO)
    vals.heading("#0", text="", anchor=CENTER)

    # creation des colonnes avec leur entete
    for i in range(len(listeSommets)):
        adj.column(str(listeSommets[i]), anchor=CENTER, width=50)
        adj.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)
        vals.column(str(listeSommets[i]), anchor=CENTER, width=50)
        vals.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)

    # insertion de chaque ligne de la matrice
    # conversion d'une ligne de type 'Series' en 'List' pour pouvoir y inserer l'indice de chaque ligne de la matrice
    for i in range(len(listeSommets) - 1):
        rowL = adjTrans[i].values.tolist()
        rowL.insert(0, i)
        adj.insert(parent='', index='end', text='',
                       values=tuple(rowL))
        rowA = valsTrans[i].values.tolist()
        rowA.insert(0, i)
        vals.insert(parent='', index='end', text='',
                       values=tuple(rowA))

    # affichage du label de la matrice d'adjacence
    label_adj = Label(frame_trace, text="La matrice d'adjacence binaire du graphe est: \n", font=("Courrier", 15),
                      bg='#ffeeee', fg='black',
                      justify=LEFT)
    label_adj.pack()

    # affichage de la matrice d'adjacence
    adj.pack()

    # affichage du label de la matrice de valeurs
    label_vals = Label(frame_trace, text="La matrice de valeurs du graphe est: \n", font=("Courrier", 15),
                           bg='#ffeeee', fg='black',
                           justify=LEFT)
    label_vals.pack()

    # affichage de la matrice de valeurs
    vals.pack()

    # pour chaque sommet k...
    for k in range(int(graphe[0])):
        # ... on vérifie si jusqu'à un sommet i...
        for i in range(int(graphe[0])):
            for j in range(int(graphe[0])):
                # le chemin courant à partir d'un sommet j en passant par k juste avant i est plus court que le chemin courant de j à i dans le tableau
                # si c'est le cas, on met le coût de ce chemin dans la matrice L
                # et k devient le prédecesseur de i dans P, soit la matrice des prédecesseurs dans les plus courts chemins connus jusqu'à l'itération k
                if L[k][i] + L[j][k] < L[j][i]:
                    L[j][i] = L[k][i] + L[j][k]
                    P[j][i] = P[j][k]
                # Detection de circuit absorbant, si oui mettre fin à l'algo et demander nouvelle analyse
                if circuitAbsorbant(L):
                    circuit_absorbant = True
                    L[j][i] = L[k][i] + L[j][k]
                    P[j][i] = P[j][k]

        # affichage du numero d'iteration
        iteration = "k = " + str(k)
        label_iteration = Label(frame_trace, text=iteration, font=("Courrier", 15), bg='#ffeeee', fg='black',
                             justify=LEFT)
        label_iteration.pack()

        # affichage des matrices L et P avec un tableau 'Treeview' pcq c + bo
        my_tabL = ttk.Treeview(frame_trace)
        my_tabP = ttk.Treeview(frame_trace)

        # on a convertit les colonnes en ligne pour pouvoir l'utiliser dans 'insert'
        Ltrans = L.transpose()
        Ptrans = P.transpose()

        # ajout d'une case vide a l'indice 0 pour que les indices des lignes ne se retouvent pas dans la colonne d'indice 0
        listeSommets = [" "]

        # on recupere la liste contenant les indices (sommets du graphe)
        for i in range(int(graphe[0])):
            listeSommets.append(str(i))

        # on convertit en tuple car 'insert' ne prend que des tuples
        my_tabL["columns"] = tuple(listeSommets)
        my_tabP["columns"] = tuple(listeSommets)

        # configuration du Treeview
        my_tabL.column("#0", width=0, stretch=NO)
        my_tabL.heading("#0", text="", anchor=CENTER)
        my_tabP.column("#0", width=0, stretch=NO)
        my_tabP.heading("#0", text="", anchor=CENTER)

        # creation des colonnes avec leur entete
        for i in range(len(listeSommets)):
            my_tabL.column(str(listeSommets[i]), anchor=CENTER, width=50)
            my_tabL.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)
            my_tabP.column(str(listeSommets[i]), anchor=CENTER, width=50)
            my_tabP.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)

        # insertion de chaque ligne de la matrice
        # conversion d'une ligne de type 'Series' en 'List' pour pouvoir y inserer l'indice de chaque ligne de la matrice
        for i in range(len(listeSommets)-1):
            rowL = Ltrans[i].values.tolist()
            rowL.insert(0, i)
            my_tabL.insert(parent='', index='end', text='',
                           values=tuple(rowL))
            rowP = Ptrans[i].values.tolist()
            rowP.insert(0, i)
            my_tabP.insert(parent='', index='end', text='',
                           values=tuple(rowP))

        # affichage du label L
        label_L = Label(frame_trace, text="L = ", font=("Courrier", 15), bg='#ffeeee', fg='black',
                        justify=LEFT)
        label_L.pack()

        # affichage de L
        my_tabL.pack()

        # affichage du label P
        label_P = Label(frame_trace, text="P = ", font=("Courrier", 15), bg='#ffeeee', fg='black',
                        justify=LEFT)
        label_P.pack()

        # affichage de P
        my_tabP.pack()

        # affichage console
        print("\nk = ", k)
        print(L)
        print("\n", P)

        # affichage d'un circuit absorbant
        if(circuit_absorbant) :
            print("Présence d'un circuit absorbant")

    if(not circuit_absorbant) :
        label_depart = Label(frame_trace, text="Sommet de depart ? \n", font=("Courrier", 15),
                            bg='#ffeeee', fg='black',
                                 justify=LEFT)
        label_depart.pack()

        depart = Entry(frame_trace, relief='raised', font=("Courrier", 20), justify="center")
        depart.pack()

        label_arrivee = Label(frame_trace, text="Sommet d'arrivee ? \n", font=("Courrier", 15),
                                bg='#ffeeee', fg='black',
                                justify=LEFT)
        label_arrivee.pack()

        arrivee = Entry(frame_trace, relief='raised', font=("Courrier", 20), justify="center")
        arrivee.pack()

        button = Button(frame_trace, text="VALIDER", font=("Courrier", 20), bg='white', fg='grey',
                                   command=lambda: chemin(root, P, int(depart.get()), int(arrivee.get())))
        button.pack()

    else :
        label_circuit_abs = Label(root, text="PRESENCE D'UN CIRCUIT ABSORBANT !", font=("Courrier", 30),
                                  bg='#ffeeee', fg='red')
        label_circuit_abs.pack()
    nouvelleAnalyse(root, circuit_absorbant)

    return circuit_absorbant