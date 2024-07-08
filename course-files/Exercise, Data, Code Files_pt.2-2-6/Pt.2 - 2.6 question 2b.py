import gurobipy as gp
from gurobipy import GRB

import json



with open("question_two_data.json", "r") as f:
    data = json.load(f)

DataSets = data["Data sets"]
Groups = data["Groups"]
Minimums = data["Minimums"]
Categories = data["Categories"]
Costs = data["Costs"]
NumToBuy = data["NumToBuy"]


NumCategories = len(Categories)

m = gp.Model("market")


# Variables: Which datasets are purchased? (1=yes, 0=no)
x = m.addVars(DataSets, vtype=GRB.BINARY, name="x")


# Objective: Minimize spend
m.setObjective(sum(Costs[i]*x[i] for i in range(DataSets) if i != 1) + Costs[1]*(NumToBuy - sum(x[i] for i in range(DataSets) if i != 1)))


# Constraints: Minimum data sets of each type and region
m.addConstrs(sum(x[i]*Groups[i][j] for i in range(DataSets) if i != 1) + Groups[1][j]*(NumToBuy - sum(x[i] for i in range(DataSets) if i != 1)) >= Minimums[j] for j in range(NumCategories))

# Constraints: Purchase exactly 8 datasets
#m.addConstr(x.sum() >= NumToBuy)


m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for i in range(DataSets):
    if x[i].X > 0.9999:
        print(f"Purchase dataset {i+1}")
