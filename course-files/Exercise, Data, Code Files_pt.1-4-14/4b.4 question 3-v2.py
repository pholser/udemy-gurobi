import gurobipy as gp
from gurobipy import GRB


import json

with open("question_two_data.json", "r") as f:
    data = json.load(f)


Furniture = data["Furniture"]
F_mins = data["Fmins"]
M_Profit = data["MarginalProfit"]
Categories = data["Categories"]
C_mins = data["Cmins"]
Classifications = data["Classifications"]
Extra = data["ExtraGeqConstraints"]

m=gp.Model("furniture")


# Variables: Floor space for each type of furniture
x = m.addVars(Furniture, lb=F_mins, ub=1, vtype=gp.GRB.CONTINUOUS, name="x")


# Objective: Maximize marginal profit
m.setObjective(x.prod(M_Profit), gp.GRB.MAXIMIZE)


# Constraints: Minimum floor space for each category
m.addConstrs(sum(x[i] for i in Furniture if j in Classifications[i]) >= C_mins[j] for j in Categories)

# Constraint: All floor space adds up to 100%
m.addConstr(x.sum() == 1)

# This model has an additional greater-than-or-equal-to constraint
# that doesn't fit nicely into any of the other families of constraints
# for this type of problem, so the information for this constraint
# is in the list "ExtraGeqConstraints"
m.addConstrs(Extra[j][0] * x[Extra[j][1]] >= Extra[j][2] * x[Extra[j][3]] for j in Extra)


m.optimize()

print("***************** Solution *****************")
print(f"Total profit: {round(m.ObjVal, 2)}")
for i in Furniture:
    print(f"Use {round(100*x[i].X,0)} percent of floor space on {i}.")
