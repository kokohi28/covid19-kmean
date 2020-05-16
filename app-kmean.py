# dataframe, numpy
import pandas as pd
import numpy as np

# graph
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# local module
import const as CONST
import menu
import kmean

# downloader file
import urllib.request

# common
import os
import time
from os import path
from datetime import datetime

# source
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
LINK_SRC = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
DOWNLOADED_SRC = 'COVID-19-geographic-disbtribution-worldwide.xlsx'
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
def doClusteringForWorld(df, K):
  print(f'\n>>> Clustering for World, with K: {K}')

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  worldCases = {}
  for index, row in df.iterrows():
    case = row[X_LABEL]
    death = row[Y_LABEL]
    country = row[COUNTRY_LABEL]

    if country not in worldCases:
      countryCase = CaseVelocity(country)
      countryCase.population = row['popData2018']
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      worldCases[country] = countryCase
    else:
      countryCase = worldCases[country]
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      worldCases[country] = countryCase

  # Create list of tuple
  print(f'\nCountries data [{len(worldCases)}]:')
  dataList = []
  i = 1
  for c in worldCases:
    case = worldCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('--------------------------------------------------------------')
    print(f'{i}. {case.id} -> population: {case.population:,.0f}   N(Day): {case.nData}')
    print(f'• sum-case: {case.sumCase:,.0f}   velocity (case / N): {caseVelocity:,.2f}')
    print(f'• sum-death: {case.sumDeath:,.0f}   velocity (death / N): {deathVelocity:,.2f}')

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

    i += 1

  # Send list of tuple, and process clustering
  print('\nClustering…\n')
  cluster = kmean.clustering(dataList, K)

  # Create clusterSize and print cluster result 
  clusterSize = {}
  print('Cluster result:')
  for i in range(len(dataList)):
    print(f'{i + 1}. {dataList[i][CONST.META_IDX]} - {cluster[i]}')
    
    clusterKey = f'cluster-{cluster[i]}'
    if clusterKey in clusterSize:
      currVal = clusterSize[clusterKey]
      clusterSize[clusterKey] = currVal + 1
    else:
      clusterSize[clusterKey] = 1
  
  print('\nSize of cluster member :')
  for key in clusterSize:
    print(f'* {key} : {clusterSize[key]}')

  # sort dataframe first
  # df = df.sort_values(by='dateRep', ascending=True) # FAIL to SORT
  # dtMin = df.loc[df.index.max(), 'dateRep']
  # dtMax = df.loc[df.index.min(), 'dateRep']
  # title = f'World covid-19 data {dtMin.strftime("%Y/%m/%d")} - {dtMax.strftime("%Y/%m/%d")}'
  title = 'World covid-19 data'

  # Plot scatter graph
  print('\nProcessing Graph…')
  scatterGraphCountryAvgCase(dataList, cluster, clusterSize, title, K)

  return

# Clustering for Southeast Asia (SEA) Data
# .  [PARAM]
# .. df -> pandas DataFrame
# .. K -> number
# .
def doClusteringForSEA(df, K):
  print(f'\n>>> Clustering for SEA, with K: {K}')

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
      queryStr += f'countriesAndTerritories == "{country}"'
    else:
      queryStr += f' or countriesAndTerritories == "{country}"'
    i += 1
  df.query(queryStr, inplace = True)

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  seaCases = {}
  for index, row in df.iterrows():
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
  print(f'\nCountries data [{len(seaCases)}]:')
  dataList = []
  i = 1
  for c in seaCases:
    case = seaCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('--------------------------------------------------------------')
    print(f'{i}. {case.id} -> population: {case.population:,.0f}   N(Day): {case.nData}')
    print(f'• sum-case: {case.sumCase:,.0f}   velocity (case / N): {caseVelocity:,.2f}')
    print(f'• sum-death: {case.sumDeath:,.0f}   velocity (death / N): {deathVelocity:,.2f}')

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

    i += 1

  # Send list of tuple, and process clustering
  print('\nClustering…\n')
  cluster = kmean.clustering(dataList, K)

  # Create clusterSize and print cluster result 
  clusterSize = {}
  print('Cluster result:')
  for i in range(len(dataList)):
    print(f'{i + 1}. {dataList[i][CONST.META_IDX]} - {cluster[i]}')
    
    clusterKey = f'cluster-{cluster[i]}'
    if clusterKey in clusterSize:
      currVal = clusterSize[clusterKey]
      clusterSize[clusterKey] = currVal + 1
    else:
      clusterSize[clusterKey] = 1
  
  print('\nSize of cluster member :')
  for key in clusterSize:
    print(f'* {key} : {clusterSize[key]}')

  # sort dataframe first
  # df = df.sort_values(by='dateRep', ascending=True) # FAIL to SORT
  # dtMin = df.loc[df.index.max(), 'dateRep']
  # dtMax = df.loc[df.index.min(), 'dateRep']
  # title = f'SEA covid-19 data {dtMin.strftime("%Y/%m/%d")} - {dtMax.strftime("%Y/%m/%d")}'
  title = 'SEA covid-19 data'

  # Plot scatter graph
  print('\nProcessing Graph…')
  scatterGraphCountryAvgCase(dataList, cluster, clusterSize, title, K)

  return

