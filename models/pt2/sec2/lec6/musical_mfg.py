from gurobipy import GRB
from models import index_of
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt2.sec2.lec6").joinpath("question_one_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

M = data["Machines"]
I = data["Instruments"]
P = data["Processing Times"]
S = data["Max Sales"]
T = data["Available Times"]
R = data["Profits"]

model = gp.Model("musical_mfg")

# Decision: how many of each instrument to make in the available time
instruments_to_make = model.addVars(I, vtype=GRB.INTEGER, name="instruments_to_make")

# Objective: maximize expected profit on instruments made and sold
model.setObjective(instruments_to_make.prod(R), sense=GRB.MAXIMIZE)

# Cannot make more instruments than can be sold in available time
max_instruments_to_make = model.addConstrs(
    (instruments_to_make[i] <= S[i] for i in I),
    name="max_instruments_to_sell"
)

# Cannot make more instruments than can be tested in available time
max_instruments_to_make = model.addConstr(
    instruments_to_make.sum() == 150,
    name="max_instruments_to_make"
)

# Cannot spend more time on machine-making instruments than allowed
max_machine_time_spent = model.addConstrs(
    (gp.quicksum(P[i][j] * instruments_to_make[j] for j in I) <= T[i] for i in M),
    name="max_machine_time_spent"
)

# Solve
model.optimize()

# Output
for i in range(len(I)):
    print(f"Make {instruments_to_make[I[i]]} {I[i]}")
    print(f"Expected profit: {model.objVal}")
