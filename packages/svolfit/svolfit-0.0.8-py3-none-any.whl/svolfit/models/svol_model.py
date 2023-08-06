import numpy as np
from abc import ABC, abstractmethod

class svol_model(ABC):
    def __init__(self, series,dt, model, method,options):
        super().__init__()

        self.series=series.copy()
        self.dt=dt
        self.model=model
        self.method=method
        self.options=options.copy()

        self.Nobs=len(self.series)

        self.workingpars_names=['tmp']
        self.workingpars=np.array([0.0])
        self.workingpars_diffs=np.array([0.01])
        self.workingpars_bounds=[(0,1)]

        self.workingpars_optflag=[True]

        self.objective_value=-1.0

        self.current=False

        self.numfunevals=0
        self.numgradevals=0

# for multithreaded grad calcs
        self.gradmodels=[]
        
        self._init_d()
        
        return

# generic abstract method -- needs to be implemented by concrete class
#    @abstractmethod
#    def AccruedAmount(self):
#        accrued=self.calc()
#        return accrued

# move all derived class initing to separate method and call automatically:
    @abstractmethod
    def _init_d(self):
        return

    @abstractmethod
    def initpars_reporting(self,pardict):
        return

    @abstractmethod
    def get_structure(self):
        return '','',[],0
    
    @abstractmethod
    def sim_step(self,asset,variance,Zs):
        return [],[]

    def get_stats(self):
        stdict={}
        stdict['current']=self.current
        stdict['numfunevals']=self.numfunevals
        stdict['numgradevals']=self.numgradevals
        return stdict

#    @abstractmethod
    def get_workingpars(self):
        
        optpars_names=[]
        optpars=[]
        optpars_bounds=[]
        for cc in range(0,len(self.workingpars)):
            if(self.workingpars_optflag[cc]==True):
                optpars_names.append(self.workingpars_names[cc])
                optpars.append(self.workingpars[cc])
                optpars_bounds.append(self.workingpars_bounds[cc])
                
        return (optpars_names,optpars,optpars_bounds)

    def get_constraints(self):
        return []

    @abstractmethod
    def get_reportingpars(self):
# remember to call this...
        if( self.current == False ):
            self.update()
            self.calculate()
        return {}


    def optpars_update(self,optpars):
# this just copies pars into the model and sets the flag:
        if(np.array_equal(optpars,self.workingpars[self.workingpars_optflag])==False):
            self.current=False
            self.workingpars[self.workingpars_optflag]=optpars
        return

    def objective_calculate(self,optpars):
 
        self.optpars_update(optpars)
        if( self.current == False ):
            self.update()
            self.calculate()

#TODO: catch errors at this point?        
#        if(self.current==False):
        
        return self.objective_value

    @abstractmethod
    def update(self):
# update and calculate are always both called, but this is where any grid 
# parameters and pre-cached quantities are calculated, to keep things cleaner.
        return

    @abstractmethod
    def calculate(self):
# calculation of objective function: conditional probability of asset path.
        return
    
    def calculate_gradient(self,workingpars):

#        print('grad in') 
        NPars=len(workingpars)

        grad=np.zeros(NPars)

        value_base = self.objective_calculate(workingpars)

        for cp in range(0,NPars):    
            wp_diff=workingpars.copy()
            wp_diff[cp]+=self.workingpars_diffs[cp]
            value_diff = self.objective_calculate(wp_diff)
            grad[cp]=(value_diff-value_base)/self.workingpars_diffs[cp]

        self.numgradevals+=1

#        print(workingpars)
#        print(grad)
#        print('grad out') 

        return grad
    
    @abstractmethod
    def variancepath(self):
        return 
    
    @abstractmethod
    def status(self):
        return ('','')
    