# Clustering for Continent Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForContinent(df, continent, K):
  print(f'\n>>> Clustering for {continent} with K: {K}')

  # Query - strip data
  queryStr = f'continentExp == "{continent}"'
  df.query(queryStr, inplace = True)

  # Sum cases and death based country
  COUNTRY_LABEL = 'countriesAndTerritories'
  continentCases = {}
  for index, row in df.iterrows():
    case = row[X_LABEL]
    death = row[Y_LABEL]
    country = row[COUNTRY_LABEL]

    if country not in continentCases:
      countryCase = CaseVelocity(country)
      countryCase.population = row['popData2018']
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      continentCases[country] = countryCase
    else:
      countryCase = continentCases[country]
      countryCase.sumCase += case
      countryCase.sumDeath += death
      countryCase.nData += 1

      continentCases[country] = countryCase

  # Create list of tuple
  print(f'\nCountries data [{len(continentCases)}]:')
  dataList = []
  i = 1
  for c in continentCases:
    case = continentCases[c]

    # Velocity based on n Cases/Data
    caseVelocity = case.sumCase / case.nData
    deathVelocity = case.sumDeath / case.nData

    print('--------------------------------------------------------------')
    print(f'{i}. {case.id} -> population: {case.population:,.0f}   N(Day): {case.nData}')
    print(f'• sum-case: {case.sumCase:,.0f}   velocity (case / N): {caseVelocity:,.2f}')
    print(f'• sum-death: {case.sumDeath:,.0f}   velocity (death / N): {deathVelocity:,.2f}')

    entry = (caseVelocity, deathVelocity, case.id)
    dataList.append(entry)

    i += 1

  # Send list of tuple, and process clustering
  print('\nClustering…\n')
  cluster = kmean.clustering(dataList, K)

  # Create clusterSize and print cluster result 
  clusterSize = {}
  print('Cluster result:')
  for i in range(len(dataList)):
    print(f'{i + 1}. {dataList[i][CONST.META_IDX]} - {cluster[i]}')
    
    clusterKey = f'cluster-{cluster[i]}'
    if clusterKey in clusterSize:
      currVal = clusterSize[clusterKey]
      clusterSize[clusterKey] = currVal + 1
    else:
      clusterSize[clusterKey] = 1
  
  print('\nSize of cluster member :')
  for key in clusterSize:
    print(f'* {key} : {clusterSize[key]}')

  # sort dataframe first
  # df = df.sort_values(by='dateRep', ascending=True) # FAIL to SORT
  # dtMin = df.loc[df.index.max(), 'dateRep']
  # dtMax = df.loc[df.index.min(), 'dateRep']
  # title = f'{continent} covid-19 data {dtMin.strftime("%Y/%m/%d")} - {dtMax.strftime("%Y/%m/%d")}'
  title = f'{continent} covid-19 data'

  # Plot scatter graph
  print('\nProcessing Graph…')
  scatterGraphCountryAvgCase(dataList, cluster, clusterSize, title, K)

  return

