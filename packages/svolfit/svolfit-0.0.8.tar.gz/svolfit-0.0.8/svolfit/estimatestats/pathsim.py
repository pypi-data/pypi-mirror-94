import numpy as np
import pandas as pd 

from numpy.random import Generator,PCG64

from svolfit.models.model_factory import model_create


def pathsim(NAME,Nsteps,Npaths,windows, dt, model, method, modeloptions ):

    success= False    
    series=[]
    try:
        modelobj=model_create(series, dt, model, method, modeloptions )
    except:
        print('failed to create model')
        return success,[],[]

    (assetname,assetval,variancename,varianceval,corrmatrix,Nperstep)=modelobj.get_structure()


    Nsimsteps=Nsteps*Nperstep
    Nfactors=np.shape(corrmatrix)[0]
    
    asset=np.zeros((Nsteps+1,Npaths))
    asset[0,:]=assetval
    variance=np.zeros((Nsteps+1,Npaths))
    variance[0,:]=varianceval
    

# 128-bit number as a seed
    root_seed = 43658736987
# I don't really like this since using the same generator with different seeds could easily lead to 
# dependent sequences -- would prefer to have separate streams from a defined generator...
#    rngs = [Generator(PCG64(root_seed + stream_id)) for stream_id in range(0,Nfactors*Npaths)]

    Zs=np.zeros((Nfactors,Nsimsteps,Npaths))
#TODO: danger!  can't really generate more paths than this!
    Nfactoroffset = 100000
    for cf in range(0,Nfactors):
        for cc in range(0,Npaths):
            rng=Generator(PCG64(root_seed + cf*Nfactoroffset+cc))
            Zs[cf,:,cc]=rng.standard_normal(Nsimsteps)
    
# correlate factors:
    if( Nfactors > 1 ):
        chol=np.linalg.cholesky(corrmatrix)
        Zs[:,:,:]=((Zs.T)@(chol.T)).T    
    
    for cs in range(0,Nsteps):
        (asset[cs+1,:],variance[cs+1,:])=modelobj.sim_step(asset[cs,:],variance[cs,:],Zs[:,cs*Nperstep:(cs+1)*Nperstep,:])


    FILE='SimPaths_'+NAME+'_'+model+'_'+method
    asset=pd.DataFrame(asset)
    cols=asset.columns
    asset.columns=[assetname+'_'+str(x) for x in cols]
    asset.to_csv(FILE+'_'+assetname+'.csv')

    variance=pd.DataFrame(variance)
    variance.columns=[variancename+'_'+str(x) for x in cols]
    variance.to_csv(FILE+'_'+variancename+'.csv')

    success=True
    
    return success,assetname,variancename

