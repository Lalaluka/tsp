from gurobipy import *

# Implementation of Dantzig, Fulkerson, and Johnson formulation for the TSP
# NAIVE IMPLEMENTATION no lazy constraints

def getPartitions(nodes):
  partitions = []
  halfiter = (len(nodes) // 2)+1
  nodes = range(len(nodes))
  for i in range(1, halfiter):
    for subset in itertools.combinations(nodes, i):
      S = set(subset)
      Scomp = set(nodes) - S
      partitions.append((S, Scomp))
      partitions.append((Scomp, S))

  return partitions

def solve(nodes, verbose=True):
  model = Model("TSP")

  if not verbose:
    model.setParam('OutputFlag', 0)

  # Variables

  ## x_ij = 1 if the edge (i,j) is in the solution
  x = {}
  for i in nodes:
    for j in nodes:
      if i != j:
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x(%s,%s)"%(i,j))

  # Constraints
  for i in nodes:
    model.addConstr(quicksum(x[i,j] for j in nodes if i < j)
                    + quicksum(x[j,i] for j in nodes if j < i) == 2)

  partitions = getPartitions(nodes)

  for (S, Scomp) in partitions:
    model.addConstr(quicksum(x[i+1, j+1] for i in S for j in Scomp if i != j) >= 2)

  # Set objective
  model.setObjective(quicksum(x[i, j] * nodes[i]['distances'][j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)


  # Set objective
  model.setObjective(quicksum(nodes[i]['distances'][j] * x[i,j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

  # Solve model
  model.optimize()