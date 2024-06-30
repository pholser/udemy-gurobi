# Column Generation Basics

Consider LP:
min c^T * x
s.t. A_1 * x = b
x >= 0

Suppose A_1 has 10000 constraints and 50000 variables.
At any simplex method iteration, how many variables are basic?
--> 10000

Consider LP:
min c^T * x
s.t. A_2 * x = b
x >= 0

Suppose A_2 has 10000 constraints and 10^30 variables.
At any simplex method iteration, how many variables are basic?
--> 10000

Cutting stock problem:
1-d: Cut rectangles of smaller widths out of generic rectangles
(the "stock") with the same standard width.

Stock rolls: 100   100   100  ... 100
Product rolls: 17    31    38    45
Demand:        211   395   610   97

Cost of using any particular cut pattern is the same.

Choose a collection of cut patterns to apply to stock rolls so that
we can meet demand for the product rolls, using as few stock rolls
as possible.

e.g.
Cut pattern       Quantity    Demand
17 17 17 17 17       43         17: 211
31 31 31            132         31: 395
38 38               305         38: 610
45 45                49         45:  49
                    529

Wasteful, in that many rolls have a lot of leftovers.

Let's introduce and use a less wasteful pattern:

Cut pattern       Quantity                    Demand
17 17 17 17 17       43 --> 0                  17: 211 
31 31 31            132                        31: 395
38 38               305 --> 94  (305 - 211)    38: 610
45 45                49                        45: 49
38 38 17            211
                    529

Can start with a solution that works, then say ok, let's introduce a
less wasteful pattern and use it while reducing usage of more wasteful
patterns.

Need an algorithm to efficiently search for additional cut patterns
to add that will yield more savings -- where the resulting rolls
cut with the new pattern offset the need to use another pattern
on other rolls. Column generation helps here. It will find new patterns
such that the reduction in stock rolls it enables exceeds the
increased use of the new pattern.

min c^T * x
s.t. Ax = b   A = (A_B, A_N)
x >= 0

_c_j = c_j - c_B^T * A_B^(-1) * A_j
     = c_j - (c_B^T * A_B^(-1)) * A_j    // y^T in parens
     = c_j - c_B^T * (A_B^(-1) * A_j)    // _A_j in parens

The reduced cost calculation can be viewed in one of two ways.

* z_j = c_j - y^T * A_j, where y are the dual variables that solve
  the linear system y^T * A_B = c_B^T, and hence have values
  y^T = c_B^T * A_B^(-1)

* z_j = c_j - c_B^T * _A_j, where _A_j is the representation of A_j
  relative to the current basis A_B.
      = (cost of increasing variable j)
        -
        (adjustment to cost to reflect changes in basic variables)

So:

Cut pattern       Quantity     Change         Demand
17 17 17 17 17       0           -43           17: 211 
31 31 31            132            0           31: 395
38 38                94         -211           38: 610
45 45                49            0           45: 49
38 38 17            211            0
                    529

c_j = 211
In the case of the 38/38 pattern, A_B^(-1) * A_j = -211
In the case of the 17/17/17/17/17 pattern, A_B^(-1) * A_j = -43
for a total reduced cost of -43.

* n stock rolls of width W
* r product roll widths w_1, ..., w_r
* demand d_1, ... d_r for each product roll

Compact formulation:
Decision: x_ij = number of product rolls i cut from stock roll j
Decision: y_j = 1 if stock roll j is used, else 0

min sum[j in 1..n] { y_j }
s.t. sum[i in 1..r] { w_i * x_ij } <= W * y_j, j in 1..n
        // no stock roll width exceeded
     sum[j in 1..n] { x_ij } >= d_i, i in 1..r
        // satisfy demand for each type of product roll

What is n?
Need to look for solutions better than that obvious one that
uses fewer stock rolls.
sum[i in 1..r] { ceil(d_i / floor(W / w_i)) }

