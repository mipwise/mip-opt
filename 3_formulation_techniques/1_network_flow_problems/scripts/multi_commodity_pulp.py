import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


sites_df = pd.read_csv(os.path.join(_this_directory(), '../data/sites.csv'))
lanes_df = pd.read_csv(os.path.join(_this_directory(), '../data/transportation_lanes.csv'))
commodities_df = pd.read_csv(os.path.join(_this_directory(), '../data/commodities.csv'))
# nodes
S = list(sites_df[sites_df['Site Type'] == 'Station']['Site ID'])
H = list(sites_df[sites_df['Site Type'] == 'Hub']['Site ID'])
I = S + H
# commodities
K = list(commodities_df['Commodity ID'])
# arcs
arcs = list(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']))
# transportation cost
tc = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Transp. Cost (Per Truck)']))
# additional transportation cost
ac = dict(zip(commodities_df['Commodity ID'], commodities_df['Additional Cost (%)']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Capacity (Trucks/Day)']))
# demand
su = dict(zip(zip(commodities_df['Origin Site ID'], commodities_df['Commodity ID']), commodities_df['Demand (Trucks)']))
dm = dict(zip(zip(commodities_df['Dest. Site ID'], commodities_df['Commodity ID']), commodities_df['Demand (Trucks)']))

x_keys = [(i, j, k) for i, j in arcs for k in K]  # Obs.: Defining one decision variable for every arc-commodity
# combination is not a good practice. Why?

mdl = pulp.LpProblem('MipExMultiCommodity', sense=pulp.LpMinimize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpInteger, lowBound=0, name='x')

for s in I:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x.get((i, s, k), 0) for i in I) + su.get((s, k), 0) ==
                          pulp.lpSum(x.get((s, j, k), 0) for j in I) + dm.get((s, k), 0), name=f'C1_{s}_{k}')

for i, j in arcs:
    mdl.addConstraint(pulp.lpSum(x.get((i, j, k), 0) for k in K) <= au[i, j], name=f'C2_{i}_{j}')

mdl.setObjective(pulp.lpSum((1+ac[k]) * tc[i, j] * x[i, j, k] for i, j, k in x_keys))

status_code = mdl.solve()
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = {(i, j, k): var.value() for (i, j, k), var in x.items() if var.value() > 0.5}
    print(x_sol)
else:
    print(f'Model is not optimal. Status: {status}')


