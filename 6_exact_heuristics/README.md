# Exact Heuristics
The literature is packed with publications of comprehensive formulations 
that address all relevant aspects of a given problem and methodologies to 
tackle these problems. 

However, in many of such publications, the authors don't report any 
computational experiments. And when they do, it's typically on a toy version 
of the problem, i.e., on a very small data instance.

This situation contrasts with the following quote taken from the book 
[Robust Optimization](https://www2.isye.gatech.edu/~nemirovs/FullBookDec11.pdf)
by Ben-Tal, El Ghaoui, Nemirovski.
> "After all, what is the point in reducing something to an optimization 
> problem that we do not know how to process computationally?" 

What determines whether a particular problem is tracktable or not is a 
combination of the formulation and the methodology adopted to solve the problem.
That's why we included this module in the program.

Specifically, in this module, we study several methodologies that has been 
proven effective for solving challenging real-world optimization problems 
from a variety of domains.

These are fairly generic strategies, but we don't expect you to use them 
exactly as they are presented. The key ingredient should be creativity. So 
to sparkle more creativity, we will present a bunch of practical examples 
rather than spending a lot of time talking about theory.  


- [Set Covering Formulations](set_covering_formulations/README.md)
- [Direct Acyclic Graphs](direct_acyclic_graph/README.md)
- [Decompositions](decompositions/README.md)
- [Smart Restrictions](smart_restrictions/README.md)
- [Callbacks](callbacks/README.md)

------------------------------------------------------------------------------

### [Home][home] | [Help][help]

[home]: ../README.md
[help]: ../0_help/README.md