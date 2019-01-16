import gurobipy as grb
import pandas as pd
import numpy as np
from utils import *


def pairwise_max_regret(x, y, preference_statements):
    model = grb.Model("PMR")
    nb_criteria = x.shape[0]

    variables = np.array([_ for _ in model.addVars(nb_criteria, name="w").values()])
    model.setObjective(np.dot(variables, y.transpose()) - np.dot(variables, x.transpose()), grb.GRB.MAXIMIZE)

    for idx, (x_p, y_p) in enumerate(preference_statements):
        model.addConstr(np.dot(variables, y_p.transpose()) - np.dot(variables, x_p.transpose()) <= 0, "p" + str(idx))

    model.addConstr(np.sum(variables) == 1)
    model.setParam('OutputFlag', False)

    model.optimize()
    model.write("pmr_model.lp")

    return model.objVal, [v.x for v in model.getVars()]


def max_regret(x, alternative_list, preference_statements):
    pairwise_regrets = [pairwise_max_regret(x, a, preference_statements) for a in alternative_list]
    max_idx = np.argmax(np.array([x[0] for x in pairwise_regrets]))
    return max_idx, pairwise_regrets[max_idx][0]

def minimax_regret(alternative_list, preference_statements):
    max_regrets = [max_regret(x, alternative_list, preference_statements) for x in alternative_list]
    min_idx = np.argmin(np.array([x[1] for x in max_regrets]))
    return min_idx, max_regrets[min_idx][1]

if __name__ == "__main__":
    raw_data = pd.read_csv("voitures.csv")
    columns = [c for c in raw_data.columns.values if c != "nom"]
    min_cols = [c for c in columns if "min" in c]
    max_cols = [c for c in columns if "max" in c]


    pareto_front = get_pareto(raw_data)
    nadir = get_nadir(raw_data, pareto_front)
    ideal = get_ideal(raw_data, pareto_front)
    min_nadir = np.array([nadir[k] for k in min_cols])
    min_norm_factor = min_nadir - np.array([ideal[k] for k in min_cols])
    max_norm_factor = np.array([ideal[k] for k in max_cols]) - np.array([nadir[k] for k in max_cols])
    print(min_nadir)

    # Normalization of the data
    alternatives = []
    for _, row in raw_data.iterrows():
        alternatives.append(np.hstack(((min_nadir - row[min_cols].values) / min_norm_factor, row[max_cols].values / max_norm_factor)))

    #alternatives /= np.amax(alternatives, axis=0)
    alternatives = np.array(alternatives)
    print(alternatives)
    print(alternatives.shape)
    print(alternatives[0], alternatives[1])
    pref = [(alternatives[13], alternatives[0]), (alternatives[7], alternatives[0]), (alternatives[9], alternatives[10]), (alternatives[13], alternatives[30]), (alternatives[3], alternatives[4])]
    #print(pairwise_max_regret(alternatives[1], alternatives[0],
    #                          [(alternatives[1], alternatives[0]), (alternatives[0], alternatives[29])]))
    print(max_regret(alternatives[14], alternatives, pref))
    print(minimax_regret(alternatives, pref))
