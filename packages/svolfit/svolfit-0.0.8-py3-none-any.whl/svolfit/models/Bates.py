import numpy as np
import math

from scipy import special
from scipy import stats

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.Bates_utils import Bates_condassetprob_limitX2,Bates_lncondassetprob
from svolfit.models.MertonJD_utils import sim_NormalJumps,moments_NormalJumps,MertonJD_calibratemoments
from svolfit.models.Heston_utils import Heston_standardreturn


#-------------------------------------

class Bates_tree(Heston_tree):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        self.lamb_scaling = 1000.0

# override/extend Heston defs
        mu=0.0
        sigma=0.1
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1
        lamb = 1.0
        gamm = 0.0
        omeg = 0.02
        lamb_upper = 504.0
        lamb_lower = 0.01
        r_lower = 0.05
        if( len(self.series)>1 ):
            (mu,sigma,lamb,gamm,omeg)=MertonJD_calibratemoments(np.array(self.series),self.dt)
            mu=0.0
            lamb_lower = 10/self.dt/len(self.series)

# careful needs unscaled lambda:
        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        r=np.maximum(r_lower,r)
        phi=math.atan2(gamm,omeg)

        lamb = lamb/self.lamb_scaling
        lamb_lower = lamb_lower/self.lamb_scaling
        lamb_upper=lamb_upper/self.lamb_scaling
        
        lamb=np.maximum(lamb_lower,lamb)

        self.gridfactor=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0','lambda','r','phi']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001, 0.001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]

        self.workingpars_optflag=[True for x in self.workingpars]
        if( 'fix_gamma' in self.options ):
            if(self.options['fix_gamma']==True):
                self.workingpars_optflag[8]=False

        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

#TODO: expose these as options at some point?
            self.ProbFactor =1.09
            self.NormProbCalc='TDist'
            
            if( self.NormProbCalc == 'Normal' ):
                sigma_base=np.std(self.yasset,ddof=1)
                mu_base=np.mean(self.yasset)
                self.cprob_base=stats.norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=stats.t.fit(self.yasset)
                self.cprob_base=stats.t.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
            else:
                print('Unknown NormProbCalc -- Handle')
        # allow for a multiplier:
            self.cprob_base*=self.ProbFactor

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        theta=sigma*sigma
        eta=xi*sigma
        v0=theta*u0

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta

        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        phi=math.atan2(gamm,omeg)
        lamb = lamb / self.lamb_scaling

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
            self.workingpars[6]=lamb
            self.workingpars[7]=r
            self.workingpars[8]=phi
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
            self.workingpars_sim[6]=lamb
            self.workingpars_sim[7]=r
            self.workingpars_sim[8]=phi

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars_sim[5]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0] 
        sigma=self.workingpars_sim[1]
#        rho=self.workingpars_sim[2]
        alpha=self.workingpars_sim[3] 
        xi=self.workingpars_sim[4]
#        u0=self.workingpars_sim[5]
        lamb = self.workingpars_sim[6]
        r = self.workingpars_sim[7]
        phi = self.workingpars_sim[8]

        theta=sigma*sigma
        eta=xi*sigma
        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: variance driver
# Zs[2,:,:]: jump indicator
# Zs[3,:,:]: jump size

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[2:4,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        Nret=self.Nobs-1
        
        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg
#        ret['u0']=u0
        ret['rep_v0']=v0

        ret['misc_muj']=lamb*np.expm1(gamm+0.5*omeg*omeg)

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
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]
        sim_lamb = self.workingpars_sim[6]
        sim_r = self.workingpars_sim[7]
        sim_phi = self.workingpars_sim[8]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi
        ret['sim_wrk_u0']=sim_u0

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_gamm=sim_r*sim_sigma*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*sim_sigma*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg
        ret['sim_rep_v0']=sim_v0

        ret['misc_q']=q
#        ret['uT']=uT
        ret['misc_vT']=vT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        Nret=self.Nobs-1
        self.standardreturns=np.zeros(Nret)
        Heston_standardreturn(self.yasset,self.upath,self.dt,rho,sigma,mu,alpha,xi,self.standardreturns)
        ret['ts_standardreturns']=self.standardreturns

        return ret

    def update(self):
        super().update()

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
#            u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        dt=self.dt
        
        CondProbCalc='Limit'
        if( CondProbCalc=='Limit' ):
            self.lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Bates_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp)
        else:
            print('Unknown Calc -- Handle')                

        return

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
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

