import numpy as np

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.model_utils import meanvariance

from svolfit.models.Heston_GBM_utils import Heston_GBM_lncondassetprob

#-------------------------------------

class Heston_GBM_tree(Heston_tree):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        
# override/extend Heston defs
        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.workingpars_names=['rho0','phi']
        self.workingpars=np.array([rho0,phi])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [rho0, phi]
        self.workingpars_bounds=[(-0.99,0.99),(-np.pi+1.0e-4,np.pi-1.0e-4)]

        self.workingpars_optflag=[True,True]

        if 'init' in options:
            self.initpars_reporting(options['init'])
        
        return

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]
    
        rho=self.HestonPars[2]
        psi=np.arcsin(rho)
        sol_rho_a=sol_rho0*np.sin(sol_phi+psi)
        sol_rho_v=sol_rho0*np.cos(sol_phi)

        ret['rho_a']=sol_rho_a
        ret['rho_v']=sol_rho_v

        return ret

    def update(self):
        super().update()
        
        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]

        mu=self.Hestonpars[0] 
        sigma=self.Hestonpars[1]
        rho=self.Hestonpars[2]
        alpha=self.Hestonpars[3] 
        xi=self.Hestonpars[4]

        lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Heston_GBM_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
    
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return

#-------------------------------------

class Heston_GBM_treeX2(Heston_treeX2):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        
# override/extend Heston defs
        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.workingpars_names=['rho0','phi']
        self.workingpars=np.array([rho0,phi])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [rho0, phi]
        self.workingpars_bounds=[(-0.99,0.99),(-np.pi+1.0e-4,np.pi-1.0e-4)]
        
        self.workingpars_optflag=[True,True]

        return

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]
    
        rho=self.HestonPars[2]
        psi=np.arcsin(rho)
        sol_rho_a=sol_rho0*np.sin(sol_phi+psi)
        sol_rho_v=sol_rho0*np.cos(sol_phi)

        ret['rho_a']=sol_rho_a
        ret['rho_v']=sol_rho_v

        return ret

    def update(self):
        super().update()

        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]

        mu=self.Hestonpars[0] 
        sigma=self.Hestonpars[1]
        rho=self.Hestonpars[2]
        alpha=self.Hestonpars[3] 
        xi=self.Hestonpars[4]

        lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Heston_GBM_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
    
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return

#-------------------------------------

class Heston_GBM_grid(Heston_grid):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)

# override/extend Heston defs
        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.workingpars_names=['rho0','phi']
        self.workingpars=np.array([rho0,phi])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [rho0, phi]
        self.workingpars_bounds=[(-0.99,0.99),(-np.pi+1.0e-4,np.pi-1.0e-4)]

        self.workingpars_optflag=[True,True]
        
        return

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]
    
        rho=self.HestonPars[2]
        psi=np.arcsin(rho)
        sol_rho_a=sol_rho0*np.sin(sol_phi+psi)
        sol_rho_v=sol_rho0*np.cos(sol_phi)

        ret['rho_a']=sol_rho_a
        ret['rho_v']=sol_rho_v

        return ret

    def update(self):
        super().update()

        sol_rho0=self.workingpars[0]
        sol_phi=self.workingpars[1]

        mu=self.Hestonpars[0] 
        sigma=self.Hestonpars[1]
        rho=self.Hestonpars[2]
        alpha=self.Hestonpars[3] 
        xi=self.Hestonpars[4]

        lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Heston_GBM_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
    
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
        lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return


#-------------------------------------


    