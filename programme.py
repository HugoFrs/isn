from random import randrange
from tkinter import *
from tkinter import messagebox # pour les alertes
import sys

joueurs={}
joueurs_ordre=[]
ordre = -1
tapis=[]
mises={}
visible={}

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

canvas.create_image(310, 240, anchor=NW, image=jetonsImages["rouge"])
canvas.create_image(410, 240, anchor=NW, image=jetonsImages["vert"])
canvas.create_image(510, 240, anchor=NW, image=jetonsImages["bleu"])
canvas.create_image(610, 240, anchor=NW, image=jetonsImages["noir"])

paquetImages = {
    "dos_de_carte":  PhotoImage(file="dos_de_carte.png"),
    
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

    "as_de_carreau": PhotoImage(file="as_de_carreau.png"),
    "as_de_coeur":   PhotoImage(file="as_de_coeur.png"),
    "as_de_pic":     PhotoImage(file="as_de_pic.png"),
    "as_de_trefle":  PhotoImage(file="as_de_trefle.png"),
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
        "all_in": False,
        "check": False,
        "combinaisons" : {},
        "valeur_cartes": 0
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
    place_carte(260,110, "dos_de_carte")

    tapis.append(nouvelle_carte())
    place_carte(360,110, "dos_de_carte")
    
    tapis.append(nouvelle_carte())
    place_carte(460,110, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(580,110, "dos_de_carte")
    
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    place_carte(680,110, "dos_de_carte")

#----------------------
# Recommence une partie
#----------------------
def nouvelle_partie():
    global mises_tour, mises, ordre, joueur_en_cours, mise_initiale
    nouveau_paquet()
    tapis = []
    mise_initiale = 50

    # Réinitialisation des boutons
    bouton_relance.configure(state=NORMAL)

    # Réinitialisation des joueurs et des mises
    mises_tour = {}
    mises = {}
    for joueur in joueurs.values():
        joueur["all_in"] = False    # réinitialise le all_in
        joueur["couche"] = False    # les joueurs ayant passé peuvent rejouer
        joueur["main"] = []         # vide la main
        joueur["combinaisons"] = {} # réinitialise les combinaisons
        joueur["valeur_cartes"] = 0 # réinitialise la valeur des cartes
        if joueur["perdu"] == False:
            mises_tour.update({joueur["nom"]: 0}) # remets uniquement les joueurs n'ayant pas perdu
            mises.update({joueur["nom"]: {
                    "rouges": 0,
                    "verts": 0,
                    "bleus": 0,
                    "noirs": 0
                }})

    if (len(mises_tour) == 1):
        messagebox.showinfo("Fin du jeu !", "Il ne reste plus qu'un joueur, la session est donc terminée.")
        fen.destroy()
        sys.exit()

    # Cherche le premier joueur
    while True:
        if (ordre >= len(joueurs)-1):
            ordre = 0
        else: 
            ordre += 1
        nom = joueurs_ordre[ordre]
        joueur_en_cours = joueurs[nom]
        if (joueur_en_cours["perdu"] == False and joueur_en_cours["couche"] == False): 
            break

    distribuer()
    affiche_visible()
    position_des_blindes()

#----------------
# Cloture le jeu
#----------------
def fin_jeu():
    # CALCUL DES COMBINAISONS ET VALEURS DE CARTES
    for joueur in joueurs.values():
        if (joueur["couche"] == False):
            toutes_les_cartes = tapis + joueur["main"]
            cartes_tri = tri(toutes_les_cartes)
            joueur["combinaisons"] = combinaisons(cartes_tri)
            joueur["valeur_cartes"] = valeur_cartes(cartes_tri)

    gagnant = None
    for joueur in joueurs.values():
        if (joueur["couche"] == False and (joueur["perdu"] == False or joueur["all_in"] == True)):
            if (gagnant == None):
                gagnant = joueur
            else:
                jc = joueur["combinaisons"]
                gc = gagnant["combinaisons"]
                # COMPARAISON PAR COMBINAISONS
                if (jc["quinte_flush_royale"] > gc["quinte_flush_royale"]):
                    gagnant = joueur
                elif (jc["quinte_flush_royale"] < gc["quinte_flush_royale"]):
                    gagnant = gagnant
                elif (jc["quinte_flush"] > gc["quinte_flush"]):
                    gagnant = joueur
                elif (jc["quinte_flush"] < gc["quinte_flush"]):
                    gagnant = gagnant
                elif (jc["carre"] > gc["carre"]):
                    gagnant = joueur
                elif (jc["carre"] < gc["carre"]):
                    gagnant = gagnant
                elif (jc["full"] > gc["full"]):
                    gagnant = joueur
                elif (jc["full"] < gc["full"]):
                    gagnant = gagnant
                elif (jc["couleur"] > gc["couleur"]):
                    gagnant = joueur
                elif (jc["couleur"] < gc["couleur"]):
                    gagnant = gagnant
                elif (jc["suite"] > gc["suite"]):
                    gagnant = joueur
                elif (jc["suite"] < gc["suite"]):
                    gagnant = gagnant
                elif (jc["suite"] == gc["suite"] and jc["suite"] != 0):
                    if (jc["suite_meilleure_valeur"] > gc["suite_meilleure_valeur"]):
                        gagnant = joueur
                elif (jc["brelan"] < gc["brelan"]):
                    gagnant = gagnant
                elif (jc["brelan"] > gc["brelan"]):
                    gagnant = joueur
                elif (jc["paire"] < gc["paire"]):
                    gagnant = gagnant
                elif (jc["paire"] > gc["paire"]):
                    gagnant = joueur
                else:
                    # COMBINAISONS EGALES DONC COMPARAISON PAR VALEUR CARTES
                    if (joueur["valeur_cartes"] > gagnant["valeur_cartes"]):
                        gagnant = joueur

    gagne_la_mise(gagnant)
    nouvelle_partie()

#----------------
# Tri les cartes
#----------------
def tri(cartes):
    t = {
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
        "10": [],
        "valet": [],
        "reine": [],
        "roi": [],
        "as": [],
        "carreau": [],
        "coeur": [],
        "pic": [],
        "trefle": [],
    }
    for carte in cartes:
        for key in t.keys():
            if (carte.startswith(key) or carte.endswith(key)):
                t[key].append(carte)
    return t

#------------------------------------
# Calcule les points par combinaison
#------------------------------------
def combinaisons(cartes_tri):
    cartes_ordre = list(paquetImages.keys())
    points = 0
    c = {
        "quinte_flush_royale": 0,
        "quinte_flush": 0,
        "carre": 0,
        "full": 0,
        "couleur": 0,
        "suite": 0,
        "suite_meilleure_valeur": 0,
        "brelan": 0,
        "paire": 0
    }

    # QUINTE FLUSH ROYALE
    if (("10_de_carreau" in cartes_tri["carreau"] and "valet_de_carreau" in cartes_tri["carreau"] and "reine_de_carreau" in cartes_tri["carreau"]
         and "roi_de_carreau" in cartes_tri["carreau"] and "as_de_carreau" in cartes_tri["carreau"])
        or ("10_de_coeur" in cartes_tri["coeur"] and "valet_de_coeur" in cartes_tri["coeur"] and "reine_de_coeur" in cartes_tri["coeur"]
            and "roi_de_coeur" in cartes_tri["coeur"] and "as_de_coeur" in cartes_tri["coeur"])
        or ("10_de_pic" in cartes_tri["pic"] and "valet_de_pic" in cartes_tri["pic"] and "reine_de_pic" in cartes_tri["pic"]
            and "roi_de_pic" in cartes_tri["pic"] and "as_de_pic" in cartes_tri["pic"])
        or ("10_de_trefle" in cartes_tri["trefle"] and "valet_de_trefle" in cartes_tri["trefle"] and "reine_de_trefle" in cartes_tri["trefle"] and
            "roi_de_trefle" in cartes_tri["trefle"] and "as_de_trefle" in cartes_tri["trefle"])):
                c["quinte_flush_royale"] += 1

    # QUINTE FLUSH
    if (points == 0): # si pas de quinte flush royale
        for symbole in ["carreau", "coeur", "pic", "trefle"]:
            if (len(cartes_tri[symbole]) >= 5):
                for carte_symbole in cartes_tri[symbole]:
                    index = cartes_ordre.index(carte_symbole)
                    if (index <= 37): # pour ne pas dépasser la liste (53-16)
                        if (cartes_ordre[index+4] in cartes_tri[symbole]
                            and cartes_ordre[index+8] in cartes_tri[symbole]
                            and cartes_ordre[index+12] in cartes_tri[symbole]
                            and cartes_ordre[index+16] in cartes_tri[symbole]):
                                c["quinte_flush"] += 1
    
    # CARRE | BRELAN | PAIRE
    for valeur in ["2","3","4","5","6","7","8","9","10","valet","reine","roi","as"]: # exclu les symboles, on garde uniquement le tri par valeur
        nbr = len(cartes_tri[valeur])
        if (nbr == 7):
            c["carre"] += 1
            c["brelan"] += 1
        elif(nbr == 6):
            c["carre"] += 1
            c["paire"] += 1
        elif(nbr == 5 or nbr == 4):
            c["carre"] += 1
        elif(nbr == 3):
            c["brelan"] += 1
        elif(nbr == 2):
            c["paire"] += 1

    # FULL
    while(c["brelan"] >= 1 and c["paire"] >= 1):
        c["full"] += 1
        c["brelan"] -= 1
        c["paire"] -= 1

    # COULEUR
    for couleur in ["carreau", "coeur", "pic", "trefle"]:
        if (len(cartes_tri[couleur]) >= 5):
            c["couleur"] += 1

    # SUITE
    cartes_tri_ordre = list(cartes_tri.keys())
    for symbole in ["2","3","4","5","6","7","8","9", "10"]:
        index = cartes_tri_ordre.index(symbole)
        if (len(cartes_tri[cartes_tri_ordre[index]]) >= 1
            and len(cartes_tri[cartes_tri_ordre[index+1]]) >= 1
            and len(cartes_tri[cartes_tri_ordre[index+2]]) >= 1
            and len(cartes_tri[cartes_tri_ordre[index+3]]) >= 1
            and len(cartes_tri[cartes_tri_ordre[index+4]]) >= 1):
                c["suite"] += 1
                if (index > c["suite_meilleure_valeur"]):
                    c["suite_meilleure_valeur"] = index
    
    return c

#-----------------------------
# Calcule la valeur par carte
#-----------------------------
def valeur_cartes(cartes_tri):
    i = 0
    points = 0
    for valeur in ["2","3","4","5","6","7","8","9","10","valet","reine","roi","as"]:
        i += 1
        points += len(cartes_tri[valeur])*i
    return points

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
def gagne_la_mise(joueur):
    global mises
    for jetons in mises.values():
        for couleur, nbr in jetons.items():
            joueur["jetons"][couleur] += nbr
    joueur["perdu"] = False # annule la défaite par all-in
    messagebox.showinfo("FELICITATIONS !", joueur["nom"] + " possède le meilleur jeu et remporte " + str(total_mises()) + " €")
    mises={}

#----------------------------------------
# Récupère et affiche le total des mises
#----------------------------------------
def total_mises():
    global visible
    total = 0
    for mise in mises.values():
        total += mise["rouges"] * 25
        total += mise["verts"] * 50
        total += mise["bleus"] * 100
        total += mise["noirs"] * 200
    if ("total_mises" in visible.keys()):
        canvas.itemconfigure(visible["total_mises"], text="BUTIN TOTAL : " + str(total) + " €")
    else:
        visible["total_mises"] = canvas.create_text(30, 40, text="BUTIN TOTAL : " + str(total) + " €", font=("Purisa",14), fill="white", anchor="w")
    return total

#--------------------
# Affiche le visible
#--------------------
def affiche_visible():
    global visible
    
    # Cache l'ancien visible
    if (visible != {}):
        canvas.delete(visible["nom"])
        canvas.delete(visible["total"])
        canvas.delete(visible["total_mises"])
        canvas.delete(visible["tableau"]["barre"])
        for main in visible["main"]:
            canvas.delete(visible["main"])
        for key in visible["jetons"].keys():
            canvas.delete(visible["jetons"][key])
        for score in visible["scoreboard"]:
            canvas.delete(score["nom"])
            canvas.delete(score["total"])
            canvas.delete(score["total_mise"])
        for titre in visible["tableau"]["titres"]:
            canvas.delete(titre)
    
    # Affiche le visible du joueur en cours
    visible = {
        "nom": canvas.create_text(960, 540, text=joueur_en_cours["nom"], font=("Purisa",18), fill="white", anchor="e"),
        "total": canvas.create_text(960, 565, text=str(total(joueur_en_cours["nom"])) + " €", font=("Purisa", 14), fill="white", anchor="e"),
        "jetons": {
            "rouges": canvas.create_text(350, 340, text="x" + str(joueur_en_cours["jetons"]["rouges"]), font=("Purisa",16), fill="white"),
            "verts" : canvas.create_text(450, 340, text="x" + str(joueur_en_cours["jetons"]["verts"]), font=("Purisa",16), fill="white"),
            "bleus" : canvas.create_text(550, 340, text="x" + str(joueur_en_cours["jetons"]["bleus"]), font=("Purisa",16), fill="white"),
            "noirs" : canvas.create_text(650, 340, text="x" + str(joueur_en_cours["jetons"]["noirs"]), font=("Purisa",16), fill="white")
        },
        "main": [],
        "scoreboard": [],
        "tableau": {}
    }
    total_mises()
    i = 0
    for joueur in joueurs.values():
        i += 1
        visible["scoreboard"].append({
                "nom": canvas.create_text(31, 600-i*25, text=joueur["nom"], font=("Purisa", 12), fill="white", anchor="w"),
                "total": canvas.create_text(150, 600-i*25, text=str(total(joueur["nom"])) + " €", font=("Purisa", 12), fill="white", anchor="w"),
                "total_mise": canvas.create_text(250, 600-i*25, text=str(mises_tour[joueur["nom"]]) + " €", font=("Purisa", 12), fill="white", anchor="w")
            })
        visible["main"].append(place_carte(420, 490, joueur_en_cours["main"][0]))
        visible["main"].append(place_carte(500, 490, joueur_en_cours["main"][1]))

    i += 1
    visible["tableau"].update({
        "titres": [
            canvas.create_text(30, 590-i*25-20, text="NOM", font=("Purisa", 14), fill="white", anchor="w"),
            canvas.create_text(150, 590-i*25-20, text="TOTAL", font=("Purisa", 14), fill="white", anchor="w"),
            canvas.create_text(250, 590-i*25-20, text="MISE TOUR", font=("Purisa", 14), fill="white", anchor="w")
        ],
        "barre": canvas.create_line(29, 590-i*25, 350, 590-i*25, fill="white", dash=(1))
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
    # Possibilité de check
    bouton_check.configure(state=NORMAL)
    for mise in mises_tour.values():
        if (mise != 0):
            bouton_check.configure(state=DISABLED)


#--------------------------------------------
# Vérifie la fin de la boucle par les checks
#--------------------------------------------
def fin_de_tour_par_check():
    for nom_joueur in mises_tour.keys():
        if (joueurs[nom_joueur]["check"] == False and joueurs[nom_joueur]["couche"] == False):
            return False
    return True

#--------------------------------------------
# Vérifie la fin de la boucle par les all-in
#--------------------------------------------
def fin_de_tour_par_all_in():
    for nom_joueur in mises_tour.keys():
        if (joueurs[nom_joueur]["all_in"] == False and joueurs[nom_joueur]["couche"] == False):
            return False
    return True

#-------------------------
# Passe au joueur suivant
#-------------------------
def joueur_suivant():
    global ordre, joueur_en_cours, mises_tour, total_jetons, joueurs_ordre
    
    total_jetons = 0

    # Vérifie si tous les joueurs ont atteint la même mise
    boucle_terminee = False
    if (fin_de_tour_par_check() == True):
        boucle_terminee = True
    elif (fin_de_tour_par_all_in() == True):
        boucle_terminee = True
    else:
        x = None
        boucle_terminee = True
        for nom_joueur, mise in mises_tour.items():
            if (joueurs[nom_joueur]["couche"] == False):
                if (x == None):
                    x = mise
                elif (x != mise or mise == 0):
                    boucle_terminee = False
                    break
                    

    # Affichage des cartes et passage au tour suivant (si tous les joueurs ont atteint la même mise)
    if (boucle_terminee == True):
        messagebox.showinfo("INFORMATION", "FIN DU TOUR, TOUS LES JOUEURS ONT ATTEINT LA MÊME MISE.")
        for nom_joueur in mises_tour.keys():
            joueurs[nom_joueur]["check"]= False
            mises_tour[nom_joueur]=0
        mise_initiale=0
        revelation_carte()
        return False # stop la procédure joueur_suivant() en cours

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

#--------------------------------
# Révèle les cartes sur le tapis
#--------------------------------
def revelation_carte():
    global flop, turn, river, jeu_fini
    
    if jeu_fini == True:
        flop=True
        turn=False
        river=False
        jeu_fini=False
        fin_jeu()
        
    elif river == True:
        place_carte(680,110, tapis[4])
        bouton_check.configure(state=NORMAL)
        jeu_fini = True
        river = False
        joueur_suivant()
        
    elif turn == True:
        place_carte(580,110, tapis[3])
        bouton_check.configure(state=NORMAL)
        turn = False
        river=True
        joueur_suivant()
   
    elif flop == True:
        for i in range(3):
            place_carte(260+i*100,110, tapis[i])
        bouton_check.configure(state=NORMAL)
        flop = False
        turn=True
        joueur_suivant()
        
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
        fin_jeu()
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
    mise_initiale = relance_mise +  mises_tour[joueur_en_cours["nom"]]
    nouvelle_mise(joueur_en_cours["nom"], {
            "rouges": scale_jetons_rouges.get(),
            "verts": scale_jetons_verts.get(),
            "bleus": scale_jetons_bleus.get(),
            "noirs": scale_jetons_noirs.get()
        })
    mises_tour.update({joueur_en_cours["nom"]: mise_initiale})
    joueur_suivant()

#----------------------
# Mise tout les jetons
#----------------------
def all_in():
    global mise_initiale, mises_tour
    joueur_en_cours["all_in"] = True
    joueur_en_cours["perdu"] = True
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
    joueur_en_cours["check"] = True
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

flop=True
turn=False
river=False
jeu_fini=False

nouveau_joueur("Hugo")
nouveau_joueur("Yves")
nouveau_joueur("Lucien")

nouvelle_partie()

fen.mainloop()
