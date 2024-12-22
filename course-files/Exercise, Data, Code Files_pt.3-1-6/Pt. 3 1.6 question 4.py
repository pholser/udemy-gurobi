import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np


with open("question_four_data.json", "r") as f:
    data = json.load(f)

Experts = data["Experts"]
Familiarities = data["Familiarities"]
Categories = data["Experience Categories"]
Levels = data["Levels"]
Countries = data["Countries"]

# Determine the number of experts available
N = len(Experts)


m = gp.Model("focus")


# Variables: which experts are chosen? (1=yes, 0=no)
x = m.addVars(N, vtype=GRB.BINARY,name="x")


# Objective: minimize the cost of the experts
m.setObjective(sum(x[i]*Experts[i]["Cost"] for i in range(N)))


# Constraints: Minimum and maximum of each familiarity
m.addConstrs(sum(x[i] for i in range(N) if Experts[i]["Familiarity"] == Familiarities[j]["Description"]) >= Familiarities[j]["Minimum"] for j in range(len(Familiarities)))
m.addConstrs(sum(x[i] for i in range(N) if Experts[i]["Familiarity"] == Familiarities[j]["Description"]) <= Familiarities[j]["Maximum"] for j in range(len(Familiarities)))

# Constraints: At least one of each experience level
m.addConstrs(sum(x[i] for i in range(N) if Experts[i]["Experience"] >= Categories[j]["Range"][0] and Experts[i]["Experience"] <= Categories[j]["Range"][1]) >= 1 for j in range(len(Categories)))
    
# Constraints: At least one of each job level
m.addConstrs(sum(x[i] for i in range(N) if Experts[i]["Level"] == j) >= 1 for j in Levels)
                 
# Constraints: At least one from each country
m.addConstrs(sum(x[i] for i in range(N) if Experts[i]["Country"] == j) >= 1 for j in Countries)

# Constraint: 4 and 8 don't get along with 10
# Note: These are indices 3, 7, and 9 when starting with index 0
m.addConstr(x[3] + x[9] <= 1)
m.addConstr(x[7] + x[9] <= 1)
               

m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for i in range(N):
    if x[i].X > 0.9999:
        print(f"Use expert {i+1}")
        
