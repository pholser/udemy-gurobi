import gurobipy as gp
from gurobipy import GRB

import json

with open("question_one_data.json", "r") as f:
    data = json.load(f)

B = data["B"]
N = data["N"]
P = data["profits"]
L = data["L"]
R = data["R"]
Mmax = data["M"]
Mmin = data["m"]
cities = data["cities"]

m=gp.Model("investment")


# Variables: Money (in millions of dollars) invested in each city
x = m.addVars(N, lb=Mmin, ub=Mmax, name="x")


# Objective: Maximize predicted increase in value
m.setObjective(gp.quicksum(P[j]*x[j] for j in range(N)), gp.GRB.MAXIMIZE)
# alternative code: m.setObjective(x.prod(P), GRB.MAXIMIZE)


# Constraint: Spend no more than B
m.addConstr(gp.quicksum(x[j] for j in range(N)) <= B, name="budget")
# alternative code: m.addConstr(x.sum() <= B)

# Constraint: Limit spending in each region
m.addConstrs((gp.quicksum(x[j] for j in R[r]) <= L[r] for r in range(len(R))), name="region")

# Constraint: Limit spending in each city
# already accounted for by the lb and ub parameters in the variable declaration

# Constraint: Non-negativity
# already accounted for in the variable declaration


m.optimize()

print("***************** Solution *****************")
print(f"Total predicted value increase: {round(m.ObjVal, 2)}")
for i in range(N):
    print(f"Invest {x[i].X} million dollars in city {cities[i]}.")