# Clustering for Country Data
# .  [PARAM]
# .. data -> pandas DataFrame
# .. K -> number
# .
def doClusteringForCountry(df, country, K):
  print(f'\n>>> Clustering for {country} with K: {K}')
  
  # Query - strip data
  queryStr = f'countriesAndTerritories == "{country}"'
  df.query(queryStr, inplace = True)

  # Create list of tuple
  META_LABEL = 'dateRep'
  dataList = []
  for index, row in df.iterrows():
    entry = (row[X_LABEL], row[Y_LABEL], row[META_LABEL])
    dataList.append(entry)
 
  # Send list of tuple, and process clustering
  print('\nClustering…\n')
  cluster = kmean.clustering(dataList, K)

  # Create clusterSize and print cluster result 
  clusterSize = {}
  print('Cluster result:')
  for i in range(len(dataList)):
    if type(dataList[i][CONST.META_IDX]) is datetime.date:
      print(f'{i + 1}. {dataList[i][CONST.META_IDX].strftime("%Y/%m/%d")} - {cluster[i]}')
    else:
      print(f'{i + 1}. {dataList[i][CONST.META_IDX]} - {cluster[i]}')
    
    clusterKey = f'cluster-{cluster[i]}'
    if clusterKey in clusterSize:
      currVal = clusterSize[clusterKey]
      clusterSize[clusterKey] = currVal + 1
    else:
      clusterSize[clusterKey] = 1
  
  print('\nSize of cluster member :')
  for key in clusterSize:
    print(f'* {key} : {clusterSize[key]}')

  # sort dataframe first
  df = df.sort_values(by='dateRep', ascending=True) # FAIL to SORT
  dtMin = df.loc[df.index.max(), 'dateRep']
  dtMax = df.loc[df.index.min(), 'dateRep']
  title = f'{country}'
  if type(dtMin) is datetime.date and type(dtMax) is datetime.date:
    title = f'{country} covid-19 data {dtMin.strftime("%Y/%m/%d")} - {dtMax.strftime("%Y/%m/%d")}'
  else:
    title = f'{country} covid-19 data {dtMin} - {dtMax}'

  # Plot scatter graph
  print('\nProcessing Graph…')
  scatterGraphCountryAvgCase(dataList, cluster, clusterSize, title, K)

  return

# Draw Scatter Graph per country velocity value
# .  [PARAM]
# .. dataList -> list tuple, ex: [(1, 2), (2, 0), <META>]
# .. cluster -> list
# .. title -> string
# .
def scatterGraphCountryAvgCase(dataList, cluster, clusterSize, title, k):
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

  # define view list
  viewList = ['COUNTRY', 'CLUSTER']

  # Add graph info
  fig, ax = plt.subplots(num=title)
  plt.subplots_adjust(bottom=0.2)

  bnext = None
  blabel = None
  listIdx = 1
  labelInc = 0

  def incDraw(currentList, showLabel):
    # Export global and nonlocal var
    global plt
    nonlocal k
    nonlocal clusterSize
    nonlocal ax

    # Clear graph
    ax.clear()

    # Country view
    if currentList == 'COUNTRY':
      # Re-plot, Add graph info
      ax.set_title(f'Cluster distribution')
      ax.set_xlabel('case / day', fontsize=11)
      ax.set_ylabel('death / day', fontsize=11)
      ax.tick_params(axis='both', which='major', labelsize=10)
      ax.tick_params(axis='both', which='minor', labelsize=8)
      ax.grid(linestyle='-', linewidth='0.3', color='gray')

      # Draw scatter
      for i in range(len(cluster)):
        entry = dataList[i]
        if cluster[i] == 0:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[0], label='K1')
        elif cluster[i] == 1:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[1], label='K2')
        elif cluster[i] == 2:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[2], label='K3')
        elif cluster[i] == 3:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[3], label='K4')
        elif cluster[i] == 4:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[4], label='K5')

        if showLabel:
          ax.text(entry[CONST.X_IDX], entry[CONST.Y_IDX], entry[CONST.META_IDX], size=7) 

    elif currentList == 'CLUSTER':
      # Re-plot, Add graph info
      ax.set_title(f'Cluster member size with K={k}')
      ax.set_xlabel('size', fontsize=11)
      ax.set_ylabel('cluster', fontsize=11)
      ax.tick_params(axis='both', which='major', labelsize=9)
      ax.tick_params(axis='both', which='minor', labelsize=7)

      # plot data
      xdata = [ key for key in clusterSize ]
      ydata = [ clusterSize[key] for key in clusterSize ]
      for i in range(len(xdata)):
        if xdata[i] == 'cluster-0':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[0], label='K1')
        elif xdata[i] == 'cluster-1':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[1], label='K1')
        elif xdata[i] == 'cluster-2':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[2], label='K1')
        elif xdata[i] == 'cluster-3':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[3], label='K1')
        elif xdata[i] == 'cluster-4':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[4], label='K1')

      ax.invert_yaxis()  # labels read top-to-bottom

    # Plot
    ax.draw(renderer=None, inframe=False)
    plt.pause(0.0001)

  # Button Next event
  def next(event):
    # Export global and nonlocal var
    nonlocal bnext
    nonlocal listIdx
    nonlocal viewList

    # set current
    currentList = viewList[listIdx]
    # print(f'\nProcessing - {currentList}')

    incDraw(currentList, True)

    # Button label for next
    listIdx = listIdx + 1
    if listIdx >= len(viewList):
      listIdx = 0
    bnext.label.set_text(viewList[listIdx])

  # Button Label event
  def swicth(event):
    # Export global and nonlocal var
    nonlocal blabel
    nonlocal labelInc
    nonlocal listIdx
    nonlocal viewList

    labelInc += 1
    # print(f'LABEL-{labelInc % 2}')

    # get prev list
    prevList = listIdx - 1
    if prevList < 0:
      prevList = len(viewList) - 1

    if labelInc % 2 == 1:
      blabel.label.set_text('LABEL-ON')
      incDraw(viewList[prevList], False)
    else:
      blabel.label.set_text('LABEL-OFF')
      incDraw(viewList[prevList], True)

  # Create button Predict
  axlabel = plt.axes([0.7, 0.05, 0.1, 0.075])
  axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
  bnext = Button(axnext, viewList[1]) # CLUSTER NEXT
  bnext.on_clicked(next)
  blabel = Button(axlabel, 'LABEL-OFF') # OFF FIRST
  blabel.on_clicked(swicth)

  ax.set_title(f'Cluster distribution')
  ax.set_xlabel('case / day', fontsize=11)
  ax.set_ylabel('death / day', fontsize=11)
  ax.tick_params(axis='both', which='major', labelsize=10)
  ax.tick_params(axis='both', which='minor', labelsize=8)
  ax.grid(linestyle='-', linewidth='0.3', color='gray')

  # Draw scatter
  for i in range(len(cluster)):
    entry = dataList[i]
    if cluster[i] == 0:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[0], label='K1')
    elif cluster[i] == 1:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[1], label='K2')
    elif cluster[i] == 2:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[2], label='K3')
    elif cluster[i] == 3:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[3], label='K4')
    elif cluster[i] == 4:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[4], label='K5')

    ax.text(entry[CONST.X_IDX], entry[CONST.Y_IDX], entry[CONST.META_IDX], size=7)  

  # plt.legend(loc="best")

  # Show the plot lib
  plt.show()

  return

