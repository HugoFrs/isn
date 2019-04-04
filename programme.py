from random import randrange
from tkinter import *
from tkinter import messagebox # pour les alertes

joueurs={}
joueurs_ordre=[]
ordre = -1
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

canvas.create_image(300, 270, anchor=NW, image=jetonsImages["rouge"])
canvas.create_image(400, 270, anchor=NW, image=jetonsImages["vert"])
canvas.create_image(500, 270, anchor=NW, image=jetonsImages["bleu"])
canvas.create_image(600, 270, anchor=NW, image=jetonsImages["noir"])

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
        "couche": False,
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
    place_carte(250,120, "dos_de_carte")

    tapis.append(nouvelle_carte())
    place_carte(350,120, "dos_de_carte")
    
    tapis.append(nouvelle_carte())
    place_carte(450,120, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(570,120, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(670,120, "dos_de_carte")

#----------------------
# Recommence une partie
#----------------------
def nouvelle_partie():
    global mises_tour, mises
    nouveau_paquet()
    tapis = []
    derniere_mise={}

    # Réinitialisation des boutons
    bouton_relance.configure(state=NORMAL)

    # Réinitialisation des joueurs et des mises
    mises_tour = {}
    mises = {}
    for joueur in joueurs.values():
        joueur["all_in"] = False  # réinitialise le all_in
        joueur["couche"] = False   # les joueurs ayant passé peuvent rejouer
        joueur["main"] = []       # vide la main
        if joueur["perdu"] == False:
            mises_tour.update({joueur["nom"]: 0}) # remets uniquement les joueurs n'ayant pas perdu
            mises.update({joueur["nom"]: {
                    "rouges": 0,
                    "verts": 0,
                    "bleus": 0,
                    "noirs": 0
                }})

    distribuer()
    joueur_suivant()
    position_des_blindes()
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
def nouvelle_mise(nom_du_joueur, mise):
    global joueurs, mises
    
    mises.update({nom_du_joueur: {
            "rouges": mises[nom_du_joueur]["rouges"] + mise["rouges"],
            "verts": mises[nom_du_joueur]["verts"] + mise["verts"],
            "bleus": mises[nom_du_joueur]["bleus"] + mise["bleus"],
            "noirs": mises[nom_du_joueur]["noirs"] + mise["noirs"],
        }})
    for couleur, nbr in mise.items():
        joueurs[nom_du_joueur]["jetons"][couleur] -= nbr

#-----------------------------------
# Fait gagner les mises à un joueur
#-----------------------------------
def gagne_la_mise(nom_du_joueur):
    global joueurs, mises

    for jetons in mises.values():
        for couleur, nbr in jetons.items():
            joueurs[nom_du_joueur]["jetons"][couleur] += nbr
    mises={}

#--------------------
# Affiche le visible
#--------------------
def affiche_visible():
    global visible
    
    # Cache l'ancien visible
    if (visible != {}):
        canvas.delete(visible["nom"])
        canvas.delete(visible["total"])
        canvas.delete(visible["table"]["barre"])
        for main in visible["main"]:
            canvas.delete(visible["main"])
        for key in visible["jetons"].keys():
            canvas.delete(visible["jetons"][key])
        for score in visible["scoreboard"]:
            canvas.delete(score["nom"])
            canvas.delete(score["total"])
            canvas.delete(score["total_mise"])
        for titre in visible["table"]["titres"]:
            canvas.delete(titre)
    
    # Affiche le visible du joueur en cours
    visible = {
        "nom": canvas.create_text(960, 540, text=joueur_en_cours["nom"], font=("Purisa",18), fill="white", anchor="e"),
        "total": canvas.create_text(960, 565, text=str(total(joueur_en_cours["nom"])) + " €", font=("Purisa", 14), fill="white", anchor="e"),
        "jetons": {
            "rouges": canvas.create_text(340, 370, text="x" + str(joueur_en_cours["jetons"]["rouges"]), font=("Purisa",16), fill="white"),
            "verts" : canvas.create_text(440, 370, text="x" + str(joueur_en_cours["jetons"]["verts"]), font=("Purisa",16), fill="white"),
            "bleus" : canvas.create_text(540, 370, text="x" + str(joueur_en_cours["jetons"]["bleus"]), font=("Purisa",16), fill="white"),
            "noirs" : canvas.create_text(640, 370, text="x" + str(joueur_en_cours["jetons"]["noirs"]), font=("Purisa",16), fill="white")
        },
        "main": [],
        "scoreboard": [],
        "table": {}
    }
    i = 0
    for joueur in joueurs.values():
        i += 1
        
        visible["scoreboard"].append({
                "nom": canvas.create_text(31, 600-i*25, text=joueur["nom"], font=("Purisa", 12), fill="white", anchor="w"),
                "total": canvas.create_text(130, 600-i*25, text=str(total(joueur["nom"])) + " €", font=("Purisa", 12), fill="white", anchor="w"),
                "total_mise": canvas.create_text(230, 600-i*25, text=str(mises_tour[joueur["nom"]]) + " €", font=("Purisa", 12), fill="white", anchor="w")
            })
        visible["main"].append(place_carte(420, 490, joueur_en_cours["main"][0]))
        visible["main"].append(place_carte(500, 490, joueur_en_cours["main"][1]))

    i += 1
    visible["table"].update({
        "titres": [
            canvas.create_text(30, 590-i*30, text="NOM", font=("Purisa", 14), fill="white", anchor="w"),
            canvas.create_text(130, 590-i*30, text="TOTAL", font=("Purisa", 14), fill="white", anchor="w"),
            canvas.create_text(230, 590-i*30, text="MISE", font=("Purisa", 14), fill="white", anchor="w")
        ],
        "barre": canvas.create_line(29, 590-i*25, 290, 590-i*25, fill="white", dash=(6))
    })

#------------------------------------------
# Mets à jour les status des boutons etc..
#------------------------------------------
def status_boutons():
    bouton_relance.configure(text="Relancer", state=DISABLED)
    # Valeurs par défaut
    scale_jetons_rouges.set(0)
    scale_jetons_verts.set(0)
    scale_jetons_bleus.set(0)
    scale_jetons_noirs.set(0)
    # Maximum
    scale_jetons_rouges.configure(to=joueur_en_cours["jetons"]["rouges"])
    scale_jetons_verts.configure(to=joueur_en_cours["jetons"]["verts"])
    scale_jetons_bleus.configure(to=joueur_en_cours["jetons"]["bleus"])
    scale_jetons_noirs.configure(to=joueur_en_cours["jetons"]["noirs"])
    # Possibilité de miser ou non les jetons en question
    if (joueur_en_cours["jetons"]["rouges"] > 0):
        scale_jetons_rouges.configure(state=NORMAL)
    else:
        scale_jetons_rouges.configure(state=DISABLED)
        
    if (joueur_en_cours["jetons"]["verts"] > 0):
        scale_jetons_verts.configure(state=NORMAL)
    else:
        scale_jetons_verts.configure(state=DISABLED)

    if (joueur_en_cours["jetons"]["bleus"] > 0):
        scale_jetons_bleus.configure(state=NORMAL)
    else:
        scale_jetons_bleus.configure(state=DISABLED)
    
    if (joueur_en_cours["jetons"]["noirs"] > 0):
        scale_jetons_noirs.configure(state=NORMAL)
    else:
        scale_jetons_noirs.configure(state=DISABLED)


#-------------------------
# Passe au joueur suivant
#-------------------------
def joueur_suivant():
    global ordre, joueur_en_cours, mises_tour, total_jetons

    total_jetons = 0

    # Vérifie si tous les joueurs ont atteint la même mise
    boucle_terminee = 0
    for nom_joueur in mises_tour.keys():
        if (joueurs[nom_joueur]["couche"] == False):
            if (boucle_terminee == 0):
                boucle_terminee = mises_tour[nom_joueur]
            elif (boucle_terminee != mises_tour[nom_joueur]):
                break
            elif (boucle_terminee == mises_tour[nom_joueur]):
                boucle_terminee = True
                break

    # Affichage des cartes et passage au tour suivant (si tous les joueurs ont atteint la même mise)
    if (boucle_terminee == True):
        # TODO: Révélation des cartes et passage au tour suivant
        affiche_visible()
        status_boutons()
        messagebox.showinfo("INFORMATION", "FIN DU TOUR, TOUS LES JOUEURS ONT ATTEINT LA MÊME MISE.\n(suite du programme prochainement...)")
        return False

    # Cherche le joueur suivant (+ passe numéro d'ordre suivant)
    while True:
        if (ordre >= len(joueurs)-1):
            ordre = 0
        else: 
            ordre += 1
        nom = joueurs_ordre[ordre]
        joueur_en_cours = joueurs[nom]
        if (joueur_en_cours["perdu"] == False and joueur_en_cours["couche"] == False): 
            break

    # Passe le tour du joueur s'il a all-in
    if (joueur_en_cours["all_in"] == True):
        joueur_suivant()
        return False # stop la procédure joueur_suivant() en cours

    affiche_visible()
    status_boutons()


#--------------------------------------------
# Récupère et affiche le total de la relance
#--------------------------------------------
def total_relance(event = False):
    global visible, total_jetons
    total_jetons = 0
    r = scale_jetons_rouges.get()
    v = scale_jetons_verts.get()
    b = scale_jetons_bleus.get()
    n = scale_jetons_noirs.get()

    # Modifie le visible (nombre de jetons)
    canvas.itemconfigure(visible["jetons"]["rouges"], text="x"+ str(joueur_en_cours["jetons"]["rouges"] - r))
    canvas.itemconfigure(visible["jetons"]["verts"], text="x"+ str(joueur_en_cours["jetons"]["verts"] - v))
    canvas.itemconfigure(visible["jetons"]["bleus"], text="x"+ str(joueur_en_cours["jetons"]["bleus"] - b))
    canvas.itemconfigure(visible["jetons"]["noirs"], text="x"+ str(joueur_en_cours["jetons"]["noirs"] - n))

    # Calcul des totaux
    total_jetons += r * 25
    total_jetons += v * 50
    total_jetons += b * 100
    total_jetons += n * 200
    tot = total_jetons + mises_tour[joueur_en_cours["nom"]]

    # Modifie le visible (total du joueur)
    canvas.itemconfigure(visible["total"], text=str(total(joueur_en_cours["nom"]) - total_jetons) + " €") 

    if (total_jetons == 0):
        bouton_relance.configure(text="Relancer", state=DISABLED)
    elif (tot == mise_initiale):
        bouton_relance.configure(text="Suivre pour " + str(total_jetons) + " €", state=NORMAL)
    elif (tot >= mise_initiale*2):
        bouton_relance.configure(text="Relancer de " + str(total_jetons) + " €", state=NORMAL)
    else:
        bouton_relance.configure(text="Mise insuffisante", state=DISABLED)
    return total_jetons

#---------------------
# Le joueur se couche
#---------------------
def se_coucher():
    global mises_tour
    joueur_en_cours["couche"] = True
    if (len(mises_tour) == 1): # s'il ne reste plus qu'un joueur, il gagne
        nouvelle_partie()
    else:
        joueur_suivant()

#------------------
# Relance une mise
#------------------
def relancer():
    global relance_mise, mises_tour, mise_initiale
    relance_mise = total_jetons
    tot = relance_mise + mises_tour[joueur_en_cours["nom"]]
    if (relance_mise == total(joueur_en_cours["nom"])): # relance de tout ce qu'il possède donc all-in
        joueur_en_cours["all_in"] = True
    mise_initiale = relance_mise
    nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": scale_jetons_rouges.get(),
            "verts": scale_jetons_verts.get(),
            "bleus": scale_jetons_bleus.get(),
            "noirs": scale_jetons_noirs.get()
        })
    mises_tour.update({joueur_en_cours["nom"]: mise_initiale + mises_tour[joueur_en_cours["nom"]]})
    joueur_suivant()

