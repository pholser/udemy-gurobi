from gurobipy import GRB
from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt3.sec1.lec6").joinpath("question_four_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
experts = data["Experts"]
expert_costs = [e["Cost"] for e in experts]
familiarities = data["Familiarities"]
experience_categories = data["Experience Categories"]
levels = data["Levels"]
countries = data["Countries"]

# Model
model = gp.Model("focus_group")

# Decisions
expert_in_focus_group = model.addVars(
    range(len(experts)),
    vtype=GRB.BINARY    
)

# Objective
# Minimize the cost of hiring experts for the focus group
model.setObjective(
    gp.quicksum(
        expert_costs[e] * expert_in_focus_group[e]
        for e in range(len(experts))
    )
)

# Constraints
# Needs spread of user familiarity in the group
familiarity_ranges_met_min = model.addConstrs(
    sum(expert_in_focus_group[e]
        for e in range(len(experts))
        if experts[e]["Familiarity"] == familiarities[f]["Description"]
    ) >= familiarities[f]["Minimum"]
    for f in range(len(familiarities))
)
familiarity_ranges_met_max = model.addConstrs(
    sum(expert_in_focus_group[e]
        for e in range(len(experts))
        if experts[e]["Familiarity"] == familiarities[f]["Description"]
    ) <= familiarities[f]["Maximum"]
    for f in range(len(familiarities))
)

# Needs spread of industry experience in the group
experience_ranges_met = model.addConstrs(
    sum(expert_in_focus_group[e]
        for e in range(len(experts))
        if experts[e]["Experience"] >= experience_categories[x]["Range"][0]
        and experts[e]["Experience"] <= experience_categories[x]["Range"][1]
    ) >= 1
    for x in range(len(experience_categories))
)

# Needs spread of organization level in the group
organization_level_met = model.addConstrs(
    sum(expert_in_focus_group[e]
        for e in range(len(experts))
        if experts[e]["Level"] >= levels[i]
        and experts[e]["Level"] <= levels[i]
    ) >= 1
    for i in range(len(levels))
)

# Needs spread of countries in the group
country_met = model.addConstrs(
    sum(expert_in_focus_group[e]
        for e in range(len(experts))
        if experts[e]["Country"] >= countries[c]
        and experts[e]["Country"] <= countries[c]
    ) >= 1
    for c in range(len(countries))
)

# Because experts 4 and 8 do not get along with expert 10, the firm can either
# choose expert 10 without 4 and 8; or one or both of experts 4 and 8
# without expert 10; or none of experts 4, 8, and 10.
if_4_or_8_then_not_10 = model.addConstr(
    expert_in_focus_group[3] + expert_in_focus_group[7]
    <=
    2 * (1 - expert_in_focus_group[9])
)

# Solve
model.optimize()

# Show results
for i, e in enumerate(experts):
    print(f"Expert {e} in focus group: {expert_in_focus_group[i]}")
print(f"Total cost: {model.objVal}")
