import numpy as np
import pandas as pd
import math
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Demande à l'utilisateur si oui ou non il souhaite analyser un nouveau graphe
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


def listeAretesEntrantes(graphe, aretes):
    databin = {}
    dataval = {}
    # x = un sommet
    for x in range(int(graphe[0])):
        # print(x)
        listematricebin = np.zeros(int(graphe[0]))
        listematriceval = math.inf + np.zeros(int(graphe[0]))
        # s'il n'y a pas d'arête qui lie les sommets : inf dans la matrice de valeurs
        for i in range(len(aretes)):
            if aretes[i][1] == x:
                listematricebin[aretes[i][0]] = 1
                listematriceval[aretes[i][0]] = aretes[i][2]
            if((aretes[i][1] == x) and (aretes[i][0] == x)) == False:
                listematriceval[x] = 0
        # print (x)
        # print(listematriceval)
        databin[x] = listematricebin
        dataval[x] = listematriceval
    return databin, dataval

# Detection de circuit absorbant dans le graphe
def circuitAbsorbant(matrice):
    for i in range(len(matrice)):
        if matrice[i][i] < 0:
            return True;
    return False;


def calculmatrices(graphe, aretes):
    index = np.arange(int(graphe[0]))
    matricebin = pd.DataFrame(listeAretesEntrantes(graphe, aretes)[0], index)
    matriceval = pd.DataFrame(listeAretesEntrantes(graphe, aretes)[1], index)
    return matricebin, matriceval


# print(calculmatrices(s))


def floydWarshall(graphe, root, canvas, frame_trace):

    # Creation d'une liste contenant toutes les aretes du graphe
    aretes = []
    for i in range(2, len(graphe), 3):
        aretes.append((int(graphe[i]), int(graphe[i + 1]), int(graphe[i + 2])))
    print(aretes)

    print("La matrice d'adjacence binaire du graphe est: \n", calculmatrices(graphe, aretes)[0], "\n")
    print("La matrice de valeurs du graphe est: \n", calculmatrices(graphe, aretes)[1], "\n")

    # initialisation
    L = calculmatrices(graphe, aretes)[1]
    # L = pd.DataFrame((listesAretesEntrantes))
    # print("\n", L)
    listesP = []
    for x in range(int(graphe[0])):
        l = x * np.ones(int(graphe[0]))
        listesP.append(l)
    P = pd.DataFrame((listesP))
    # print("\n", P)

    decalage = 0

    circuit_absorbant = False

    # itérations
    print("Deroulement de l'algorithme : ")
    for k in range(int(graphe[0])):
        for i in range(int(graphe[0])):
            for j in range(int(graphe[0])):
                if L[k][i] + L[j][k] < L[j][i]:
                    L[j][i] = L[k][i] + L[j][k]
                    P[j][i] = P[j][k]
                # Detection de circuit absorbant, si oui mettre fin à l'algo et demander nouvelle analyse
                if circuitAbsorbant(L):
                    circuit_absorbant = True
                    print("Présence d'un circuit absorbant")
                    nouvelleAnalyse(root, circuit_absorbant)

        print("\nk = ", k)
        print(L)
        print("\n", P)
        #for i in range(len(L)):
        #    for j in range(len(L[i])):
        #        print("\"", str(L[i][j]), "\"")
        #        print(type(str(L[i][j])))

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
        for i in range(int(graphe[0])) :
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
        for i in range(len(listeSommets)) :
            my_tabL.column(str(listeSommets[i]), anchor=CENTER, width=50)
            my_tabL.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)
            my_tabP.column(str(listeSommets[i]), anchor=CENTER, width=50)
            my_tabP.heading(str(listeSommets[i]), text=str(listeSommets[i]), anchor=CENTER)

        # insertion de chaque ligne de la matrice
        # conversion d'une ligne de type 'Series' en 'List' pour pouvoir y inserer l'indice de chaque ligne de la matrice
        for i in range(len(listeSommets)-1) :
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

        #Lstr = str(L)
        #for i in range(int(graphe[0])):
        #    for j in range(int(graphe[0])):
        #        Lstr[i][j] = "{:>6}".format(str(L[i][j]))
        #print(Lstr)

        # Affichage de la matrice des plus courts chemins et de la matrice des predecesseurs pour chaque itération
        # Création d'un label contenant le numero de l'itération
        #iteration = "k = " + str(k)
        #label_title1 = Label(frame_trace, text=iteration, font=("Courrier", 15), bg='#ffeeee', fg='black',
        #                             justify=LEFT)

        # Création d'un label contenant le graphe des plus courts chemins
        #label_title2 = Label(frame, text=Lstr, font=("Courrier", 15), bg='white', fg='grey',
        #                             justify=LEFT, anchor=CENTER)

        # Création d'un label contenant le graphe des prédecesseurs
        #label_title3 = Label(frame, text=P, font=("Courrier", 15), bg='white', fg='grey', justify=LEFT)

        # Affichage des labels dans le canvas
        #label_title1.pack()
        #label_title2.pack()
        #label_title3.pack()

        #canvas.create_text(5, decalage, text=iteration, justify=LEFT)
        #canvas.create_text(5, decalage+50, text=str(L), justify=RIGHT)
        #canvas.create_text(5, decalage+150, text=str(P), justify=RIGHT)

        #decalage += 200

    nouvelleAnalyse(root, circuit_absorbant)
    return L