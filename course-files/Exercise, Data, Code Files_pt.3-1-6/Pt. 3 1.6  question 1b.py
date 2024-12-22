import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np


with open("question_one_data.json", "r") as f:
    data = json.load(f)


Projects = data["Projects"]
Council = data["Council"]
Suggested = data["Suggested"]
Cost = data["Costs"]
Surplus = data["Surplus"]
Beneficiaries = data["Beneficiaries"]

m = gp.Model("city")


# Variables: which projects are chosen (1=yes, 0=no)
x = m.addVars(Projects, vtype=gp.GRB.BINARY,name="x")

# Objective: Maximize person-benefits
m.setObjective(x.prod(Beneficiaries), gp.GRB.MAXIMIZE)

# Constraint: At least one project suggested by each council member
m.addConstrs(sum(x[p] for p in Suggested[c]) >= 1 for c in Council)

# Constraint: Can't spend more than surplus
m.addConstr(x.prod(Cost) <= Surplus)

# Additional constraints
m.addConstr(x["Property"] <= x["Police"])
m.addConstr(x["Park"] <= x["Tax"])
m.addConstr(x["EV"] <= x["Tax"])
m.addConstr(x["Property"] + x["Tax"] <= 1)
m.addConstr(x["City Hall"] <= x["Potholes"])
m.addConstr(x["Park"] == x["Police"])


m.optimize()

print("***************** Solution *****************")
print(f"Total Beneficiaries: {round(m.ObjVal, 2)}")
for p in Projects:
    if x[p].X > 0.9999:
        print(f"Fund project {p}")
        
