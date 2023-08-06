import numpy as np
import pandas as pd 
import multiprocessing as mp

from svolfit import svolfit
from svolfit.models.model_factory import model_create

def gridanalysis_correlation(NAME,FILES1,SERIES1,PARAMS1,FILES2,SERIES2,PARAMS2,ow_start,ow_finish,windows,stride,NumProc,dt, model='Heston_GBM', method = 'grid'):
    
    if(NumProc > 1 ):
        if( NumProc>mp.cpu_count() ):
            NumProc=mp.cpu_count()-1
        pool=mp.Pool(processes=NumProc)
    
    windowsizes=np.sort(windows)[::-1]
    
    sols=[]
    solsm=[]
    for cf in range(0,np.minimum(len(FILES1),len(FILES2),dtype=int)):
        FILE1=FILES1[cf]
        FILE2=FILES2[cf]
        print(FILE1,FILE2)

        PARAMSFILE1=PARAMS1[cf]
        PARAMSFILE2=PARAMS2[cf]
        PARAM1 = pd.read_csv(PARAMSFILE1,index_col=0)
        PARAM2 = pd.read_csv(PARAMSFILE2,index_col=0)

        TS1 = pd.read_csv(FILE1,index_col=0)
        TS2 = pd.read_csv(FILE2,index_col=0)

        if( ow_start < 0 ):
            ow_start=0
        if( (ow_finish <= ow_start)|(ow_finish > np.minimum( len(TS1), len(TS2), dtype=int ) ) ):
            ow_finish = np.minimum( len(TS1), len(TS2), dtype=int )
        
        for cw in range(0,len(windowsizes)):
            print(str(cw))
    
            NObs=ow_finish-ow_start+1
            Ninit=1
            if(stride>0):
                Ninit=int((NObs-windowsizes[cw]-1)/stride+1)

            for cc in range(0,Ninit):
                print(str(cc)+' of '+str(Ninit))
                start=ow_start+cc*stride
                finish=ow_start+cc*stride+(windowsizes[cw]+1)
                TS1_window=TS1[start:finish].copy()
                TS2_window=TS2[start:finish].copy()

                for cseries in range(0,np.minimum( len(SERIES1), len(SERIES2) ,dtype=int ) ):        
                    series1=np.array(TS1_window[SERIES1[cseries]].copy())
                    series2=np.array(TS2_window[SERIES2[cseries]].copy())

                    TMP=PARAM1[ (PARAM1.RunInfo_FILE==FILE1)&(PARAM1.RunInfo_SeriesName==SERIES1[cseries])&(PARAM1.RunInfo_start==start) & (PARAM1.RunInfo_finish==finish) ]  
                    if( len(TMP) > 1 ):
                        print('too many parameters...')
                    m1pars={}
                    if( 'model' in TMP ):
                        m1pars['model']=TMP.iloc[0]['model']
                    if( 'method' in TMP ):
                        m1pars['method']=TMP.iloc[0]['method']
                    for x in TMP.columns:
                        if( (x[0:4]=='sol_')&(x[0:9]!='sol_grad_') ):
                            m1pars['init_'+x[4:len(x)]]=TMP.iloc[0][x]
#                            print(x,x[4:len(x)])
#                    model1=model_create(series1, dt, m1pars['model'], m1pars['method'],m1pars)

                    TMP=PARAM2[ (PARAM2.RunInfo_FILE==FILE2)&(PARAM2.RunInfo_SeriesName==SERIES2[cseries])&(PARAM2.RunInfo_start==start) & (PARAM2.RunInfo_finish==finish) ]  
                    if( len(TMP) > 1 ):
                        print('too many parameters...')
                    m2pars={}
                    if( 'model' in TMP ):
                        m2pars['model']=TMP.iloc[0]['model']
                    if( 'method' in TMP ):
                        m2pars['method']=TMP.iloc[0]['method']
                    for x in TMP.columns:
                        if( (x[0:4]=='sol_')&(x[0:9]!='sol_grad_') ):
                            m2pars['init_'+x[4:len(x)]]=TMP.iloc[0][x]
#                            print(x,x[4:len(x)])
#                    model2=model_create(series2, dt, m2pars['model'], m2pars['method'],m2pars)
        
                    RunPars={}
                    RunPars['Name']=NAME
                    RunPars['FILE1']=FILE1
                    RunPars['FILE2']=FILE2
                    RunPars['SeriesName1']=SERIES1[cseries]
                    RunPars['SeriesName2']=SERIES2[cseries]
                    RunPars['ow_start']=ow_start
                    RunPars['ow_finish']=ow_finish
                    RunPars['start']=start
                    RunPars['finish']=finish
                    RunPars['offset']=start-ow_start
                    RunPars['stride']=stride
                    RunPars['Nobs']=windowsizes[cw]
       
                    if(NumProc > 1 ):
                        pool.apply_async(svolfit,args=(series.copy(), dt, model, method, RunPars.copy()),callback=lambda x: solsm.append(x) )
                    else:
                        (rpdict,sol)=svolfit( series, dt, model, method, RunPars.copy() )
                        ssl={}
                        ssl.update(rpdict)
                        ssl.update(sol)
                        sols.append(ssl)
    
    
    if(NumProc > 1 ):
        pool.close()
        pool.join()
        for x in solsm:
            ssl={}
            ssl.update(x[0])
            ssl.update(x[1])
            sols.append(ssl)
    
    sols=pd.DataFrame(sols)
    if( len(sols)==0 ):
        print('no results')
        return
    sols.sort_values(['RunInfo_FILE','RunInfo_SeriesName','RunInfo_Nobs','RunInfo_offset'],ignore_index=True,inplace=True)
    
    upaths = pd.DataFrame(sols.upath.tolist(),index=sols.index)
    upaths.columns=['upath_'+str(x) for x in upaths.columns]
    vpaths = pd.DataFrame(sols.vpath.tolist(),index=sols.index)
    vpaths.columns=['vpath_'+str(x) for x in vpaths.columns]        
    sols.drop(['upath','vpath'],axis=1,inplace=True)

    sols.to_csv(NAME+'_'+model+'_'+method+'_raw.csv')

# a bit more palatable to have these in columns, with column headers corresponding to the index in sols...
    upaths.T.to_csv(NAME+'_'+model+'_'+method+'_raw_upaths.csv')
    vpaths.T.to_csv(NAME+'_'+model+'_'+method+'_raw_vpaths.csv')
    
    return

