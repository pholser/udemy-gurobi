import gurobipy as gp
from gurobipy import GRB

import json

with open("question_seven_data.json", "r") as f:
    data = json.load(f)
    

T = data["TruckSize"]
L = data["LoadSizes"]
NL = len(L)
d = data["Demand"]
P = data["Patterns"]
NP = len(P)
c = data["TruckCost"]


m = gp.Model("truck")


# Variables: Number of patterns of used of each type
x = m.addVars(NP, vtype=GRB.INTEGER, name="x")


# Objective: Minimize cost of trucks used
m.setObjective(sum(c*x[p] for p in range(NP)), GRB.MINIMIZE)


# Constraints: Ship the correct amount of each load size
m.addConstrs(sum(P[p][l]*x[p] for p in range(NP)) == d[l] for l in range(NL))



m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for p in range(NP):
        if x[p].X > 0:
            print(f"Send {x[p].X} trucks with:")
            for l in range(NL):
                    print(f"...... {P[p][l]} loads of size {L[l]}")
            print(f"...... {T - sum(L[l]*P[p][l] for l in range(NL))} empty")