#----------------------
# Mise tout les jetons
#----------------------
def all_in():
    global mise_initiale, mises_tour
    joueur_en_cours["all_in"] = True
    bouton_relance.configure(state=DISABLED)
    mise_initiale = total(joueur_en_cours["nom"]) + mises_tour[joueur_en_cours["nom"]]
    nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": joueur_en_cours["jetons"]["rouges"],
            "verts": joueur_en_cours["jetons"]["verts"],
            "bleus": joueur_en_cours["jetons"]["bleus"],
            "noirs": joueur_en_cours["jetons"]["noirs"]
        })
    mises_tour.update({joueur_en_cours["nom"]: mise_initiale})
    joueur_suivant()

#-------
# Check
#-------
def check():
    global mise_initiale
    mise_initiale=0
    joueur_suivant()

#------------------------------------
# Mise de la grosse et petite blinde
#------------------------------------
def position_des_blindes():

    # PETITE BLINDE
    if (joueur_en_cours["jetons"]["rouges"] >= 1): # Mise par rouge (défaut)
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 1, "verts": 0,
            "bleus": 0, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 25})
    elif (joueur_en_cours["jetons"]["verts"] >= 1): # Mise par vert si plus de rouges
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 1,
            "bleus": 0, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 50})
    elif (joueur_en_cours["jetons"]["bleus"] >= 1): # Mise par bleu si plus de verts
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 0,
            "bleus": 1, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 100})
    elif (joueur_en_cours["jetons"]["noirs"] >= 1): # Mise par noir si plus de bleus
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 0,
            "bleus": 0, "noirs": 1
        })
        mises_tour.update({joueur_en_cours["nom"]: 200})
    else:
        joueur_en_cours["perdu"] = True
    
    joueur_suivant()

    # GROSSE BLINDE
    if (joueur_en_cours["jetons"]["rouges"] >= 2): # Mise par rouges (défaut)
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 2, "verts": 0,
            "bleus": 0, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 50})
    elif (joueur_en_cours["jetons"]["verts"] >= 1): # Mise par vert si plus de rouges
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 1,
            "bleus": 0, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 50})
    elif (joueur_en_cours["jetons"]["bleus"] >= 1): # Mise par bleu si plus de verts
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 0,
            "bleus": 1, "noirs": 0
        })
        mises_tour.update({joueur_en_cours["nom"]: 100})
    elif (joueur_en_cours["jetons"]["noirs"] >= 1): # Mise par noir si plus de bleus
        nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": 0, "verts": 0,
            "bleus": 0, "noirs": 1
        })
        mises_tour.update({joueur_en_cours["nom"]: 200})

    # INFO: La grosse blinde ne perd pas car elle peut encore avoir un jeton rouge
    joueur_suivant()    
    
    
    
    
