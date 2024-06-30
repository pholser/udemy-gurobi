Modeling notes:
=====
Mathematical optimization: a framework for stating and solving
optimization problems.

e.g.
* max sum[i in I] { sum[j in J] { c_ij * x_ij } }
subject to:
  * sum[i in I] { x_ij } <= 1  forall j in J
  * sum[j in J] { x_ij } <= 1  forall i in I
  * x_ij in {0, 1}  forall i in I, j in J

Model components:
* Decision variables: represent choices to be made
* Objective function: function of the decision variables, to optimize
* Constraints: how is the system defined, what are its limits?
* Data/parameters: what you already know

e.g. museum heist
* several unique items of varying weights worth different amounts to steal
* backpack of certain carrying (weight) capacity to stash items in
Which objects to take?

* decisions: should I take this item?
* constraints: weights of items in the backpack respect capacity
* objective: maximize the value of the items taken

Decision: Let x_1, x_2, ..., x_i be 1 if we take item i, 0 else.
Parameter: Let w_1, w_2, ..., w_i be the weights of items.
Parameter: Let v_1, v_2, ..., v_i be the values of items.
Parameter: Let I = {1, 2, ..., i} be the set of items.
Parameter: Let C be the capacity of the backpack.

Then:
max sum[i in I] { v_i * x_i }
subject to: sum[i in I] { w_i * x_i } <= C
x_i in {0, 1} forall i in I

e.g. MLB
* National League 15 teams
* American League 15 teams
* 162 games in a season for every team over six months
  ... 2430 games per season
* # of home games ~~ $ of away games over the season
* # of home games ~~ $ of away games over the weekends in a month
* Games are played in series: 3-4 consecutive games with the same team
* 2-3 consecutive series for a homestand
* Moderate traveling for away games
* Requirements for interleague games
* Rival matches (e.g. NYY vs. NYM, TEX vs. HOU)

How do MLB schedule their games?

Consider a reduced problem:
* Six teams {A, B, C, D, E, F}
* All teams play each other once at home and once away
* There are ten days
* Each team plays once a day
* Maximize total expected audience size

