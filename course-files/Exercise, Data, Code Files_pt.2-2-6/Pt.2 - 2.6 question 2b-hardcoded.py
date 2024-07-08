import gurobipy as gp
from gurobipy import GRB


m = gp.Model("market")


# Variables: Which datasets are purchased? (1=yes, 0=no)
x = m.addVars(range(1,13), vtype=GRB.BINARY, name="x")


# Objective: Minimize spend
m.setObjective(1.1*x[1] + 0.5*(8-(x[1] + x[3] + x[4] + x[5] + x[6] + x[7] +
                                  x[8] + x[9] + x[10] + x[11] + x[12])) +
               0.2*x[3] + 0.7*x[4] + 1.1*x[5] + 0.9*x[6] + 1.0*x[7] +
               1.6*x[8] + 0.8*x[9] + 0.5*x[10] + 0.7*x[11] + 1.0*x[12])


# Constraints: Minimum data sets of each type and region
m.addConstr(x[4] + x[5] + x[6] + x[8] >= 2) # Credit
m.addConstr(x[3] + x[10] >= 1) # Housing
m.addConstr(x[9] + x[11] + x[12] >= 1) # Online retail
m.addConstr(x[1] + (8-(x[1] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] +
                       x[9] + x[10] + x[11] + x[12]))
            + x[7] + x[8] >= 1) # Retail
m.addConstr(x[1] + (8-(x[1] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] +
                       x[9] + x[10] + x[11] + x[12]))
            + x[7] + x[8] + x[9] + x[11] + x[12] >= 3) # Total retail
m.addConstr(x[1] + x[5] + x[8] + x[10] + x[12] >= 2) # USA
m.addConstr(x[3] + x[9] >= 1) # Canada
m.addConstr((8-(x[1] + x[3] + x[4] + x[5] + x[6] + x[7] + x[8] + x[9] +
                x[10] + x[11] + x[12]))
            + x[4] + x[11] >= 2) # Europe
m.addConstr(x[6] + x[7] >= 1) # Japan

    
# Constraints: Purchase exactly 8 datasets
#m.addConstr(x.sum() == 8)


m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for i in range(1,13):
    if x[i].X > 0.9999:
        print(f"Purchase dataset {i}")
