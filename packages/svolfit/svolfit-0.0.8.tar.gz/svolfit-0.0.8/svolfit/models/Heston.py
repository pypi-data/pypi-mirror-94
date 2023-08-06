import numpy as np

from scipy.stats import norm
from scipy.stats import t as tdist
from scipy.special import gammaln

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.Heston_utils import stepcalc_tree,condassetprob_calc_exact,condassetprob_calc_limit_X2
from svolfit.models.Heston_utils import Heston_lncondassetprob,Heston_griddefs,Heston_pathprob,Heston_UsefulGrid,Heston_standardreturn

#---------------------------------------------

class Heston_tree(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        mu=0.0
        sigma=0.1
        if( len(self.series) > 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1
        
        self.gridfactor=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0)]

        self.workingpars_optflag=[True for x in self.workingpars]

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
                self.cprob_base=norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=tdist.fit(self.yasset)
                self.cprob_base=tdist.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
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

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta
        
        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
    
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars_sim[5]

        corrmatrix=np.array([[1.0,rho],[rho,1.0]])
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

        theta=sigma*sigma
        eta=xi*sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12
        
        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]

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
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
#        ret['u0']=u0
        ret['rep_v0']=v0


        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_u0']=sim_u0

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
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
        u0=self.workingpars[5]
        q=2.0*alpha/(xi*xi)

        dt=self.dt
        
        if( alpha*dt < 1.0e-6 ):
            self.gamm=0.5*alpha*dt*(1+0.5*alpha*dt)
            self.Vb=(xi*xi)*np.exp(-alpha*dt)*dt*(1-0.5*alpha*dt)
        else:
            self.gamm=np.expm1(alpha*dt)/2.0
            self.Vb=-xi*xi*np.expm1(-alpha*dt)*np.exp(-alpha*dt)/alpha
        if( np.isnan(self.gamm) or np.isnan(self.Vb) ):
            print('NAN ERROR: gamm,Vb')
            print(alpha,q,xi,self.gamm,self.Vb)
        
        self.delta=self.Vb/(2.0*self.gridfactor)
        
        t=np.linspace(1,self.Nobs,self.Nobs)*dt
        uj=-np.expm1(-alpha*t)+np.exp(-alpha*t)*u0
    
        deltajrat=(np.sqrt(0.25+2.0*(self.gamm+uj)/self.delta)-0.5)
        self.nj=np.array( np.ceil( np.sqrt(0.25+2.0*(self.gamm+uj)/self.delta)-np.sqrt(0.25+2.0*self.gamm/self.delta ) ) , int)
    
        self.tu0=uj+self.delta*(-self.nj*deltajrat+self.nj*(self.nj-1)/2.0)
        self.tdelta0=self.delta*(deltajrat-self.nj)
        
        maxindex = self.Nobs+np.max(self.nj)

