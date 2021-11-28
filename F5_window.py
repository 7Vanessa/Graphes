from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import F5_FloydWarshall as fw

# Fonction de création de la fenetre du programme
def create_window():
    # Creation d'une nouvelle fenetre qui permettra l'execution du programme
    window = Tk()

    # Personnalisation de la fenetre
    window.title("Algorithme de Floyd Warshall (Groupe F5)")
    window.geometry("900x600")
    window.minsize(550, 430)
    window.iconbitmap("efrei_logo.ico")
    window.config(background='#ffeeee')

    # Création d'une frame
    frame = Frame(window, bg='#ffeeee')

    # Ajout d'un texte indiquez de choisir le graphe
    label_title = Label(frame, text="Veuillez indiquez le numéro du graphe à étudier : ", font=("Courrier", 30), bg='#ffeeee', fg='grey')
    label_title.pack()

    # Creation de la saisie
    choix = Entry(frame, relief='raised', font=("Courrier", 20), justify="center")
    choix.pack()

    # Creation du bouton
    submit_button = Button(frame, text="Valider", font=("Courrier", 20), bg='white', fg='grey', command=lambda: onClick_Button(int(choix.get()), window, ))
    submit_button.pack()

    # Ajout de la frame a la fenetre
    frame.pack(expand=YES)

    # Affichage de la fenetre
    window.mainloop()


# Appliquer Floyd Warshall directement dans le fichier data, sans avoir besoin d'ouvrir
# Fonction de choix du graphe à étudier
def onClick_Button(numero, window):
    # Creation d'un nouvelle fenetre qui contiendra l'application de l'algorithme de Floyd Warshall
    root = Tk()
    root.title("Floyd Warshall")
    root.config(background='#ffeeee')
    root.geometry("1200x600")
    root.resizable(True, True)
    root.iconbitmap("efrei_logo.ico")

    # Ouverture de du fichier texte contenant la trace
    filename = askopenfilename(parent=root, title="Ouvrir votre fichier de graphes", filetypes=[('txt files', '.txt'), ('all files', '.*')])

    # Recuperation du contenu du fichier texte
    with open(filename) as file:
        content = file.read()

    # Creation de la frame principale
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)

    # Creation d'un canvas
    my_canvas = Canvas(frame, bg='white')
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Ajout d'une barre de defilement
    my_scrollbar = Scrollbar(frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # Configurer le Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Creation d'une frame à l'interieur de la frame principale
    frame_trace = Frame(my_canvas, bg='white')

    # L'ajouter a une fenetre dans le canvas
    my_canvas.create_window((0, 0), window=frame_trace, anchor="nw")

    # Affichage du graphe selectionné
    new_content = content.split("g")

    # Recuperation du graphe à etudier
    my_graphe = new_content[numero]
    my_graphe.strip() # On retire les espaces en trop au debut et à la fin du string

    # On créer une liste avec toutes les lignes de la structure du graphe
    my_graphe = my_graphe.split()

    #Label(frame_trace, text=new_content[numero], bg='white', fg='black', pady=20).pack()

    # On applique Floyd-Warshall
    fw.floydWarshall(my_graphe, window, root)

