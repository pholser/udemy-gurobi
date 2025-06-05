import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_four_data.json", "r") as f:
    data = json.load(f)

plants = data["plants"]
production = data["production"]
stores = data["stores"]
demand = data["demand"]
costs = data["costs"]


m = gp.Model("shipping")


# Variables: x_ij: number of refrigerators sent from plant i to store j
x = m.addVars(plants, stores, vtype=GRB.INTEGER, name="x")


# Objective: Minimize total cost
m.setObjective(sum(costs[plants.index(i)][stores.index(j)]*x[(i,j)] for i in plants for j in stores), sense=GRB.MINIMIZE)


# Constraints: Each plant ships a certain number of refrigerators
m.addConstrs((x.sum(i, "*") == production[plants.index(i)] for i in plants))

# Constraints: Each store receives a certain number of refrigerators
m.addConstrs((x.sum("*", j) == demand[stores.index(j)] for j in stores))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(plants, stores):
    if x[i, j].X > 0:
        print(f"Plant {i} should ship {x[i, j].X} refrigerators to {j}.")
