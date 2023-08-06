import numpy as np

from scipy import special
from scipy import stats

from svolfit.models.model_utils import logsumexp

#---------------------------------------------

def GARCHdiff_griddefs(dt,alpha,xi,lamb):
    
    q=2.0*alpha/(xi*xi)

    if( alpha*dt < 1.0e-6 ):
        ff=alpha*dt*(1.0-alpha*dt/2.0)
    else:
        ff=-np.expm1(-alpha*dt)
    
# when both these conditions are satisfied then there is cacellation in B 
# across the two terms.  Hopefully this wont matter...
    if( alpha*dt/q < 1.0e-6 ):
        C=np.exp(-2.0*alpha*dt)*(2.0*alpha*dt/q)*(1.0+alpha*dt/q)
    else:
        C=np.exp(-2.0*alpha*dt)*np.expm1(2.0*alpha*dt/q)

    if( alpha*dt*(2.0-q)/q < 1.0e-6 ):
        B=(4.0*alpha*dt/q)*np.exp(-alpha*dt)*(1.0+alpha*dt*(2.0-q)/(2.0*q)+alpha*alpha*dt*dt*(2.0-q)*(2.0-q)/(6.0*q*q) )
        B-=2.0*C
        A=np.exp(-alpha*dt)*ff+ff/(q-1.0) \
            -(q/(q-1.0))*np.exp(-alpha*dt)*alpha*dt*(1.0-alpha*dt*(q-2.0)/(2.0*q))
    else:
        B=(4.0/(2.0-q))*np.exp(-alpha*dt)*np.expm1(alpha*dt*(2.0-q)/q)
        B-=2.0*C        
        A=np.exp(-alpha*dt)*ff+ff/(q-1.0) \
            +(q*q/(q-1.0))*np.exp(-alpha*dt)*np.expm1(-alpha*dt*(q-2.0)/q)/(q-2.0)

# need A for the variance calc
    A=0 
        
    if( np.isnan(B) or np.isnan(C) ):
        print('B,C')
        print(alpha,xi,q,B,C)# should not happen with limit on alpha...
    
    BoC=B/C

    eb=1.0+C/(2.0*lamb)+np.sqrt((2.0+C/(2.0*lamb))*C/(2.0*lamb))
    b=np.log(eb)
    delta1=B/(4.0*lamb)+np.sqrt( (BoC+B/(4.0*lamb))*B/(4.0*lamb) )

    num=1.0+2.0/BoC
    den=1.0+(eb-1.0)/2.0/ff
    i_lower=np.maximum(0, np.int64( np.floor( np.log(num/den)/b ) ) )

    den=1.0-(1.0-1.0/eb)/2.0/ff

# estimated a target i_upper by matching the cdf with tail prob:
    ptarg=1.0e-12
    u_targ=stats.invgamma.isf(ptarg,1.0+q,scale=q)
    i_targ=np.int64(np.ceil( np.log(1.0+2.0*C*u_targ/B)/b ) )

    i_upper=i_targ
    if( den > 0.0 ):
        i_upper=np.minimum( i_upper, np.int64(np.ceil( np.log(num/den)/b ) ) )
            
    i_length=i_upper-i_lower + 1

    u_grid=B/(2.0*C)*(np.array([np.power(eb,i) for i in range(i_lower,i_upper+1)]) -1.0)    

#    tmp=invgamma.pdf(u_grid,1.0+q,scale=q)

    deltap=np.zeros(i_length)
    deltam=np.zeros(i_length)

    deltap[1:i_length-1]= u_grid[2:i_length]-u_grid[1:i_length-1]
    deltam[1:i_length-1]= u_grid[1:i_length-1]-u_grid[0:i_length-2]
    deltap[i_length-1]=deltap[i_length-2] 
    deltam[i_length-1]=deltap[i_length-3] 
    deltap[0]=deltam[2] 
    deltam[0]=deltam[1] 

    mp=np.sqrt(deltap/deltam)/2.0
    mm=np.sqrt(deltam/deltap)/2.0

# just lnp:
    lnp_init=(1.0+q)*np.log(q)-(2.0+q)*np.log(u_grid)-q/u_grid-special.loggamma(1.0+q)
    lnp_init+= (np.log(deltam)+np.log(deltap))/2.0
    if( (q<1.0) & (u_grid[0]<=0.0) ):
        lnp_init[0]=-logsumexp(lnp_init[1:])
    lnp_init-=logsumexp(lnp_init)

    i_map=np.array([i for i in range(0,i_length)])
    i_map[0]=1
    i_map[i_length-1]=i_map[i_length-2]

    M=-np.expm1(-alpha*dt)+np.exp(-alpha*dt)*u_grid
    m=(M-u_grid[i_map])/np.sqrt(deltap*deltam)

    v=(A+B*u_grid+C*u_grid*u_grid)/(deltap*deltam)
    
    pi3=np.zeros((3,i_length))
    pi_up=pi3[2,:]
    pi_mid=pi3[1,:]
    pi_dn=pi3[0,:]
    
    pi_up[:]=(deltam/(deltap+deltam))*(v+m*(m+2.0*mm))
    pi_dn[:]=(deltap/(deltap+deltam))*(v+m*(m-2.0*mp))
    pi_mid[:]=1.0-pi_up[:]-pi_dn[:]

# just floor and re-scale:
    pi_up[:]=np.maximum(0.0,pi_up)
    pi_mid[:]=np.maximum(0.0,pi_mid)
    pi_dn[:]=np.maximum(0.0,pi_dn)
#    tmp=np.sum([pi_up,pi_mid,pi_dn],axis=0)
    tmp=np.sum(pi3,axis=0)
    pi_up[:]/=tmp
    pi_mid[:]/=tmp
    pi_dn[:]/=tmp
    
    return (i_lower,i_upper,i_map,u_grid,lnp_init,pi3)

#----------------------------------------------------------------------------------------------------


def GARCHdiff_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,lncp):

    utol=1.0e-12
    
    coeff_dt=mu*dt
    coeff_iu = -sigma*sigma/2.0

    coeff_invsqrtu = -alpha*rho*sigma/xi
    coeff_sqrtu = alpha*sigma*rho/xi+rho*sigma*xi/4.0

    coeff_dsqrtu = 2.0*rho*sigma/xi
    
    dsqrtu_tmp=np.sqrt(u_this)-np.sqrt(u_prev)

    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))/3.0
    iu_tmp[iu_tmp<utol]=utol
        
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp*dt)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)
    
    lncp[:,:]=np.tile(y,(len(u_this),1)).T
    lncp[:,:]=( lncp-coeff_dt-coeff_iu*iu_tmp*dt \
               -coeff_invsqrtu * dt / np.sqrt(iu_tmp) \
               -coeff_sqrtu * dt * np.sqrt(iu_tmp) \
               -coeff_dsqrtu*dsqrtu_tmp )/vol_tmp
    
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    lncp[:,:]=-0.5*lncp*lncp - np.log( vol_tmp*np.sqrt(2.0*np.pi) )
        
    return 
