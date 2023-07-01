# Parser to read TSPLIB files
# http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
import re
from parser.distances import distance_EUC_2D, distance_HAMILTON

def append_node(nodes, x, y , name, distance_function):
    new_node = {
      'name': name,
      'coordinates': (x, y),
      'distances': {}
    }
    for node in nodes:
        x1, y1 = nodes[node]["coordinates"]
        x2, y2 = new_node['coordinates']
        if distance_function == "distance_EUC_2D":
          distance = distance_EUC_2D(x1, y1, x2, y2)
        elif distance_function == "distance_HAMILTON":
          distance = distance_HAMILTON(x1, y1, x2, y2)
        else:
          raise Exception("Distance function not implemented")
        
        nodes[node]['distances'][new_node['name']] = distance
        new_node['distances'][node] = distance
    
    nodes[new_node['name']] = new_node
    return nodes

def parseTSPLIBFile(path, save_debug=False):
  nodes = dict()
  with open(str(path), "r") as file:
    weight_type = "distance_EUC_2D"
    for line in file:
      if line.find("TYPE") == 0:
        if line.split(":")[1].strip() == "TSP":
          continue
        else:
          raise Exception("File is not a TSP file")
      if line.find("EDGE_WEIGHT_TYPE") == 0:
        if line.split(":")[1].strip() == "EUC_2D":
          weight_type = "distance_EUC_2D"
        else:
          raise Exception("File is not a EUC_2D file")
      if line.find("DIMENSION") > -1:
        n = int(line.split(":")[1])
      if re.match("[A-Z]", line) != None:
        continue

      res = line.replace("\n", "").split(" ")

      if len(res) >= 3:
        nodes = append_node(nodes, float(res[1]), float(res[2]), res[0], weight_type)

  if save_debug:
    with open("data/debug.txt", "w") as file:
      for node in nodes:
        file.write(str(node) + "\n")
        file.write(str(nodes[node]['coordinates']) + "\n")
        file.write(str(nodes[node]['distances']) + "\n")
        file.write("\n")

  return nodes
