import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


sites_df = pd.read_csv(os.path.join(_this_directory(), '../data/sites.csv'))
lanes_df = pd.read_csv(os.path.join(_this_directory(), '../data/transportation_lanes.csv'))
# nodes
S = list(sites_df[sites_df['Site Type'] == 'Station']['Site Name'])
H = list(sites_df[sites_df['Site Type'] == 'Hub']['Site Name'])
I = S + H
# arcs
arcs = list(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']))
# transit distance
tc = dict(zip(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']), lanes_df['Transp. Cost (Per Truck)']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']), lanes_df['Capacity (Trucks/Day)']))

x_keys = arcs

mdl = pulp.LpProblem('MipEx_Shortest_Path', sense=pulp.LpMinimize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpInteger, lowBound=0, name='x')

mdl.addConstraint(pulp.lpSum(x[i, 'Station 5'] for i, j in x_keys if j == 'Station 5') == 7, name='C1')
mdl.addConstraint(pulp.lpSum(x['Station 1', j] for i, j in x_keys if i == 'Station 1') == 3, name='C2S1')
mdl.addConstraint(pulp.lpSum(x['Station 3', j] for i, j in x_keys if i == 'Station 3') == 4, name='C2S3')
for h in H:
    mdl.addConstraint(pulp.lpSum(x[i, h] for i, j in x_keys if j == h) ==
                      pulp.lpSum(x[h, j] for i, j in x_keys if i == h), name=f'C3_{h}')

for i, j in x_keys:
    x[i, j].upBound = au[i, j]

mdl.setObjective(pulp.lpSum(tc[i, j] * x[i, j] for i, j in x_keys))

mdl.solve()

x_sol = {(i, j): var.value() for (i, j), var in x.items() if var.value() > 0.5}
print(x_sol)
