import numpy as np
import pandas as pd 

from scipy import stats

from svolfit.timeseries_utils.gnuplot_utils import gnuplot_paramdistplots,gnuplot_plotvpaths
from svolfit.timeseries_utils.latex_utils import latex_documentwrite

def tsparamstats(NAME,assetfilename,assetname,obswindow_start,obswindow_finish):

    success = False

# files produced by the fits are: Name_File_xxx.csv
    RawFileName=NAME+'_raw.csv'
    RawPars = pd.read_csv(RawFileName,index_col=0)

# names as in the raw dataframe, the inits have 'init_' prepended:
    pars_rep=[]
    pars_wrk=[]
    pars_misc=[]
    for x in RawPars.columns:
        if( (x[0:4]=='wrk_')&(x[0:9]!='wrk_grad_') ):
            pars_wrk.append(x)
        if( (x[0:4]=='rep_') ):
            pars_rep.append(x)
        if( (x[0:5]=='misc_') ):
            pars_rep.append(x)
    pars=[]
    for x in pars_rep:
        pars.append(x)
    for x in pars_wrk:
        pars.append(x)
    for x in pars_misc:
        pars.append(x)
        
#assume only one run is in a file, all starting from the beginning
    Names=RawPars.RunInfo_Name.unique()
    Files=RawPars.RunInfo_FILE.unique()
    if( (len(Names)>1)|(len(Files)>1) ):
       print('this doesnot work with multiple runs in a file')
       return success
#    Offset=RawPars.offset.unique()[0]    
#    STARTS=RawPars.start.unique()
    
    STARTS=RawPars.RunInfo_start.unique()
    STARTS.sort()

    FINISHES=RawPars.RunInfo_finish.unique()
    FINISHES.sort()

    SERIES=RawPars.RunInfo_SeriesName.unique()
    Nseries=len(SERIES)
    SERIES=[assetname]    
    NOBSS=RawPars.RunInfo_Nobs.unique()
    NOBSS=np.sort(NOBSS)
    
    asset_series = pd.read_csv(assetfilename,index_col=0)
    if( (obswindow_finish < obswindow_start) | (obswindow_finish>asset_series.index.max()) ):
        obswindow_finish=asset_series.index.max()+1
    asset_series=asset_series[obswindow_start:obswindow_finish]


    varestFileName=NAME+'_raw_vpaths.csv'
    varest_paths= pd.read_csv(varestFileName,index_col=0)
        

#---------------------------    
# table with messages
    TMP=RawPars[['status','message']].copy()
    TMP=pd.DataFrame(TMP.value_counts())
    TMP.rename(columns={0:'total'},inplace=True)
    for cc in NOBSS:
        T2=pd.DataFrame(RawPars[RawPars['RunInfo_Nobs']==cc][['status','message']].value_counts())
        T2.rename(columns={0:cc},inplace=True)
        TMP=TMP.join(T2,how='left',on=['status','message'])
    TMP.fillna(value=0,inplace=True)
    TMP.to_csv(NAME+'_messages.csv', float_format="%.0f")
            
            
            
#---------------------------    
# plot by start            
            
    ParamGrid=pd.DataFrame(index=STARTS)
    ParamGrid.index.name='start'
    for x in pars:
        for Nobs in NOBSS:
            TMP=RawPars[['RunInfo_start',x]][(RawPars.RunInfo_SeriesName==assetname)&(RawPars.RunInfo_Nobs==Nobs)]
            TMP.rename(columns={'RunInfo_start': 'start'},inplace=True)
            TMP.set_index('start',inplace=True)
            TMP.rename(columns={x: x+'_'+str(Nobs)},inplace=True)
            ParamGrid=ParamGrid.join(TMP,how='left')
    paramstartfilename=NAME+'_paramgrid_start.csv'
    ParamGrid.to_csv(paramstartfilename)

    ParamGrid=pd.DataFrame(index=FINISHES)
    ParamGrid.index.name='finish'
    for x in pars:
        for Nobs in NOBSS:
            TMP=RawPars[['RunInfo_finish',x]][(RawPars.RunInfo_SeriesName==assetname)&(RawPars.RunInfo_Nobs==Nobs)]
            TMP.rename(columns={'RunInfo_finish': 'finish'},inplace=True)
            TMP.set_index('finish',inplace=True)
            TMP.rename(columns={x: x+'_'+str(Nobs)},inplace=True)
            ParamGrid=ParamGrid.join(TMP,how='left')
    paramfinishfilename=NAME+'_paramgrid_finish.csv'
    ParamGrid.to_csv(paramfinishfilename)


