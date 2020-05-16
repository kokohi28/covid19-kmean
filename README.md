# COVID-19 K-MEAN CLUSTERING IMPLEMENTATION (FROM SCRATCH)
Python repository for K-mean clustering implementation, case for Covid-19 data.

## Note
This project works with limitation(for now), as for :
- space/axis used 2 axis (cases and deaths)
- K limit from 2 until 5

## Preview
![Menu](https://github.com/kokohi28/covid19-kmean/blob/master/menu.png?raw=true)

SEA Cluster
![SEA Cluster](https://github.com/kokohi28/covid19-kmean/blob/master/sea_sample.png?raw=true)

Indonesia Daily Case Cluster
![Indonesia Daily](https://github.com/kokohi28/covid19-kmean/blob/master/indonesia_sample.png?raw=true)

## Requirements
* Python 3.7

## Requirements Library
* numpy ->
  $ pip install numpy

* pandas ->
  $ pip install pandas

* matplotlib ->
  $ pip install matplotlib

## File Structure
### py files
* const.py -> Constant for all python project files

* menu.py -> Handle terminal/command-line menu

* kmean.py -> Main k-mean calculation

* app-kmean.py -> Main program

### Excel / CSV files
* COVID-19-geographic-disbtribution-worldwide.xlsx -> Embedded source data file (until 2020 Mei 14)

## How to Run
$ python3 app-kmean.py