# maxindex can depend on parameters, so have to reallocate all the time...
        self.ni_s=np.zeros(maxindex+1,dtype=int)
        self.space=np.zeros((7,maxindex+1))
        self.pi_s=np.zeros((12,maxindex+1))
        self.u_s=np.zeros((3,maxindex+1))
        self.p_s=np.zeros((2,maxindex+1))
        
        CondProbCalc='Limit'
        if( CondProbCalc=='Limit' ):
            self.lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Heston_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
        elif( CondProbCalc=='Exact' ):
    #TODO: If you really want to use this then it needs to be cleaned up and reviewed!!
            # coeff_dt=(mu-alpha*rho*sigma/xi)*dt
            # coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
            # coeff_du = rho*sigma/xi
    
            # epsilon=alpha*dt/2.0
            # MI_f1=1.0-2.0*epsilon*epsilon/15.0+2.0*epsilon*epsilon*epsilon*epsilon/105.0
            # MI_f2=1.0-epsilon*epsilon/15.0+2.0*epsilon*epsilon*epsilon*epsilon/315.0
            # MI_f3=1.0-7.0*epsilon*epsilon/30.0+31.0*epsilon*epsilon*epsilon*epsilon/840.0
            # if( epsilon > 1.0e-4 ):
            #     MI_f1=3.0*(np.cosh(epsilon)/(epsilon*np.sinh(epsilon))-1.0/(np.sinh(epsilon)**2))/2.0
            #     MI_f2=3.0*(epsilon*np.cosh(epsilon)/np.sinh(epsilon)-1.0)/(epsilon**2)
            #     MI_f3=3.0*(epsilon*np.cosh(epsilon)/np.sinh(epsilon)-1.0)/(epsilon*np.sinh(epsilon))
    
            # self.condprob_calc=lambda yasset,u_prev,u_this: condassetprob_calc_exact(yasset,u_prev,u_this,dt,alpha,rho,sigma,xi,q,MI_f1,MI_f2,MI_f3,coeff_dt,coeff_iu,coeff_du)
    
            pass
        else:
            print('Unknown Calc -- Handle')                
        

        return

    def calculate(self,OptRun=True):
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        q=2.0*alpha/(xi*xi)

        dt=self.dt
        nj=self.nj
        Nret=self.Nobs-1
        delta=self.delta
        Vb=self.Vb
        gamm=self.gamm
        tu0=self.tu0
        tdelta0=self.tdelta0
        yasset=self.yasset
        cprob_base=self.cprob_base

        ni_s=self.ni_s    
        space=self.space
        pi_s=self.pi_s
        u_s=self.u_s
        p_s=self.p_s
        
        iseven=True
        u_prev = u_s[0,0:1]
        u_prev[:] = u0
        if( OptRun==False ):
            ulist=[]
            ulist.append(u_prev.copy())
            vplist=[]
            vilist=[]
            pv_prev=[1]
    
        p_prev = p_s[0,0:1]
        p_prev[:]=1.0
        n_min=int(nj[0])
        n_max=int(nj[0])
        for cc in range(0,Nret): 
            n_top=n_max-n_min+1
    
            ni=ni_s[0:n_top]
    
            pi_up=pi_s[0,0:n_top]
            pi_dn=pi_s[1,0:n_top]
            pi_mid=pi_s[2,0:n_top]
    
            ptmp_up=pi_s[3,0:n_top]
            ptmp_dn=pi_s[4,0:n_top]
            ptmp_mid=pi_s[5,0:n_top]
    
            condprob_up=pi_s[6,0:n_top]
            condprob_dn=pi_s[7,0:n_top]
            condprob_mid=pi_s[8,0:n_top]
    
            if( iseven == True ):
                u_prev = u_s[0,0:n_top]
                u_this = u_s[1,:]
                p_prev = p_s[0,0:n_top]
            else:
                u_prev = u_s[1,0:n_top]
                u_this = u_s[0,:]
                p_prev = p_s[1,0:n_top]
    
            (n_min,n_max,n_top2)=stepcalc_tree(alpha,dt,delta,Vb,gamm,tu0[cc],tdelta0[cc],u_prev,space,ni,u_this,pi_mid,pi_up,pi_dn)
            
            if( iseven == True ):
                u_this = u_s[1,0:n_top2]
                p_this = p_s[1,0:n_top2]
                iseven=False
            else:
                u_this = u_s[0,0:n_top2]
                p_this = p_s[0,0:n_top2]
                iseven=True
 
