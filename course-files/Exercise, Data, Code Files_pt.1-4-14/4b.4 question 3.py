import gurobipy as gp
from gurobipy import GRB

m=gp.Model("furniture")


N = 10
name = ["","beds","bookcases","chairs (dining room)","chairs (living room)", "chairs(office)", "coffee tables", "couches", "desks", "dining tables", "dressers"]


# Variables: Floor space for each type of furniture
x = m.addVars(range(1,N+1),lb=0.05,ub=1, vtype=gp.GRB.CONTINUOUS,name="x")


# Objective: Maximize marginal profit
m.setObjective(10*x[1] + 7*x[2] + 12*x[3] + 9*x[4] + 3*x[5] + 5*x[6] + 8*x[7] + 6*x[8] + 13*x[9] + 4*x[10], gp.GRB.MAXIMIZE)


# Constraints: Minimum floor space
m.addConstr(x[1] + x[10] >= 0.2) # Bedroom
m.addConstr(x[4] + x[6] + x[7] >= 0.2) # Living room
m.addConstr(x[3] + x[9] >= 0.15) # Dining room
m.addConstr(x[2] + x[5] + x[8] >= 0.1) # Office
m.addConstr(x[1] >= 0.1) # Beds
m.addConstr(x[3] + x[4] + x[5] + x[7] >= 0.5) # Seating
m.addConstr(x[6] + x[9] >= 0.1) # Tables
m.addConstr(x[2] + x[8] + x[10] >= 0.05) # Storage/Work

# Constraint: Dining tables must be 1.5 times the space for dining room chairs
m.addConstr(x[9] == 1.5*x[3])

# Constraint: All floor space adds up to 100%
m.addConstr(sum(x[i] for i in range(1,N+1)) == 1)


m.optimize()

print("***************** Solution *****************")
print(f"Total profit: {round(m.ObjVal, 2)}")
for i in range(1,N+1):
    print(f"Use {round(100*x[i].X,0)} percent of floor space on {name[i]}.")
