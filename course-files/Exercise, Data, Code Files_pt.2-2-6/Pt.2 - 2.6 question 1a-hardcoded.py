import gurobipy as gp
from gurobipy import GRB

N = 4 # 0 = trumpets, 1 = flugelhorns, 2 = baritones, 3 = contrabasses
InstType = ["Trumpets", "Flugelhorns", "Baritones", "Contrabasses"]

m = gp.Model("music")


# Variables: How many of each instrument to make (include maximum amounts here as upper bounds)
x = m.addVars(4, vtype=GRB.INTEGER,name="x")


# Objective: maximize profit
m.setObjective(600*x[0] + 700*x[1] + 1000*x[2] + 1500*x[3],GRB.MAXIMIZE)


# Constraints: Machine time limits
m.addConstr(10*x[0] + 8*x[1] + 12*x[2] + 15*x[3] <= 2000)
m.addConstr(20*x[0] + 20*x[1] + 20*x[2] + 20*x[3] <= 3000)
m.addConstr(10*x[0] + 12*x[1] + 15*x[2] + 20*x[3] <= 2000)

# Constraints: Total Manufactured must be 150 by contract
m.addConstr(x.sum() == 150)
               
# Constraints: Don't produce more than allowed of any instrument
m.addConstr(x[0] <= 100)
m.addConstr(x[1] <= 40)
m.addConstr(x[2] <= 40)
m.addConstr(x[3] <= 20)


m.optimize()

print("***************** Solution *****************")
print(f"Total Profit: {round(m.ObjVal, 2)}")
for i in range(N):
    print(f"Manufacture {x[i].X} {InstType[i]}")
        
