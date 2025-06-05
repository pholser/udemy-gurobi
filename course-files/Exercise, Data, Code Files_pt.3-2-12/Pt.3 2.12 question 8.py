import gurobipy as gp
from gurobipy import GRB

from itertools import product
import numpy as np

import json

with open("question_eight_data.json", "r") as f:
    data = json.load(f)

black = data["black"]
white = data["white"]
scores = data["scores"]

# Calculate value of each matchup
values = np.empty((len(black),len(white)), dtype=float)
for i in range(len(black)):
    for j in range(len(white)):
        values[i][j] = (scores[black[i]]+scores[white[j]])**2


m = gp.Model("chess")


# Variables: x_ij = 1 if player i is matched against player j
x = m.addVars(black, white, vtype=GRB.INTEGER, name="x")


# Objective: Maximize value
m.setObjective(gp.quicksum(x[black[i],white[j]]*values[i][j] for i in range(len(black)) for j in range(len(white))), sense=GRB.MAXIMIZE)


# Constraints: Each black player gets one opponent
m.addConstrs((x.sum(i, "*") == 1 for i in black))

# Constraints: Each white player gets one opponent
m.addConstrs((x.sum("*", j) == 1 for j in white))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(black, white):
    if x[i, j].X > 0:
        print(f"{i} is matched against {j}.")
