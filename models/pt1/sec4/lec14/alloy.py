from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt1.sec4.lec14").joinpath("question_two_data.json")
rsrc.as_file(data_file_path)
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

P = data["P"]
process_1_index = next((i for i, item in enumerate(P) if item["name"] == "Process 1"), None)

m = gp.Model("alloy")
x = m.addVars(len(P), name="x")
production_quota = m.addConstr(
    (
        gp.quicksum(x[p] for p in range(len(P)))
        >=
        data["production_quota_in_tons"]
    ),
    name="production quota"
)
process_1_pollution_limit = m.addConstr(
    (
        x[process_1_index]
        <=
        (2 * gp.quicksum(
                 P[p]["pollution_per_ton_of_alloy_created_in_pounds"] * x[p]
                 for p in range(len(P)))
            / 3)
    ),
    name="process 1 pollution limit"
)
pollution_ceiling = m.addConstr(
    (
        gp.quicksum(P[p]["pollution_per_ton_of_alloy_created_in_pounds"] * x[p] for p in range(len(P)))
        <=
        data["pollution_ceiling_in_pounds"]
    ),
    name="pollution ceiling"
)

m.setObjective(
    gp.quicksum(P[p]["cost_per_ton_of_alloy_created"] * x[p] for p in range(len(P))),
    sense=GRB.MINIMIZE
)

m.optimize()

for p, process in enumerate(P):
    print(f"Produce {x[p].x} tons using {process['name']}")
print(f"Production cost: {m.objVal}")
