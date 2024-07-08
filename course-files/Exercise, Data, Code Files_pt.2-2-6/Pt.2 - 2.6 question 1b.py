import gurobipy as gp
from gurobipy import GRB

import json


with open("question_one_data.json", "r") as f:
    data = json.load(f)

Machines = data["Machines"]
Instruments = data["Instruments"]
Times = data["Processing Times"]
MaxSales = data["Max Sales"]
Available = data["Available Times"]
Profit = data["Profits"]

InstNoFlugel = data["NoFlugelhorns"]


m = gp.Model("music")


# Variables: How many of each instrument to make (include maximum amounts here as upper bounds)
x = m.addVars(InstNoFlugel, ub=MaxSales, vtype=GRB.INTEGER,name="x")


# Objective: maximize profit
m.setObjective(Profit["Flugelhorn"]*(150-x.sum()) + sum(Profit[i]*x[i] for i in InstNoFlugel),GRB.MAXIMIZE)


# Constraints: Machine time limits
m.addConstrs(Times[j][ "Flugelhorn"]*(150-x.sum()) + sum(Times[j][i]*x[i] for i in InstNoFlugel) <= Available[j] for j in Machines)

# Constraints: Total Manufactured must be 150 by contract
# Implied by substitution


m.optimize()

print("***************** Solution *****************")
print(f"Total Profit: {round(m.ObjVal, 2)}")
for i in InstNoFlugel:
    print(f"Manufacture {x[i].X} {i}s")
print(f"This means to manufacture {150-sum(x[i].X for i in InstNoFlugel)} Flugelhorns")
