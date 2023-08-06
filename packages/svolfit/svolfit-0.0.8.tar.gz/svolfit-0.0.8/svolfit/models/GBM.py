import numpy as np

from svolfit.models.svol_model import svol_model

from svolfit.models.GBM_utils import GBM_lncondassetprob,GBM_meanvariance


#---------------------------------------------

class GBM_analytic(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=GBM_meanvariance(np.array(self.series),self.dt)

        self.workingpars_names=['mu','sigma']
        self.workingpars=np.array([mu,sigma])
        self.workingpars_sim=np.array([mu,sigma])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-10.0,10.0), (0.0, 10.0)]

        self.workingpars_optflag=[True,True]

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

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='sigma' ):
                sigma=pardict[x]

        if( pardict['type']=='init' ):
            pass
# prevent overwriting of calibrated parameters
#            self.workingpars[0]=mu
#            self.workingpars[1]=sigma
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        corrmatrix=np.array([1.0])
        Nperstep=1

        sigma=self.workingpars_sim[1]

        assetval=1.0
        varianceval=sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep

    def sim_step(self,asset,variance,Zs):

        mu=self.workingpars_sim[0]
        sigma=self.workingpars_sim[1]

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       

        
        dt=self.dt/Nperstep
        for cs in range(0,Nperstep):
            sim_asset+=(mu-sigma*sigma/2.0)*dt+sigma*np.sqrt(dt)*Zs[0,cs,:]

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance


    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

        theta=sigma*sigma

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_sigma']=sigma

        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]

#        sim_theta=sim_sigma*sim_sigma
#        sim_v0=sim_sigma*sim_sigma

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_sigma']=sim_sigma


        ret['misc_theta']=theta
#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_v0']=v0
        ret['misc_vT']=vT

        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret
    
    def update(self):
        super().update()

#        mu=self.workingpars[0] 
#        sigma=self.workingpars[1]
            
        return


    def calculate(self):
   
#        mu=self.workingpars[0] 
#        sigma=self.workingpars[1]

        value = 0.0
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,sigma)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.ones(Nret+1)

        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

#TODO: std errors on mean?
        status='Success'
        message='No issues.'
                   
        return (status,message)



#---------------------------------------------

class GBM_optimize(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=GBM_meanvariance(np.array(self.series),self.dt)

        self.workingpars_names=['mu','sigma']
        self.workingpars=np.array([mu,sigma])
        self.workingpars_sim=np.array([mu,sigma])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5)]

        self.workingpars_optflag=[True,True]

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

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='sigma' ):
                sigma=pardict[x]

        if( pardict['type']=='init' ):
            self.workingpars[0]=mu
            self.workingpars[1]=sigma
        else:
            self.workingpars_sim[0]=mu
            self.workingpars_sim[1]=sigma

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        corrmatrix=np.array([1.0])
        Nperstep=1

        sigma=self.workingpars_sim[1]

        assetval=1.0
        varianceval=sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep

    def sim_step(self,asset,variance,Zs):

        mu=self.workingpars_sim[0]
        sigma=self.workingpars_sim[1]

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       

        
        dt=self.dt/Nperstep
        for cs in range(0,Nperstep):
            sim_asset+=(mu-sigma*sigma/2.0)*dt+sigma*np.sqrt(dt)*Zs[0,cs,:]

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance


    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

        theta=sigma*sigma

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_sigma']=sigma

        sim_mu=self.workingpars_sim[0] 
        sim_sigma=self.workingpars_sim[1]

        sim_theta=sim_sigma*sim_sigma
        sim_v0=sim_sigma*sim_sigma

        ret['sim_wrk_mu']=sim_mu
        ret['sim_wrk_sigma']=sim_sigma

        ret['sim_rep_mu']=sim_mu
        ret['sim_rep_sigma']=sim_sigma


        ret['misc_theta']=theta
#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_v0']=v0
        ret['misc_vT']=vT

        (GBM_mu,GBM_sigma)=GBM_meanvariance(np.array(self.series),self.dt)
        ret['misc_GBM_mu']=GBM_mu
        ret['misc_GBM_sigma']=GBM_sigma


        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret
    
    def update(self):
        super().update()

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

        Nret=self.Nobs-1

        self.grid_lncondprob_mid = np.zeros((Nret,1))

        self.lncondprob_calc=lambda yasset,lncp: GBM_lncondassetprob(yasset,self.dt,mu,sigma,lncp)

            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

        self.lncondprob_calc(self.yasset,self.grid_lncondprob_mid)

        lncondprob_mid = self.grid_lncondprob_mid
#        value = logsumexp(lncondprob_mid)/Nret
        value = np.sum(lncondprob_mid)/Nret

        if( np.isnan(value) == True ):
            print(value,mu,sigma)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,sigma)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.ones(Nret+1)

        return 

    def status(self):
        if self.current != True:
            return 'Failure','Incorrect Model State.'

#TODO: std errors on mean?
        status='Success'
        message='No issues.'
                   
        return (status,message)

