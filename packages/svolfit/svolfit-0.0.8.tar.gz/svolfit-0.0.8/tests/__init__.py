# this makes model_create available to the package without having to specifically load it
# only want to expose this one I think:
from svolfit.models.model_factory import model_create

# import here so the used can just import functions like:
#from svolfit import svolfit
#from svolfit import gridanalysis
from svolfit.svolfit import svolfit
from svolfit.gridanalysis import gridanalysis

