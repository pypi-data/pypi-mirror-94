import numpy as np
from scipy import special

from svolfit.models.model_utils import logsumexp
from svolfit.models.MertonJD_utils import lnprob_NormalJump

#---------------------------------------------

def B32_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp):

    utol=1.0e-12
    
    coeff_dt=(mu-alpha*rho*sigma/xi)*dt
    coeff_iu = (rho*alpha*sigma/xi -rho*xi*sigma/2.0 -sigma*sigma/2.0)
    coeff_du = -rho*sigma/xi
    
    du_tmp=np.log(np.maximum(utol,u_this)/np.maximum(utol,u_prev))
# assume average: doesn't seem to make a lot of difference
#    iu_tmp=(u_this+u_prev)*dt/2.0
    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))/3.0
    iu_tmp[iu_tmp<utol]=utol
    iu_tmp = dt/iu_tmp
    
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    
    Nobs=len(y)
    Ngrid=len(u_this)

    Nmix=1
    mix_lnprobs=np.zeros(1) # 1 x Nmix=1
    mix_vol = np.tile(vol_tmp,(1,Nmix)).T # Ngrid x Nmix=1
    mix_yret = np.zeros((Nobs,Ngrid,Nmix)) # Nobs x Ngrid x Nmix=1
    mix_yret[:,:,:]=np.tile(y,(Nmix,Ngrid,1)).T
    mix_yret[:,:,:]-=np.tile(np.tile(coeff_dt+coeff_iu*iu_tmp+coeff_du*du_tmp,(Nobs,1)).T,(Nmix,1,1)).T

    (mix_lnprobs,mix_vol,mix_yret)=lnprob_NormalJump(dt,lamb,gamm,omeg,mix_vol,mix_yret)

# log-probs    
    mix_yret[:,:,:]=-0.5*mix_yret*mix_yret-np.log(np.tile(mix_vol,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)
# add jump log-probs
    mix_yret[:,:,:]+=np.tile(mix_lnprobs,(Nobs,Ngrid,1))

#    lncp[:,:] = special.logsumexp(mix_yret,axis=2)
    lncp[:,:] = logsumexp(mix_yret,axis=2)

    return 
