import numpy as np

#TODO: probably these can be generalized by adding a tuple that 
# idicates which entries play the role of alpha and xi...
def Constraint_Feller(xvect):
    
#    mu=xvect[0] 
#    sigma=xvect[1]
    alpha=xvect[2] 
    xi=xvect[3]
#    u0=xvect[4]

    q=2.0*alpha/(xi*xi)
#    print(q)
    return q-1.0

def Constraint_Feller_grad(xvect):
    
#    mu=xvect[0] 
#    sigma=xvect[1]
    alpha=xvect[2] 
    xi=xvect[3]
#    u0=xvect[4]
  
    grad=np.zeros(len(xvect)) 
    
    grad[2]=2.0/(xi*xi)
    grad[3]=-4.0*alpha/(xi*xi*xi)
#    print(grad)
    return grad
    