# recall the s=reshape makes the array Nobs=1 x Ngrid so that the same function call will work
# I believe without making a copy of memory on the array...
            self.lncondprob_calc(yasset[[cc]],u_prev,u_this[ni-n_min]  ,np.reshape(condprob_mid,(1,n_top)))
            self.lncondprob_calc(yasset[[cc]],u_prev,u_this[ni-n_min-1],np.reshape(condprob_dn ,(1,n_top)))
            self.lncondprob_calc(yasset[[cc]],u_prev,u_this[ni-n_min+1],np.reshape(condprob_up ,(1,n_top)))
            condprob_mid[:]=np.exp(condprob_mid)
            condprob_dn[:]=np.exp(condprob_dn)
            condprob_up[:]=np.exp(condprob_up)

            p_this[:]=np.zeros(n_top2)
            if( OptRun==False ):
                vp=np.zeros(n_top2)
                vi=-np.ones(n_top2,dtype=int)
                pv_this=np.zeros(n_top2)
    
            ptmp_mid[:]=p_prev*pi_mid*condprob_mid/cprob_base[cc]
            ptmp_dn[:]=p_prev*pi_dn*condprob_dn/cprob_base[cc]
            ptmp_up[:]=p_prev*pi_up*condprob_up/cprob_base[cc]
    
    #
    # This allows us to avoid the for loop at the expense of a 'unique' call per loop.
    # is slower for small Nobs, but significantly faster as the number of observations becomes larger... (~50%)
    #
    # note the order of additions is different, so the results are not exactly the same... ~1e-15 diff
    #
            ndunq = np.unique(ni-n_min) 
            R_up=pi_s[9,0:len(ndunq)]
            R_dn=pi_s[10,0:len(ndunq)]
            R_mid=pi_s[11,0:len(ndunq)]
    
            chgs = np.r_[0,np.where(np.diff(ni-n_min))[0]+1]
    
            R_mid[:]=np.add.reduceat(ptmp_mid,chgs, axis=0)
            R_dn[:]=np.add.reduceat(ptmp_dn,chgs, axis=0)
            R_up[:]=np.add.reduceat(ptmp_up,chgs, axis=0)
    
            p_this[ndunq] += R_mid
            p_this[ndunq+1] += R_up
            p_this[ndunq-1] += R_dn
    
    # recall: this loop is here because python doesn't do anything particularly intelligent with 
    # repeated indices: A[0,0,1] +=? and there will typically be a repeated index or two in ni-n_min... 
    #        for c2 in range(0,len(ni)):
    #            p_this[ni[c2]-n_min]+=ptmp_mid[c2]
    #            p_this[ni[c2]-n_min-1]+=ptmp_dn[c2]
    #            p_this[ni[c2]-n_min+1]+=ptmp_up[c2]
    
            if( OptRun==False ):
                for c2 in range(0,len(ni)):
                    if(ptmp_mid[c2]>=vp[ni[c2]-n_min]):
                        vp[ni[c2]-n_min]=ptmp_mid[c2]
                        vi[ni[c2]-n_min]=c2
                    if(ptmp_dn[c2]>=vp[ni[c2]-n_min-1]):
                        vp[ni[c2]-n_min-1]=ptmp_dn[c2]
                        vi[ni[c2]-n_min-1]=c2
                    if(ptmp_up[c2]>=vp[ni[c2]-n_min+1]):
                        vp[ni[c2]-n_min+1]=ptmp_up[c2]
                        vi[ni[c2]-n_min+1]=c2
    #                print('xxx')
                    pv_this[ni[c2]-n_min]+=pv_prev[c2]*pi_mid[c2]
                    pv_this[ni[c2]-n_min-1]+=pv_prev[c2]*pi_dn[c2]
                    pv_this[ni[c2]-n_min+1]+=pv_prev[c2]*pi_up[c2]
    
    # this just replaces underflow nan's with zero
            np.nan_to_num(p_this,copy=False)
    #        print(np.sum(p_this),p_this)
    #        print(np.sum(p_this))
            
    #        u_prev[0:n_top2]=u_this[0:n_top2]
            if( OptRun==False ):
                ulist.append(u_this.copy())
                vplist.append(vp)
                vilist.append(vi)
                pv_prev=pv_this
    #        p_prev=p_this
    #        p_prev[0:n_top2]=p_this[0:n_top2]
            pass
            
        value = np.sum(p_this)
        if( (value <= 0.0) or (np.isnan(value)==True) ):
            value = -np.inf
        else:
            value=np.log(value)
    
        fitU0=True
        if( fitU0 == True ): 
            value += (q-1.0)*np.log(u0)-q*u0+q*np.log(q)-gammaln(q)
            dt0=(np.sqrt(0.25+2.0*(gamm+u0)/delta)-0.5)
            value+=0.5*np.log(dt0*(dt0+1.0))+np.log(delta)                
        
    #    print(value,mu,sigma,rho,u0,q,alpha,xi,np.max(nj),np.min(nj),delta)
    #    print(value)
    
    
        if( OptRun==False ):
            upath=np.zeros(Nret+1)
    # prediction of the variance at end of path:    
            entry_current=np.argmax(p_this)
            uT=u_this[entry_current]
            upath[Nret]=uT
            for cpath in range (Nret-1,-1,-1):        
    #            print(cpath)
                entry_current=vilist[cpath][entry_current]
                upath[cpath]=ulist[cpath][entry_current]
    #        print(uT)
#            n0=nj[0]
#            nT=nj[Nret-1]
            self.upath=upath

        self.objective_value = -value
        self.current=True
        self.numfunevals+=1
    
        return

    def variancepath(self):
        self.calculate(False)
        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

        status = 'Success'
        message = 'No issues.'        
        return (status,message)

#---------------------------------------------

class Heston_treeX2(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        mu=0.0
        sigma=0.1
        if( len(self.series) > 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1
        
        self.gridfactor=0.4
        self.dt2 = self.dt/2.0

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 4.5),(0.1,3.0)]

        self.workingpars_optflag=[True for x in self.workingpars]

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
                self.cprob_base=norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=tdist.fit(self.yasset)
                self.cprob_base=tdist.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
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

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta
        
        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
            
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars_sim[5]

        corrmatrix=np.array([[1.0,rho],[rho,1.0]])
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

        theta=sigma*sigma
        eta=xi*sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12
        
        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]

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
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
#        ret['u0']=u0
        ret['rep_v0']=v0


        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_u0']=sim_u0

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
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
        u0=self.workingpars[5]
        q=2.0*alpha/(xi*xi)

