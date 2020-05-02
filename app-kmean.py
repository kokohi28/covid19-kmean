import pandas as pd
import matplotlib.pyplot as plt
import const as CONST
import menu
import kmean

FILE_SRC = 'COVID-19-geographic-disbtribution-worldwide.xlsx'
SHEET = 'COVID-19-geographic-disbtributi'

# Data label
X_LABEL = 'cases'
Y_LABEL = 'deaths'

def doClusteringForWorld(data, K):
  print('\n>>> Clustering for World, with K: {}'.format(K))
  return

def doClusteringForSEA(data, K):
  print('\n>>> Clustering for SEA, with K: {}'.format(K))
  return

def doClusteringForContinent(data, continent, K):
  print('\n>>> Clustering for {} with K: {}'.format(continent, K))
  return

def doClusteringForCountry(data, country, K):
  print('\n>>> Clustering for {} with K: {}'.format(country, K))
  
  queryStr = 'countriesAndTerritories == "{}"'.format(country)
  data.query(queryStr, inplace = True)

  dataList = []
  for index, row in data.iterrows():
    pos = (row[X_LABEL], row[Y_LABEL])
    dataList.append(pos)
 
  cluster = kmean.clustering(dataList, K)
  plotGraph(dataList, cluster, country)

  return

def plotGraph(dataList, cluster, title):
    # Mapping scatter color
  colors = []
  colors.append('g')
  if k == 2:
    colors.append('r')
  elif k == 3:
    colors.append('y')
    colors.append('r')
  elif k == 4:
    colors.append('c')
    colors.append('m')
    colors.append('r')
  elif k == 5:
    colors.append('c')
    colors.append('m')
    colors.append('k')
    colors.append('r')

  # Draw scatter
  plt.figure(num=title)
  plt.xlabel(X_LABEL, fontsize=14)
  plt.ylabel(Y_LABEL, fontsize=14)

  for i in range(len(cluster)):
    pos = dataList[i]
    if cluster[i] == 0:
      plt.scatter(pos[CONST.X_IDX], pos[CONST.Y_IDX], c=colors[0], label='K1')
    elif cluster[i] == 1:
      plt.scatter(pos[CONST.X_IDX], pos[CONST.Y_IDX], c=colors[1], label='K2')
    elif cluster[i] == 2:
      plt.scatter(pos[CONST.X_IDX], pos[CONST.Y_IDX], c=colors[2], label='K3')
    elif cluster[i] == 3:
      plt.scatter(pos[CONST.X_IDX], pos[CONST.Y_IDX], c=colors[3], label='K4')
    elif cluster[i] == 4:
      plt.scatter(pos[CONST.X_IDX], pos[CONST.Y_IDX], c=colors[4], label='K5')

  # plt.legend(loc="best")

  # Show the plot lib
  plt.show()

  return
# main
if __name__ == '__main__':
  print('\nReading data...\n')
  data = pd.read_excel(FILE_SRC, sheet_name=SHEET)
  print(data.head())
  print(data.info())

  continents = []
  countries = []
  for index, row in data.iterrows():
    continent = row['continentExp']
    country = row['countriesAndTerritories']
    
    if continent not in continents:
      continents.append(continent)

    if country not in countries:
      countries.append(country)

  res = menu.menuLoop(continents, countries)
  zone = res[CONST.IDX_ZONE]
  subZone = res[CONST.IDX_SUB_ZONE]
  k = res[CONST.IDX_K]
  
  if zone == '' and subZone == '' and k == 0:
    print('Nothing Todo')
  elif k <= 1:
    print('No K specified')
  else:
    if zone == 'WORLD':
      doClusteringForWorld(data, k)
    elif zone == 'SEA':
      doClusteringForSEA(data, k)
    elif zone == 'CONTINENT':
      if subZone == '':
        print('No continent specified')
      else:
        doClusteringForContinent(data, subZone, k)
    elif zone == 'COUNTRY':
      if subZone == '':
        print('No continent specified')
      else:
        doClusteringForCountry(data, subZone, k)
    else:
      print('No zone specified')

  print('')
  print('Exiting...')
  print('')