import gurobipy as gp
from gurobipy import GRB

import json

with open("question_one_data.json", "r") as f:
    data = json.load(f)

NumSurveys = data["NumSurveys"]
Surveys = data["Surveys"]
NumCustomers = data["NumCustomers"]
Customers = data["Customers"]
Costs = data["Costs"]
Ages = data["Ages"]
Maximums = data["Maximums"]
Needed = data["Needed"]
MinAge = data["MinAge"]
MaxAge = data["MaxAge"]


m = gp.Model("survey")


# Variables: Number of people of each survey type used for each customer's survey
x = m.addVars(NumSurveys, NumCustomers, vtype=GRB.CONTINUOUS, name="x")


# Objective: Minimize cost
m.setObjective(sum(Costs[i]*x[i,j] for i in range(NumSurveys) for j in range(NumCustomers)))


# Constraints: Can't use more than maximum that can be surveyed
m.addConstrs(sum(x[i,j] for j in range(NumCustomers)) <= Maximums[i] for i in range(NumSurveys))

# Constraints: Must survey at least the required number of people for each customer
m.addConstrs(sum(x[i,j] for i in range(NumSurveys)) >= Needed[j] for j in range(NumCustomers))

# Constraints: Average age for each customer must be between min and max
m.addConstrs(sum(Ages[i]*x[i,j] for i in range(NumSurveys)) >= MinAge[j]*sum(x[i,j] for i in range(NumSurveys)) for j in range(NumCustomers))
m.addConstrs(sum(Ages[i]*x[i,j] for i in range(NumSurveys)) <= MaxAge[j]*sum(x[i,j] for i in range(NumSurveys)) for j in range(NumCustomers))


m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
for j in range(NumCustomers):
    for i in range(NumSurveys):
        if x[i,j].X > 0:
            print(f"Survey {round(x[i,j].X,0)} people by {Surveys[i]} for {Customers[j]}")

