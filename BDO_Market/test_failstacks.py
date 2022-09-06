import pytest
import bdorequester as rq
import stonky_nerd_stuff as sn
import time
import numpy as np
import failstack_comparing as fs


def test_vectorizationfs():
    results=fs.FailstacksComparing('disto',3,105,112).failstack_producing()
    assert results.all() == np.array([0.2875,0.29,0.2925,0.295,0.2975,0.3,0.3005]).all()
    
def test_profitcalc():
    results=fs.FailstacksComparing('disto',3,128,129).calculate_profits()
    assert results.all()==np.array([[ 3.09000000e-01,3.09500000e-01],[-1.79900000e+08,-1.66450000e+08],[-1.38515450e+09,-1.37365475e+09]]).all()