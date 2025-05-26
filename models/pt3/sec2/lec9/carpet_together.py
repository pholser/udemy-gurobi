from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec9").joinpath("question_three_data-separate.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
roll_width = data["MfgRoll"]
purchase_widths = data["PurchaseLengths"]
demand = data["Demand"]
complete_patterns = data["Complete"]
incomplete_patterns = data["Incomplete"]
complete_scrap_cost = data["CompleteScrapCost"]
incomplete_scrap_cost = data["IncompleteScrapCost"]

def scrap(patterns):
    return [
        (roll_width
        -
        sum(k * purchase_widths[i] for i, k in enumerate(patterns[c])))
        for c in range(len(patterns))
    ]

complete_scraps = scrap(complete_patterns)
incomplete_scraps = scrap(incomplete_patterns)

# Model
model = gp.Model("carpet_together")

# Decisions
# How many rolls will I cut using what pattern?
cut_to_pattern = model.addVars(
    len(complete_patterns) + len(incomplete_patterns),
    lb=0,
    vtype=GRB.INTEGER
)

# Objective
# Minimize scrap costs
model.setObjective(
    sum(complete_scrap_cost * complete_scraps[i] * cut_to_pattern[i]
        for i in range(len(complete_patterns)))
    +
    sum(
        incomplete_scrap_cost
        * incomplete_scraps[j]
        * cut_to_pattern[len(complete_patterns) + j]
        for j in range(len(incomplete_patterns))),
    sense=GRB.MINIMIZE
)

# Constraints
# Meet demand for the cut rolls
meet_demand = model.addConstrs(
    (gp.quicksum(
        complete_patterns[i][j] * cut_to_pattern[i]
        for i in range(len(complete_patterns))))
    +
    (gp.quicksum(
        incomplete_patterns[i][j] * cut_to_pattern[len(complete_patterns) + i]
        for i in range(len(incomplete_patterns))))
    ==
    demand[j]
    for j in range(len(purchase_widths))
)

# Solve
model.optimize()

# Results
for i, p in enumerate(complete_patterns):
    print(f"Total {complete_patterns[i]} cut: {cut_to_pattern[i]}")
for j, p in enumerate(incomplete_patterns):
    print(f"Total {incomplete_patterns[j]} cut: {cut_to_pattern[len(complete_patterns) + j]}")
print(f"Objective value: {model.objVal}")
