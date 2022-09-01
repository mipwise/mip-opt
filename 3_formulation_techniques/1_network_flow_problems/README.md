# Network Flow Problems
Many real-world problems can be modeled as a network flow problem. Here are 
a few examples:
- What is the shortest path to drive from work to home?
- What is the most economical way for the courier to deliver a package you 
  shipped to a friend that lives in another state?
- What is the maximum amount of data that can be transferred through a given 
  communication network?

One thing in common among these problems is that they all have an 
underlying network, i.e., a set of nodes and a set of arcs that connect 
these nodes. And the goal is to optimally move something through this network.

Here is a simple example to start with:
[SoyKing](https://www.mipwise.com/use-cases/soyking).

The network in the case of the SoyKing problem is composed by five nodes and 
six arcs. One thing to notice is that some nodes are **sources** (origin of flow)
and some are **sink** (destination of flow).

Many network flow problems, however, have a third type of node called 
**intermediate** nodes.

Let's see an example.

## MipEx
MipEx is a courier company that operates on the following network:

![MipEx](docs/MipEx.png)

The transit distance, transit time, transportation cost, and the maximum 
number of trucks that can travel on each arc in a day are given in the 
[Transportation Lanes](data/transportation_lanes.csv) table.

### Shortest Path
What's the fastest way for MipEx to ship a package from Station 1 to Station 5?

### Min Cost
MipEx now needs to ship 3 trucks from Station 1 and 4 trucks 
from Station 3 to Station 5.

What's the most economical way for MipEx to ship the orders without exceeding 
the maximum number of available trucks on each lane?

### Max Flow
What is the maximum number of trucks that MipEx can ship from Station 1 and 
3 to Station 5 in a single day?

What is the maximum number of trucks that MipEx can ship from Station 1, 2 
and 3 to Station 5 and 4 in a single day?

### Multi-Commodities Flow
MipEx now needs to ship 3 trucks of a commodity from Station 1 to Station 5 
and 4 trucks of a different commodity from Station 3 to Station 4.

In addition, the commodities that go from Station 1 to Station 5 
require a special type of truck that increases the transportation cost by 
20%.

What's the most economical way for MipEx to ship the orders without exceeding 
the maximum number of available trucks?

The [Commodities](data/commodities.csv) table contains the relevant data to 
solve this problem.

------------------------------------------------------------------------------

In the next section, we will study routing problems.

### [Up][up] | [Back][back] | [Next][next] | [Help][help]

[up]: ../README.md
[back]: ../0_formulation_template/README.md
[next]: ../2_routing_problems/README.md
[help]: ../../0_help/README.md