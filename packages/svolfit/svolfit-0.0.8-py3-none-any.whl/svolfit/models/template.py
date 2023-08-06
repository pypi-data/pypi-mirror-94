from svolfit.models.svol_model import svol_model

class template(svol_model):
    def __init__(self, series,dt, model, method):
        super().__init__(series,dt, model, method)
        
        return

    def get_reportingpars(self):
        super().get_reportingpars()
        ret={}
        return ret

    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)
        return

    def calculate(self):
        self.current=False
        return
    
    def variancepath(self):
        return 
    
    
    