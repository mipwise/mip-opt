# Data Agnostic
You may have noticed that we have explicitly used the given 
data instance in some formulations and implementations studied so far.

For example, in the [TicTech][tictech] problem
we see the numbers 1, 2, and 3 (which we used to identify the three
technologies) being explicitly used to define the decision variables,
constraints, and objective function.

However, **using explicit data to formulate and implement models is NOT 
a good practice**, even more so when it comes to solving real-world 
problems. The only reason we still use explicit data here and there is to avoid 
introducing too much abstraction at once, i.e., for didactic reasons.

As you get more familiar with the process of writing formulations and 
implementing models, you should shift towards a more professional style.

## Motivation
Let's consider the [SoyKing][soyking] problem for a moment. In the instance 
provided with the statement, there were only 3 farms and 2 distribution 
centers (DCs). As a result, we had 6 decision variables and 5 constraints. 
If we had 10 farms and 5 DCs, we would have had 50 decision variables and 15 
constraints, which would be quite boring to type down. 

Imagine that right after looking at the results, your client tells you 
that there are now a few new farms to be considered and the demands have 
changed a bit. Further, imagine that even before you are done updating your 
formulation and model, your client sends you an updated costs table!

A situation like this would be a nightmare, and it will surely
happen in the real world if you formulate and implement the model 
as a function of a given data instance!

## Writing data agnostic formulations
The way to avoid the inefficiency described above is to abstract the data 
by defining **collections of indices and parameters**.

Going back to the [SoyKing][soyking] problem, we need to define 
a collection of farms and a collection of DCs. Then we can define parameters to 
represent supply, demand, and transportation costs accordingly.

The formulation itself can be completely data agnostic. And once 
such formulation is implemented as an optimization model, we
can populate these indices and parameters with actual data from a given
instance of the problem and solve it. We can then repeat this for
multiple instances of the problem without having to modify the formulation
or the optimization model at all. That is the target!

To see some practical examples, have a look at the data agnostic formulation 
of the TicTech and other problems in the respective Jupyter Notebooks
located inside the [jupyter_notebooks](jupyter_notebooks) directory.

## Implementation of the data agnostic formulation
Below is an implementation of the data agnostic formulation of TicTech.
As you can see, the input data is completely apart from the model. 
In fact, this data could even be loaded from a file, such as a JSON or a CSV 
file. That's precisely what typically happens in real-life applications, and we 
will transition into that style as we move along.

```python
import pulp

# Input data
# technologies
I = {'T1', 'T2', 'T3'}
# scores
s = {'T1': 12, 'T2': 17, 'T3': 25}

# Define the model
mdl = pulp.LpProblem('TicTech', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indices=I, cat=pulp.LpBinary, name='x')

# Add Constraints
mdl.addConstraint(sum(x[i] for i in I) == 1, name='c1')

# Set the objective function
mdl.setObjective(sum(s[i] * x[i] for i in I))

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {i: x[i].value() for i in I}
print(f'x = {x_sol}')
```

For more examples, check out 
[soyking_pro_pulp.py](scripts/soyking_pro_pulp.py) and
[pastesian_pro_pulp.py](scripts/pastesian_pro_pulp.py)
located inside the [scripts](scripts) directory.

## Using IDs instead of business names
You may have noticed that we used IDs instead of business names in the "pro"
implementations. The reason for that is mainly *performance*. Of course, it 
would not make any difference for these little instances. But for large 
instances, depending on which solver and API you are using,
having lengthy strings as indices can seriously compromise performance
when loading and solving the optimization model.

In the case of time periods, like in the Pastesian problem, we not only use
IDs as we also make sure they are contiguous integers starting from 1,
because we typically use these assumptions as part of the modeling.

[tictech]: ../../1_introduction/2_tictech_formulation/README.md
[soyking]: https://www.mipwise.com/use-cases/soyking

------------------------------------------------------------------------------

Click **Next** to continue.

### [Home][home] | [Back][back] | [Next][next] | [Help][help]

[home]: ../../README.md
[back]: ../README.md
[next]: ../2_formulation_template/README.md
[help]: ../../0_help/README.md






