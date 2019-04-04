from random import randrange
from tkinter import *
from tkinter import messagebox # pour les alertes

joueurs={}
joueurs_ordre=[]
tour = -1
tapis=[]
mises={}
visible={}
derniere_mise={}

fen = Tk()
fen.title("Poker")

canvas = Canvas(fen, width=1000, height=600, background="darkgreen")
canvas.pack(side=LEFT)

jetonsImages = {
    "rouge": PhotoImage(file="jeton_rouge.png"),
    "vert": PhotoImage(file="jeton_vert.png"),
    "bleu": PhotoImage(file="jeton_bleu.png"),
    "noir": PhotoImage(file="jeton_noir.png")
}

canvas.create_image(300, 350, anchor=NW, image=jetonsImages["rouge"])
canvas.create_image(400, 350, anchor=NW, image=jetonsImages["vert"])
canvas.create_image(500, 350, anchor=NW, image=jetonsImages["bleu"])
canvas.create_image(600, 350, anchor=NW, image=jetonsImages["noir"])

paquetImages = {
    "dos_de_carte":  PhotoImage(file="dos_de_carte.png"),
    
    "as_de_carreau": PhotoImage(file="as_de_carreau.png"),
    "as_de_coeur":   PhotoImage(file="as_de_coeur.png"),
    "as_de_pic":     PhotoImage(file="as_de_pic.png"),
    "as_de_trefle":  PhotoImage(file="as_de_trefle.png"),
    "2_de_carreau":  PhotoImage(file="2_de_carreau.png"),
    "2_de_coeur":    PhotoImage(file="2_de_coeur.png"),
    "2_de_pic":      PhotoImage(file="2_de_pic.png"),
    "2_de_trefle":   PhotoImage(file="2_de_trefle.png"),

    "3_de_carreau":  PhotoImage(file="3_de_carreau.png"),
    "3_de_coeur":    PhotoImage(file="3_de_coeur.png"),
    "3_de_pic":      PhotoImage(file="3_de_pic.png"),
    "3_de_trefle":   PhotoImage(file="3_de_trefle.png"),
    "4_de_carreau":  PhotoImage(file="4_de_carreau.png"),
    "4_de_coeur":    PhotoImage(file="4_de_coeur.png"),
    "4_de_pic":      PhotoImage(file="4_de_pic.png"),
    "4_de_trefle":   PhotoImage(file="4_de_trefle.png"),

    "5_de_carreau":  PhotoImage(file="5_de_carreau.png"),
    "5_de_coeur":    PhotoImage(file="5_de_coeur.png"),
    "5_de_pic":      PhotoImage(file="5_de_pic.png"),
    "5_de_trefle":   PhotoImage(file="5_de_trefle.png"),
    "6_de_carreau":  PhotoImage(file="6_de_carreau.png"),
    "6_de_coeur":    PhotoImage(file="6_de_coeur.png"),
    "6_de_pic":      PhotoImage(file="6_de_pic.png"),
    "6_de_trefle":   PhotoImage(file="6_de_trefle.png"),

    "7_de_carreau":  PhotoImage(file="7_de_carreau.png"),
    "7_de_coeur":    PhotoImage(file="7_de_coeur.png"),
    "7_de_pic":      PhotoImage(file="7_de_pic.png"),
    "7_de_trefle":   PhotoImage(file="7_de_trefle.png"),
    "8_de_carreau":  PhotoImage(file="8_de_carreau.png"),
    "8_de_coeur":    PhotoImage(file="8_de_coeur.png"),
    "8_de_pic":      PhotoImage(file="8_de_pic.png"),
    "8_de_trefle":   PhotoImage(file="8_de_trefle.png"),

    "9_de_carreau":  PhotoImage(file="9_de_carreau.png"),
    "9_de_coeur":    PhotoImage(file="9_de_coeur.png"),
    "9_de_pic":      PhotoImage(file="9_de_pic.png"),
    "9_de_trefle":   PhotoImage(file="9_de_trefle.png"),
    "10_de_carreau": PhotoImage(file="10_de_carreau.png"),
    "10_de_coeur":   PhotoImage(file="10_de_coeur.png"),
    "10_de_pic":     PhotoImage(file="10_de_pic.png"),
    "10_de_trefle":  PhotoImage(file="10_de_trefle.png"),

    "valet_de_carreau": PhotoImage(file="valet_de_carreau.png"),
    "valet_de_coeur":   PhotoImage(file="valet_de_coeur.png"),
    "valet_de_pic":     PhotoImage(file="valet_de_pic.png"),
    "valet_de_trefle":  PhotoImage(file="valet_de_trefle.png"),

    "reine_de_carreau": PhotoImage(file="reine_de_carreau.png"),
    "reine_de_coeur":   PhotoImage(file="reine_de_coeur.png"),
    "reine_de_pic":     PhotoImage(file="reine_de_pic.png"),
    "reine_de_trefle":  PhotoImage(file="reine_de_trefle.png"),
    "roi_de_carreau":   PhotoImage(file="roi_de_carreau.png"),
    "roi_de_coeur":     PhotoImage(file="roi_de_coeur.png"),
    "roi_de_pic":       PhotoImage(file="roi_de_pic.png"),
    "roi_de_trefle":    PhotoImage(file="roi_de_trefle.png"),
}

