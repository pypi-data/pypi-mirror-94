import numpy as np
import pandas as pd 

from scipy import stats

from svolfit.estimatestats.gnuplot_utils import gnuplot_convergeplots,gnuplot_paramdistplots,gnuplot_plotvpaths
from svolfit.estimatestats.latex_utils import latex_documentwrite

def simparamstats(NAME,assetname,variancename):

    success = False

# files produced by the fits are: Name_File_xxx.csv
    RawFileName=NAME+'_raw.csv'
    RawPars = pd.read_csv(RawFileName,index_col=0)

# names as in the raw dataframe, the inits have 'init_' prepended:
    pars_rep=[]
    pars_wrk=[]
    for x in RawPars.columns:
        if( (x[0:4]=='wrk_')&(x[0:9]!='wrk_grad_') ):
            pars_wrk.append(x)
        if( (x[0:4]=='rep_') ):
            pars_rep.append(x)
    pars=[]
    for x in pars_rep:
        pars.append(x)
    for x in pars_wrk:
        pars.append(x)
        
#assume only one run is in a file, all starting from the beginning
    Names=RawPars.RunInfo_Name.unique()
    Files=RawPars.RunInfo_FILE.unique()
    if( (len(Names)>1)|(len(Files)>1) ):
       print('this doesnot work with multiple runs in a file')
       return success
#    Offset=RawPars.offset.unique()[0]    
#    STARTS=RawPars.start.unique()
    offset = 0
    
    SERIES=RawPars.RunInfo_SeriesName.unique()
    Nseries=len(SERIES)
    SERIES=[assetname+'_'+str(cc) for cc in range(0,len(SERIES))]    
    VSERIES=[variancename+'_'+str(cc) for cc in range(0,len(SERIES))]
    NOBSS=RawPars.RunInfo_Nobs.unique()
    NOBSS=np.sort(NOBSS)
    
    asset_series = pd.read_csv('SimPaths_'+NAME+'_'+assetname+'.csv',index_col=0)
    asset_series=asset_series[offset:]
    variance_series = pd.read_csv('SimPaths_'+NAME+'_'+variancename+'.csv',index_col=0)
    variance_series=variance_series[offset:]

    varestFileName=NAME+'_raw_vpaths.csv'
    varest_paths= pd.read_csv(varestFileName,index_col=0)
        
    DC=[]
    STATL=[]
    Npaths=len(SERIES)
    for Nobs in NOBSS:

        vavg=np.zeros(Npaths)        
        vstd=np.zeros(Npaths)        
        vT=np.zeros(Npaths)        

        DD={}
        DD['Nobs']=Nobs
 
        for par in pars:
            parv=np.zeros(Npaths)        

            for ca in range(0,Npaths):
                asset=SERIES[ca]
                ptmp=RawPars[(RawPars.RunInfo_Nobs==Nobs)&(RawPars.RunInfo_SeriesName==asset)]
                parv[ca]=ptmp.iloc[0][par]

            expected=ptmp.iloc[0]['sim_'+par]
            DD[par+'_exp']=expected
            DD[par+'_mean']=parv.mean()
            DD[par+'_std']=parv.std()
            DD[par+'_5']=np.percentile(parv,5)
            DD[par+'_95']=np.percentile(parv,95)
            DD[par+'_bias']=(parv-expected).mean()
            DD[par+'_estd']=(parv-expected).std()
            DD[par+'_rmse']=np.sqrt((parv-expected).mean()*(parv-expected).mean()+(parv-expected).std()*(parv-expected).std())
                        
            for par2 in pars:
                parv2=np.zeros(Npaths)        
    
                for ca in range(0,Npaths):
                    asset2=SERIES[ca]
                    ptmp2=RawPars[(RawPars.RunInfo_Nobs==Nobs)&(RawPars.RunInfo_SeriesName==asset2)]
                    parv2[ca]=ptmp2.iloc[0][par2]
                
                corr=np.corrcoef(parv,parv2)
                cov=np.cov(parv,parv2)
                DCdict={}
                DCdict['Nobs']=Nobs
                DCdict['par1']=par
                DCdict['par2']=par2
                if(par==par2):
                    DCdict['rho']=1.0
                else:
                    if(np.isnan(corr[0,1]) ):
                        DCdict['rho']=0.0 #this happens when a parameter is fixed...
                    else:
                        DCdict['rho']=corr[0,1]
                DCdict['cov']=cov[0,1]
                DC.append(DCdict)

        for ca in range(0,Npaths):
            asset=SERIES[ca]
            vasset=VSERIES[ca]
                    
            VAR=pd.DataFrame(variance_series[vasset])

            iii=RawPars.index[(RawPars.RunInfo_Nobs==Nobs)&(RawPars.RunInfo_SeriesName==asset)]
