from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_four_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
"""
{
	"plants": ["Saskatoon", "Portage la Prairie", "Medicine Hat"],

	"production": [9, 6, 6],

	"stores": ["Moose Jaw", "Winnipeg", "Great Falls", "Bismarck", "Prince Albert", "Storage"],

	"demand": [2, 4, 8, 4, 1, 2],

	"costs": [ 
		[5750,7500,7625,7750,5500,1000],
		[6750,5250,9750,6875,7750,800],
		[6250,8125,6500,8250,7000,1300] ]
}
"""
costs = data["costs"]
plants = data["plants"]
plant_production = data["production"]
stores = data["stores"]
store_demand = data["demand"]

# Model
model = gp.Model("refrigerators")

# Decisions
# How many refrigerators do I send from plant to store?
flow = model.addVars(
    plants,
    stores,
    vtype=GRB.INTEGER
)

# Objective
# Minimize costs
model.setObjective(
    sum(costs[plants.index(p)][stores.index(s)] * flow[p, s]
        for p in plants
        for s in stores),
    sense=GRB.MINIMIZE
)

# Constraints
# Flow in == flow out at plants
plant_balance = model.addConstrs(
    (plant_production[plants.index(p)] == flow.sum(p, "*")
    for p in plants)
)

# Flow in == flow out at stores
store_balance = model.addConstrs(
    (store_demand[stores.index(s)] == flow.sum("*", s)
    for s in stores)
)

# Solve
model.optimize()

# Results
for p in plants:
    for s in stores:
        if flow[p, s].X > 0.5:
            print(f"Send {flow[p, s]} from {p} to {s}")
print(f"Total cost: {model.objVal}")
