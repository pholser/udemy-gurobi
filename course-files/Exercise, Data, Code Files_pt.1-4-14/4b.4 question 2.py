import gurobipy as gp
from gurobipy import GRB


m=gp.Model("metal")


# Variables: Tons of alloy produced by each process
x = m.addVars(range(1,3), lb=0, vtype=gp.GRB.CONTINUOUS, name="x")


# Objective: Minimize production cost
m.setObjective(28*x[1] + 53*x[2], gp.GRB.MINIMIZE)


# Constraint: Yearly requirement
m.addConstr(x[1] + x[2] >= 3400)

# Constraint: Process 1 is at most 2/3 of total production
m.addConstr(x[1] <= 2*x[2])

# Constraint: Pollution limit
m.addConstr(90*x[1] + 50*x[2] <= 200000)


m.optimize()

print("***************** Solution *****************")
print(f"Total cost: {round(m.ObjVal, 2)}")
for i in range(1,3):
    print(f"Run process {i} to produce {x[i].X} tons of alloy.")
