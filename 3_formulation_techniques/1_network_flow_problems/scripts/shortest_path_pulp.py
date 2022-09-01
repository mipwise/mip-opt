import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


sites_df = pd.read_csv(os.path.join(_this_directory(), '../data/sites.csv'))
lanes_df = pd.read_csv(os.path.join(_this_directory(), '../data/transportation_lanes.csv'))
# nodes
S = list(sites_df[sites_df['Site Type'] == 'Station']['Site ID'])
H = list(sites_df[sites_df['Site Type'] == 'Hub']['Site ID'])
I = S + H
# arcs
arcs = list(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']))
# transit distance
td = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Transit Distance (Km)']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Capacity (Trucks/Day)']))

x_keys = arcs

mdl = pulp.LpProblem('MipExShortestPath', sense=pulp.LpMinimize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpBinary, name='x')

mdl.addConstraint(pulp.lpSum(x[i, 'S5'] for i, j in x_keys if j == 'S5') == 1, name='C1')
mdl.addConstraint(pulp.lpSum(x['S1', j] for i, j in x_keys if i == 'S1') == 1, name='C2')
for h in H:
    mdl.addConstraint(pulp.lpSum(x[i, h] for i, j in x_keys if j == h) ==
                      pulp.lpSum(x[h, j] for i, j in x_keys if i == h), name=f'C3_{h}')

mdl.setObjective(pulp.lpSum(td[i, j] * x[i, j] for i, j in x_keys))

mdl.solve()

x_sol = [(i, j) for (i, j), var in x.items() if var.value() > 0.5]
print(x_sol)
