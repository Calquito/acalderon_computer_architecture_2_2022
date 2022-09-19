from config import *
import time

def read_from_memory(direction):
    global using_memory_bus
    #waits for the bus to be free
    while(using_memory_bus):
        time.sleep(1)
        pass
    #now memory bus is free
    using_memory_bus=True
    data=''
    time.sleep(going_to_memory_time)
    data=main_memory_matrix[0][direction]
    using_memory_bus=False
    return data

def write_to_memory(direction,data):
    global using_memory_bus
    #waits for the bus to be free
    while(using_memory_bus):
        time.sleep(1)
        pass
    #now memory bus is free
    using_memory_bus=True
    time.sleep(going_to_memory_time)
    main_memory_matrix[0][direction]=data
    using_memory_bus=False