#---------------------------    
# vpaths    
    TS=VPaths(obswindow_start,SERIES,NOBSS,STARTS,RawPars,asset_series,varest_paths,[],[])
    vpathfilename=NAME+'_vpaths.csv'
    headers=[str(x).replace('_','-') for x in TS.columns]
    TS.columns=headers
    TS.to_csv(vpathfilename)

#---------------------------    
# gnuplot+latex output:

    NOSTS = RawPars[['RunInfo_Nobs','RunInfo_start']].copy()

    gnuplotfilename=NAME+'_params.plt'
    gnuplot_paramdistplots(NAME,NOSTS,pars,paramstartfilename,paramfinishfilename,gnuplotfilename,obswindow_start,obswindow_finish)
    
    gnuplotfilename=NAME+'_plotvpaths.plt'
    gnuplot_plotvpaths(NAME,NOSTS,assetname,vpathfilename,gnuplotfilename,obswindow_start,obswindow_finish)
    
    
    latexfilename=NAME+'.tex'
    latex_documentwrite(NAME,NOSTS,pars,latexfilename)

#---------------------------    

#    UGridFileName=Name+'_'+FILE+'_raw_ugrid.csv'
#    UGRIDS = pd.read_csv(UGridFileName,index_col=0)

#    PVGridFileName=Name+'_'+FILE+'_raw_pvgrid.csv'
#    PVGRIDS = pd.read_csv(PVGridFileName,index_col=0)

#    UD = AsymptDist(SERIES,NOBSS,STARTS,RawPars,UGRIDS,PVGRIDS)
#    UD.to_csv(Name+'_'+File+'_udist.csv')

    success = True    
    return success



def VPaths(Offset,SERIES,NOBSS,STARTS,RawPars,TimeSeries,VPATHS,VSERIES,VarianceSeries):

    if( 'date' in TimeSeries ):
        TS = pd.DataFrame( TimeSeries.date.copy() )
    else:
        TS = pd.DataFrame( index=TimeSeries.index.copy() )
    for ca in range(0,len(SERIES)):
        asset=SERIES[ca]
        TMP=pd.DataFrame(TimeSeries[asset])
        TMP[asset+'_logret'] = np.log( TMP[asset].shift(-1) / TMP[asset] ) 
        TS=TS.join(TMP,how='left')
        
        if(len(VarianceSeries)>0):
            TMP=pd.DataFrame(VarianceSeries[VSERIES[ca]])
            TS=TS.join(TMP,how='left')
        
        for Nobs in NOBSS:
            for start in STARTS:
                iii=RawPars.index[(RawPars.RunInfo_Nobs==Nobs)&(RawPars.RunInfo_start==start)&(RawPars.RunInfo_SeriesName==asset)]
#                print(iii,len(iii))
                if( len(iii)>0 ):
                    VPATH=pd.DataFrame(VPATHS[str(iii[0])])
                    VPATH.rename(columns={str(iii[0]):asset+'_'+str(Nobs)+'_'+str(start-Offset)},inplace=True)
                    VPATH.dropna(inplace=True)
                    VPATH.reset_index(inplace=True)
                    VPATH['index']=VPATH.index+start
                    VPATH.set_index(['index'],inplace=True)
                    if( len(VPATH)>0 ):
                        TS=TS.join(VPATH,how='left')
                    
    return TS

def AsymptDist(SERIES,NOBSS,STARTS,RawPars,UGRIDS,PVGRIDS):
   
    UD = pd.DataFrame()
    for asset in SERIES:
        for Nobs in NOBSS:
            for start in STARTS:
                iii=RawPars.index[(RawPars.Nobs==Nobs)&(RawPars.start==start)&(RawPars.SeriesName==asset)]
                if( len(iii) > 0 ):
                    UGRID=pd.DataFrame(UGRIDS[str(iii[0])])
                    PVGRID=pd.DataFrame(PVGRIDS[str(iii[0])])
                    if( len(UGRID)>0 ):
                        UGRID.rename(columns={str(iii[0]):asset+'_'+str(Nobs)+'_'+str(start)+'_u'},inplace=True)
                        UGRID.dropna(inplace=True)
                        UGRID.reset_index(drop=True,inplace=True)
                        UD=UD.join(UGRID,how='outer')
                        
                        PVGRID.rename(columns={str(iii[0]):asset+'_'+str(Nobs)+'_'+str(start)+'_pv'},inplace=True)
                        PVGRID.dropna(inplace=True)
                        PVGRID.reset_index(drop=True,inplace=True)
                        UD=UD.join(PVGRID,how='outer')

    
    return UD

