import pytest
import pytest_mock
import bdorequester
import time
from requests_mock.mocker import Mocker
import requests
import cache_managing as cm
import numpy as np

@pytest.fixture(autouse=True)
def mock_request(mocker):
    mocker.patch(
        'bdorequester.Item.send_request',
        return_value={"resultCode":0,"resultMsg":"11853-0-0-319000000-0-855072-11400000-342000000-342000000-1659167525|11853-1-1-950000000-26-57821-34100000-1020000000-1010000000-1659156482|11853-2-2-2850000000-11-52252-102000000-3060000000-3060000000-1659154427|11853-3-3-7950000000-15-30072-284000000-8500000000-8150000000-1659165016|11853-4-4-26900000000-20-20374-1360000000-40800000000-26900000000-1659166978|11853-5-5-166000000000-1-524-2730000000-200000000000-162000000000-1659125442|"})
    yield
    with open('BDO_Market/cache.json', 'w'):
        pass
def test_get_id():
    #checks get id system
    result = bdorequester.Item('disto').item_id()
    assert result==11853
        
def test_get_id2():
    result = bdorequester.Item('''basilisk's belt''',read_cache=False).item_id()
    assert result==12230
    
def test_get_id3():
    result = bdorequester.Item('ominous',read_cache=False).item_id()
    assert result==12068
        
def test_get_id4():
    result = bdorequester.Item('dawn',read_cache=False).item_id()
    assert result==11855
    
def test_produce_array1():
    #checks if the first column of the array is the enhancing level
    result = bdorequester.Item('disto').get_array[3,0]
    assert result==3
    
def test_cache_array():
    #tests if requests are properly cached
    data=bdorequester.Item('disto').get_array
    cached= cm.CacheManager.CachedArrays.saved['disto']
    
    assert data.all()==np.array(cached).all()

def test_cache_times():
    #tests if request caching times work properly
    timed=time.time()
    cached_time= cm.CacheManager.CachedArrays.times['disto']
    assert cached_time-timed<5
    
def test_cache_read():
    cache=cm.CacheLoader