import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_six_data.json", "r") as f:
    data = json.load(f)

players = data["players"]
positions = data["positions"]
values = data["values"]


m = gp.Model("position_assignment")


# Variables: x_ij = 1 if player i is assigned to position j
x = m.addVars(players, positions, vtype=GRB.INTEGER, name="x")


# Objective: Maximize value
m.setObjective(gp.quicksum(x[players[i],positions[j]]*values[i][j] for i in range(len(players)) for j in range(len(positions))), sense=GRB.MAXIMIZE)


# Constraints: Each player plays one position
m.addConstrs((x.sum(i, "*") == 1 for i in players))

# Constraints: Each position is played by one player
m.addConstrs((x.sum("*", j) == 1 for j in positions))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(players, positions):
    if x[i, j].X > 0:
        print(f"Player {i} should play Position {j}.")
