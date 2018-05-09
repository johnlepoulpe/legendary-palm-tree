##############
## Logimage ##
##############

B = 0 #case blanche
N = 1 #case noire
inconnu = 2 #case inconnue

from copy import deepcopy 
import numpy
import pylab


##############################################
##Programme principal : solveur de logimage ##
##############################################
res=[]
def resolution_logimage (L,C) :
    global res
    #Mesure de la taille du logimage :
    n=taille(L,C)
    
    #Création des possibilités
    poss_lignes = possibilite_ligne(L,n)
    poss_colonnes = possibilite_colonne(C,n)
    T= creation_tableau_reponse (n) #tableau initial rempli de 2 
    
    # On remplit le tableau tant qu'on est sûr 
    
    #boucle permettant d'entrer dans le backtrack si le tableau n'est pas complété
    Image=backtrack(T,poss_lignes,poss_colonnes)
    
    if Image == None :
        return ('erreur')
    
    return pylab.imshow(Image, cmap= 'gray_r', interpolation = 'nearest')


#########################
## Analyse du logimage ##
#########################

## Détermination de la taille du logimage :

def taille(L,C):
    """détermine la taille de la grille à remplir, et fait les ajustements nécéssaires à la résolution de logimages rectangulaires"""
    nc=len(C)
    nl=len(L)
    if nc==nl:
        n=nc
        
    elif nc>nl :        
        n=nc
        for i in range(nc-nl):
            L.append([0])
    else :
        n=nl
        for i in range (nl-nc):
            C.append([0])
    return(n)

## Création d'une liste de possibilités
# La fonction prend en arguments la liste des indices et la dimension de la ligne/colonne et renvoie une liste de listes de toutes les possibilités. On procède par récursivité. 


def possibilite(Indice,n):   # Indice = liste d'indices de la ligne ou de la colonne, n= nombre de cases à remplir
    l=[]                     # l = toutes les listes de solutions
    
    # Cas 1 : On a déjà travaillé sur toutes les cases, le programme s'arrête. 
    if n == 0 :              
        return [l] 
    
    # Cas 2 : Quand on a déjà rentré toutes les cases noires on complète les cases restantes en blanc 
    if len(Indice)==0:      
        return  [[B]*n]
    
    # Cas 3 : On travaille sur le dernier indice à part 
    if len(Indice)==1:        
        case_blanche = n-Indice[0]
        for k in range (case_blanche+1):
            l.append([B]*k+[N]*Indice[0]+[B]*(n-k-Indice[0]))    #On place la (ou les) case(s) noire(s) dans toutes les positions possibles et on complète avec les blanches 
        return l         
        
    cases_imposees = sum(Indice)+len(Indice)-1         # correspond à l'ensemble des cases à colorier (noires) et aux cases blanches imposées entre les noires
    cases_libres=n-cases_imposees
    
    # Cas 4 : Si on n'a pas de cases libres on crée l'unique possibilté
    if cases_libres == 0:                               
        a = [] 
        for j in range (len(Indice)-1):
             a=a+[N]*Indice[j]+[B]
        a = a + [N]*Indice[-1]
        return [a]
    
    # Si toutes les conditions d'arrêt sont non vérifiées, on rentre dans le programme de récursivité   
    for i in range(cases_libres+1):                 
        m=n-(i+1+Indice[0])                              # cases restantes après chaque boucle 
        for p in possibilite(Indice[1:],m):   
            l.append([B]*i+[N]*Indice[0]+[B]+ p)    # on place les premières cases noires avec leur case blanche imposée, et on répète la même opération pour tous les indices
        
    return l
            
            
## Création des listes (pour les lignes et colonnes) de toutes les possibilités pour le logimage
# Les deux fonctions créent des listes de listes de listes de possibilités pour les lignes et les colonnes séparemment 


def possibilite_ligne(L,n):   # n = nombre de lignes L= liste d'indices pour la ligne 
    poss_lignes = []
    for k in range (n):
        poss_lignes.append(possibilite(L[k],n))
    return poss_lignes
        

def possibilite_colonne(C,n):   # n = nombre de colonnes C= liste d'indices pour la colonne  
    poss_colonnes = []
    for k in range (n):
        poss_colonnes.append(possibilite(C[k],n))
    return poss_colonnes


###################################
## Remplissage du tableau réponse##
###################################

def creation_tableau_reponse (n) :
    return inconnu*numpy.ones((n,n))
    
##remplir les cases certaines dans le tableau réponse