#            dt=self.dt
        dt2=self.dt2
        
        if( alpha*dt2 < 1.0e-6 ):
            self.gamm=0.5*alpha*dt2*(1+0.5*alpha*dt2)
            self.Vb=(xi*xi)*np.exp(-alpha*dt2)*dt2*(1-0.5*alpha*dt2)
        else:
            self.gamm=np.expm1(alpha*dt2)/2.0
            self.Vb=-xi*xi*np.expm1(-alpha*dt2)*np.exp(-alpha*dt2)/alpha
        if( np.isnan(self.gamm) or np.isnan(self.Vb) ):
            print('NAN ERROR: gamm,Vb')
            print(alpha,q,xi,self.gamm,self.Vb)
        
        self.delta=self.Vb/(2.0*self.gridfactor)
        
        t=np.linspace(1,2*self.Nobs,2*self.Nobs)*dt2
        uj=-np.expm1(-alpha*t)+np.exp(-alpha*t)*u0
    
        deltajrat=(np.sqrt(0.25+2.0*(self.gamm+uj)/self.delta)-0.5)
        self.nj=np.array( np.ceil( np.sqrt(0.25+2.0*(self.gamm+uj)/self.delta)-np.sqrt(0.25+2.0*self.gamm/self.delta ) ) , int)
    
        self.tu0=uj+self.delta*(-self.nj*deltajrat+self.nj*(self.nj-1)/2.0)
        self.tdelta0=self.delta*(deltajrat-self.nj)
        
        maxindex = 2*self.Nobs+np.max(self.nj)

# maxindex can depend on parameters, so have to reallocate all the time...
        self.ni_s=np.zeros((2,maxindex+1),dtype=int)
        self.space=np.zeros((7,maxindex+1))
        self.pi_s=np.zeros((27,maxindex+1))
        self.u_s=np.zeros((3,maxindex+1))
        self.p_s=np.zeros((2,maxindex+1))
        
        CondProbCalc='Limit'
        if( CondProbCalc=='Limit' ):
            coeff_dt=(mu-alpha*rho*sigma/xi)*dt2
            coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
            coeff_du = rho*sigma/xi
            self.condprob_calc=lambda yasset,u_prev,u_mid,u_this: condassetprob_calc_limit_X2(yasset,u_prev,u_mid,u_this,dt2,rho,sigma,coeff_dt,coeff_iu,coeff_du)
        elif( CondProbCalc=='Exact' ):
    #TODO: If you really want to use this then it needs to be cleaned up and reviewed!!
    
            pass
        else:
            print('Unknown Calc -- Handle')                
            
        return

    def calculate(self,OptRun=True):
        
#        mu=self.workingpars[0] 
#        sigma=self.workingpars[1]
#        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        q=2.0*alpha/(xi*xi)
        
