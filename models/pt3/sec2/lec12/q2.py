from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_two_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
costs = data["numbers"]
ads = data["left_nodes"]
networks = data["right_nodes"]
ad_desired_runs = data["supplies"]
network_run_contract = data["demands"]

# Model
model = gp.Model("ads")

# Decisions
# How many times do I run each ad on each network?
ad_runs_on_network = model.addVars(
    ads,
    networks,
    vtype=GRB.INTEGER
)

# Objective
# Minimize costs
model.setObjective(
    sum(costs[ads.index(a)][networks.index(n)] * ad_runs_on_network[a, n]
        for a in ads
        for n in networks),
    sense=GRB.MINIMIZE
)

# Constraints
# Each ad run a certain number of times
ad_runs_met = model.addConstrs(
    (ad_runs_on_network.sum(a, "*") == ad_desired_runs[a]
     for a in ads)
)

# Network runs contracted number of ads
network_contract_met = model.addConstrs(
    (ad_runs_on_network.sum("*", n) == network_run_contract[n]
     for n in networks)
)

# Solve
model.optimize()

# Results
for a in ads:
    for n in networks:
        if ad_runs_on_network[a, n].X > 0.5:
            print(f"Run ad {a} {ad_runs_on_network[a, n]} times on network {n}")
print(f"Total cost: {model.objVal}")
