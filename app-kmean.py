import pandas as pd
import matplotlib.pyplot as plt
import const as CONST
import menu
import kmean

# source
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
# https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx
FILE_SRC = 'COVID-19-geographic-disbtribution-worldwide.xlsx'
SHEET = 'COVID-19-geographic-disbtributi'

# Data label
X_LABEL = 'cases'
Y_LABEL = 'deaths'

# CaseVelocity class
# .  [PARAM]
# .. id -> string
class CaseVelocity:
  id = ''
  sumCase = 0
  sumDeath = 0
  nData = 0
  population = 0

  def __init__(self, id):
    self.id = id

# Clustering for World Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForWorld(data, K):
  print('\n>>> Clustering for World, with K: {}'.format(K))

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  seaCases = {}
  for index, row in data.iterrows():
    case = row[X_LABEL]
    death = row[Y_LABEL]
    country = row[COUNTRY_LABEL]

    if country not in seaCases:
      countryCase = CaseVelocity(country)
      countryCase.population = row['popData2018']
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase
    else:
      countryCase = seaCases[country]
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase

  # Create list of tuple
  print('##############################################################################')
  print('Countries data:')
  dataList = []
  for c in seaCases:
    case = seaCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('\n{} -> population: {}, N-Data (N-Day): {}'.format(case.id, case.population, case.nData))
    print('SUM-Case:{}, Velocity (Case / N-Data):{}'.format(case.sumCase, caseVelocity))
    print('SUM-Death:{}, Velocity (Death / N-Data):{}'.format(case.sumDeath, deathVelocity))

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

  # Send list of tuple, and process clustering
  print('##############################################################################')
  print('Cluster result:')
  cluster = kmean.clustering(dataList, K)

  # Plot scatter graph
  print('##############################################################################')
  print('Graph:')
  plotScatterGraph(dataList, cluster, 'World')

  return

# Clustering for Southeast Asia (SEA) Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForSEA(data, K):
  print('\n>>> Clustering for SEA, with K: {}'.format(K))

  # Declare SEA countries
  seaCountries = []
  seaCountries.append('Brunei_Darussalam')
  seaCountries.append('Cambodia')
  seaCountries.append('Timor_Leste')
  seaCountries.append('Indonesia')
  seaCountries.append('Laos')
  seaCountries.append('Malaysia')
  seaCountries.append('Myanmar')
  seaCountries.append('Philippines')
  seaCountries.append('Singapore')
  seaCountries.append('Thailand')
  seaCountries.append('Vietnam')

  # Query - strip data
  queryStr = ''
  i = 0
  for country in seaCountries:
    if i == 0:
      queryStr += 'countriesAndTerritories == "{}"'.format(country)
    else:
      queryStr += ' or countriesAndTerritories == "{}"'.format(country)
    i += 1
  data.query(queryStr, inplace = True)

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  seaCases = {}
  for index, row in data.iterrows():
    case = row[X_LABEL]
    death = row[Y_LABEL]
    country = row[COUNTRY_LABEL]

    if country not in seaCases:
      countryCase = CaseVelocity(country)
      countryCase.population = row['popData2018']
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase
    else:
      countryCase = seaCases[country]
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase

  # Create list of tuple
  print('##############################################################################')
  print('Countries data:')
  dataList = []
  for c in seaCases:
    case = seaCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('\n{} -> population: {}, N-Data (N-Day): {}'.format(case.id, case.population, case.nData))
    print('SUM-Case:{}, Velocity (Case / N-Data):{}'.format(case.sumCase, caseVelocity))
    print('SUM-Death:{}, Velocity (Death / N-Data):{}'.format(case.sumDeath, deathVelocity))

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

  # Send list of tuple, and process clustering
  print('##############################################################################')
  print('Cluster result:')
  cluster = kmean.clustering(dataList, K)

  # Plot scatter graph
  print('##############################################################################')
  print('Graph:')
  plotScatterGraph(dataList, cluster, 'SEA')

  return

