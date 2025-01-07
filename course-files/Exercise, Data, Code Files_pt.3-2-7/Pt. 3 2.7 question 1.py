import gurobipy as gp
from gurobipy import GRB

import numpy as np

m = gp.Model("space_launch")

payloads, revenues, weights = gp.multidict(
    {
        "A": [15, 100],
        "B": [12, 80],
        "C": [9, 70],
        "D": [17, 130],
        "E": [23, 250],
        "F": [3, 10],
        "G": [8, 20],
        "H": [4, 30],
        "I": [10, 70],
    }
)
maximum_allowable_weight = 350

# x_i = 1: if payload i is selected
x = m.addVars(payloads, vtype=GRB.BINARY, name="x")

# Objective: maximize the total revenue
m.setObjective(x.prod(revenues), sense=GRB.MAXIMIZE)

# The total payloads' weights does not go beyond the maximum allowable weight
m.addConstr(
    x.prod(weights) <= maximum_allowable_weight, name="allowable_weight"
)

m.optimize()

print("***************** Solution *****************")
print(f"Total revenue: {round(m.ObjVal, 4)}")
for payload in payloads:
    if x[payload].X > 0.5:
        print(f"Payload {payload} selected.")
