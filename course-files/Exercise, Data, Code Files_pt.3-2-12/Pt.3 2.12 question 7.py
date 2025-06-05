import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_seven_data.json", "r") as f:
    data = json.load(f)

high = data["high_areas"]
extra = data["extras"]
low = data["low_areas"]
need = data["needs"]
costs = data["costs"]


m = gp.Model("dirt")


# Variables: x_ij: dirt sent from location i to location j
x = m.addVars(high, low, vtype=GRB.INTEGER, name="x")


# Objective: Minimize total cost
m.setObjective(sum(costs[high.index(i)][low.index(j)]*x[(i,j)] for i in high for j in low), sense=GRB.MINIMIZE)


# Constraints: From each high area, all dirt must be sent
m.addConstrs((x.sum(i, "*") == extra[i] for i in high))

# Constraints: Each low area must receive all dirt needed
m.addConstrs((x.sum("*", j) == need[j] for j in low))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(high, low):
    if x[i, j].X > 0:
        print(f"Area {i} should send {x[i, j].X} tons of dirt to area {j}.")
