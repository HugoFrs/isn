from random import randrange

joueurs={}
tapis=[]
mises={}
derniere_mise={}

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
# Ajoute un nouveau joueur
#-------------------------
def nouveau_joueur(nom_du_joueur):
    global joueurs
    joueurs.update({nom_du_joueur: {
        "jetons": {"rouges":8,"verts":4,"bleus":2,"noirs":2},
        "main": [], # les cartes que le joueur possède en main
        "perdu": False
    }})

#-------------------------
# Tire une carte au hasard
#-------------------------
def nouvelle_carte():
    global paquet

    x=randrange(0,len(paquet))
    nouvelle_carte=paquet[x]
    paquet.remove(paquet[x])

    return nouvelle_carte

#----------------------
# Distribue les cartes
#----------------------
def distribuer():
    global paquet,joueurs

    nouveau_paquet()
    nouvelle_carte()
    for joueur in joueurs.keys():
        joueurs[joueur]["main"]=[nouvelle_carte(),nouvelle_carte()]

    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    tapis.append(nouvelle_carte())
    tapis.append(nouvelle_carte())
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())
    nouvelle_carte() # brûle une carte
    tapis.append(nouvelle_carte())

#----------------------
# Recommence une partie
#----------------------
def nouvelle_partie():
    nouveau_paquet()
    derniere_mise={}
    # + retirer les cartes des mains des joueurs
    # + retirer les cartes sur le tapis
    # + faire gagner les mises

#----------------------
# Fait perdre un joueur
#----------------------
def perdu(nom_du_joueur):
    global joueurs
    joueurs[nom_du_joueur]["perdu"] = True

#----------------------
# Fait miser un joueur
#----------------------
def nouvelle_mise(nom_du_joueur, mise):
    global joueurs, mises
    
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