Compact, but weak formulation.
Consider the level of disconnect between the physical system of
a MIP formulation and its LP relaxation.
In the MIP formulation, individual cut patterns can result in
wasted material. That no longer holds in the LP formulation.
We can reassemble wasted material into product rolls at no cost.

Also, symmetry: Indexing of the product rolls is arbitrary and
interchangeable

Column generation:
Implicitly consider all feasible cut patterns and encode the number
of product rolls in each pattern. We can't explicitly enumerate
all possible encodings, but we can enumerate enough to create a
restricted master problem; then let the subproblem efficiently find
other good encoded cut patterns.

(5, 0, 0, 0) == 17, 17, 17, 17, 17

K = implicit set of all possible cut patterns
p_ij = number of product rolls of type i in pattern j

Decision: z_j = number of stock rolls cut in pattern j

min[j in K] { z_j }
s.t. p_ij * z_j >= d_i
z_j >= 0, integer

Each cut pattern is unique, so no symmetry as in previous formulation.

Let J be a way smaller subset of K.

Full master problem:
min sum[j in J] { z_j } + sum[j in K/J] { z_j }
s.t. sum[j in J] { p_ij * z_j } + sum[j in K/J] { p_ij * z_j } >= d_i
     z_j >= 0  (no integrality restriction)

Restricted master problem:
min sum[j in J] { z_j }
s.t. sum[j in J] { p_ij * z_j } >= d_i
     z_j >= 0

Now, automate the thought process that we used to find an improving
cut pattern.

We implicitly used the reduced cost computation:
c_j - (c_B^T * A_B^(-1)) * A_j

Subproblem:
(min 1 - y^T * p)        // 1 = cost of another roll
max y^T * p
s.t. sum[i in 1..r] { w_i * p_i } <= W
p >= 0, integer
// knapsack

The subproblem is an integer program with one variable per product
roll. It is a single-constraint knapsack problem that's easy(-er)
to solve. Its optimal solution comes from the implicit cut patterns
in the full master problem (i.e. a pattern we haven't already considered).
If that new pattern has a negative reduced cost, then the objective
of the restricted master problem will improve.

So, column generation:

* start with a restricted master problem (integrality relaxed)
* solve RMP, get yourself a y vector.
* Use the y vector to solve the subproblem; this yields a p_q,
  where q in K / J.
* Is y^T * p_q <= 1?
  * If yes --> optimal
  * If not --> J := J union { q }
    * Solve new RMP, etc.

When the best cut pattern no longer has a favorable reduced cost,
I have the optimal solution to the RMP, but then also the full
master problem. The optimality of the solution to the last RMP
implies that no more variables can be added to improve the objective
function further. Therefore, the solution to the last RMP is also
the optimal solution to the full master problem, as it represents
the best solution achievable with the given set of columns.

In essence, the column generation algorithm iteratively refines
the set of variables until no further improvement is possible,
at which point the solution to the last RMP is indeed the optimal
solution to the full master problem.

Column generation solves the full master problem, possibly with
fractional values for the variables. We need an integer number for
each pattern cut. But the fractional solution satisfies demand; so
a solution with each of these values rounded up also satisfies demand.
And, the optimal LP objective, rounded up, gives you a strong bound
on the best possible integer solution.


CRUD /api/v1/intrinsic_validations
    for the out-of-the-box intrinsic validations.
    edits to these become available to all customers.
    use with care. restrict usage to someone who knows what they're doing

CRUD /api/v1/standard_validations
    for the out-of-the-box standard validations.
    edits to these become available to all customers.
    use with care. restrict usage to someone who knows what they're doing.

CRUD /api/v1/{customer_schema}/intrinsic_validations
    customer-specific intrinsic validation alterations or additions.
    more than likely we only allow alterations, and only of the
    error level (no less severe than suspend_row)

CRUD /api/v1/{customer_schema}/standard_validations
    customer-specific standard validations and additions.

GET /api/v1/{customer_schema}/operative_intrinsic_validations
    merged set of intrinsic validations

GET /api/v1/{customer_schema}/operative_standard_validations
    merged set of standard validations
