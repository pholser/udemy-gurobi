from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec9").joinpath("question_five_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
raw_sheet_length = data["MfgSheet"]
window_lengths = data["WindowLengths"]
demand = data["Demand"]
patterns = data["Patterns"]
scrap_cost = data["ScrapCost"]

def scrap(patterns):
    return [
        (raw_sheet_length
        -
        sum(k * window_lengths[i] for i, k in enumerate(patterns[p])))
        for p in range(len(patterns))
    ]

scraps = scrap(patterns)

# Model
model = gp.Model("float_glass")

# Decisions
# How many sheets will I cut using what pattern?
cut_to_pattern = model.addVars(
    len(patterns),
    lb=0,
    vtype=GRB.INTEGER
)

# Objective
# Minimize scrap costs
model.setObjective(
    sum(scrap_cost * scraps[i] * cut_to_pattern[i]
        for i in range(len(patterns))),
    sense=GRB.MINIMIZE
)

# Constraints
# Meet demand for the cut glass
meet_demand = model.addConstrs(
    (gp.quicksum(patterns[i][j] * cut_to_pattern[i]
                 for i in range(len(patterns))))
    ==
    demand[j]
    for j in range(len(window_lengths))
)

# Solve
model.optimize()

# Results
for i, p in enumerate(patterns):
    print(f"Total {patterns[i]} cut: {cut_to_pattern[i]}")
print(f"Objective value: {model.objVal}")
