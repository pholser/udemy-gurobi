import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np


with open("question_four_data.json", "r") as f:
    data = json.load(f)

M, c, alpha = data["M"], np.array(data["cost"]), np.array(data["alpha"])

m = gp.Model("ovens")


# Price of each oven model
p = m.addVars(range(1,M+1), vtype=gp.GRB.CONTINUOUS, name="p")

# Quantity sold of each oven model
q = m.addVars(range(1,M+1), vtype=gp.GRB.CONTINUOUS, name="q")


# Objective: maximize total profit
m.setObjective(sum(q[i]*(p[i]-c[i]) for i in range(1,M+1)), gp.GRB.MAXIMIZE)


# Elasticity equations
m.addConstrs((q[i] == alpha[i,0] + sum(alpha[i,j]*p[j] for j in range(1,M+1))) for i in range(1,M+1))


m.setParam("NonConvex",2)
m.optimize()

print("***************** Solution *****************")
print(f"Total profit: {round(m.ObjVal, 2)}")
for i in range(1,M+1):
    print(f"Sell {q[i].X} of m {i} at price {p[i].X}.")
