import numpy as np

from svolfit.gridanalysis import gridanalysis
from svolfit.timeseries_utils.tsparamstats import tsparamstats

def analysis_timeseries_multiple(NAME,FILENAMES,assetname,obswindow_start,obswindow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions ):

	for filename in FILENAMES:
		modifier=filename[0:len(filename)-4]
		analysis_timeseries(NAME+'_'+modifier,filename,assetname,obswindow_start,obswindow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions )
		
	return

def analysis_timeseries(NAME,filename,assetname,obswindow_start,obswindow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions ):

#TODO: only one asset series at a time now


    print('Fitting model')
    FILES=['SimPaths_'+NAME+'_'+model+'_'+method+'_'+assetname+'.csv']
    try:
        gridanalysis(NAME,[filename],[assetname],obswindow_start,obswindow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions )
    except:
        print('path fits failed')

    print('Calculating Statistics and Reporting.')
    try:
        tsparamstats(NAME+'_'+model+'_'+method,filename,assetname,obswindow_start,obswindow_finish)
    except:
        print('paramters stats calcs failed')
    return
