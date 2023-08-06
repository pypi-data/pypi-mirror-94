import numpy as np

from scipy.stats import ncx2
from scipy.special import iv,ive
from scipy.special import gammaln

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance

from svolfit.models.HestonNandi_utils import Constraint_Feller,Constraint_Feller_grad

class HestonNandi_v(svol_model):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
	        (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        alpha=2.0
        xi=1.0
        u0=1.0

        self.eps=-1.0

#TODO: better if this weren't model-specific...
        for x in self.options:
            if( x=='init_rho' ):
                if( self.options[x] <= 0.0 ):
                    self.eps=-1.0
                else:
                    self.eps=1.0

        self.workingpars_names=['mu','sigma','alpha','xi','u0']
        self.workingpars=np.array([mu,sigma,alpha,xi,u0])
        self.workingpars_sim=np.array([mu,sigma,alpha,xi,u0])
        self.workingpars_diffs=[0.0001,0.0001,0.001,0.0001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (alpha_min, 20.0), (0.1, 4.0),(0.1,3.0)]

        self.workingpars_optflag=[True,True,True,True,True]

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
# this alters self.working_pars, so make sure it's called after they are init'd
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
        u0=self.workingpars[4]

        eps=self.eps

        theta=sigma*sigma
        eta=xi*sigma
        v0=theta*u0
        
        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                theta=pardict[x]
            if( x=='alpha' ):
                alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='rho' ):
                if(pardict[x]>0.0):
                    eps = +1.0
                else:
                    eps = -1.0

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta
        
        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=alpha
            self.workingpars[3]=xi
            self.workingpars[4]=u0
            self.eps=eps
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=alpha
            self.workingpars_sim[3]=xi
            self.workingpars_sim[4]=u0
        self.eps=eps
            
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        u0=self.workingpars_sim[4]

        corrmatrix=np.array([1.0])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars_sim[0] 
        sigma=self.workingpars_sim[1]
        alpha=self.workingpars_sim[2] 
        xi=self.workingpars_sim[3]

        eps = self.eps
        
        theta=sigma*sigma
        eta=xi*sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12

# same as Heston but both use the same Zs and eps multiplies eta:        
        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eps*eta*np.sqrt(dt)*Zs[0,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
        u0=self.workingpars[4]

        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['misc_rho']=self.eps
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
#        ret['u0']=u0
        ret['rep_v0']=v0

        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_alpha=self.workingpars_sim[2] 
        sim_xi=self.workingpars_sim[3]
        sim_u0=self.workingpars_sim[4]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_u0']=sim_u0

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_v0']=sim_v0


        ret['misc_q']=q
        ret['misc_vT']=vT
#        ret['uT']=uT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath
        
        return ret

    def update(self):
        super().update()

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
        u0=self.workingpars[4]

        q=2.0*alpha/(xi*xi)
 
        eps = self.eps
        dt=self.dt

        if(alpha*dt<1.0e-8):
            self.c=2.0/(xi*xi*dt)
        else:
            self.c=-q/np.expm1(-alpha*dt)

# populate the u vector here, calculate probs elsewhere:
        coeff_dt=(mu-eps*alpha*sigma/xi)*dt        
        coeff_udt=(eps*alpha*sigma/xi-sigma*sigma/2.0)*dt        
        coeff_du=eps*sigma/xi
        coeff_du+=(eps*alpha*sigma/xi-sigma*sigma/2.0)*dt/2.0
        
        self.upath[0]=u0
        utol=1.0e-4
        for cc in range(1,self.Nobs):
            self.upath[cc]=self.upath[cc-1]+(self.yasset[cc-1]-coeff_dt-coeff_udt*self.upath[cc-1])/coeff_du
            self.upath[cc]=np.maximum(utol,self.upath[cc])

        return

    def get_constraints(self):
        cons=[]

        con={}
        con['type']='ineq'
        con['fun']=lambda x: Constraint_Feller(x)
        con['jac']=lambda x: Constraint_Feller_grad(x)
       
        cons.append(con)
        
        return cons

    def calculate(self):

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
        u0=self.workingpars[4]

        q=2.0*alpha/(xi*xi)

        Nret=self.Nobs-1
        
        dt=self.dt
        c=self.c
        Nret=self.Nobs-1
        
        lnprobs=np.zeros(Nret)
        
#        lnprobs[:]=ncx2.logpdf(2.0*c*self.upath[1:Nret+1],2.0*q,2.0*c*np.exp(-alpha*dt)*self.upath[0:Nret])
#        lnprobs[:]+=np.log(2.0*c)

#        for cc in range(0,Nret):
#            if((self.upath[cc+1]<=0.0)|(self.upath[cc]<=0.0)):
#                lnprobs[cc]=-np.inf
#            else:
#                z=2.0*c*np.exp(-alpha*dt)*np.sqrt(self.upath[cc]*self.upath[cc+1])
#                lnprobs[cc]=np.log(c)-c*(self.upath[cc+1]+self.upath[cc]*np.exp(-alpha*dt))
#                lnprobs[cc]+=np.log(self.upath[cc+1]*np.exp(alpha*dt)/self.upath[cc])*(q-1.0)/2.0
#    #            lnprobs[cc]+=np.log(iv(q-1.0,z))
#                lnprobs[cc]+=z+np.log(ive(q-1.0,z))

        SIG=sigma*np.sqrt( (self.upath[0:Nret]+self.upath[1:Nret+1]+np.sqrt(self.upath[0:Nret]*self.upath[1:Nret+1]))*dt/3.0 )
#        SIG=sigma*np.sqrt( (self.upath[0:Nret]+self.upath[1:Nret+1])*dt/2.0 )
        m=mu*dt-0.5*SIG*SIG
        ZN=(self.yasset-m)/SIG
        lnprobs[:]=-0.5*ZN*ZN-0.5*np.log(2*np.pi)-0.5*np.log(SIG)

        value=np.sum(lnprobs)
 
# include probability of initial variance:
        value += (q-1.0)*np.log(u0)-q*u0+q*np.log(q)-gammaln(q)

        value/=Nret

        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,sigma,alpha,xi,u0,q,c)
        
        return
    
    def variancepath(self):
        return 
    
    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

        status = 'Success'
        message = 'No issues.'        
        return (status,message)

 
    
