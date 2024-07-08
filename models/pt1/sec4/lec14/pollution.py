from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt1.sec4.lec14").joinpath("question_five_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)
C = data["companies"]
T = data["T"]

model = gp.Model("pollution")

# Decisions
# how much pollution to allow each company to emit
allowed_emitted_pollution = model.addVars(len(C), name="allowed_emitted_pollution")

# Objective
# minimize total operating expenses of companies
# that is: current operating expenses + cost of decreasing emissions per ton of pollution
model.setObjective(
    gp.quicksum(
        C[c]["c"] + (C[c]["d"] * (C[c]["p"] - allowed_emitted_pollution[c]))
        for c in range(len(C))
    ),
    sense=GRB.MINIMIZE
)

# Constraints
# Expenses no greater than specified ceiling
expenses_curbed = model.addConstrs(
    (C[c]["c"]
     + (C[c]["d"] * (C[c]["p"] - allowed_emitted_pollution[c]))
     <=
     C[c]["m"]
     for c in range(len(C))),
    name="expenses_curbed"
)

# Total pollution emitted by all companies no greater than specified ceiling
total_pollution_curbed = model.addConstr(
    gp.quicksum(allowed_emitted_pollution[c] for c in range(len(C))) <= T,
    name="total_pollution_curbed"
)

# Disallow greater pollution than companies are currently emitting
no_increase_in_pollution = model.addConstrs(
    (allowed_emitted_pollution[c] <= C[c]["p"] for c in range(len(C))),
    name="no_increase_in_pollution"
)
model.optimize()

# Output
