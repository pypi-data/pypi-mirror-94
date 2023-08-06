import numpy as np

#---------------------------------------------

def H32_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,lncp):

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
    
    lncp[:,:]=np.tile(y,(len(u_this),1)).T
    lncp[:,:]=( lncp-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
    
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    lncp[:,:]=-0.5*lncp*lncp - np.log( vol_tmp*np.sqrt(2.0*np.pi) )
        
    return 
