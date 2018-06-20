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
#IDMOI = int(sys.argv[1])
IDMOI = 5
JOUEURS = 2 #IDMOI #On mets à jour le nombre de jour au fur et à mesure qu'on apperçoit des nouveaux joueurs

class Noeud() : #On partage [id, parent1, parent2, contenu]
  def __init__(self, parent1=-1, parent2=-1, action=[], dernier_temps = -1) : #remplacer le time.time par qqch, c'est pour debug la
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
      return None
    #Temps médian de reception
    return sorted(self.temps)[len(self.temps)//2]
  @property
  def tempsPropre(self) :
    return min([-1] + [i for i in self.temps if i != -1])

class DAG() :
  def __init__(self) :
    #On ajoute un noeud originel pour chaque ligne
    self.liste = []
    for k in range(JOUEURS) :
      self.liste.append([])
      originel = Noeud(k, k)
      self.liste[k].append(originel)
    #Liste de jusqu'à quel indice inclus dans la liste des noeuds de chaque ligne chacun a déjà vu
    self.dejavu = []
    for k in range(JOUEURS) :
      self.dejavu.append([-1]*JOUEURS)
      self.dejavu[k][k] = 0  
      
  def __repr__(self) : #json.loads(repr(listepersonne[0].dag)) pour l'objet json associé
      """On partage tout"""
      return '{"liste" : '+ repr(self.liste) + ', "dejavu" : '+ repr(self.dejavu)+'}'

  def ajout(self, expediteur, destinataire, action, temps) : #expediteur et destinataire sont les id
    noeud = Noeud(destinataire, expediteur, action)
    #Ajout dans la ligne du destinataire
    self.liste[destinataire].append(noeud)
    noeud.temps[destinataire] = temps
    self.dejavu[destinataire][destinataire] += 1
    #Mise à jour des derniers vu pour la ligne destinataire
    for k in range(JOUEURS) :
      #Soit il apprends une nouvelle info, soit ça change rien
      for i in range(self.dejavu[destinataire][k]+1, self.dejavu[expediteur][k]+1) :
        #Mise à jour des temps de reception
        self.liste[k][i].temps[destinataire] = temps
      self.dejavu[destinataire][k] = max(self.dejavu[destinataire][k], self.dejavu[expediteur][k])

  def calculListeValide(self) :
    #Cette liste est définitive et les temps sont communs
    res = [-1]*JOUEURS
    for k in range(JOUEURS) :
      res[k] = min([self.dejavu[i][k] for i in range(JOUEURS)])
    return res

  def graphique(self, avecTempsMoyen = False) :
    """Affiche le dag dans une fenêtre pyplot. Les noeuds valides en bleus et les non valides en rouges"""
    listevalide = self.calculListeValide()
    print("Liste valide", listevalide)
    derniers = [-1]*JOUEURS
    premiers = [self.liste[i][0].temps[i] for i in range(JOUEURS)]
    for k in range(JOUEURS) :
      for i in range(len(self.liste[k])) :
        noeud = self.liste[k][i]
        if i <= listevalide[k] :
          #Le noeud est valide, on affiche le temps final
          date = noeud.tempsFinal
          if not avecTempsMoyen :
            date = noeud.temps[k]
            plt.plot(date-debut, k, "x", color="g")
          else :
            plt.plot(date-debut, k, "x", color="b")
          derniers[k] = max(derniers[k], date)
          if premiers[k] == -1 :
            premiers[k] = date
          #On relie à ses deux parents
          if noeud.parent1 != noeud.parent2 :
            plt.plot([derniers[noeud.parent1]-debut, derniers[noeud.parent1]-debut], [noeud.parent2, noeud.parent1], color="k", alpha=0.3)
        else :
          #Le noeud est pas valide
          date = noeud.temps[k]
          plt.plot(date-debut, k, "x", color="r") #On affiche le temps de reception pour le joueur de la ligne seulement
          derniers[k] = max(derniers[k], date)
          if premiers[k] == -1 :
            premiers[k] = date
          if noeud.parent1 != noeud.parent2 :
            plt.plot([derniers[noeud.parent1]-debut, derniers[noeud.parent1]-debut], [noeud.parent2, noeud.parent1], color="k", alpha=0.3)
    #On trace les lignes de joueurs
    for k in range(JOUEURS) :
      plt.plot([min(premiers)-debut, max(derniers)-debut], [k, k], color="k", alpha=0.3)
    #Affichage
    plt.ylabel('Numéros des joueurs')
    plt.yticks(range(0, 3))
    plt.xlabel('Temps depuis le début du jeu (s)')
    plt.title("Graphe global du système")
    plt.show()

class Personne() :
  def __init__(self, idmoi) :
    self.id = idmoi
    self.dag = DAG() #DAG de ce qu'il passé dans la game pour lui
    self.actionTodo = [] #Celle qu'on va passer dans le prochain noeud
    self.temps = -1
  def partage(self) :
      return repr(self.dag)
  def sync_dag(self, json_obj) :
    """Mets à jour son graphe en fonction du graphe d'un autre"""
    liste = json_obj["liste"]
    _liste = [0]*JOUEURS
    temps_logique = -1 #On ajoute tous les noeuds d'un temps, et ainsi de suite
    nb_vu = 0
    while nb_vu < len(liste) - 1 :
      #On recherche les noeuds qui ont le temps temps_logique
      for _k in liste :
        for k in _k : #Parcours de chaque noeuds de chaque ligne
            parent1 = k["parent1"]
            parent2 = k["parent2"]
            action = k["action"]
            _temps_logique = k["tempsPropre"]
            if _temps_logique == temps_logique :
              #Incrémentaion du nombre de vu
              nb_vu += 1
              _liste[parent1] += 1
              #On regarde si ce noeud était absent du graphe, si oui on l'ajoute
              if _liste[parent1] > len(self.dag.liste[parent1]) :
                  #On ajoute dans la ligne du destinataire (à vérifier) donc destinataire est parent1
                  self.dag.ajout(parent2, parent1, action, self.temps)
      #Incrémentation du temps logique
      temps_logique += 1
  def __repr__(self) :
    return repr(self.liste)

