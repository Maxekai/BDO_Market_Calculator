import bdorequester as rq
import failstackcalculator as fs
import pandas as pd
import numpy as np
from scipy.stats import binom
from scipy.stats import geom
import matplotlib.pyplot as plt

#example=rq.Item('disto')

def get_dataframe(item):
    df=pd.DataFrame(item.array)
    df.columns=['Enhancement','Base Price','Stock','Total Trades','Min Cap','Max Cap','Last Sale Price','Last Sale Time']
    df['Last Sale Time']=pd.to_datetime(df['Last Sale Time'], unit='s')
    return df

def get_ratio(item,level):
    array=item.array
    unenhanced_price=array[level-1][6]
    enhanced_price=array[level][6]
    return enhanced_price/unenhanced_price


class BinomialDistribution(rq.Item):
    def __init__(self,name,tries,level,failstack=None):
        super().__init__(name)
        self.n=tries
        self.level=level
        if failstack:
            self.p=fs.chance(level,failstack)
    
    def price(self,beginning=True):
        #Beginning determines if the price is for the unenchanted (true) or enchanted (false) item.
        if beginning==True:
            return self.array[self.level-1][6]
        else:
            return self.array[self.level][6]
    
    def total_price(self,beginning=True):
        return self.n*self.price(beginning)
        
    def expected_profit(self):
        success_price=self.array[self.level][6]
        expected_successes=binom.mean(self.n,self.p)
        expected_income=success_price*expected_successes
        expected_cost=self.n*self.price()
        return expected_income-expected_cost
    
    def gamble(self,seed=None):
        return int(binom.rvs(self.n, self.p, loc=0, size=1, random_state=seed))
    
    def show_distribution(self):
        fig, ax = plt.subplots(1, 1)
        mean, var, skew, kurt = binom.stats(self.n, self.p, moments='mvsk')
        x = np.arange(binom.ppf(0.01, self.n+1, self.p),
                      binom.ppf(0.99, self.n+1, self.p))
        ax.plot(x, binom.pmf(x, self.n, self.p), 'bo', ms=8, label='binom pmf')
        ax.vlines(x, 0, binom.pmf(x, self.n, self.p), colors='b', lw=5, alpha=0.5)
        plt.show()
    
    


class GeometricDistribution(rq.Item):
    def __init__(self,name,level,failstack):
        self.p=fs.chance(level,failstack)
        self.level=level
        super().__init__(name)
        
    def price(self):
        return self.array[self.level-1][6]
        
    def show_distribution(self,with_price=False):
        fig, ax = plt.subplots(1, 1)
        mean, var, skew, kurt = geom.stats(self.p, moments='mvsk')
        x = np.arange(geom.ppf(0.01, self.p),
                      geom.ppf(0.99, self.p))
        if with_price==True:
            ax.plot(x*self.price(), geom.cdf(x, self.p), 'bo', ms=5, label='geom pmf')
        else:
            ax.plot(x, geom.cdf(x, self.p), 'bo', ms=5, label='geom pmf')
        plt.show()   
    
    def expected_value(self):
        price=self.price()
        expected_tries=geom.mean(self.p)
        expected_cost=price*expected_tries
        return expected_cost
    
    def median(self):
        return self.price()*geom.median(self.p, loc=0)

    def conf_intervals(self):
        interval= geom.interval(0.5, self.p, loc=0)
        return [self.price()*element for element in interval]


class Price:
    def __init__(self,array,level):
        self.unenh_price=array[level][6]



class BigGambling:
    distributions=[]
    def __init__(self,name,tries,baselevel,failstack):
        self.name=name
        self.tries=tries
        self.level=baselevel+1
        self.failstack=failstack
        self.gambling()
        #starts by creating the first binomial distribution for the beginning level
        #performs gamble to check how many tries succeeded
        
    def gambling(self):
        self.distributions.append(BinomialDistribution(self.name,self.tries,self.level,self.failstack))
        self.tries=self.distributions[-1].gamble()
        print(f'Obtained {self.tries} Level {self.level} items')
        self.level+=1
        self.choice()
        
    def choice(self):
        if self.level<=5:
            print('Enter 1 to continue gambling, 0 to stop')
            decision=int(input())
            if decision==1:
                print(f'Enter Failstack for {self.tries} Level {self.level} attempts')
                self.failstack=int(input())
                self.gambling()
            
            else:
                print(f'Profit:{display(self.profit())}')
        else:
            print(f'Profit:{display(self.profit())}')
    
    def total_tries(self):
        #gets a list of all tries (to sum the amount of base tier 1 spent)
        trieslist=[distribution.n for distribution in self.distributions]
        print(sum(trieslist))
        return sum(trieslist)
    
    def profit(self):
        #calculates profit as revenue of selling fully enhanced items minus purchased base items (basepurchase) and enhancing items (materialcost)
        basepurchase=self.distributions[0].total_price()
        #produces a distribution for the materials. it is only used to calculate the price. Level 1 is used because price uses level-1, so it uses base items as material.
        materialcost=self.total_tries()*BinomialDistribution(self.name,self.tries,1).price()
        cost=basepurchase+materialcost
        print(f'Cost:{display(cost)} from Base: {display(basepurchase)} and Materials: {display(materialcost)}')
        #produces a distribution for the selling items used only to calculate its price. total price with parameter False means that its using its enhancement level, not level-1
        revenue=BinomialDistribution(self.name,self.tries,self.level-1).total_price(False)
        print(f'Revenue:{display(revenue)}')
        return revenue-cost
    
    

def display(price):
    if abs(price)>1000000000:
        return f'{price/1000000000:.3f} b'
    else:
        return f'{price/1000000:.3f} m'
    
        
        
#print(get_ratio(example,4))
#print(BinomialDistribution('disto',10,1,30).gamble(0))

#Dist=GeometricDistribution('disto',4,111).show_distribution(True)
#print(GeometricDistribution('disto',4,111).conf_intervals())
#print(GeometricDistribution('disto',4,111).median())
#print(get_dataframe(example))
#print(BinomialDistribution('disto',4,4,111).expected_profit())
BigGambling('disto',30,1,30)