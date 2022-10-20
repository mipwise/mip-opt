import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


periods_df = pd.read_csv(os.path.join(_this_directory(), '../data/periods.csv'))
sites_df = pd.read_csv(os.path.join(_this_directory(), '../data/sites.csv'))
lanes_df = pd.read_csv(os.path.join(_this_directory(), '../data/transportation_lanes.csv'))
commodities_df = pd.read_csv(os.path.join(_this_directory(), '../data/commodities.csv'))
# periods
T = list(periods_df['Period ID'])
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
# transit time
tt = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Transit Time (Hrs)']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site ID'], lanes_df['Dest. Site ID']), lanes_df['Capacity (Trucks/Hr)']))
# demand
su = dict(zip(
    zip(commodities_df['Origin Site ID'], commodities_df['Commodity ID'], commodities_df['Arrival Time (Hr)']),
    commodities_df['Demand (Trucks)']))
dm = dict(zip(
    zip(commodities_df['Dest. Site ID'], commodities_df['Commodity ID'], commodities_df['Due Time (Hr)']),
    commodities_df['Demand (Trucks)']))

# Obs.: Defining one decision variable for every arc-commodity-period combination is not a good practice. Why?
x_keys = [(i, j, k, t) for i, j in arcs for k in K for t in T]
y_keys = [(i, k, t) for i in I for k in K for t in T]
z_keys = [(i, j, t) for i, j in arcs for t in T]

mdl = pulp.LpProblem('MipExMultiCommodityWithDueDate', sense=pulp.LpMinimize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
y = pulp.LpVariable.dicts(indices=y_keys, cat=pulp.LpContinuous, lowBound=0, name='y')
z = pulp.LpVariable.dicts(indices=z_keys, cat=pulp.LpInteger, lowBound=0, name='z')

for s in I:
    for k in K:
        for t in T:
            mdl.addConstraint(su.get((s, k, t), 0) + y.get((s, k, t-1), 0)
                              + pulp.lpSum(x.get((i, s, k, t-tt.get((i, s), 0)), 0) for i in I)
                              == dm.get((s, k, t), 0) + y.get((s, k, t), 0)
                              + pulp.lpSum(x.get((s, j, k, t), 0) for j in I), name=f'C1_{s}_{k}_{t}')

for i, j, t in z_keys:
    mdl.addConstraint(pulp.lpSum(x.get((i, j, k, t), 0) for k in K) <= z[i, j, t], name=f'C2_{i}_{j}_{t}')

for i, j, t in z_keys:
    mdl.addConstraint(z[i, j, t] <= au[i, j], name=f'C3_{i}_{j}_{t}')

mdl.setObjective(pulp.lpSum(tc[i, j] * z[i, j, t] for i, j, t in z_keys))

status_code = mdl.solve()
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = [(i, j, k, t, var.value()) for (i, j, k, t), var in x.items() if var.value() > 1e-4]
    x_df = pd.DataFrame(x_sol, columns=['Origin Site ID', 'Dest. Site ID', 'Commodity ID', 'Period', 'Num. Of Trucks'])
    x_df = x_df[['Commodity ID', 'Origin Site ID', 'Dest. Site ID', 'Period', 'Num. Of Trucks']]
    x_df.sort_values('Commodity ID', inplace=True)
    print(x_df.to_string(index=False))
else:
    print(f'Model is not optimal. Status: {status}')


