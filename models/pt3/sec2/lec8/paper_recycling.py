from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt3.sec2.lec8").joinpath("question_two_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
num_paper_types = data["NumPapers"]
paper_types = data["Papers"]
old_pulp_qualities = data["OldPulpQualities"]
new_pulp_min_qualities = data["NewPulpMinimums"]
new_pulp_max_qualities = data["NewPulpMaximums"]
incoming_paper_tons = data["PaperReceived"]
recycled_paper_sale_price_per_ton = data["SellPrice"]

# Model
model = gp.Model("paper_recycling")

# Decisions
# How much pulp of each type to use to make recycled product
# of the various types?
pulp_to_product = model.addVars(
    num_paper_types,
    num_paper_types,
    vtype=GRB.CONTINUOUS
)
product_produced = model.addVars(
    num_paper_types,
    vtype=GRB.CONTINUOUS
)

# Objective
# Maximize sales of the produced recyclable paper products
model.setObjective(
    product_produced.prod(recycled_paper_sale_price_per_ton),
    sense=GRB.MAXIMIZE
)

# Constraints
# Use all incoming recycled paper
use_all_incoming_paper = model.addConstrs(
    sum(pulp_to_product[p, q] for q in range(num_paper_types)) == incoming_paper_tons[p]
    for p in range(num_paper_types)
)

# Minimum/maximum quality thresholds met
model.addConstrs(
    sum(old_pulp_qualities[p] * pulp_to_product[p, q] for p in range(num_paper_types))
    >=
    new_pulp_min_qualities[q] * product_produced[q]
    for q in range(num_paper_types)
)

model.addConstrs(
    sum(old_pulp_qualities[p] * pulp_to_product[p, q] for p in range(num_paper_types))
    <=
    new_pulp_max_qualities[q] * product_produced[q]
    for q in range(num_paper_types)
)

# Link product produced to pulp used to make the paper
model.addConstrs(
    product_produced[q] == sum(pulp_to_product[p, q] for p in range(num_paper_types))
    for q in range(num_paper_types)
)

# Solve
model.optimize()

# Show results
for j, q in enumerate(paper_types):
    for i, p in enumerate(paper_types):
        print(f"Use {pulp_to_product[i, j]} to contribute to making of {paper_types[j]}")
    print(f"Total {paper_types[j]} made: {product_produced[j]}")
print(f"Objective value: {model.objVal}")
