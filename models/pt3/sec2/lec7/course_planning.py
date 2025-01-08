from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec7").joinpath("course-planning.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
areas = data["areas"]
A = len(areas)
courses = data["courses"]
C = len(courses)

# Model
model = gp.Model("course-planning")

# Decisions
# Whether or not to select a course
x = model.addVars(C, vtype=GRB.BINARY, name="x")

# Objective
# Register for as few courses as possible
model.setObjective(x.sum(), sense=GRB.MINIMIZE)

# Constraints
# Every subject area must be covered by at least one registered-for course
subject_areas_covered = model.addConstrs(
    (sum(x[c]
         for c in range(C)
         if i in courses[c]["applicable-areas"]) >= 1
    ) for (i, a) in enumerate(areas)
)

# Solve
model.optimize()

# Show results
for i, c in enumerate(courses):
    print(f"Include course {c}: {x[i]}")
print(f"Objective value: {model.objVal}")