#        dt=self.dt
        dt2=self.dt2
        nj=self.nj
        Nret=self.Nobs-1
        delta=self.delta
        Vb=self.Vb
        gamm=self.gamm
        tu0=self.tu0
        tdelta0=self.tdelta0
        yasset=self.yasset
        cprob_base=self.cprob_base

        ni_s=self.ni_s    
        space=self.space
        pi_s=self.pi_s
        u_s=self.u_s
        p_s=self.p_s
        
        iseven=True
        u_prev = u_s[0,0:1]
        u_prev[:] = u0
        if( OptRun==False ):
            ulist=[]
            ulist.append(u_prev.copy())
            vplist=[]
            vilist=[]
            pv_prev=[1]
    
        p_prev = p_s[0,0:1]
        p_prev[:]=1.0
        n2_min=int(nj[0])
        n2_max=int(nj[0])
        n2_top=n2_max-n2_min+1
        for cc in range(0,Nret): 
    
            ni1=ni_s[0,0:n2_top]
    
            pi1_up=pi_s[0,0:n2_top]
            pi1_dn=pi_s[1,0:n2_top]
            pi1_mid=pi_s[2,0:n2_top]
    
            ptmp_up_up=pi_s[9,0:n2_top]
            ptmp_up_dn=pi_s[10,0:n2_top]
            ptmp_up_mid=pi_s[11,0:n2_top]
            ptmp_dn_up=pi_s[12,0:n2_top]
            ptmp_dn_dn=pi_s[13,0:n2_top]
            ptmp_dn_mid=pi_s[14,0:n2_top]
            ptmp_mid_up=pi_s[15,0:n2_top]
            ptmp_mid_dn=pi_s[16,0:n2_top]
            ptmp_mid_mid=pi_s[17,0:n2_top]
    
            condprob_up_up=pi_s[18,0:n2_top]
            condprob_up_dn=pi_s[19,0:n2_top]
            condprob_up_mid=pi_s[20,0:n2_top]
            condprob_mid_up=pi_s[21,0:n2_top]
            condprob_mid_dn=pi_s[22,0:n2_top]
            condprob_mid_mid=pi_s[23,0:n2_top]
            condprob_dn_up=pi_s[24,0:n2_top]
            condprob_dn_dn=pi_s[25,0:n2_top]
            condprob_dn_mid=pi_s[26,0:n2_top]
    
            if( iseven == True ):
                u_prev = u_s[0,0:n2_top]
                u_this = u_s[1,:]
                u_mid = u_s[2,:]
                p_prev = p_s[0,0:n2_top]
            else:
                u_prev = u_s[1,0:n2_top]
                u_this = u_s[0,:]
                u_mid = u_s[2,:]
                p_prev = p_s[1,0:n2_top]
     
    #        print(1,cc,u0,u_prev)
            (n1_min,n1_max,n1_top)=stepcalc_tree(alpha,dt2,delta,Vb,gamm,tu0[2*cc],tdelta0[2*cc],u_prev,space,ni1,u_mid,pi1_mid,pi1_up,pi1_dn)
    
            if( iseven == True ):
                u_mid = u_s[2,0:n1_top]
            else:
                u_mid = u_s[2,0:n1_top]
    
            ni2=ni_s[1,0:n1_top]
    
            pi2_up=pi_s[3,0:n1_top]
            pi2_dn=pi_s[4,0:n1_top]
            pi2_mid=pi_s[5,0:n1_top]
    
    #        print(2,cc,u0,u_prev)
            (n2_min,n2_max,n2_top)=stepcalc_tree(alpha,dt2,delta,Vb,gamm,tu0[2*cc+1],tdelta0[2*cc+1],u_mid,space,ni2,u_this,pi2_mid,pi2_up,pi2_dn)
    
            if( iseven == True ):
                u_this = u_s[1,0:n2_top]
                p_this = p_s[1,0:n2_top]
                iseven=False
            else:
                u_this = u_s[0,0:n2_top]
                p_this = p_s[0,0:n2_top]
                iseven=True
    
            condprob_up_mid[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min+1],u_this[ni2[ni1-n1_min+1]-n2_min])
            condprob_up_dn[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min+1],u_this[ni2[ni1-n1_min+1]-n2_min-1])
            condprob_up_up[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min+1],u_this[ni2[ni1-n1_min+1]-n2_min+1])
    
            condprob_mid_mid[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min],u_this[ni2[ni1-n1_min]-n2_min])
            condprob_mid_dn[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min],u_this[ni2[ni1-n1_min]-n2_min-1])
            condprob_mid_up[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min],u_this[ni2[ni1-n1_min]-n2_min+1])
    
            condprob_dn_mid[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min-1],u_this[ni2[ni1-n1_min-1]-n2_min])
            condprob_dn_dn[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min-1],u_this[ni2[ni1-n1_min-1]-n2_min-1])
            condprob_dn_up[:]=self.condprob_calc(yasset[[cc]],u_prev,u_mid[ni1-n1_min-1],u_this[ni2[ni1-n1_min-1]-n2_min+1])
    
            p_this[:]=np.zeros(n2_top)
            if( OptRun==False ):
                vp=np.zeros(n2_top)
                vi=-np.ones(n2_top,dtype=int)
                pv_this=np.zeros(n2_top)
    
            ptmp_up_mid[:]=p_prev*pi1_up*pi2_mid[ni1-n1_min+1]*condprob_up_mid/cprob_base[cc]
            ptmp_up_dn[:]=p_prev*pi1_up*pi2_dn[ni1-n1_min+1]*condprob_up_dn/cprob_base[cc]
            ptmp_up_up[:]=p_prev*pi1_up*pi2_up[ni1-n1_min+1]*condprob_up_up/cprob_base[cc]
    
            ptmp_dn_mid[:]=p_prev*pi1_dn*pi2_mid[ni1-n1_min]*condprob_dn_mid/cprob_base[cc]
            ptmp_dn_dn[:]=p_prev*pi1_dn*pi2_dn[ni1-n1_min]*condprob_dn_dn/cprob_base[cc]
            ptmp_dn_up[:]=p_prev*pi1_dn*pi2_up[ni1-n1_min]*condprob_dn_up/cprob_base[cc]
    
            ptmp_mid_mid[:]=p_prev*pi1_mid*pi2_mid[ni1-n1_min-1]*condprob_mid_mid/cprob_base[cc]
            ptmp_mid_dn[:]=p_prev*pi1_mid*pi2_dn[ni1-n1_min-1]*condprob_mid_dn/cprob_base[cc]
            ptmp_mid_up[:]=p_prev*pi1_mid*pi2_up[ni1-n1_min-1]*condprob_mid_up/cprob_base[cc]
    
    #
    # pretty significant reduction to remove the for loops, despite the ugliness...
    #
    #
            ndunq = np.unique(ni2[ni1-n1_min]-n2_min) 
            R_up=pi_s[6,0:len(ndunq)]
            R_dn=pi_s[7,0:len(ndunq)]
            R_mid=pi_s[8,0:len(ndunq)]
            chgs = np.r_[0,np.where(np.diff(ni2[ni1-n1_min]-n2_min))[0]+1]
            R_mid[:]=np.add.reduceat(ptmp_mid_mid,chgs, axis=0)
            R_dn[:]=np.add.reduceat(ptmp_mid_dn,chgs, axis=0)
            R_up[:]=np.add.reduceat(ptmp_mid_up,chgs, axis=0)
            p_this[ndunq] += R_mid
            p_this[ndunq+1] += R_up
            p_this[ndunq-1] += R_dn
    
            ndunq = np.unique(ni2[ni1-n1_min+1]-n2_min) 
            R_up=pi_s[6,0:len(ndunq)]
            R_dn=pi_s[7,0:len(ndunq)]
            R_mid=pi_s[8,0:len(ndunq)]
            chgs = np.r_[0,np.where(np.diff(ni2[ni1-n1_min+1]-n2_min))[0]+1]
            R_mid[:]=np.add.reduceat(ptmp_up_mid,chgs, axis=0)
            R_dn[:]=np.add.reduceat(ptmp_up_dn,chgs, axis=0)
            R_up[:]=np.add.reduceat(ptmp_up_up,chgs, axis=0)
            p_this[ndunq] += R_mid
            p_this[ndunq+1] += R_up
            p_this[ndunq-1] += R_dn
    
            ndunq = np.unique(ni2[ni1-n1_min-1]-n2_min) 
            R_up=pi_s[6,0:len(ndunq)]
            R_dn=pi_s[7,0:len(ndunq)]
            R_mid=pi_s[8,0:len(ndunq)]
            chgs = np.r_[0,np.where(np.diff(ni2[ni1-n1_min-1]-n2_min))[0]+1]
            R_mid[:]=np.add.reduceat(ptmp_dn_mid,chgs, axis=0)
            R_dn[:]=np.add.reduceat(ptmp_dn_dn,chgs, axis=0)
            R_up[:]=np.add.reduceat(ptmp_dn_up,chgs, axis=0)
            p_this[ndunq] += R_mid
            p_this[ndunq+1] += R_up
            p_this[ndunq-1] += R_dn
        
            if( OptRun==False ):
                for c2 in range(0,len(ni1)):   
    # slow, ugly...
    # but I need to first sum probabilities across all paths that have the same starting and ending node, then do the comparison...
                    junq = np.array([ ni2[ni1[c2]-n1_min+n1]-n2_min+n2 for n1 in [-1,0,1] for n2 in [-1,0,1] ])
                    junq=np.unique(junq)
                    junq_min=np.min(junq)
                    ptmptmp=np.zeros(len(junq))
                    
                    ptmptmp[ni2[ni1[c2]-n1_min+1]-n2_min+1-junq_min] += ptmp_up_up[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min+1]-n2_min+0-junq_min] += ptmp_up_mid[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min+1]-n2_min-1-junq_min] += ptmp_up_dn[c2]
    
                    ptmptmp[ni2[ni1[c2]-n1_min+0]-n2_min+1-junq_min] += ptmp_mid_up[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min+0]-n2_min+0-junq_min] += ptmp_mid_mid[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min+0]-n2_min-1-junq_min] += ptmp_mid_dn[c2]
    
                    ptmptmp[ni2[ni1[c2]-n1_min-1]-n2_min+1-junq_min] += ptmp_dn_up[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min-1]-n2_min+0-junq_min] += ptmp_dn_mid[c2]
                    ptmptmp[ni2[ni1[c2]-n1_min-1]-n2_min-1-junq_min] += ptmp_dn_dn[c2]
                    
                    for cunq in range(0,len(junq)):
                        if(ptmptmp[cunq]>=vp[junq[cunq]]):
                            vp[junq[cunq]]=ptmptmp[cunq]
                            vi[junq[cunq]]=c2
                        
                    nnn=ni1[c2]-n1_min+1
                    pv_this[ni2[nnn]-n2_min]+=pv_prev[c2]*pi1_up[c2]*pi2_mid[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min-1]+=pv_prev[c2]*pi1_up[c2]*pi2_dn[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min+1]+=pv_prev[c2]*pi1_up[c2]*pi2_up[ni1[c2]-n1_min]
         
                    nnn=ni1[c2]-n1_min
                    pv_this[ni2[nnn]-n2_min]+=pv_prev[c2]*pi1_mid[c2]*pi2_mid[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min-1]+=pv_prev[c2]*pi1_mid[c2]*pi2_dn[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min+1]+=pv_prev[c2]*pi1_mid[c2]*pi2_up[ni1[c2]-n1_min]
         
                    nnn=ni1[c2]-n1_min-1
                    pv_this[ni2[nnn]-n2_min]+=pv_prev[c2]*pi1_dn[c2]*pi2_mid[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min-1]+=pv_prev[c2]*pi1_dn[c2]*pi2_dn[ni1[c2]-n1_min]
                    pv_this[ni2[nnn]-n2_min+1]+=pv_prev[c2]*pi1_dn[c2]*pi2_up[ni1[c2]-n1_min]
    
    # this just replaces underflow nan's with zero
            np.nan_to_num(p_this,copy=False)
            
            if( OptRun==False ):
                ulist.append(u_this.copy())
                vplist.append(vp)
                vilist.append(vi)
                pv_prev=pv_this
            pass
            
        value = np.sum(p_this)
        if( (value <= 0.0) or (np.isnan(value)==True) ):
            value = -np.inf
        else:
            value=np.log(value)
    
        fitU0=True
        if( fitU0 == True ): 
            value += (q-1.0)*np.log(u0)-q*u0+q*np.log(q)-gammaln(q)
            dt0=(np.sqrt(0.25+2.0*(gamm+u0)/delta)-0.5)
            value+=0.5*np.log(dt0*(dt0+1.0))+np.log(delta)                
        
    #    print(value,mu,sigma,rho,u0,q,alpha,xi,np.max(nj),np.min(nj),delta)
    #    print(value)
    
        if( OptRun==False ):
            upath=np.zeros(Nret+1)
    # prediction of the variance at end of path:    
            entry_current=np.argmax(p_this)
            uT=u_this[entry_current]
            upath[Nret]=uT
            for cpath in range (Nret-1,-1,-1):        
    #            print(cpath)
                entry_current=vilist[cpath][entry_current]
                upath[cpath]=ulist[cpath][entry_current]
    #        print(uT)
