import numpy as np

from svolfit.estimatestats.pathsim import pathsim
from svolfit.gridanalysis import gridanalysis
from svolfit.estimatestats.simparamstats import simparamstats

def estimationstats(NAME,Npaths,windows,NumProcesses, dt, model, method, modeloptions, statsonly=False ):

    Nsteps=np.max(windows)

    assetname = 'asset'
    variancename = 'variance'
    if( statsonly != True ):    
        print('Running path simulation')
        try:
            (success,assetname,variancename)=pathsim(NAME,Nsteps,Npaths,windows,dt, model, method, modeloptions )
        except:
            print('Path simulation failed')
        ow_start=0
        ow_finish = -1
        stride=-1
            
        print('Fitting model')
        FILES=['SimPaths_'+NAME+'_'+model+'_'+method+'_'+assetname+'.csv']
        SERIES=[assetname+'_'+str(cc) for cc in range(0,Npaths)]
        try:
            success = gridanalysis(NAME,FILES,SERIES,ow_start,ow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions )
        except:
            print('path fits failed')

    print('Calculating Statistics and Reporting.')
    try:
        simparamstats(NAME+'_'+model+'_'+method,assetname,variancename)
    except:
        print('paramters stats calcs failed')
    return
