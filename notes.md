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


e.g. Chemical production
Purchasing raw materials:
* Sulfur
* Ammonia
* Nitrogen
* etc.

-- How much sulfur/ammonia/nitrogen used?   x, y, z
-- Cost per unit of ____?   c, d, e
-- Total cost of sulfur used?  c * x + d * y + e * z

Start running out of symbols with more chemicals...

Use subscripts:
x_s8 (S_8 = sulfur)
x_nh3 (NH_3 = ammonia)
x_n2 (N_2 = nitrogen)

then: c_s8, c_nh3, c_n2

total cost of chemicals used:
c["s8"] * x["s8"]
+ c["nh3"] * x["nh3"]
+ c["n2"] * x["n2"]
==
sum[j] { c_j * x_j }
==
quicksum(c[j] * x[j] for j in ["s8", "nh3", "n2"])
==
quicksum(c[j] * x[j] for j in range(3))
   # adopting numeric indices for the different chemicals
==
quicksum(c[j] * x[j] for j in chemicals)
   # named set

Multiple subscripts:

e.g. Bicycle sharing
N: number of locations at which you can pick up a bicycle to rent

with open("data.json") as f:
    data = json.load(f)
locations = data["locations"]
pairs = data["pairs"]   # pairs of locations

e_i: count of bicycles at location i in the evening
m_i = count of bicycles needed at location i the next morning
E = data["E"]
M = data["M"]

If e_i = m_i at every location i, great! A perfect setup,
but very unlikely.

Otherwise: what's the minimum cost to rearrange the bicycles to
get the right number m_i at each location i?

Define x_ij to be the number of bicycles moved overnight from
location i to location j.

model = gurobipy.Model()
x = model.addVars(pairs)
    # e.g. x["Home", "Tech"] = count of bicycles moved overnight from home
    # to campus
# When modeling mathematically x_ij, no need for comma.
# Nice to use comma when referencing x_{specific-val},{other-val}
# and vice versa

For every location i, we must move the correct number of bicycles
there.

How many bicycles are moved from to Tech?
from Home:
   x["Home", "Tech"]
from Truist:
   x["Truist", "Tech"]
from ...
Bicycles already at Tech:
   x["Tech", "Tech"]

--> x.sum("*", "Tech")

model.addConstr(x.sum("*", "Tech") == M["GT"])
model.addConstr(x.sum("*", "Truist") == M["Truist"])
model.addConstr(x.sum("*", "Aquarium") == M["Aquarium"])
...
-->
model.addConstrs(
    x.sum("*", j) == M[j] for j in locations,
    name="correct-number-bicycles"
)

Uses:
* from-and-to situations (amount of something going from i to j)
* blending/mixing  (amount of ingredient used to make x)
* two distinguishing characteristics (# of books in genre i of length j)
* combinations of these

Sets:
Helpful for sums over non-consecutive variables

e.g. Purchasing ad space
* in 1000 locations, for $1M
* physical billboards
* TV commercials
* Internet ads

Let x_j = money spent on location j
Then m.addConstr(quicksum(x[j] for j in range(1000)) <= 1e6)

Order the locations? Physical billboards 1-400, TV ads 401-650,
internet ads 651-1000...
m.addConstr(quicksum(x[j] for j in range(400)) <= 4e5)
m.addConstr(quicksum(x[j] for j in range(400, 650)) <= 4e5)
m.addConstr(quicksum(x[j] for j in range(650, 1000)) <= 4e5)

Additional constraints:
* No more than 40% on a type of ad (physical, TV, internet)
* No more than 30% on sports
* No more than 20% on news

How to add up news, tho? news outlets might be non-consecutive.

Create sets:
P = set of physical locations
T = set of TV locations
I = set of Internet locations
Partition each of 1-1000 into these sets
m.addConstr(quicksum(x[j] for j in P) <= 4e5)
m.addConstr(quicksum(x[j] for j in T) <= 4e5)
m.addConstr(quicksum(x[j] for j in I) <= 4e5)

S = set of sports locations
N = set of news locations
m.addConstr(quicksum(x[j] for j in S) <= 3e5)
m.addConstr(quicksum(x[j] for j in N) <= 2.5e5)

Or...indicator data.
Let P_j = 1 if location j is physical, else 0
Let T_j = 1 if location j is TV, else 0
Let I_j = 1 if location j is Internet, else 0
Let S_j = 1 if location j is sports, else 0
Let N_j = 1 if location j is news, else 0
Then...
m.addConstr(quicksum(P[j] * x[j] for j in range(1000)) <= 4e5)
m.addConstr(quicksum(T[j] * x[j] for j in range(1000)) <= 4e5)
m.addConstr(quicksum(I[j] * x[j] for j in range(1000)) <= 4e5)
m.addConstr(quicksum(S[j] * x[j] for j in range(1000)) <= 3e5)
m.addConstr(quicksum(N[j] * x[j] for j in range(1000)) <= 2.5e5)
Alternately...
m.addConstr(quicksum(x[j] for j in range(1000) if P[j] == 1) <= 4e5)
Or...
m.addConstr(x.prod(P) <= 4e5)

Building a model:
-----
e.g. real estate investment example
A real estate investment company has an investment budget that they
want to spend in a number of cities, in a way that maximizes the
predicted increase in value.
To diversify, they want to limit their spending in each region,
and have also set min and max spending limits in each city.

Hint: Look for nouns about the situation; look for verbs about the actions
that can be taken

* param budget: B
* param cities: N = number of cities
* var amount spent/invested in each city j: x_j
* param predicted value increase in each city j: P_j
* param regions: S = number of regions
* param set of cities in region s: R_s
* param investment limit in region s: L_s
* param maximum spend for any city: M
* param min spend for each city j: m_j
* constraint budget: sum[j in 1..N] { x_j } <= B
* objective: max predicted value increase:
    max sum[j in 1..n] { P_j * x_j }
    
-->

from gurobipy import GRB
import gurobipy as gp
import json

m = gp.Model("investment")
with open("investment.json", "r") as f:
    data = json.load(f)

B = data["B"]
N = data["N"]
P = data["profits"]
L = data["L"]
R = data["R"]
Mmax = data["M"]
Mmin = data["m"]
x = m.addVars(N, lb=Mmin, ub=Mmax, name="x")
m.addConstr(gp.quicksum(x[j] for j in range(N)) <= B, name="budget")
m.setObjective(gp.quicksum(P[j] * x[j] for j in range(N)), GRB.MAXIMIZE)
m.addConstrs(
  (gp.quicksum(x[j] for j in S[r]) <= L[r] \
    for r in range(len(R))),
  name="region"
)

