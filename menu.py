import os
import const as CONST

# Const
MENU_ROOT = 0
MENU_SELECT_COUNTRY = 1
MENU_SELECT_CONTINENT = 2
MENU_SELECT_K_FOR_COUNTRY = 3
MENU_SELECT_K_FOR_SEA = 4
MENU_SELECT_K_FOR_CONTINENT = 5
MENU_SELECT_K_FOR_WORLD = 6

prevMenu = MENU_ROOT
currMenu = MENU_ROOT

def welcomeMessage():
  print('##############################################################')
  print('##                                                          ##')
  print('##   COVID-19 K-MEAN CLUSTERING IMPLEMENTATION              ##')
  print('##                                                          ##')
  print('##   BY : - M. Khafidhun Alim Muslim (17051204063)          ##')
  print('##        - Akhmad Hilmy Zakaria (17051204028)              ##')
  print('##        - Koko Himawan Permadi (19051204111)              ##')
  print('##                                                          ##')
  print('##############################################################')
  return

def menuSelectK(cluster):
  print(f'\nSpecify K for {cluster} cluster ({CONST.MIN_K}-{CONST.MAX_K}):')
  print('')
  print('Press [B] for Back')
  return

def menuSelectContinent(continents):
  print('')
  print('Select continent :')
  for i in range(len(continents)):
    print(f'{(i + 1)}. {continents[i]}')
  print('')
  print('Press [B] for Back')
  return

def menuSelectCountries(countries):
  print('')
  print('Select country :')
  for i in range(len(countries)):
    print(f'{(i + 1)}. {countries[i]}')
  print('')
  print('Press [B] for Back')
  return

def menuRoot():
  print('\nSelect Operation:')
  print('1. Clustering by Country')
  print('2. Clustering for SEA (Southeast Asia) region')
  print('3. Clustering by Continent')
  print('4. Clustering World')
  print('')
  print('Press [Q] for Exit')
  return

def handleInputK(inputVal):
  global currMenu
  global prevMenu

  if inputVal == 'B' or \
     inputVal == 'b':
    currMenu = prevMenu
    return 0
  else:
    if inputVal.isnumeric():
      num = int(inputVal)
      if num == 0 or \
         num == 1 or \
         num > CONST.MAX_K:
        print(f'\n{num} is INVALID, Specify {CONST.MIN_K} until {CONST.MAX_K}... (Press ENTER to continue)')
        input('')
        return 0
      else :
        return num
    else:
      print(f'\nINVALID Input, Specify {CONST.MIN_K} until {CONST.MAX_K}... (Press ENTER to continue)')
      input('')
      return 0

def handleInputContinent(inputVal, continents):
  global currMenu
  global prevMenu

  if inputVal == 'B' or \
     inputVal == 'b':
    currMenu = prevMenu
    return ''
  else:
    size = len(continents)
    if inputVal.isnumeric():
      num = int(inputVal)
      if num == 0 or \
         num > size:
        print('\nSelection INVALID... (Press ENTER to continue)')
        input('')
        return ''
      else:
        return continents[num - 1]
    else:
      print('\nSelection INVALID... (Press ENTER to continue)')
      input('')
      return ''

def handleInputCountry(inputVal, countries):
  global currMenu
  global prevMenu

  if inputVal == 'B' or \
     inputVal == 'b':
    currMenu = prevMenu
    return ''
  else:
    size = len(countries)
    if inputVal.isnumeric():
      num = int(inputVal)
      if num == 0 or \
         num > size:
        print('\nSelection INVALID... (Press ENTER to continue)')
        input('')
        return ''
      else:
        return countries[num - 1]
    else:
      print('\nSelection INVALID... (Press ENTER to continue)')
      input('')
      return ''

def menuLoop(continents, countries):
  loopMenu = True
  global currMenu
  global prevMenu

  zone = ''
  subZone = ''
  k = 0

  while loopMenu:
    try:
      # Clear screen
      os.system('cls' if os.name == 'nt' else 'clear')

      # Display
      welcomeMessage()
      
      if currMenu == MENU_ROOT:
        menuRoot()
      elif currMenu == MENU_SELECT_COUNTRY:
        menuSelectCountries(countries)
      elif currMenu == MENU_SELECT_CONTINENT:
        menuSelectContinent(continents)
      elif currMenu == MENU_SELECT_K_FOR_WORLD or \
           currMenu == MENU_SELECT_K_FOR_SEA:
        menuSelectK(zone)
      elif currMenu == MENU_SELECT_K_FOR_CONTINENT or \
          currMenu == MENU_SELECT_K_FOR_COUNTRY:
        menuSelectK(zone + '-' + subZone)

      # Input
      inputVal = input("Select: ")

      if inputVal == 'Q' or \
        inputVal == 'q':
        zone = ''
        subZone = ''
        k = 0

        loopMenu = False
      else:
        # Root
        if currMenu == MENU_ROOT:
          if inputVal == '1':
            zone = 'COUNTRY'
            currMenu = MENU_SELECT_COUNTRY
            prevMenu = MENU_ROOT
          elif inputVal == '2':
            zone = 'SEA'
            currMenu = MENU_SELECT_K_FOR_SEA
            prevMenu = MENU_ROOT
          elif inputVal == '3':
            zone = 'CONTINENT'
            currMenu = MENU_SELECT_CONTINENT
            prevMenu = MENU_ROOT
          elif inputVal == '4':
            zone = 'WORLD'
            currMenu = MENU_SELECT_K_FOR_WORLD
            prevMenu = MENU_ROOT

        # Select Country
        elif currMenu == MENU_SELECT_COUNTRY:
          subZone = handleInputCountry(inputVal, countries)
          if subZone != '':
            currMenu = MENU_SELECT_K_FOR_COUNTRY
            prevMenu = MENU_SELECT_COUNTRY

        # Select Continent
        elif currMenu == MENU_SELECT_CONTINENT:
          subZone = handleInputContinent(inputVal, continents)
          if subZone != '':
            currMenu = MENU_SELECT_K_FOR_CONTINENT
            prevMenu = MENU_SELECT_CONTINENT

        # K for world
        elif currMenu == MENU_SELECT_K_FOR_WORLD or \
            currMenu == MENU_SELECT_K_FOR_CONTINENT or \
            currMenu == MENU_SELECT_K_FOR_COUNTRY or \
            currMenu == MENU_SELECT_K_FOR_SEA:
          k = handleInputK(inputVal)
          if k > 1:
            loopMenu = False
          else:
            prevMenu = MENU_ROOT

    except KeyboardInterrupt:
      zone = ''
      subZone = ''
      k = 0

      loopMenu = False

  return (zone, subZone, k)