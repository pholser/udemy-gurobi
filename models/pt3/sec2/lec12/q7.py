from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_seven_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
"""
{
	"high_areas": ["B", "D", "F", "Outside"],

	"extras": {
		"B": 15,
		"D": 10,
		"F": 90,
		"Outside": 25
	},

	"low_areas": ["A", "C", "E"],

	"needs": {
		"A": 20,
		"C": 80,
		"E": 40
	},

	"costs": [ [500,400,1000], [1000,600,500],
		[1600,1200,700], [2000,2200,2000] ]
}

"""
costs = data["costs"]
high_areas = data["high_areas"]
high_extras = data["extras"]
low_areas = data["low_areas"]
low_needs = data["needs"]

# Model
model = gp.Model("dirt")

# Decisions
# How much 
flow = model.addVars(high_areas, low_areas)

# Objective
# Minimize costs
model.setObjective(
    sum(costs[high_areas.index(h)][low_areas.index(j)] * flow[h, j]
        for h in high_areas
        for j in low_areas),
    sense=GRB.MINIMIZE
)

# Constraints
# Flow in == flow out at areas
high_balance = model.addConstrs(
    (high_extras[h] == flow.sum(h, "*")
    for h in high_areas)
)

low_balance = model.addConstrs(
    (low_needs[j] == flow.sum("*", j)
    for j in low_areas)
)

# Solve
model.optimize()

# Results
for h in high_areas:
    for j in low_areas:
        if flow[h, j].X > 0:
            print(f"Send {flow[h, j].X} from {h} to {j}")
print(f"Total cost: {model.objVal}")