def remplissage_cases_certaines(tableau_reponse,poss_lignes, poss_colonnes,n):
    """compare toutes les possibilités pour une même ligne et remplir le tableau si on trouve une case sûre, noire ou blanche"""
    modif = False #variable-drapeau qui permet de sortir de la boucle finale si on n'a plus de modifications
    
    # on prend les différentes possibilités pour une même ligne
    for i in range (len(poss_lignes)):
        p = len (poss_lignes[i])
        for j in range(n):
            # on somme tous les éléments d'indice j des possibilités pour une ligne donnée : si on trouve p, il n'y a que des 1 donc la case est noire, si on trouve 0, la case est blanche, sinon, elle n'est pas certaine et on ne fait rien
            S = sum(poss_lignes[i][k][j] for k in range (p))
            if S == p and tableau_reponse[i][j] != N :
                tableau_reponse [i][j] = N 
                modif=True
                
            elif S == 0 and tableau_reponse[i][j] != B :
                tableau_reponse [i][j] = B
                modif=True
                
    #on répète l'opération sur les colonnes
    for j in range (len(poss_colonnes)) :
        p = len (poss_colonnes[j])
        for i in range(n):
            S = sum(poss_colonnes[j][k][i] for k in range (p))
            if S == p and tableau_reponse[i][j] != N :
                tableau_reponse [i][j] = N
                modif=True
                
            elif S == 0 and tableau_reponse[i][j] != B:
                tableau_reponse [i][j] = B
                modif=True
                
    return modif          
                                          
                            
## éliminer les listes de possibilités devenues fausses après un premier remplissage        
# On parcourt le tableau, si une case donnée est certaine, toutes les listes de possibilités ne possédant pas cette case sont éliminées

def elimination_possibilites(tableau_reponse,poss_lignes,poss_colonnes,n):

    for i in range(n): #ligne
        for j in range(n): #colonne
            if tableau_reponse[i][j] != inconnu :  #on ne traite pas les cases non sûres (2)
            
                # on regarde toutes les lignes qui contiennent la case considérée
                Linter = [] # liste intermédiaire qui va contenir les possibilités conservées
                for L in poss_lignes[i]: # L = toutes les possibilités pour la ligne du tableau d'indice i
                    if L[j] == tableau_reponse[i][j] :
                        Linter.append(L)
                poss_lignes[i] = deepcopy(Linter)
                
                #on répète la même opération avec les colonnes
                Linter = []
                for C in poss_colonnes[j]:
                    if C[i] == tableau_reponse[i][j] :
                        Linter.append(C)
                poss_colonnes[j] = deepcopy(Linter)
            
    
                
                
                
## remplissage du tableau
#on remplit les cases sûres et on élimine les possibilités non valides tant que le tableau réponse est modifié

def remplissage_tableau (T,poss_lignes,poss_colonnes,n):
        modif=True
       
        while modif :
            modif = remplissage_cases_certaines(T,poss_lignes,poss_colonnes,n)     
            elimination_possibilites(T,poss_lignes,poss_colonnes,n)
    
            

##Backtracking

def meilleur_essai(L):
    """renvoie la plus petite liste de possibilités possédant au moins 2 possibilités"""
    lignes_incertaines=[ (i,len(L[i])) for i in range(len(L)) if len(L[i])!=1]
    # recherche du minimum
    indice, min = lignes_incertaines[0]
    for i,m in lignes_incertaines:
        if m<min :
            indice,min=i,m
    return indice              
      
        
# Lorsqu'il n'y a plus de solution évidente

def est_fini(tableau_reponse,n):
    """ vérifie si le logimage est résolu """
    for i in range(n):
        for j in range(n):
            if tableau_reponse[i][j]==inconnu:
                return False
    return True


def erreur(poss_lignes,poss_colonnes,n):
    """ détecte si une ligne donnée n'a plus de possibilité"""
    for i in range(n):
        if len(poss_lignes[i])==0:
            print("ligne")
            print("i=",i)
            return True
        if len(poss_colonnes[i])==0:
            print("i=",i)
            return True
    return False


def backtrack(tableau_reponse, poss_lignes, poss_colonnes) :
    global res
    
    n=taille(poss_lignes,poss_colonnes)
    er = erreur(poss_lignes, poss_colonnes, n)
    
    changement = True
    
    while not er and changement :
        changement = remplissage_cases_certaines(tableau_reponse, poss_lignes, poss_colonnes, n)
        elimination_possibilites(tableau_reponse,poss_lignes,poss_colonnes,n)
        er = erreur (poss_lignes, poss_colonnes, n)
    res.append([    tableau_reponse,poss_lignes,poss_colonnes])
    
    if est_fini(tableau_reponse, n):
        print(tableau_reponse)
        return tableau_reponse
        
    elif not er :
        rang_essais = meilleur_essai(poss_lignes)
        essais=poss_lignes[rang_essais]
        for es in essais:
            print('r=',rang_essais)
            print('es =',es)
            t,l,c= deepcopy(tableau_reponse), deepcopy (poss_lignes),deepcopy (poss_colonnes)
            l[rang_essais]=[es]
            remplissage_cases_certaines(t,l,c,n)
            elimination_possibilites(t,l,c,n)
            
            print("t=",t)
            b = backtrack(t,l,c)
            if b is not None:
                return b
    return None
            
        
        

