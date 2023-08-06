import numpy as np
import pandas as pd
import os

from svolfit import svolfit
    
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
testpars=[]

cc=0
models.append('Template')
methods.append('tree')
testpars.append(
    {}
    )

cc=1
models.append('GBM')
methods.append('analytic')
testpars.append(
    {'rep_mu': 0.016652991518886752, 'rep_sigma': 0.05528406408983379, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_sigma': 0.055184064089833784, 'misc_theta': 0.0030563277422888495, 'misc_v0': 0.0030563277422888495, 'misc_vT': 0.0030563277422888495}
    )
cc=2
models.append('HestonNandi')
methods.append('v')
testpars.append(
    {'rep_mu': 0.019167046975972598, 'rep_theta': 0.006074114143482877, 'misc_rho': -1.0, 'rep_alpha': 19.999999999999993, 'rep_eta': 0.007793660336121198, 'rep_v0': 0.0060778089007671, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 3999.9999999999977, 'misc_vT': 0.006022323697355837}
    )
cc=3
models.append('MertonJD')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.017042107875148725, 'rep_sigma': 0.05129371384101479, 'rep_lambda': 15.669499422052123, 'rep_gamma': -0.0007970984983167956, 'rep_omega': 0.005046327921345223, 'misc_theta': 0.0026310450796039123, 'misc_v0': 0.0026310450796039123, 'misc_vT': 0.0026310450796039123, 'misc_V': 1.2063616734200935e-05, 'misc_S': -0.0911212008287291, 'misc_S_sig': 0.21821789023599236, 'misc_Kexc': 0.8728839915498428, 'misc_Kexc_sig': 0.8728715609439694, 'misc_JB': 25.04687080347473, 'misc_JBpvalue': 0.9999963596670173, 'sim_wrk_mu': 0.0, 'sim_wrk_s': 0.055147554615715064, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_sigma': 0.03585226169759344, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186}
    )
cc=4
models.append('LognormalJump')
methods.append('moments')
testpars.append(
    {'rep_mu': 0.01665085002139574, 'rep_lambda': 433.05308872201954, 'rep_gamma': -8.29626596868496e-05, 'rep_omega': 0.002648760960950317, 'misc_muj': -0.03440673303916978, 'misc_V': 1.2068463413068553e-05, 'misc_S': -0.07159687750650902, 'misc_S_sig': 0.21821789023599236, 'misc_Kexc': 1.7457432716327612, 'misc_Kexc_sig': 0.8728715609439694, 'misc_JB': 96.64590669066223, 'misc_JBpvalue': 1.0, 'sim_wrk_mu': 0.01665085002139574, 'sim_wrk_lambda': 433.05308872201954, 'sim_wrk_r': 0.055147554615715064, 'sim_wrk_phi': -0.03231107238565219, 'sim_rep_mu': 0.01665085002139574, 'sim_rep_lambda': 433.05308872201954, 'sim_rep_gamma': -8.561137872501338e-05, 'sim_rep_omega': 0.0026486766739240875}
    )

cc=5
models.append('Heston')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.031598578372465116, 'rep_theta': 0.0031625449896207154, 'rep_rho': 0.3783686034802998, 'rep_alpha': 3.2654036384020606, 'rep_eta': 0.03593784165348757, 'rep_v0': 0.0037384545754480065, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 15.99188281772672, 'misc_vT': 0.0029216493740896183}
    )
cc=6
models.append('Heston')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03055071749984695, 'rep_theta': 0.003132865268790383, 'rep_rho': 0.3607679427218266, 'rep_alpha': 4.233093285968648, 'rep_eta': 0.04028996174265257, 'rep_v0': 0.004270168559368956, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 16.33939015419114, 'misc_vT': 0.002914018962491343}
    )
cc=7
models.append('Heston')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.03411855836869871, 'rep_theta': 0.003156592911928414, 'rep_rho': 0.48495286998294873, 'rep_alpha': 3.3384898883577567, 'rep_eta': 0.03799206422445619, 'rep_v0': 0.004408771967202047, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.055184064089833784, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 14.602017222890494, 'misc_vT': 0.0030085719536116946}
    )

cc=8
models.append('Bates')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.02425774152860242, 'rep_theta': 0.0026643215588595293, 'rep_rho': 0.678400855417787, 'rep_alpha': 3.47228259907357, 'rep_eta': 0.02102780422738257, 'rep_lambda': 17.411653523138828, 'rep_gamma': -0.0006003489561445636, 'rep_omega': 0.004857252735251394, 'rep_v0': 0.003074427398216179, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.03585226169759344, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.153925053825784, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0012853846688327254, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.03585226169759344, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186, 'sim_rep_v0': 0.00148323757316964, 'misc_muj': -0.010244657226117409, 'misc_q': 41.84502662654438, 'misc_vT': 0.002739269694427413}
    )
cc=9
models.append('Bates')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.018664714859984468, 'rep_theta': 0.0025837605779726477, 'rep_rho': 0.6586499249235344, 'rep_alpha': 19.99999999999993, 'rep_eta': 0.027471615126273222, 'rep_lambda': 18.615318322163674, 'rep_gamma': -0.000741507679342623, 'rep_omega': 0.004914037353953643, 'rep_v0': 0.0026009397243306697, 'misc_muj': -0.01357369118429949, 'misc_V': 1.2077437314886955e-05, 'misc_S': -0.09525885049290958, 'misc_S_sig': 0.21821789023599236, 'misc_Kexc': 0.9264190267517792, 'misc_Kexc_sig': 0.8728715609439694, 'misc_JB': 28.17830003677403, 'misc_JBpvalue': 0.9999992393937455, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.03585226169759344, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0012853846688327254, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.03585226169759344, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186, 'sim_rep_v0': 0.0012853846688327254, 'misc_q': 136.94427213981749, 'misc_vT': 0.002719176942770672}
    )
