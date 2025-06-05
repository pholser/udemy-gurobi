import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_one_data.json", "r") as f:
    data = json.load(f)

times = data["numbers"]
num_drivers = len(times)
num_riders = len(times[0])


m = gp.Model("driver_assignment")


# Variables: x_dr = 1 if driver d is assigned to rider r
x = m.addVars(num_drivers, num_riders, vtype=GRB.BINARY, name="x")


# Objective: Minimize total time to pickups
m.setObjective(sum(times[d][r]*x[(d,r)] for d in range(num_drivers) for r in range(num_riders)), sense=GRB.MINIMIZE)


# Constraints: Each driver is assigned to one rider
m.addConstrs(
    (x.sum(i, "*") == 1 for i in range(num_drivers))
)
# Constraints: Each rider needs one driver
m.addConstrs(
    (x.sum("*", j) == 1 for j in range(num_riders))
)


m.optimize()


print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (d,r) in product(range(num_drivers),range(num_riders)):
            if x[(d,r)].X > 0.5:
                print(f"Assign driver {d+1} to rider {r+1}.")