#------------------------------------------------------------------------------------------

bouton_se_coucher=Button(fen,text="Se coucher", command=se_coucher)
bouton_se_coucher.pack()
bouton_check=Button(fen,text="Check", state=DISABLED, command=check)
bouton_check.pack()
bouton_all_in=Button(fen,text="All-in", command=all_in)
bouton_all_in.pack()

# Barres de relance
jetons_rouges = IntVar()
scale_jetons_rouges = Scale(fen, orient="horizontal", from_=0, to=8, length=175, label="Jetons rouges", variable=jetons_rouges,
                            resolution=1, tickinterval=1, command=total_relance)
scale_jetons_rouges.pack()

jetons_verts = IntVar()
scale_jetons_verts = Scale(fen, orient="horizontal", from_=0, to=4, length=150, label="Jetons verts", variable=jetons_verts,
                           resolution=1, tickinterval=1, command=total_relance)
scale_jetons_verts.pack()

jetons_bleus = IntVar()
scale_jetons_bleus = Scale(fen, orient="horizontal", from_=0, to=2, length=125, label="Jetons bleus", variable=jetons_bleus,
                           resolution=1, tickinterval=1, command=total_relance)
scale_jetons_bleus.pack()

jetons_noirs = IntVar()
scale_jetons_noirs = Scale(fen, orient="horizontal", from_=0, to=2, length=125, label="Jetons noirs", variable=jetons_noirs,
                           resolution=1, tickinterval=1, command=total_relance)
scale_jetons_noirs.pack()

bouton_relance=Button(fen,text="Relancer", command=relancer, state=DISABLED)
bouton_relance.pack()

mise_initiale=50

nouveau_joueur("Hugo")
nouveau_joueur("Yves")
nouveau_joueur("Lucien")

nouvelle_partie()

fen.mainloop()
