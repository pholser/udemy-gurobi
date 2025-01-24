import gurobipy as gp
from gurobipy import GRB

import json

with open("question_two_data.json", "r") as f:
    data = json.load(f)

NumRawMetals = data["NumRawMetals"]
RawMetals = data["RawMetals"]

NumBronzes = data["NumBronzes"]
Bronzes = data["Bronzes"]
MinCopper = data["MinCopper"]
MaxCopper = data["MaxCopper"]
SellPrice = data["SellPrice"]

NumExtractions = data["NumExtractions"]
Extractions = data["Extractions"]
WorkersNeeded = data["WorkersNeeded"]
WorkersAvailable = data["WorkersAvailable"]
RockNeeded = data["RockNeeded"]
RockAvailable = data["RockAvailable"]

RawMetalsProduced = data["RawMetalsProduced"]


m = gp.Model("bronze")


# Variables: Hours of each extraction process per day
x = m.addVars(NumExtractions, ub=24, vtype=GRB.CONTINUOUS, name="x")

# Variables: Pounds of each raw metal extracted per day
y = m.addVars(NumRawMetals, vtype=GRB.CONTINUOUS, name="y")

# Variables: Pounds of each grade of bronze produced per day
z = m.addVars(NumBronzes, vtype=GRB.CONTINUOUS, name="z")

# Variables: Pounds of each raw metal used to produce each grade of bronze per day
w = m.addVars(NumRawMetals, NumBronzes, vtype=GRB.CONTINUOUS, name="w")


# Objective: Maximize revenue
m.setObjective(z.prod(SellPrice), GRB.MAXIMIZE)


# Constraints: Can't use more worker-hours or rock than is available
m.addConstr(x.prod(WorkersNeeded) <= WorkersAvailable)
m.addConstr(x.prod(RockNeeded) <= RockAvailable)

# Constraints: Raw metals produced equals total raw metals extracted
m.addConstrs(sum(RawMetalsProduced[j][i] * x[j] for j in range(NumExtractions)) == y[i] for i in range(NumRawMetals))

# Constraints: Can't use more raw metals than amount produced
m.addConstrs(sum(w[j,k] for k in range(NumBronzes)) <= y[j] for j in range(NumRawMetals))

# Constraints: Copper content for each grade of bronze must be between min and max
m.addConstrs(w[0,k] >= MinCopper[k] * z[k] for k in range(NumBronzes))
m.addConstrs(w[0,k] <= MaxCopper[k] * z[k] for k in range(NumBronzes))

# Constraints: Bronze produced of each grade equals total raw metals used to make it
m.addConstrs(z[k] == sum(w[j,k] for j in range(NumRawMetals)) for k in range(NumBronzes))


m.optimize()

print("***************** Solution *****************")
print(f"Total Revenue: {round(m.ObjVal, 2)}")
for i in range(NumExtractions):
    if x[i].X > 0:
        print(f"Run {Extractions[i]} for {x[i].X} hours per day")
for j in range(NumRawMetals):
    if y[j].X > 0:
        print(f"Extract {y[j].X} pounds of {RawMetals[j]} per day")
for k in range(NumBronzes):
    for j in range(NumRawMetals):
        if w[j,k].X > 0:
            print(f"Use {w[j,k].X} pounds of {RawMetals[j]} to make {Bronzes[k]} bronze per day")
for k in range(NumBronzes):
    if z[k].X > 0:
        print(f"Sell {z[k].X} pounds of {Bronzes[k]} bronze per day")
