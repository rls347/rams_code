import numpy as np
from utils.iocode import getvar
from RAMS_Post_Process.fx_postproc_RAMS import read_head

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

def get_tempk(f):
    ''' Returns temperature in Kelvin '''
    var=getvar(f,'PI')*getvar(f,'THETA')/1004.
    return var

def rainrate(f):
    ''' Returns surface rain rate in mm/hr '''
    rain = getvar(f,'PCPRR')*3600
    return rain
