#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas
import matplotlib as plt
from utils import *


def tchebycheff_augmente(data, pareto, w, ideal, nadir):
    """
    process the aumented tchebytcheff value for each solution among pareto 
    data : solutions (columns = criteria, rows = solutions)
    pareto : list of indices of the rows of the best solutions in data
    ideal : reference point
    w : weights for each criterion
    """
    pareto_list = get_paretoList(pareto)
    values = dict((row,0) for row in pareto_list) 
    
    epsilon = 0.5
    
    for index in pareto_list:
        difference = [abs(data[criterion][index] - ideal[criterion]) for criterion in data.keys()]
        c_values = w*(difference) #calcul de la valeur de chaque critère
        values[index] = np.max(c_values) + epsilon*np.sum(c_values)
    
    return values, min(values, key=values.get)




def interaction(df, data):
    
    """
    interactive exploration of the pareto front using augmented tchebytcheff
    """
    
    stop = False
    pareto = get_pareto(data)
    print(pareto)
    print("Solutions de pareto :", get_paretoList(pareto))
    
    
    suggestion = input("Avez vous une solution en tête que vous aimeriez approcher?\no : oui\nn : non\nvotre réponse : ")
    if suggestion == "o":
        reference = {criterion:0 for criterion in data.columns.values}
        print("Veuillez donner la valeur idéale attendue sur chaque critère :")
        for criterion in reference.keys():
            reference[criterion] = int(input(criterion+" : "))

    else:
        reference = get_ideal(data, pareto)
    print("Point de référence :",reference)
    count = 0
    
    while not stop:

        # process Nadir
        nadir = get_nadir(data,pareto)
        
        
        
        # update the weights
        w = update_weights(reference, nadir)
        
        # apply augmented tchebytcheff
        values, best_index = tchebycheff_augmente(data, pareto, w, reference, nadir)
        
        # plot values
        plot(data, get_paretoList(pareto), reference, nadir, best_index, count)
        print(values)
        # show result
        print("**************************************************")
        print("Solution qu'on vous propose : ", df['nom'][best_index],"\nValeurs :")
        
        for criterion in data.columns:
            print(criterion, ":", data[criterion][best_index])
        print("**************************************************")
        
        # ask if satisfied
        satisfait = input("Etes-vous satisfait de la solution retournée? \no : oui \nn : non \nvotre réponse : ")
        if satisfait == "o" : 
            stop = True
        else :

            # get favorite criterion to improve
            print("************\nListe des critères : ",data.columns.values)
            c = input("Quel est le critère que vous voulez améliorer ?")
            while c not in data.columns:
                c = input("Erreur. \nQuel est le critère que vous voulez améliorer ?\nRéponse : ")
            bound = data[c][best_index]
            
#            print("Select criterion : ", c," bound : ", bound)
            
            # reduce pareto front
            pareto = update_pareto(data, pareto, c, bound)
            
            # check if there are solutions left
            pareto_list = get_paretoList(pareto)
            if len(pareto_list) == 0:
                print("Aucune solution ne correspond à vos critères")
                stop = True

        count += 1
    


            
df = pandas.read_csv('voitures.csv')
#print(df)
#data = df[['presentation(max)','chassis(max)','prix(min)']] # valeurs utilisées
#data = df[['pollution(min)','couple moteur(max)']] # valeurs utilisées
data = df[['prix(min)','presentation(max)']] # valeurs utilisées
print(data)


interaction(df, data)
