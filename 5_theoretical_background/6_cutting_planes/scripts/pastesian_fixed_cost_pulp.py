import pulp
import pandas as pd
import os
import inspect
from itertools import chain, combinations


def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


def get_optimization_data(instance):
    path = f'../data/{instance}.xlsx'
    periods_df = pd.read_excel(os.path.join(_this_directory(), path), sheet_name='periods')
    demand_df = pd.read_excel(os.path.join(_this_directory(), path), sheet_name='demand')
    costs_df = pd.read_excel(os.path.join(_this_directory(), path), sheet_name='costs')

    I = list(set(demand_df['Lasagna Type ID']))
    T = list(set(periods_df['Period ID']))
    pc = dict(zip(zip(costs_df['Lasagna Type ID'], costs_df['Period ID']), costs_df['Production Cost']))
    ic = dict(zip(zip(costs_df['Lasagna Type ID'], costs_df['Period ID']), costs_df['Inventory Cost']))
    fc = dict(zip(zip(costs_df['Lasagna Type ID'], costs_df['Period ID']), costs_df['Fixed Cost']))
    d = dict(zip(zip(demand_df['Lasagna Type ID'], demand_df['Period ID']), demand_df['Demand']))
    pu = dict(zip(periods_df['Period ID'], periods_df['Production Capacity']))

    # Variables keys
    x_keys = list(d.keys())
    s_keys = list(d.keys())
    z_keys = list(d.keys())
    return I, T, pc, ic, fc, d, pu, x_keys, s_keys, z_keys


def solve(instance, cuts, relax):
    I, T, pc, ic, fc, d, pu, x_keys, s_keys, z_keys = get_optimization_data(instance)

    mdl = pulp.LpProblem('PastesianFixedCost', sense=pulp.LpMinimize)

    x = pulp.LpVariable.dicts(indices=x_keys, cat=pulp.LpContinuous, lowBound=0, name='x')
    s = pulp.LpVariable.dicts(indices=s_keys, cat=pulp.LpContinuous, lowBound=0, name='s')
    if relax:
        z = pulp.LpVariable.dicts(indices=z_keys, cat=pulp.LpContinuous, lowBound=0, upBound=1, name='z')
    else:
        z = pulp.LpVariable.dicts(indices=z_keys, cat=pulp.LpBinary, name='z')

    # C1) Flow balance constraint for Period  𝑡 :
    for i, t in x_keys:
        mdl.addConstraint(s.get((i, t-1), 0) + x[i, t] == d[i, t] + s[i, t], name=f'C1_{i}_{t}')

    # Production capacity of Period  𝑡 :
    for t in T:
        mdl.addConstraint(pulp.lpSum(x[i, t] for i in I) <= pu[t], name=f'C2_{t}')

    # C3) If lasagnas of Type  𝑖  are produced in Period  𝑡 , then  𝑧𝑖𝑡  equals  1 :
    for i, t in x_keys:
        mdl.addConstraint(x[i, t] <= pu[t] * z[i, t], name=f'C3_{i}_{t}')

    # VI) Valid inequalities derived from this paper: https://pubsonline.informs.org/doi/epdf/10.1287/mnsc.30.10.1255)
    if cuts:  # this code needs to be optimized
        dd = {(i, t1, t2): sum(d[i, t] for t in T if t1 <= t <= t2) for t1 in T for t2 in T if t1 <= t2 for i in I}
        dd.update({(i, t2, t1): sum(d[i, t] for t in T if t1 <= t <= t2) for t1 in T for t2 in T if t1 <= t2 for i in I})
        for i in I:
            for l in T:
                L = T[:l+1]
                for k, S in enumerate(powerset(L)):
                    if len(S) <= 4:  # Limiting the size of S because there can be too many!
                        mdl.addConstraint(
                            pulp.lpSum(x[i, t] for t in S) +
                            pulp.lpSum(dd[i, t, l] * z[i, t] for t in L if (t not in S)) >= dd[i, 1, l],
                            name=f'VI_{i}_{l}_{k}')

    production_cost = pulp.lpSum(pc[i, t] * x[i, t] for i, t in x_keys)
    inventory_cost = pulp.lpSum(ic[i, t] * s[i, t] for i, t in s_keys)
    fixed_cost = pulp.lpSum(fc[i, t] * z[i, t] for i, t in z_keys)
    mdl.setObjective(production_cost + inventory_cost + fixed_cost)

    status_code = mdl.solve()
    status = pulp.LpStatus[status_code]
    if status == 'Optimal':
        print(f'Optimal solution found!')
        x_sol = [(i, t, var.value(), d[i, t], z[i, t].value(), z[i, t].value() * fc[i, t]) for (i, t), var in x.items()]
        s_sol = [(i, t, var.value()) for (i, t), var in s.items() if var.value() > 1e-4]
        x_df = pd.DataFrame(x_sol, columns=['Lasagna Type ID', 'Period ID', 'Produced', 'Demand', 'z', 'Fixed Cost'])
        s_df = pd.DataFrame(s_sol, columns=['Lasagna Type ID', 'Period ID', 'Stored'])
        df = x_df.merge(s_df, on=['Lasagna Type ID', 'Period ID'], how='outer')
        df['Stored'] = df['Stored'].fillna(0.0)
        df.sort_values(['Lasagna Type ID', 'Period ID'], inplace=True)
        df = df[['Lasagna Type ID', 'Period ID', 'Produced', 'Demand', 'Stored', 'Fixed Cost', 'z']]
        print(df.to_string(index=False))
    else:
        print(f'Model is not optimal. Status: {status}')


if __name__ == '__main__':
    solve(instance='pastesian_data', cuts=True, relax=True)
