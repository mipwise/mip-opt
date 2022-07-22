# TicTech Modeling
Following are three optimization models for the TicTech formulation
that we saw in a previous section. They are all written in Python.

Here is the formulation of the TicTech problem for your reference:
```text
max 12*x_1 + 17*x_2 + 25*x_3
s.t.    x_1 + x_2 + x_3 = 1
        x_1, x_2, x_3 in {0, 1}
```

To solve any of the model below, just copy and paste the code into a Python 
script and execute it (of course, you may have to install the corresponding 
packages). But don't get hung up on these examples as we will learn much 
more about model building in subsequent sections.

## Gurobi model
We can use Gurobi in Python through the package `gurobipy`.

```python
import gurobipy as gp

# Define the model
mdl = gp.Model('TicTech')

# Add variables
x = mdl.addVars([1, 2, 3], vtype=gp.GRB.BINARY, name='x')

# Add Constraints
mdl.addConstr(x[1] + x[2] + x[3] == 1, name='one_tech')

# Set the objective function
mdl.setObjective(12 * x[1] + 17 * x[2] + 25 * x[3], sense=gp.GRB.MAXIMIZE)

# Optimize
mdl.optimize()

# Retrieve the solution
x_sol = {i: x[i].X for i in [1, 2, 3]}
print(f'x = {x_sol}')
```

## CPLEX model
We can use CPLEX in Python through the package `docplex`.
```python
import docplex.mp.model as cpl

# Define the model
mdl = cpl.Model('TicTech')

# Add variables
x = mdl.var_dict(keys=[1, 2, 3], vartype=mdl.binary_vartype, name='x')

# Add Constraints
mdl.add_constraint(x[1] + x[2] + x[3] == 1, ctname='one_tech')

# Set the objective function
mdl.maximize(12 * x[1] + 17 * x[2] + 25 * x[3])

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {i: x[i].solution_value for i in [1, 2, 3]}
print(f'x = {x_sol}')
```

## PuLP model
We can use CBC in Python through the package `pulp`.
Like CBC, [PuLP] is also part of the [COIN-OR][coin-or] project.
But it's important to notice that PuLP itself is not a solver, it's a modeling 
language for optimization in Python from which you can call [several
solvers][pulp_solvers].

```python
import pulp

# Define the model
mdl = pulp.LpProblem('TicTech', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indices=[1, 2, 3], cat=pulp.LpBinary, lowBound=0, name='x')

# Add Constraints
mdl.addConstraint(x[1] + x[2] + x[3] == 1, name='one_tech')

# Set the objective function
mdl.setObjective(12 * x[1] + 17 * x[2] + 25 * x[3])

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {i: x[i].value() for i in [1, 2, 3]}
print(f'x = {x_sol}')
```

Note that older version of the `pulp` package use to use `indexs` instead of 
`indices` as an argument name in the `pulp.LpVariable.dicts` method.

[coin-or]: https://www.coin-or.org/
[pulp_solvers]: https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html

------------------------------------------------------------------------------

Click **Next** to see how to formulate and solve another small problem.

### [Home][home] | [Back][back] | [Next][next] | [Help][help]

[home]: ../../README.md
[back]: ../4_optimization_model/README.md
[next]: ../next_steps/README.md
[help]: ../../0_help/README.md