#-------------------------------------

class Bates_treeX2(Heston_treeX2):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        self.lamb_scaling = 1000.0

        mu=0.0
        sigma=0.1
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1
        lamb = 1.0/self.lamb_scaling
        gamm = 0.0
        omeg = 0.02
        lamb_upper = 504.0
        lamb_lower = 0.01
        r_lower = 0.05
        if( len(self.series)>1 ):
            (mu,sigma,lamb,gamm,omeg)=MertonJD_calibratemoments(np.array(self.series),self.dt)
            mu = 0.0
#            print(mu,sigma,lamb,gamm,omeg)
            lamb_lower = 10/self.dt/len(self.series)

        self.dt2 = self.dt/2.0

# careful needs unscaled lambda:
        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        r=np.maximum(r_lower,r)
        phi=math.atan2(gamm,omeg)

        s=sigma*np.sqrt(1.0+r*r)    

        lamb = lamb/self.lamb_scaling
        lamb_lower = lamb_lower/self.lamb_scaling
        lamb_upper=lamb_upper/self.lamb_scaling
        
        lamb=np.maximum(lamb_lower,lamb)

        self.gridfactor=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0','lambda','r','phi']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001, 0.001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]
        
        self.workingpars_optflag=[True for x in self.workingpars]
        if( 'fix_gamma' in self.options ):
            if(self.options['fix_gamma']==True):
                self.workingpars_optflag[8]=False

        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

#TODO: expose these as options at some point?
            self.ProbFactor =1.09
            self.NormProbCalc='TDist'
            
            if( self.NormProbCalc == 'Normal' ):
                sigma_base=np.std(self.yasset,ddof=1)
                mu_base=np.mean(self.yasset)
                self.cprob_base=stats.norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=stats.t.fit(self.yasset)
                self.cprob_base=stats.t.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
            else:
                print('Unknown NormProbCalc -- Handle')
        # allow for a multiplier:
            self.cprob_base*=self.ProbFactor

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        v0=theta*u0

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta

        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        phi=math.atan2(gamm,omeg)
        lamb = lamb / self.lamb_scaling

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
            self.workingpars[6]=lamb
            self.workingpars[7]=r
            self.workingpars[8]=phi
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
            self.workingpars_sim[6]=lamb
            self.workingpars_sim[7]=r
            self.workingpars_sim[8]=phi
    
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars_sim[5]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0] 
        sigma=self.workingpars_sim[1]
#        rho=self.workingpars_sim[2]
        alpha=self.workingpars_sim[3] 
        xi=self.workingpars_sim[4]
#        u0=self.workingpars_sim[5]
        lamb = self.workingpars_sim[6]
        r = self.workingpars_sim[7]
        phi = self.workingpars_sim[8]

        theta=sigma*sigma
        eta=xi*sigma

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: variance driver
# Zs[2,:,:]: jump indicator
# Zs[3,:,:]: jump size

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[2:4,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg
#        ret['u0']=u0
        ret['rep_v0']=v0


        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]
        sim_lamb = self.workingpars_sim[6]
        sim_r = self.workingpars_sim[7]
        sim_phi = self.workingpars_sim[8]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi
        ret['sim_wrk_u0']=sim_u0

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_gamm=sim_r*sim_sigma*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*sim_sigma*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg
        ret['sim_rep_v0']=sim_v0

        ret['misc_muj']=lamb*np.expm1(gamm+0.5*omeg*omeg)

        ret['misc_q']=q
