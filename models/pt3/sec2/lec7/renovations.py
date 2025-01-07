from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec7").joinpath("renovations.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
renovations = data["renovations"]
number_of_renovations = len(renovations)
costs = [r["cost"] for r in renovations]
values = [r["resale-value"] - r["cost"] for r in renovations]
budget = data["budget"]

# Model
model = gp.Model("renovations")

# Decisions
x = model.addVars(number_of_renovations, vtype=GRB.BINARY, name="x")

# Objective
model.setObjective(x.prod(values), sense=GRB.MAXIMIZE)

# Constraints
budget_constraint = model.addConstr(
    gp.quicksum(x[r] * costs[r] for r in range(number_of_renovations)) <= budget
)

# Solve
model.optimize()

# Show results
for i, r in enumerate(renovations):
    print(f"Perform renovation {r}: {x[i]}")
print(f"Objective value: {model.objVal}")