"""def backtracking(tableau_reponse,poss_lignes,poss_colonnes,n):
    test_lignes=deepcopy(poss_lignes)
    test_colonnes = deepcopy(poss_colonnes)
    tableau_test=deepcopy(tableau_reponse)
    
    x=meilleur_essai(test_lignes)
    A=test_lignes[x]
    A=[A[0]]
    remplissage_tableau(tableau_test,test_lignes,test_colonnes,n)
    
    if est_fini(tableau_test):
        return tableau_test
    
    
    if erreur(test_lignes,test_colonnes):
        poss_lignes[x].pop(0)
        backtracking(tableau_reponse,poss_lignes,poss_colonnes)
        
    if est_fini(tableau_test) == False :
        backtracking(tableau_test,test_lignes,test_colonnes)

"""

#########################
## Logimage à résoudre ##
#########################

# Indices du logimage 
C1=[[2],[1,1,1],[2,1],[1,1,1],[2]]
L1=[[3],[1],[1,1],[1,1],[5]]

#Truc à pattes
C2 = [[1],[5],[1,2],[3],[2]]
L2 = [[3],[1,1],[4],[3],[1,1]]

#Chateau
C3 = [[3],[1,9],[6,7],[4,4,2,1],[6,4,1],[1,1,9],[6,3],[2,1,5],[2,9],[2,1,2,5],[12],[1,1,4,1],[9,2,1],[15],[1,3]]
L3 =[[1,2],[3,1,4],[5,3,2],[3,2,2,2],[1,3,1,4],[3,5,2],[6,1,1,2],[1,1,6,2],[15],[3,2,2,2,2],[15],[13],[2,2,3,1],[2,1,2,1],[5,5]]

#Abeille
C4 = [[5,3],[8,4,1,1],[9,9],[9,4,1,2],[13],[5,4],[17],[9,4,4],[8,5,1],[5,6,2],[6,4],[2,2,8,1],[4,6,2],[7,4],[2,2,6,1],[3,7,2,2],[6,5],[6],[5,2,2],[3,6]]
L4 = [[2,3,1,1],[4,5,2,2],[4,5,1,1],[4,5,1,2],[4,5,2,1],[4,5,1,4],[3,3,7],[4,3,9],[3,2,11],[2,1,10],[4,9],[15],[14,1],[12,1,2],[5,1,1,2,2,1],[1,1,1,2,2,1,1],[4,2,2,1,1,1],[1,1,1,1,1,1,1],[4,1,1,4,2],[3,2,2,1,1]]

#Tests (à ne pas utiliser car ne marchent pas)
C5=[[1,1,1,1,5],[1,1,1,1,5],[1,1,1,1,5],[1,1,1,1,3],[1,1,1,1,3],[1,1,1,1,1],[1,1,1,1,2,1],[1,1,1,1,5,1,2],[1,1,1,1,7,1,2],[1,1,1,1,11,2],[1,1,1,1,12,3],[6,13,5],[2,13,5],[2,15,6],[4,24],[29],[29],[2,25],[11,12],[4,3,10],[2,6,9],[6,8],[2,6],[2,5],[3,4],[2,4],[4],[2],[1],[1]]
L5 =[[12,3],[1,5],[17,1],[10],[12,8],[1,5],[11,7],[8],[10],[12],[14],[12,2],[12,2],[12,2],[11,3],[12,4],[11,3],[3,12,3],[5,14,2],[30],[5,14],[3,12],[12],[10],[9],[9],[7],[7],[6],[5],[6],[6]]

C6 = [[3],[1,9],[6,7],[3,4,2,1],[6,4,1],[1,1,9],[6,3],[2,1,5],[2,9],[2,1,2,5],[12],[1,1,4,1],[9,2,1],[15],[1,3]]
L6 =[[2],[3,1,4],[5,3,2],[3,2,2,2],[1,3,1,4],[3,5,2],[6,1,1,2],[1,1,6,2],[15],[3,2,2,2,2],[15],[13],[2,2,3,1],[2,1,2,1],[5,5]]

#pégase
Lpegase =[[11],[11],[10],[9,1],[8,3],[8,5],[7,7],[7,9],[5,5,2],[9],[13],[16],[2,14],[2,14],[3,14],[2,15],[2,4,5],[3,4,3],[2,5,1,1],[2,2,1,1],[1,2,2,1],[1,2,2],[1,1],[2,2],[2,2]]
Cpegase =[[1,2],[1,5],[2,6],[2,4],[3,1],[3,5,6],[4,10,2],[6,9,1],[8,11],[9,12],[9,6,3],[15,2],[15,1],[14],[5,7],[8],[10],[11],[12,1],[6,6],[4,2,1],[5,5],[3],[3],[2]]


