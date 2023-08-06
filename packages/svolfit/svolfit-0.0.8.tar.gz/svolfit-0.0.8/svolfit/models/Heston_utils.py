import numpy as np
from scipy.special import loggamma,ive
#from scipy.special import logsumexp,loggamma

from svolfit.models.model_utils import logsumexp

def stepcalc_tree(alpha,dt,delta,Vb,gamma,tu0,tdelta0,u_prev,space,ni,u_this_full,pi_mid,pi_up,pi_dn):

    n_top = len(u_prev)

    M=space[0,0:n_top]
    m=space[1,0:n_top]
    v=space[2,0:n_top]
    mm=space[3,0:n_top]
    mp=space[4,0:n_top]
    deltam=space[5,0:n_top]
    deltap=space[6,0:n_top]

    M[:]=-np.expm1(-alpha*dt)+np.exp(-alpha*dt)*u_prev

    ni[:]=np.floor(0.5 -(0.5+tdelta0/delta)+np.sqrt((0.5+tdelta0/delta)*(0.5+tdelta0/delta)-2.0*(tu0-M)/delta) )

    #avoids pointing to the zero state:
    ni[:]=np.maximum(ni,1)        
    n_min=np.maximum(0,np.min(ni)-1)
    n_max=np.max(ni)+1
#        print(M,ni,n_min,n_max)
        
    n_top2=n_max-n_min+1
        
    u_this=u_this_full[0:n_top2]
    
#    u_this[:]=np.linspace(n_min,n_max,n_max-n_min+1,int)
    try:
        u_this[:]=np.array(range(n_min,n_max+1))
    except:
        print(n_min,n_max,range(n_min,n_max+1))
    u_this[:]=tu0+u_this*tdelta0+u_this*(u_this+1)*delta/2.0

# set the first entry to zero when it is at the zero entry.
    if(n_min==0 ):
        u_this[0]=0.0
#    if( RunTests==True ):
#        if(np.min(u_this)<0):
#            print('min fail')
   
    deltap[:]= u_this[ni-n_min+1]-u_this[ni-n_min]
    deltam[:]= u_this[ni-n_min]-u_this[ni-n_min-1]

#    if( RunTests==True ):
#        if(np.min([np.min(deltap),np.min(deltam)])<=0.0 ):
#            print(1,np.min(deltap),np.min(deltam))#should not happen

    mp[:]=np.sqrt(deltap/deltam)/2.0
    mm[:]=np.sqrt(deltam/deltap)/2.0

    m[:]=(M-u_this[ni-n_min])/np.sqrt(deltap*deltam)
    v[:]=Vb*(gamma+u_prev)/(deltap*deltam)

#    if( RunTests==True ):
#        if( (np.max(m-mp)>0.0) or (np.max(mm+m)<0.0) ):
#            print('m bound failure')
    
    pi_up[:]=(deltam/(deltap+deltam))*(v+m*(m+2.0*mm))
    pi_dn[:]=(deltap/(deltap+deltam))*(v+m*(m-2.0*mp))
    pi_mid[:]=1.0-pi_up-pi_dn
#        print(pi_dn,pi_mid,pi_up)

#TODO: fix this, 2-pt calc using bracketing nodes
    for off in range(0,4):
        if( len(pi_up)> off ):
            if( np.min([pi_up[off],pi_dn[off],pi_mid[off]]) < 0.0 ):
#                    print(off,pi_dn[off],pi_mid[off],pi_up[off])
                if( M[off] < u_this[ni[off]-n_min] ):
                    pi_up[off]=0.0
                    pi_mid[off]=-(M[off]-u_this[ni[off]-n_min])/deltam[off]
                    pi_dn[off]=1.0-pi_mid[off]
#                        print(1,off,pi_dn[off],pi_mid[off],pi_up[off])
                elif( M[off] > u_this[ni[off]-n_min] ):
                    pi_dn[off]=0.0
                    pi_up[off]=-(M[off]-u_this[ni[off]-n_min+1])/deltap[off]
                    pi_mid[off]=1.0-pi_up[off]                
#                        print(2,off,pi_dn[off],pi_mid[off],pi_up[off])
                else:
                    print('fail')
    #            print('pidn')

    # if( RunTests==True ):
    #     if( (np.max([pi_dn,pi_mid,pi_up])>1.0) or (np.min([pi_dn,pi_mid,pi_up])<0.0) ) :
    #         print(pi_dn)
    #         print(pi_mid)
    #         print(pi_up)
    #         print(ni)
    #         print('piplus')
   
    return (n_min,n_max,n_top2)

#TODO: Clean up!
# def condassetprob_calc_limit(y,u_prev,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du):
#
#     du_tmp=u_this-u_prev
# # assume average: doesn't seem to make a lot of difference
# #    iu_tmp=(u_this+u_prev)*dt/2.0
#     iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
#     vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
#     vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    
# #    if( RunTests==True ):
# #        if( np.min(vol_tmp)<= 0.0 ):
# #            print(2,vol_tmp)
#        
#     yy_tmp=( y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
#    
#     condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
#        
#     return condprob

