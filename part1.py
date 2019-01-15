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
    '''
    returns True if val1 is better than val2
    '''
    if "max" in columnName:
        return val1>val2
    return val1<val2


def getWorst(data, rows_indices, criterion, bound=None):
    """
    returns worst value given a list 
    """
    worst = None
    
    for index in rows_indices:
        if worst == None :
            if bound == None or (isBetter(data[criterion][index],bound,criterion) and not data[criterion][index]==bound):
                worst = data[criterion][index]
        elif isBetter(worst,data[criterion][index], criterion):
            if bound == None or (isBetter(data[criterion][index],bound,criterion) and not data[criterion][index]==bound):
                worst = data[criterion][index]
        
    
    return worst

def update_weights(ideal, nadir):
    """
    sample the poidss so as to focus around the preferred solution 
    stated by the decision maker
    """
    diff = np.array([np.abs(nadir[criterion]-ideal[criterion])+0.1 for criterion in nadir.keys()])
    
    weights = 1/diff
    
    return weights
  
def get_pareto(data):
    pareto = dict((criterion,[]) for criterion in data.columns.values if not(criterion=='nom')) 
    #{} #indexes of rows containing best criterion
    
    for index, row in data.iterrows():
        for criterion in pareto.keys():
#            print(pareto[criterion])
            if len(pareto[criterion]) == 0: 
                pareto[criterion] = [index]
            elif row[criterion] == data[criterion][pareto[criterion][0]]:
                pareto[criterion].append(index)
            elif isBetter(row[criterion],data[criterion][pareto[criterion][0]],criterion): # row[criterion] < data[criterion][pareto[criterion]]: 
                pareto[criterion] = [index]
    return pareto
      
def get_ideal(data,pareto):
    """
    calculer le point idéal  
    """
    ideal = {criterion:data[criterion][pareto[criterion][0]] for criterion in pareto.keys()}
    
    return ideal

def get_paretoList(pareto):
    """
    retourne une liste des indices des lignes des solutions pareto optimales contenues dans pareto
    pareto : dict contenant pour chaque critère la liste des indices des solutions opt
    """"
    rows = []    
    for pareto_list in pareto.values():
        rows += pareto_list
    rows = set(rows)
#    print(rows)
    return rows

def get_nadir(data, pareto, fav_criterion=None, bound=None):
    """
    retourne une approximation du point nadir. Si une critère est passé en entrée
    accompagné de sa borne inf on le prend en considération lors du calcul 
    """
    rows = get_paretoList(pareto)
    nadir = dict((criterion,None) for criterion in pareto.keys()) 
    for criterion in nadir.keys():
        if fav_criterion == None:
            nadir[criterion] = getWorst(data, rows, criterion)
        elif criterion == fav_criterion:
            nadir[criterion] = getWorst(data, rows, criterion, bound)
            
    return nadir
    

def tchebycheff_augmente(data, pareto, w, ideal, nadir):
    """
    data : solutions (chaque ligne correspond à un ensemble de critères)
    ideal : point de référence
    w : poids associés à chaque critère
    """
    paretoList = get_paretoList(pareto)
    values = dict((row,0) for row in paretoList) 
    
    pareto_list = get_paretoList(pareto)
    epsilon = 0.01
    
    for index in pareto_list:
        difference = [data[criterion][index] - ideal[criterion] for criterion in data.keys()]
        c_values = w*(np.abs(difference)) #calcul de la valeur de chaque critère
        values[index] = np.max(c_values) + epsilon*np.sum(difference)
          
    
    return values, min(values, key=values.get)


def update_pareto(data, pareto, fav_criterion, bound):
    """
    met à jour les pareto en fonction du critère passé en entrée
    """
    new_pareto =  dict((criterion,[]) for criterion in pareto.keys()) 
    
    # gather rows to delete
    for criterion in pareto.keys():
        for index in pareto[criterion]:
            if not data[fav_criterion][index] == bound and isBetter(data[fav_criterion][index], bound, fav_criterion) :
                new_pareto[criterion].append(index)
    
    return new_pareto            


def interaction(df, data):
    
    stop = False
    pareto = get_pareto(data)
    print("pareto :", pareto)
    ideal = get_ideal(data, pareto)
    print("ideal :",ideal)
    while not stop:
        
        # process Nadir
        nadir = get_nadir(data,pareto)
        print("***new nadir \n",nadir)
        
        # update the weights
        w = update_weights(ideal, nadir)
        
        # apply augmented tchebytcheff
        values, best_index = tchebycheff_augmente(data, pareto, w, ideal, nadir)
        print("Solution qu'on vous propose : ", df['nom'][best_index],"\nValeurs :")
        
        # show result
        for criterion in data.columns:
            print(criterion, ":", data[criterion][best_index])
        
        # ask if satisfied
        satisfait = input("Etes-vous satisfait de la solution retournée? \no : oui \nn : non \nvotre réponse : ")
        if satisfait == "o" : 
            stop = True
        else :

            # get favorite criterion to improve
            print("************\nListe des critères : ",data.columns.values)
            c = input("Quel est le critère que vous voulez favoriser ?")
            while c not in data.columns:
                c = input("Quel est le critère que vous voulez favoriser ?")
            bound = data[c][best_index]
            
            print("---- criterion : ", c," bound =", bound)
            
            # reduce pareto front
            pareto = update_pareto(data, pareto, c, bound)
            
            # check if there are solutions left
            pareto_list = get_paretoList(pareto)
            if len(pareto_list) == 0:
                print("Aucune solution ne correspond à vos critères")
                stop = True
#            print("***new pareto \n",pareto)
            
    


            
df = pandas.read_csv('voitures.csv')
print(df)
data = df[['presentation(max)','chassis(max)','prix(min)']] # valeurs utilisées
print(data)


interaction(df, data)
