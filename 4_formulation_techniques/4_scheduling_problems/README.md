# Scheduling Problems
Scheduling problems are also multi-period problems. What makes them special 
(and challenging) is that there are typically events that must happen in a 
specific sequence. Therefore, some people also call them *sequencing problems*.

For example, in machine scheduling, the goal is to decide when to start 
making each item and for how long to produce it. In sports scheduling, the 
goal is to decide when and where each event takes place. In nurse scheduling, 
the goal is to determine when each staff starts and ends their shift.

In some cases, it's appropriate to discretize the time horizon into time 
slots and assign events to them. For example, suppose that football matches can 
take place on Wednesday, Saturday, or Sunday over the next following three 
months and each team must play two away and two home games. This can be 
modeled as an assignment of teams to matches and matches to days using 
binary decision variables.

In some other cases, it's more appropriate to use continuous decision 
variables that determine the start time and duration of each event. For 
example, an electric power generator may be turned on at 10:23, turned off at 
11:45, turned on again at 1:12, and turned off at 1:56.

Let's get some practice starting with the 
[Voltwise](https://www.mipwise.com/use-cases/voltwise) use case. 

## Unit Commitment Problem
Production of electric power is a challenging yet very important 
optimization problem that is solved daily across the globe. It's all about 
scheduling the production of a set of electrical generators to match energy 
demand at a minimum cost. 

Different from most commodities, electric power can't be stored very 
efficiently. Therefore, all generators must work synchronously to 
accurately match the expected demand.

In addition, there may be multiple types of generators, each with 
different requirements and associated costs.

For example, turning on or off certain types of generators can be a very 
expensive process and may require multiple time periods. Additionally, 
switching off a generator may only be allowed after it's operating for a 
minimum number of time periods.

------------------------------------------------------------------------------

In the next section, we will study a list of abstract techniques that can be 
applied to many contexts.

### [Up][up] | [Back][back] | [Next][next] | [Help][help]

[up]: ../README.md
[back]: ../3_multi_period_problems/README.md
[next]: ../5_generalized_techniques/README.md
[help]: ../../0_help/README.md