#Totoro
Ltotoro=[[3,3],[3,3],[4,4],[4,4],[11],[13],[2,5,2],[1,1,3,1,1],[3,2,2,3],[15],[15],[6,6],[4,3,4],[3,3],[3,2,2,3],[2,2],[2,2],[3,3],[2,2],[3,3]]
Ctotoro=[[7],[12],[10,3],[7,5,1],[6,3,1],[6,1,3,1],[5,3],[7,1],[4,2,1],[7,1],[5,3],[6,1,3,1],[6,3,1],[7,5,1],[10,3],[12],[7]]
    
#backtrack
L=[[2,1,1],[1,1],[2],[1,1,1,1],[1,1,1,1,1,1],[1,1,1,1],[2,1,1,1],[1,3,1],[1,1,1,1],[2,1,1,1,3],[1,1,1,1],[1,3,1],[1,1,1,1],[1,1],[1,9]]
C=[[9],[1,1,1,1],[1],[1,1,1,1],[6,3],[1,1],[1,1,1],[1,1,1,1,1],[1,1,6,1],[1,1,1,2],[1,1],[1,1,1],[1,9],[1,1],[1]]

#Nouveau Backtraking 
Lb=[[1,1],[1,3,1],[1],[2,2],[3,2],[3,1,1],[1,1,1],[1,2,2],[1,3,1],[1,1,2,2]]
Cb=[[2,1,3],[1,1],[1,1,2,2],[1,1,1],[1,1,1,1],[4,1,1],[1,2,1],[1,1,1],[1,1,1,1],[1,1,1]]

#3eme essai
Lg = [[1],[2,1],[],[2,1],[2,1],[1,1,1],[1,1,1],[1,1],[1,1,1,1],[1,1,1,1]]
Cg = [[1,1,2],[1],[1,1,2,2],[1],[1,1,1],[2],[2,2],[1,1],[1,1],[1,1]]

Lmarylin = [[9],[7,1],[5,2,2],[4,2,4,10],[3,1,7,4],[2,2,4,2],[2,4,3,2],[2,4,2,3],[1,3,2,2,3],[1,2,4,2],[1,2,1],[1,1,1],[1,1,6,8],[3,3,3,2],[2,3,2,1],[1,1,7,7,1],[2,1,2,1,2,2],[3,3,6,7,1],[5,6,1,1,8],[8,1,1,1,5],[3,1,1,1,1],[1,3,1],[1,7,1],[3,3,4,1],[2,3,2,2,1,1],[2,5,1,2],[3,2,2,1,3,4,1],[4,2,2,1,10,1],[1,3,3,1,3,3,2],[2,6,1,8,1],[3,3,2,6,2],[4,4,4,3,1],[14,7],[12,2,2,5],[12,9,5]]

#Marylin Monroe
Cmarylin = [[13,14],[8,2,5,6],[5,3,2,3,5],[4,2,1,3,4],[3,3,1,2,2,3],[2,2,1,4,2,3],[2,5,2,1,2,3],[1,10,4,2,3,3],[1,5,2,7,5,3],[3,2,4,1,3,4],[3,1,2,3,2,5],[6,1,1,3,11],[2,2,1,1,2,2],[1,1,2,1,3,2,2],[3,1,4,1,4,2],[4,2,3,1,5,1],[6,6,1,2,3,1],[3,1,2,1,3,1],[2,2,2,3,1],[1,6,1,2,3,1],[2,4,5,1],[1,3,1,4,1],[1,2,1,2,1,2,2],[1,2,1,2,2],[1,1,1,4,2],[2,1,1,3,4],[3,1,2,2,5],[6,1,1,3,3,3],[3,4,2,3,4,3],[3,9,1,4,4]]

#Crabe
Lcrabe = [[1],[2],[3],[4,2,2],[6,4],[3,3],[6,2],[2,2],[2,1,1,2],[4,2,2,2],[1,2,1,4,2],[1,1,9,4],[14,2,2],[2,12,2,1],[2,1,10,2,3],[1,15,1],[2,11,4,1],[2,14,3],[1,2,15,1],[1,2,9,2,2,1],[1,3,3],[1,1],[1,1],[1]]

Ccrabe = [[2,3],[1,2,2],[2,2,2,5],[2,1,2,3],[2,1,1,1],[2,2,4],[3,10],[6,8],[4,11],[2,1,9],[2,1,1,10],[2,1,12],[1,12],[1,1,11],[2,9],[3,2,10],[11,1,1,3],[7,1,1,1,2],[2,1,1,1],[1,1,1,2],[1,1,2,2,1],[2,2,2,3],[3,2,2],[1]]

    
##Appel automatique de la fonction
    
    
    
    
    
    
    
    
