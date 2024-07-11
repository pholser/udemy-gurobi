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
T = data["T"]

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

time_constraints = model.addConstrs(
    (x[j] <= T[j] for j in range(N)),
    name="time_constraints"
)

# Objective: minimize cost
model.setObjective(
    gp.quicksum(costs[j] * x[j] for j in range(N))
)

# Solve
model.optimize()

# Output
for j in range(N):
    print(f"x[{j}] = {x[j].x}")
print(f"Optimal cost: {model.objVal}")