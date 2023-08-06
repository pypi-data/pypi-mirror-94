import numpy as np
import pandas as pd
import os

from svolfit.models.model_factory import model_create
    
dt=1.0/252.0
FILE='test_path.csv'
SERIES='asset'

dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'data', FILE)

#TODO: need to test that test data file exists...
series=pd.read_csv(file_path)
series=series[SERIES].to_numpy()
#print(series)

#TODO: test vpath as well...?

models=[]
methods=[]
moptions=[]
values=[]

cc=0
models.append('Template')
methods.append('tree')
moptions.append({'init':{}})
values.append( -1.0 )

cc=1
models.append('GBM')
methods.append('analytic')
moptions.append({'init':{'type':'init', 'mu': 0.05, 'sigma': 0.12}})
values.append( 0.0 )
cc=2
models.append('HestonNandi')
methods.append('v')
moptions.append({'init':{'type':'init', 'mu': 0.05, 'sigma': 0.12, 'alpha': 5.0, 'eta': 0.1}})
values.append( -1.384488150809701 )
cc=3
models.append('MertonJD')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.05, 'sigma': 0.12, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( -3.82547922659836 )
cc=4
models.append('LognormalJump')
methods.append('moments')
#moptions.append({'init':{'type':'init', 'mu': 0.05, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
moptions.append({})
values.append( 0.0 )

cc=5
models.append('Heston')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2}})
values.append( -4.206827739890868 )
cc=6
models.append('Heston')
methods.append('tree')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'v0':0.015}})
values.append( 101.3305206505631 )
cc=7
models.append('Heston')
methods.append('treeX2')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'v0':0.015}})
values.append( 102.2216704171099 )

cc=8
models.append('Bates')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( -4.165946616879436 )
cc=9
models.append('Bates')
methods.append('tree')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'v0':0.015, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( 132.39798622016292 )
cc=10
models.append('Bates')
methods.append('treeX2')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'v0':0.015, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( 124.58348274713246 )

cc=11
models.append('H32')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2}})
values.append( -4.09491843483529 )

cc=12
models.append('B32')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( -4.053739373447876 )

cc=13
models.append('GARCHdiff')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2}})
values.append( -4.196547196442306 )

cc=14
models.append('GARCHjdiff')
methods.append('grid')
moptions.append({'init':{'type':'init', 'mu': 0.0, 'theta': 0.01, 'rho': -0.5, 'alpha': 5.0, 'eta': 0.2, 'lambda': 10.0, 'gamma': 0.02, 'omega': 0.03}})
values.append( -4.166733983214081 )

#for cc in range(0,len(models)):
#for cc in [3]:
#    print(models[cc]+' '+methods[cc])
#    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
#    (wpn,wp,wpb)=model.get_workingpars()
#    val=model.objective_calculate(wp)
#    print(cc,val)

# Tests:

def test_0():
    cc=0
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_1():
    cc=1
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_2():
    cc=2
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_3():
    cc=3
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_4():
    cc=4
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_5():
    cc=5
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_6():
    cc=6
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_7():
    cc=7
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_8():
    cc=8
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_9():
    cc=9
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_10():
    cc=10
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_11():
    cc=11
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_12():
    cc=12
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_13():
    cc=13
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])

def test_14():
    cc=14
    model=model_create(series, dt, models[cc], methods[cc], moptions[cc] )
    (wpn,wp,wpb)=model.get_workingpars()
    val=model.objective_calculate(wp)
    assert (val==values[cc])
