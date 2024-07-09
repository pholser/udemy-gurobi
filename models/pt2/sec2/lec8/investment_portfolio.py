from gurobipy import GRB
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt2.sec2.lec8").joinpath("question_two_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

stocks = data["stocks"]
expected_returns = [s["expected_return"] for s in stocks]
covariance = data["covariance"]
budget = data["available_portfolio_budget"]
risk_tolerance = data["risk_tolerance"]
minimum_expected_return = data["minimum_expected_return"]

model = gp.Model("investment_portfolio")

# Decision: how much to invest in each stock
amt_invested = model.addVars(len(stocks), name="stock_investment")

# Objective: maximize expected return on investment
# model.setObjective(amt_invested.prod(expected_returns), sense=GRB.MAXIMIZE)

# Objective: minimize risk
model.setObjective(
    gp.quicksum(
        gp.quicksum(
            covariance[i][j] * amt_invested[i] * amt_invested[j]
            for j in range(len(stocks))
        )
        for i in range(len(stocks))),
    sense=GRB.MINIMIZE)

# Constraint: cannot invest more than available budget
budget_constraint = model.addConstr(
    amt_invested.sum() <= budget,
    name="budget_constraint"
)

# Constraint: keep risk below tolerance
# risk_constraint = model.addConstr(
#     gp.quicksum(
#         gp.quicksum(
#             covariance[i][j] * amt_invested[i] * amt_invested[j]
#             for j in range(len(stocks))
#         )
#         for i in range(len(stocks)))
#     <=
#     risk_tolerance,
#     name="risk_constraint"
# )

# Constraint: Ensure a minimum expected return
min_return_constraint = model.addConstr(
    amt_invested.prod(expected_returns) >= minimum_expected_return,
    name="min_return_constraint"
)

# Solve
model.optimize()

# Output
for i in range(len(stocks)):
    print(f"Invest ${amt_invested[i].x} in {stocks[i]['name']}")
# print(f"Expected return: {model.objVal}")
print(f"Risk: {model.objVal}")
print(f"Min return: {min_return_constraint.pi}")
