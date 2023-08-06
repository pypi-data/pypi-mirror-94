import numpy as np

from scipy import special
from math import factorial

from svolfit.models.model_utils import logsumexp
from svolfit.models.MertonJD_utils import lnprob_NormalJump


#---------------------------------------------

def Bates_condassetprob_limitX2(y,u_prev,u_mid,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du,lamb,gamm,omeg):

    probtol=1.0e-10

    du_tmp=u_this-u_prev
    iu_tmp=(u_this+u_mid+np.sqrt(u_this*u_mid))*dt/3.0
    iu_tmp+=(u_mid+u_prev+np.sqrt(u_mid*u_prev))*dt/3.0

    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)

#    yy_tmp=( y-2.0*coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))

#    du_tmp=u_this-u_prev
## assume average: doesn't seem to make a lot of difference
##    iu_tmp=(u_this+u_prev)*dt/2.0
#    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
#    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
#    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)
##    yy_tmp=( y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
##    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))

# note need 2xdt here since the jumps are for the combined interval!
    NumberTerms=11
    j_probs=np.array([ np.exp(-lamb*2.0*dt)*np.power(lamb*2.0*dt,cj)/factorial(cj) for cj in range(0,NumberTerms)])

    if( j_probs[-1] > probtol ):
        NumberTerms=np.maximum(3,np.argmax(j_probs<=probtol))
    j_probs=j_probs[0:NumberTerms]
    j_probs[NumberTerms-1]=1.0-np.sum(j_probs[0:NumberTerms-1])

    j_nj = np.array(range(0,NumberTerms))

    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,omeg*omeg*j_nj))
    j_yy_tmp=( np.subtract.outer(y-2.0*coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp,gamm*j_nj) )/j_vol_tmp
    
    j_condprob=np.exp(-0.5*j_yy_tmp*j_yy_tmp)/(j_vol_tmp*np.sqrt(2.0*np.pi))
    
    condprob=j_probs@j_condprob.T
    
    return condprob

#---------------------------------------------

def Bates_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp):

    coeff_dt=(mu-alpha*rho*sigma/xi)*dt
    coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
    coeff_du = rho*sigma/xi
    
    du_tmp=u_this-u_prev
# assume average: doesn't seem to make a lot of difference
#    iu_tmp=(u_this+u_prev)*dt/2.0
    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)

# checking all entries is slow!
#    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    if( vol_tmp[0]<1.0e-12 ):
#        print(vol_tmp[vol_tmp<1.0e-12])
        vol_tmp[0]=1.0e-12
    
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
