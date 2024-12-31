from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec1.lec6").joinpath("question_three_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
countries = data["Countries"]
country_index = {c: i for i, c in enumerate(countries)}
adjacencies = [(country_index[a[0]], country_index[a[1]]) for a in data["Adjacencies"]]
colors = list(range(len(countries)))

# Model
model = gp.Model("map_colors")

# Decisions
# Color each country
country_gets_color = model.addVars(
    range(len(countries)),
    colors,
    vtype=GRB.BINARY    
)
color_used = model.addVars(colors, vtype=GRB.BINARY)

# Objective
# Minimize the number of distinct colors used
model.setObjective(color_used.sum())

# Constraints
# Every country gets one color
every_country_colored = model.addConstrs(
    sum(country_gets_color[c, k] for k in colors) == 1
    for c in range(len(countries))
)

# Adjacent countries must not share a color
adjacent_countries_colored_differently = model.addConstrs(
    country_gets_color[c1, k] + country_gets_color[c2, k] <= 1
     for (c1, c2) in adjacencies
     for k in colors
)

# "color used" dictated by whether a country uses that color
model.addConstrs(
    country_gets_color[c, k] <= color_used[k]
     for c in range(len(countries))
     for k in colors
)

# Solve
model.optimize()

# Show results
for c in countries:
    for k in colors:
        if country_gets_color[c, k] > 0:
            print("Color country {c} with color {k}")
print(f"Objective value: {model.objVal}")