#            n0=nj[0]
#            nT=nj[Nret-1]
            self.upath=upath

        self.objective_value = -value
        self.current=True
        self.numfunevals+=1
    
        return

    def variancepath(self):
        self.calculate(False)
        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

        status = 'Success'
        message = 'No issues.'        
        return (status,message)

#---------------------------------------------

class Heston_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        mu=0.0
        sigma=0.1
        if( len(self.series) > 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1.0
        
        self.gridfactor=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_sim=np.array([mu,sigma,rho,alpha,xi,u0])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-1.0,1.0), (0.05, 1.0), (-0.9,0.9), (alpha_min, 20.0), (0.1, 4.0),(0.1,3.0)]

        self.workingpars_optflag=[True for x in self.workingpars]
        self.workingpars_optflag[-1]=False

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

        theta=sigma*sigma
        eta=xi*sigma
        v0=u0*theta
        
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
# this sucks: the model needs a v0, but the optimiation doesn't...
            if( x=='v0' ):
                v0=pardict[x]

        sigma=np.sqrt(theta)
        xi=eta/sigma
        u0=v0/theta

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
            self.workingpars[2]=rho
            self.workingpars[3]=alpha
            self.workingpars[4]=xi
            self.workingpars[5]=u0
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma
            self.workingpars_sim[2]=rho
            self.workingpars_sim[3]=alpha
            self.workingpars_sim[4]=xi
            self.workingpars_sim[5]=u0
            
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars_sim[1]
        rho=self.workingpars_sim[2]
        u0=self.workingpars[5]

        corrmatrix=np.array([[1.0,rho],[rho,1.0]])
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
#        u0=self.workingpars[5]

        theta=sigma*sigma
        eta=xi*sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12
        
        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]

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
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta
#        ret['u0']=u0
        ret['rep_v0']=v0

        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]
        sim_rho=self.workingpars_sim[2]
        sim_alpha=self.workingpars_sim[3] 
        sim_xi=self.workingpars_sim[4]
        sim_u0=self.workingpars_sim[5]

        sim_theta=sim_sigma*sim_sigma
        sim_eta=sim_xi*sim_sigma
        sim_v0=sim_sigma*sim_sigma*sim_u0

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma
        ret['sim_wrk_rho']=sim_rho
        ret['sim_wrk_alpha']=sim_alpha
        ret['sim_wrk_xi']=sim_xi
        ret['sim_wrk_u0']=sim_u0

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_theta']=sim_theta
        ret['sim_rep_rho']=sim_rho
        ret['sim_rep_alpha']=sim_alpha
        ret['sim_rep_eta']=sim_eta
        ret['sim_rep_v0']=sim_v0

        
        Nusefulgrid=Heston_UsefulGrid(0.001,self.grid_lnp_init)
        ret['misc_Nusefulgrid']=Nusefulgrid

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

        tmp=Heston_griddefs(self.dt,alpha,xi,self.gridfactor)
        self.grid_i_lower=tmp[0]
        self.grid_i_upper=tmp[1]
        self.grid_i_map=tmp[2]
        self.grid_u_grid=tmp[3]
        self.grid_lnp_init=tmp[4]
        self.grid_pi3=tmp[5]

        self.grid_i_length=self.grid_i_upper-self.grid_i_lower + 1

        self.grid_lnp_prev = np.zeros(self.grid_i_length)
        self.grid_lnp_this = np.zeros(self.grid_i_length)

        Nret=self.Nobs-1

        self.grid_lncondprob_dn = np.zeros((Nret,self.grid_i_length))
        self.grid_lncondprob_mid = np.zeros((Nret,self.grid_i_length))
        self.grid_lncondprob_up = np.zeros((Nret,self.grid_i_length))

        self.grid_tmp_dn = np.zeros(self.grid_i_length)
        self.grid_tmp_mid = np.zeros(self.grid_i_length)
        self.grid_tmp_up = np.zeros(self.grid_i_length)

        self.lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Heston_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

