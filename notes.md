import gurobipy as gp
from gurobipy import GRB

model = gp.Model("invest")

cities = {"Atlanta", "Boston", "Charlotte", "Detroit"}
x = model.addVars(cities, name="x")
model.addConstr(x.sum() <= 20, name="budget")
model.addConstr(
    x["Boston"] + x["Detroit"] <= 12,
    name="NorthBudget"
)
model.addConstr(
    x["Atlanta"] + x["Charlotte"] <= 12,
    name="SouthBudget"
)


# also...
north = {"Boston", "Detroit"}
assert north.issubset(cities)
south = {"Atlanta", "Charlotte"}
assert south.issubset(cities)

model.addConstr(
    gp.quicksum(x.select(north)) <= 12,
    name="NorthBudget"
)
model.addConstr(
    gp.quicksum(x.select(south)) <= 12,
    name="SouthBudget"
)
model.addConstrs(
    (x[c] >= 2 for c in cities),
    name="minInvest"
)
model.addConstrs(
    (x[c] <= 8 for c in cities),
    name="maxInvest"
)
# or ... without constraints, using bounds
model.addVars(cities, lb=2, ub=8, name="x")

priceIncrease = {
    "Atlanta": 0.11, "Boston": 0.02, "Charlotte": 0.04, "Detroit": 0.03
}
model.setObjective(x.prod(priceIncrease), GRB.MAXIMIZE)


e.g. "diet problem" (US Army)
* satisfy soldiers' nutritional requirements
* at minimum cost

Parameters:

F: set of foods
N: set of nutrients
a_ij: amount of nutrient i per unit of food j
m_i, M_i: min/max daily intake of nutrient i
c_j: per-unit cost of food j

Decisions:
x_j: amount of food j in daily diet

Constraints:
sum[j in F] { a_ij * x_j } >= m_i, forall i in N
sum[j in F] { a_ij * x_j } <= M_i, forall i in N

Objective:
min sum[j in F] { c_j * x_j }


import gurobipy as gp
from gurobipy import GRB

with open("diet-data.json") as f:
    d = json.load(f)
foods = d["foods"]
nutrients = d["nutrients"]
a = {tuple(i["pair"]): i["val"] for i in d["a"]}
Mmin = d["m"]
Mmax = d["M"]
cost = d["cost"]

