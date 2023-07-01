from parser.tsplibParser import parseTSPLIBFile

print("Welcome to this TSP Solver")

parser = "tsplibParser"
algo = "MTZ"
solver = "gurobi"
file = "data/st70.tsp"

if parser == "tsplibParser":
  nodes = parseTSPLIBFile(file, save_debug=True)
  if solver == "gurobi":
    if algo == "MTZ":
      from solvers.gurobi.MTZ import solve as solveMTZ
      solveMTZ(nodes)
    elif algo == "naiveDFJ":
      from solvers.gurobi.naiveDFJ import solve as solveNaiveDFJ
      solveNaiveDFJ(nodes)
    elif algo == "DFJ":
      from solvers.gurobi.DFJ import solve as solveDFJ
      solveDFJ(nodes)
    else:
      raise Exception("Algorithm not implemented")
  elif solver == "scip":
    if algo == "MTZ":
      from solvers.scip.MTZ import solve as solveMTZ
      solveMTZ(nodes)
    else:
      raise Exception("Algorithm not implemented")
  else:
    raise Exception("Solver not implemented")

