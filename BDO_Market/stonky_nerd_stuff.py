import bdorequester as rq
import failstackcalculator as fs
import pandas as pd
import numpy as np
from scipy.stats import binom
from scipy.stats import geom
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



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

def display(price):
    if abs(price)>=100000000000:
        return f'{price/1000000000:.0f} b'
    elif abs(price)>=10000000000:
        return f'{price/1000000000:.1f} b'
    elif abs(price)>=1000000000:
        return f'{price/1000000000:.2f} b'
    else:
        return f'{price/1000000:.0f} m'
    
def plot_formatting(ax,with_price):
    plt.ylabel('Accumulated Success Chance')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    if with_price:
        ax.set_xticklabels([display(x) for x in ax.get_xticks()])
        plt.xlabel('Spent silver')
    else:
        plt.xlabel('Tries')

class BinomialDistribution(rq.Item):
    def __init__(self,name,tries,level,failstack=None):
        super().__init__(name)
        self.n=tries
        self.level=level
        if failstack:
            self.p=fs.chance(level,failstack)
        self.price=rq.Price(self.array,self.level)
    
    def total_price(self,after=False):
        if after:
            return self.n*self.price.after
        
        return self.n*self.price.before
    
    def expected(self):
        return float(binom.mean(self.n,self.p))
        
    def expected_profit(self):
        expected_successes=binom.mean(self.n,self.p)
        expected_income=self.price.after*expected_successes
        expected_cost=self.n*self.price.before+self.n*self.price.base
        return expected_income-expected_cost
    
    def gamble(self,seed=None):
        return int(binom.rvs(self.n, self.p, loc=0, size=1, random_state=seed))
    
    def show_distribution(self):
        fig, ax = plt.subplots(1, 1)
        x = np.arange(binom.ppf(0.01, self.n+1, self.p),
                      binom.ppf(0.99, self.n+1, self.p))
        ax.plot(x, binom.pmf(x, self.n, self.p))
        plt.show()


class GeometricDistribution(rq.Item):
    def __init__(self,name,level,failstack):
        self.p=fs.chance(level,failstack)
        self.level=level
        super().__init__(name)
        self.price=rq.Price(self.array,self.level)
        
    def show_distribution(self,with_price=False):
        fig, ax = plt.subplots(1, 1)
        x = np.arange(geom.ppf(0.01, self.p),
                      geom.ppf(0.99, self.p))
        ax.set_yticks(np.linspace(0,1,21).tolist())
        #Draws the plot, x axis being price or tries, y axis is accumulated chance. also draws a line at x=enhanced price
        if with_price:
            ax.plot(x*(self.price.before+self.price.base), geom.cdf(x, self.p))
            plt.axvline(x=self.price.after,linestyle='dashed',color='#808080')
        else:
            ax.plot(x, geom.cdf(x, self.p))
            plt.axvline(x=self.price.after/(self.price.before+self.price.base),linestyle='dashed',color='#808080')
        #the formatting function is called to name axes, configure ticks, etc.
        plot_formatting(ax,with_price)
        plt.show()   
    
        
    def expected_costs(self):
        expected_tries=geom.mean(self.p)
        expected_cost=(self.price.before+self.price.base)*expected_tries
        return expected_cost
    
    def expected_profit(self):
        return self.price.after-self.expected_costs()
    
    def median(self):
        return self.price.after-self.price.before*geom.median(self.p, loc=0)

    def conf_intervals(self):
        interval= geom.interval(0.5, self.p, loc=0)
        return [self.price.before*element for element in interval]

    def gamble(self,seed=None):
        return int(geom.rvs(self.p, loc=0, size=1, random_state=seed))

class BigGambling:
    distributions=[]
    def __init__(self,name,tries,baselevel,failstack):
        self.name=name
        self.tries=tries
        self.level=baselevel
        self.failstack=failstack
        #starts by creating the first binomial distribution for the beginning level
        #performs gamble to check how many tries succeeded
        
    def gambling(self):
        self.distributions.append(BinomialDistribution(self.name,self.tries,self.level,self.failstack))
        self.tries=self.distributions[-1].gamble()
        self.level+=1
        print(f'Obtained {self.tries} Level {self.level} items at {self.distributions[-1].p*100:.2f} %')
        self.choice()
        
    def choice(self):
        if self.level<=4:
            print('Enter 1 to continue gambling, 0 to stop')
            decision=int(input())
            if decision==1:
                print(f'Enter Failstack for {self.tries} Level {self.level+1} attempts')
                self.failstack=int(input())
                self.gambling()
            
            else:
                self.profit()
        else:
            self.profit()
    
    def total_tries(self):
        #gets a list of all tries (to sum the amount of base tier 1 spent)
        trieslist=[distribution.n for distribution in self.distributions]
        return sum(trieslist)
    
    def profit(self):
        #Distributions are created to calculate the price of the final items, as if we were to enhance them. Nothing else is done with them.
        basepurchase=self.distributions[0].total_price()
        materialcost=self.total_tries()*BinomialDistribution(self.name,self.tries,0).price.before
        cost=basepurchase+materialcost
        revenue=BinomialDistribution(self.name,self.tries,self.level-1).total_price(True)
        taxed=revenue*rq.tax.keep
        self.print_profit(cost,basepurchase,materialcost,revenue,taxed)
        return revenue-cost, taxed-cost
    
    def print_profit(self,cost,basepurchase,materialcost,revenue,taxed):
        profit=revenue-cost
        taxed_profit=taxed-cost
        print(f'Cost:{display(cost)} from Base: {display(basepurchase)} and Materials: {display(materialcost)}')
        print(f'Revenue:{display(revenue)} , Taxed: {display(taxed)}')
        print(f'Profit:{display(profit)}, Taxed: {display(taxed_profit)}')
        
        
class ProgrammedBigGambling(BigGambling):
    def __init__(self,name,tries,baselevel,failstacklist):
        #Initializes big gambling, to register tries and baselevel. Failstack is later overwritten, doesnt matter.
        super().__init__(name,tries,baselevel,failstacklist[0])
        self.failstacklist=failstacklist
    def multigamble(self):
    #this function does BigGambling without asking user input, iterating over the failstack list. Assumes enhancing ends at end of FS list.
        for failstack in self.failstacklist:
            self.distributions.append(BinomialDistribution(self.name,self.tries,self.level,failstack))
            self.tries=self.distributions[-1].gamble()
            self.level+=1
            print(f'Obtained {self.tries} Level {self.level} items at {self.distributions[-1].p*100:.2f} %') 
        self.profit()
    
    def expected(self):
        for failstack in self.failstacklist:
            self.distributions.append(BinomialDistribution(self.name,self.tries,self.level,failstack))
            self.tries=self.distributions[-1].expected()
            self.level+=1
            print(f'Expected {self.tries:.2f} Level {self.level} items at {self.distributions[-1].p*100:.2f} %') 
        profit,taxed= self.profit()
        return profit, taxed

if __name__ == "__main__":
    #plt.style.use('seaborn')
    #print(GeometricDistribution('disto',3,140).expected_profit())
    #GeometricDistribution('disto',4,242).show_distribution(True)
    #print(ProgrammedBigGambling('ogre',100,0,[18,40,70,110,250]).expected())
    print(ProgrammedBigGambling('disto',100,0,[18,40,60,110,250]).expected())