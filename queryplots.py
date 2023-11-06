import glob,os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rams_code.varcalc import *
import moviepy.editor as moviepy

def animateoverhead(i,var3d,xs,ys,levels,cbarlabel):
    timeslice = var3d[i,:,:]
    plt.clf()
    frame = plt.contourf(xs,ys,timeslice,levels = levels)
    cbar = plt.colorbar(frame,label = cbarlabel)
    title='Time ' + str(i)
    plt.title(title)
    return frame

def animateslice(i,var3d,xs,height,levels,cbarlabel):
    timeslice = var3d[i,:,:]
    plt.clf()
    frame = plt.contourf(xs,height,timeslice,levels = levels)
    plt.ylim(0,18)
    cbar = plt.colorbar(frame,label = cbarlabel)
    title='Time ' + str(i)
    plt.title(title)
    return frame


def makemovie(anim,filename):
    writergif = animation.PillowWriter(fps=3)
    anim.save(filename+'.gif', writer=writergif)
    clip = moviepy.VideoFileClip(filename+'.gif')
    clip.write_videofile(filename+".mp4")
    os.system('rm '+filename+'.gif')
    return

def sanityprint(modeldir):
    vars = ['THETA','PI','RV','RCP','RRP','WP','UP','VP','PCPRR']
    print(' ')
    print(modeldir)
    files = sorted(glob.glob(modeldir+'/*h5'))
    files=[files[-1]]
    for a,fil in enumerate(files):
        print(a)
        for v in vars:
            var = getvar(fil,v)
            print(v,var.min(),var.max())
        var=getvar(fil,'PI')*getvar(fil,'THETA')/1004.
        print('tempk',var.min(),var.max())
        print('sfc tmp',np.min(var[1,:,:]),np.max(var[1,:,:]))
    return


def precipmovie(modeldir,name):
    files = sorted(glob.glob(modeldir+'/*h5'))
    xs,ys,height = get_dims(files[0])
    pcp = []
    for a,fil in enumerate(files):
        rain = rainrate(fil)
        if np.max(rain)>np.min(rain):
            pcp.append(rain)
    pcp = np.array(pcp)

    if len(pcp)>0:
        fig = plt.figure()
        levels=np.linspace(0.1,np.max(rain),20)
        fargs = [pcp,xs,ys,levels,"Precip Rate (mm/hr)"]
        anim = animation.FuncAnimation(fig, animateoverhead, frames=pcp.shape[0],fargs=fargs)
        makemovie(anim,name+'preciprate') 
    else:
        print(name, ' has little or no precip')

    return


def maxslicemovie(modeldir,name,var='cond'):
    files = sorted(glob.glob(modeldir+'/*h5'))
    print(len(files))
    xs,ys,height = get_dims(files[0])
    var3d = []
    for f in files:
        if var == 'cond':
            q=sum_cond(f)
        elif var == 'w':
            q = getvar(f,'WC')
        else:
            q = getvar(f,var)
        if np.max(q)>np.min(q):
            var3d.append(np.max(q,1))
    var3d = np.array(var3d)

    if len(var3d)>0:
        levels=np.linspace(0.01,np.max(var3d),50)
        fig = plt.figure()
        fargs = [var3d,xs,height,levels,'Max slice '+var]
        anim = animation.FuncAnimation(fig,animateslice, frames = var3d.shape[0], fargs=fargs) 
        makemovie(anim, name+'slice'+var)
    else:
        print(name, 'has no variation in ',varname)
    return


def sfctempmovie(modeldir,name):
    files = sorted(glob.glob(modeldir+'/*h5'))
    xs,ys,height = get_dims(files[0])
    temp3d = []
    for a,fil in enumerate(files):
        sfctemp = get_tempk(fil)[1,:,:] #first point above ground
        if np.max(sfctemp)>np.min(sfctemp):
            temp3d.append(sfctemp)
    temp3d= np.asarray(temp3d)

    if len(temp3d)>0:
        levels = np.linspace(np.min(temp3d),np.max(temp3d),20)
        fig = plt.figure()
        fargs = [temp3d,xs,ys,levels,'Surface Temp (K)']
        anim = animation.FuncAnimation(fig, animateoverhead, frames=temp3d.shape[0],fargs=fargs)
        makemovie(anim,name+'sfctemp')
    else:
        print(name, ' has no variation in surface temp')

    return

def maxoverheadmovie(modeldir,name,var='w'):
    files = sorted(glob.glob(modeldir+'/*h5'))
    xs,ys,height = get_dims(files[0])
    var3d= []
    for a,fil in enumerate(files):
        if var == 'w':
            maxvar = np.max(getvar(fil,'WC'),0)
            if maxvar.max()>maxvar.min():
                var3d.append(maxvar)
    var3d= np.asarray(var3d)

    if len(var3d)>0:
        levels = np.linspace(np.min(var3d),np.max(var3d),20)
        fig = plt.figure()
        fargs = [var3d,xs,ys,levels,'Max '+var]
        anim = animation.FuncAnimation(fig, animateoverhead, frames=var3d.shape[0],fargs=fargs)
        makemovie(anim,name+'maxwoverhead')
    else:
        print(name, ' has no variation in ',var)

    return



