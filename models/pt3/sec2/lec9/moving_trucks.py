from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec9").joinpath("question_seven_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
truck_size = data["TruckSize"]
load_sizes = data["LoadSizes"]
demand = data["Demand"]
patterns = data["Patterns"]
truck_cost = data["TruckCost"]

# Model
model = gp.Model("float_glass")

# Decisions
# How many of each load pattern will I load into a truck?
patterns_loaded = model.addVars(
    len(patterns),
    lb=0,
    vtype=GRB.INTEGER
)

# Objective
# Minimize cost of trucks used
model.setObjective(
    sum(truck_cost * patterns_loaded[i]
        for i in range(len(patterns))),
    sense=GRB.MINIMIZE
)

# Constraints
# Meet delivery demand
meet_demand = model.addConstrs(
    sum(patterns[i][j] * patterns_loaded[i]
        for i in range(len(patterns)))
    ==
    demand[j]
    for j in range(len(load_sizes))
)

# Solve
model.optimize()

# Results
for i, p in enumerate(patterns):
    print(f"Total {patterns[i]} cut: {patterns_loaded[i]}")
print(f"Objective value: {model.objVal}")