# needs to be here to avoid double calculate by derive classdes:
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)
    
        lnp_init=self.grid_lnp_init
        pi3=self.grid_pi3

        lnp_prev = self.grid_lnp_prev
        lnp_this = self.grid_lnp_this

        pi_up=pi3[2,:]
        pi_mid=pi3[1,:]
        pi_dn=pi3[0,:]
    
        lncondprob_dn = self.grid_lncondprob_dn
        lncondprob_mid = self.grid_lncondprob_mid
        lncondprob_up = self.grid_lncondprob_up

        tmp_dn = self.grid_tmp_dn
        tmp_mid = self.grid_tmp_mid
        tmp_up = self.grid_tmp_up

        lnp_prev[:]=lnp_init.copy()
        Heston_pathprob(lnp_prev,lnp_this,lncondprob_dn,lncondprob_mid,lncondprob_up,pi_dn,pi_mid,pi_up,tmp_dn,tmp_mid,tmp_up)
        value = logsumexp(lnp_this)/Nret

#        print(value,value2)
#        print(mu,sigma,rho,alpha,xi)

    #    print(value)
        if( np.isnan(value) == True ):
            print(value,mu,sigma,rho,alpha,xi)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1
    
        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
    
# don'tneed to recalc on here?
# needs to be here to avoid double calculate by derived classdes:
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
        self.lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

