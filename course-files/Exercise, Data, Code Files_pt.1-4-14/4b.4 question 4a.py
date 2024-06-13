import gurobipy as gp
from gurobipy import GRB


M = ["Paper", "Glass", "Plastic"]
C = ["A", "B", "C", "D"]


m=gp.Model("recycle")


# Variables: Bundles sold to each large company
x = m.addVars(C, lb=100, vtype=gp.GRB.CONTINUOUS, name="x")

# Variables: Pounds of each material sold to small companies
y = m.addVars(M, vtype=gp.GRB.CONTINUOUS, name="y")


# Objective: Maximize revenue
m.setObjective(2*x["A"] + 3*x["B"] + 1*x["C"] + 2*x["D"] + 0.05*y["Paper"] + 0.03*y["Glass"] + 0.02*y["Plastic"], GRB.MAXIMIZE)


# Constraints: Sell all collected materials (in bundles and to small companies)
m.addConstr(5*x["A"] + 7*x["B"] + 2*x["C"] + 3*x["D"] + y["Paper"] == 15000)
m.addConstr(3*x["A"] + 3*x["B"] + 1*x["C"] + 1*x["D"] + y["Glass"] == 7000)
m.addConstr(1*x["A"] + 2*x["B"] + 1*x["C"] + 4*x["D"] + y["Plastic"] == 14000)


m.optimize()

print("***************** Solution *****************")
print(f"Total revenue: {round(m.ObjVal, 2)}")
for i in C:
    print(f"Sell {x[i].X} bundles to company {i}.")
for j in M:
    if y[j].X > 0:
        print(f"Sell {y[j].X} pounds of {j} to small recyclers.")
        