#------------------------------------------------------------------------------------------

#-------------------------
# Ajoute un nouveau joueur
#-------------------------
def nouveau_joueur(nom_du_joueur):
    global joueurs, joueurs_ordre
    joueurs.update({nom_du_joueur: {
        "nom": nom_du_joueur,
        "jetons": {"rouges":8,"verts":4,"bleus":2,"noirs":2},
        "main": [], # les cartes que le joueur possède en main
        "perdu": False,
        "all_in": False
    }})
    joueurs_ordre.append(nom_du_joueur)

#----------------------------------
# Calcule l'argent total du joueur
#----------------------------------
def total(nom_du_joueur):
    global joueurs
    total = 0
    total += joueurs[nom_du_joueur]["jetons"]["rouges"] * 25
    total += joueurs[nom_du_joueur]["jetons"]["verts"] * 50
    total += joueurs[nom_du_joueur]["jetons"]["bleus"] * 100
    total += joueurs[nom_du_joueur]["jetons"]["noirs"] * 200
    return total
    

#---------------------------------
# Crée un nouveau paquet de cartes
#---------------------------------
def nouveau_paquet():
    global paquet
    paquet=['as_de_carreau','as_de_coeur','as_de_pic','as_de_trefle','2_de_carreau','2_de_coeur','2_de_pic','2_de_trefle',
            '3_de_carreau','3_de_coeur','3_de_pic','3_de_trefle','4_de_carreau','4_de_coeur','4_de_pic','4_de_trefle',
            '5_de_carreau','5_de_coeur','5_de_pic','5_de_trefle','6_de_carreau','6_de_coeur','6_de_pic','6_de_trefle',
            '7_de_carreau','7_de_coeur','7_de_pic','7_de_trefle','8_de_carreau','8_de_coeur','8_de_pic','8_de_trefle',
            '9_de_carreau','9_de_coeur','9_de_pic','9_de_trefle','10_de_carreau','10_de_coeur','10_de_pic','10_de_trefle',
            'valet_de_carreau','valet_de_coeur','valet_de_pic','valet_de_trefle',
            'reine_de_carreau','reine_de_coeur','reine_de_pic','reine_de_trefle','roi_de_carreau','roi_de_coeur','roi_de_pic','roi_de_trefle']
    return paquet

#-------------------------
# Tire une carte au hasard
#-------------------------
def nouvelle_carte():
    global paquet

    x=randrange(0,len(paquet))
    nouvelle_carte=paquet[x]
    paquet.remove(paquet[x])

    return nouvelle_carte

#-------------------
# Affiche une carte
#-------------------
def place_carte(x, y, nom_de_la_carte):
    return canvas.create_image(x,y, anchor=NW, image=paquetImages[nom_de_la_carte])

