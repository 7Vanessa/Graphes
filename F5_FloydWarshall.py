import numpy as np
import pandas as pd
import math
import F5_window as w

# Detection de circuit absorbant dans le graphe
def circuitAbsorbant(matrice):
    for i in range(len(matrice)):
        if matrice[i][i]<0:
            return True;
    return False;

# Demande à l'utilisateur si oui ou non il souhaite analyser un nouveau graphe
def nouvelleAnalyse(window, root):
    # reponse de l'utilisateur
    choix = input("Souhaitez-vous analyser un nouveau graphe ? ('o' or 'n')")

    # si oui alors demander un nouveau graphe
    if choix.lower()=="o":
        print("Lancer une nouvelle analyse")
        root.destroy()
        window.destroy()
        w.create_window()


    # si non alors fermer le programme
    if choix.lower()=="n":
        print("Stop")
        exit()

def listeAretesEntrantes(s, aretes):
    databin = {}
    dataval = {}
    # x = un sommet
    for x in range(int(s[0])):
        # print(x)
        listematricebin = np.zeros(int(s[0]))
        listematriceval = math.inf + np.zeros(int(s[0]))
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
        if matrice[i][i]<0:
            return True;
    return False;


def calculmatrices(s, aretes):
    index = np.arange(int(s[0]))
    matricebin = pd.DataFrame(listeAretesEntrantes(s, aretes)[0], index)
    matriceval = pd.DataFrame(listeAretesEntrantes(s, aretes)[1], index)
    return matricebin, matriceval


# print(calculmatrices(s))


def floydWarshall(graphe, window, root):

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
                    print("Présence d'un circuit absorbant")
                    nouvelleAnalyse(window, root)

        # Affichage de la matrice des plus courts chemins et de la matrice des predecesseurs pour chaque itération
        print("\nk = ", k)
        print(L)
        print("\n", P)
    nouvelleAnalyse(window, root)
    return L