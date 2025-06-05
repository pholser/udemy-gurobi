import gurobipy as gp
from gurobipy import GRB

from itertools import product

import json

with open("question_three_data.json", "r") as f:
    data = json.load(f)

profs = data["profs"]
loads = data["loads"]
courses = data["courses"]
needs = data["needs"]
ratings = data["ratings"]


m = gp.Model("course_assignment")


# Variables: x_ij: 1 if prof i teaches course j, 0 if not
x = m.addVars(profs, courses, vtype=GRB.INTEGER, name="x")


# Objective: Maximize total rating
m.setObjective(sum(ratings[profs.index(i)][courses.index(j)]*x[(i,j)] for i in profs for j in courses), sense=GRB.MAXIMIZE)


# Constraints: Each prof teaches a certain number of courses
m.addConstrs((x.sum(i, "*") == loads[profs.index(i)] for i in profs))

# Each course has a certain number of sections offered
m.addConstrs((x.sum("*", j) == needs[courses.index(j)] for j in courses))


m.optimize()

print("***************** Solution *****************")
print(f"Total value: {round(m.ObjVal, 4)}")
for (i, j) in product(profs, courses):
    if x[i, j].X > 0:
        print(f"Professor {i} should teach {x[i, j].X} sections of course {j}.")