cc=10
models.append('Bates')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.018119678702321604, 'rep_theta': 0.0025000000000000005, 'rep_rho': 0.8576475300735013, 'rep_alpha': 19.99999999999999, 'rep_eta': 0.024189004808894722, 'rep_lambda': 20.42050841008607, 'rep_gamma': -0.0005292549011090432, 'rep_omega': 0.004878996605444682, 'rep_v0': 0.0025079971417839224, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.03585226169759344, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0012853846688327254, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.03585226169759344, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186, 'sim_rep_v0': 0.0012853846688327254, 'misc_muj': -0.01056187072031071, 'misc_q': 170.90863212007937, 'misc_vT': 0.0026697774154610886}
    )

cc=11
models.append('H32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.035319851283899334, 'rep_theta': 0.0036560879003834364, 'rep_rho': 0.4464775392335281, 'rep_alpha': 567.7257321334562, 'rep_eta': 11.197457987805034, 'rep_v0': 0.00430649913663229, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.006090561858941766, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 328.3769291438573, 'sim_rep_eta': 18.12117350349743, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 11.055859822435137, 'misc_theta': 333.9229002023523, 'misc_eta': 11.197457987805034, 'misc_vT': 0.0029017053006185484}
    )

cc=12
models.append('B32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.025503336739110895, 'rep_theta': 0.0026108069748885547, 'rep_rho': 0.6678789860703397, 'rep_alpha': 3.308281359779547, 'rep_eta': 0.02267130122384659, 'rep_lambda': 17.413984372531505, 'rep_gamma': -0.0005657038002190354, 'rep_omega': 0.004772493616004772, 'rep_v0': 0.003166890768741878, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.03585226169759344, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0012853846688327254, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 0.03585226169759344, 'sim_rep_v0': 0.0012853846688327254, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186, 'misc_muj': -0.0096501657632628, 'misc_q': 33.60890037584837, 'misc_vT': 0.0027542353049361183}
    )

cc=13
models.append('GARCHdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03042537186423229, 'rep_theta': 0.003169068293374862, 'rep_rho': 0.32992493777168147, 'rep_alpha': 3.697982718742663, 'rep_eta': 0.7331282453343007, 'rep_v0': 0.004275322841112933, 'sim_wrk_mu': 0.016652991518886752, 'sim_wrk_sigma': 0.055184064089833784, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_rep_mu': 0.016652991518886752, 'sim_rep_theta': 0.0030452809294708827, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 1.0, 'sim_rep_v0': 0.0030452809294708827, 'misc_q': 13.760523902903858, 'misc_vT': 0.002897869549584506}
    )

cc=14
models.append('GARCHjdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.0363064629828038, 'rep_theta': 0.0025000000000000005, 'rep_rho': 0.5116918703645418, 'rep_alpha': 2.0847934791954637, 'rep_eta': 0.9858214292507342, 'rep_lambda': 504.0, 'rep_gamma': 1.0833990122822872e-05, 'rep_omega': 0.0014142920817083685, 'rep_v0': 0.004228616972072912, 'sim_wrk_mu': 0.0, 'sim_wrk_sigma': 0.03585226169759344, 'sim_wrk_rho': 0.0, 'sim_wrk_alpha': 2.0, 'sim_wrk_xi': 1.0, 'sim_wrk_u0': 1.0, 'sim_wrk_lambda': 0.144351134391109, 'sim_wrk_r': 1.1687708944803676, 'sim_wrk_phi': 0.0, 'sim_rep_mu': 0.0, 'sim_rep_theta': 0.0012853846688327254, 'sim_rep_rho': 0.0, 'sim_rep_alpha': 2.0, 'sim_rep_eta': 1.0, 'sim_rep_lambda': 144.35113439110899, 'sim_rep_gamma': 0.0, 'sim_rep_omega': 0.0034876736903755186, 'sim_rep_v0': 0.0012853846688327254, 'misc_muj': 0.005964422280901977, 'misc_q': 4.290387581490741, 'misc_vT': 0.0019242573004908752}
    )

#for cc in range(0,len(models)):
#for cc in [4,8,9,10,12,14]:
#    print(models[cc]+' '+methods[cc])
#    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
#    print(cc,status,message)
#    print(pars)


def compare(testpars,pars):

# a bit subtle -- seems a couple of these (5,8) are not so stable numerically
# 1e-8 is what i've seen as differences between math libraries, leave this here
# and look into the failures at some point...
#TODO: investigate
#    fittol=1.0e-4 # would pass...
    fittol=1.0e-5
    passed=True    
    for x in testpars:
# only compare reporting parmeters so that the testing is less sensitive to output changes
        if(x[0:4]=='rep_'): 
            if( x in pars ):
                if( np.abs(testpars[x]-pars[x]) > fittol ):
                    passed = False
            else:
                passed = False

    return passed

def test_0():
    cc=0
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert not pars

def test_1():
    cc=1
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_2():
    cc=2
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_3():
    cc=3
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_4():
    cc=4
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_5():
    cc=5
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_6():
    cc=6
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_7():
    cc=7
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_8():
    cc=8
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_9():
    cc=9
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_10():
    cc=10
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_11():
    cc=11
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_12():
    cc=12
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_13():
    cc=13
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_14():
    cc=14
    (status,message,pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)
