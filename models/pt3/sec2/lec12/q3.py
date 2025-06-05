from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_three_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
ratings = data["ratings"]
profs = data["profs"]
prof_loads = data["loads"]
courses = data["courses"]
course_needs = data["needs"]

# Model
model = gp.Model("courses")

# Decisions
# How fo I pair up professors and courses?
prof_course_assignment = model.addVars(
    profs,
    courses,
    vtype=GRB.INTEGER
)

# Objective
# Maximize student rating
model.setObjective(
    sum(ratings[profs.index(p)][courses.index(c)] * prof_course_assignment[p, c]
        for p in profs
        for c in courses),
    sense=GRB.MAXIMIZE
)

# Constraints
prof_loads_respected = model.addConstrs(
    (prof_course_assignment.sum(p, "*") == prof_loads[profs.index(p)]
     for p in profs)
)

course_needs_respected = model.addConstrs(
    (prof_course_assignment.sum("*", c) == course_needs[courses.index(c)]
     for c in courses)
)

# Solve
model.optimize()

# Results
for p in profs:
    for c in courses:
        if prof_course_assignment[p, c].X > 0.5:
            print(f"Professor {p} teaches course {c}")
print(f"Rating: {model.objVal}")