#            print(iii,len(iii))
            if( len(iii)>0 ):
                VPATH=pd.DataFrame(varest_paths[str(iii[0])])
                VPATH.rename(columns={str(iii[0]):asset},inplace=True)
                VPATH.dropna(inplace=True)
                VPATH.reset_index(drop=True,inplace=True)

                VPATH=VPATH.join(VAR,how='left')
                diff=(VPATH[asset]-VPATH[vasset]).to_numpy()
                
                vavg[ca]=diff.mean()
                vstd[ca]=diff.std()
                vT[ca]=diff[-1]
        
        
        DD['vavg_exp']=0.0
        DD['vavg_mean']=vavg.mean()
        DD['vavg_std']=vavg.std()
        DD['vavg_5']=np.percentile(vavg,5)
        DD['vavg_95']=np.percentile(vavg,95)
        DD['vavg_bias']=vavg.mean()
        DD['vavg_estd']=vavg.std()
        DD['vavg_rmse']=np.sqrt(vavg.mean()*vavg.mean()+vavg.std()*vavg.std())

        DD['vstd_exp']=0.0
        DD['vstd_mean']=vstd.mean()
        DD['vstd_std']=vstd.std()
        DD['vstd_5']=np.percentile(vstd,5)
        DD['vstd_95']=np.percentile(vstd,95)
        DD['vstd_bias']=vstd.mean()
        DD['vstd_estd']=vstd.std()
        DD['vstd_rmse']=np.sqrt(vstd.mean()*vstd.mean()+vstd.std()*vstd.std())

        DD['vT_exp']=0.0
        DD['vT_mean']=vT.mean()
        DD['vT_std']=vT.std()
        DD['vT_5']=np.percentile(vT,5)
        DD['vT_95']=np.percentile(vT,95)
        DD['vT_bias']=vT.mean()
        DD['vT_estd']=vT.std()
        DD['vT_rmse']=np.sqrt(vT.mean()*vT.mean()+vT.std()*vT.std())
        
        STATL.append(DD)
    
    STATL=pd.DataFrame(STATL)
    header=[x.replace('_','-') for x in STATL.columns]
    STATL.columns=header
    statsfilename=NAME+'_stats.csv'
    STATL.to_csv(statsfilename)
    
   
    
#---------------------------    
# log-slopes of estd
    pars_ext=pars.copy()
    pars_ext.append('vavg')
    pars_ext.append('vstd')
    pars_ext.append('vT')
    res=[]
    lnobs=np.log(STATL.Nobs.to_numpy())    
    for x in pars_ext:
        xfix=x.replace('_','-')
        y=np.log(STATL[xfix+'-estd'].to_numpy())
        bias=STATL[xfix+'-bias'].to_numpy()
        estd=STATL[xfix+'-estd'].to_numpy()
        sim=STATL[xfix+'-exp'].to_numpy()
        
        (lg_m, lg_b, _, _, se_m) = stats.linregress(lnobs, y)
        TRT={}
        TRT['par']=xfix
        TRT['a']=-lg_m
        TRT['asigma']=se_m
        TRT['sim']=sim[0]

        if( 1260 in NOBSS ):
            TRT['bias5']=bias[NOBSS==1260][0]
            TRT['estd5']=estd[NOBSS==1260][0]
        TRT['C5']=np.exp(lg_b)*(1260**lg_m)

        if( 2520 in NOBSS ):
            TRT['bias10']=bias[NOBSS==2520][0]
            TRT['estd10']=estd[NOBSS==2520][0]
        TRT['C10']=np.exp(lg_b)*(2520**lg_m)

        res.append(TRT)
    res=pd.DataFrame(res)
    res.to_csv(NAME+'_convergence.csv',index=False, float_format="%.4f")

#---------------------------    
# correlation

# just output these if available
    ReportCorr=[1260,2520]
    ReportCorr = list(set(NOBSS).intersection(ReportCorr))
    ReportCorr.sort()
    if(len(ReportCorr)==0 ):
        ReportCorr.append(np.max(NOBSS))
    
    DC=pd.DataFrame(DC)
    for Nobs in ReportCorr:
        corr=np.zeros((len(pars),len(pars)))
        for c1 in range(0,len(pars)):
            for c2 in range(0,len(pars)):
                TMP=DC[(DC.Nobs==Nobs)&(DC.par1==pars[c1])&(DC.par2==pars[c2])]['rho']
                corr[c1,c2]=TMP.iloc[0]
        headers=[x.replace('_','-') for x in pars]
        corr=pd.DataFrame(corr,columns=headers)
        corr['par']=headers
        corr.set_index('par',drop=True,inplace=True)
        corr.to_csv(NAME+'_corr_'+str(Nobs)+'.csv', float_format="%.3f")

    DC=pd.DataFrame(DC)
    for Nobs in ReportCorr:
        corr=np.zeros((len(pars_rep),len(pars_rep)))
        for c1 in range(0,len(pars_rep)):
            for c2 in range(0,len(pars_rep)):
                TMP=DC[(DC.Nobs==Nobs)&(DC.par1==pars_rep[c1])&(DC.par2==pars_rep[c2])]['rho']
                corr[c1,c2]=TMP.iloc[0]
        (eigenvals,eigenvects)=np.linalg.eig(corr)
        headers=[x.replace('_','-') for x in pars_rep]
        corr=pd.DataFrame(corr,columns=headers)
        corr['par']=headers
        corr.set_index('par',drop=True,inplace=True)
        corr.to_csv(NAME+'_corr_rep_'+str(Nobs)+'.csv', float_format="%.3f")
        
        EG=pd.DataFrame(np.append([eigenvals],eigenvects,axis=0))
        EG.to_csv(NAME+'_corr_eigen_rep_'+str(Nobs)+'.csv', float_format="%.3f")


    DC=pd.DataFrame(DC)
    for Nobs in ReportCorr:
        corr=np.zeros((len(pars_wrk),len(pars_wrk)))
        for c1 in range(0,len(pars_wrk)):
            for c2 in range(0,len(pars_wrk)):
                TMP=DC[(DC.Nobs==Nobs)&(DC.par1==pars_wrk[c1])&(DC.par2==pars_wrk[c2])]['rho']
                corr[c1,c2]=TMP.iloc[0]
        (eigenvals,eigenvects)=np.linalg.eig(corr)
        headers=[x.replace('_','-') for x in pars_wrk]
        corr=pd.DataFrame(corr,columns=headers)
        corr['par']=headers
        corr.set_index('par',drop=True,inplace=True)
        corr.to_csv(NAME+'_corr_wrk_'+str(Nobs)+'.csv', float_format="%.3f")
        
        EG=pd.DataFrame(np.append([eigenvals],eigenvects,axis=0))
        EG.to_csv(NAME+'_corr_eigen_wrk_'+str(Nobs)+'.csv', float_format="%.3f")