#        i_lower=self.grid_i_lower
#        i_upper=self.grid_i_upper
        i_length=self.grid_i_length
        i_map=self.grid_i_map
        u_grid=self.grid_u_grid
        lnp_init=self.grid_lnp_init
        pi3=self.grid_pi3

        lnp_prev = self.grid_lnp_prev
        lnp_this = self.grid_lnp_this

        pi_up=pi3[2,:]
        pi_mid=pi3[1,:]
        pi_dn=pi3[0,:]
    
        lncondprob_dn = self.grid_lncondprob_dn
        lncondprob_mid = self.grid_lncondprob_mid
        lncondprob_up = self.grid_lncondprob_up
    
        tmp_dn = self.grid_tmp_dn
        tmp_mid = self.grid_tmp_mid
        tmp_up = self.grid_tmp_up

        vplist=[]
        vilist=[]

        lnp_prev[:]=lnp_init.copy()

        for cc in range(0,Nret):
   
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
    
            vp=-np.inf*np.ones(i_length)
            vi=-np.ones(i_length,dtype=int)

            for c2 in range(0,i_length):
                if(tmp_mid[c2]+np.log(pi_mid[c2])>=vp[i_map[c2]]):
                    vp[i_map[c2]]=tmp_mid[c2]+np.log(pi_mid[c2])
                    vi[i_map[c2]]=c2
                if(tmp_dn[c2]+np.log(pi_dn[c2])>=vp[i_map[c2]-1]):
                    vp[i_map[c2]-1]=tmp_dn[c2]+np.log(pi_dn[c2])
                    vi[i_map[c2]-1]=c2
                if(tmp_up[c2]+np.log(pi_up[c2])>=vp[i_map[c2]+1]):
                    vp[i_map[c2]+1]=tmp_up[c2]+np.log(pi_up[c2])
                    vi[i_map[c2]+1]=c2
            vplist.append(vp)
            vilist.append(vi)
            
#        value = logsumexp(lnp_this)/Nret
#        print(value,self.objective_value)
        
#        print(mu,sigma,rho,alpha,xi)

    #    print(value)
#        if( np.isnan(value) == True ):
#            print(value,mu,sigma,rho,alpha,xi)
#            print(value)
#            value=np.inf

# prediction of the variance at end of path:    
        upath=np.zeros(Nret+1)
#        indpath=np.zeros(Nret+1,int)
        entry_current=np.argmax(lnp_this)
#        indpath[Nret]=entry_current
        uT=u_grid[entry_current]
        upath[Nret]=uT
        for cpath in range (Nret-1,-1,-1):        
#            print(cpath)
            entry_current=vilist[cpath][entry_current]
#            indpath[cpath]=entry_current
            upath[cpath]=u_grid[entry_current]
#        print(uT)
    

# include in numfunevals even though this one will be a lot slower.
        self.numfunevals+=1
# don't change current -- it should be before here, and if this 
# fails then the grid should still be current.

        self.upath=upath

        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

        status = 'Success'
        message = 'No issues.'        
        return (status,message)
