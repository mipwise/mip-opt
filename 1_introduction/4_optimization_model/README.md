# Optimization Model
Formulating the problem is just one step of the optimization process. After 
that, we need to implement the mathematical formulation and solve the 
problem. The result of this implementation  is what we call an *optimization 
model*, which can be thought as a translation of the formulation into a 
language that computers can understand. 

You might be wondering, if it's just an implementation of the formulation, 
why do we use the word "model" then? The modeling was already done with the 
formulation, right? Turns out that many aspects of the problem, including 
requirements, can be modeled during the implementation, by manipulating the
input data, for example. We will revisit this topic later.

So how do we write an optimization model? The answer to this question 
depends on many things, such as the class of the optimization problem, the 
programming language, and the optimization solver adopted.

## Optimization Solvers
While you could implement algorithms by yourself to solve your problems, 
there are compelling reasons to not do so.

Nowadays, there are professional implementations of all standard algorithms. 
They typically come in the form of a library of algorithms that work 
together to solve a whole class of problems. These libraries are often 
called *solvers* and they are accessible from multiple programming languages. 

Beating these professional implementations in terms of performance is not an 
easy task.

Some examples of solvers for LP and MILP include
[COIN-OR CBC][cbc], [CPLEX][cplex], [GLPK][glpk], and [Gurobi][gurobi].

Example of solvers for CP include
[CPLEX][cplex] and [Google CP solver][google_cp].

The solvers CBC, GLPK, and Google CP are open source while CPLEX and Gurobi 
are proprietary. And all of them are accessible via API from Python.

[cplex]: https://www.ibm.com/analytics/cplex-optimizer 
[gurobi]: https://www.gurobi.com/
[glpk]: https://en.wikipedia.org/wiki/GNU_Linear_Programming_Kit 
[cbc]: https://en.wikipedia.org/wiki/COIN-OR#CBC
[gecode]: https://www.gecode.org/
[google_cp]: https://developers.google.com/optimization/cp


------------------------------------------------------------------------------

Click **Next** to see how to use some of these solvers to solve
the TicTech problem.

### [Home][home] | [Back][back] | [Next][next] | [Help][help]

[home]: ../../README.md
[back]: ../3_classes_of_optimization/README.md
[next]: ../5_tictech_modeling/README.md
[help]: ../../0_help/README.md