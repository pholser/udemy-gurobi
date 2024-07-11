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
    ((gp.quicksum(a[i][j] * x[j] for j in range(3)) >= d[i])
     for i in range(3)),
    name="needs_met"
)

# Solve
model.optimize()

# Output
for i in range(3):
    print(f"Buy {x[i].x} kg diamonds from supplier {i}")
print(f"Total cost: {model.objVal}")
