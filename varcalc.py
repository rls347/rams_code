import numpy as np
from utils.iocode import getvar
from RAMS_Post_Process.fx_postproc_RAMS import read_head

cp = 1004.
cpor = 1004./287
rd = 287.
p00 = 1000.

def get_dims(f):
    datafile = f
    headfile = f[:-5]+'head.txt'
    zm, zt, nx, ny, dxy, npa = read_head(headfile,datafile)
    height = zt/1000.
    x = np.arange(nx)*dxy/1000.
    y = np.arange(ny)*dxy/1000.
    return x,y,height

def sum_cond(f):
    ''' Returns condensate mixing ratio in g/kg '''
    q=(getvar(f,'RCP')+getvar(f,'RRP')+getvar(f,'RPP')+getvar(f,'RSP')+getvar(f,'RAP')+
        getvar(f,'RGP')+getvar(f,'RHP'))*1000.
    return q

def get_tempk(f,lev=None):
    ''' Returns temperature in Kelvin '''
    if lev=='sfc':
        var=getvar(f,'PI')[1,:,:]*getvar(f,'THETA')[1,:,:]/cp
    else:
        var=getvar(f,'PI')*getvar(f,'THETA')/cp
    return var

def getpress(f):
    ''' Returns pressure in mb/hpa'''
    return (getvar(f,'PI')/cp)**cpor*p00

def getrho(f):
    ''' Returns density'''
    return (getpress(f)*100.)/(rd*get_tempk(f))

def rainrate(f):
    ''' Returns surface rain rate in mm/hr '''
    rain = getvar(f,'PCPRR')*3600
    return rain

def intvapor(f):
    ''' Returns precipitable water in mm or kg/m2'''
    vapor = getvar(f,'RV')
    rho = getrho(f)
    headfile = f[:-5]+'head.txt'
    zm, zt, nx, ny, dxy, npa = read_head(headfile,f)
    var = vapor[1:,:,:]*rho[1:,:,:]*np.diff(zm)[:,None,None]
    pcpw = np.sum(var,0)
    return pcpw

def getcloudtop(fil):
    ''' returns a 2d variable with the indices of cloud top'''
    q=sum_cond(fil)*1000.
    c=np.where(q>.01)
    q[c]=100.
    inds = q.shape[0]-1-np.argmax(q[::-1,:,:],0)
    inds[np.max(q,0)<.01]=0

    return inds
