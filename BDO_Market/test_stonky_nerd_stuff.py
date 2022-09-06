import pytest
import bdorequester as rq
import stonky_nerd_stuff as sn
import time
import numpy as np
import pytest_mock


def test_price():
    #checks if material (before enhancing) item price is properly detected from array in binomial distribution
    result=sn.BinomialDistribution('disto',3,0,40).price.before
    assert result==342000000
def test_price2():
    #checks if material (before enhancing) item price is properly detected from array in geometric distribution
    result=sn.GeometricDistribution('disto',4,40).price.before
    assert result==26900000000
    
def test_expectected_profit():
    #checks if expected profit works
    result=sn.BinomialDistribution('disto',4,3,111).expected_profit()
    assert abs(result+1634199999)<1
    
def test_gamble():
    #checks gamble method using 0 as seed
    result= sn.BinomialDistribution('disto',10,0,30).gamble(0)
    assert result==8
        
def test_display():
    result=sn.display(3900000)
    assert result == '4 m'
        
def test2_display():
    result=sn.display(5505000000)
    assert result == '5.50 b'

def test_multigamble():
    profit, taxed= sn.ProgrammedBigGambling('disto',100,0,[18,40,60,110,250]).expected()
    assert profit == -16120898999.999954 and taxed == -29876290649.99997
    