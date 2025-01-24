from models.data_manipulation.arrays import array_to_indices, dict_to_array
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt3.sec2.lec8").joinpath("question_one_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
num_survey_types = data["NumSurveys"]
survey_types = data["Surveys"]
cost_per_person_by_survey_type = data["Costs"]
average_age_by_survey_type = data["Ages"]
max_people_surveyed_by_survey_type = data["Maximums"]

num_customers = data["NumCustomers"]
customers = data["Customers"]
min_people_surveyed_needed_by_customer = data["Needed"]
min_age_surveyed_needed_by_customer = data["MinAge"]
max_age_surveyed_needed_by_customer = data["MaxAge"]


# Model
model = gp.Model("polling")

# Decisions
# Number of people of each survey type to use for each customer
surveyed = model.addVars(
    num_survey_types,
    num_customers,
    vtype=gp.GRB.CONTINUOUS
)

# Objective
# Minimize cost of compiling survey data
model.setObjective(
    gp.quicksum(
        cost_per_person_by_survey_type[s] * surveyed[s, c]
        for s in range(num_survey_types)
        for c in range(num_customers)
    )
)

# Constraints
# Each customer needs a certain minimum number of people surveyed
min_surveyed_per_customer = model.addConstrs(
    surveyed.sum("*", c) >= min_people_surveyed_needed_by_customer[c]
    for c in range(num_customers)
)

# Ages of those surveyed must respect age ranges for each customer
age_range_min = model.addConstrs(
   (gp.quicksum(average_age_by_survey_type[s] * surveyed[s, c]
                for s in range(num_survey_types))
    >=
    min_age_surveyed_needed_by_customer[c] * surveyed.sum("*", c)
   )
   for c in range(num_customers)
)
age_range_max = model.addConstrs(
   (gp.quicksum(average_age_by_survey_type[s] * surveyed[s, c]
                for s in range(num_survey_types))
    <=
    max_age_surveyed_needed_by_customer[c] * surveyed.sum("*", c)
   )
   for c in range(num_customers)
)

# Solve
model.optimize()

# Show results
for si, s in enumerate(survey_types):
    for ci, c in enumerate(customers):
        print(f"Survey {surveyed[si, ci]} people in manner {s} for customer {c}")
print(f"Objective value: {model.objVal}")
