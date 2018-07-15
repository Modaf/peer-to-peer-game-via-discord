"""
Chaque joueur posède un DAG
Il est différent pour chacun mais si suffisament de temps passe ils sont tous pareil à partir d'un certain seuil
Le nombre de joueurs JOUEURS est fixe
Chaque DAG stoque les noeuds par ligne et pour chaque personne combien pour chaque ligne il en a vu
"""

"""
Les temps sont par rapport à la logical clock
"""
#Imports
from matplotlib import pyplot as plt
import sys
import time
import random
import json
from copy import deepcopy
#IDMOI = int(sys.argv[1])

class Noeud() : #On partage [id, parent1, parent2, contenu]
  def __init__(self, parent1=-1, parent2=-1, action=[], dernier_temps = -1, JOUEURS = 0) : #remplacer le time.time par qqch, c'est pour debug la
    self.parent1 = parent1 #Celui de la même ligne
    self.parent2 = parent2
    self.action = action
    self.temps = [-1]*JOUEURS
    self.dernier_temps = dernier_temps #La logical clock
    self.temps[parent1] = self.dernier_temps
  def __repr__(self) :
    return '{"parent1" : ' + repr(self.parent1) + ', "parent2" : ' + repr(self.parent2) + ', "action" : ' + json.dumps(self.action) + ', "temps" : ' + json.dumps(self.temps) + ', "tempsPropre" : ' + str(self.tempsPropre) + '}'
  @property
  def tempsFinal(self) :
    if -1 in self.temps :
      print("Erreur dans le calcul du temps moyen", self.temps)
      print("Parent1", self.parent1, "Parent2", self.parent2)
      return -1
    #Temps médian de reception
    return sorted(self.temps)[len(self.temps)//2-1] #Liste d'au moins deux éléments
  @property
  def tempsPropre(self) :
    #On regarde si c'est un noeud originel
    if self.parent1 == self.parent2 :
      return -1
    try :
      return min([i for i in self.temps if i != -1])
    except :
      print("ERREUR calcul du temps propre alors qu'on est pas un noeud originel")
      return -1

class DAG() :
  def __init__(self, JOUEURS) :
    #Nombre de joueurs
    self.JOUEURS = JOUEURS
    #On ajoute un noeud originel pour chaque ligne
    self.liste = []
    for k in range(self.JOUEURS) :
      self.liste.append([])
      originel = Noeud(k, k, [], -1, self.JOUEURS)
      self.liste[k].append(originel)
    #Liste de jusqu'à quel indice inclus dans la liste des noeuds de chaque ligne chacun a déjà vu
    self.dejavu = []
    for k in range(self.JOUEURS) :
      self.dejavu.append([-1]*(self.JOUEURS))
      self.dejavu[k][k] = 0

  def __repr__(self) : #json.loads(repr(listepersonne[0].dag)) pour l'objet json associé
      """On partage tout"""
      return '{"liste" : '+ repr(self.liste) + ', "dejavu" : '+ repr(self.dejavu)+'}'

  def ajout(self, expediteur, destinataire, action, temps) : #expediteur et destinataire sont les id
    """temps est la date à laquelle on reçoit l'information"""
    noeud = Noeud(destinataire, expediteur, action, temps, self.JOUEURS)
    #Ajout dans la ligne du destinataire
    self.liste[destinataire].append(noeud)
    noeud.temps[destinataire] = temps #inutile
    self.dejavu[destinataire][destinataire] += 1
    #Mise à jour des derniers vu pour la ligne destinataire
    for k in range(self.JOUEURS) :
      #Soit il apprends une nouvelle info, soit ça change rien
      # #Il faudrait affiner cette condition
      for i in range(len(self.liste[k])) :
        #Mise à jour des temps de reception
        if self.liste[k][i].temps[destinataire] == -1 : #Ne devrait pas être la si la condition est suffisament fine
          self.liste[k][i].temps[destinataire] = temps #On apprends l'information à notre temps
      for i in range(self.dejavu[destinataire][k]+1, self.dejavu[expediteur][k]+1) :
        self.dejavu[destinataire][k] = max(self.dejavu[destinataire][k], self.dejavu[expediteur][k]) #Fonctionne normalement

  def calculListeValide(self) :
    #Cette liste est définitive et les temps sont communs
    res = [-1]*(self.JOUEURS)
    for k in range(self.JOUEURS) :
      res[k] = min([self.dejavu[i][k] for i in range(self.JOUEURS)])
    return res

  def graphique(self, avecTempsMoyen = False, tPropre = False) :
    """Affiche le dag dans une fenêtre pyplot. Les noeuds valides en bleus et les non valides en rouges"""
    listevalide = self.calculListeValide()
    print("Liste valide", listevalide)
    derniers = [-1]*(self.JOUEURS)
    premiers = [self.liste[i][0].temps[i] for i in range(self.JOUEURS)]
    for k in range(self.JOUEURS) :
      for i in range(len(self.liste[k])) :
        noeud = self.liste[k][i]
        if i <= listevalide[k] :
          #Le noeud est valide, on affiche le temps final
          date = 0
          if not tPropre :
            date = noeud.tempsFinal
          if tPropre :
            date = noeud.tempsPropre
          if not avecTempsMoyen :
            date = noeud.temps[k]
            plt.plot(date, k, "x", color="g")
          else :
            plt.plot(date, k, "x", color="b")
          derniers[k] = max(derniers[k], date)
          if premiers[k] == -1 :
            premiers[k] = date
          #On relie à ses deux parents
          if noeud.parent1 != noeud.parent2 :
            plt.plot([derniers[noeud.parent1], derniers[noeud.parent1]], [noeud.parent2, noeud.parent1], color="k", alpha=0.3)
        else :
          #Le noeud est pas valide
          date = noeud.temps[k]
          plt.plot(date, k, "x", color="r") #On affiche le temps de reception pour le joueur de la ligne seulement
          derniers[k] = max(derniers[k], date)
          if premiers[k] == -1 :
            premiers[k] = date
          if noeud.parent1 != noeud.parent2 :
            plt.plot([derniers[noeud.parent1], derniers[noeud.parent1]], [noeud.parent2, noeud.parent1], color="k", alpha=0.3)
    #On trace les lignes de joueurs
    for k in range(self.JOUEURS) :
      plt.plot([min(-1, min(premiers)), max(derniers)], [k, k], color="k", alpha=0.3) #TODO : virer ce -1 pour quand un joueur rentre dans le jeu en cours de route
    #Affichage
    plt.ylabel('Numéros des joueurs')
    plt.yticks(range(0, 3))
    plt.xlabel('Temps depuis le début du jeu (s)')
    plt.title("Graphe du système")
    plt.show()

  def graphique_propre(self) :
    """Affiche le dag dans une fenêtre pyplot. Les noeuds valides en bleus et les non valides en rouges"""
    listevalide = self.calculListeValide()
    print("Liste valide", listevalide)
    derniers = [-1]*(self.JOUEURS)
    premiers = [self.liste[i][0].temps[i] for i in range(self.JOUEURS)]
    for k in range(self.JOUEURS) :
      for i in range(len(self.liste[k])) :
        noeud = self.liste[k][i]
        date = noeud.tempsPropre
        plt.plot(date, k, "x", color="b")
        if noeud.parent1 != noeud.parent2 :
          plt.plot([derniers[noeud.parent1], derniers[noeud.parent1]], [noeud.parent2, noeud.parent1], color="k", alpha=0.3)
    #On trace les lignes de joueurs
    for k in range(self.JOUEURS) :
      plt.plot([-1, 10], [k, k], color="k", alpha=0.3)
    #Affichage
    plt.ylabel('Numéros des joueurs')
    plt.yticks(range(0, 3))
    plt.xlabel('Temps depuis le début du jeu (s)')
    plt.title("Graphe global du système")
    plt.show()

class Personne() :
  def __init__(self, idmoi, JOUEURS) :
    self.JOUEURS = JOUEURS
    self.id = idmoi
    self.dag = DAG(self.JOUEURS) #DAG de ce qu'il passé dans la game pour lui
    self.actionTodo = [] #Celle qu'on va passer dans le prochain noeud
    self.temps = -1
  def partage(self) :
      return repr(self.dag)
  def ajoutJoueur(self) :
    #Incrémentation du nombre de joueurs
    self.JOUEURS += 1
    self.dag.JOUEURS += 1
    #Mise à jour de la liste dejavu
    for li in self.dag.dejavu :
      li.append(-1) #Ce qu'à vu le nouveau joueur : rien
    self.dag.dejavu.append([-1]*(self.JOUEURS))
    #Ajout pour chaque noeud du nouveau joueur
    for liste in self.dag.liste :
      for noeud in liste :
        noeud.temps.append(-1)
    #Ajout d'une liste pour le dernier joueur dans le dag
    self.dag.liste.append([])
    originel = Noeud(self.JOUEURS-1, self.JOUEURS-1, [], -1, self.JOUEURS)
    self.dag.liste[-1].append(originel)
  def sync_dag(self, json_obj) :
    """Mets à jour son graphe en fonction du graphe d'un autre"""
    liste = json_obj["liste"]
    _liste = [0]*(self.JOUEURS)
    temps_logique = -1 #On ajoute tous les noeuds d'un temps, et ainsi de suite
    nb_vu = 0
    while nb_vu < sum([len(i) for i in liste]) :
      #On recherche les noeuds qui ont le temps temps_logique
      for _k in liste :
        for k in _k : #Parcours de chaque noeuds de chaque ligne
            parent1 = k["parent1"]
            parent2 = k["parent2"]
            action = k["action"]
            _temps_logique = k["tempsPropre"] #Temps propre du noeud
            if _temps_logique == temps_logique :
              #Incrémentaion du nombre de vu
              nb_vu += 1
              _liste[parent1] += 1
              #On regarde si ce noeud était absent du graphe, si oui on l'ajoute
              if _liste[parent1] > len(self.dag.liste[parent1]) :
                  #On ajoute dans la ligne du destinataire (à vérifier) donc destinataire est parent1
                  self.dag.ajout(parent2, parent1, action, _temps_logique)
                  print("Ajout dans notre graphe")
                  #Mise a jour de la liste de temps du noeud créé
                  self.dag.liste[parent1][-1].temps = deepcopy(k["temps"])
                  self.dag.liste[parent1][-1].temps[parent1] = _temps_logique
      #Incrémentation du temps logique
      temps_logique += 1
    print("Temps logique", temps_logique-1)
  def __repr__(self) :
    return repr(self.liste)

