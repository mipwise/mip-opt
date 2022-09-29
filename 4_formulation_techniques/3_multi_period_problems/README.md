# Multi-Period Problems
Very often we want to make decisions over a time horizon when decisions made 
for one time period may impact decisions for other periods. 

A good example are production problems where there is the option to hold 
inventory from one period to the next. The 
[Pastesian](https://www.mipwise.com/use-cases/pastesian) and the 
[Frisbee Square](https://www.mipwise.com/use-cases/frisbee-square) use cases 
illustrate this situation very well.

One thing that become apparent as soon as we start to solve these problems 
is that there is an underlying network where nodes are period in time and 
arcs are links between there period--it's typically helpful to picture that 
network when solving the problem. As a result, flow balance constraints 
always show up in the formulation of these problems.

Transportation problems, including routing, will often have a time component 
too. For example, when there are time windows to pick up or delivery. In 
this case, the underlying network spans in space and time.

------------------------------------------------------------------------------

In the next section, we will study scheduling problems.

### [Up][up] | [Back][back] | [Next][next] | [Help][help]

[up]: ../README.md
[back]: ../2_routing_problems/README.md
[next]: ../4_scheduling_problems/README.md
[help]: ../../0_help/README.md