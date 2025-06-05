import gurobipy as gp
from gurobipy import GRB

import json

# Choose the correct data file and comment out the other
#with open("question_five_data-time.json", "r") as f:
with open("question_five_data-distance.json", "r") as f:
    data = json.load(f)

Nodes = data["Nodes"]
Arcs = [tuple(k) for k in data["Arcs"]]
Costs = data["Costs"]
Capacities = data["Capacities"] 
Start = data["Start"]
End = data["End"]
Highways = data["Highways"]

NumNodes = len(Nodes)
NumArcs = len(Arcs)


m = gp.Model("parks")


# Variables: Flow on each arc
x = m.addVars(Arcs, ub=Capacities, vtype=GRB.CONTINUOUS, name="x")


# Objective: Minimize cost
m.setObjective(sum(Costs[Arcs.index((i,j))] * x[(i,j)] for i in Nodes for j in Nodes if (i,j) in Arcs), GRB.MINIMIZE)


# Constraints: Flow in = flow out at every node
m.addConstrs((i == Start) + sum(x[(j,i)] for j in Nodes if (j,i) in Arcs) == (i == End) + sum(x[(i,j)] for j in Nodes if (i,j) in Arcs) for i in Nodes)


m.optimize()

print("***************** Solution *****************")
print(f"Total: {round(m.ObjVal, 2)}")
for (i,j) in Arcs:
    if x[(i,j)].X > 0:
        print(f"Drive from {i} to {j} on {Highways[Arcs.index((i,j))]}")
