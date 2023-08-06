import numpy as np
from scipy import stats
from scipy import special
from scipy import optimize
import math

from svolfit.models.model_utils import logsumexp

#-------------------------------------------------

def sim_NormalJumps(dt,lamb,gamm,omeg,Zs,sim_asset):

    Nperstep=np.shape(Zs)[1]
    dtN=dt/Nperstep

#TODO:
# 21 is the maximum number before factorial overflows
# really should be sufficient, but this could do with some improvement...
    max_jumps=21        
    njumps=np.zeros(Nperstep,int)
    probs=np.array([ np.exp(-lamb*dtN)*(lamb*dtN)**cj/math.factorial(cj) for cj in range(0,max_jumps)])
# TODO: put the excess in the first bucket...
    probs=np.cumsum(probs)
    thresh=special.ndtri(probs)

    njumps=np.searchsorted(thresh,Zs[0,:,:])
 
    muj = lamb*np.expm1(gamm+0.5*omeg*omeg)
    sim_asset+=-muj*dt
#    print(lamb,gamm,omeg,muj,dt,muj*dt)

    for cc in range(0,Nperstep):
        sim_asset+=gamm*njumps[cc,:]
        sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[1,cc,:]

    return


#-------------------------------------------------

def moments_NormalJumps(dt,sigma,lamb,gamm,omeg):

    V=sigma*sigma*dt+lamb*dt*(gamm*gamm+omeg*omeg)
    m3=lamb*dt*gamm*(gamm*gamm+3.0*omeg*omeg)
    m4=lamb*dt*(gamm*gamm*gamm*gamm+6.0*gamm*gamm*omeg*omeg+3.0*omeg*omeg*omeg*omeg)
    S=m3/(V*np.sqrt(V))
    K=m4/(V*V)

    return V,S,K

def Constraint_JB(workingpars,JBthreshold,dt,lamb_scaling):
    
#    mu=workingpars[0] 
    sigma=workingpars[1]
    lamb = workingpars[2]
    gamm = workingpars[3]
    omeg = workingpars[4]

    lamb = lamb * lamb_scaling

    V=sigma*sigma*dt+lamb*dt*(gamm*gamm+omeg*omeg)
    m3=lamb*dt*gamm*(gamm*gamm+3.0*omeg*omeg)
    m4=lamb*dt*(gamm*gamm*gamm*gamm+6.0*gamm*gamm*omeg*omeg+3.0*omeg*omeg*omeg*omeg)

    S=m3/(V*np.sqrt(V))
    K=m4/(V*V)

    JB=(S*S+K*K/4.0)

    return JB-JBthreshold

def Constraint_JB_grad(workingpars,JBthreshold,dt,lamb_scaling):
    
#    mu=workingpars[0] 
    sigma= workingpars[1]
    lamb = workingpars[2]
    gamm = workingpars[3]
    omeg = workingpars[4]

    lamb = lamb * lamb_scaling

    V=sigma*sigma*dt+lamb*dt*(gamm*gamm+omeg*omeg)
    m3=lamb*dt*gamm*(gamm*gamm+3.0*omeg*omeg)
    m4=lamb*dt*(gamm*gamm*gamm*gamm+6.0*gamm*gamm*omeg*omeg+3.0*omeg*omeg*omeg*omeg)

    S=m3/(V*np.sqrt(V))
    K=m4/(V*V)

    grad=np.zeros(len(workingpars)) 
    
    grad[0]=0.0

    grad[2]+=2.0*S*(1.0/(V*np.sqrt(V)))*m3/lamb
    grad[3]+=2.0*S*(1.0/(V*np.sqrt(V)))*(m3/gamm+2.0*lamb*dt*gamm*gamm)
    grad[4]+=2.0*S*(1.0/(V*np.sqrt(V)))*6.0*lamb*dt*gamm*omeg

    grad[2]+=0.5*K*(1.0/(V*V))*m4/lamb
    grad[3]+=0.5*K*(1.0/(V*V))*lamb*dt*(4.0*gamm*gamm*gamm+12.0*gamm*omeg*omeg)
    grad[4]+=0.5*K*(1.0/(V*V))*lamb*dt*(12.0*gamm*gamm*omeg+12*omeg*omeg)

    grad[1]+=2.0*S*(-3.0*S/(2.0*V))*2.0*sigma*dt
    grad[2]+=2.0*S*(-3.0*S/(2.0*V))*(gamm*gamm+omeg*omeg)*dt
    grad[3]+=2.0*S*(-3.0*S/(2.0*V))*(2.0*lamb*dt*gamm)
    grad[4]+=2.0*S*(-3.0*S/(2.0*V))*(2.0*lamb*dt*omeg)

    grad[1]+=0.5*K*(-2.0*K/V)*2.0*sigma*dt
    grad[2]+=0.5*K*(-2.0*K/V)*(gamm*gamm+omeg*omeg)*dt
    grad[3]+=0.5*K*(-2.0*K/V)*(2.0*lamb*dt*gamm)
    grad[4]+=0.5*K*(-2.0*K/V)*(2.0*lamb*dt*omeg)

    return grad
    

