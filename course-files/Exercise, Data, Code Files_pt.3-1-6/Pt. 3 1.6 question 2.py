import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np


with open("question_two_data.json", "r") as f:
    data = json.load(f)

Items = data["Items"]
ItemName = data["ItemNames"]
Heirs = data["Heirs"]
Art = data["Art"]
Value = data["Value"]
Ideal = data["Ideal"]


m = gp.Model("heirs")


# Variables: which projects are chosen (1=yes, 0=no)
x = m.addVars(Items, Heirs, vtype=gp.GRB.BINARY,name="x")

# Variables: auxiliary variables to calculate total value for each heir
t = m.addVars(Heirs, vtype=gp.GRB.CONTINUOUS,name="t")

# Objective: minimize sum of squared deviations from ideal
m.setObjective(sum((Ideal - t[h])**2 for h in range(Heirs)))

# Constraint: Each item goes to exactly one heir
m.addConstrs(sum(x[i,h] for h in range(Heirs)) == 1 for i in range(Items))

# Constraint: Set auxiliary variables (calculate each heir's deviation from ideal)
m.addConstrs(sum(Value[i]*x[i,h] for i in range(Items)) == t[h] for h in range(Heirs))

# Constraint: Each heir gets one art item
m.addConstrs(sum(x[i,h] for i in Art) == 1 for h in range(Heirs))


m.optimize()

print("***************** Solution *****************")
print(f"Total Squared Deviation: {round(m.ObjVal, 2)}")
for i in range(Items):
    for h in range(Heirs):
        if x[i,h].X > 0.9999:
            print(f"Give item {i+1} ({ItemName[i]}) to Heir {h+1}")
        
