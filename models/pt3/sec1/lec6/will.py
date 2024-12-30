from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec1.lec6").joinpath("question_two_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
items = data["Items"]
item_values = [i["Value"] for i in items]
number_of_heirs = data["Heirs"]
ideal_split = data["Ideal"]
art_items = [i for i in range(len(items)) if items[i]["Art"] == 1]

# Model
model = gp.Model("will")

# Decisions
heir_item = model.addVars(
    number_of_heirs,
    range(len(items)),
    name="heir_item",
    vtype=GRB.BINARY)
heir_value = model.addVars(
    range(number_of_heirs),
    vtype=GRB.CONTINUOUS
)

# Objective
# Minimize the sum of each heir item set's stddev from ideal
model.setObjective(
    sum((ideal_split - heir_value[h]) ** 2 for h in range(number_of_heirs)),
    sense=GRB.MINIMIZE
)


# Constraints

# Every item is given to one person
every_item_to_an_heir = model.addConstrs(
    (sum(heir_item[h, i] for h in range(number_of_heirs)) == 1)
    for i in range(len(items))
)
# Tie the sum value of the items given to each heir
value_sum = model.addConstrs(
    (heir_value[h] == sum(item_values[i] * heir_item[h, i] for i in range(len(items))))
    for h in range(number_of_heirs)
)

# All of the music and art items must be given to different people
music_art_distribution = model.addConstrs(
    (sum(heir_item[h, i] for i in art_items) == 1)
    for h in range(number_of_heirs)
)

# Solve
model.optimize()

# Show results

for h in range(number_of_heirs):
    for i in range(len(items)):
        print(f"Heir {h} received item {items[i]["Name"]}: {heir_item[h, i].X}")
    print(f"Heir {h} value received: {heir_value[h].X}")
print(f"Objective value: {model.objVal}")
