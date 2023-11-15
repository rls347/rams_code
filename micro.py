import numpy as np
from scipy.special import gamma
from utils.iocode import getvar

def getdefault(var):
    ''' Returns default RAMS microphysics parameters for the selected hydrometeor '''
    cfmas = { 'pristine': 110.8,
              'cloud': 524.,
              'aggregates': 0.496,
              'snow': 0.002739,
              'drizzle': 524.,
              'hail': 471.,
              'rain': 524.,
              'graupel': 157.   }

    pwmas = { 'cloud': 3.,
              'drizzle': 3.,
              'rain': 3.,
              'pristine': 2.91,
              'snow': 1.74,
              'aggregates': 2.4,
              'graupel': 3.,
              'hail': 3.  }
  
    nu = {    'cloud': 4.,
              'drizzle': 4.,
              'rain': 2.,
              'pristine': 2.,
              'snow': 2.,
              'aggregates': 2.,
              'graupel':2.,
              'hail': 2.  }
    return cfmas[var],pwmas[var],nu[var]
	
def calcgammadist(m,n,coef,ex,nu):
    '''Returns diameters and number for size distribution'''
    dvals = np.linspace(1,10000,5000)*1e-6
    with np.errstate(invalid='ignore',divide='ignore'):
        d=(m/(n*coef))**(1./ex)
        
    dn = (gamma(nu)/gamma(nu+ex))**(1./ex)*d
    func = (1/gamma(nu))*((dvals/dn)**(nu-1))*(1/dn)*np.exp(-1*dvals/dn)
    return dvals, func
	
def gammadist_diam(d,ex,nu):
    '''Returns diameters and number for size distribution given mean mass diameter'''

    dvals = np.linspace(1,10000,5000)*1e-6
    dn = (gamma(nu)/gamma(nu+ex))**(1./ex)*d

    func = (1/gamma(nu))*((dvals/dn)**ex)*(1/dn)*np.exp(-1*dvals/dn)
    
    return dvals, func
	
def calcd_revu(fil,var):
    nnames = {  'pristine':'pris_concen_kg',
                'cloud':'cloud_concen_mg',
                'aggregates':'agg_concen_kg',
                'snow':'snow_concen_kg',
                'drizzle':'drizzle_concen_mg',
                'hail':'hail_concen_kg',
                'rain':'rain_concen_kg',
                'graupel':'graup_concen_kg'
            }

    mass = getvar(fil,var)/1000.
    num = getvar(fil,nnames[var])
    if var == 'cloud' or var == 'drizzle':
        num=num*1000.*1000.
    
    coef, ex, nu = getdefault(var)

    
    with np.errstate(invalid='ignore',divide='ignore'):
        d=(mass/(num*coef))**(1./ex)
        d[num==0]=0.0
    
    return d
    
	
def calcd(fil,var):
    mnames = {  'pristine':'RPP',
                'cloud':'RCP',
                'aggregates':'RAP',
                'snow':'RSP',
                'drizzle':'RDP',
                'hail':'RHP',
                'rain':'RRP',
                'graupel':'RGP'
            }

    nnames = {  'pristine':'CPP',
                'cloud':'CCP',
                'aggregates':'CAP',
                'snow':'CSP',
                'drizzle':'CDP',
                'hail':'CHP',
                'rain':'CRP',
                'graupel':'CGP'
            }

    mass = getvar(fil,mnames[var])
    num = getvar(fil,nnames[var])

    coef, ex, nu = getdefault(var)

    
    with np.errstate(invalid='ignore',divide='ignore'):
        d=(mass/(num*coef))**(1./ex)
        d[num==0]=0.0
    
    return d
    


