import gurobipy as gp
from gurobipy import GRB

import json

with open("question_three_data.json", "r") as f:
    data = json.load(f)

skills = data["skills"]
people = data["people"]
skills_people = data["skills_people"]


m = gp.Model("team")


# Variables: Which people are chosen?
x = m.addVars(people, vtype=GRB.BINARY, name="x")


# Objective: minimize the number of people chosen
m.setObjective(x.sum(),sense=GRB.MINIMIZE)


# Each skill must be covered
m.addConstrs(sum(x[p] for p in skills_people[s]) >= 1 for s in skills)


m.optimize()

print("***************** Solution *****************")
print(f"Total people selected: {round(m.ObjVal, 4)}")
for p in people:
    if x[p].X > 0.5:
        print(f"Person {p} selected.")


