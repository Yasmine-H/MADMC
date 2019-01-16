import numpy as np
import matplotlib.pyplot as plt

def isBetter(val1, val2, columnName):
    '''
    returns True if val1 is better than val2
    '''
    if "max" in columnName:
        return val1>val2
    return val1<val2


def getWorst(data, rows_indices, criterion, bound=None):
    """
    returns worst value among the selected rows of data for a given criterion
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


def getBest(data, rows_indices, criterion):
    """
    returns index of best value among the rows of data for a given criterion
    """
    best = None
    for index in rows_indices:
        if best == None or isBetter(data[criterion][index], data[criterion][best], criterion):
            best = index
    
    return best

def update_weights(reference, nadir):
    """
    update the weights according to the difference between the reference point and nadir
    """
    print(nadir, reference)
    diff = np.array([abs(nadir[criterion]-reference[criterion])+0.1 for criterion in nadir.keys()])

    weights = 1/diff
#    print("-------------- new weights!! ",weights)

    return weights


def isDominatedBy(data, index1, index2):
    """
    returns True if solution at row index1 is dominated by the solution at row of index 2 
    """
    
    for criterion in data.columns.values:
        if isBetter(data[criterion][index1], data[criterion][index2], criterion):
#            if index1 == 10:
#                print(criterion, index2, data[criterion][index1], data[criterion][index2],isBetter(data[criterion][index1], data[criterion][index2], criterion) )
            return False
            
    return True


def get_pareto(data):
    """
    returns the pareto solutions 
    """
    pareto = dict((criterion,[]) for criterion in data.columns.values if not(criterion=='nom'))
    #{} #indexes of rows containing best criterion
    
    # gather the possible rows for each criterion (initialize dict)
    for index, row in data.iterrows():
        for criterion in pareto.keys():
#            print(pareto[criterion])
            pareto[criterion].append(index)
                
   
    pareto_list = get_paretoList(pareto)

    # process list of dominated points among the list of pareto solutions
    dominated_points = set([])
    
    for i in pareto_list:
        for j in pareto_list:
            if not i == j and isDominatedBy(data, i, j):
                dominated_points.add(i)
#                print(i," dominé par ",j)
                break
    
    # remove dominated from pareto
    for criterion in pareto.keys():
#            print(criterion, pareto[criterion])
            for row in dominated_points:
                if row in pareto[criterion]:
                    pareto[criterion].remove(row)
    
    return pareto

def get_ideal(data,pareto):
    """
    process the ideal point (fictive point with the best possible value for each criterion)
    """
    ideal = {criterion:data[criterion][getBest(data, pareto[criterion], criterion)] for criterion in pareto.keys()}

    return ideal

def get_paretoList(pareto):
    """
    returns a set of all the pareto solutions contained in pareto
    pareto : dictionary containing for each criterion a list of pareto
    """
    rows = []
    for pareto_list in pareto.values():
        rows += pareto_list
    rows = set(rows)
#    print(rows)
    return rows

def get_nadir(data, pareto, fav_criterion=None, bound=None):
    """
    returns the nadir point for the pareto alternatives. If a criterion is given,
    its bound is taken into account when processing
    """
    rows = get_paretoList(pareto)
    nadir = dict((criterion,None) for criterion in pareto.keys())
    for criterion in nadir.keys():
        if fav_criterion == None:
            nadir[criterion] = getWorst(data, rows, criterion)
        elif criterion == fav_criterion:
            nadir[criterion] = getWorst(data, rows, criterion, bound)

    return nadir

def plot(data, pareto, ideal, nadir, solution,i):
    """
    plots the results
    pareto : list of indices of pareto solutions contained in data
    ideal : dict containing for each criterion the best value for this criterion
    nadir : dict containing for each criterion the worst value for this criterion among pareto list
    solution : index of the row of the suggested solution
    i : counter used when saving the figure
    """
    
    criteria = [criterion for criterion in data.columns.values]
    
    
    pareto_x = [data[criteria[0]][index] for index in pareto]
    pareto_y = [data[criteria[1]][index] for index in pareto]
    
    ideal_x = ideal[criteria[0]] 
    ideal_y = ideal[criteria[1]] 
    
    nadir_x = nadir[criteria[0]] 
    nadir_y = nadir[criteria[1]] 
    
#    print(solution)
    solution_x = data[criteria[0]][solution]
    solution_y = data[criteria[1]][solution]

    plt.xlabel(criteria[0])
    plt.ylabel(criteria[1])
    plt.plot(data[criteria[0]], data[criteria[1]], 'ko', label="points éliminés")
    plt.plot(pareto_x, pareto_y, 'mo', label="solutions pareto optimales restantes")
    plt.plot(ideal_x, ideal_y, 'go', label="point référence")
    plt.plot(nadir_x, nadir_y, 'ro', label="point nadir")
    plt.plot(solution_x, solution_y, 'bo', label="solution proposée")
    
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
   
    plt.show()

def update_pareto(data, pareto, fav_criterion, bound):
    """
    update the pareto list according to the criterion fav_criterion and its bound
    """
    new_pareto =  dict((criterion,[]) for criterion in pareto.keys())


    for criterion in pareto.keys():
        for index in pareto[criterion]:
            if not data[fav_criterion][index] == bound and isBetter(data[fav_criterion][index], bound, fav_criterion):
                new_pareto[criterion].append(index)

    return new_pareto