#        ret['uT']=uT
        ret['misc_vT']=vT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        Nret=self.Nobs-1
        self.standardreturns=np.zeros(Nret)
        Heston_standardreturn(self.yasset,self.upath,self.dt,rho,sigma,mu,alpha,xi,self.standardreturns)
        ret['ts_standardreturns']=self.standardreturns

        return ret

    def update(self):
        super().update()

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]
   
        dt2=self.dt2

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        CondProbCalc='Limit'
        if( CondProbCalc=='Limit' ):
            coeff_dt=(mu-alpha*rho*sigma/xi)*dt2
            coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
            coeff_du = rho*sigma/xi
            self.condprob_calc=lambda yasset,u_prev,u_mid,u_this: Bates_condassetprob_limitX2(yasset,u_prev,u_mid,u_this,dt2,rho,sigma,coeff_dt,coeff_iu,coeff_du,lamb,gamm,omeg)
    
            pass
        else:
            print('Unknown Calc -- Handle')                

        return

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
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

#-------------------------------------

class Bates_grid(Heston_grid):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        self.lamb_scaling = 1000.0

        mu=0.0
        sigma=0.1
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1
        lamb = 1.0/self.lamb_scaling
        gamm = 0.0
        omeg = 0.02
        lamb_upper = 504.0
        lamb_lower = 0.01
        r_lower = 0.05
        if( len(self.series)>1 ):
            (mu,sigma,lamb,gamm,omeg)=MertonJD_calibratemoments(np.array(self.series),self.dt)
            mu = 0.0
#            print(mu,sigma,lamb,gamm,omeg)
            lamb_lower = 10/self.dt/len(self.series)

# careful needs unscaled lambda:
        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        r=np.maximum(r_lower,r)
        phi=math.atan2(gamm,omeg)

        lamb = lamb/self.lamb_scaling
        lamb_lower = lamb_lower/self.lamb_scaling
        lamb_upper=lamb_upper/self.lamb_scaling
        
        lamb=np.maximum(lamb_lower,lamb)

        self.gridfactor=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0','lambda','r','phi']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001, 0.001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]

        self.workingpars_optflag=[True for x in self.workingpars]
        self.workingpars_optflag[5]=False
        if( 'fix_gamma' in self.options ):
            if(self.options['fix_gamma']==True):
                self.workingpars_optflag[8]=False

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
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        v0=u0*theta

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta

        r=np.sqrt(lamb*(gamm*gamm+omeg*omeg))/sigma
        phi=math.atan2(gamm,omeg)
        lamb = lamb / self.lamb_scaling

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
            self.workingpars[6]=lamb
            self.workingpars[7]=r
            self.workingpars[8]=phi
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
            self.workingpars_sim[6]=lamb
            self.workingpars_sim[7]=r
            self.workingpars_sim[8]=phi

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars_sim[5]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0] 
        sigma=self.workingpars_sim[1]
#        rho=self.workingpars_sim[2]
        alpha=self.workingpars_sim[3] 
        xi=self.workingpars_sim[4]
#        u0=self.workingpars_sim[5]
        lamb = self.workingpars_sim[6]
        r = self.workingpars_sim[7]
        phi = self.workingpars_sim[8]

        theta=sigma*sigma
        eta=xi*sigma

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: variance driver
# Zs[2,:,:]: jump indicator
# Zs[3,:,:]: jump size

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[2:4,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

# already called in super?
        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg
#        ret['u0']=u0
        ret['rep_v0']=v0

        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]
        sim_lamb = self.workingpars_sim[6]
        sim_r = self.workingpars_sim[7]
        sim_phi = self.workingpars_sim[8]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi
        ret['sim_wrk_u0']=u0

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_gamm=sim_r*sim_sigma*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*sim_sigma*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg
        ret['sim_rep_v0']=sim_v0

        ret['misc_muj']=lamb*np.expm1(gamm+0.5*omeg*omeg)

        ret['misc_q']=q
#        ret['uT']=uT
        ret['misc_vT']=vT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        Nret=self.Nobs-1
        self.standardreturns=np.zeros(Nret)
        Heston_standardreturn(self.yasset,self.upath,self.dt,rho,sigma,mu,alpha,xi,self.standardreturns)
        ret['ts_standardreturns']=self.standardreturns

        return ret

    def update(self):
        super().update()

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]
 
        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        self.lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Bates_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp)
    
# calculated in super, so done 2x?      
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)


        return

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        Nret=self.Nobs-1

        lamb = lamb * self.lamb_scaling
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

#-------------------------------------


    
