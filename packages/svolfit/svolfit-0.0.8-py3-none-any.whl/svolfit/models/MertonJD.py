import numpy as np
import math
from scipy import stats

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import logsumexp,meanvariance
from svolfit.models.MertonJD_utils import MertonJD_lncondassetprob,MertonJD_calibratemoments,Constraint_JB,Constraint_JB_grad,moments_NormalJumps,sim_NormalJumps,MertonJD_standardreturn

#---------------------------------------------

class MertonJD_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        self.lamb_scaling = 1000.0
        
        mu=0.0
        sigma=0.1
        lamb = 20.0/self.lamb_scaling
        gamm = 0.0
        omeg = 0.05
        lamb_upper = 504.0
        lamb_lower = 0.01
        r_lower = 0.05
        if( len(self.series)> 1 ):
            (mu,sigma,lamb,gamm,omeg)=MertonJD_calibratemoments(np.array(self.series),self.dt)
            mu = 0.0
#            print(mu,sigma,lamb,gamm,omeg)
            lamb_lower = 10/self.dt/len(self.series)

# careful needs unscaled lambda:
        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        r=np.maximum(r_lower,r)
        phi=math.atan2(gamm,omeg)

        s=sigma*np.sqrt(1.0+r*r)    

        lamb = lamb/self.lamb_scaling
        lamb_lower = lamb_lower/self.lamb_scaling
        lamb_upper=lamb_upper/self.lamb_scaling
        
        lamb=np.maximum(lamb_lower,lamb)
            
        self.workingpars_names=['mu','s','lambda','r','phi']
        self.workingpars=np.array([mu,s,lamb,r,phi])
        self.workingpars_sim=np.array([mu,s,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0001,0.0001, 0.001]
# recall that only if phi is restricted can we guarantee that omega>0:
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 10.0),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]

        self.workingpars_optflag=[True,True,True,True,True]
        if( 'fix_gamma' in self.options ):
            if(self.options['fix_gamma']==True):
                self.workingpars_optflag[4]=False

        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        s=self.workingpars[1]
        lamb=self.workingpars[2]
        r=self.workingpars[3] 
        phi=self.workingpars[4]

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    

        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)
        
        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='sigma' ):
                sigma=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        phi=math.atan2(gamm,omeg)

        lamb = lamb / self.lamb_scaling
        s=sigma*np.sqrt(1.0+r*r)    

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=s
            self.workingpars[2]=lamb
            self.workingpars[3]=r
            self.workingpars[4]=phi
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=s
            self.workingpars_sim[2]=lamb
            self.workingpars_sim[3]=r
            self.workingpars_sim[4]=phi

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        s=self.workingpars_sim[1]
        r=self.workingpars_sim[3] 
        sigma=s/np.sqrt(1.0+r*r)    

        corrmatrix=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0] 
        s=self.workingpars_sim[1]
        lamb=self.workingpars_sim[2]
        r=self.workingpars_sim[3] 
        phi=self.workingpars_sim[4]

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    

        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        
        dtN=self.dt/Nperstep
        
# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: jump indicator
# Zs[2,:,:]: jump size
        
        sim_asset+=(mu-0.5*variance)*self.dt

        for cc in range(0,Nperstep):
            sim_asset+=np.sqrt(variance*dtN)*Zs[0,cc,:]

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[1:3,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        sim_variance =variance       

        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        s=self.workingpars[1]
        lamb = self.workingpars[2]
        r = self.workingpars[3]
        phi = self.workingpars[4]

        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    

        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        theta=sigma*sigma

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[Nret]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_sigma']=sigma
        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg

        ret['misc_muj']=lamb*np.expm1(gamm+0.5*omeg*omeg)

#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_theta']=theta
        ret['misc_v0']=v0
        ret['misc_vT']=vT

        (V,S,K)=moments_NormalJumps(self.dt,sigma,lamb,gamm,omeg)

        ret['misc_V']=V
        ret['misc_S']=S
        ret['misc_S_sig']=6.0/np.sqrt(Nret)
        ret['misc_Kexc']=K
        ret['misc_Kexc_sig']=24.0/np.sqrt(Nret)
        JB=(S*S+K*K/4.0)*(self.Nobs-1)/6.0
        ret['misc_JB']=JB
        JBpvalue=stats.chi2.cdf(JB,2)
        ret['misc_JBpvalue']=JBpvalue

        sim_mu=self.workingpars_sim[0] 
        sim_s=self.workingpars_sim[1]
        sim_lamb = self.workingpars_sim[2]
        sim_r = self.workingpars_sim[3]
        sim_phi = self.workingpars_sim[4]

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_s']=sim_s
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_sigma=sim_s/np.sqrt(1.0+sim_r*sim_r)    

        sim_gamm=sim_r*sim_sigma*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*sim_sigma*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_sigma']=sim_sigma
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg

        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        Nret=self.Nobs-1
        self.standardreturns=np.zeros(Nret)
        MertonJD_standardreturn(self.yasset,self.upath,self.dt,mu,sigma,lamb,gamm,omeg,self.standardreturns)
        ret['ts_standardreturns']=self.standardreturns

        return ret
    

    def get_constraints(self):
        cons=[]


#        self.JBthreshold = stats.chi2.ppf(0.9,2)*6.0/(self.Nobs-1)

#        con={}
#        con['type']='ineq'
#        con['fun']=lambda x: Constraint_JB(x,self.JBthreshold,self.dt,self.lamb_scaling)
#        con['jac']=lambda x: Constraint_JB_grad(x,self.JBthreshold,self.dt,self.lamb_scaling)
       
#        cons.append(con)
        
        return cons

    def update(self):
        super().update()

        mu=self.workingpars[0] 
        s=self.workingpars[1]
        lamb = self.workingpars[2]
        r = self.workingpars[3]
        phi = self.workingpars[4]

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    

        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)
        
        Nret=self.Nobs-1

        self.grid_lncondprob_mid = np.zeros((Nret,1))

        self.lncondprob_calc=lambda yasset,lncp: MertonJD_lncondassetprob(yasset,self.dt,mu,sigma,lamb,gamm,omeg,lncp)

            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        s=self.workingpars[1]
        lamb = self.workingpars[2]
        r = self.workingpars[3]
        phi = self.workingpars[4]

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    

        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        self.lncondprob_calc(self.yasset,self.grid_lncondprob_mid)

        lncondprob_mid = self.grid_lncondprob_mid
#        value = logsumexp(lncondprob_mid)/Nret
        value = np.sum(lncondprob_mid)/Nret

        if( np.isnan(value) == True ):
            print(value,mu,s,lamb,gamm,omeg)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,sigma,lamb,gamm,omeg)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.ones(Nret+1)

        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'
        
        mu=self.workingpars[0] 
        s=self.workingpars[1]
        lamb = self.workingpars[2]
        r = self.workingpars[3]
        phi = self.workingpars[4]
        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
        sigma=s/np.sqrt(1.0+r*r)    
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)
       
        (V,S,K)=moments_NormalJumps(self.dt,sigma,lamb,gamm,omeg)

        fact = 2.0
        if(np.abs(S)<fact*6.0/np.sqrt(Nret)):
            if(K<fact*24.0/np.sqrt(Nret)):
                status='Warning'
                message='Jump Skewness and Kurtosis not material.'
            else:
                status='Warning'
                message='Jump Skewness not material--try zero jump mean.'
        else:
            if(K<fact*24.0/np.sqrt(Nret)):
                status='Warning'
                message='Jump Kurtosis not material--noisy parameters.'
            else:
                status='Success'
                message='No issues.'
            
        
        return (status,message)

#---------------------------------------------

