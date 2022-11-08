import sys, os, time
# pour lire un dictionnaire d'un fichier
import ast
# pour faire la statistique
import numpy
# pour utiliser random, si besoin est
import random

def mon_algo_est_deterministe():
    # par défaut l'algo est considéré comme déterministe
    # changez response = False dans le cas contraire
    response = True
    return response

def potential_sets(el, set_collection_restant):
    potential = []
    for name in set_collection_restant:
        subset = set_collection_restant[name]
        if el in subset:
            potential.append(name)
    return potential

##############################################################
#                      DETERMINISTIC
##############################################################

def det_min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already):
    if el in covered_already:
        return None, covered_already
    potential = potential_sets(el, set_collection_restant)
    if len(potential) == 0:
        return None, covered_already
    elif len(potential) == 1:
        solution = potential[0]
        covered_already = covered_already.union(set_collection_restant[solution])
        return solution, covered_already
    
    # 1 # solution is the subset with the largest number of elements not already covered and in covered already
    # solution = min(potential, key=lambda x: len(set_collection_restant[x] - covered_already))

    # 2 #
    # if univers_size not in [50, 247, 309, 337, 340]:
    #     solution = potential[len(potential)//2]
    # else:
    #     solution = potential[0]

    # 3 #
    if univers_size < 2000:
        means = []
        for X in potential:
            summ=0
            for x in set_collection_restant[X]:
                summ+=len(potential_sets(x, set_collection_restant))
            n=len(set_collection_restant[X])
            if n==0:
                means.append(0)
            else:
                means.append(summ/n)
        solution = potential[means.index(max(means))]
    else:
        solution = max(potential, key=lambda x: len(set_collection_restant[x] - covered_already))

    covered_already = covered_already.union(set_collection_restant[solution])
    return solution, covered_already

##############################################################
#                          RANDOM
##############################################################

def random_min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already):
    if el in covered_already:
        return None, covered_already
    potential = potential_sets(el, set_collection_restant)
    if len(potential) == 0:
        return None, covered_already
    
    # 1 #
    solution = random.choice(potential)

    # 2 #

    covered_already = covered_already.union(set_collection_restant[solution])
    return solution, covered_already

##############################################################
# La fonction à completer pour la compétition
##############################################################

def min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already):
    """
        A Faire:         
        - Ecrire une fonction qui retourne la nouvelle coupe

        :univers_size: taille de l'univers
        
        :collection_size: taille de la famille couvrante

        :set_collection_restant: la famille des ensembles couvrants NON-UTILISES
 
        :el: un élément courant venant de la séquence, à couvrir 

        :covered_already: éléments déjà couverts par une solution en construction 

        :return l'ensemble couvrant el (None si el déjà couvert) et tous les éléménts déjà couverts par une solution en constuction  
    """

    # ###############################
    # complétez cette fonction en choisissant un sous-enseble couvrant l'élément courant el
    # ###############################

    if mon_algo_est_deterministe():
        solution, covered_already = det_min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already)
    else:
        solution, covered_already = random_min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already)

    return solution, covered_already


##############################################################
#### LISEZ LE README et NE PAS MODIFIER LE CODE SUIVANT ####
##############################################################
if __name__=="__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    
    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(output_dir, "doesn't exist")
        exit()       
	
    # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))             
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    # le bloc de lancement dégagé à l'exterieur pour ne pas le répeter pour deterministe/random
    def launching_sequence():
        solution_eleve  = []    
        covered_already = set()
        set_collection_restant = set_collection.copy()
        for el in sequence_a_couvrir:
            # votre algoritme est lancé ici pour un élément courant el
            set_couvrant, covered_already = min_set_cover_online(univers_size, collection_size, set_collection_restant, el, covered_already)
            if set_couvrant is not None :
                solution_eleve.append(set_couvrant)
                del set_collection_restant[set_couvrant]

        # Un algorithme doit toujours tout couvrir (ici, pour vérifier chaque run du randomisé)
        if not set(sequence_a_couvrir).issubset(covered_already):
            print("Couverture n'est pas faite !")
            exit()     
        return solution_eleve, covered_already


    # Collecte des résultats
    scores = []
    
    for instance_filename in sorted(os.listdir(input_dir)):
        
        # C'est une partie pour inserer dans ingestion.py !!!!!
        # importer l'instance depuis le fichier (attention code non robuste)
        # le code repris de Safouan - refaire pour m'affanchir des numéros explicites
        instance_file = open(os.path.join(input_dir, instance_filename), "r")
        lines = instance_file.readlines()
        
        univers_size = int(lines[1])
        collection_size = int(lines[4])
        set_collection = ast.literal_eval(lines[7])
        exact_solution = int(lines[10])
        str_lu_sequence_a_couvrir = lines[13]
        sequence_a_couvrir = ast.literal_eval(str_lu_sequence_a_couvrir)


        # lancement conditionelle de votre algorithme
        # N.B. il est lancé par la fonction launching_sequence() 
        if mon_algo_est_deterministe():
            print("lancement d'un algo deterministe")  
            solution_eleve, covered_already = launching_sequence()
            # la composition de la solution perd son intérêt, conversion vers sa longueur
            # aussi pour être cohérent avec la solution randomisé
            solution_eleve=len(solution_eleve)  
        else:
            print("lancement d'un algo randomisé")
            runs = 10
            sample = numpy.empty(runs)
            for r in range(runs):
                solution_eleve, covered_already = launching_sequence()  
                sample[r] = len(solution_eleve)
            solution_eleve = numpy.mean(sample)


        best_ratio = solution_eleve/float(exact_solution)
        scores.append(best_ratio)
        # ajout au rapport
        output_file.write(instance_filename + ': score: {}\n'.format(best_ratio))

    output_file.write("Résultat moyen des ratios:" + str(sum(scores)/len(scores)))

    output_file.close()

