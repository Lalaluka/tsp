from gurobipy import *

# Implementation of the Miller-Tucker-Zemlin formulation for the TSP
def solve(nodes, verbose=True):
  model = Model("TSP")

  if not verbose:
    model.setParam('OutputFlag', 0)

  # Big M
  M = len(nodes)

  # Variables

  ## x_ij = 1 if the edge (i,j) is in the solution
  x = {}
  for i in nodes:
    for j in nodes:
      if i != j:
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x(%s,%s)"%(i,j))

  ## u_i = position of node i in the tour
  u = {}
  for i in nodes:
    u[i] = model.addVar(vtype=GRB.INTEGER, name="u(%s)"%(i))

  # Constraints
  # incoming edges = 1 for every node
  for i in nodes:
    model.addConstr(quicksum(x[j, i] for j in nodes if j != i) == 1)
  
  # outgoing edges = 1 for every node
  for i in nodes:
    model.addConstr(quicksum(x[i, j] for j in nodes if j != i) == 1)

  # Subtour elimination
  for i in nodes:
    for j in nodes:
      if i != j and i != "1" and j != "1":
        model.addConstr(u[i] - u[j] + M * x[i, j] <= M - 1)

  # Starting Node
  model.addConstr(u["1"] == 1)

  # Set objective
  model.setObjective(quicksum(nodes[i]['distances'][j] * x[i,j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

  # Solve model
  model.optimize()