def MertonJD_calibratemoments(series,dt):
	
# 
    Nret=len(series)-1
    yasset=np.log( series[1:Nret+1]/series[0:Nret] )

    m=np.mean(yasset)/dt
    V=stats.moment(yasset,moment=2)
    m3=stats.moment(yasset,moment=3)
    m4=stats.moment(yasset,moment=4)

    Slim=2.0*6.0/np.sqrt(Nret)
    Klim=2.0*24.0/np.sqrt(Nret)

    S=m3/(V*np.sqrt(V))
    K=m4/(V*V)-3.0
#    print(m,V,m3,m4,S,K)

    if( np.abs(S)<= Slim ): #assume S=0
        K=np.maximum(Klim,K)# assures that lambda isn't overly large
        lamb=1.0/K/dt
        rsq=0.5*(1.0+np.sqrt(3.0))
        r=np.sqrt(rsq)
#        print(r)
        
        sigma=np.sqrt(V/dt/(1+rsq))
    
        gamm=0.0
        omeg=r*sigma/np.sqrt(lamb)
#        print(gamm,omeg)
        bbar = np.expm1(gamm+0.5*omeg*omeg)
        mu=m+0.5*sigma*sigma+lamb*bbar
    	
#        print(S,K,mu,sigma,lamb,gamm,omeg)
        
        return (mu,sigma,lamb,gamm,omeg)

# this all assumes that S is material        
    K=np.maximum(Klim,K)# assures that lambda isn't overly large

    lamb=1.0/K/dt
#    print(lamb)
#solve
#    x=np.sin(phi)**2
    R1=S*S/K
    R1=np.minimum(R1,1.0-1.0/101.0)

    h = lambda x: 1.0-R1*R1*(3.0-2.0*x*x)*(3.0-2.0*x*x)*(3.0-2.0*x*x)/( x*x*(3.0-2.0*x)*(3.0-2.0*x)*(3.0-2.0*x)*(3.0-2.0*x) )
    res = optimize.root_scalar(h, bracket=[1.0e-6,1.0], method='brentq')
#    print(res)
    x=res.root
    phi=np.arcsin(np.sqrt(x))
    if( S < 0.0 ):
        phi = -phi
#    print(S,K,R1,x,phi)
    g = x*(3.0-2.0*x)*(3.0-2.0*x)/(3.0-2.0*x*x)
    rsq=R1/(g-R1)
#    print(rsq)

    r=np.sqrt(rsq)
#    print(r)
    
    sigma=np.sqrt(V/dt/(1+rsq))

    gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
    omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)
#    print(gamm,omeg)
    bbar = np.expm1(gamm+0.5*omeg*omeg)
    mu=m+0.5*sigma*sigma+lamb*bbar
	
#    print(S,K,mu,sigma,lamb,gamm,omeg)
    
    return (mu,sigma,lamb,gamm,omeg)


def MertonJD_calibratemoments_old(series,dt):
	
    Nret=len(series)-1
    yasset=np.log( series[1:Nret+1]/series[0:Nret] )

    mu=np.mean(yasset)/dt
    V=stats.moment(yasset,moment=2)
    m4=stats.moment(yasset,moment=4)
    m6=stats.moment(yasset,moment=6)

    f1 = m4/(3.0*V*V)-1.0
    f2 = (m6/(15.0*V*V*V)-1.0)
#    print(mu,V,m4,m6,f1,f2)

    gamm=0.0
    
    if( f1 <= 0.0 ):
# tails aren't fat...
        omeg=0.002
        lamb=1.0
        sigma = np.sqrt(V/dt)
#        print(mu,sigma,lamb,gamm,omeg)
        return (mu,sigma,lamb,gamm,omeg)
    if( f2 <= 3.0 * f1 ):
# tails aren't the right shape...
        omeg=0.002
        lamb=1.0
        sigma = np.sqrt(V/dt)
#        print(mu,sigma,lamb,gamm,omeg)
        return (mu,sigma,lamb,gamm,omeg)
        
    omeg=np.sqrt( (f2-3.0*f1)*V/f1 )
    lamb=f1*f1*f1/(f2-3.0*f1)/(f2-3.0*f1)
    lamb /= dt
    lamb = np.minimum(126.0,lamb)
