import bdorequester as rq
import numpy as np
import stonky_nerd_stuff as sn
from scipy.stats import binom
import failstackcalculator as fs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class FailstacksComparing(rq.Item):
    def __init__(self,name,level,min,max):
        super().__init__(name)
        self.level=level
        self.min=min
        self.max=max
        self.price=rq.Price(self.array,self.level)

    def failstack_producing(self):
        failstacks=np.arange(self.min,self.max,1)
        self.failstacks=failstacks
        chances=self.chance_vectorization(failstacks)
        return chances
    
    def chance_vectorization(self,failstacks):
        vectorized_fs=np.vectorize(fs.chance)
        return vectorized_fs(self.level,failstacks)

    def expected_costs(self):
        return self.price.before + self.price.base
    
    def expected_profits(self,probability):
        success_chance=float(binom.mean(1,probability))
        revenue=success_chance*self.price.after
        taxed=revenue*rq.tax.keep
        cost=self.expected_costs()
        return revenue-cost, taxed-cost
    
    def calculate_profits(self):
        vectorized_profits=np.vectorize(self.expected_profits)
        chances=self.failstack_producing()
        untaxed,taxed=vectorized_profits(chances)
        return np.array([untaxed,taxed])
    
class FailstacksPlotting(FailstacksComparing):
    def __init__(self,name,level,min,max):
        super().__init__(name,level,min,max)
        self.profitarray=super().calculate_profits()
        
    def plot_profits(self):
        fig, ax =plt.subplots()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(10))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
        ax.plot(self.failstacks,self.profitarray[0],color='blue',label='Untaxed')
        ax.legend()
        ax.plot(self.failstacks,self.profitarray[1],color='green',label='Taxed')
        ax.legend()
        ax.set_yticklabels([sn.display(x) for x in ax.get_yticks()])
        plt.xlabel('Failstack')
        plt.ylabel('Average profit per attempt')
        plt.show()


#gFailstacksPlotting('disto',0,0,60).plot_profits()
