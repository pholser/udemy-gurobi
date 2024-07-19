2a.
x = model.addVars(N, vtype=GRB.BINARY, name="x")

2b.
  x.prod(rental_cost)

2c.
  x.prod(capacity) >= 100000

2d.
  L_i <= capacity_i * x_i  forall i in N 

3a.
  x = model.addVars(100, vtype=GRB.BINARY, name="x")

3b.
  x.prod(expected_profit)

3c.
  f_i <= x_i  forall i in range(100)

4a.
  x = model.addVars(50, vtype=GBR.BINARY, name="x")

4b.
  k = model.addVars(50, 10, vtype=GRB.BINARY, name="k")

4c.
  x_i == sum[j in 1..10] { k_ij }, for all players i

4d.
  sum[i in players, j in years] { value_ij * k_ij }

4e.
  m_i <= M * x_i  for all players i

5a.
  x = model.addVars(16, vtype=GRB.BINARY, name="x")

5b.
  sum[i in projects] { cost_i * x_i } <= B

5c.
  s_i <= 24 * x_i   forall i in projects

