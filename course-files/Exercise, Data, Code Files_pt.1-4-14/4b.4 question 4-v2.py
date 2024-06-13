import gurobipy as gp
from gurobipy import GRB


import json

# select correct data file, comment out the other two
with open("question_threeA_data.json", "r") as f:
#with open("question_threeB_data.json", "r") as f:
#with open("question_threeC_data.json", "r") as f:
    data = json.load(f)


Materials = data["Materials"]
Companies = data["Companies"]
Bundles = data["Bundles"]
Minimums = data["Minimums"]
BundlePrices = data["BundlePrices"]
SmallPrices = data["SmallPrices"]
Collected = data["Collected"]


m=gp.Model("recycle")


# Variables: Bundles sold to each large company
x = m.addVars(Companies, lb=Minimums, vtype=gp.GRB.CONTINUOUS, name="x")

# Variables: Pounds of each material sold to small companies
y = m.addVars(Materials, vtype=gp.GRB.CONTINUOUS, name="y")


# Objective: Maximize revenue
m.setObjective(x.prod(BundlePrices) + y.prod(SmallPrices), gp.GRB.MAXIMIZE)


# Constraints: Sell all collected materials (in bundles and to small companies)
m.addConstrs(sum(Bundles[i][j] * x[i] for i in Companies) + y[j] == Collected[j] for j in Materials)


m.optimize()

print("***************** Solution *****************")
print(f"Total revenue: {round(m.ObjVal, 2)}")
for i in Companies:
    print(f"Sell {x[i].X} bundles to company {i}.")
for j in Materials:
    if y[j].X > 0:
        print(f"Sell {y[j].X} pounds of {j} to small recyclers.")
        
