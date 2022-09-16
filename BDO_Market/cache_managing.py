import json
import numpy as np
import time

class Cache:
    def __init__(self,saved={},times={}):
        self.saved=saved
        self.times=times
        
    def save_cache(self):
        with open('cache.json', 'r+') as outfile:
            json.dump(self.__dict__,outfile,indent=4)

    def cache_array(self,name,array):
        self.saved.update({name:array})
        self.times.update({name:time.time()})
        self.save_cache()
        
    def lookup(self,name):
        return self.saved[name]
    
    @property
    def saved_array(self):
        return np.array(self.saved) 
    
    @staticmethod
    def load_cache():
        #Creates a cache instance reading from the file
        f=open('cache.json','r')
        dictionary=json.load(f)
        saved=dictionary["saved"]
        f.close()
        return Cache(dictionary['saved'],dictionary["times"])

class CacheLoader:
    #Creates a Cache instance, by using a static method if there is information in the file, or creates an empty cache instance if there is not.
    def __init__(self):
            try:
                self.CachedArrays=Cache.load_cache()
            except json.decoder.JSONDecodeError:
                self.CachedArrays=Cache()  

CacheManager=CacheLoader()
