from pyaeronet import aeronet
import  numpy as np
import pandas as pd
import os

db_path = os.getenv('aeronet_db_path')

sites_table = aeronet.site()

dates = ['20191222', '20191223', '20191224', '20191225']

a = dict()
wv = 550

sites = ['Birdsville'] #, 'Fowlers_Gap', 'Lake_Argyle', 'Lake_Lefroy', 'Learmonth', 'Lucinda', 'Tumbarumba', 'Adelaide_Site_7']
#aod
for date in dates :
  print(date)
  site_dict = dict()
  for i, s in enumerate(sites) :
      print(s)
      AOD = aeronet.product(s, 2019, "AOD")
      lon, lat = sites_table.get_site_coordinates(s)
      site_dict[s] = (lon, lat, AOD.get_AOD(date[6:8], date[4:6], wv, 1.2) )
  #a[date] = pd.DataFrame.from_dict(site_dict)
  #a[date] = site_dict
  b = pd.DataFrame(site_dict)
  b.T.to_csv(date + '_aus_aod_aeronet0.csv', header=[ 'lon','lat', f'aod_{wv}'])


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

##radius
#for date in dates :
#  site_dict = dict()
#  for i, s in enumerate(sites) :
#    print(s)
#    VOL = aeronet.product(s, 2019, "VOL")
#    lon, lat = sites_table.get_site_coordinates(s)
#    site_dict[s] = (lon, lat, VOL.get_VOL_radius(22,12 ))
#  #a[date] = pd.DataFrame.from_dict(site_dict)
#  #a[date] = site_dict
#  b = pd.DataFrame(site_dict)
#  b.to_csv(date + '_aus_radius_aeronet.csv')
