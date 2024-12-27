from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json



data_file_path = rsrc.files("models.pt3.sec1.lec6").joinpath("question_one_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

projects = data["Projects"]
project_index = {p: i for i, p in enumerate(projects)}
council = data["Council"]
suggested_projects = [
    array_to_indices(ps, project_index)
    for ps in dict_to_array(data["Suggested"], council)
]
costs = dict_to_array(data["Costs"], projects)
surplus = data["Surplus"]
beneficiaries = dict_to_array(data["Beneficiaries"], projects)

model = gp.Model("city_projects")

project_chosen = model.addVars(range(len(projects)),
    name="project_chosen",
    vtype=GRB.BINARY)

model.setObjective(
    gp.quicksum(beneficiaries[p] * project_chosen[p] for p in range(len(projects))),
    GRB.MAXIMIZE)

budget = model.addConstr(
    gp.quicksum(costs[p] * project_chosen[p] for p in project_chosen) <= surplus
)

all_council_respected = model.addConstrs(
    (gp.quicksum(project_chosen[s] for s in suggestions) >= 1
     for suggestions in suggested_projects)
)

# Solve
model.optimize()

for p in range(len(projects)):
    print(f"{projects[p]}: {project_chosen[p].X}, {beneficiaries[p]}, {costs[p]}")
print(f"Total beneficiaries: {model.objVal}")
