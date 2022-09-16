import pulp

# Input data
# time periods
T = [1, 2, 3, 4]
# production cost
c = {1: 5.50, 2: 7.20, 3: 8.80, 4: 10.90}
# inventory holding cost
h = {1: 1.30, 2: 1.95, 3: 2.20, 4: 0.0}
# demands
d = {1: 200, 2: 350, 3: 150, 4: 250}
# opening inventory
oi = 50

# Define the model
mdl = pulp.LpProblem('Pastesian', sense=pulp.LpMinimize)

# Add variables
x = pulp.LpVariable.dicts(indices=T, cat=pulp.LpContinuous, lowBound=0, name='x')
s = pulp.LpVariable.dicts(indices=T, cat=pulp.LpContinuous, lowBound=0, name='s')

# Add Constraints
mdl.addConstraint(oi + x[1] == d[1] + s[1], name='c1')
for t in T[1:]:
    mdl.addConstraint(s[t - 1] + x[t] == d[t] + s[t], name=f'c2_{t}')
# no inventory after the last period
s[T[-1]].upBound = 0

# Set the objective function
mdl.setObjective(pulp.lpSum(c[t] * x[t] + h[t] * s[t] for t in T))

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {t: x[t].value() for t in T}
s_sol = {t: s[t].value() for t in T[:-1]}
print(f'Amount to produce = {x_sol}')
print(f'Amount to store = {s_sol}')
