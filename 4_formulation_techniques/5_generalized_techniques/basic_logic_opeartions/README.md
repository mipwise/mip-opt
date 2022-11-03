# Basic Logic Operations
There are many logic operations, such as "if-them" and "either-or", that are 
often required to model real-world situations. We will study some of them in 
this session.

As usual, let's go with examples!

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

## SoyKing
The original SoyKing problem is on the Mip Wise website: 
https://www.mipwise.com/use-cases/soyking

But here we will consider a slightly larger instance and additional 
requirements.

The input data is available from [this worksheet](docs/soyking_data.xlsx).

The additional requirements are the following:
 
1) If a given Farm decides to serve a given DC, then it must fulfill at 
   least 20% of its demand.
2) SoyKing does not have to meet the demand of all DCs in full. But for each 
   ton of soy demanded and not supplied, SoyKing pays a penalty as provided 
   in the "Not Supplying Penalty" column of the "demands" table.
3) At least four DCs must have its demand met in full.
4) At least three of the following DCs must have at least 75% of its demand 
   met: D3, D4, D7, and D8.
5) If D4 receives at least 60% of its demand, then D2 and D6 must both 
   receive at least 60% of its demand as well.


## Generic Requirements
Now that we have seen how the need to model logic operations show up in 
practical setting, it's a good idea to have summary of them for quick 
reference in the future.

The [logical_constraints.ipynb](formulations/logical_constraints.ipynb) 
notebook contains several generic implementations that you can use and 
customize to better fit in your toolbox. 




------------------------------------------------------------------------------


### [Up][up] | [Help][help]

[up]: ../README.md
[help]: ../../../0_help/README.md