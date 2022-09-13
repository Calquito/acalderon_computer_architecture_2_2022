clock_time=3



#Lists require to be in a matrix to be put on the table
#L1,L2,L3,L4

cache_initial_state='I   |   0   |   0'
cache_matrix=[['','','',''],['','','',''],['','','',''],['','','','']]

for i in range(len(cache_matrix)):
    for j in range(len(cache_matrix[0])):
        cache_matrix[i][j]=cache_initial_state

#Main memory
main_memory_matrix=[[0,0,0,0,0,0,0,0]]
#Processor and its last instruction
processor_matrix=[['Procesador 0',''],['Procesador 1',''],['Procesador 2',''],['Procesador 3','']]

#variables shared by the system
#Last instruction
last_instruction=''

#temporal_mode
paso_a_paso=False

using_memory_bus=False