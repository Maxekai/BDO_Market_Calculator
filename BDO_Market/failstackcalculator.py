

def chance(level,failstack):
    base=[0.25,0.1,0.075,0.025,0.0050]
    softcap=[18,40,44,110,390]
    
    if failstack<=softcap[level]:
        return base[level]+(base[level]*0.1)*failstack
    else:
        chance=base[level]+(base[level]*0.1)*softcap[level]+(base[level]*0.02)*(failstack-softcap[level])
        if chance<0.9:
            return chance
        else:
            return 0.9
        
