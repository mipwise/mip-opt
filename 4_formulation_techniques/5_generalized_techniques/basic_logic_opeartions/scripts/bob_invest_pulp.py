import pulp
import pandas as pd


# allocations
a = {1: 16.00, 2: 22.00, 3: 18.00, 4: 10.00, 5: 31.00, 6: 38.00}
# returns (ROI)
r = {1: 4.2, 2: 3.1, 3: 4.0, 4: 4.8, 5: 2.5, 6: 3.9}
# budget
b = 100

I = list(a.keys())

mdl = pulp.LpProblem('BobInvest', sense=pulp.LpMaximize)

x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpBinary, name='x')

# C1) Total budget:
mdl.addConstraint(pulp.lpSum(a[i] * x[i] for i in I) <= b, name=f'C1')

# C2) If Bob invests in Portfolio 1, then he can't invest in Portfolio 2:
mdl.addConstraint(x[1] <= 1 - x[2], name=f'C2')

# C3) If Bob invests in Portfolio 4, then he must invest in Portfolio 1:
mdl.addConstraint(x[4] <= x[1], name=f'C3')

# C4) Bob must invest in either Portfolio 3 and 4 or neither:
mdl.addConstraint(x[3] == x[4], name=f'C4')

# C5) Bob must either invest in at least one of Portfolio 2 and 5 or in at least two of Portfolio 2, 4, and 5:
z1 = pulp.LpVariable(cat=pulp.LpBinary, name='z1')
mdl.addConstraint(x[2] + x[5] <= 2*z1, name=f'C5a1')
mdl.addConstraint(z1 <= x[2] + x[5], name=f'C5a2')
z2 = pulp.LpVariable(cat=pulp.LpBinary, name='z2')
mdl.addConstraint(x[2] + x[4] + x[5] - 1 <= 2*z2, name=f'C5b1')
mdl.addConstraint(2*z2 <= x[2] + x[4] + x[5], name=f'C5b2')
mdl.addConstraint(z1 + z2 == 1, name=f'C5C')

profit = pulp.lpSum((1 + r[i] / 100) * a[i] * x[i] for i in I) - pulp.lpSum(a[i] * x[i] for i in I)
mdl.setObjective(profit)

status_code = mdl.solve()
status = pulp.LpStatus[status_code]
if status == 'Optimal':
    print(f'Optimal solution found!')
    x_sol = [(i, a[i], (r[i] / 100) * a[i] * var.value()) for i, var in x.items() if var.value() > 0.5]
    x_df = pd.DataFrame(x_sol, columns=['Portfolio ID', 'Allocation', 'Return'])
    x_df['Return'] = x_df['Return'].round(2)
    x_df.sort_values('Portfolio ID', inplace=True)
    print(x_df.to_string(index=False))
    print([z1.value(), z2.value()])
else:
    print(f'Model is not optimal. Status: {status}')
