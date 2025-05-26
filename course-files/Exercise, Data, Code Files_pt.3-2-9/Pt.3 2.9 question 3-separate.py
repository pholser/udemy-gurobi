import gurobipy as gp
from gurobipy import GRB

import json

with open("question_three_data-separate.json", "r") as f:
    data = json.load(f)
    

M = data["MfgRoll"]
L = data["PurchaseLengths"]
N = len(L)
d = data["Demand"]
PC = data["Complete"]
nC = len(PC)
PI = data["Incomplete"]
nI = len(PI)

# Calculate scrap
sC = [None] * nC
for j in range(nC):
	sC[j] = M - sum(L[i]*PC[j][i] for i in range(N))
sI = [None] * nI
for j in range(nI):
	sI[j] = M - sum(L[i]*PI[j][i] for i in range(N))

fC = data["CompleteScrapCost"]
fI = data["IncompleteScrapCost"]


m = gp.Model("carpet")


# Variables: Number of complete patterns cut of each type
xC = m.addVars(nC, vtype=GRB.INTEGER, name="xC")

# Variables: Number of incomplete patterns cut of each type
xI = m.addVars(nI, vtype=GRB.INTEGER, name="xI")


# Objective: Minimize cost of scrap from complete and incomplete patterns
m.setObjective(sum(fC*sC[j]*xC[j] for j in range(nC)) + sum(fI*sI[j]*xI[j] for j in range(nI)), GRB.MINIMIZE)


# Constraints: Cut the correct amount of purchased rolls of each size
m.addConstrs(sum(PC[j][i]*xC[j] for j in range(nC)) + sum(PI[j][i]*xI[j] for j in range(nI)) == d[i] for i in range(N))



m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for j in range(nC):
        if xC[j].X > 0:
            print(f"Cut {xC[j].X} complete patterns with:")
            for i in range(N):
                    print(f"...... {PC[j][i]} rolls of size {L[i]} feet")
            print(f"...... {sC[j]} feet of scrap")
for j in range(nI):
        if xI[j].X > 0:
            print(f"Cut {xI[j].X} incomplete patterns with:")
            for i in range(N):
                    print(f"...... {PI[j][i]} rolls of size {L[i]} feet")
            print(f"...... {sI[j]} feet of scrap")
        

