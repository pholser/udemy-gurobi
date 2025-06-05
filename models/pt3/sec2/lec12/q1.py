from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_one_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
wait_times = data["numbers"]
drivers = list(range(len(wait_times)))
riders = list(range(len(wait_times[0])))

# Model
model = gp.Model("drivers")

# Decisions
# How fo I pair up drivers and riders?
pairings = model.addVars(
    len(drivers),
    len(riders),
    vtype=GRB.BINARY
)

# Objective
# Minimize wait times
model.setObjective(
    sum(wait_times[d][r] * pairings[d, r]
        for d in range(len(drivers))
        for r in range(len(riders))),
    sense=GRB.MINIMIZE
)

# Constraints
# Every driver paired with exactly one rider
driver_single_rider = model.addConstrs(
    (pairings.sum(d, "*") == 1 for d in range(len(drivers)))
)
# Every rider paired with exactly one driver
rider_single_driver = model.addConstrs(
    (pairings.sum("*", r) == 1 for r in range(len(riders)))
)

# Solve
model.optimize()

# Results
for d in range(len(drivers)):
    for r in range(len(riders)):
        if pairings[d, r].X == 1:
            print(f"Pair driver {d} with rider {r}: {wait_times[d][r]}")
print(f"Total wait time: {model.objVal}")
