import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_two_data.json", "r") as f:
    data = json.load(f)

employees = data["left_nodes"]
available = data["supplies"]
jobs = data["right_nodes"]
needed = data["demands"]
values = data["numbers"]


m = gp.Model("job-hour_assignment")


# Variables: x_ij: number of hours spent by employee i on job j
x = m.addVars(employees, jobs, vtype=GRB.INTEGER, name="x")


# Objective: Minimize total cost
m.setObjective(sum(values[employees.index(i)][jobs.index(j)]*x[(i,j)] for i in employees for j in jobs), sense=GRB.MAXIMIZE)


# Constraints: Each employee can work a certain number of hours
m.addConstrs((x.sum(i, "*") == available[i] for i in employees))

# Each job requires certain number of hours
m.addConstrs((x.sum("*", j) == needed[j] for j in jobs))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(employees, jobs):
    if x[i, j].X > 0:
        print(f"employee {i} should spend {x[i, j].X} hours on job {j}.")