# Draw Scatter Graph per country date
# .  [PARAM]
# .. dataList -> list tuple, ex: [(1, 2), (2, 0), <META>]
# .. cluster -> list
# .. title -> string
# .
def scatterGraphCountryDate(dataList, cluster, clusterSize, title, k):
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

  # define view list
  viewList = ['DATE', 'CLUSTER']

  # Add graph info
  fig, ax = plt.subplots(num=title)
  plt.subplots_adjust(bottom=0.2)

  bnext = None
  blabel = None
  listIdx = 1
  labelInc = 0

  def incDraw(currentList, showLabel):
    # Export global and nonlocal var
    global plt
    nonlocal k
    nonlocal clusterSize
    nonlocal ax

    # Clear graph
    ax.clear()

    # Country view
    if currentList == 'DATE':
      # Re-plot, Add graph info
      ax.set_title(f'Cluster distribution')
      ax.set_xlabel('case', fontsize=11)
      ax.set_ylabel('death', fontsize=11)
      ax.tick_params(axis='both', which='major', labelsize=10)
      ax.tick_params(axis='both', which='minor', labelsize=8)
      ax.grid(linestyle='-', linewidth='0.3', color='gray')

      # Draw scatter
      for i in range(len(cluster)):
        entry = dataList[i]
        if cluster[i] == 0:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[0], label='K1')
        elif cluster[i] == 1:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[1], label='K2')
        elif cluster[i] == 2:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[2], label='K3')
        elif cluster[i] == 3:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[3], label='K4')
        elif cluster[i] == 4:
          ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[4], label='K5')

        if showLabel:
          ax.text(entry[CONST.X_IDX], entry[CONST.Y_IDX], entry[CONST.META_IDX].strftime("%Y/%m/%d"), size=7) 

    elif currentList == 'CLUSTER':
      # Re-plot, Add graph info
      ax.set_title(f'Cluster member size with K={k}')
      ax.set_xlabel('size', fontsize=11)
      ax.set_ylabel('cluster', fontsize=11)
      ax.tick_params(axis='both', which='major', labelsize=9)
      ax.tick_params(axis='both', which='minor', labelsize=7)

      # plot data
      xdata = [ key for key in clusterSize ]
      ydata = [ clusterSize[key] for key in clusterSize ]
      for i in range(len(xdata)):
        if xdata[i] == 'cluster-0':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[0], label='K1')
        elif xdata[i] == 'cluster-1':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[1], label='K1')
        elif xdata[i] == 'cluster-2':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[2], label='K1')
        elif xdata[i] == 'cluster-3':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[3], label='K1')
        elif xdata[i] == 'cluster-4':
          ax.barh(xdata[i], ydata[i], align='center', color=colors[4], label='K1')

      ax.invert_yaxis()  # labels read top-to-bottom

    # Plot
    ax.draw(renderer=None, inframe=False)
    plt.pause(0.0001)

  # Button Next event
  def next(event):
    # Export global and nonlocal var
    nonlocal bnext
    nonlocal listIdx
    nonlocal viewList

    # set current
    currentList = viewList[listIdx]
    # print(f'\nProcessing - {currentList}')

    incDraw(currentList, True)

    # Button label for next
    listIdx = listIdx + 1
    if listIdx >= len(viewList):
      listIdx = 0
    bnext.label.set_text(viewList[listIdx])

  # Button Label event
  def swicth(event):
    # Export global and nonlocal var
    nonlocal blabel
    nonlocal labelInc
    nonlocal listIdx
    nonlocal viewList

    labelInc += 1
    # print(f'LABEL-{labelInc % 2}')

    # get prev list
    prevList = listIdx - 1
    if prevList < 0:
      prevList = len(viewList) - 1

    if labelInc % 2 == 1:
      blabel.label.set_text('LABEL-ON')
      incDraw(viewList[prevList], False)
    else:
      blabel.label.set_text('LABEL-OFF')
      incDraw(viewList[prevList], True)

  # Create button Predict
  axlabel = plt.axes([0.7, 0.05, 0.1, 0.075])
  axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
  bnext = Button(axnext, viewList[1]) # CLUSTER NEXT
  bnext.on_clicked(next)
  blabel = Button(axlabel, 'LABEL-OFF') # OFF FIRST
  blabel.on_clicked(swicth)

  ax.set_title(f'Cluster distribution')
  ax.set_xlabel('case', fontsize=11)
  ax.set_ylabel('death', fontsize=11)
  ax.tick_params(axis='both', which='major', labelsize=10)
  ax.tick_params(axis='both', which='minor', labelsize=8)
  ax.grid(linestyle='-', linewidth='0.3', color='gray')

  # Draw scatter
  for i in range(len(cluster)):
    entry = dataList[i]
    if cluster[i] == 0:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[0], label='K1')
    elif cluster[i] == 1:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[1], label='K2')
    elif cluster[i] == 2:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[2], label='K3')
    elif cluster[i] == 3:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[3], label='K4')
    elif cluster[i] == 4:
      ax.scatter(entry[CONST.X_IDX], entry[CONST.Y_IDX], c=colors[4], label='K5')

    ax.text(entry[CONST.X_IDX], entry[CONST.Y_IDX], entry[CONST.META_IDX].strftime("%Y/%m/%d"), size=7)  

  # plt.legend(loc="best")

  # Show the plot lib
  plt.show()

  return