def condassetprob_calc_exact(y,u_prev,u_this,dt,alpha,rho,sigma,xi,q,MI_f1,MI_f2,MI_f3,coeff_dt,coeff_iu,coeff_du):

    epsilon=alpha*dt/2.0    

    du_tmp=u_this-u_prev
    iu_tmp=MI_Calc(alpha,sigma,xi,q,dt,epsilon,MI_f1,MI_f2,MI_f3,u_prev,u_this)
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    if( np.min(vol_tmp)<= 0.0 ):
        print(2,vol_tmp)
    yy_tmp=(y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp)/vol_tmp
    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    
    return condprob

def MI_Calc(alpha,sigma,xi,q,dt,epsilon,MI_f1,MI_f2,MI_f3,v1,v2):

    z_tol=1.0e-2

    iu_tmp=MI_f1*(v2+v1)*dt/3.0
    iu_tmp+=MI_f2*sigma*sigma*dt*epsilon/3.0

# the floor doesn't matter since the contribution is zeroed below
    epsoZ0=xi*xi*dt/(4.0*np.maximum( 1.0e-16, np.sqrt(v2*v1) ) )

#looks like this is robust enough that it will be very close to 1 or nan in the limit
    shoe = 1.0+epsilon*epsilon/6.0+epsilon*epsilon*epsilon*epsilon/120.0
    if( epsilon > 1.0e-4 ):
        shoe = np.sinh(epsilon)/epsilon
    z=epsoZ0/shoe
    MI_Rat=ive(q,z)/ive(q-1,z)
    np.nan_to_num(MI_Rat,nan=1.0,copy=False)

#     MI_Rat=1.0-epsoZ0*(2.0*q-1.0)/2.0+epsoZ0*epsoZ0*(2.0*q-1.0)*(2.0*q+1.0)/8.0

# # can have epsilon small when epsoZ0 is not -- currently not handled well... 
#     shoe = 1.0+epsilon*epsilon/6.0+epsilon*epsilon*epsilon*epsilon/120.0
#     if( epsilon > 1.0e-4 ):
#         shoe = np.sinh(epsilon)/epsilon
# #    z=2.0*alpha*np.sqrt(v2*v1)/(xi*xi)/np.sinh(epsilon)
#     z=epsoZ0/shoe
    
#     maskcond = np.logical_and( epsoZ0>z_tol, v1*v2>0.0 )
#     MI_Rat[maskcond]=ive(q,z[maskcond])/ive(q-1,z[maskcond])

    # if( len ( ive(q-1,z[maskcond]) ) > 0 ):
    #     if( np.min( ive(q-1,z[maskcond]) ) < 1.0e-12 ):
    #         print('ive')
    #         print(ive(q-1,z[maskcond]))    

    iu_tmp+=MI_f3*(np.sqrt(v2*v1)*dt/3.0)*MI_Rat

    return iu_tmp


#-------------------------------------------------

def condassetprob_calc_limit_X2(y,u_prev,u_mid,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du):

    du_tmp=u_this-u_prev
