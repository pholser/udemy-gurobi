from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec7").joinpath("project-staffing.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
people = data["people"]
P = len(people)
skills = data["skills"]

# Model
model = gp.Model("project-staffing")

# Decisions
# Whether or not to include a person on the project
x = model.addVars(P, vtype=GRB.BINARY, name="x")

# Objective
# Keep team size small
model.setObjective(x.sum())

# Constraints
# There must be at least one person with a given skill on project
for s in skills:
    model.addConstr(
        gp.quicksum(x[p - 1] for p in s["skilled-people"]) >= 1,
        name=f"{s['name']}_skill_constraint"
    )

# Solve
model.optimize()

# Show results
for i, p in enumerate(people):
    print(f"Include {p} on project: {x[i]}")
print(f"Objective value: {model.objVal}")