* Parameter: Let T be the set of teams.
* Parameter: Let R be the set of rounds [1..10]
* Decision: Let x[t, t', r] = 1 if team t hosts team t' in round r,
   t in T, t' in T, t != t', r in R
* Constraint: Each team plays once per round:
  sum[t' in T, t != t] { x[t, t', r] + x[t', t, r] } = 1
     forall t in T, r in R
* Constraint: x[t, t', r] in {0, 1} forall t, t' in T: t != t', r in R
* Constraint: Each team hosts each other team once:
  sum[r in R, t' in T:t != t'] { x[t, t', r] } = 1
     forall t in T
* Objective: Maximize number of expected viewers:
  max sum[t in T, t' in T : t != t', r in R] {
     v[t, t', r] * x[t, t', r]
  }

e.g. Burrito trucks optimization
* Parameter: Let J be the set of possible locations for burrito trucks
* Parameter: Let I be the set of buildings with potential customers
* Decision: Let x_j = 1 if a truck is placed at location j in J, else 0
* Decision: Let y_ij = 1 if a truck at location j in J serves location
  i in I
* Objective:
  max sum[i in I, j in J] { (r - k) * alpha_ij * d_i * y_ij }
      -
      sum[j in J] { f_j * x_j }
* Parameters:
  r: revenue, k: ingredient cost, alpha: demand multiplier, d: demand

Constraints:
* sum[j in J] { y_ij } <= 1  forall i in I  // at most 1 truck per customer
* y_ij <= x_j  forall i in I, j in J  // truck must be open to serve customer
* x_j, y_ij in {0, 1}  forall i in I, j in J


Python provides some data structures that are well-suited for deploying
optimization models: tuples, lists, sets, dictionaries

gurobipy also offers a few data structures that allow you to build subsets
from a collection of tuples efficiently:
* Tuplelists
* Tupledicts
* Multidicts

* tuple: ordered, compound grouping
  * cannot be modified once created
  * ideal for representing multi-dimensional subscripts
  * items indexed starting at 0
* list: ordered group; each item indexed (starting at 0)
  * can be modified by adding, deleting, or sorting elements
* set: unordered group; no repeated elements
  * can be modified by adding or deleting elements
* dictionary: mapping from keys to values
  * ideal for representing indexed data, e.g. cost, demand, capacity
  * typically, strings, numbers, and tuples are used as keys (hashable)
  * keys are to be unique within a dictionary

Gurobipy data structures:
* Tuplelist: extension of Python list to efficiently build sublists
  from a list of tuples
e.g.
   x = gp.tuplelist([
     ("d4", "t22"), ("d4", "t37"), ("d4", "truck53"), ("d22", "truck22")
   ])
   x.select("d4", "*")  # list of tuples with first component "d4"

* Tupledict: extension of Python dict for creating subsets of Gurobi
  variable objects. Keys of a tupledict are stored as a tuplelist, which
  enables the efficient creation of math expressions that contain a
  subset of matching variables, by using methods list select(), sum(),
  or prod().
e.g.
  assign = model.addVars(expertise, name="assign")  # gives a tupledict
  supply = model.addConstrs((assign.sum(r, "*") == 1 for r in resources))
    # also gives a tupledict

* Multidict: a convenience function to define multiple dictionaries
  (each with the same set of keys) and their indices in one statement.
  Input consists of a Python dict with lists of the same length as the
  values associated with the keys. The first output of this function is
  a tuplelist, and the rest are tupledicts.
e.g.
  bldg_truck_spot_pairs, distance, scaled_demand = gp.multidict({
    ("d4", "t11"): [112.7, 20],
    ("d4", "t10"): [149.3, 15],
    ("d22", "t11): [155.7, 10]
  })
  print(scaled_demand.sum("*", "t11"))  # 30

e.g.
  cities = ['A', 'B', 'C', 'D']
  routes = gp.tuplelist([
    ('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')
  ])

  for c in cities:
    print(routes.select(c, '*'))
  # --> [('A', 'B'), ('A', 'C')]
  # --> [('B', 'C'), ('B', 'D')]
  # --> [('C', 'D')]
  # --> []

Indexed variables: Model.addVars()
Using integers:
  x = model.addVars(2, 3, name="x")
  # x[0, 0], x[0, 1], x[0, 2], x[1, 0], x[1, 1], x[1, 2]
  # x is a tupledict

Using lists of scalars:
  y = model.addVars(cities, cities, name="y")
  # y[A, A], y[A, B], ..., y[D, C], y[D, D]

Using a tuplelist:
  z = model.addVars(routes, name="z")
  # z[A, B], ..., z[C, D]

Using a generator expression:
  w = model.addVars((i for i in range(5) if i != 2), name="w")
  # w[0], w[1], w[3], w[4]
  # w is a tupledict with indices as keys and variables as values

* Model.addVars() automatically takes the cross product of
  multiple indices
* addVars() call without provided "name", generates names automatically,
  using the indices

Indexed constraints: Model.addConstrs()
* Can use a generator expression to build constraints:
  e.g.
  x = model.addVars(routes, name="x")
  y = model.addVars(routes, name="y")
  cap = model.addConstrs(
    (x[i, j] + y[i, j] <= 2 for i, j in routes),
    name="capacity"
  )
  # gives a tupledict with route as key, constraint as value

Operators and Python:
* Linear and quadratic expressions are used in constraints
  and objective
  * Basic (binary) math operators +, -, *, /
  * Aggregate sum operator (sum())
    * Used alone as well as in dot-products

Aggregate sum: using tupledict.sum():
e.g.
x = model.addVars(3, 4, vtype=GRB.BINARY, name="x")
model.addConstrs(x.sum(i, "*") <= 1 for i in range(3))
  # x[0, 0] + x[0, 1] + x[0, 2] <= 1
  # x[1, 0] + x[1, 1] + x[1, 2] <= 1
  # x[2, 0] + x[2, 1] + x[2, 2] <= 1

Aggregate sum: using quicksum()
* Use generator expression inside a quicksum() call:
  e.g.
  obj = gp.quicksum(cost[i, j] * x[i, j] for i, j in routes)

* quicksum() works just like Python's sum() function, but is more
  efficient for optimization models.

A tupledict of variables has a prod() function to compute dot-products.
e.g. if `cost` is a dictionary, the following are equivalent:
  * obj = gp.quicksum(cost[i, j] * x[i, j] for i, j in arcs)
  * obj = x.prod(cost)

e.g.
  x = model.addVars([(1, 2), (1, 3), (2, 3)])
  coeff = dict([((1, 2), 2.0), ((1, 3), 2.1), ((2, 3), 3.3)])
  expr = x.prod(coeff)   # 2.0 * x[1, 2] + 2.1 * x[1, 3] + 3.3 * x[2, 3]
  expr = x.prod(coeff, "*", 3)   # 2.1 * x[1, 3] + 3.3 * x[2, 3]
    # gives LinExpr objects

Matrix API (since Gurobi 9.0):
* Support numpy's ndarray and scipy.sparse matrices as inputs
* More convenient if the underlying model is naturally expressed
  with matrices
* Faster, b/c no modeling objects created for individual linear exprs
* API offers two layers:
  * Add matrix constraints directly from the data:
    model.addMConstrs(A, x, sense, b)
  * Use matrix variable and constraint modeling objects:
    x = model.addMVar(shape)
    model.addConst(A @ x <= b)
  * Set a quadratic objective fn:
    model.setObjective(x @ Q @ x)

Advanced modeling features:
----
Range constraints:
e.g. L <= sum[i] { a_i * x_i } <= U

rewritten:
  r + sum[i] { a_i * x_i } = U
  0 <= r <= U - L

model.addRange(sum, L, U, "range0")

If you need to modify the range:
* Retrieve the additional range var, name `RgYourConstraintName`
* Modify the bounds on that var

For full control, it may be easier to model this yourself.
* Useful for efficient deactivation/reactivation of constraints
  in the model
  * Set infinite bounds to deactivate; restore to 0 and (U - L)
    to reactivate

Indicator variables and convexity:
Many advanced models are based on binary indicator variables
* represent whether or not a condition holds

Models with convext regions and convex functions are generally
much easier to solve.

Special ordered sets:
* Type 1: at most one variable in the set may be != 0 in a solution:
  SOS1(x_1, ..., x_n)
  * Any permutation of a feasible SOS solution is also feasible

* Type 2:
  * At most two variables in the set may be != 0 in a solution
  * Non-zero variables must be adjacent
  SOS2(x_1, ..., x_n)

Variables need not be integer.

Absolute value: convex case
Simply substitute if absolute value fn creates a convex model

min |x| s.t. linear constraints, some with x
x free
==>
min z
s.t. z = x_pos + x_neg
     x = x_pos - x_neg
     linear constraints, some with x
x free; z, x_pos, x_neg >= 0
# any optimal soln has either x_pos or x_neg = 0

Absolute value, non-convex case:
Use indicator variable and arbitrary big-M value to prevent both
x_pos and x_neg from being non-zero

max |x|
s.t. linear constraints, some with x
x free
==>
max z
s.t. z = x_pos + x_neg
x = x_pos - x_neg = (x_pos + delta) - (x_neg - delta)
x_pos <= My
x_neg <= M(1 - y)
y in {0, 1}
x free; z, x_pos, x_neg >= 0

Piecewise linear functions:
* generalization of absolute value fns
* convex case is "easy" -- fn represented by LP
* Non-convex case is more challenging
  * Function represented as MIP or SOS-2 constraints

Gurobi has an API for piecewise linear objectives and constraints
* Built-in algo support for the convex case (objective)
* Conversion to MIP is hidden from user

e.g.
* Fixed/tiered costs in manufacturing due to setup
* Economies of scale when discounts applied after buying in bulk
* Approximating non-linear functions
  * More pieces -> better approximation
  * trade-off between performance and exactness
* Unit commitment models in energy sector
* Pooling problem
* Trig/log functions

API: need only specify function breakpoints
  * no aux variables/constraints needed

model.setPWLObj(x, [1, 3, 5], [1, 2, 4])
model.addGenConstrPWL(x, y, x_pts, y_pts, "gc")

* x must be non-decreasing
* repeat x value for a jump or discontinuity

Under the hood:
let (x_i, y_i) represent the i'th point in piecewise linear fn
To represent y = f(x), use:
* x = sum[i] { lambda_i * x_i }
* y = sum[i] { lambda_i * y_i }
* sum[i] { lambda_i } = 1
* lambda_i >= 0, SOS2
SOS2 constraint is redundant if f is convex.

Min/max functions - convex case:
* It is easy to minimize the largest value, or maximize the smallest.
* min { max[i] { x_i } }  --> min z, s.t. z >= x_i, forall i
* Harder to minimize smallest value, or maximize largest value

* y = min { x_1, x_2, x_3 }  ==> addGenConstrMin(y, [x_1, x_2, x_3])
* y = max { x_1, x_2, x_3 }  ==> addGenConstrMax(y, [x_1, x_2, x_3])
* y = |x|  ==> addGenConstrAbs(y, x)

Logical conditions on binary variables:
* AND:
    x_1 = 1 and x_2 = 1   ==>  x_1 + x_2 = 2
* OR:
    x_1 = 1 or x_2 = 1    ==>  x_1 + x_2 >= 1
* XOR:
    x_1 = 1 xor x_2 = 1   ==>  x_1 + x_2 == 1
* At least/at most/counting:
    x_i = 1 for at least/most 3 i  ==> sum[i] { x_i } >= 3
* If-then (implication):
    if x_1 = 1 then x_2 = 1        ==> x_1 <= x_2

Logical conditions - variable result:
* AND:
    y = (x_1 = 1 and x_2 = 1)
    ==>
    y <= x_1
    y <= x_2
    y >= x_1 + x_2 - 1
* OR:
    y = (x_1 = 1 or x_2 = 1)
    ==>
    y >= x_1
    y >= x_2
    y <= x_1 + x_2
* XOR:
    y = (x_1 = 1 xor x_2 = 1)
    ==>
    y >= x_1 - x_2
    y >= x_2 - x_1
    y <= x_1 + x_2
    y <= 2 - x_1 - x_2

General constraints for logical expressions:
* addGenConstrAnd(y, [x_1, x_2])
* addGenConstrOr(y, [x_1, x_2])

Logical conditions on constraints:
* Add indicator vars for each constraint
* Enforce logical conditions via constraints on indicator vars
* For `and` constraints, add individual constraints to the model:
    sum[i] { a_1i * x_i } <= b_1
    and
    sum[i] { a_2i * x_i } <= b_2
* All other logical conditions require indicator vars
* `or` constraints:
  * Use indicator for the satisfied constraint, plus big-M value:
    sum[i] { a_1i * x_i } <= b_1
    or
    sum[i] { a_2i * x_i } <= b_2
    or
    sum[i] { a_3i * x_i } <= b_3
    ==>
    sum[i] { a_1i * x_i } <= b_1 + M(1 - y_1)
    sum[i] { a_2i * x_i } <= b_2 + M(1 - y_2)
    sum[i] { a_3i * x_i } <= b_3 + M(1 - y_3)
    y_1 + y_2 + y_3 >= 1
    y_1, y_2, y_3 in {0, 1}

Logical conditions on equalities: `or`
* Add a free slack var to each equality constraint
* Use indicator var to designate whether slack/surplus is zero
  * sum[i] { a_ki * x_i } = b_k
    ==>
    sum[i] { a_ki + w_k } = b_k
    w_k <= M(1 - y_k)
    w_k >= -M(1 - y_k)
    y_1 + ... + y_k >= 1
    y_1, ..., y_k in {0, 1}

Logical conditions on constraints: `at least`
* Generalizes the `or` constraint
* Use indicator for the satisfied constraints
* Count the binding constraints via a constraint on indicator vars
e.g.
  at least four constraints must be satisfied with:
    y_1 + y_2 + ... + y_k >= 4

Logical conditions on constraints: `if-then`
* Indicator general constraints represent if-then logic
* e.g.
  if z = 1, then x_1 + 2*x_2 - x_3 >= 2
  ==>
  addGenConstrIndicator(z, 1, x_1 + 2*x_2 - x_3 >= 2)
* Condition must be a binary variable (e.g. z above) and a value
  (e.g. 1 above)

Semi-continuous variables:
* Many models have a special kind of "or" constraint
  e.g. x = 0 or 40 <= x <= 100
* x is a semi-continuous variable
* Common in manufacturing, inventory, power generation, etc.
* Semi-integer variables are of similar form, with an added
  integrality constraint

Two options:
* Add indicator yourself
    40y <= x <= 100y, y in {0,1}
* Let Gurobi handle vars you designate as semi-continuous/semi-integer:
    x = model.addVar(vtype=GRB.SEMICONT, lb=40, ub=100, name="x")
    x = model.addVar(vtype=GRB.SEMIINT, lb=40, ub=100, name="x")
  * Practical option when upper bound is large or non-existent

e.g. Combined logical constraints
Limit on number of non-zero semi-continuous variables
* Easy if you use indicator vars:
    40*y_i <= x_i <= 100*y_i
    sum[i] { y_i } <= 30
* Need to model this logic yourself instead of using semi-continuous
  variables -- else you cannot restrict the non-zero semi-vars

Selecting big-M values:
* You want M as tight (small) as possible.
e.g.
  x_1 + x_2 <= 10 + M*y
  If x_1, x_2 <= 100, then M = 190
  (max possible difference between LHS and RHS)

* Gurobi presolve will do its best to tighten big-M values.
* Tight, constraint-specific big-M values are better than a giant
  one-size-fits-all big-M
  * Too-large big-M leads to numerical problems and poor performance
  * Pick big-M values specifically for each constraint
  * Can look at stats of presolved model to assess how well Gurobi
    reduced the big-M coefficents
* What if presolve doesn't provide tighter big-M values?

   x_1 + x_2 <= My
   <<other constraints involving x_1, x_2>>
   Add x_1 + x_2 >= 100000
   * If problem becomes infeasible, M should be < 100000
   * Try again with RHS < 100000
   * Or, run Gurobi infeasibility finder; IIS may reveal a group
     of constraints from which we can derive a tighter M.
   * Or, solve a subproblem to determine M:
     max x_1 + x_2
     s.t. <<model constraints>>
     --> M = optimial subproblem objective value

General constraint helper functions specific to gurobipy to
simplify construction of constraints:
* max_(), min_(), abs_(), and_(), or_(), norm()
* model.addConstr(x == abs_(y))
  model.addConstr(x == or_(y, z, w))

General non-linear functions of decision vars:
* e^x, a^x  ==> addGenConstrExp(), addGenConstrExpA()
* ln(x), log_a(x)  ==> addGenConstrLog(), addGenConstrLogA()
* sin, cos, tan
* x^a  ==> addGenConstrPow()
* ax^3 + bx^2 + cx + d  ==> addGenConstrPoly()

* Non-convex quadratic fns are supported by Gurobi >= 9.0
* Previously, needed to linearize or approximate (piecewise-linear)

Multiple objectives:
* Real-world optimization problems often have multiple, competing objectives
  * Cost fns/revenue
  * Satisfaction/target achievement
  * Fairness
  * KPIs
  * Error/Feasibility
  * Switching configurations
* Approaches:
  * Make a single objective fn by using a weighted combination of
    multiple objectives
  * Hierarchical approach: solve model for each objective, but limit
    degradation of previous results
  * Combination of both as above

API:
  model.setObjectiveN(LinExpr, index, ...)

  coeff1 = [0, 1, 2, 3, 4]
  coeff2 = [4, 3, 2, 1, 0]
  x = model.addVars(5)

Variant 1:
  model.setObjectiveN(x.prod(coeff1), 0, priority=2, weight=1)
  model.setObjectiveN(x.prod(coeff2), 1, priority=1, weight=1)

Variant 2:
  model.setObjectiveN(x[1] + 2*x[2] + 3*x[3] + 4*x[4], 0, priority=2, weight=1)
  model.setObjectiveN(4*x[0] + 3*x[1] + 2*x[2] + x[3], 1, priority=1, weight=1)

Enhanced termination control for MOP:
model.getMultiobjEnv()

env0 = model.getMultiobjEnv(0)
env1 = model.getMultiobjEnv(1)

env0.setParam("TimeLimit", 100)
env1.setParam("TimeLimit", 10)

model.optimize()
model.discardMultiobjEnvs()

* Allows for fine-grained control of each multi-objective optimization pass:
  * algo choices, termination criteria
* One optimization pass per objective priority level
  * Settings for additional objectives of same prio level are ignored
* MIP starts are only used for first priority level objectives

MIP cuts:
* Cuts are constraints added to a model to restrict (cut away)
  non-integer solutions that would otherwise be solutions of the
  continuous relaxation. The addition of cuts usually reduces the
  number of branches needed to solve a MIP.
* Tightening: reduce the feasible region of a linear relaxation of a MIP
  without removing any feasible MIP points

Termination criteria:
* Relative MIP gap (%)
* Absolute MIP gap (specific value)
* Time spent solving
* Number of BnB nodes explored
* Number of feasible solutions found




