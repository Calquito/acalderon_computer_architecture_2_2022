#processor class
import time
import random
from config import *

class Processor:
    def __init__(self,processor_number,pressed_next_cicle,cache):
        self.processor_number=processor_number
        self.pressed_next_cicle=pressed_next_cicle
        self.cache=cache
    
    def write(self,direction,data):
        data=data+2

    def read(self,direction):
        direction=2

    def calc(self):
        return True

    def generate_instruction(self):
        #Clock cicle
        if not paso_a_paso:
            time.sleep(clock_time)
        self.pressed_next_cicle=False

        #generate random instruction
        instruction_p=random.randint(0,100)
        self.current_instruction= 'P'+str(self.processor_number)+':'

        #CALC
        if(instruction_p<33):
            self.current_instruction+= "CALC"
            self.calc()
        #READ
        elif(instruction_p<66):
            read_direction=random.randint(0,15)
            read_direction_binary=bin(read_direction)
            self.current_instruction+= " READ "+read_direction_binary[2:]
            self.read(read_direction)

        #WRITE
        else:
            write_direction=random.randint(0,15)
            write_direction_binary=bin(write_direction)
            #max hex data
            data=random.randint(0,65536)
            data_hex=hex(data)
            #remove 0b and 0x
            self.current_instruction+= " WRITE "+write_direction_binary[2:]+" ; "+ data_hex[2:]
            self.write(write_direction,data)

        #update processors matrix
        processor_matrix[self.processor_number][1]=self.current_instruction
        processor_table_GUI.data_matrix=processor_matrix
        processor_table_GUI.update()


        #update cache matrix
        self.cache[3][2]+=2

        for i in range(4):
            cache_matrix[self.processor_number][i]=self.cache[i][0]+'   |   '+str(self.cache[i][1])+'   |   '+str(self.cache[i][2])
        cache_table_GUI.data_matrix=cache_matrix
        cache_table_GUI.update()


        #update last instruction
        last_instruction=self.current_instruction
        label9.config(text='Última instrucción generada por el sistema:'+last_instruction)

        #recursive
        while(paso_a_paso):
            #avoid infinite loop to take resources
            time.sleep(1)
            if(self.pressed_next_cicle):
                break
        self.generate_instruction()
