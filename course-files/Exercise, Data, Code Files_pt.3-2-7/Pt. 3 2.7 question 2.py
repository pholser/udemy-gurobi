import gurobipy as gp
from gurobipy import GRB

import numpy as np

m = gp.Model("renovation")

items, costs, resale_values = gp.multidict(
    {
        "roof": [10, 12],
        "kitchen": [30, 45],
        "bathrooms": [20, 28],
        "HVAC": [15, 18],
        "floors": [38, 70],
        "landscaping": [6, 10],
    }
)
renovation_budget = 75

# x_i = 1: if item i is selected for renovation
x = m.addVars(items, vtype=GRB.BINARY, name="x")


# Objective: maximize the total resale value
m.setObjective(x.prod(resale_values)-x.prod(costs), sense=GRB.MAXIMIZE)


# The total renovation cost does not exceed the renovation budget
m.addConstr(x.prod(costs) <= renovation_budget, name="budget")

m.optimize()

print("***************** Solution *****************")
print(f"Total resale impact: {round(m.ObjVal, 4)}")
for item in items:
    if x[item].X > 0.5:
        print(f"Item {item} selected for renovation.")


