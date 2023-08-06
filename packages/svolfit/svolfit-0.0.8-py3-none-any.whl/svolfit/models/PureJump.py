import numpy as np
import math
from scipy.special import ndtri

from scipy.stats import norm,mode
from scipy.stats import t as tdist
from scipy.special import gammaln

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.PureJump_utils import PureJump_lncondassetprob,PureJump_calibratemoments,PureJump_moments
from svolfit.models.MertonJD_utils import sim_NormalJumps

#---------------------------------------------

class PureJump_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)

        return

    def _init_d(self):

        self.lamb_scaling = 1000.0

        mu=0.0
        lamb = 20.0/self.lamb_scaling
        gamm = 0.0
        omeg = 0.02
        lamb_upper = 504.0
        lamb_lower = 0.01
        r_lower = 0.05
        if( len(self.series) > 1 ):
#            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
#            Nret=self.Nobs-1
#            ytmp=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
#            mu=mode(ytmp,axis=None)[0][0]/self.dt		
            (mu,lamb,gamm,omeg) = PureJump_calibratemoments(np.array(self.series),self.dt)
            mu=0.0			
            lamb_lower = 10/self.dt/len(self.series)

# careful needs unscaled lambda:
        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))
        r=np.maximum(r_lower,r)
        phi=math.atan2(gamm,omeg)

        lamb = lamb/self.lamb_scaling
        lamb_lower = lamb_lower/self.lamb_scaling
        lamb_upper=lamb_upper/self.lamb_scaling
        
        lamb=np.maximum(lamb_lower,lamb)

        self.workingpars_names=['mu','lambda','r','phi']
        self.workingpars=np.array([mu,lamb,r,phi])
        self.workingpars_sim=np.array([mu,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0001,0.001]


#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]

        self.workingpars_optflag=[True,True,True,True]

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
        lamb=self.workingpars[1]
        r=self.workingpars[2] 
        phi=self.workingpars[3]
        
        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))
        phi=math.atan2(gamm,omeg)

        lamb = lamb / self.lamb_scaling

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=lamb
            self.workingpars[2]=r
            self.workingpars[3]=phi
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=lamb
            self.workingpars_sim[2]=r
            self.workingpars_sim[3]=phi
        
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

# keep the unneeded dimension in here so that the jumps are the same as the Merton Simulations!
        corrmatrix=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=0.0

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0]
        lamb=self.workingpars_sim[1]
        r=self.workingpars_sim[2] 
        phi=self.workingpars_sim[3]

        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)

#        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: jump indicator
# Zs[2,:,:]: jump size

        sim_asset+=(mu-0.5*variance)*self.dt

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[1:3,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        sim_variance =variance       

        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu = self.workingpars[0]
        lamb = self.workingpars[1]
        r = self.workingpars[2]
        phi = self.workingpars[3]

        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        vpath=self.upath

        ret['rep_mu']=mu
        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg

        sim_mu = self.workingpars_sim[0]
        sim_lamb = self.workingpars_sim[1]
        sim_r = self.workingpars_sim[2]
        sim_phi = self.workingpars_sim[3]

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_gamm=sim_r*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg

        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret
    
    def update(self):
        super().update()

        mu = self.workingpars[0]
        lamb = self.workingpars[1]
        r = self.workingpars[2]
        phi = self.workingpars[3]

        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)
        
        Nret=self.Nobs-1

        self.grid_lncondprob_mid = np.zeros((Nret,1))

        self.lncondprob_calc=lambda yasset,lncp: PureJump_lncondassetprob(yasset,self.dt,mu,lamb,gamm,omeg,lncp)

            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu = self.workingpars[0]
        lamb = self.workingpars[1]
        r = self.workingpars[2]
        phi = self.workingpars[3]

        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)

        self.lncondprob_calc(self.yasset,self.grid_lncondprob_mid)

        lncondprob_mid = self.grid_lncondprob_mid
#        value = logsumexp(lncondprob_mid)/Nret
        value = np.sum(lncondprob_mid)/Nret

        if( np.isnan(value) == True ):
            print(value,mu,lamb,gamm,omeg)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,jumpintensity,jumpmean,jumpvolatility)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.zeros(Nret+1)

        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'
        
        mu=self.workingpars[0] 
        lamb = self.workingpars[1]
        r = self.workingpars[2]
        phi = self.workingpars[3]
        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
        gamm=r*np.sin(phi)/np.sqrt(lamb)
        omeg=r*np.cos(phi)/np.sqrt(lamb)
       
        (V,S,K)=PureJump_moments(self.dt,lamb,gamm,omeg)

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
                message='Jump Kurtosis not material--noisy fit.'
            else:
                status='Success'
                message='No issues.'
            
        
        return (status,message)
        
#---------------------------------------------

