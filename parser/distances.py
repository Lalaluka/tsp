import math

def distance_EUC_2D(x1, y1, x2, y2):
  return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

def distance_HAMILTON(x1, y1, x2, y2):
  raise NotImplementedError
