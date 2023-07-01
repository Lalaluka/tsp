from gurobipy import *
import networkx as nx

epsilon = 0.0000000001

def solve(nodes, verbose=True, mode="classic"):
  if mode == "cb":
    return solveCB(nodes, verbose)
  else:
    return solveClassic(nodes, verbose)
   
# Implementation of Dantzig, Fulkerson, and Johnson formulation for the TSP using lazy constraints
def solveCB(nodes, verbose=True):
  model = Model("TSP")
    
  # Variables
  x = {}
  for i in nodes:
    for j in nodes:
      if i != j:
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x(%s,%s)"%(i,j))

  # Constraints
  for i in nodes:
    model.addConstr(quicksum(x[i,j] for j in nodes if i < j)
                  + quicksum(x[j,i] for j in nodes if j < i) == 2)
    
  # Set objective
  model.setObjective(quicksum(x[i, j] * nodes[i]['distances'][j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

  # Callback adding Cuts
  def cb(model, where):
    if where == GRB.Callback.MIPSOL or where == GRB.Callback.MIPNODE:
      if where == GRB.Callback.MIPSOL:
        rel = model.cbGetSolution(x)
      else:
        status = model.cbGet(GRB.Callback.MIPNODE_STATUS)
        if status != GRB.OPTIMAL:
          return

        rel = model.cbGetNodeRel(x)
      G = nx.Graph()
      for i in nodes:
        for j in nodes:
          if i >= j:
            continue
          G.add_edge(i, j, weight=max(0,rel[i,j]))
        cut_val, partition = nx.stoer_wagner(G)
      
        if cut_val < 2 - epsilon:
          violated_cut = []
          for i in partition[0]:
            for j in partition[1]:
              if i < j:
                violated_cut.append((i,j))
              else:
                violated_cut.append((j,i))
          model.cbLazy(quicksum(x[i,j] for (i,j) in violated_cut) >= 2)  
          SECs_added += 1

  model.params.LazyConstraints = 1
  model.optimize(cb)

# Implementation of Dantzig, Fulkerson, and Johnson formulation for the TSP
def solveClassic(nodes, verbose=True):
  model = Model("TSP")
    
  # Variables
  x = {}
  for i in nodes:
    for j in nodes:
      if i != j:
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x(%s,%s)"%(i,j))

  # Constraints
  for i in nodes:
    model.addConstr(quicksum(x[i,j] for j in nodes if i < j)
                  + quicksum(x[j,i] for j in nodes if j < i) == 2)
    
  # Set objective
  model.setObjective(quicksum(x[i, j] * nodes[i]['distances'][j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

  SEC_amount = 0

  while True:
      model.optimize()
      G = nx.Graph()
      for i in nodes:
          for j in nodes:
              if i >= j:
                  continue
              G.add_edge(i, j, weight=max(0,x[i,j].x))
      
      cut_val, partition = nx.stoer_wagner(G)
      if cut_val < 2 - epsilon:
          violated_cut = []
          for i in partition[0]:
              for j in partition[1]:
                  if i < j:
                      violated_cut.append((i,j))
                  else:
                      violated_cut.append((j,i))
          model.addConstr(quicksum(x[i,j] for (i,j) in violated_cut) >= 2)        
          SEC_amount += 1
      else:    
        break

  model.optimize()
