#return new state
def MESI(instruction,state):
    if(instruction=="write"):
        #all states return to M in write
        return 'M'
    elif(state=='S' and instruction=='read'):
        return 'S'
    elif(state=='M' and instruction=='read'):
        return 'M'
    elif(state=='M' and instruction=='veo_wr'):
        #writeback
        return 'I'
    elif(state=='M' and instruction=='veo_rd'):
        #writeback
        return 'S'
    elif (state=='S' and instruction=='veo_wr'):
        return 'I'
    elif(state=='I' and instruction=='read'):
        return 'E'
    elif(state=='E' and instruction=='read'):
        return 'E'
    elif(state=='I' and instruction=='veo_rd'):
        return 'S'
    elif(state=='E' and instruction=='veo_rd'):
        return 'S'
    elif(state=='E' and instruction=='veo_wr'):
        return 'I'
    else:
        return state