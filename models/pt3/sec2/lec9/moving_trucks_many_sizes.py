from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec9").joinpath("question_nine_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

"""
{
	"TruckSizes": [ 1, 0.75, 0.5 ],

	"LoadSizes": [ 1, 0.5, 0.25 ],

	"Demand": [ 1, 4, 10 ],

	"Patterns": [
		[ [1,0,0], [0,2,0], [0,1,2], [0,0,4], [0,1,1], [0,1,0], [0,0,3],
			[0,0,2], [0,0,1] ],
		[ [0,1,1], [0,0,3], [0,1,0], [0,0,2], [0,0,1] ],
		[ [0,1,0], [0,0,2], [0,0,1] ]
	],

	"TruckCosts": [ 1000, 800, 700 ]
}
"""

# Data
truck_sizes = data["TruckSizes"]
load_sizes = data["LoadSizes"]
demand = data["Demand"]
patterns_by_truck_size = data["Patterns"]
truck_costs = data["TruckCosts"]

# Model
model = gp.Model("float_glass_many_sizes")

# Decisions
# How many of each load pattern will I load into what size of truck?
patterns_loaded = model.addVars(
    [(t, p)
     for t in range(len(truck_sizes))
     for p in range(len(patterns_by_truck_size[t]))],
    lb=0,
    vtype=GRB.INTEGER
)

# Objective
# Minimize cost of trucks used
model.setObjective(
    sum(truck_costs[t] * patterns_loaded[t, p]
        for t in range(len(truck_sizes))
        for p in range(len(patterns_by_truck_size[t]))),
    sense=GRB.MINIMIZE
)

# Constraints
# Meet delivery demand
meet_demand = model.addConstrs(
    sum(patterns_by_truck_size[t][p][j] * patterns_loaded[t, p]
        for t in range(len(truck_sizes))
        for p in range(len(patterns_by_truck_size[t])))
    ==
    demand[j]
    for j in range(len(load_sizes))
)

# Solve
model.optimize()

# Results
print(f"Objective value: {model.objVal}")
