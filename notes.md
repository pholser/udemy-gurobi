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

Optimization in data science:
-----
Linear regression model:
* variables a_0, a_1, ..., a_m
* no constraints
* objective:
  minimize sum[i in 1..n] {
    (y_i - (a_0 + sum[j in 1..m] { a_j * x_ij }))^2
  }

Given n data points:
* x_ij = j'th factor for data point i
* y_i = response for data point i
* find coefficients a_0, a_1, ..., a_m to best fit data

a = model.addVars(m + 1, lb=-GRB.INFINITY)
model.setObjective(
  gp.quicksum(
    (y[i] -
      (a[0] +
        gp.quicksum(
	  a[j+1] * x[i][j] for j in range(m)
	)
      )
    ) ** 2
    for i in range(n)
  )
)

Lasso regression constraint: added to above model to
restrict sum of variables:
* sum[j in 1..m] { abs(a_j) } <= T

a_abs = model.addVars(range(1, m + 1))
model.addConstrs(
  (a_abs[j] == gp.abs_(a[j]) for j in range(1, m + 1))
)
model.addConstr(a_abs.sum() <= T)

Ridge regression constraint:
* sum[j in 1..m] { (a_j)^2 } <= T
model.addConstr(
  gp.quicksum(a[j] ** 2 for j in range(1, m + 1)) <= T)

Elastic net constraint:
* lambda * sum[j in 1..m] { abs(a_j) }
  +
  (1 - lambda) * sum[j in 1..m] { (a_j)^2 }
  <= T
model.addConstr(
  lam * a_abs.sum()
  +
  (1 - lam) * gp.quicksum(a[j] ** 2 for j in range(1, m + 1))
  <= T
)

Logistic regression:
estimates the probability of an event occurring, such as
voted or didn’t vote, based on a given data set of
independent variables.
Often used to build a binary classifier.
* variables a_0, a_1, ..., a_m
* no constraints
* objective:
  minimize
  sum[i : y_i = 1] { p(x_i) }
  +
  sum[i : y_i = 0] { 1 - p(x_i) }

where p(x_i) =
  1 / (1 + exp(-(a_0 + sum[j in 1..m] { a_j * x_ij })))

Given n data points:
* x_ij = j'th factor for data point i
* y_i = response for data point i
* find coefficients a_0, a_1, ..., a_m to best fit data

Classification: what category does this data point
  belong in

Support vector machines, for hard classification:
* variables a_0, a_1, ..., a_m
* constraints:
  (a_0 + sum[j in 1..m] { a_j * x_ij }) * y_i >= 1
    for each i
* objective: minimize sum[j in 1..m] { (a_j}^2 }

Support vector machines, for soft classification:
* variables a_0, a_1, ..., a_m
* no constraints
* objective:
  minimize sum[i in 1..n] {
    max[
      0,
      1 - (a_0 + sum[j in 1..m] { a_j * x_ij }) * y_i
    ]
    +
    lambda * sum[j in 1..m] { (a_j)^2 }
  }

Time series models:
A time series model is a set of data points ordered in time,
where time is the independent variable. These models are used
to analyze and forecast the future.

Exponential smoothing:
* variables: alpha, beta, gamma
* constraints:
  * 0 <= alpha <= 1
  * 0 <= beta <= 1
  * 0 <= gamma <= 1
  C_t = gamma * (x_t / S_t) + (1 - gamma) * C_{t - 1}
  T_t = beta * (S_t - S_{t - 1}) + (1 - beta) * T_{t - 1}
  S_t = alpha * x_t / C_{t - L} + (1 - alpha) * (S_{t - 1] + T{t - 1])
* objective:
  minimize sum[t in 1..n] { (x_t - x^_t)^2 }

ARIMA:
* variables: mu, phi_i, theta_i
* no constraints
* objective:
  minimize sum[t in 1..n] { (x_t - x^_t)^2 }
where
  x^_t = mu
       + sum[i in 1..p] { phi_i * D_(d)i }
       - sum[i in 1..q] { theta_i * (x^_{t - i} - x_{t - i}) }

GARCH:
* variables: omega, beta_i, gamma_i
* no constraints
* objective:
  minimize sum[t in 1..n] { (sigma_t^2 - sigma^_t^2)^2 }
