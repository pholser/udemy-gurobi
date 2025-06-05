import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_two_data.json", "r") as f:
    data = json.load(f)

ads = data["left_nodes"]
desired = data["supplies"]
networks = data["right_nodes"]
contracted = data["demands"]
costs = data["numbers"]


m = gp.Model("advert_assignment")


# Variables: x_ij: number times advertisement i runs on network j
x = m.addVars(ads, networks, vtype=GRB.INTEGER, name="x")


# Objective: Minimize total cost
m.setObjective(sum(costs[ads.index(i)][networks.index(j)]*x[(i,j)] for i in ads for j in networks), sense=GRB.MINIMIZE)


# Constraints: Each advertisement must run a certain number of times
m.addConstrs((x.sum(i, "*") == desired[i] for i in ads))

# Constraints: Each network requires certain number of advertisements run
m.addConstrs((x.sum("*", j) == contracted[j] for j in networks))


m.optimize()

print("***************** Solution *****************")
print(f"Total cost: {round(m.ObjVal, 4)}")
for (i, j) in product(ads, networks):
    if x[(i, j)].X > 0:
        print(f"advertisement {i} should run {x[(i, j)].X} times on network {j}.")
