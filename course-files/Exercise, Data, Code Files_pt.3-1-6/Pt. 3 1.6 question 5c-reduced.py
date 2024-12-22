import gurobipy as gp
from gurobipy import GRB

import json
import numpy as np
import pandas

cost_demand_data = pandas.read_csv('question_five_data_part_1.csv',sep=',',header=0,index_col=0).to_dict() 
distance_data = pandas.read_csv('question_five_data_part_2.csv',sep=',',header=0,index_col=0).to_dict()

States = distance_data.keys() 
FacilityCost = cost_demand_data['Facility cost'] 
Demand = cost_demand_data['Demand'] 
Distance = {k.strip():{k2.strip(): int(v2) for k2,v2 in v.items()} for k,v in distance_data.items()}  

# Determine total demand
TotalDemand = sum(Demand.values()) 


with open("question_five_data.json", "r") as f:
    data = json.load(f)

ShipPerMile = data["Shipping Cost"]
AssemblyLimit = data["Facility Assembly Limit"]
Abbreviations = data["Abbreviations"]


m = gp.Model("facility")


# Variables: which states will have facilities? (1=yes, 0=no)
x = m.addVars(States, vtype=gp.GRB.BINARY,name="x")

# Variables: amount shipped from each facility to each state
y = m.addVars([(s,t) for s in States for t in States if Distance[s][t] <= 1600], vtype=gp.GRB.CONTINUOUS,name="y")


# Objective: minimize the cost of the facilities plus the shipping
m.setObjective(sum(FacilityCost[s]*x[s] for s in States) + sum(ShipPerMile*Distance[s][t]*y[s,t] for s in States for t in States if Distance[s][t] <= 1600))


# Constraints: Meet demand in each state by shipping from facilities
m.addConstrs(sum(y[t,s] for t in States if Distance[t][s] <= 1600) == Demand[s] for s in States)
               
# Constraints: No products can be shipped from a facility unless the facility is open
m.addConstrs(sum(y[s,t] for t in States if Distance[s][t] <= 1600) <= TotalDemand*x[s] for s in States)
              
# Constraints: No facility can assemble more than 250,000 units of product
m.addConstrs(sum(y[s,t] for t in States if Distance[s][t] <= 1600) <= AssemblyLimit for s in States)


m.optimize()

print("***************** Solution *****************")
print(f"Total Cost: {round(m.ObjVal, 2)}")
print(f"Open {sum(x[s].X for s in States)} facilities:")
for s in States:
    if x[s].X > 0.9999:
        print(f"Open a facility in {s}")
        for t in States:
            if Distance[s][t] <= 1600:
                if y[s,t].X > 0.0001:
                   print(f"......Ship {y[s,t].X} units of product to {t}")
               
        
