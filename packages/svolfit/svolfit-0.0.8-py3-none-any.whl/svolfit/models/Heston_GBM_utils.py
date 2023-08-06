import numpy as np

from scipy.special import logsumexp as splse
from math import factorial

#---------------------------------------------

def Heston_GBM_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,jumpintensity,jumpmean,jumpvolatility,lncp):

# calc probabilities first to determine the number of terms needed:    
    lnprobtol=np.log(1.0e-10)
    Njump=11
    j_lnprobs=np.zeros(Njump)
    j_lnprobs[0]=-jumpintensity*dt
    j_lnprobs[1:Njump]=np.array([-jumpintensity*dt+cj*np.log(jumpintensity*dt)-np.log(factorial(cj)) for cj in range(1,Njump)])
    Njump=np.argmax(j_lnprobs<=lnprobtol)
    j_lnprobs=j_lnprobs[0:Njump]
    j_lnprobs-=splse(j_lnprobs)

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
    
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)
       
    Nobs=len(y)
    Ngrid=len(u_this)

    j_nj = np.array(range(0,Njump))
    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,jumpvolatility*jumpvolatility*j_nj))
   
    j_yy_tmp=np.zeros((Nobs,Ngrid,Njump))
    j_yy_tmp[:,:,:]=np.tile(y,(Njump,Ngrid,1)).T
    j_yy_tmp[:,:,:]-=np.tile(np.tile(coeff_dt+coeff_iu*iu_tmp+coeff_du*du_tmp,(Nobs,1)).T,(Njump,1,1)).T
    j_yy_tmp[:,:,:]-=np.tile(jumpmean*j_nj,(Nobs,Ngrid,1))
    j_yy_tmp[:,:,:]/=np.tile(j_vol_tmp,(Nobs,1,1))
    
# log-probs    
    j_yy_tmp[:,:,:]=-0.5*j_yy_tmp*j_yy_tmp-np.log(np.tile(j_vol_tmp,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)

# add jump log-probs
    j_yy_tmp[:,:,:]+=np.tile(j_lnprobs,(Nobs,Ngrid,1))

# logsumexp to result in log prob for condasset unconditional on jumps
    lncp[:,:] = splse(j_yy_tmp,axis=2)

    return 
