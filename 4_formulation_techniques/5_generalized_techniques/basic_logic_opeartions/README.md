# Basic Logic Operations
There are many logic operations, such as "if-them" and "either-or", that are 
often required to model real-world situations. We will study some of them in 
this session.

Let's start with an artificial problem to get started.

## Bob Invest
Bob wants to invest $100, and he got six portfolios to chose from:

| Portfolio ID | Allocation ($) | ROI (%) |
|--------------|----------------|---------|
| 1            | 16.00          | 4.2     |
| 2            | 22.00          | 3.1     |
| 3            | 18.00          | 4.0     |
| 4            | 10.00          | 4.8     |
| 5            | 31.00          | 2.5     |
| 6            | 38.00          | 3.9     |

How can Bob allocate his budget to maximize his profit?

Now consider the following additional conditions:
1) If Bob invests in Portfolio 1, then he can't invest in Portfolio 2.
2) If Bob invests in Portfolio 4, then he must invest in Portfolio 1.
3) Bob must invest in either Portfolio 3 and 4 or neither.
4) Bob must either invest in at least one of Portfolio 2 and 5 or in at 
   least two of Portfolio 2, 4, and 5.

How does the total return decrease as we account for each additional 
constraint?

------------------------------------------------------------------------------


### [Up][up] | [Help][help]

[up]: ../README.md
[help]: ../../../0_help/README.md