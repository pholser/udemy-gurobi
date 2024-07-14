import gurobipy as gp
from gurobipy import GRB
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt2.sec3.lec10").joinpath("print-shop.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

# Data
H = data["available_hours"]
M = data["machines"]
J = data["jobs"]

model = gp.Model("print-shop")

# Decision: on what machine should each job run
job_on_machine = model.addVars(
    range(len(J)),
    range(len(M)),
    vtype=GRB.BINARY,
    name="job_on_machine"
)

# Objective: minimize ink cost
# model.setObjective(
#     gp.quicksum(
#         J[j]["ink_costs"][m] * job_on_machine[j, m]
#         for j in range(len(J))
#         for m in range(len(M))
#     ),
#     sense=GRB.MINIMIZE
# )

# Objective: maximize number of completed jobs
model.setObjective(
    gp.quicksum(
        job_on_machine[j, m]
        for j in range(len(J))
        for m in range(len(M))
    ),
    sense=GRB.MAXIMIZE
)

# Constraint: each job can be run on at most one machine
one_machine_constraints = model.addConstrs(
    (gp.quicksum(job_on_machine[j, m] for m in range(len(M))) <= 1 for j in range(len(J))),
    name="one_machine_constraints"
)

# Constraint: machine hours
machine_hours_constraints = model.addConstrs(
    (
        gp.quicksum(
            J[j]["machine_times_in_hours"][m] * job_on_machine[j, m]
            for j in range(len(J)))
        <= H for m in range(len(M))
    ),
    name="machine_hours_constraints"
)

# Solve
model.optimize()

print(job_on_machine)
# Output
for j in range(len(J)):
    for m in range(len(M)):
        if job_on_machine[j, m].X > 0.5:
            print(f"Job {j} runs on machine {m}")
# print(f"Total ink cost: {model.objVal}")
print(f"Total jobs completed: {model.objVal}")
