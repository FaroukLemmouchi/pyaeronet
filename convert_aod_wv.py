

def convert_aod_wv(aod1, wv1, wv2, alpha) :
  """Converts AOD using angstrom exponent :
    Args : floats
      aod1(wv1), wv1, wv2, alpha

    return: float    aod2(wv2)"""
  if __verbose__ > 1 :  print(f'\nConverted AOD from {wv1} nm to {wv2} nm using angstrom exp = {alpha}')
  return  aod1 * ( wv2/wv1 )**(-alpha)