# Clustering for Continent Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForContinent(data, continent, K):
  print('\n>>> Clustering for {} with K: {}'.format(continent, K))

  # Query - strip data
  queryStr = 'continentExp == "{}"'.format(continent)
  data.query(queryStr, inplace = True)

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  seaCases = {}
  for index, row in data.iterrows():
    case = row[X_LABEL]
    death = row[Y_LABEL]
    country = row[COUNTRY_LABEL]

    if country not in seaCases:
      countryCase = CaseVelocity(country)
      countryCase.population = row['popData2018']
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase
    else:
      countryCase = seaCases[country]
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      seaCases[country] = countryCase

  # Create list of tuple
  print('##############################################################################')
  print('Countries data:')
  dataList = []
  for c in seaCases:
    case = seaCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('\n{} -> population: {}, N-Data (N-Day): {}'.format(case.id, case.population, case.nData))
    print('SUM-Case:{}, Velocity (Case / N-Data):{}'.format(case.sumCase, caseVelocity))
    print('SUM-Death:{}, Velocity (Death / N-Data):{}'.format(case.sumDeath, deathVelocity))

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

  # Send list of tuple, and process clustering
  print('##############################################################################')
  print('Cluster result:')
  cluster = kmean.clustering(dataList, K)

  # Plot scatter graph
  print('##############################################################################')
  print('Graph:')
  plotScatterGraph(dataList, cluster, continent)

  return

# Clustering for Country Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForCountry(data, country, K):
  print('\n>>> Clustering for {} with K: {}'.format(country, K))
  
  # Query - strip data
  queryStr = 'countriesAndTerritories == "{}"'.format(country)
  data.query(queryStr, inplace = True)

  # Create list of tuple
  META_LABEL = 'dateRep'
  dataList = []
  for index, row in data.iterrows():
    entry = (row[X_LABEL], row[Y_LABEL], row[META_LABEL])
    dataList.append(entry)
 
  # Send list of tuple, and process clustering
  print('##############################################################################')
  print('Cluster result:')
  cluster = kmean.clustering(dataList, K)

  # Plot scatter graph
  print('##############################################################################')
  print('Graph:')
  plotScatterGraph(dataList, cluster, country)

  return

# Draw Catter Graph
# .  [PARAM]
# .. dataList -> list tuple, ex: [(1, 2), (2, 0), <META>]
# .. cluster -> list
# .. title -> string
# .
def plotScatterGraph(dataList, cluster, title):
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

  # Add graph info
  plt.figure(num=title)
  plt.xlabel(X_LABEL, fontsize=14)
  plt.ylabel(Y_LABEL, fontsize=14)

  # Draw scatter
  for i in range(len(cluster)):
    entry = dataList[i]
    if cluster[i] == 0:
      plt.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[0], label='K1')
    elif cluster[i] == 1:
      plt.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[1], label='K2')
    elif cluster[i] == 2:
      plt.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[2], label='K3')
    elif cluster[i] == 3:
      plt.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[3], label='K4')
    elif cluster[i] == 4:
      plt.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[4], label='K5')

  # plt.legend(loc="best")

  # Show the plot lib
  plt.show()

  return

# MAIN PROGRAM
if __name__ == '__main__':
  print('\nReading data...\n')

  # Reading source file
  data = pd.read_excel(FILE_SRC, sheet_name=SHEET)
  print(data.head())
  print(data.info())

  # Extract continents and countries list
  continents = []
  countries = []
  for index, row in data.iterrows():
    continent = row['continentExp']
    country = row['countriesAndTerritories']
    
    if continent not in continents:
      continents.append(continent)

    if country not in countries:
      countries.append(country)

  # Handle user input by Menu
  res = menu.menuLoop(continents, countries)

  # Parse zone, subZone and k
  zone = res[CONST.IDX_ZONE]
  subZone = res[CONST.IDX_SUB_ZONE]
  k = res[CONST.IDX_K]
  
  # Call the clustering function, respected by zone, subZone and k
  # And plot/draw the clusters result
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