# MAIN PROGRAM
if __name__ == '__main__':
  print('\nReading data…\n')
  
  srcExcel = f'cov19-worldwide-{datetime.now().strftime("%Y-%m-%d")}.xls'
  # Try read Buffer File
  fileBuffExist = path.exists(srcExcel)
  if fileBuffExist:
    print(f'Reading data from local: {srcExcel}')
  else:
    try:
      print('Downloading…')
      link = LINK_SRC
      urllib.request.urlretrieve(link, srcExcel)
    except urllib.error.HTTPError as ex:
      print('Download FAILED')
      print(ex)

      print(f'\nUsing EMBEDDED SOURCE: {DOWNLOADED_SRC}')
      srcExcel = DOWNLOADED_SRC

  # Reading source file
  df = pd.read_excel(srcExcel, sheet_name=SHEET)
  print(df.head())

  # Extract continents and countries list
  continents = []
  countries = []
  for index, row in df.iterrows():
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
      doClusteringForWorld(df, k)
    elif zone == 'SEA':
      doClusteringForSEA(df, k)
    elif zone == 'CONTINENT':
      if subZone == '':
        print('No continent specified')
      else:
        doClusteringForContinent(df, subZone, k)
    elif zone == 'COUNTRY':
      if subZone == '':
        print('No continent specified')
      else:
        doClusteringForCountry(df, subZone, k)
    else:
      print('No zone specified')

  print('')
  print('Exiting…')
  print('')