# assume average: doesn't seem to make a lot of difference
#    iu_tmp=(u_this+u_prev)*dt/2.0
    iu_tmp=(u_this+u_mid+np.sqrt(u_this*u_mid))*dt/3.0
    iu_tmp+=(u_mid+u_prev+np.sqrt(u_mid*u_prev))*dt/3.0

    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)
    yy_tmp=( y-2.0*coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
    
    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    
    return condprob


#-------------------------------------------------

def Heston_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,lncp):

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
        
    lncp[:,:]=np.tile(y,(len(u_this),1)).T
    lncp[:,:]=( lncp-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
    
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    lncp[:,:]=-0.5*lncp*lncp - np.log( vol_tmp*np.sqrt(2.0*np.pi) )
    
    return 

def Heston_standardreturn(y,upath,dt,rho,sigma,mu,alpha,xi,strets):

    coeff_dt=(mu-alpha*rho*sigma/xi)*dt
    coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
    coeff_du = rho*sigma/xi

    u_prev=upath[0:len(upath)-1]
    u_this=upath[1:len(upath)]
    
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
        
    strets[:]=y
    strets[:]=( strets-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
    
    
    return 

#----------------------------------------------------------------------------------------------------

def Heston_griddefs(dt,alpha,xi,lamb):
    
    q=2.0*alpha/(xi*xi)
    
    if( alpha*dt < 1.0e-6 ):
        gamm=0.5*alpha*dt*(1+0.5*alpha*dt)
        Vb=(xi*xi)*np.exp(-alpha*dt)*dt*(1-0.5*alpha*dt)
        gamff=(1.0+alpha*dt/2.0+alpha*dt*alpha*dt/12.0)/(alpha*dt)
    else:
        gamm=np.expm1(alpha*dt)/2.0
        Vb=-xi*xi*np.expm1(-alpha*dt)*np.exp(-alpha*dt)/alpha
        gamff=-1.0/np.expm1(-alpha*dt)
    if( np.isnan(gamm) or np.isnan(Vb) ):
        print('gamma,Vb')
        print(alpha,q,xi,gamm,Vb)# should not happen with limit on alpha...
    
    delta=Vb/(2.0*lamb)

    A=(gamff+1.0)/2.0
    B=gamff*( 2.0*lamb*q*(2.0*gamm+1.0) -1.0 )
    i_lower=np.int64( np.floor( -A+np.sqrt( A*A+B ) ) )

    A=(-gamff+1.0)/2.0
    B=gamff*( 2.0*lamb*q*(2.0*gamm+1.0) )
    i_upper=np.int64(np.ceil( -A+np.sqrt( A*A+B ) ) )
    i_lower=np.maximum(0,i_lower)
    i_length=i_upper-i_lower + 1

    u_grid=(delta/2.0)*np.array([i*(i+1) for i in range(i_lower,i_upper+1)])    

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

#don't need p, just lnp -- more direct
#    p_init=gamma.pdf(u_grid,q,scale=1.0/q)
#    p_init*=np.sqrt(deltap*deltam)
#    if( np.isinf(p_init[0]) == True ):
#        p_init[0]=np.maximum(0.0,1.0-np.sum(p_init[1:]))
#    p_init/=np.sum(p_init)
#    lnp_init=np.log(p_init)
    lnp_init=q*np.log(q)+(q-1.0)*np.log(u_grid)-q*u_grid-loggamma(q)
    lnp_init+= (np.log(deltam)+np.log(deltap))/2.0
    if( (q<1.0) & (u_grid[0]<=0.0) ):
        lnp_init[0]=-logsumexp(lnp_init[1:])
    lnp_init-=logsumexp(lnp_init)

    i_map=np.array([i for i in range(0,i_length)])
    i_map[0]=1
    i_map[i_length-1]=i_map[i_length-2]

    M=-np.expm1(-alpha*dt)+np.exp(-alpha*dt)*u_grid
    m=(M-u_grid[i_map])/np.sqrt(deltap*deltam)

    v=Vb*(gamm+u_grid)/(deltap*deltam)
    
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

def Heston_UsefulGrid(pthresh,lnp):

    pcdf=np.cumsum(np.exp(lnp))    

    Nusefulgrid=len(lnp)
    if( pcdf[-1] > 1.0-pthresh ):
        Nusefulgrid=np.argmax(pcdf>=1.0-pthresh)
    if( pcdf[0] < pthresh ):
        Nusefulgrid-=np.argmin(pcdf<pthresh)

    return Nusefulgrid+1

#----------------------------------------------------------------------------------------------------

def Heston_pathprob(lnp_prev,lnp_this,lncondprob_dn,lncondprob_mid,lncondprob_up,pi_dn,pi_mid,pi_up,tmp_dn,tmp_mid,tmp_up):

    NObs=np.shape(lncondprob_dn)[0]    
    i_length=len(lnp_prev)

    for cc in range(0,NObs):

        tmp_up[:]=lncondprob_up[cc,:]+lnp_prev
        tmp_mid[:]=lncondprob_mid[cc,:]+lnp_prev
        tmp_dn[:]=lncondprob_dn[cc,:]+lnp_prev

        lnp_this[:] = np.zeros(i_length)

        lnp_this[3:i_length-3]=logsumexp( [tmp_up[2:i_length-4],tmp_mid[3:i_length-3],tmp_dn[4:i_length-2]] ,b=[pi_up[2:i_length-4],pi_mid[3:i_length-3],pi_dn[4:i_length-2]], axis=0 )

        lnp_this[0]=logsumexp( [tmp_dn[0],tmp_dn[1]] ,b=[pi_dn[0],pi_dn[1]], axis=0 )
        lnp_this[i_length-1]=logsumexp( [tmp_up[i_length-1],tmp_up[i_length-2]] ,b=[pi_up[i_length-1],pi_up[i_length-2]], axis=0 )

        lnp_this[1]=logsumexp( [tmp_mid[0],tmp_mid[1],tmp_dn[2]] ,b=[pi_mid[0],pi_mid[1],pi_dn[2]], axis=0 )
        lnp_this[i_length-2]=logsumexp( [tmp_mid[i_length-1],tmp_mid[i_length-2],tmp_up[i_length-3]] ,b=[pi_mid[i_length-1],pi_mid[i_length-2],pi_up[i_length-3]], axis=0 )

        lnp_this[2]=logsumexp( [tmp_up[0],tmp_up[1],tmp_mid[2],tmp_dn[3]] ,b=[pi_up[0],pi_up[1],pi_mid[2],pi_dn[3]], axis=0 )
        lnp_this[i_length-3]=logsumexp( [tmp_dn[i_length-1],tmp_dn[i_length-2],tmp_mid[i_length-3],tmp_up[i_length-4]] ,b=[pi_dn[i_length-1],pi_dn[i_length-2],pi_mid[i_length-3],pi_up[i_length-4]], axis=0 )

#        print( lnp_this )        

        lnp_prev[:]=lnp_this
        
    value = logsumexp(lnp_this)

    
    return value
