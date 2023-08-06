import numpy as np

#-------------------------------------------------
def GBM_meanvariance(asset,dt):
    
    rets=np.log(asset[1:len(asset)]/asset[0:len(asset)-1])
    
    sigma=np.std(rets,ddof=1)
    mu=np.mean(rets)+0.5*sigma*sigma

    mu = mu/dt
    sigma=sigma/np.sqrt(dt)

    return (mu,sigma)

def GBM_lncondassetprob(y,dt,mu,sigma,lncp):

    coeff_dt=(mu-sigma*sigma/2.0)*dt
    coeff_dt=mu*dt
    
    vol_tmp=sigma*np.sqrt(dt)
        
    yy_tmp=np.tile((y-coeff_dt)/vol_tmp,(1,1)).T
    
# log-probs    
    lncp[:,:]=-0.5*yy_tmp*yy_tmp-np.log(vol_tmp)-0.5*np.log(2.0*np.pi)
        
    return 
    