#----------------------
# Distribue les cartes
#----------------------
def distribuer():
    global paquet, joueurs, tapis

    nouveau_paquet()
    for joueur in joueurs.keys():
        joueurs[joueur]["main"]=[nouvelle_carte(),nouvelle_carte()]

    nouvelle_carte() # brûle une carte
    
    tapis.append(nouvelle_carte())
    place_carte(250,200, "dos_de_carte")

    tapis.append(nouvelle_carte())
    place_carte(350,200, "dos_de_carte")
    
    tapis.append(nouvelle_carte())
    place_carte(450,200, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(570,200, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(670,200, "dos_de_carte")

#----------------------
# Recommence une partie
#----------------------
def nouvelle_partie():
    global tour_joueur, mises_tour
    nouveau_paquet()
    derniere_mise={}
    tapis = []
    distribuer()

    # Réinitialisation des boutons
    bouton_relance.configure(state=NORMAL)

    # Réinitialisation des joueurs et des mises
    mises_tour = {}
    for joueur in joueurs.values():
        joueur["all_in"] = False # réinitialise le all_in
        joueur["main"] = []
        if joueur["perdu"] == False:
            mises_tour.update({joueur["nom"]: 0})

    tour_suivant()
    # TODO: + faire gagner les mises

#----------------------
# Fait perdre un joueur
#----------------------
def perdu(nom_du_joueur):
    global joueurs
    joueurs[nom_du_joueur]["perdu"] = True
    del mises_tour[joueur_en_cours["nom"]]

#----------------------
# Fait miser un joueur
#----------------------
def nouvelle_mise(nom_du_joueur, n):
    global joueurs, mises
    mise={"rouges":int(n%200%50/25),"verts":int(n%200%100/50), "bleus":int(n%200/100), "noirs":int(n/200)}
    
    mises.update({nom_du_joueur: mise})
    derniere_mise = mise
    for couleur, nbr in mise.items():
        joueurs[nom_du_joueur]["jetons"][couleur] -= nbr

#-----------------------------------
# Fait gagner les mises à un joueur
#-----------------------------------
def gagne_la_mise(nom_du_joueur):
    global joueurs, mises

    for miseur, jetons in mises.items():
        for couleur, nbr in jetons.items():
            joueurs[nom_du_joueur]["jetons"][couleur] += nbr
    mises={}

#----------------------------------------
# Passe au tour suivant (joueur suivant)
#----------------------------------------
def tour_suivant():
    global tour, visible, joueur_en_cours, mises_tour

    # Vérifie si tous les joueurs ont atteint la même mise
    boucle_terminee = 0
    for loop in mises_tour.keys():
        if (boucle_terminee == 0):
            boucle_terminee = mises_tour[loop]
        elif (boucle_terminee != mises_tour[loop]):
            break
        elif (boucle_terminee == mises_tour[loop]):
            boucle_terminee = True
            break

    # Affichage des cartes et passage au tour suivant (si tous les joueurs ont atteint la même mise)
    if (boucle_terminee == True):
        # TODO: Révélation des cartes et passage au tour suivant
        messagebox.showinfo("INFORMATION", "FIN DU TOUR, TOUS LES JOUEURS ONT ATTEINT LA MÊME MISE.")
        return False

    # Passe le tour suivant (+ joueur suivant)
    while True:
        if (tour >= len(joueurs)-1):
            tour = 0
        else: 
            tour += 1
        nom = joueurs_ordre[tour]
        joueur_en_cours = joueurs[nom]
        if (joueur_en_cours["perdu"] == False): 
            break

    # Passe le tour du joueur s'il a all-in
    if (joueur_en_cours["all_in"] == True):
        tour_suivant()
        return False # stop la procédure tour_suivant() en cours
    
    # Cache le visible
    if (visible != {}):
        canvas.delete(visible["nom"])
        canvas.delete(visible["total"])
        for i in range(len(visible["main"])):
            canvas.delete(visible["main"][i])
        for key in visible["jetons"].keys():
            canvas.delete(visible["jetons"][key])
    
    # Affiche le visible du joueur suivant
    visible = {
        "nom": canvas.create_text(950, 550, text=nom, font=("Purisa",16), anchor="e"),
        "total": canvas.create_text(950, 575, text=str(total(nom)) + " €", font=("Purisa", 12), anchor="e"),
        "jetons": {
            "rouges": canvas.create_text(340, 445, text="x" + str(joueur_en_cours["jetons"]["rouges"]), font=("Purisa",16), fill="white"),
            "verts" : canvas.create_text(440, 445, text="x" + str(joueur_en_cours["jetons"]["verts"]), font=("Purisa",16), fill="white"),
            "bleus" : canvas.create_text(540, 445, text="x" + str(joueur_en_cours["jetons"]["bleus"]), font=("Purisa",16), fill="white"),
            "noirs" : canvas.create_text(640, 445, text="x" + str(joueur_en_cours["jetons"]["noirs"]), font=("Purisa",16), fill="white")
        },
        "main": []
    }
    for i in range(len(joueur_en_cours["main"])):
        visible["main"].append(place_carte(420+i*80, 500, joueur_en_cours["main"][i]))



#---------------
# Passe le tour
#---------------
def passer():
    global mises_tour
    perdu(joueur_en_cours["nom"])
    tour_suivant()
    print(mises_tour)

#----------------------------
# Suivre le joueur précédent
#----------------------------
def suivre():
    global mises_tour, mise_initiale
    nouvelle_mise(joueur_en_cours["nom"], mise_initiale - mises_tour.get(joueur_en_cours["nom"]))
    mises_tour.update({joueur_en_cours["nom"]: mise_initiale})
    tour_suivant()
    print(mises_tour)

#------------------
# Relance une mise
#------------------
def relancer():
    global relance_mise, mises_tour, mise_initiale
    relance_mise = int(val.get())
    if (relance_mise < mise_initiale*2):
        messagebox.showerror("Erreur lors de la relance", "Vous devez relancer d'au moins " + str(mise_initiale*2) + ".")
    elif (relance_mise > total(joueur_en_cours["nom"])):
        messagebox.showerror("Erreur lors de la relance", "Vous n'avez pas assez de jetons pour miser cette somme.")
    else:
        mise_initiale = relance_mise
        nouvelle_mise(joueur_en_cours["nom"], mise_initiale - mises_tour.get(joueur_en_cours["nom"]))        
        mises_tour.update({joueur_en_cours["nom"]: mise_initiale})
        tour_suivant()
        print(mises_tour)

#----------------------
# Mise tout les jetons
#----------------------
def all_in():
    global mise_initiale, mises_tour, joueur_en_cours
    joueur_en_cours["all_in"] = True
    bouton_relance.configure(state=DISABLED)
    
    mise_initiale = total(joueur_en_cours["nom"]) + mises_tour.get(joueur_en_cours["nom"])
    nouvelle_mise(joueur_en_cours["nom"], mise_initiale - mises_tour.get(joueur_en_cours["nom"])) # mise tous les jetons
    mises_tour.update({joueur_en_cours["nom"]: mise_initiale})
    tour_suivant()
    print(mises_tour)

#-------
# Check
#-------
def check():
    global mise_initiale
    mise_initiale=0
    tour_suivant()
    print(mises_tour)

#------------------------------------
# Mise de la grosse et petite blinde
#------------------------------------
def position_des_blindes():
    
    if mise_initiale/2 > total(joueur_en_cours["nom"])/2:
        perdu(joueur_en_cours["nom"])
    else:
        nouvelle_mise(joueur_en_cours["nom"], mise_initiale/2) # petite blinde
        mises_tour.update({joueur_en_cours["nom"]: mise_initiale/2})
                    # ici la syntaxe est surment a changer mais le but et de connaitre
                    # la mise d'un joueur pour le tour de table
    tour_suivant()

    if mise_initiale > total(joueur_en_cours["nom"]):
        perdu(joueur_en_cours["nom"]) # idem
    else:
        nouvelle_mise(joueur_en_cours["nom"], mise_initiale) # grosse blinde
        mises_tour.update({joueur_en_cours["nom"]: mise_initiale})

    tour_suivant()    
    
    
    
    
#------------------------------------------------------------------------------------------

bouton_passer=Button(fen,text='Passer',command=passer)
bouton_passer.pack()
bouton_suivre=Button(fen,text='Suivre',command=suivre)
bouton_suivre.pack()
bouton_check=Button(fen,text='Check',state=DISABLED,command=check)
bouton_check.pack()
bouton_allin=Button(fen,text='All-in',command=all_in)
bouton_allin.pack()
val=DoubleVar()
Scale1=Scale(fen, orient='vertical', from_=0, to=1000,resolution=25,tickinterval=200,
             length=125,label='Relance',variable=val)
Scale1.pack()
bouton_relance=Button(fen,text='Relancer',command=relancer)
bouton_relance.pack()

mise_initiale=50

nouveau_joueur("Hugo")
nouveau_joueur("Yves")
nouveau_joueur("Lucien")

nouvelle_partie()
position_des_blindes()

fen.mainloop()
