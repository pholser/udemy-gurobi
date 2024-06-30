from gurobipy import GRB
from models import index_of
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt1.sec4.lec14").joinpath("question_four_b_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)
M = data["materials"]
C = data["companies"]

model = gp.Model("recycling")

# Decisions
# how many bundles of material to sell to large recyclers
bundles = model.addVars(len(C), lb=100, name="bundles")
# how much unbundled material to sell to small recyclers
unbundled_material = model.addVars(len(M), name="unbundled_material")

# Objective
# maximize revenue from selling bundles and unbundled material
model.setObjective(
    gp.quicksum(C[c]["bundle_purchase_price"] * bundles[c] for c in range(len(C)))
    +
    gp.quicksum(M[m]["price_per_pound"] * unbundled_material[m] for m in range(len(M))),
    sense=GRB.MAXIMIZE
)

# Constraints
# Sell all the recyclables collected
model.addConstrs(
    (
        gp.quicksum(C[c]["pounds_of_material_per_bundle"][m] * bundles[c] for c in range(len(C)))
        + unbundled_material[m]
        ==
        M[m]["volume_collected_in_pounds"]
        for m in range(len(M))
    ),
    name="sell_all_recyclables"
)

model.optimize()

# Output
print(f"Maximum revenue: ${model.objVal:.2f}")
print("Number of bundles to sell to each company:")
for c in range(len(C)):
    print(f"Company {c + 1}: {bundles[c].x:.2f}")
print("Amount of unbundled material to sell to small recyclers:")
for m in range(len(M)):
    print(f"{M[m]['name']}: {unbundled_material[m].x:.2f}")
