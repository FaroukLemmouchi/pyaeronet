#!/bin/python3

import os
__db_path__ = os.getenv('aeronet_db_path')
__verbose__ = 1

from glob import glob as _glob
if _glob(__db_path__) == [] :
  print(f"WARNING: __db_path__:{__db_path__} \n doesn't exist! Please set another path")


class site :
  def __init__(self, db_path=None) :
    import os
    from glob import glob
    import pandas as pd
    #__db_path__ = os.path.dirname(__file__)
    if glob(__db_path__+'/sites.csv') == [] :
      os.system(f'wget https://aeronet.gsfc.nasa.gov/aeronet_locations_v3.txt -O {__db_path__}/sites.csv')
    self.data = pd.read_csv(__db_path__ + '/sites.csv', skiprows=1, delimiter=',')

  def get_site_coordinates(self, site) :
    "Returrn coordinates of the site as tupple"
    a = self.data[self.data['Site_Name'] == site]
    return a.iloc[0,1], a.iloc[0,2]

  def get_site_name(self, pixlon, pixlat, nearby):
    """Returns the site name if located {nearby} degree from {lon}, {lat}"""
    a=(self.data['Longitude(decimal_degrees)'] - float(pixlon))**2 < nearby
    b=(self.data['Latitude(decimal_degrees)'] - float(pixlat))**2 < nearby
    c= a & b

    res = self.data[c]
    if __verbose__ : print(res)
    if len(res) == 0 :
      print('no site {nearby} degree nearby')
      return 

    site = res.iloc[0,0]
    if __verbose__ > 0 : print(f'Site (+-) {nearby} deg : {site}')
    return site
  