#    sigma=np.sqrt(V/dt)*np.sqrt( np.maximum( 0.001*0.001*dt,1.0-f1*f1/(f2-3.0*f1)) )
    sigma=np.sqrt(V/dt)

    bbar = np.expm1(gamm+0.5*omeg*omeg)
    mu=mu+0.5*sigma*sigma+lamb*bbar
	
#    print(mu,sigma,lamb,gamm,omeg)

    return (mu,sigma,lamb,gamm,omeg)


#-------------------------------------------------

def lnprob_NormalJump(dt,lamb,gamm,omeg,base_vol,base_yret):

# jump_lnprobs:    1 x Nmix=Njump
# jump_vol:    Ngrid x Nmix=Njump
# jump_yret:    Nobs x Ngrid x Nmix=Njump

# calc probabilities first to determine the number of terms needed:    
    lnprobtol=np.log(1.0e-12)
    Njump=21
    jump_lnprobs=np.zeros(Njump) 
    jump_lnprobs[0]=-lamb*dt
    jump_lnprobs[1:Njump]=np.array([-lamb*dt+cj*np.log(lamb*dt)-np.log(math.factorial(cj)) for cj in range(1,Njump)])
# check first that the last entry is smaller, otherwise it returns 0!
    if( jump_lnprobs[-1] > lnprobtol ):
        Njump=np.maximum(3,np.argmax(jump_lnprobs<=lnprobtol))
    jump_lnprobs=jump_lnprobs[0:Njump]
#    jump_lnprobs-=special.logsumexp(jump_lnprobs)
    jump_lnprobs-=logsumexp(jump_lnprobs)

    j_nj = np.array(range(0,Njump))

    bbar = np.expm1(gamm+0.5*omeg*omeg)
    coeff_dt=-lamb*bbar*dt

    jump_vol = np.sqrt(np.add.outer(base_vol[:,0]*base_vol[:,0],omeg*omeg*j_nj))
   
    Ngrid=np.shape(base_vol)[0]
    Nobs=np.shape(base_yret)[0]
    
    jump_yret=np.zeros((Nobs,Ngrid,Njump))

    jump_yret[:,:,:]=np.tile(base_yret[:,:,0].T,(Njump,1,1)).T
    jump_yret[:,:,:]-=coeff_dt
    jump_yret[:,:,:]-=np.tile(gamm*j_nj,(Nobs,Ngrid,1))
    jump_yret[:,:,:]/=np.tile(jump_vol,(Nobs,1,1))
    
    return (jump_lnprobs,jump_vol,jump_yret)

def MertonJD_lncondassetprob(y,dt,mu,sigma,lamb,gamm,omeg,lncp):

    coeff_dt=(mu-sigma*sigma/2.0)*dt
    vol_tmp=sigma*np.sqrt(dt)
        
    Nobs=len(y)
    Ngrid=1

    Nmix=1
    mix_lnprobs=np.zeros(1) # 1 x Nmix=1
    mix_vol = np.tile(vol_tmp,(1,Nmix)).T # Ngrid x Nmix=1
    mix_yret = np.zeros((Nobs,Ngrid,Nmix)) # Nobs x Ngrid=1 x Nmix=1
    mix_yret[:,:,:]=np.tile(y,(Nmix,Ngrid,1)).T # Nobs x Ngrid=1 x Nmix=1
    mix_yret[:,:,:]-=np.tile(np.tile(coeff_dt,(Nobs,1)).T,(Nmix,1,1)).T

    (mix_lnprobs,mix_vol,mix_yret)=lnprob_NormalJump(dt,lamb,gamm,omeg,mix_vol,mix_yret)

# log-probs    
    mix_yret[:,:,:]=-0.5*mix_yret*mix_yret-np.log(np.tile(mix_vol,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)
# add jump log-probs
    mix_yret[:,:,:]+=np.tile(mix_lnprobs,(Nobs,Ngrid,1))

#    lncp[:,:] = special.logsumexp(mix_yret,axis=2)
    lncp[:,:] = logsumexp(mix_yret,axis=2)

    return 
    
def MertonJD_standardreturn(y,upath,dt,mu,sigma,lamb,gamm,omeg,strets):

    coeff_dt=(mu-sigma*sigma/2.0)*dt
    vol_tmp=sigma*np.sqrt(dt)

    bbar = np.expm1(gamm+0.5*omeg*omeg)
    coeff_dt=-lamb*bbar*dt

    u_prev=upath[0:len(upath)-1]
    u_this=upath[1:len(upath)]
       
    strets[:]=y
    strets[:]=( strets-coeff_dt )/vol_tmp
    
    
    return 

