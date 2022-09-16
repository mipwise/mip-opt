import pulp

# Input data
# farms
I = ['F1', 'F2', 'F3']
# DCs
J = ['D1', 'D2']
# supplies
s = {'F1': 16, 'F2': 11, 'F3': 23}
# demands
d = {'D1': 20, 'D2': 25}
# costs
c = {('F1', 'D1'): 66, ('F2', 'D1'): 51, ('F3', 'D1'): 73,
     ('F1', 'D2'): 54, ('F2', 'D2'): 82, ('F3', 'D2'): 63}

# Define the model
mdl = pulp.LpProblem('SoyKing', sense=pulp.LpMinimize)

# Add variables
keys = [(i, j) for i in I for j in J]
x = pulp.LpVariable.dicts(indices=keys, cat=pulp.LpContinuous, lowBound=0, name='x')

# Add Constraints
for i in I:
    mdl.addConstraint(sum(x[i, j] for j in J) <= s[i], name=f's{i}')
for j in J:
    mdl.addConstraint(sum(x[i, j] for i in I) >= d[j], name=f'd{j}')

# Set the objective function
mdl.setObjective(sum(c[i, j] * x[i, j] for i, j in keys))

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: x[key].value() for key in keys}
print(f'Amount to produce = {x_sol}')
