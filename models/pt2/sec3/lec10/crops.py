import gurobipy as gp
from gurobipy import GRB
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt2.sec3.lec10").joinpath("crops.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
crops = data["crops"]
acreage = data["acreage"]
labor_hours = data["available_labor_hours"]
fertilizer_tons = data["available_tons_of_fertilizer"]

model = gp.Model("crops")

# Decision: how many acres to plant for each crop
acres_planted = model.addVars(
    len(crops),
    vtype=GRB.CONTINUOUS,
    name="acres_planted"
)

# Objective: maximize total profit
model.setObjective(
    gp.quicksum(
        acres_planted[i] * crops[i]["profit_per_acre_planted"]
        for i in range(len(crops))
    ),
    sense=GRB.MAXIMIZE
)

# Constraint: labor hours
labor_constraint = model.addConstr(
    gp.quicksum(
        acres_planted[i] * crops[i]["labor_hours_per_acre_planted"]
        for i in range(len(crops))
    ) <= labor_hours,
    name="labor_constraint"
)

# Constraint: fertilizer
fertilizer_constraint = model.addConstr(
    gp.quicksum(
        acres_planted[i] * crops[i]["tons_of_fertilizer_per_acre_planted"]
        for i in range(len(crops))
    ) <= fertilizer_tons,
    name="fertilizer_constraint"
)

# Constraint: acreage
acreage_constraint = model.addConstr(
    acres_planted.sum() <= acreage,
    name="acreage_constraint"
)

# Solve
model.optimize()

# Output
for i in range(len(crops)):
    print(f"Plant {acres_planted[i].X} acres of {crops[i]['name']}")
print(f"Total profit: {model.objVal}")
