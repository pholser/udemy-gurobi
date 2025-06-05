from models.data_manipulation.arrays import array_to_indices, dict_to_array
from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec2.lec12").joinpath("question_six_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
"""
{
	"players": ["A", "B", "C", "D", "E", "F"],

	"positions": ["Center", "Power Forward", "Small Forward", "Shooting Guard", "Point Guard", "Sixth Player"],

	"values": [ 
		[5,4,2,3,3,2], [8,6,4,2,2,4],
		[8,5,2,1,1,4], [4,4,5,8,7,4],
		[1,2,4,10,8,5], [1,1,2,3,6,2] ]
}

"""
players = data["players"]
positions = data["positions"]
player_values_for_position = data["values"]

# Model
model = gp.Model("basketball_team")

# Decisions
# How should I assign players to positions?
player_at_position = model.addVars(
    players,
    positions,
    vtype=GRB.BINARY
)

# Objective
# Maximize perceived value
model.setObjective(
    sum(player_values_for_position[players.index(p)][positions.index(q)]
        * player_at_position[p, q]
        for p in players
        for q in positions),
    sense=GRB.MAXIMIZE
)

# Constraints
one_position_per_player = model.addConstrs(
    (player_at_position.sum(p, "*") == 1
     for p in players)
)

one_player_per_position = model.addConstrs(
    (player_at_position.sum("*", q) == 1
     for q in positions)
)

# Solve
model.optimize()

# Results
for p in players:
    for q in positions:
        if player_at_position[p, q].X > 0.5:
            print(f"Player {p} at position {q}")
print(f"Value: {model.objVal}")
