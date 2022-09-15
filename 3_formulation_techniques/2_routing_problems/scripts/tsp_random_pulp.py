import math
import pulp
import os
import inspect
import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


def eliminate_this_sub_tour(nodes):
    assert len(nodes) < len(I)
    mdl.addConstraint(pulp.lpSum(x.get((i, j), 0) for i in nodes for j in nodes) <= len(nodes) - 1)


# region Prepare the input data
num_cities = 10
asymmetry = 0.2  # float between 0 (inclusive) and 1 (inclusive), percentage asymmetry between cost(i, j) and cost(j, i)
density = 1.0  # float between 0 (exclusive) and 1 (inclusive), percentage arcs included
random.seed(1)
# cities
I = list(range(1, num_cities+1))
position = {i: (random.randint(1, 3*num_cities), random.randint(1, 3*num_cities)) for i in I}
# arcs
arcs = [(i, j) for i, j in itertools.permutations(I, 2) if random.random() <= density]
# travel cost
c = dict()
for i, j in arcs:
    dist = math.sqrt((position[i][0] - position[j][0]) ** 2 + (position[i][1] - position[j][1]) ** 2)
    deviation = 2 * asymmetry * (random.random() - 0.5)
    c[i, j] = max(1.0, dist + dist * deviation)
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

# DFJ sub-tours elimination constraints
for tup in itertools.combinations(I, 2):
    eliminate_this_sub_tour(tup)
for tup in itertools.combinations(I, 3):
    eliminate_this_sub_tour(tup)
# eliminate_this_sub_tour([1, 17, 12, 6, 15, 9])

# MTZ sub-tours elimination constraints
# n = len(I)
# u = pulp.LpVariable.dicts(indices=I, cat=pulp.LpInteger, lowBound=1, upBound=n, name='u')
# for i, j in x_keys:
#     if j != I[0]:
#         mdl.addConstraint(u[i] + 1 - n * (1 - x[i, j]) <= u[j], name=f'mtz_{i}_{j}')

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
    G.add_nodes_from([(i, {"pos": pos}) for i, pos in position.items()])
    node_color_map = ['red' if node == I[0] else 'gray' for node in G.nodes]
    G.add_edges_from(x_sol)
    edge_color_map = ['gray' for edge in G.edges]
    edge_weight = [2-asymmetry for edge in G.edges]
    nx.draw(G, with_labels=True, node_color=node_color_map, edge_color=edge_color_map,
            width=edge_weight, pos=position)
    plt.show()
else:
    print(f'Model is not optimal. Status: {status}')
# endregion
