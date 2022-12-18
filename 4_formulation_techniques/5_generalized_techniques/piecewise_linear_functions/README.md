# Piecewise Linear Functions
Quite often we encounter applications where the objective function or 
certain constraints can't be captured with just a linear expression. One 
example of this is the pricing structure of the 
[ProJeans](https://www.mipwise.com/use-cases/projeans) use case.

Specifically, suppliers offer discounts that depend on the order size. This 
is called economy of scale, the more you order, the higher the discount. 

The figure below abstract that idea. The x-axis is the order quantity and 
the y-axis is the total cost of the order. You can think of the first 
breakpoint, a1, as the minimum order quantity (MOQ) and the last breakpoint, 
a4, as the size of the largest order that one can place to this supplier.

![fig](docs/piecewise_linear.png)

As you can see, the function is linear between any two consecutive breakpoints.
Bt overall, it's not linear. Therefore, it's called a _piecewise linear 
function_.

To model piecewise linear functions, we need to introduce auxiliary 
decision variables, including one binary variable for each interval.  

------------------------------------------------------------------------------


### [Up][up] | [Help][help]

[up]: ../README.md
[help]: ../../../0_help/README.md