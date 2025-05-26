import gurobipy as gp
from gurobipy import GRB

import json

with open("question_three_data-together.json", "r") as f:
    data = json.load(f)
    

M = data["MfgRoll"]
L = data["PurchaseLengths"]
N = len(L)
d = data["Demand"]
P = data["Patterns"]
nP = len(P)

# Calculate scrap and whether each pattern is complete or incomplete
s = [None] * nP
T = [None] * nP
for j in range(nP):
        s[j] = M - sum(L[i]*P[j][i] for i in range(N))
        if s[j] < min(L):
                T[j] = 0 # T[j] == 0 means Complete
        else:
                T[j] = 1 # T[j] == 1 means Incomplete

f = [data["CompleteScrapCost"], data["IncompleteScrapCost"]]


m = gp.Model("carpet")


# Variables: Number of patterns cut of each type
x = m.addVars(nP, vtype=GRB.INTEGER, name="x")


# Objective: Minimize cost of scrap from all patterns
m.setObjective(sum(f[T[j]]*s[j]*x[j] for j in range(nP)), GRB.MINIMIZE)


# Constraints: Cut the correct amount of purchased rolls of each size
m.addConstrs(sum(P[j][i]*x[j] for j in range(nP)) == d[i] for i in range(N))



m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for j in range(nP):
        if x[j].X > 0:
            print(f"Cut {x[j].X} complete patterns with:")
            for i in range(N):
                    print(f"...... {P[j][i]} rolls of size {L[i]} feet")
            print(f"...... {s[j]} feet of scrap")
