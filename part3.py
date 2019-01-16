import gurobipy as grb
import numpy as np
from utils import *
import pandas as pd


def generate_knapsack_instance(n, p, utility_range=(0, 20), weight_range=(0, 10)):
    objects_utilities = np.random.randint(utility_range[0], utility_range[1], size=(p, n))
    objects_weights = np.random.randint(weight_range[0], weight_range[1], size=p)

    capacity = np.sum(objects_weights) / 2

    return objects_utilities, objects_weights, capacity

def knapsack_plmo(instance, ideal, nadir):
    model = grb.Model("PLMO Knapsack (" + str(instance[0].shape[0]) + ", " + str(instance[1].shape[0]) + ")")

    z_variable = model.addVar(name="z")
    obj_variables = np.array([_ for _ in model.addVars(instance[1].shape[0], vtype=grb.GRB.BINARY, name="w").values()])

    utility_expr = (ideal - instance[0].transpose().dot(obj_variables)) / (ideal - nadir)
    aggregated_utilities = np.sum(utility_expr)

    model.setObjective(z_variable + aggregated_utilities, grb.GRB.MINIMIZE)

    for idx, criterion in enumerate(utility_expr):
        model.addConstr(z_variable >= criterion, "u" + str(idx))

    model.addConstr(np.dot(instance[1], obj_variables) <= instance[2])

    model.optimize()
    model.write("knapsack_plmo.lp")

    print(model.objVal)
    return [v.x for v in model.getVars()]

if __name__ == "__main__":
    nb_criterion = 2
    nb_objects = 10
    knapsack = generate_knapsack_instance(nb_criterion, nb_objects)
    #res = knapsack_plmo(knapsack)

    data = {str(i) : d for (i, d) in enumerate(knapsack[0])}
    print(data)
    raw_data = pd.DataFrame.from_dict(data, orient='index', columns=["u" + str(i) + "(max)" for i in range(knapsack[0].shape[1])])
    print(raw_data)

    pareto_front = get_pareto(raw_data)
    nadir = np.array([_ for _ in get_nadir(raw_data, pareto_front).values()])
    ideal = np.array([_ for _ in get_ideal(raw_data, pareto_front).values()])
    print(nadir, ideal)

    res = knapsack_plmo(knapsack, ideal, nadir)
    print(res)
    print("Capacity : ", knapsack[2])
    print("Items total weight : ", np.dot(np.array(res[1:]), knapsack[1]))
    print("Items total utility : ", np.sum(np.dot(np.array(res[1:]), knapsack[0])))