class product :    
  def __init__(self, site, year, product):
    """Get AERONET product : site, year, product
    from AERONET download tool

      [product_type] Value  Explanation**
      SIZ Size distribution
      RIN Refractive indicies (real and imaginary)
      CAD Coincident AOT data with almucantar retrieval
      VOL Volume concentration, volume mean radius, effective radius and standard deviation
      TAB AOT absorption
      AOD AOT extinction
      SSA Single scattering albedo
      ASY Asymmetry factor
      FRC Radiative Forcing
      LID Lidar and Depolarization Ratios
      FLX Spectral flux
      ALL All of the above retrievals (SIZ to FLUX) in one file
      PFN*  Phase function (available for only all points data format: AVG=10)
      U27 Estimation of Sensitivity to 27 Input Uncertainty Variations (available for only all points data format: AVG=10 and ALM20 and HYB20)


      [inv_type] Value  Explanation
      ALM15 Level 1.5 Almucantar Retrievals
      ALM20 Level 2.0 Almucantar Retrievals
      HYB15 Level 1.5 Hybrid Retrievals
      HYB20 Level 2.0 Hybrid Retrievals
    """
    import os 
    from glob import glob
    import pandas as pd
    year = str(year)

    self.product = product
    product_filename = f'{__db_path__}/{site}_{year}_{product}'
    self.__product_filename__ = product_filename 
    server = 'https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_inv_v3' 
    self.__server__ = server
    self.__year__ = year

    if glob(product_filename) == [] :    
      AVG='20' # 20 => @12:00:00
      ALM15='1' # Almucantar
      if_no_html='1'
      #optional hour = 13; hour2=14
      dwcmd = f'wget -O {product_filename}'
      query = f"{server}?site={site}\&year={year}\&month=1\&day=1\&year2={int(year)+1}\&month2=12\&day2=31\&product={product}\&AVG={AVG}\&ALM15={ALM15}\&if_no_html={if_no_html}"
      #query = f"{server}?site={site}\&year={year}\&month=1\&day=1\&year2={int(year)+1}\&month2=12\&day2=31\&hour={hour}\&hour2={hour2}\&product={product}\&AVG={AVG}\&ALM15={ALM15}\&if_no_html={if_no_html}"
      if __verbose__ > 0 :
        print(query)
      os.system(f'{dwcmd} {query}')
    try :
      self.data = pd.read_csv(product_filename, skiprows=6, delimiter=',')
    except :
      raise Exception("Reading file error")

  def _check_day_availability(self, day, month):
    try :
      a = (self.data['Date(dd:mm:yyyy)'] == f'{day}:{month}:{self.__year__}')
      if not a.any() :
        if __verbose__ : print(f'{self.__product_filename__} day not recorded') #, using default')
        return None
    except:
      if __verbose__ : print( f"{self.__product_filename__} is empty") #, use default configuration")
      return None
    return a

  def get_VOL_radius(self, day, month) :
    """Return microphysics of aerosol data :
       mean_hat, sds_hat, weights
       2 predominent modes only
    """
    if self.product != "VOL" : raise Exception(f"{self.product} does not have this property")
    import numpy as np

    day = str(day) ; month = str(month)

    a = self._check_day_availability(day, month)
    if a is None : return None, None

    ReffF_V = self.data["REff-F"][a]
    StdF = self.data["Std-F"][a]
    ReffF_N = ReffF_V / np.exp(-3 * StdF**2)

    return np.float(ReffF_N), np.float(np.exp(StdF))

  def calculate_SIZ_modes(self, day, month, components) :
    """Return microphysics of aerosol data :
       mean_hat, sds_hat, weights
       2 predominent modes only
    """ 
    if self.product != "SIZ" : raise Exception(f"{self.product} does not have this property")
    from sklearn.mixture import GaussianMixture
    import numpy as np
    
    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return None, None, None
  

    N = np.array(self.data[a])[0,5:27]
    R = np.asarray(self.data.keys()[5:27], dtype=float)

    samples = []
    for i in range(N.size):
      for _ in range(int(N[i]*10**6)): 
        samples.append(R[i])

    mixture = GaussianMixture(n_components=components).fit(np.asarray(samples).reshape(-1, 1))
    means_hat = list(mixture.means_.flatten())
    sds_hat = list(np.sqrt(mixture.covariances_).flatten())
    weights_hat = list(mixture.weights_.flatten())

    if components == 2 : 
      if weights_hat[0] < weights_hat[1] : #dominant mode first
        means_hat.reverse()
        sds_hat.reverse()
        weights_hat.reverse()

    return  means_hat, sds_hat, weights_hat

  def get_total_column(self, day, month, bin_lim) :
    """bin_lim as tupple in micrometer
       Return : Total colum of AERONEt in particle/cm^2"""
    if self.product != "SIZ" : raise Exception(f"{self.product} does not have this property")
    import numpy as np
    
    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return
    
    dvdlnr = np.array(np.array(self.data[a]))[0,5:27]
    r = np.asarray(self.data.keys()[5:27], dtype=float)
  
    mask = (np.array(r) < bin_lim[0]) | (np.array(r) > bin_lim[1])
  
    r = r[~mask]
    dvdlnr = dvdlnr[~mask]
  
    dn = 0
    for i in range(r.size-1) : #integrale (4/3 pi r^3)^-1 dv/dlnr * 1e8 [particule/cm^3]
      dn = dn + (dvdlnr[i]/r[i]**3 + dvdlnr[i+1]/r[i+1]**3) * np.log(r[i+1]/r[i])  
    return 0.5 * dn / (4/3 * np.pi) * 1e8 

  def get_RIN(self, day, month) :
    """Return refractive index of aerosol data """ 
    if self.product != "RIN" : raise Exception(f"{self.product} does not have this property")
    import numpy as np
    
    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return None, None, None
      
    lambdas = np.array([440, 675, 870])
    real = np.array(self.data[a])[0,5:8]
    imag = np.array(self.data[a])[0,9:12]
    return lambdas, real, imag
  
  def get_AOD_angstrom_440_870(self, day, month): 
    """
    """ 
    if self.product != "AOD" : raise Exception(f"{self.product} does not have this property")
    import numpy as np
    
    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return None

    return float(self.data['Extinction_Angstrom_Exponent_440-870nm-Total'][a.flatten()])
    

  def calculate_AOD_angstrom(self, day, month, alpha=1.2, wv1=None, wv2=None): 
    """Return : AOD value at any particular wavelength using alpha as Angstrom coefficient
       WARNING: wavelengths hardly coded 440 & 675 nm
    """ 
    if self.product != "AOD" : raise Exception(f"{self.product} does not have this property")
    import numpy as np
    
    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return None

    if wv1 or wv2 : 
      raise Exception("Wavelengths : Not implemented")

    try :
      AOD440, AOD675 = ( self.data['AOD_Extinction-Total[440nm]'][a.flatten()], self.data['AOD_Extinction-Total[675nm]'][a.flatten()] )
      alpha = - np.log(AOD440/AOD675)/np.log(440/675)
    except :
      AOD443, AOD667 = ( self.data['AOD_Extinction-Total[443nm]'][a.flatten()], self.data['AOD_Extinction-Total[667nm]'][a.flatten()] )
      alpha = - np.log(AOD443/AOD667)/np.log(443/667)
    return  float(alpha)

  def get_AOD(self, day, month, wv) :
    """Reads AERONET AOD file
       Return : AOD value at any wv nm wavelength
    """ 
    from pyaeronet.utils import convert_aod_wv
    import numpy as np

    day = str(day) ; month = str(month)
    a = self._check_day_availability(day, month)
    if a is None : return None

    alpha = self.data['Extinction_Angstrom_Exponent_440-870nm-Total'][a]
    try :
      AOD440 = self.data['AOD_Extinction-Total[440nm]'][a]
      AODwv = convert_aod_wv(AOD440, 440, wv, alpha)
    except :
      AOD443 = self.data['AOD_Extinction-Total[443nm]'][a]
      AODwv = convert_aod_wv(AOD443, 443, wv, alpha)
  
    return np.float(AODwv)  #aod at requested lambda

