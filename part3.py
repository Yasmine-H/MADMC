import gurobipy as grb
import numpy as np
from utils import *
import pandas as pd
import sys
import time


def generate_knapsack_instance(n, p, utility_range=(0, 20), weight_range=(0, 10)):
    objects_utilities = np.random.randint(utility_range[0], utility_range[1], size=(p, n))
    objects_weights = np.random.randint(weight_range[0], weight_range[1], size=p)

    capacity = np.sum(objects_weights) / 2

    return objects_utilities, objects_weights, capacity

def knapsack_plmo(instance, ideal, nadir):
    model = grb.Model("PLMO Knapsack (" + str(instance[0].shape[0]) + ", " + str(instance[1].shape[0]) + ")")

    z_variable = model.addVar(name="z")
    obj_variables = np.array([_ for _ in model.addVars(instance[1].shape[0], vtype=grb.GRB.BINARY, name="w").values()])

    utility_expr = (ideal - instance[0].transpose().dot(obj_variables)) / (ideal - nadir + sys.float_info.epsilon)
    aggregated_utilities = np.sum(utility_expr)

    model.setObjective(z_variable + aggregated_utilities, grb.GRB.MINIMIZE)

    for idx, criterion in enumerate(utility_expr):
        model.addConstr(z_variable >= criterion, "u" + str(idx))

    model.addConstr(np.dot(instance[1], obj_variables) <= instance[2])

    model.setParam('OutputFlag', False)
    model.optimize()
    model.write("knapsack_plmo.lp")

    return model.objVal, [v.x for v in model.getVars()][1:]

def interaction(knapsack):
    processed_data = {str(i) : d for (i, d) in enumerate(knapsack[0])}
    raw_data = pd.DataFrame.from_dict(processed_data, orient='index', columns=["u" + str(i) + "(max)" for i in range(knapsack[0].shape[1])])
    print(raw_data)

    stop = False
    pareto_front = get_pareto(raw_data)
    print("pareto :", pareto_front)
    while not stop:

        # process Nadir
        nadir = np.array([_ for _ in get_nadir(raw_data, pareto_front).values()])
        ideal = np.array([_ for _ in get_ideal(raw_data, pareto_front).values()])
        print("***new nadir \n",nadir)

        value, elems = knapsack_plmo(knapsack, ideal, nadir)
        #values, best_index = tchebycheff_augmente(data, pareto, w, ideal, nadir)

        #print("Solution qu'on vous propose : ", df['nom'][best_index],"\nValeurs :")

        # show result
        for idx, elem in enumerate(elems):
            if np.isclose(elem, 1):
                print("object : {}".format(idx))
                for criterion in raw_data.columns:
                    if np.isclose(elem, 1):
                        #print(raw_data[criterion])
                        print(criterion, ":", raw_data[criterion][idx])

        # ask if satisfied
        satisfait = input("Etes-vous satisfait de la solution retournée? \no : oui \nn : non \nvotre réponse : ")
        if satisfait == "o" :
            stop = True
        else :

            # get favorite criterion to improve
            print("************\nListe des critères : ",raw_data.columns.values)
            c = input("Quel est le critère que vous voulez favoriser ?")
            while c not in raw_data.columns:
                c = input("Quel est le critère que vous voulez favoriser ?")

            bound = np.min(raw_data[c])

            print("---- criterion : ", c," bound =", bound)

            # reduce pareto front
            pareto_front = update_pareto(raw_data, pareto_front, c, bound)

            # check if there are solutions left
            pareto_list = get_paretoList(pareto_front)
            if len(pareto_list) == 0:
                print("Aucune solution ne correspond à vos critères")
                stop = True
#            print("***new pareto \n",pareto)

def benchmark():
    nb_objects_steps = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
    nb_criterion_steps = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
    benchmark_times = []
    for idx1, s1 in enumerate(nb_objects_steps):
        print("objects : ", s1)
        benchmark_times.append([])
        for idx2, s2 in enumerate(nb_criterion_steps):
            print("criterion : ", s2)
            knapsack = generate_knapsack_instance(s2, s1)
            data = {str(i) : d for (i, d) in enumerate(knapsack[0])}
            raw_data = pd.DataFrame.from_dict(data, orient='index', columns=["u" + str(i) + "(max)" for i in range(knapsack[0].shape[1])])

            pareto_front = get_pareto(raw_data)
            nadir = np.array([_ for _ in get_nadir(raw_data, pareto_front).values()])
            ideal = np.array([_ for _ in get_ideal(raw_data, pareto_front).values()])
            current_time = 0
            r = 100
            if s1 >= 500 and s2 >= 500:
                r = 1
            for i in range(r):
                start = time.time()
                knapsack_plmo(knapsack, ideal, nadir)
                end = time.time()
                current_time += (end - start)

            benchmark_times[-1].append(current_time / r)

    print(benchmark_times)

if __name__ == "__main__":
    nb_criterion = 2
    nb_objects = 10
    knapsack = generate_knapsack_instance(nb_criterion, nb_objects)
    #res = knapsack_plmo(knapsack)

    data = {str(i) : d for (i, d) in enumerate(knapsack[0])}
    raw_data = pd.DataFrame.from_dict(data, orient='index', columns=["u" + str(i) + "(max)" for i in range(knapsack[0].shape[1])])

    pareto_front = get_pareto(raw_data)
    nadir = np.array([_ for _ in get_nadir(raw_data, pareto_front).values()])
    ideal = np.array([_ for _ in get_ideal(raw_data, pareto_front).values()])
    print(nadir, ideal)

    res = knapsack_plmo(knapsack, ideal, nadir)
    print(res)
    print("Capacity : ", knapsack[2])
    print("Items total weight : ", np.dot(np.array(res[1]), knapsack[1]))
    print("Items total utility : ", np.sum(np.dot(np.array(res[1]), knapsack[0])))
    benchmark()
    # interaction(knapsack)
