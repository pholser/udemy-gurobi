import gurobipy as gp
from gurobipy import GRB

import json

# Select the correct file to open
#with open("question_four_data.json", "r") as f:
with open("question_five_data.json", "r") as f:
    data = json.load(f)
    

M = data["MfgSheet"]
L = data["WindowLengths"]
N = len(L)
d = data["Demand"]
P = data["Patterns"]
nP = len(P)

# Calculate scrap
s = [None] * nP
for j in range(nP):
        s[j] = M - sum(L[i]*P[j][i] for i in range(N))

f = data["ScrapCost"]


m = gp.Model("glass")


# Variables: Number of patterns cut of each type 
x = m.addVars(nP, vtype=GRB.INTEGER, name="x")


# Objective: Minimize cost of scrap from all patterns
m.setObjective(sum(f*s[j]*x[j] for j in range(nP)), GRB.MINIMIZE)


# Constraints: Cut the correct amount of windows of each size
m.addConstrs(sum(P[j][i]*x[j] for j in range(nP)) == d[i] for i in range(N))



m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for j in range(nP):
        if x[j].X > 0:
            print(f"Cut {x[j].X} patterns with:")
            for i in range(N):
                    print(f"...... {P[j][i]} windows of size {L[i]} feet")
            print(f"...... {s[j]} feet of scrap")
