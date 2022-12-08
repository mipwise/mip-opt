import pulp
import pandas as pd
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


periods_df = pd.read_csv(os.path.join(_this_directory(), '../data/ucp_data_10_generators/periods.csv'))
generators_df = pd.read_csv(os.path.join(_this_directory(), '../data/ucp_data_10_generators/generators.csv'))

# periods
T = list(periods_df['Period ID'])
# generators
I = list(generators_df['Generator ID'])
# generator status
s = dict(zip(generators_df['Generator ID'], generators_df['Status']))
# generator production
p = dict(zip(generators_df['Generator ID'], generators_df['Production']))
# demand
d = dict(zip(periods_df['Period ID'], periods_df['Demand']))
# min power output
pl = dict(zip(generators_df['Generator ID'], generators_df['Min Output']))
# min power output
pu = dict(zip(generators_df['Generator ID'], generators_df['Max Output']))
# production cost
cp = dict(zip(generators_df['Generator ID'], generators_df['Production Cost']))
# startup cost
cu = dict(zip(generators_df['Generator ID'], generators_df['Startup Cost']))
# shutdown cost
cd = dict(zip(generators_df['Generator ID'], generators_df['Shutdown Cost']))
# min up
tu = dict(zip(generators_df['Generator ID'], generators_df['Min Up']))
# min down
td = dict(zip(generators_df['Generator ID'], generators_df['Min Down']))
# max startup rate
su = dict(zip(generators_df['Generator ID'], generators_df['Max Startup Rate']))
# max shutdown rate
sd = dict(zip(generators_df['Generator ID'], generators_df['Max Shutdown Rate']))


x_keys = [(i, t) for i in I for t in T]
y_keys = [(i, t) for i in I for t in T]
z_keys = [(i, t) for i in I for t in [0] + T]
w_keys = [(i, t) for i in I for t in T]

mdl = pulp.LpProblem('MipExMultiCommodityWithDueDate', sense=pulp.LpMinimize)

x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
y = pulp.LpVariable.dicts(indices=y_keys, cat=pulp.LpBinary, name='y')
z = pulp.LpVariable.dicts(indices=z_keys, cat=pulp.LpBinary, name='z')
w = pulp.LpVariable.dicts(indices=w_keys, cat=pulp.LpBinary, name='w')

for i in I:
    if s[i] == 'On':
        z[i, 0].lowBound = 1
    elif s[i] == 'Off':
        z[i, 0].upBound = 0
    else:
        raise ValueError(f'Bad generator status: {s[i]}')

# C1) Demand for power in Period  𝑡 :
for t in T:
    mdl.addConstraint(pulp.lpSum(pl[i] * z[i, t] + x[i, t] for i in I) >= d[t], name=f'C1_{t}')

# C2) If Generator  𝑖  is turned on in Period  𝑡 , then it's on for  𝑡𝑢𝑖  periods:
for i, t in y_keys:
    for tp in T:
        if t <= tp <= t + tu[i] - 1:
            mdl.addConstraint(y[i, t] <= z[i, tp], name=f'C2_{i}_{t}_{tp}')

# C3) If Generator  𝑖  is turned off in Period  𝑡 , then it's off for  𝑡𝑑𝑖  periods:
for i, t in w_keys:
    for tp in T:
        if t <= tp <= t + td[i] - 1:
            mdl.addConstraint(w[i, t] <= 1 - z[i, tp], name=f'C3_{i}_{t}_{tp}')

# C4) Production of Generator  𝑖  must be between its lower and upper bounds:
for i, t in x_keys:
    mdl.addConstraint(x[i, t] <= (pu[i] - pl[i]) * z[i, t], name=f'C4_{i}_{t}')

# C5) If Generator  𝑖  is off in Period  𝑡−1  and on in Period  𝑡 , then it has been turned on:
for i, t in y_keys:
    mdl.addConstraint(z[i, t] - z[i, t-1] <= y[i, t], name=f'C5_{i}_{t}')

