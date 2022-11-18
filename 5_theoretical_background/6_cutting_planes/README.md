# Cutting Planes
Cutting planes (also called cuts or valid inequalities) are constraints that cut 
off solutions from the LP relaxation but don't violate any integer feasible 
solution. 

So these are redundant constraints in the sense that they are not required 
to define the set of feasible solution of the problem. Their role is to 
improve the dual bound and bring us closer to an optimal solution.

To illustrate the potential of cuts, we will revisit the Pastesian use case. 
Except that this time we will assume that there are multiple types of 
lasagnas and that a fixed cost (per type of lasagna) is charged when at least 
one lasagna is produced in a period.

Sample data is provided in the 
[data/pastesian_data.xlsx](data/pastesian_data.xlsx) worksheet and the 
formulation of this extended version of Pastesian is in the 
[formulations/pastesian_fixed_cost_formulation.ipynb](formulations/pastesian_fixed_cost_formulation.ipynb)
notebook.

------------------------------------------------------------------------------


### [Up][up] | [Back][back] | [Help][help]

[up]: ../README.md
[back]: ../5_branch_and_bound/README.md
[help]: ../../0_help/README.md