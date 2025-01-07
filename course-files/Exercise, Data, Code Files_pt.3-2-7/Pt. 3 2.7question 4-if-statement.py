import gurobipy as gp
from gurobipy import GRB

import json

with open("question_four_data.json", "r") as f:
    data = json.load(f)

areas = data["areas"]
courses = data["courses"]
courses_areas = data["courses_areas"]


m = gp.Model("courses")


# Variables: Which courses are chosen?
x = m.addVars(courses, vtype=GRB.BINARY, name="x")


# Objective: minimize the number of courses chosen
m.setObjective(x.sum(),sense=GRB.MINIMIZE)


# Each area must be covered
m.addConstrs(sum(x[c] for c in courses if a in courses_areas[c]) >= 1 for a in areas)


m.optimize()

print("***************** Solution *****************")
print(f"Total courses selected: {round(m.ObjVal, 4)}")
for c in courses:
    if x[c].X > 0.5:
        print(f"Course {c} selected.")

