import numpy as np

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
    """
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