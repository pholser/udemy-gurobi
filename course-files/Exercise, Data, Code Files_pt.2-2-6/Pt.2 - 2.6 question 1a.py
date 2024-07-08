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


m = gp.Model("music")


# Variables: How many of each instrument to make (include maximum amounts here as upper bounds)
x = m.addVars(Instruments, ub=MaxSales, vtype=GRB.INTEGER,name="x")


# Objective: maximize profit
m.setObjective(x.prod(Profit),GRB.MAXIMIZE)


# Constraints: Machine time limits
m.addConstrs(sum(Times[j][i]*x[i] for i in Instruments) <= Available[j] for j in Machines)

# Constraints: Total Manufactured must be 150 by contract
m.addConstr(x.sum() == 150)
               

m.optimize()

print("***************** Solution *****************")
print(f"Total Profit: {round(m.ObjVal, 2)}")
for i in Instruments:
    print(f"Manufacture {x[i].X} {i}s")
        
