import pulp
import pandas as pd
import os
import inspect
import networkx as nx
import matplotlib.pyplot as plt


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


# region Prepare the input data
cities_df = pd.read_csv(os.path.join(_this_directory(), '../data/tsp/cities.csv'))
travel_costs_df = pd.read_csv(os.path.join(_this_directory(), '../data/tsp/travel_costs.csv'))
# cities
I = list(cities_df['City ID'])
# arcs
arcs = list(zip(travel_costs_df['Origin City ID'], travel_costs_df['Dest. City ID']))
# travel cost
c = dict(zip(zip(travel_costs_df['Origin City ID'], travel_costs_df['Dest. City ID']), travel_costs_df['Travel Cost']))
# keys for decision variables
x_keys = arcs
# endregion

# region Define the model
mdl = pulp.LpProblem('TSP', sense=pulp.LpMinimize)

# decision variables
x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpBinary, name='x')

# main constraints
for j in I:
    mdl.addConstraint(pulp.lpSum(x[i, j] for i, j_ in x_keys if j_ == j) == 1, name=f'C1_{j}')

for k in I:
    mdl.addConstraint(pulp.lpSum(x[i, k] for i, j in x_keys if j == k) ==
                      pulp.lpSum(x[k, j] for i, j in x_keys if i == k), name=f'C2_{k}')

# DFJ two-sites sub-tours elimination constraints
# for i, j in x_keys:
#     mdl.addConstraint(x[i, j] + x[j, i] <= 1, name=f'dfj_{i}_{j}')

# MTZ sub-tours elimination constraints
n = len(I)
u = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpInteger, lowBound=1, upBound=n, name='u')
for i, j in x_keys:
    if j != I[0]:
        mdl.addConstraint(u[i] + 1 - n * (1 - x[i, j]) <= u[j], name=f'mtz_{i}_{j}')

# objective function
mdl.setObjective(pulp.lpSum(c[i, j] * x[i, j] for i, j in x_keys))
# endregion

# region Solve the model and retrieve solution
status_code = mdl.solve()
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = [(i, j) for (i, j), var in x.items() if var.value() > 0.5]
    print(x_sol)
    # plot solution
    G = nx.DiGraph()
    G.add_weighted_edges_from([(i, j, v) for (i, j), v in c.items()])
    node_color_map = ['red' if node == I[0] else 'green' for node in G.nodes]
    edge_color_map = ['red' if edge in x_sol else 'gray' for edge in G.edges]
    edge_weight = [2 if edge in x_sol else 0.5 for edge in G.edges]
    nx.draw(G, with_labels=True, font_weight='bold', node_color=node_color_map, edge_color=edge_color_map,
            width=edge_weight)
    plt.show()
else:
    print(f'Model is not optimal. Status: {status}')
# endregion
