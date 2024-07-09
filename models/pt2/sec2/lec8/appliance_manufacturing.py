from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.files("models.pt2.sec2.lec8").joinpath("question_four_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

M = data["M"]
cost = data["cost"]
alpha = data["alpha"]

model = gp.Model("appliance_manufacturing")

# Decision: how many units of each appliance to manufacture
units = model.addVars(range(1, M + 1), vtype=GRB.INTEGER, name="units")

# Decision: prices at which to sell each appliance
prices = model.addVars(range(1, M + 1), vtype=GRB.CONTINUOUS, name="prices")

# Objective: maximize profit (selling price - manufacturing cost)
model.setObjective(
    gp.quicksum(
        (prices[i] - cost[i]) * units[i]
        for i in range(1, M + 1)
    ),
    sense=GRB.MAXIMIZE
)

# Constraint: number of units sold depends on prices of all models
units_sold_constraint = model.addConstrs(
    (units[i]
     ==
     alpha[i][0] + sum(alpha[i][j] * prices[j] for j in range(1, M + 1)))
    for i in range(1, M + 1)
)

# Solve
model.optimize()

# Output
for i in range(1, M + 1):
    print(f"Model {i}:")
    print(f"  Units: {units[i].x}")
    print(f"  Price: {prices[i].x}")
    print(f"  Revenue: {prices[i].x * units[i].x}")
    print(f"  Cost: {cost[i] * units[i].x}")
    print(f"  Profit: {(prices[i].x - cost[i]) * units[i].x}")
