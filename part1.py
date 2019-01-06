#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas
import matplotlib as plt



"""
TODO:
    1/ what if ideal==nadir ? 
    2/ change the weights update procedure ?
    3/ a lot of tests, ex. with 2 values and plot them
    4/ add the mode automatic mode 
"""

def isBetter(val1, val2, columnName):
    if "max" in columnName:
        return val1>val2
    return val1<val2

def update_weights(ideal, nadir, bias=None, preferred_criterion=None):
    """
    sample the poidss so as to focus around the preferred solution 
    stated by the decision maker
    """
    if bias is None:
        bias = dict((criterion,1) for criterion in data.columns.values)
    
    else:
        bias[preferred_criterion]+=1
    
    diff = np.array([nadir[criterion]-ideal[criterion]+0.1 for criterion in nadir.keys()])
    
    weights = [val for val in bias.values()]/diff
#    weights = np.array([val for val in bias.values()])/sum([val for val in bias.values()])

    return bias, weights
  
      
def get_ideal_nadir(data):
    """
    calculer le point idéal et l'approximation du point nadir 
    """
    ideal_dict = dict((criterion,None) for criterion in data.columns.values if not(criterion=='nom')) 
    #{} #indexes of rows containing best criterion
    
    for index, row in data.iterrows():
        for criterion in ideal_dict.keys():
            if ideal_dict[criterion] == None or isBetter(row[criterion],data[criterion][ideal_dict[criterion]],criterion): # row[criterion] < data[criterion][ideal_dict[criterion]]: 
                ideal_dict[criterion] = index
            
    ideal = {criterion:data[criterion][ideal_dict[criterion]] for criterion in ideal_dict.keys()}
    nadir = {criterion:max([data[criterion][row] for row in ideal_dict.values()]) 
    for criterion in ideal_dict.keys()}    
    return ideal, nadir    

def tchebycheff_augmente(data, w, ideal, nadir):
    """
    déterminer la solution la plus proche du point idéal dans la direction du point nadir, au
    sens de la norme de Tchebycheff augmenté
    data : solutions (chaque ligne correspond à un ensemble de critères)
    ideal : point de référence
    w : poids associés à chaque critère
    """
    values = np.zeros((data.shape[0],1))
    print(values.shape)
    
    epsilon = 0.01
    for index, row in data.iterrows():
        difference = [row[criterion] - ideal.get(criterion, 0) for criterion in data.keys()]
        c_values = w*(np.abs(difference)) #calcul de la valeur de chaque critère
        values[index] = np.max(c_values) + epsilon*np.sum(difference)
    
    return values, np.argmin(values)


def interaction(df, data):
    
    stop = False
    
    ideal, nadir = get_ideal_nadir(data)
    print("ideal :",ideal)
    print("nadir :",nadir)
    
    bias, w = update_weights(ideal, nadir)
    while not stop:
        values, best_index = tchebycheff_augmente(data, w, ideal, nadir)
        print("Solution qu'on vous propose : ", df['nom'][best_index],"\nValeurs :")
        for criterion in data.columns:
            print(criterion, ":", data[criterion][best_index])
        satisfait = input("Etes-vous satisfait de la solution retournée? \no : oui \nn : non \nvotre réponse : ")
        if satisfait == "o" : 
            stop = True
        else :
#            identifier le critère principal sur lequel il faudrait apporter une amélioration 
#            et le cas échéant de
#            proposer une solution qui va dans le sens indiqué
            print("************\nListe des critères : ",data.columns.values)
            c = input("Quel est le critère que vous voulez favoriser ?")
            while c not in data.columns:
                c = input("Quel est le critère que vous voulez favoriser ?")
            bias, w = update_weights(ideal, nadir, bias=bias, preferred_criterion=c)


            
df = pandas.read_csv('voitures.csv')
print(df)
data = df[['presentation(max)','chassis(max)','prix(min)']] # valeurs utilisées
print(data)


interaction(df, data)
