import const as CONST
import math

# class - function
class MemberDistance:
  def __init__(self, member, distance):
    self.member = member
    self.distance = distance

def calculate(data, centers, K):
  clusterSnapshot = []
  sse = 0

  sumX = []
  sumY = []
  n = []

  for j in range(K):
    sumX.append(0)
    sumY.append(0)
    n.append(0)

  for pos in data:
    x = pos[CONST.X_IDX]
    y = pos[CONST.Y_IDX]

    distances = []

    for j in range(K):
      centre = centers[j]
      d = math.sqrt(math.pow(x - centre[CONST.X_IDX], 2) + math.pow(y - centre[CONST.Y_IDX], 2))
      distance = MemberDistance(j, d)
      distances.append(distance)

    # sort membership distance
    distances.sort(key=lambda x: x.distance)

    # idx 0 zero is CLOSEST
    clusterSnapshot.append(distances[0].member)
    sse += math.pow(distances[0].distance, 2)
    
    sumX[distances[0].member] += x
    sumY[distances[0].member] += y
    n[distances[0].member] += 1

  else:
    print('clusterSnapshot: ' + str(clusterSnapshot))
    print('sse: ' + str(sse))
    # print('sumX: ' + str(sumX))
    # print('sumY: ' + str(sumY))
    # print('n: ' + str(n))

  newCenter = []
  for j in range(K):
    xNew = sumX[j] / n[j]
    yNew = sumY[j] / n[j]
    newCenter.append((xNew, yNew))

  print('newCenter: ' + str(newCenter))
  return (newCenter, clusterSnapshot, sse)

def clustering(data, k):
  print('')

  # Init center with data itself
  centerInit = []
  for i in range(k):
    centerInit.append(data[i])

  center = centerInit
  cluster = []

  # Loop until center same as previous
  i = 0
  isNotEqual = True
  while isNotEqual:
    i += 1
    print('loop at i-' + str(i) + ':')

    res = calculate(data, center, k)
    if center != res[CONST.RES_IDX_CENTER]:
      center = res[CONST.RES_IDX_CENTER]
    else:
      print('\nfinally equal at i-' + str(i))
      isNotEqual = False
      cluster = res[CONST.RES_IDX_SNAPSHOT]
    print('')

  return cluster