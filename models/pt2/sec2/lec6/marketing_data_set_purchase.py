from gurobipy import GRB
from models import index_of
import gurobipy as gp
import importlib.resources as rsrc
import json

data_file_path = rsrc.files("models.pt2.sec2.lec6").joinpath("question_two_data.json")
with rsrc.as_file(data_file_path) as p:
    with p.open() as stream:
        data = json.load(stream)

D = data["Data sets"]
C = data["Costs"]
G = data["Groups"]
K = data["Categories"]
M = data["Minimums"]
N = data["NumToBuy"]

model = gp.Model("marketing_data_set_purchase")

# decision: which data sets to purchase
purchase_data_set = model.addVars(D, vtype=GRB.BINARY, name="data_sets_to_purchase")

# objective: minimize cost of data sets purchased
model.setObjective(purchase_data_set.prod(C), sense=GRB.MINIMIZE)

# Helper var: number of data sets of each category purchased
data_sets_purchased_in_category = model.addVars(len(K), vtype=GRB.INTEGER)
model.addConstrs(
    (data_sets_purchased_in_category[k]
     ==
     gp.quicksum(purchase_data_set[d] * G[d][k] for d in range(D))
     for k in range(len(K))),
    name="constrained_data_sets_purchased_in_category"
)

# constraint: must purchase at least minimum number of data sets in each category
min_data_sets_per_category = model.addConstrs(
    (data_sets_purchased_in_category[k] >= M[k] for k in range(len(K))),
    name="min_data_sets_per_category"
)

# constraint: purchase exactly a certain number of data sets
model.addConstr(purchase_data_set.sum() == N, name="exactly_fixed_number_of_purchases")

model.optimize()

# output
for i in range(D):
    if purchase_data_set[i].x > 0.5:
        print(f"Purchase data set {i + 1}")
print(f"Expected cost: {model.objVal}")