model = gp.Model("diet")
x = model.addVars(foods, name="x")
model.addConstrs(
  (gp.quicksum(a[i, j] * x[j] for j in foods) == [Mmin[i], Mmax[i]]
  for i in nutrients
)
model.setObjective(x.prod(cost), sense=GRB.MINIMIZE)

Other complexities:
-- Variety in diets
-- Seasonal cost variation
-- Taste of foods, combinations of foods
-- etc.

e.g. feed calculator (Single Spark)


e.g. call center scheduling
-- Meet forecasted demand d_j for each day of week j
-- Workers work 5 days in a row, then 2 days off
-- Minimize worker-days used

Variables:
x_j : number of people who start working on day j

Objective:
min 5 * sum[j in days] { x_j }

Constraints:
-- Demand met: sum[i working on day j] { x_i } >= d_j, forall j in days
   (e.g. x_fri + x_sat + x_sun + x_mon + x_tue >= d_tue)
-- x_j >= 0 for all days j, x_j integer

import gurobipy as gp
from gurobipy import GRB
import numpy as np

num_workers = 10
num_days = 7
demands = np.loadtxt("demands.csv", dtype=int)
A = np.loadtxt("A.csv", dtype=int, encoding=None)
# A_ij = 1 if workers who start on day i are still working on day j, 0 else
A = A.reshape((num_days, num_days))

model = gp.Model("workers")
x = model.addVars(days, lb=0, vtype=GRB.INTEGER, name="x")
model.setObjective(5 * x.sum(), sense=GRB.MINIMIZE)
model.addConstrs(
  (gp.quicksum(A[i, j] * x[j] for j in range(num_days)) \
    >= \
    demands[i]
  for i in range(num_days),
  name="demand"
)


gurobipy expressions:
-----
Variable types:
* Continuous  (vtype=GRB.CONTINUOUS)
* Integer     (vtype=GRB.INTEGER)
* Binary      (vtype=GRB.BINARY)
model.addVar, model.addVars

Simple linear expressions:
* Variable multiplied by a number
   2 * x, -17 * y

* Sums and differences of variables multiplied by numbers
   2 * x - 17 * y + 5/4 * x

Quadratic expressions:
* Variable squared multiplied by a number, or two variables
  multiplied together ("bilinear")
  2 * x**2, -17 * y**2, 5/4 * x * z

* Sums and differences of these

Other functions (examples):
Can be modeled; Gurobi reformulates with linear expressions, bounds, etc.
* Divide variable by another:
  x/y
  # z = x/y
  z = model.addVar(vtype=GRB.CONTINUOUS)
  model.addConstr(z * y == x)

* Three variables multiplied:
  x * y * z
  # w = x * y * z
  v = model.addVar(vtype=GRB.CONTINUOUS)
  w = model.addVar(vtype=GRB.CONTINUOUS)
  model.addConstr(v == x * y)
  model.addConstr(w == z * v)

* Variable to a power other than zero or one:
  y**3, z**1.5
  # z = y^a
  z = model.addVar(vtype=GRB.CONTINUOUS)
  model.addGenConstrPow(y, z, a)

* Trig function of a variable
  cos(x)
  # z = cos(x)
  z = model.addVar(vtype=GRB.CONTINUOUS)
  model.addGenConstrCos(x, z)

* Logarithm of a variable:
  log(y)
  # z = log(y)
  z = model.addVar(vtype=GRB.CONTINUOUS)
  model.addGenConstrLogA(y, z, 10)

Avoid if possible; often can slow solution time.

Constraint types:
* expr <= expr
* expr >= expr
* expr == expr
  (equivalent to >= and <=)

Cannot use: >, <, !=; optimization algos generally cannot handle these

Advanced Gurobi constraint types:
* "AND": binary var y is 1 iff all of binary vars x_1, ..., x_n are 1
  y <= x_1
  ...
  y <= x_n
  y >= sum[i] { x_i } - (n - 1)

  gurobipy:
  x = model.addVars(n, name="x")
  model.addGenConstrAnd(y, x)

* "OR": binary var y is 1 iff at least one of binary vars x_1, ..., x_n are 1
  y <= x_1
  ...
  y <= x_n
  y <= sum[i] { x_i }

  gurobipy:
  x = model.addVars(n, name="x")
  model.addGenConstrOr(y, x)

* "MAX": variable y is equal to the maximum (largest) of variables
  x_1, ..., x_n and constant c

  y >= x_1
  ...
  y >= x_n
  y >= c

  gurobipy:
  x = model.addVars(n, name="x")
  model.addGenConstrMax(y, x)

* "MIN": variable y is equal to the minimum (smallest) of variables
  x_1, ..., x_n and constant c

  y <= x_1
  ...
  y <= x_n
  y <= c

  gurobipy:
  x = model.addVars(n, name="x")
  model.addGenConstrMin(y, x)

* "ABS": variable y is equal to the absolute value of variable x:
  introduce vars x_pos and x_neg, the decomposition of x into itss
  positive and negative parts  (x_pos is max(x, 0); x_neg is max(-x, 0))
  x == x_pos - x_neg
  x_pos >= 0
  x_neg >= 0
  y == x_pos + x_neg

  gurobipy:
  x = model.addVars(n, name="x")
  model.addGenConstrAbs(y, x)

* "Indicator constraints": If a binary variable y has a certain value v,
  then a constraint a * x <= b must be satisfied

  model.addConstr((y == v) >> (a * x <= b))
  # or ...
  model.addGenConstrIndicator(y, v, a * x <= b)

  a * x <= b is enforced only if y == v


* e.g. Chemical production
Purchasing raw materials:
* Sulfur
* Ammonia
* Nitrogen
* etc.

-- How much sulfur/ammonia/nitrogen used?   x, y, z
-- Cost per unit of ____?   c, d, e
-- Total cost of sulfur used?  c * x + d * y + e * z



