import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


# region Prepare the input data
sites_df = pd.read_csv(os.path.join(_this_directory(), '../data/woodler/sites.csv'))
trucks_df = pd.read_csv(os.path.join(_this_directory(), '../data/woodler/trucks.csv'))
orders_df = pd.read_csv(os.path.join(_this_directory(), '../data/woodler/orders.csv'))
transit_matrix_df = pd.read_csv(os.path.join(_this_directory(), '../data/woodler/transit_matrix.csv'))

depot_id = 0
# Set of indices
I = set(sites_df['Site ID'])
K = set(trucks_df['Truck ID'])
L = set(orders_df['Order ID'])

# Optimization parameters
u = dict(zip(trucks_df['Truck ID'], trucks_df['Capacity (M3)']))
cf = dict(zip(trucks_df['Truck ID'], trucks_df['Fixed Cost']))
cv = dict(zip(trucks_df['Truck ID'], trucks_df['Variable Cost (dollar/KM)']))
v = dict(zip(orders_df['Order ID'], orders_df['Volume (M3)']))
s = dict(zip(orders_df['Order ID'], orders_df['Site ID']))
td = dict(zip(zip(transit_matrix_df['Origin Site ID'], transit_matrix_df['Dest. Site ID']),
              transit_matrix_df['Distance (KM)']))

# Keys of decision variables
x_keys = [(i, j, k) for i in I for j in I for k in K if i != j]
y_keys = [(k, l) for k in K for l in L]
z_keys = K
# endregion

# region Define the model
# TODO: complete this formulation
mdl = pulp.LpProblem('woodler', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpBinary, name='x')
y = pulp.LpVariable.dicts(indices=y_keys, cat=pulp.LpBinary, name='y')
z = pulp.LpVariable.dicts(indices=z_keys, cat=pulp.LpBinary, name='z')

# Add Constraints
# C1) Every truck departs from the DC

# C2) At most one origin
for k in K:
    for j in I:
        mdl.addConstraint(sum(x.get((i, j, k), 0) for i in I) <= 1, name=f'c2_{k}_{j}')

# C3) At most one destination
for k in K:
    for i in I:
        mdl.addConstraint(sum(x.get((i, j, k), 0) for j in I) <= 1, name=f'c3_{k}_{i}')

# C4) Flow balance
for k in K:
    for h in I:
        mdl.addConstraint(sum(x.get((i, h, k), 0) for i in I) == sum(x.get((h, j, k), 0) for j in I),
                          name=f'c4_{k}_{h}')

# C5) Must deliver every order

# C6) Relationship between y and x

# C7) Relationship between y and z

# C8) Truck capacity

# Miller–Tucker–Zemlin (MTZ) sub-tour elimination constraints

# Dantzig–Fulkerson–Johnson (DFJ) sub-tour elimination constraints


# Set the objective function
variable_cost = sum(cv[k] * td[i, j] * x[i, j, k] for i, j, k in x_keys)
mdl.setObjective(variable_cost)
# endregion

# region Solve the model and retrieve solution
status = mdl.solve(pulp.PULP_CBC_CMD(timeLimit=60, gapRel=0.05))
if pulp.LpStatus[status] == 'Optimal':
    x_sol = [key for key in x_keys if x[key].value() > 0.5]
    print(f'variable_cost: {variable_cost.value()}')
else:
    print(f'Model is not optimal. Status: {status}')
# endregion
