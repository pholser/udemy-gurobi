import gurobipy as gp
from gurobipy import GRB

import json

with open("question_nine_data.json", "r") as f:
    data = json.load(f)
    

T = data["TruckSizes"]
NT = len(T)
L = data["LoadSizes"]
NL = len(L)
d = data["Demand"]
P = data["Patterns"]
NP = [None] * NT
for t in range(NT):
        NP[t] = len(P[t])
c = data["TruckCosts"]


m = gp.Model("truck")


# Create variables for each pattern for each truck
x = m.addVars([(t,p) for t in range(NT) for p in range(NP[t])], vtype=GRB.BINARY, name="x")


# Objective: Minimize cost of trucks used
m.setObjective(sum(c[t]*x[t,p] for t in range(NT) for p in range(NP[t])), GRB.MINIMIZE)


# Constraints: Ship the correct amount of each load
m.addConstrs(sum(P[t][p][l]*x[t,p] for t in range(NT) for p in range(NP[t])) == d[l] for l in range(NL))


m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for t in range(NT):
        for p in range(NP[t]):
                if x[t,p].X > 0:
                        print(f"Send {x[t,p].X} trucks of size {T[t]} with:")
                        for l in range(NL):
                                print(f"...... {P[t][p][l]} loads of size {L[l]}")
                        print(f"...... {T[t] - sum(P[t][p][l]*L[l] for l in range(NL))} empty")
