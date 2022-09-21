import requests
import numpy as np
import time
import json
import jsonpickle
from datetime import datetime
import cache_managing as cm
    
class Item:
    def __init__(self,name,read_cache=True):
        self.name=name
        #read cache should be kept as True. False is passed only for testing purposes, where it does not interact with any cache objects.
        if read_cache:
            self.check_if_cached_exists()
       
    def check_if_cached_exists(self):
        #gets a cached array if it belongs to the item. otherwise it produces a request
            if self.name in cm.CacheManager.CachedArrays.saved:
                self.array=np.array(cm.CacheManager.CachedArrays.lookup(self.name))
            else:
                self.request_coordination()
    
    def request_coordination(self):
        #checks for item id, makes a request and produces an array from that request.
        self.id=self.item_id()
        self.response=self.send_request()
        self.array=self.produce_array() 
        
    def item_id(self):
        IDlist=[(['disto','distortion','black distortion earring'],11853),
                (['dawn','dawn earring'],11855),
                (['tungrad earring','tungrad ear'],11828),
                (['narc','nark','narcs','nark ear','nark earring','narc ear accesory'],11834),
                (['tungrad neck','tungrad necklace'],11629),
                (['''laytenn's power stone''','laytenn','layten','laytenns'],11630),
                (['ogre','ogre ring'],11607),
                (['lunar','lunar necklace','revived lunar necklace'],11663),
                (['crescent','crecent','ring of crescent guardian','crescent ring'],12301),
                (['eye of the ruins ring','ruins','eye of the ruins','eye'],12060),
                (['tungrad ring'],12061),
                (['ominous','ominous ring'],12068),
                (['tungrad belt'],12237),
                (['valtarra','valtarra belt','baltarra eclipsed belt'],12236),
                (['''basilisk's belt''','basilisk','basilisk belt','sychros belt'],12230),
                (['turo','turos','''turo's belt''','turo belt','turos belt'],12257)]
    
        for items, id in IDlist:
            if self.name.lower() in items:
                return id    
        raise NameError('Item name not found')
    
    @property
    def get_id(self):
        return self.id
        
    @property
    def get_array(self):
        return self.array
    
    def send_request(self):
        url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetWorldMarketSubList'
        headers = {
        "Content-Type": "application/json",
        "User-Agent": "BlackDesert"
    }
        payload = {
        "keyType": 0,
        "mainKey": self.id
    }
        response = requests.request('POST', url, json=payload, headers=headers)
        return json.loads(response.text)
        
    def produce_array(self):
        response_data=self.response['resultMsg']
        responses_list=response_data.split('|')
        nested_responses=[responselist.split('-') for responselist in responses_list if responselist !='']
        useful_responses=[response[2:] for response in nested_responses]
        response_array=np.array(useful_responses).astype(float)
        cm.CacheManager.CachedArrays.cache_array(self.name,response_array.tolist())
        return response_array
    
        
        


ItemsNames={11853:'Black Distortion Earring',
            11855:'Dawn Earring',
            11828:'Tungrad Earring',
            11834:'Narc Ear Accessory',
            11629:'Tungrad Necklace',
            11630:'''Laytenn's Power Stone''',
            11607:'Ogre Ring',
            11663:'Revived Lunar Necklace',
            12031:'Ring of Crescent Guardian',
            12060:'Eye of the Ruins Ring',
            12061:'Tungrad Ring',
            12068:'Ominous Ring',
            12237:'Tungrad Belt',
            12236:'Valtarra Eclipsed Belt',
            12230:'''Basilisk's Belt''',
            12257:'''Turo's Belt'''}



def get_history(item):
    url = 'https://eu-trade.naeu.playblackdesert.com/Trademarket/GetMarketPriceInfo'
    headers = {
    "Content-Type": "application/json",
    "User-Agent": "BlackDesert"
    }
    payload = {
    "keyType": 0,
    "mainKey": 10210,
    "subKey": 0
    }


class Price:
    def __init__(self,array,level):
        self.base=array[0][6]
        self.before=array[level][6]
        self.after=array[level+1][6]
        
class Tax:
    def __init__(self,tax):
        self.keep=1-(tax/100)  
tax=Tax(14.5)       

