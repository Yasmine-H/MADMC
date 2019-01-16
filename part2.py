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
    regret_values = np.array([x[0] for x in pairwise_regrets])
    max_idx = np.argwhere(regret_values == np.amax(regret_values))
    return max_idx.flatten(), pairwise_regrets[max_idx[0][0]][0], [pairwise_regrets[idx][1] for idx in max_idx[0]]

def minimax_regret(alternative_list, preference_statements):
    max_regrets = [max_regret(x, alternative_list, preference_statements) for x in alternative_list]
    regret_values = np.array([x[1] for x in max_regrets])
    min_idx = np.argwhere(regret_values == np.amin(regret_values))
    return min_idx.flatten(), max_regrets[min_idx[0][0]][1], [max_regrets[idx][2] for idx in min_idx[0]]

def pandas_series_to_list(columns, a):
    return [x for _, x in a[columns].iteritems()]

def build_alternative_choice_string(columns, a1, a2):
    lines1 = []
    lines2 = []
    a1 = pandas_series_to_list(columns, a1)
    a2 = pandas_series_to_list(columns, a2)
    res = "Laquelle préférez vous ? Tapez 1 ou 2 : \n"

    for (c, d) in zip(columns, a1):
        lines1.append(c + " : " + str(d))

    for (c, d) in zip(columns, a2):
        lines2.append(c + " : " + str(d))

    length = []

    for (l1, l2) in zip(lines1, lines2):
        length.append(len(l1))

    idx = np.argmax(length)
    max_length = len(lines1[idx])

    for (l1, l2) in zip(lines1, lines2):
        curr_length = len(l1)
        res += l1 + " " * (max_length - curr_length + 4) + l2 + "\n"

    return res

def interactive_elicitation(raw_data, alternatives):
    print("Elicitation interactive. Nous allons vous présenter une série de question afin de déterminer vos préférences ...")

    stop = False
    preference_statements = []
    columns = [c for c in raw_data.columns.values if c != "nom"]
    orig_data = raw_data[columns]

    iter = 0
    while not stop:
        iter += 1

        x_p_idx, v_mmr, weights = minimax_regret(alternatives, preference_statements)
        print(np.array(weights).flatten())
        print(v_mmr)
        if np.isclose(v_mmr, 0):
            print("end")
            print(weights)
            weights = np.array(weights).flatten()
            for (_, d), a in zip(raw_data.iterrows(), alternatives):
                print(d, np.dot(weights, a.transpose()))
            stop = True
            return weights

        print("iteration : ", iter)

        x_p_idx = np.random.choice(x_p_idx)
        x_p = alternatives[x_p_idx]
        y_p_idx = np.random.choice(max_regret(x_p, alternatives, preference_statements)[0])
        y_p = alternatives[y_p_idx]

        print(x_p_idx, y_p_idx)

        choice = ""
        while not choice == "1" and not choice == "2":
            choice = input(build_alternative_choice_string(columns, orig_data.iloc[x_p_idx], orig_data.iloc[y_p_idx]))

        if choice == "1":
            preference_statements.append((x_p, y_p))
        else:
            preference_statements.append((y_p, x_p))

def automatic_elicitation(raw_data, alternatives, dm):
    print("Elicitation interactive. Nous allons vous présenter une série de question afin de déterminer vos préférences ...")

    stop = False
    preference_statements = []
    columns = [c for c in raw_data.columns.values if c != "nom"]
    orig_data = raw_data[columns]

    iter = 0
    while not stop:
        iter += 1

        x_p_idx, v_mmr, weights = minimax_regret(alternatives, preference_statements)
        print(np.array(weights).flatten())
        print(v_mmr)
        if np.isclose(v_mmr, 0):
            print("end")
            print(weights)
            weights = np.array(weights).flatten()
            for (_, d), a in zip(raw_data.iterrows(), alternatives):
                print(d, np.dot(weights, a.transpose()))
            stop = True
            return weights

        print("iteration : ", iter)

        x_p_idx = np.random.choice(x_p_idx)
        x_p = alternatives[x_p_idx]
        y_p_idx = np.random.choice(max_regret(x_p, alternatives, preference_statements)[0])
        y_p = alternatives[y_p_idx]

        print(x_p_idx, y_p_idx)


        if dm(x_p) >= dm(y_p):
            preference_statements.append((x_p, y_p))
        else:
            preference_statements.append((y_p, x_p))


if __name__ == "__main__":
    raw_data = pd.read_csv("voitures.csv")
    columns = [c for c in raw_data.columns.values if c != "nom"]
    min_cols = [c for c in columns if "min" in c]
    max_cols = [c for c in columns if "max" in c]


    pareto_front = get_pareto(raw_data)
    nadir = get_nadir(raw_data, pareto_front)
    ideal = get_ideal(raw_data, pareto_front)
    pareto_alternatives = list(get_paretoList(pareto_front))
    min_nadir = np.array([nadir[k] for k in min_cols])
    min_norm_factor = min_nadir - np.array([ideal[k] for k in min_cols])
    max_norm_factor = np.array([ideal[k] for k in max_cols]) - np.array([nadir[k] for k in max_cols])
    print(min_nadir)

    # Normalization of the data
    alternatives = []
    for _, row in raw_data.iloc[pareto_alternatives].iterrows():
        alternatives.append(np.hstack(((min_nadir - row[min_cols].values) / min_norm_factor, row[max_cols].values / max_norm_factor)))

    #alternatives /= np.amax(alternatives, axis=0)
    alternatives = np.array(alternatives)
    print(alternatives)
    print(alternatives.shape)
    print(alternatives[0], alternatives[1])
    pref = [(alternatives[13], alternatives[0]), (alternatives[7], alternatives[0]), (alternatives[9], alternatives[10]), (alternatives[13], alternatives[12]), (alternatives[3], alternatives[4])]
    #print(pairwise_max_regret(alternatives[1], alternatives[0],
    #                          [(alternatives[1], alternatives[0]), (alternatives[0], alternatives[29])]))
    print(max_regret(alternatives[14], alternatives, pref))
    #print(minimax_regret(alternatives, pref))
    #interactive_elicitation(raw_data, alternatives)
    dm1 = lambda x: np.dot(np.array([0, 0.5, 0.5, 0, 0, 0, 0]), x)
    print(automatic_elicitation(raw_data, alternatives, dm1))
