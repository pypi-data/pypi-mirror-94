
from svolfit.models.Template import Template
from svolfit.models.GBM import GBM_analytic,GBM_optimize
from svolfit.models.MertonJD import MertonJD_grid
from svolfit.models.LognormalJump import LognormalJump_moments,LognormalJump_grid
from svolfit.models.HestonNandi import HestonNandi_v
from svolfit.models.Heston import Heston_grid,Heston_tree,Heston_treeX2
from svolfit.models.Bates import Bates_grid,Bates_tree,Bates_treeX2
from svolfit.models.H32 import H32_grid
from svolfit.models.B32 import B32_grid
from svolfit.models.GARCHdiff import GARCHdiff_grid
from svolfit.models.GARCHjdiff import GARCHjdiff_grid
from svolfit.models.Heston_GBM import Heston_GBM_grid,Heston_GBM_tree,Heston_GBM_treeX2

def model_create(series, dt, model, method,options):

#    print(model,method)
    if( model == 'Template' ):
        modelobj = Template(series,dt, model, method,options)
    elif( model == 'GBM' ):
        if( method == 'analytic' ):
            modelobj = GBM_analytic(series,dt, model, method,options)
        if( method == 'optimize' ):
            modelobj = GBM_optimize(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'MertonJD' ):
        if( method == 'grid' ):
            modelobj = MertonJD_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'LognormalJump' ):
        if( method == 'moments' ):
            modelobj = LognormalJump_moments(series,dt, model, method,options)
        elif( method == 'grid' ):
            modelobj = LognormalJump_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'HestonNandi' ):
        if( method == 'v' ):
            modelobj = HestonNandi_v(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'Heston' ):
        if( method == 'tree' ):
            modelobj = Heston_tree(series,dt, model, method,options)
        elif( method == 'treeX2' ):
            modelobj = Heston_treeX2(series,dt, model, method,options)
        elif( method == 'grid' ):
            modelobj = Heston_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'Bates' ):
        if( method == 'tree' ):
            modelobj = Bates_tree(series,dt, model, method,options)
        elif( method == 'treeX2' ):
            modelobj = Bates_treeX2(series,dt, model, method,options)
        elif( method == 'grid' ):
            modelobj = Bates_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'H32' ):
        if( method == 'grid' ):
            modelobj = H32_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'B32' ):
        if( method == 'grid' ):
            modelobj = B32_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'GARCHdiff' ):
        if( method == 'grid' ):
            modelobj = GARCHdiff_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'GARCHjdiff' ):
        if( method == 'grid' ):
            modelobj = GARCHjdiff_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    elif( model == 'Heston_GBM' ):
        if( method == 'tree' ):
            modelobj = Heston_GBM_tree(series,dt, model, method,options)
        elif( method == 'treeX2' ):
            modelobj = Heston_GBM_treeX2(series,dt, model, method,options)
        if( method == 'grid' ):
            modelobj = Heston_GBM_grid(series,dt, model, method,options)
        else:
            print(model+' with unknown method: '+method)
    else:
        print('Unsupported model: '+model+' with supplied method: '+method)

    return modelobj
