from gurobipy import GRB
import gurobipy as gp
import numpy as np
import pandas as pd


def generate_data(n_samples, n_features, noise=0.1, random_state=None):
    np.random.seed(random_state)

    # Generate random feature data
    X = np.random.rand(n_samples, n_features)

    # Generate random coefficients
    coefficients = np.random.rand(n_features)

    # Generate the response variable with some noise
    y = X.dot(coefficients) + noise * np.random.randn(n_samples)

    # Create a DataFrame for the features
    df = pd.DataFrame(X)

    # Add the response variable to the DataFrame
    df["response"] = y

    return df


# Parameters
number_of_samples = 300
number_of_features = 5
data = generate_data(
    n_samples=number_of_samples,
    n_features=number_of_features,
    random_state=19387410
)
y = data["response"]
X = data.drop(columns=["response"])

model = gp.Model("constrained_regression")

# Decisions: coefficients for the regression model
regression_coefficients = model.addVars(
    range(number_of_features + 1),
    lb=-1,
    ub=1,
    name="regression_coefficients")

# Constraint: fix regression constant at 0
fix_regression_constant_constraint = model.addConstr(
    regression_coefficients[0] == 0,
    name="fix_regression_constant_constraint"
)

# Constraint: sum of regression coefficients must be zero
sum_of_regression_coefficients_constraint = model.addConstr(
    regression_coefficients.sum() == 0,
    name="sum_of_regression_coefficients_constraint"
)

# Objective: minimize sum of squared residuals
residuals = model.addVars(
    range(1, number_of_samples + 1),
    lb=-GRB.INFINITY,
    name="residuals"
)
residuals_definition_constraints = model.addConstrs(
    (residuals[i]
     ==
     y[i - 1] - sum(regression_coefficients[j] * X.iloc[i - 1, j - 1]
                    for j in range(1, number_of_features + 1)
                    )
     )
    for i in range(1, number_of_samples + 1)
)
model.setObjective(
    sum(residuals[i] ** 2 for i in range(1, number_of_samples + 1)),
    sense=GRB.MINIMIZE
)

# Solve
model.optimize()

# Output
print("Regression coefficients:")
for i in range(number_of_features):
    print(f"{regression_coefficients[i].varName}: {regression_coefficients[i].x}")
print(f"Sum of squared residuals: {model.objVal}")