# covariance            
    DC=pd.DataFrame(DC)
    for Nobs in ReportCorr:
        corr=np.zeros((len(pars_rep),len(pars_rep)))
        for c1 in range(0,len(pars_rep)):
            for c2 in range(0,len(pars_rep)):
                TMP=DC[(DC.Nobs==Nobs)&(DC.par1==pars_rep[c1])&(DC.par2==pars_rep[c2])]['cov']
                corr[c1,c2]=TMP.iloc[0]
        (eigenvals,eigenvects)=np.linalg.eig(corr)
        headers=[x.replace('_','-') for x in pars_rep]
        corr=pd.DataFrame(corr,columns=headers)
        corr['par']=headers
        corr.set_index('par',drop=True,inplace=True)
        corr.to_csv(NAME+'_cov_rep_'+str(Nobs)+'.csv', float_format="%.5f")
        
        EG=pd.DataFrame(np.append([eigenvals],eigenvects,axis=0))
        EG.to_csv(NAME+'_cov_eigen_rep_'+str(Nobs)+'.csv', float_format="%.3f")

    DC=pd.DataFrame(DC)
    for Nobs in ReportCorr:
        corr=np.zeros((len(pars_wrk),len(pars_wrk)))
        for c1 in range(0,len(pars_wrk)):
            for c2 in range(0,len(pars_wrk)):
                TMP=DC[(DC.Nobs==Nobs)&(DC.par1==pars_wrk[c1])&(DC.par2==pars_wrk[c2])]['cov']
                corr[c1,c2]=TMP.iloc[0]
        (eigenvals,eigenvects)=np.linalg.eig(corr)
        headers=[x.replace('_','-') for x in pars_wrk]
        corr=pd.DataFrame(corr,columns=headers)
        corr['par']=headers
        corr.set_index('par',drop=True,inplace=True)
        corr.to_csv(NAME+'_cov_wrk_'+str(Nobs)+'.csv', float_format="%.5f")
        
        EG=pd.DataFrame(np.append([eigenvals],eigenvects,axis=0))
        EG.to_csv(NAME+'_cov_eigen_wrk_'+str(Nobs)+'.csv', float_format="%.3f")

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
# vpaths    
    TS=VPaths(offset,SERIES,NOBSS,[0],RawPars,asset_series,varest_paths,VSERIES,variance_series)
    vpathfilename=NAME+'_vpaths.csv'
    headers=[str(x).replace('_','-') for x in TS.columns]
    TS.columns=headers
    TS.to_csv(vpathfilename)

#---------------------------    
# gnuplot+latex output:

    plotpaths=[0,1,2,3,4]
    gnuplotfilename=NAME+'_paramconverge.plt'
    gnuplot_convergeplots(NAME,NOBSS,pars_ext,statsfilename,gnuplotfilename)
    gnuplotfilename=NAME+'_paramdist.plt'
    gnuplot_paramdistplots(NAME,NOBSS,pars_ext,statsfilename,gnuplotfilename)
    
    gnuplotfilename=NAME+'_plotvpaths.plt'
    gnuplot_plotvpaths(NAME,plotpaths,NOBSS,vpathfilename,gnuplotfilename)
    
    
    latexfilename=NAME+'.tex'
    latex_documentwrite(NAME,plotpaths,NOBSS,ReportCorr,pars_ext,latexfilename)

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
                    VPATH.rename(columns={str(iii[0]):asset+'_'+str(Nobs)},inplace=True)
                    VPATH.dropna(inplace=True)
                    VPATH.reset_index(inplace=True)
                    VPATH['index']=VPATH.index+Offset+start
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

