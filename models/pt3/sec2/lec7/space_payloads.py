from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec7").joinpath("payloads.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
payloads = data["payloads"]
number_of_payloads = len(payloads)
revenues = [p["revenue"] for p in payloads]
weights = [p["weight"] for p in payloads]
max_weight = data["max-weight"]

# Model
model = gp.Model("space_payloads")

# Decisions
x = model.addVars(number_of_payloads, vtype=GRB.BINARY, name="x")

# Objective
model.setObjective(x.prod(revenues), sense=GRB.MAXIMIZE)

# Constraints
weight_constraint = model.addConstr(
    gp.quicksum(x[p] * weights[p] for p in range(number_of_payloads)) <= max_weight
)

# Solve
model.optimize()

# Show results
for i, p in enumerate(payloads):
    print(f"Take payload {p}: {x[i]}")
print(f"Objective value: {model.objVal}")
