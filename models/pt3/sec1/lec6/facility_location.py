from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json
import pandas as pd


data_file_path = rsrc.files("models.pt3.sec1.lec6")
with rsrc.as_file(data_file_path.joinpath("question_five_data.json")) as p:
    with p.open() as stream:
        data = json.load(stream)


# Data
demands_and_costs = pd.read_csv(
    data_file_path.joinpath("question_five_data_part_1.csv"),
    index_col=0)
distances = pd.read_csv(
    data_file_path.joinpath("question_five_data_part_2.csv"),
    index_col=0)

# Model
model = gp.Model("facility_location")


# Decisions

# Do I open a facility or not?
facility_open = model.addVars(
    range(len(data["Abbreviations"])),
    vtype=GRB.BINARY
)

# How much product do I ship from a facility?
product_shipped_from_to = model.addVars(
    range(len(data["Abbreviations"])),
    range(len(data["Abbreviations"])),
    vtype=GRB.CONTINUOUS
)


# Objective
# Minimize overall costs
# model.setObjective(
#     gp.quicksum(demands_and_costs[s])
# )

# Constraints

# Solve
model.optimize()

# Show results
# print(f"Objective value: {model.objVal}")
