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
O = ['S1', 'S3']
D = ['S5']
# arcs
arcs = list(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Capacity (Trucks/Day)']))

x_keys = arcs

mdl = pulp.LpProblem('MipExMaxFlow', sense=pulp.LpMaximize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpInteger, lowBound=0, name='x')
for s in S:
    if s not in O+D:
        mdl.addConstraint(pulp.lpSum(x[s, j] for i, j in x_keys if i == s) == 0, name=f'C1_{s}')
        mdl.addConstraint(pulp.lpSum(x[i, s] for i, j in x_keys if j == s) == 0, name=f'C2_{s}')
for h in H:
    mdl.addConstraint(pulp.lpSum(x[i, h] for i, j in x_keys if j == h) ==
                      pulp.lpSum(x[h, j] for i, j in x_keys if i == h), name=f'C3_{h}')

for i, j in x_keys:
    x[i, j].upBound = au[i, j]

mdl.setObjective(pulp.lpSum(x[i, j] for i, j in x_keys if j == 'S5'))

status_code = mdl.solve()
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = {(i, j): var.value() for (i, j), var in x.items() if var.value() > 0.5}
    print(x_sol)
else:
    print(f'Model is not optimal. Status: {status}')
