from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json


data_file_path = rsrc.path("models.pt1.sec4.lec14", "question_one_data.json")

with data_file_path as p:
    with p.open() as stream:
        data = json.load(stream)

B = data["B"]
N = data["N"]
P = data["profits"]
L = data["L"]
R = data["R"]
Mmax = data["M"]
Mmin = data["m"]
cities = data["cities"]

m = gp.Model("investment")
x = m.addVars(N, lb=Mmin, ub=Mmax, name="x")
m.addConstr(gp.quicksum(x[j] for j in range(N)) <= B, name="budget")
m.setObjective(gp.quicksum(P[j] * x[j] for j in range(N)), GRB.MAXIMIZE)
m.addConstrs(
  (gp.quicksum(x[j] for j in R[r]) <= L[r] for r in range(len(R))),
  name="region"
)

m.optimize()

for j, city in enumerate(cities):
    print(f"Invest {x[j].x} in city {city}")
print(f"Expected profit: {m.objVal}")
