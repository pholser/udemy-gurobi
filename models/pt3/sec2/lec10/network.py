from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec10").joinpath("question_five_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
nodes = data["Nodes"]
demands = data["Demands"]
supplies = data["Supplies"]
arcs = [tuple(a) for a in data["Arcs"]]
costs = data["Costs"]
capacities = data["Capacities"]

# Model
model = gp.Model("network")

# Decisions
# How much stuff do I send on each arc?
flow = model.addVars(
    arcs,
    lb=0.0,
    ub=capacities
)

# Objective
# Minimize arc costs
model.setObjective(
    sum(costs[arcs.index((i, j))] * flow[(i, j)]
        for (i, j) in arcs),
    GRB.MINIMIZE
)

# Constraints
# Respect arc capacities; specified as upper bounds on variables

# Balance constraints: flow in == flow out at each node
balance = model.addConstrs(
    sum(flow[(i, k)] for i in nodes if (i, k) in arcs)
        + supplies[nodes.index(k)]
    ==
    sum(flow[(k, j)] for j in nodes if (k, j) in arcs)
        + demands[nodes.index(k)]
    for k in nodes
)

# Solve
model.optimize()

# Results
for a in arcs:
    print(f"Flow on arc {a}: {flow[a]}")
print(f"Objective value: {model.objVal}")
