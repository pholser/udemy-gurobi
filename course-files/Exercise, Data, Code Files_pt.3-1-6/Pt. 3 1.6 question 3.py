import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np


with open("question_three_data.json", "r") as f:
    data = json.load(f)

Countries = data["Countries"]
Adjacencies = data["Adjacencies"]

    
# At worst every country is its own color, so the number of colors to consider is equal to the number of countries
Colors = len(Countries)


m = gp.Model("heirs")


# Variables: which color is used for each country? (1=yes, 0=no)
x = m.addVars(Countries, Colors, vtype=gp.GRB.BINARY,name="x")

# Variables: which colors are used (1=yes, 0=no)
y = m.addVars(Colors, vtype=gp.GRB.BINARY,name="y")

# Objective: minimize the number of colors used
m.setObjective(y.sum())

# Constraint: Every country is exactly one color
m.addConstrs(sum(x[i,j] for j in range(Colors)) == 1 for i in Countries)

# Constraint: No pair of adjacent countries can be the same color
m.addConstrs(x[i,j] + x[k,j] <= 1 for (i,k) in Adjacencies for j in range(Colors))

# Constraint: A color is used if any country is that color
m.addConstrs(x[i,j] <= y[j] for i in Countries for j in range(Colors))

# Constraint: Put the used colors first
#m.addConstrs(y[j-1] >= y[j] for j in range(1,Colors))


m.optimize()

print("***************** Solution *****************")
print(f"Total Colors Used: {round(m.ObjVal, 2)}")
for i in Countries:
    for j in range(Colors):
        if x[i,j].X > 0.9999:
            print(f"Country {i} is color {j+1}")
        
