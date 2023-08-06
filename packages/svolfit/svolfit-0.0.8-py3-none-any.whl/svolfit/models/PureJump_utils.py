import numpy as np
from scipy import special
from scipy import stats
from math import factorial

from svolfit.models.model_utils import logsumexp

#-------------------------------------------------
def PureJump_moments(dt,lamb,gamm,omeg):

    V=lamb*dt*(gamm*gamm+omeg*omeg)
    m3=lamb*dt*gamm*(gamm*gamm+3.0*omeg*omeg)
    m4=lamb*dt*(gamm*gamm*gamm*gamm+6.0*gamm*gamm*omeg*omeg+3.0*omeg*omeg*omeg*omeg)
    S=m3/(V*np.sqrt(V))
    K=m4/(V*V)

    return V,S,K


def PureJump_calibratemoments(series,dt):
	
    Nret=len(series)-1
    yasset=np.log( series[1:Nret+1]/series[0:Nret] )

    mu=np.mean(yasset)
    gamm=0.0
    V=stats.moment(yasset,moment=2)
    m4=stats.moment(yasset,moment=4)
    fact=m4/(3.0*V*V)-1.0
    if( fact < 1.0e-6 ):
        lamb=1.0
        omeg=np.sqrt(V/dt)
        return (mu,lamb,gamm,omeg)
    
#    lamb=3.0/fact
#    omeg=np.sqrt(V/lamb)	
#    lamb /= dt

    lamb=1.0
    omeg=np.sqrt(V/dt)

    return (mu,lamb,gamm,omeg)

def calibratemoments(series,dt):
	
    Nret=len(series)-1
    yasset=np.log( series[1:Nret+1]/series[0:Nret] )

    mu=np.mean(yasset)
    gamm=0.0
    V=stats.moment(yasset,moment=2)
    fact=stats.moment(yasset,moment=4)
    fact=fact/(3.0*V*V)-1.0
    lamb=1.0/fact
    omeg=np.sqrt(V*fact)	
    lamb /= dt

    return (mu,lamb,gamm,omeg)

def PureJump_lncondassetprob(y,dt,mu,lamb,gamm,omeg,lncp):

#TODO: tune this somehow...
    sigma=1.0e-4
# calc probabilities first to determine the number of terms needed:    
    lnprobtol=np.log(1.0e-32)
    Njump=21# can't do more than 21, the log(fact) overflows.
    j_lnprobs=np.zeros(Njump)
    j_lnprobs[0]=-lamb*dt
    j_lnprobs[1:Njump]=np.array([-lamb*dt+cj*np.log(lamb*dt)-np.log(factorial(cj)) for cj in range(1,Njump)])
    if( j_lnprobs[-1] > lnprobtol ):
        Njump=np.maximum(3,np.argmax(j_lnprobs<=lnprobtol))
    j_lnprobs=j_lnprobs[0:Njump]
#    j_lnprobs-=special.logsumexp(j_lnprobs)
    j_lnprobs-=logsumexp(j_lnprobs)

    bbar = np.expm1(gamm+0.5*omeg*omeg)
    coeff_dt=(mu-sigma*sigma/2.0-lamb*bbar)*dt
#    coeff_dt=mu*dt
    
    vol_tmp=sigma*np.sqrt(dt)
        
    Nobs=len(y)
    Ngrid=1

    j_nj = np.array(range(0,Njump))
    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,omeg*omeg*j_nj))
   
    j_yy_tmp=np.zeros((Nobs,Ngrid,Njump))
    j_yy_tmp[:,:,:]=np.tile(y,(Njump,Ngrid,1)).T
    j_yy_tmp[:,:,:]-=np.tile(np.tile(coeff_dt,(Nobs,1)).T,(Njump,1,1)).T
    j_yy_tmp[:,:,:]-=np.tile(gamm*j_nj,(Nobs,Ngrid,1))
    j_yy_tmp[:,:,:]/=np.tile(j_vol_tmp,(Nobs,1,1))
    
# log-probs    
    j_yy_tmp[:,:,:]=-0.5*j_yy_tmp*j_yy_tmp-np.log(np.tile(j_vol_tmp,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)

# add jump log-probs
    j_yy_tmp[:,:,:]+=np.tile(j_lnprobs,(Nobs,Ngrid,1))

# logsumexp to result in log prob for condasset unconditional on jumps
#    lncp[:,:] = special.logsumexp(j_yy_tmp,axis=2)
    lncp[:,:] = logsumexp(j_yy_tmp,axis=2)
        
    return 
    
