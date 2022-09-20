#############################################################global variables########################################################
clock_time=1  
going_to_memory_time=5 


#Lists require to be in a matrix to be put on the table
#L1,L2,L3,L4

cache_matrix=[['','','',''],['','','',''],['','','',''],['','','','']]

#fills cache with initial states
for i in range(len(cache_matrix)):
    for j in range(len(cache_matrix[0])):
        #cache_matrix[i][j]='I   |   '+str(j)+'   |   0'
        cache_matrix[i][j]='I   |   0   |   0'

#Main memory
main_memory_matrix=[[0,0,0,0,0,0,0,0]]
#Processor and its last instruction
processor_matrix=[['Procesador 0','','',''],['Procesador 1','','',''],['Procesador 2','','',''],['Procesador 3','','','']]

#variables shared by the system
#Last instruction
last_instruction=''

#temporal_mode
paso_a_paso=False

using_memory_bus=False


