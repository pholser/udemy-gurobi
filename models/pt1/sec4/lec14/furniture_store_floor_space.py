from gurobipy import GRB
from models import index_of
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt1.sec4.lec14").joinpath("question_three_data.json")
rsrc.as_file(data_file_path)
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)
C = data["categories"]
T = data["furniture_types"]

model = gp.Model("furniture_store_floor_space")

# Decisions
floor_space = model.addVars(len(T), lb=5, ub=100, name="floor_space")

# Objective
model.setObjective(
    gp.quicksum(
        T[t]["marginal_annual_profit_per_extra_percent_of_floor_space"] * floor_space[t]
        for t in range(len(T))
    ),
    sense=GRB.MAXIMIZE
)

# Constraints
total_floor_space = model.addConstr(floor_space.sum() == 100, name="total_floor_space")
bedroom_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Bedroom")] * floor_space[t]
        for t in range(len(T))
    ) >= 20),
    name="bedroom_floor_space"
)
living_room_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Living Room")] * floor_space[t]
        for t in range(len(T))
    ) >= 20),
    name="living_room_floor_space"
)
dining_room_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Dining Room")] * floor_space[t]
        for t in range(len(T))
    ) >= 15),
    name="dining_room_floor_space"
)
office_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Office")] * floor_space[t]
        for t in range(len(T))
    ) >= 10),
    name="office_floor_space"
)
beds_floor_space = model.addConstr(
    floor_space[index_of(T, lambda t: t["name"] == "Beds")] >= 10,
    name="beds_floor_space"
)
seating_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Seating")] * floor_space[t]
        for t in range(len(T))
    ) >= 50),
    name="seating_floor_space"
)
tables_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Tables")] * floor_space[t]
        for t in range(len(T))
    ) >= 10),
    name="tables_floor_space"
)
storage_work_floor_space = model.addConstr(
    (gp.quicksum(
        T[t]["categories"][C.index("Storage/Work")] * floor_space[t]
        for t in range(len(T))
    ) >= 5),
    name="storage_work_floor_space"
)
dining_room_tables_vs_dining_room_chairs_floor_space = model.addConstr(
    (floor_space[index_of(T, lambda t: t["name"] == "Dining Tables")]
     ==
     1.5 * floor_space[index_of(T, lambda t: t["name"] == "Chairs, dining room")]),
    name="dining_room_tables_vs_dining_room_chairs_floor_space"
)

model.optimize()

for t, furniture_type in enumerate(T):
    print(f"Allocate {floor_space[t].x} square feet to {furniture_type['name']}")
print(f"Expected profit: {model.objVal}")