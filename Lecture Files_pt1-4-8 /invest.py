import gurobipy as gp
from gurobipy import GRB


# Data
cities = {"Atlanta", "Boston", "Charlotte", "Detroit"}
north = {"Boston", "Detroit"}
assert north.issubset(cities)
south = {"Atlanta", "Charlotte"}
assert south.issubset(cities)
 

model = gp.Model("invest")


# Variables: millions of dollars invested in each city
x = model.addVars(cities,lb=2,ub=8,name="x")


# Objective: maximize predicted increase
priceIncrease={"Atlanta":0.11,"Boston": 0.02,"Charlotte":0.04,"Detroit":0.03}
model.setObjective(x.prod(priceIncrease),GRB.MAXIMIZE)


# Constraint: Budget of $20 million
model.addConstr(x.sum()<=20,name="Budget")

# Constraints: Regional limits of $12 million
model.addConstr(gp.quicksum(x.select(north)) <= 12,name="NorthBudget")
model.addConstr(gp.quicksum(x.select(south)) <= 12,name="SouthBudget")

# Constraints: City min of $2 million and max of $8 million (for each city)
# No constraints needed because the lower 
# and upper bounds for these variables are
# defined in the variable definitions


# Optimize
model.optimize()

print(f"Predicted value increase = ${round(model.ObjVal,2)} million")
for city in cities:
    print(f"Invest ${round(x[city].X,1)} million in {city}")
    
