### **OBS: This program is under construction and many sections/modules are just placeholders for now.**

If you have any question or comment, please 
[Reach out](https://www.mipwise.com/contact) to us.

# Mip Optimization

Welcome to the **Mip Optimization** program!

Mathematical optimization is an outstanding technology to solve 
decision-making problems. Here is a quote taken from the preface of the online 
book [Optimization Models][optimization_modes_book] by Fabio Schoen that 
summarizes it very well: 

>"Having the possibility of learning from data so that future trends (demand,
production, yield, interest rates, …) can be reliably and robustly estimated 
is absolutely wonderful. However, after a reliable forecast becomes 
available, managers still need to take decisions. And this is where 
optimization (operations research) comes into play."

Before you move forward, we recommend that you read the following article to 
get some more context on what is waiting for you in the program:
https://www.mipwise.com/technical-articles/math-optimization

[optimization_modes_book]: https://webgol.dinfo.unifi.it/OptimizationModels/contents.html

### [Next][next] | [Help][help]

[next]: 1_introduction/README.md
[help]: 0_help/README.md

---

### References
Here is a list of books for those wanting to take a deeper dive in specific 
operations research topics:

- **Operations Research: Applications and Algorithms**; Wayne L. Winston
- **Integer and Combinatorial Optimization**; George Nemhauser, Laurence Wolsey
- **Linear Optimization and Duality: A Modern Exposition**; Craig A. Tovey
- **Integer Programming**; Michele Conforti, Gérard Cornuéjols, Giacomo Zambelli


### License
The content of Mip Optimization is licensed under the [GNU GPLv3](LICENSE) 
license.

Contributions and constructive feedback are very welcome. 
Please [Reach out](https://www.mipwise.com/contact) to us.

### Table of Content
- [Help](./0_help/README.md)
- [Introduction](./1_introduction/README.md)
	- [Mathematical Formulation](./1_introduction/1_mathematical_formulation/README.md)
	- [Tictech Formulation](./1_introduction/2_tictech_formulation/README.md)
	- [Classes of Optimization](./1_introduction/3_classes_of_optimization/README.md)
	- [Optimization Model](./1_introduction/4_optimization_model/README.md)
	- [Tictech Modeling](./1_introduction/5_tictech_modeling/README.md)
	- [Next Steps](./1_introduction/next_steps/README.md)
- [Beginner Examples](./2_beginner_examples/README.md)
- [Best Practices](./3_best_practices/README.md)
	- [Data Agnostic](./3_best_practices/1_data_agnostic/README.md)
		- jupyter_notebooks
	- [Formulation Template](./3_best_practices/2_formulation_template/README.md)
- [Formulation Techniques](./4_formulation_techniques/README.md)
	- [Network Flow Problems](./4_formulation_techniques/1_network_flow_problems/README.md)
		- data
		- docs
		- formulations
	- [Routing Problems](./4_formulation_techniques/2_routing_problems/README.md)
		- data
			- tsp
			- woodler
		- docs
		- formulations
	- [Multi Period Problems](./4_formulation_techniques/3_multi_period_problems/README.md)
		- data
		- docs
		- formulations
	- [Scheduling Problems](./4_formulation_techniques/4_scheduling_problems/README.md)
		- data
			- ucp_data_3_generators
		- docs
		- formulations
	- [Generalized Techniques](./4_formulation_techniques/5_generalized_techniques/README.md)
		- [Absolute Values](./4_formulation_techniques/5_generalized_techniques/absolute_values/README.md)
		- [Basic Logic Opeartions](./4_formulation_techniques/5_generalized_techniques/basic_logic_opeartions/README.md)
			- docs
			- formulations
		- [Disjunctions](./4_formulation_techniques/5_generalized_techniques/disjunctions/README.md)
		- [Fixed Charge](./4_formulation_techniques/5_generalized_techniques/fixed_charge/README.md)
		- [Knapsack Problem](./4_formulation_techniques/5_generalized_techniques/knapsack_problem/README.md)
		- [Min Max](./4_formulation_techniques/5_generalized_techniques/min_max/README.md)
		- [Packing Covering Partitioning](./4_formulation_techniques/5_generalized_techniques/packing_covering_partitioning/README.md)
		- [Piecewise Linear Functions](./4_formulation_techniques/5_generalized_techniques/piecewise_linear_functions/README.md)
- [Theoretical Background](./5_theoretical_background/README.md)
	- [Solving Integer Programs](./5_theoretical_background/1_solving_integer_programs/README.md)
		- docs
	- [The Simplex Algorithm](./5_theoretical_background/2_the_simplex_algorithm/README.md)
	- [LP Duality](./5_theoretical_background/3_lp_duality/README.md)
	- [Sensitivity Analysis](./5_theoretical_background/4_sensitivity_analysis/README.md)
	- [Branch and Bound](./5_theoretical_background/5_branch_and_bound/README.md)
	- [Cutting Planes](./5_theoretical_background/6_cutting_planes/README.md)
		- data
		- formulations
- [Handling Performance Issues](./6_handling_performance_issues/README.md)
	- [Concurrent LP Solvers](./6_handling_performance_issues/concurrent_lp_solvers/README.md)
	- [Infeasible Models](./6_handling_performance_issues/infeasible_models/README.md)
	- [Integer Vs Binary Variables](./6_handling_performance_issues/integer_vs_binary_variables/README.md)
	- [Interpreting The Solver Log](./6_handling_performance_issues/interpreting_the_solver_log/README.md)
	- [Memory Issues](./6_handling_performance_issues/memory_issues/README.md)
	- [Numerical Issues](./6_handling_performance_issues/numerical_issues/README.md)
	- [Parameters Tuning](./6_handling_performance_issues/parameters_tuning/README.md)
	- [Primal Vs Dual Bound](./6_handling_performance_issues/primal_vs_dual_bound/README.md)
	- [Reformulations](./6_handling_performance_issues/reformulations/README.md)
	- [Symmetry](./6_handling_performance_issues/symmetry/README.md)
	- [Warm Starting](./6_handling_performance_issues/warm_starting/README.md)
- [Exact Heuristics](./7_exact_heuristics/README.md)
	- [Callbacks](./7_exact_heuristics/callbacks/README.md)
	- [Decompositions](./7_exact_heuristics/decompositions/README.md)
	- [Direct Acyclic Graph](./7_exact_heuristics/direct_acyclic_graph/README.md)
	- [Set Covering Formulations](./7_exact_heuristics/set_covering_formulations/README.md)
	- [Smart Restrictions](./7_exact_heuristics/smart_restrictions/README.md)
- miscellaneous
	- [Docs](./miscellaneous/docs/README.md)
	- notebooks