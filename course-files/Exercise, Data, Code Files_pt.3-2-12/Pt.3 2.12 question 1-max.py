import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_one_data.json", "r") as f:
    data = json.load(f)

values = data["numbers"]
num_people = len(values)
num_projects = len(values[0])


m = gp.Model("project_assignment")


# Variables: x_ij = 1 if person i is assigned to project j
x = m.addVars(num_people, num_projects, vtype=GRB.BINARY, name="x")


# Objective: Maximize total value on projects
m.setObjective(sum(values[i][j]*x[(i,j)] for i in range(num_people) for j in range(num_projects)), sense=GRB.MAXIMIZE)


# Constraints: Each person is assigned to one project
m.addConstrs(
    (x.sum(i, "*") == 1 for i in range(num_people))
)

# Constraints: Each project needs one person
m.addConstrs(
    (x.sum("*", j) == 1 for j in range(num_projects))
)


m.optimize()


print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(range(num_people), range(num_projects)):
    if x[i, j].X > 0.5:
        print(f"Assign person {i+1} to project {j+1}.")
