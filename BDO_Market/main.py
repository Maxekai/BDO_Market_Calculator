import bdorequester as rq
import stonky_nerd_stuff as sn
import failstackcalculator as fs
import failstack_comparing as fc
import matplotlib.pyplot as plt
import warnings
import cache_managing as cm

def TrueHandler(input):
    if input.lower()=='y':
        return True
    if input.lower()=='n':
        return False

class Commander:
    def __init__(self):
        self.initial=input('Enter command. Enter help to show commands\n')
        self.executer=Executer()
        self.decide_action(self.initial)
        
    def decide_action(self,choice):
        commands={'help':self.executer.show_commands,
                  'prex1':self.executer.profit_exp_one,
                  'prmed1':self.executer.prof_med_one,
                  'gamb1':self.executer.gamble_one,
                  'chart1':self.executer.chart_one,
                  'profx':self.executer.prof_mul,
                  'gambx':self.executer.gamble_mul,
                    'chartx':self.executer.chart_mul,
                    'biggamb':self.executer.big_gamb,
                    'proggamb':self.executer.prog_gamb,
                    'progexp':self.executer.prog_exp,
                    'plotfs':self.executer.plot_fs}
        if choice in commands:
            commands[choice]()
    

class Executer:
    
    def __init__(self):
        self.Instructions={
        'Enchanting until the first success':
            {
            'prex1': 'Expected profit.', 
            'prmed1': 'Median profit Not average! If 100 people did this enchantment and we ordered them by profit, the 50th person would get this profit.',
            'gamb1': 'Enchanting simulation',
            'chart1': 'Result probabilities chart'
            },
        'Enchanting a fixed amount of items':
            {
            'profx': 'Expected profit',
            'gambx': 'Enchanting simulation',
            'chartx': 'Result probabilities chart'
            },
        'Enchant across multiple levels, as in going from base to PEN':
            {
            'biggamb':'From a fixed amount of items, enchants through the levels until the user commands it to stop. Then calculates profits.',
            'proggamb':'Does the same as biggambling but the end level and failstacks are chosen before starting to gamble',
            'progexp':'Calculates expected profit of a gambling session like proggamb'
            },
        'Failstack Information':
            {
            'plotfs':'Plots expected attempt profit across a range of failstacks'
            }
        }            
    
    def show_commands(self):
        for key,value in self.Instructions.items():
            print(f'\n{key}')
            for k,v in value.items():
                print(f'{k}: {v}')
                
    def profit_exp_one(self):
        inputlist=input('\nItem, Level before enchanting, Failstack\n').split(',')
        print(sn.display((sn.GeometricDistribution((inputlist[0]),int(inputlist[1]),int(inputlist[2])).expected_profit())))
    
    def prof_med_one(self):
        inputlist=input('\nItem, Level before enchanting, Failstack\n').split(',')
        print(sn.display(sn.GeometricDistribution((inputlist[0]),int(inputlist[1]),int(inputlist[2])).median()))

    def gamble_one(self):
        inputlist=input('\nItem, Level before enchanting, Failstack\n').split(',')
        #RANDOM SEED FOR TESTING PURPOSES.
        try:
            seed=int(inputlist[3].strip())
        except IndexError:
            seed=None
        print(f'Tries to first success: {sn.GeometricDistribution((inputlist[0]),int(inputlist[1]),int(inputlist[2])).gamble(seed)}')
    
    def chart_one(self):
        inputlist=input('\nItem, Level before enchanting, Failstack, Show Price (y/n)\n').split(',')
        sn.GeometricDistribution((inputlist[0]),int(inputlist[1]),int(inputlist[2])).show_distribution(TrueHandler(inputlist[3]))

    def prof_mul(self):
        inputlist=input('\nItem, Tries, Level before enchanting, Failstack\n').split(',')
        print(sn.display(sn.BinomialDistribution(inputlist[0],int(inputlist[1]),int(inputlist[2]),int(inputlist[3])).expected_profit()))
    
    def gamble_mul(self):
        inputlist=input('\nItem, Tries, Level before enchanting, Failstack\n').split(',')
         #RANDOM SEED FOR TESTING PURPOSES.
        try:
            seed=int(inputlist[4].strip())
        except IndexError:
            seed=None
        print(f'Successes: {sn.BinomialDistribution(inputlist[0],int(inputlist[1]),int(inputlist[2]),int(inputlist[3])).gamble(seed)}')
    
    def chart_mul(self):
        inputlist=input('\nItem, Tries, Level before enchanting, Failstack\n').split(',')
        sn.BinomialDistribution(inputlist[0],int(inputlist[1]),int(inputlist[2]),int(inputlist[3])).show_distribution()
    
    def big_gamb(self):
        inputlist=input('\nItem, Tries, Initial Level, First level failstack\n').split(',')
        sn.BigGambling(inputlist[0],int(inputlist[1]),int(inputlist[2]),int(inputlist[3])).gambling()  
 
    def prog_gamb(self):       
        userinput=input('\nItem, Tries, Initial Level, [Failstack1, Failstack2...]\n')
        inputlist=userinput[:userinput.find('[')-1].split(',')
        failstacklist=userinput[userinput.find('[')+1:userinput.find(']')].split(',')
        sn.ProgrammedBigGambling(inputlist[0],int(inputlist[1]),int(inputlist[2]),[int(element) for element in failstacklist]).multigamble()
    
    def prog_exp(self):
        userinput=input('\nItem, Tries, Initial Level, [Failstack1, Failstack2...]\n')
        inputlist=userinput[:userinput.find('[')-1].split(',')
        failstacklist=userinput[userinput.find('[')+1:userinput.find(']')].split(',')
        sn.ProgrammedBigGambling(inputlist[0],int(inputlist[1]),int(inputlist[2]),[int(element) for element in failstacklist]).expected()
        
    def plot_fs(self):
        inputlist=input('\nItem, Level before enchanting, Min. Failstack, Max. Failstack\n').split(',')
        fc.FailstacksPlotting(inputlist[0],int(inputlist[1]),int(inputlist[2]),int(inputlist[3])).plot_profits()

        
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    plt.style.use('seaborn')
    while True:
        Commander()
        cm.CacheManager.CachedArrays.clear_cache()
        print("Ask again? y/n")
        if input()!= "y":
            break
    
    

    
