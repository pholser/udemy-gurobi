import gurobipy as gp
from gurobipy import GRB

import json

with open("question_three_data.json", "r") as f:
    data = json.load(f)

NumPapers = data["NumPapers"]
Papers = data["Papers"]
OldPulpQualities = data["OldPulpQualities"]
NewPulpMinimums = data["NewPulpMinimums"]
NewPulpMaximums = data["NewPulpMaximums"]
PaperReceived = data["PaperReceived"]
SellPrice = data["SellPrice"]


m = gp.Model("bronze")


# Variables: Tons of each old paper quality used to produce each new paper quality each day
x = m.addVars(NumPapers, NumPapers, vtype=GRB.CONTINUOUS, name="x")

# Variables: Tons of each new paper quality produced each day
y = m.addVars(NumPapers, vtype=GRB.CONTINUOUS, name="y")


# Objective: Maximize revenue
m.setObjective(y.prod(SellPrice), GRB.MAXIMIZE)


# Constraints: Must recycle all paper received
m.addConstrs(sum(x[i,j] for j in range(NumPapers)) == PaperReceived[i] for i in range(NumPapers))

# Constraints: Quality rating for each type of new paper must be between minimum and maximum
m.addConstrs(sum(OldPulpQualities[i]*x[i,j] for i in range(NumPapers)) >= NewPulpMinimums[j] * y[j] for j in range(NumPapers))
m.addConstrs(sum(OldPulpQualities[i]*x[i,j] for i in range(NumPapers)) <= NewPulpMaximums[j] * y[j] for j in range(NumPapers))

# Constraints: New paper produced equals total old paper used to make it
m.addConstrs(y[j] == sum(x[i,j] for i in range(NumPapers)) for j in range(NumPapers))


m.optimize()

print("***************** Solution *****************")
print(f"Total Revenue: {round(m.ObjVal, 2)}")
for j in range(NumPapers):
    for i in range(NumPapers):
        if x[i,j].X > 0:
            print(f"Use {x[i,j].X} tons of {Papers[i]} to make {Papers[j]} per day")
for j in range(NumPapers):
    if y[j].X > 0:
        print(f"Make {y[j].X} tons of {Papers[j]} per day (Quality = {sum(OldPulpQualities[i]*x[i,j].X for i in range(NumPapers)) / y[j].X})")
