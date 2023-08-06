import numpy as np
import math
from scipy.special import ndtri

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.B32_utils import B32_lncondassetprob
from svolfit.models.MertonJD_utils import sim_NormalJumps,MertonJD_calibratemoments


#-------------------------------------

class B32_grid(Heston_grid):
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
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,r,phi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001,0.001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0),(0.1, 3.5),(0.1,3.0),(lamb_lower,lamb_upper),(r_lower,100.0),(-np.pi/2.0,np.pi/2.0)]

        self.workingpars_optflag=[True for x in self.workingpars]
        self.workingpars_optflag[5]=False

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

        theta=1.0/(sigma*sigma)
        eta=xi/sigma
        t_alpha=(alpha-xi*xi)/(sigma*sigma)
        t_theta=alpha/t_alpha
        v0=u0*theta

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                t_theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                t_alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
# this sucks: the model needs a v0, but the optimiation doesn't...
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        alpha=t_alpha*t_theta
        theta=(t_alpha+eta*eta)/alpha
        sigma=1.0/np.sqrt(theta)
        xi=eta*sigma
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

        corrmatrix=np.array([[1.0,rho,.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=8

        assetval=1.0
        varianceval=u0/(sigma*sigma)

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

        theta=1.0/(sigma*sigma)
        eta=xi/sigma

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =1.0/variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12
        
# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: variance driver
# Zs[2,:,:]: jump indicator
# Zs[3,:,:]: jump size

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5/sim_variance)*dt+np.sqrt(dt/sim_variance)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)-0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_NormalJumps(self.dt,lamb,gamm,omeg,Zs[2:4,:,:],sim_asset)

        sim_asset=np.exp(sim_asset)
        sim_variance=1.0/sim_variance
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
        
        u0=np.maximum(1.0e-12,self.upath[0])
        uT=self.upath[self.Nobs-1]

# note 1/u:
        v0=sigma*sigma/u0
        vT=sigma*sigma/uT
    
        vpath=sigma*sigma/self.upath

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
        sim_v0=sim_sigma*sim_sigma/sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_u0']=sim_u0
        ret['sim_wrk_lambda']=sim_lamb
        ret['sim_wrk_r']=sim_r
        ret['sim_wrk_phi']=sim_phi

        sim_lamb = sim_lamb * self.lamb_scaling
        sim_gamm=sim_r*sim_sigma*np.sin(sim_phi)/np.sqrt(sim_lamb)
        sim_omeg=sim_r*sim_sigma*np.cos(sim_phi)/np.sqrt(sim_lamb)

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_v0']=sim_v0
        ret['sim_rep_lambda']=sim_lamb
        ret['sim_rep_gamma']=sim_gamm
        ret['sim_rep_omega']=sim_omeg

        ret['misc_muj']=lamb*np.expm1(gamm+0.5*omeg*omeg)

        ret['misc_q']=q
#        ret['uT']=uT
        ret['misc_vT']=vT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret

    def update(self):
        super().update()
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
#        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        r = self.workingpars[7]
        phi = self.workingpars[8]

        lamb = lamb * self.lamb_scaling
        gamm=r*sigma*np.sin(phi)/np.sqrt(lamb)
        omeg=r*sigma*np.cos(phi)/np.sqrt(lamb)

        self.lncondprob_calc=lambda yasset,u_prev,u_this,lncp: B32_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp)
    
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
#        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return


#-------------------------------------


    
