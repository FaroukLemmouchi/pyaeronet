<<<<<<< HEAD
from pyaeronet import aeronet
import  numpy as np
import pandas as pd
import os

db_path = os.getenv('aeronet_db_path')

sites_table = aeronet.site() #pd.read_csv('/home/flemmouchi/lib/aeronet/sites.csv', sep=',', skiprows=1)
=======
import pyaeronet.aeronet as aeronet
import  numpy as np
import pandas as pd
from sys import exit
import os

db_path = os.getenv('aeronet_db_path')
sites_table = pd.read_csv(f'{aeronet_db}/sites.csv', sep=',', skiprows=1)

>>>>>>> 42387658be6daaed74e1ef1517108f43e5b57c16

dates = ['20191222', '20191223', '20191224', '20191225']

a = dict()

sites = ['Adelaide_Site_7', 'Birdsville', 'Fowlers_Gap', 'Lake_Argyle', 'Lake_Lefroy', 'Learmonth', 'Lucinda', 'Tumbarumba']
<<<<<<< HEAD
##aod
#for date in dates :
#  site_dict = dict()
#  for i, s in enumerate(sites) :
#    print(s)
#    AOD = aeronet.product(s, 2019, "AOD")
#    lon, lat = sites_table.get_site_coordinates(s)
#    site_dict[s] = (lon, lat, AOD.get_AOD(22,12, 550, 1.2) )
#  #a[date] = pd.DataFrame.from_dict(site_dict)
#  #a[date] = site_dict
#  b = pd.DataFrame(site_dict)
#  b.to_csv(date + '_aus_aod_aeronet.csv')


##total column
#for date in dates :
#  site_dict = dict()
#  for i, s in enumerate(sites) :
#    print(s)
#    SIZ = aeronet.product(s, 2019, "SIZ")
#    lon, lat = sites_table.get_site_coordinates(s)
#    site_dict[s] = (lon, lat, SIZ.get_total_column(22,12, (0,2)) )
#  #a[date] = pd.DataFrame.from_dict(site_dict)
#  #a[date] = site_dict
#  b = pd.DataFrame(site_dict)
#  b.to_csv(date + '_aus_totcol_aeronet.csv')

##angstrom column
#for date in dates :
#  site_dict = dict()
#  for i, s in enumerate(sites) :
#    print(s)
#    AOD = aeronet.product(s, 2019, "AOD")
#    lon, lat = sites_table.get_site_coordinates(s)
#    site_dict[s] = (lon, lat, AOD.calculate_AOD_angstrom(22,12 ))
#  #a[date] = pd.DataFrame.from_dict(site_dict)
#  #a[date] = site_dict
#  b = pd.DataFrame(site_dict)
#  b.to_csv(date + '_aus_angs_aeronet.csv')

#radius
=======
for date in dates :
  site_dict = dict()
  for i, s in enumerate(sites) :
    lon, lat = aeronet.get_site_coordinates(s)
    site_dict[s] = (lon, lat, aeronet.get_aod(22,12, s) )
  #a[date] = pd.DataFrame.from_dict(site_dict)
  #a[date] = site_dict
  b = pd.DataFrame(site_dict)
  b.to_csv(date + '_aus_aod_aeronet.csv')

#b.to_csv('farouk')
sites = ['Adelaide_Site_7', 'Birdsville', 'Fowlers_Gap', 'Lake_Argyle', 'Lake_Lefroy', 'Learmonth', 'Lucinda', 'Tumbarumba']
>>>>>>> 42387658be6daaed74e1ef1517108f43e5b57c16
for date in dates :
  site_dict = dict()
  for i, s in enumerate(sites) :
    print(s)
<<<<<<< HEAD
    VOL = aeronet.product(s, 2019, "VOL")
    lon, lat = sites_table.get_site_coordinates(s)
    site_dict[s] = (lon, lat, VOL.get_VOL_radius(22,12 ))
  #a[date] = pd.DataFrame.from_dict(site_dict)
  #a[date] = site_dict
  b = pd.DataFrame(site_dict)
  b.to_csv(date + '_aus_radius_aeronet.csv')
=======
    AOD = aeronet.product(s, 2019, "AOD")
    lon, lat = sites_table.get_site_coordinates(s)
    site_dict[s] = (lon, lat, AOD.get_AOD(22,12, 550, 1.2) )
  #a[date] = pd.DataFrame.from_dict(site_dict)
  #a[date] = site_dict
  b = pd.DataFrame(site_dict)
  b.to_csv(date + '_aus_totcol_aeronet.csv')
>>>>>>> 42387658be6daaed74e1ef1517108f43e5b57c16
