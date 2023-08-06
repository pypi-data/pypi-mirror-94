import time
#from scipy.optimize import minimize
from scipy import optimize

from svolfit.models.model_factory import model_create

def svolfit( series, dt, model='Heston', method = 'grid', modeloptions={}, RunInfo={} ):

    status='Failed'
    message='Incomplete'

    sol = {}
    sol['RunInfo_'+'model']=model
    sol['RunInfo_'+'method']=method
    sol['RunInfo_'+'dt']=dt

    for x in RunInfo:
        sol['RunInfo_'+x]=RunInfo[x]
    
    try:
        model=model_create(series, dt, model, method, modeloptions )
    except:
        message='Model creation failed.'
        sol['ts_upath']=[]
        sol['ts_vpath']=[]
        return status,message,{},sol
    
    (wpn,wp,wpb)=model.get_workingpars()
    for cc in range(0,len(wpn)):
        sol['init_wrk_'+wpn[cc]]=wp[cc]

    (rdict)=model.get_reportingpars()
    for x in rdict:
        if( x[0:4]=='rep_' ):
            sol['init_'+x]=rdict[x]


    mcons=model.get_constraints()

    opts={'disp': True, 'ftol': 1.0e-8}
    start_time = time.process_time()

    res = optimize.minimize(lambda x: model.objective_calculate(x), wp, jac=lambda x: model.calculate_gradient(x),method='SLSQP',bounds=wpb,constraints=mcons,options=opts)
#    res = optimize.differential_evolution(lambda x: model.objective_calculate(x), bounds=wpb,constraints=mcons,popsize=150,disp=True)

    for x in res:
        sol['opt_'+x]=res[x]

    wp=res.x
    wpg=res.jac
    for cc in range(0,len(wp)):
        sol['wrk_'+wpn[cc]]=wp[cc]
        sol['wrk_grad_'+wpn[cc]]=wpg[cc]
    
    (rdict)=model.get_reportingpars()
    rpdict={}
    for x in rdict:
        if( (x[0:3] != 'ts_') ):
            rpdict[x]=rdict[x]
    if( 'ts_upath' in rdict ):
        sol['ts_upath']=rdict['ts_upath']
    else:
        sol['ts_upath']=[]
    if( 'ts_vpath' in rdict ):
        sol['ts_vpath']=rdict['ts_vpath']
    else:
        sol['ts_vpath']=[]
    if( 'ts_standardreturns' in rdict ):
        sol['ts_standardreturns']=rdict['ts_standardreturns']
    else:
        sol['ts_standardreturns']=[]
    
    elapsed_time = time.process_time() - start_time
    sol['proctime']=elapsed_time

#TODO: with diagnostics flag, check that value, grad/etc 
# matches on recalc?
#    grad=model.calculate_gradient(wp)
#    sol['gradient']=grad

# delete some of the vectors we dont need any more -- they make the dataframe ugly:
    dellist=['opt_x','opt_jac']
    for x in dellist:
        if( x in sol):
            del sol[x]        

# do last!
    stdict=model.get_stats()
    for x in stdict:
        sol['stat_'+x]=stdict[x]

    (status,message)=model.status()
    sol['model_status']=status
    sol['model_message']=message

    if( res['success']!=True ):
        status='Failed'
        message='Optimization unsuccessful.'
                
    print(status,message,sol['proctime'],sol['opt_fun'],RunInfo)
    
    return (status,message,rpdict,sol)