# C6) If Generator  𝑖  is turned on in Period  𝑡 , then it was off in Period  𝑡−1 :
for i, t in y_keys:
    mdl.addConstraint(y[i, t] <= 1 - z[i, t - 1], name=f'C6_{i}_{t}')

# C7) If Generator  𝑖  is on in Period  𝑡−1  and off in Period  𝑡 , then it has been turned off:
for i, t in w_keys:
    mdl.addConstraint(z[i, t-1] - z[i, t] <= w[i, t], name=f'C7_{i}_{t}')

# C8) If Generator  𝑖  is turned off in Period  𝑡 , then it was on in Period  𝑡−1 :
for i, t in w_keys:
    mdl.addConstraint(w[i, t] <= z[i, t-1], name=f'C8_{i}_{t}')

# SR1) Production of Generator  𝑖  must not go over  𝑠𝑢𝑖  when it's starting up:
# SR2) Production of Generator  𝑖  must be over  𝑠𝑑𝑖  when it's shutting down:
for i, t in x_keys:
    if t == T[0]:
        mdl.addConstraint(pl[i] * z[i, t] + x[i, t] <= su[i] + (pu[i] - su[i]) * (1 - y[i, t]), name=f'SR1_{i}_{t}')
        mdl.addConstraint(p[i] <= sd[i] + (pu[i] - sd[i]) * (1 - w[i, t]), name=f'SR2_{i}_{t}')
    else:
        mdl.addConstraint(pl[i] * z[i, t] + x[i, t] <= su[i] + (pu[i] - su[i]) * (1 - y[i, t]), name=f'SR1_{i}_{t}')
        mdl.addConstraint(pl[i] * z[i, t-1] + x[i, t-1] <= sd[i] + (pu[i] - sd[i]) * (1 - w[i, t]), name=f'SR2_{i}_{t}')

production_cost = pulp.lpSum(cp[i] * (pl[i] * z[i, t] + x[i, t]) for i, t in x_keys)
startup_cost = pulp.lpSum(cu[i] * y[i, t] for i, t in y_keys)
shutdown_cost = pulp.lpSum(cd[i] * w[i, t] for i, t in w_keys)
mdl.setObjective(production_cost + startup_cost + shutdown_cost)

status_code = mdl.solve(pulp.PULP_CBC_CMD(gapRel=0.001, timeLimit=60))
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    print(f'Production Cost: {production_cost.value()}')
    print(f'Startup Cost: {startup_cost.value()}')
    print(f'Shutdown Cost: {shutdown_cost.value()}')

    x_sol = [(i, t, d[t], pl[i] * z[i, t].value() + var.value()) for (i, t), var in x.items()]
    x_df = pd.DataFrame(x_sol, columns=['Generator ID', 'Period', 'Demand', 'Production'])

    y_sol = [(i, t, int(var.value())) for (i, t), var in y.items()]
    y_df = pd.DataFrame(y_sol, columns=['Generator ID', 'Period', 'Startup'])
    df = x_df.merge(y_df, on=['Generator ID', 'Period'], how='left')

    z_sol = [(i, t, int(var.value())) for (i, t), var in z.items()]
    z_df = pd.DataFrame(z_sol, columns=['Generator ID', 'Period', 'Status'])
    df = df.merge(z_df, on=['Generator ID', 'Period'], how='left')

    w_sol = [(i, t, int(var.value())) for (i, t), var in w.items()]
    w_df = pd.DataFrame(w_sol, columns=['Generator ID', 'Period', 'Shutdown'])
    df = df.merge(w_df, on=['Generator ID', 'Period'], how='left')

    df = df[['Period', 'Generator ID', 'Demand', 'Production', 'Startup', 'Status', 'Shutdown']]
    df.sort_values(['Period', 'Generator ID'], inplace=True)
    print(df.to_string(index=False))
else:
    print(f'Model is not optimal. Status: {status}')


