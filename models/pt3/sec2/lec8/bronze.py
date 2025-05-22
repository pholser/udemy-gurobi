from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt3.sec2.lec8").joinpath("question_three_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data

# Model
model = gp.Model("bronze")

# Decisions

# Objective

# Constraints

# Solve
model.optimize()

# Show results
# for j, q in enumerate(paper_types):
#     for i, p in enumerate(paper_types):
#         print(f"Use {pulp_to_product[i, j]} to contribute to making of {paper_types[j]}")
#     print(f"Total {paper_types[j]} made: {product_produced[j]}")
# print(f"Objective value: {model.objVal}")