where
  sigma^_t = omega
       + sum[i in 1..q] { beta_i * (sigma_{t - i})^2 }
       - sum[i in 1..p] { gamma_i * (x^_{t - i} - x_{t - i}) }

K-means for clustering:
* Given data:
  * x_ij = value of j'th attribute of data point i
* variables:
  * x_jk = coordinate j of cluster center k
  * y_ik = 1 if point i is in cluster k, else 0
* constraints:
  * sum[k] { y_ik } = 1 for all data points i
    (each data point is assigned a cluster)
* objective:
  minimize sum[i] { sum[k] { y_ik * p'th-root(sum[j] { (x_ij - z_jk)^p } ) } }
  (minimize total distance from data points to their cluster centers)

Optimization within data science algos:
* Tree-based methods (including random forests):
  * splits determined by maximizing information gain
* Gradient boosting:
  * Gradient is the direction of maximum improvement
  * Weight on each new model can be determined to minimize error
* Reinforcement learning:
  * Optimize cumulative reward function
* Neural networks/deep learning:
  * Learn by optimizing cost function for parameter updates

Customizing data science models using optimization:
e.g. Linear regression model
* Tweak exponent from 2 to lesser so that large residuals have less effect
* Use optimization software to find best-fit regression line after that
  # with exponent = 1...
  a = model.addVars(n + 1, lb=-GRB.INFINITY)
  residual = model.addVars(m, lb=-GRB.INFINITY)
  residual_abs = model.addVars(m)
  model.addConstrs(
    (residual[i]
      ==
      y[i] - (a[0] + gp.quicksum(a[j + 1] * x[i][j] for j in range(n)))
      for i in range(m))
  )
  model.addConstrs(
    (residual_abs[i] == gp.abs_(residual[i]) for i in range(m))
  )
  model.setObjective(residual_abs.sum())
* Add constraints: lasso regression, ridge, elastic net
* Other constraints related to the question you want to answer
  * fix the a_0 (intercept)
  * ensure regression coefficients are decreasing
    a_1 >= a_2, a_2 >= a_3, ...
  * ensure differences between coefficients are decreasing
* e.g. feature selection
  * lasso regression model
  * Higher tau_lasso for more features, lower tau_lasso for fewer features
  * No way to set tau_lasso directly for a specific number of features
  * Include new optimization variables w_i = 1 if feature i is selected,
      else 0
  * min[a_0, a_1, ..., a_n] {
      sum[i in 1..m] (y_i - (a_0 + sum[j in 1..n] { a_j * x_ij }))^2
    }
  * select exactly F features:
     sum[j in 1..n] { w_i } = F
  * Feature can't have positive coefficient unless it is selected:
     a_i <= U_i * w_i for each feature i  (big-M)
  * Feature can't have negative coefficient unless it is selected:
     a_i >= L_i * w_i for each feature i  (big-M)

Modeling example:
* Each day, an airline has planes flying on the following routes:
  * LAX to IAH (1500 miles)
  * IAH to LGA (1700 miles)
  * LGA to MIA (1300 miles)
  * MIA to LAX (2700 miles)
* Airline needs to purchase jet fuel
* Can be purchased at any of the four airports
  * LAX: $0.88/gal
  * HOU: $0.15/gal
  * LGA: $1.05/gal
  * MIA: $0.95/gal
* Fuel is heavy: flying a plane with more fuel *requires* more fuel
  to carry it
* Planes have a fuel tank capacity of 14000 gal
* For safety margin, planes need to land with at least 600 gal in tank
* May purchase no more than 12000 gal of fuel at each stop

Model:
* Data:
  * Fuel cost in city i : c_i
  * Tank capacity, safety margin, purchase limit: T, S, M
  * Distance from i to next city: d_i
* Variables:
  * Fuel purchased at city i: x_i
  * Fuel at takeoff at city i: y_i
  * Fuel at landing at city i: z_i
* Objective: keep fuel cost low
  * minimize sum[i] { c_i * x_i }
* Constraints:
  * tank capacity: y_i <= T for all cities i
  * landing safety margin: z_i >= S for all cities i
  * purchase limit: x_i <= M for all cities i
  * non-negativity
  * fuel take off with from city i
    = fuel landed with at city i
      + fuel purchase at city i
    z_i + x_i = y_i  for all cities i
    // balance constraint
  * fuel landed with at cities i =
      fuel taken off with from predecessor of city i
      - fuel used in flight from predecessor of city i to city i
  * fuel used in flight: (1 + (avg fuel level in flight)/2000) * d_{pred(i)}
  * avg fuel level in flight = (y_{pred(i)} + z_i) / 2

import gurobipy as gp
from gurobipy import GRB
import pandas as pd

df = pd.read_excel("jet-fuel.xlsx", sheet_name="jet-fuel")
cities = df["cities"]
city, fuel_cost, pred = gp.multidict(
  {c: [f, p]
    for c, f, p in zip(
      df["city"],
      df["fuel_cost"],
      df["predecessor"]
    )
  }
)
legs, distance = gp.multidict(
  {(f, t): d
    for f, t, d in zip(
      df["legs:from"],
      df["legs:to"],
      df["distance"]
    )
  }
)
tank_capacity = df["tank_capacity"].dropna().values[0]
safety_margin = df["safety_margin"].dropna().values[0]
max_purchase = df["max_purchase"].dropna().values[0]

model = gp.Model("jet-fuel")

x = model.addVars(cities, ub=max_purchase, vtype=GRB.CONTINUOUS, name="x")
y = model.addVars(cities, ub=tank_capacity, vtype=GRB.CONTINUOUS, name="y")
z = model.addVars(cities, lb=safety_margin, vtype=GRB.CONTINUOUS, name="z")

model.setObjective(x.prod(fuel_cost), sense=GRB.MINIMIZE)
model.addConstrs(
  (z[i] + x[i] == y[i] for i in cities),
  name='ground_balance'
)
model.addConstrs(
  (y[pred[i]]
    - (1 + 0.5 * (y[pred[i]] + z[i]) / 2000) * dist[i]
   ==
   z[i]
   for i in cities),
   name="air_balance"
)

model.optimize()

print(f"Fuel cost: ${round(model.ObjVal, 0)}")
for c in cities:
    print("*" * 50)
    print(f"Fuel at landing at {c}: {round(z[c].X, 0)} gal")
    print(f"Fuel purchased at {c}: {round(x[c].X, 0)} gal")
    print(f"Fuel at takeoff at {c}: {round(y[c].X, 0)} gal")

* Include constraints to link variables where needed
* Even constraints that look "recursive" are ok

Non-negativity:
* Don't leave these out if needed
* Consider whether negative-valued variables may make
  sense in the model

Variable substitution/extra variables:
* In jet fuel example:
  * fuel purchased / at takeoff from / at landing at city i
  * Ground balance: since z_i + x_i = y_i forall cities i,
    you could eliminate y_i from the model entirely...
    substitute z_i + x_i instead.
    * or substitute for x_i or z_i also
  * four models, all valid
* Older times: do the substitution, since fewer vars
  means less memory used, more speed
* Newer times: more variables means better explainability,
  solvers do a great job of pre-solving, simplifying
  models where possible
* If substituting, watch out for math (e.g. you substitute
  y_i - z_i)...negative values for what would be x_i
  * remember non-negativity constraints

* predictive modeling to find data for model

Quadratic objectives:
e.g.
import gurobipy as gp
from gurobipy import GRB

model = gp.Model("quadratic")
# let `n` be some number of variables
x = model.addVars(n, vtype=GRB.CONTINUOUS, name="x")

# objective: minimize square of sum
model.setObjective(x.sum() ** 2, sense=GRB.MINIMIZE)
# n^2 multiplications, n^2 terms to add

# another way:
z = m.addVar(vtype=GRB.CONTINUOUS, name="z")
model.addConstr(z == x.sum())
model.setObjective(z ** 2, sense=GRB.MINIMIZE)
# n terms to add, 1 multiplication

e.g. regression objective:
# number of data points: n
# number of features: m
# data points:
# * features for each data point i: x_ij
# * response for each data point i: y_i
# variables: regression coefficients a_0, a_1, ..., a_m
a = model.addVars(m + 1, lb=-GRB.INFINITY, name="coeffs")

# objective: minimize sum of squared residuals
model.setObjective(
  gp.quicksum(
    (y[i] - (a[0]
              + gp.quicksum(
                  a[j + 1] * x[i][j]
		  for j in range(m)
                )
            )
    ) ** 2
    for i in range(n)
  )
)

# make new vars for each residual
z = model.addVars(n, lb=-GRB.INFINITY, name="residual")
m.addConstrs(
  (z[i] == (
    y[i] - (
      a[0] + gp.quicksum(
        a[j + 1] * x[i][j] for j in range(m)
      )
    )
  ) for i in range(n))
)
model.setObjective(gp.quicksum(z ** 2 for i in range(n)))

e.g. quadratic constraints:
vars x, y
compact constraint: (x + y)^2 <= 10
multiplied out: x^2 + 2xy + y^2 <= 10
instead, new variable z:
constraint: z = x + y
constraint: z^2 <= 10

Reusability of models:
* Use same model structure, on different days, situations,
  instances
* Read data from files instead of baking into gurobipy
  code

Infeasibility and debugging:
e.g. industrial diamond purchasing
* Three types of diamond drills made:
    heavy-, medium-, light-duty
* Three diamond suppliers supply mixes of diamonds usable
  for different drill types:
  * (1) ($3/kg): 40% heavy, 35% medium, 25% light
  * (2) ($2.50/kg): 35% h, 55% m, 10% light
  * (3) ($2.70/kg): 30, 30, 40
* Purchase requirements:
  * 1700 kg for heavy, 1200 kg for medium, 1800 kg for light

* How much to buy from each supplier to meet needs,
  at least cost?

import gurobipy as gp
from gurobipy import GRB

# Data
c = {0: 3.0, 1: 2.5, 2: 2.7}
d = [1700, 1200, 1800]
a = [
  [0.4, 0.35, 0.3],
  [0.35, 0.55, 0.3],
  [0.25, 0.1, 0.4]
]

model = gp.Model("diamonds")

# Decision: how much to buy from each supplier
x = model.addVars(3, vtype=GRB.CONTINUOUS, name="x")

# Objective: minimize total purchase cost
model.setObjective(x.prod(c), sense=GRB.MINIMIZE)

# Constraint: meet needs for each type of drill's diamonds
needs_met = model.addConstrs(
  (gp.quicksum(a[i][j] * x[j] for j in range(3)) >= d[i])
  for i in range(3),
  name="needs_met"
)

It turns out that if you change the demand constraints
to be equality constraints, the model becomes infeasible --
no possible solution meets all of the constraints.
Causes:
* model is infeasible
* human error in writing model

Using models to analyze sensitivity:
e.g. Chemical manufacturing
* A chemical company produces several types of chemicals
  by running reactions on various machines
* Company produces M types of chemicals by running
  N different processes
* Goal: produce all chemicals at minimum cost
* Data science team estimates:
  * demand forecast d_i for chemical i
  * for each hour of runtime for process j,
    a_ij gallons of chemical i is produced
* Each process j costs c_j per hour to run

import gurobipy as gp
from gurobipy import GRB
import json

with open("chemicals.json") as f:
    data = json.load(f)

# Data
M = data["M"]
N = data["N"]
demands = data["demands"]
a = data["a"]
costs = data["costs"]

model = gp.Model("chemicals")

# Decision: how many hours per day to run each process
x = model.addVars(N, vtype=GRB.CONTINUOUS, name="x")

# Constraints: meed demand for each chemical
demand_constraints = model.addConstrs(
    (
        (gp.quicksum(a[i][j] * x[j] for j in range(N))
         >=
         demands[i]
         for i in range(M))
    ),
    name="demand_constraints"
)

# Objective: minimize cost
model.setObjective(
    gp.quicksum(costs[j] * x[j] for j in range(N))
)

Result: process 1 0 hr, process 2 30 hr/day, $30K/day

We want the process to run in <= 24 hr

time_constraints = model.addConstrs(
    (x[j] <= 24 for j in range(N)),
    name="time_constraints"
)

Now, Result: process 1 2 hr, process 2 24 hr/day, $32K/day

Option 1:
* Install a second set of process 2 machinery for $1.5M
* Allows original solution
* Payback period: $1.5M / ($32K - $30K) = 750 days

Sensitivity analysis: showing changes to solution as
data changes

What about demand uncertainty: What if demand drops 20%?
* tweak the forecast data accordingly, re-run model

Now, Result: process 1 0 hr, process 2 24 hr/day
Total cost: $24K/day

What happens with original forecasted demand, but process 2
deteriorates by 10%?

Result: process 1 6.8 hr/day, process 2 24 hr/day,
  cost $51.2K/day

--> Optimization results tell us that it's important to
    keep process 2 machinery in good working order

If process 2 deteriorates, should the company now install
another set of process 2 machinery, at a cost of $1.5M?

add another var for this: x_2A
c_2A = $1000
a_*,2A = [100, 100, 200]
x_2A <= 24

Now, Result: process 1 0 hr, process 2 6.667 hr/day,
process 2A 24 hr/day
cost: $30666.67/day
payback period: 88 days

OTOH, what if we take process 2A away, restore process 2
to its previous non-deteriorated output, and take it down
for 4 hr/day for preventive maintenance?

--> P1 10 hr/day, P2 20 hr/day --> $60K/day!

Classification of models:
x = vector of variables
Min or max f(x)
s.t. x in X

LP:
* f(x) is a linear function
* constraint set X is defined by linear equations
  and inequalities
* easy and fast to solve even for large instances

QP:
* f(x) is a quadratic function
* constraint set X is defined by linear equations
  and inequalities
* Gurobi solution speed depends on f(x)

Convex QP:
* f(x) is a quadratic convex function
* constraint set X is defined by linear equations
  and inequalities
* Gurobi can solve these quickly

Non-convex QP:
* f(x) is a quadratic non-convex function
* constraint set X is defined by linear equations
  and inequalities
* Gurobi can solve these, but it takes much longer

QCP (quadratically constrained program), convex:
* f(x) is a linear or quadratic function
* constraint set X is defined by linear and quadratic
  equations and inequalities
* each of the constraints defines a convex set
* Gurobi can solve these quickly

QCP (quadratically constrained program), non-convex:
* f(x) is a linear or quadratic function
* constraint set X is defined by linear and quadratic
  equations and inequalities
* Constraints do not define a convex set
* Gurobi can solve these, but it takes much longer

MILP (mixed integer linear program):
* f(x) is a linear function
* constraint set X is defined by linear equations
  and inequalities
* Some variables are required to have integer values
* (binary integer program: all variables are in {0, 1})
* (pure integer program: all variables are integer)

Combinations of all the above

What if your problem is non-convex?
* piecewise linear approximations
* bounds to show quality
* heuristics to get good solutions

How models are solved (high-level):
Two main steps:
* Initialization: create a first solution
  * can be simple/bad/infeasible
* Iteration:
  * Find an improving direction t
  * Use a step size theta to move along it
  * New solution = old solution + theta * t
* Stop when solution:
  * doesn't change much
  * time runs out, or
  * it's optimal or close enough to it

Similar to gradient boosting

Convex optimization problem:
* Guaranteed to find optimal soln
Non-convex problem:
* Might converge to an infeasible soln
  * Split into two subset models to exclude infeasible soln
    and iterate
  * Optimal soln is best soln over all subsets
* Might converge to a local optimum
  * Solve from multiple starting solutions

Modeling complex situations with binary variables:
e.g. stock market investment

import gurobipy as gp
from gurobipy import GRB

m = gp.Model("stocks")

# Data
with open("data-stock-market.json") as f:
    data = json.load(f)
num_stocks = data["num_stocks"]
investment_budget = data["budget"]
expected_return = \
    {i: data["relative_return"][i] for i in range(num_stocks)}
Q = data["covariance_of_return"]

# Decision: how much money to invest in each stock
x = model.addVars(num_stocks, vtype=GRB.CONTINUOUS, name="x")

# Constraint: stay within budget
budget_constraint = m.addConstr(x.sum() <= investment_budget)

# Objective: balance risk and return
m.setObjective(
  x.prod(r)
  -
  theta * gp.quicksum(
      Q[i][j] * x[i] * x[j]
      for i in range(n)
      for j in range(n)
  ),
  sense=GRB.MAXIMIZE
)

What else might be needed?
* Transaction cost t
  * Broker fee per company invested in
    (fixed cost regardless of how much money invested)
--> Current set of vars isn't set up for this

-->
y = m.addVars(num_stocks, vtype=GRB.BINARY, name="y")
add factor to objective: - rho * t * y.sum()

# fixed charge

# could add transaction costs to budget constraints

# now, link vars: if invest in stock i, must pay transaction cost
# if x_i >= 0, then y_i must be 1.
# rather: if y_i = 0, then x_i must be zero.
m.addConstrs(x_i <= budget * y_i for i in range(n))

# could also use gurobi indicator constraints:
for i in range(n):
    m.addGenConstrIndicator(y[i], 0, x[i] == 0)

Yes/no decisions and related constraints:
e.g.
import gurobipy as gp
from gurobipy import GRB

m = gp.Model("stocks")

# Data
with open("data-stock-market.json") as f:
    data = json.load(f)
num_stocks = data["num_stocks"]
investment_budget = data["budget"]
stocks = data["stocks"]
energy_stocks = data["energy_stocks"]
expected_return = \
  {stock: data["relative_return"][i]
   for i, stock in enumerate(stocks)}
Q = data["covariance_of_return"]
transaction_cost = {
  stock: data["transaction_cost"]
  for i, stock in enumerate(stocks)
}

# Decision: how much money to invest in each stock
x = model.addVars(stocks, vtype=GRB.CONTINUOUS, name="x")
y = model.addVars(stocks, vtype=GRB.BINARY, name="y")

# Constraint: stay within budget
budget_constraint = m.addConstr(x.sum() <= investment_budget)

# Objective: balance risk and return
m.setObjective(
  x.prod(r)
  -
  theta * gp.quicksum(
      Q[i][j] * x[i] * x[j]
      for i in range(n)
      for j in range(n)
  )
  -
  rho * y.prod(t),
  sense=GRB.MAXIMIZE
)

# Constraint: stay within budget
budget_constraint = m.addConstr(
  x.sum() <= investment_budget - y.prod(t)
)

# linking constraint: if not investing in stock i, then amt invested == 0
for i in range(n):
  m.addGenConstrIndicator(y[i], 0, x[i] == 0)

What else might be needed?
* Minimum investment, if any, in each stock
  * Not worth investing $0.03 in a $600 stock

Data: min_i = minimum amount invested in stock i, if any
Constraint:
  x_i >= min_i * y_i

  * If y_i is 1, then x_i >= min_i
  * If y_i is 0, then x_i >= 0
    * and another constraint forces x_i <= 0,
      so x_i == 0

* Purchase whole shares
Data: p_i = price per share of stock i
Vars: z_i = shares of stock i purchased (integer)

z = model.addVars(n, vtype=GRB.INTEGER, name="z")

Add constraints:
-- p_i * z_i >= min_i * y_i for all stocks i
-- p_i * z_i == x_i for all stocks i

Personal investment constraints:
* Must invest in Tesla --> y["Tesla"] == 1
* Invest in at least two of A, B, and C:
  --> y[A] + y[B] + y[C] >= 2
* Invest in exactly two of A, B, and C:
  --> y[A] + y[B] + y[C] == 2
* Either invest in A and B, or neither of A and B:
  --> y[A] == y[B]
* Opposite decisions for A and B:
  --> y[A] == 1 - y[B]

If/then constraints:
e.g.
If we invest in any energy stock, then invest in at least
  five energy stocks.
--> sum[j in energy_stocks] { y_j } >= 5 * y_i  forall energy stocks i

alternatively:
var w_energy = 1 if investing in energy, 0 if not.
then:
-- sum[j in energy_stocks] { y_j } >= 5 * w_energy
-- w_energy >= y_j for all energy stocks j

Using truth tables to troubleshoot constraints:
v1  v2  ....   LHS   RHS   Constraint true?   Want this result?
---------------------------------------------------------------

Modeling logic using binary variables:
with two binary vars a and b
Basic building blocks:
* AND: two things both have to happen    a + b == 2
* OR: at least one of two things has to happen   a + b >= 1
* XOR: exactly one of two things has to happen   a + b == 1
* SAME: either both things happen, or neither happens   a == b
* DIFFERENT: one happens and the other does not   a == 1 - b
* IF-THEN: if the first one happens, so does the second
           (if first does not happen, no restriction on second)
    a <= b
    gurobipy: m.addConstr(a <= b)
      or
      m.addConstr((a == 1) >> (b == 1))
Sometimes if-then stated as contrapositive: if not b, then not a
      (1 - b) <= (1 - a)
      -->
      a <= b

e.g. either invest in an auto company (Tesla or GM)
 or invest in both Walmart and ExxonMobil

() + () >= 1
(y_T + y_GM) + (y_WM + y_EX) / 2 >= 1
or
2y_T + 2y_GM + y_WM + y_EX >= 2

e.g. rolling-horizon power generation:

How much power should each in a set of power plants produce each day
to meet varying demand?
-- at min cost
-- meet emission restrictions
   -- monthly limit, cannot exceed
   -- daily limit, can exceed <= 7x/month, no more than 3 days in a row
      in any month; fine when exceeded
-- plan one month in advance (30 days)


import gurobipy as gp
import json

model = gp.Model("electricity")
with open("electricity.json", "r") as f:
    data = json.load(f)

n_days = data["num_days"]
n_plants = data["num_plants"]
demand = data["demand"]
max_out = data["max_power_output"]
pollution = data["pollution"]
cost = data["cost"]

month_limit = data["monthly_emission_limit"]
daily_limit = data["daily_emission_limit"]
fine = data["fine"]

# How much power to produce at each plant each day?
z = model.addVars(n_plants, n_days)

# Pay fine on day d or no?
y = model.addVars(n_days, vtype=gp.GRB.BINARY)

# Minimize total cost
model.setObjective(
    gp.quicksum(cost[i] * z[i, d] \
    for d in range(n_days) \
    for i in range(n_plants) \
    + fine * y.sum()
)

# Meet power demand each day
model.addConstrs((z.sum("*", d) >= demand[d] for d in range(n_days)))
# Respect power production capacity
model.addConstrs((z[i, d] <= max_out[i] \
    for i in range(n_plants) \
    for d in range(n_days)))

# Respect monthly emission limit
model.addConstr(
    gp.qucksum(pollution[i] * z[i, d] \
    for d in range(n_days) \
    for i in range(n_plants)) <= month_limit
)

# Respect daily emissions limit
m.addConstr(y.sum() <= 7)
m.addConstr(y[1] + y[2] + y[3] + y[4] <= 3)
m.addConstr(y[2] + y[3] + y[4] + y[5] <= 3)
...
# or
m.addConstrs((y[j] + y[j+1] + y[j+2] + y[j+3] <= 3 for j in range(n_days - 3)))

# Which days are above emission limit?

# If total emissions is more than E, then y_d must be 1
m.addConstrs(((gp.quicksum(poll[i, d] * z[i, d] for i in range(n_plants)) <= daily_limit + monthly_limit * y[i, d]) for d in range(n_days)))

Can they plan 30 days ahead?

Rolling-horizon model:
Solve model every week or day, each time looking a month ahead

Adjust model after each day


(1) orchestration
(2) [smart-tl] incorporate forecasting loads into dispatching
(3) [smart-tl] coordinate output driver states (from end of dispatching)
    to be read in by load acceptance

forecasting file -- download, and for use in engine
-- grab a LA run, dispatching run starting at same time, how to (3)
-- include only forecasted loads from that booking time after sim start time

-- turn forecasting on in dispatching

-- booking time == expected arrival time
-- load acceptance == i have that time

output driver states, how to stitch together

driver pre dispatch states file
write a dynamic driver file before i'm done

drivers out of original dispatch horizon but will be available during
LA


Let x_ih = 1 if item i is given to heir h.
Let v_h = sum[i in I] { i.value * x_ih } for all h in H.
Let ideal = the ideal split value.

Then

minimize sum[h in H] { (ideal - v_h)^2 }

Subject to:
# each item given to exactly one heir
sum[h in H] { x_ih } = 1 for all i in I

# each music/art item must be given to a different heir
sum[i in I where I is art/music] { x_ih } == 1 for all h in H

