from tkinter import *
from threading import Thread
import time
import random


#############################################################global variables########################################################3
clock_time=2
going_to_memory_time=10


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
######################################################################################################################################

#processor class

class Processor:
    def __init__(self,processor_number,pressed_next_cicle,cache):
        self.processor_number=processor_number
        self.pressed_next_cicle=pressed_next_cicle
        self.cache=cache
    
    def write(self,direction,data):
        #check if data is in memory
        write_hit=False
        hit_block_number=0
        new_state=''


        for i in range(len(self.cache)):
            if self.cache[i][1]==direction:
                write_hit==True
                hit_block_number=i
                break
        
        new_state=MESI('write',self.cache[hit_block_number][0])
        
        if (write_hit):
            self.cache[hit_block_number][2]=data
            
        #write miss
        else:
            #waits for the bus to be free
            while(using_memory_bus):
                time.sleep(1)
                pass
            #now memory bus is free
            main_memory_matrix[0][direction]=data
            #one way associative
            self.cache[direction%4]=[new_state,direction,data]

        invalidate_blocks(self.processor_number,direction)



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
            read_direction=random.randint(0,7)
            read_direction_binary=bin(read_direction)
            self.current_instruction+= " READ "+read_direction_binary
            self.read(read_direction)

        #WRITE
        else:
            write_direction=random.randint(0,7)
            write_direction_binary=bin(write_direction)
            #max hex data
            data=random.randint(0,65536)
            data_hex=hex(data)
            #remove 0b and 0x
            self.current_instruction+= " WRITE "+write_direction_binary+" ; "+ data_hex
            self.write(write_direction,data)

        #update processors matrix
        processor_matrix[self.processor_number][1]=self.current_instruction
        processor_table_GUI.data_matrix=processor_matrix
        processor_table_GUI.update()


        #update cache matrix
        for i in range(4):
            cache_matrix[self.processor_number][i]=self.cache[i][0]+'   |   '+str(bin(self.cache[i][1]))+'   |   '+str(hex(self.cache[i][2]))
        cache_table_GUI.data_matrix=cache_matrix
        cache_table_GUI.update()

        #update main memory data:
        main_memory_matrix_hex=[[]]
        for i in range(len(main_memory_matrix[0])):
            main_memory_matrix_hex[0].append(hex(main_memory_matrix[0][i]))

        main_memory_table_GUI.data_matrix=main_memory_matrix_hex
        main_memory_table_GUI.update()


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




def controller():
    while(True):
        time.sleep(1)

            



#create processor instances
#number of processor, paso a paso, matrix: state, memory direction, data
cpu0= Processor(0,False,[['I',0,0],['I',0,0],['I',0,0],['I',0,0]])
cpu1= Processor(1,False,[['I',0,0],['I',0,0],['I',0,0],['I',0,0]])
cpu2= Processor(2,False,[['I',0,0],['I',0,0],['I',0,0],['I',0,0]])
cpu3= Processor(3,False,[['I',0,0],['I',0,0],['I',0,0],['I',0,0]])


#create processor threads
cpu0_thread = Thread(target=cpu0.generate_instruction)
cpu1_thread = Thread(target=cpu1.generate_instruction)
cpu2_thread = Thread(target=cpu2.generate_instruction)
cpu3_thread = Thread(target=cpu3.generate_instruction)
controller_thread=Thread(target=controller)


cpu0_thread.start()
cpu1_thread.start()
cpu2_thread.start()
cpu3_thread.start()
controller_thread.start()


#change temporal mode
def temporal_mode():
    global paso_a_paso
    paso_a_paso= not paso_a_paso
    if (paso_a_paso):
        mode_button.config(text="Modo ejecución continua")
    else:
        mode_button.config(text="Modo paso a paso")
    
#execute next cicle in "paso a paso" mode
def execute_next_cicle(e):
    cpu0.pressed_next_cicle=True
    cpu1.pressed_next_cicle=True
    cpu2.pressed_next_cicle=True
    cpu3.pressed_next_cicle=True


#return new state
def MESI(instruction,state):
    if(instruction=="write"):
        #all states return to M in write
        return 'M'
    elif(state=='S' and instruction=='read'):
        return 'S'
    elif(state=='M' and (instruction=='read' or instruction=='write')):
        return 'M'
    elif(state=='M' and instruction=='veo_wr'):
        #writeback
        return 'I'
    elif(state=='M' and instruction=='veo_wr'):
        #writeback
        return 'S'
    elif(state=='I' and instruction=='read'):
        return 'S'
    elif (state=='S' and instruction=='veo_wr'):
        return 'I'
    elif(state=='I' and instruction=='read'):
        return 'E'
    elif(state=='E' and instruction=='read'):
        return 'E'
    elif(state=='E' and instruction=='veo_read'):
        return 'S'
    elif(state=='E' and instruction=='veo_wr'):
        return 'I'
    else:
        return state
    

    
    
    
    

    

#invalidate blocks
def invalidate_blocks(processor_number,direction):
    if(cpu0.processor_number != processor_number):
        for i in range(4):
            if cpu0.cache[i][1]==direction:
                cpu0.cache[i][0]='I'
    if(cpu1.processor_number != processor_number):
        for i in range(4):
            if cpu0.cache[i][1]==direction:
                cpu0.cache[i][0]='I'
    if(cpu1.processor_number != processor_number):
        for i in range(4):
            if cpu0.cache[i][1]==direction:
                cpu0.cache[i][0]='I'
    if(cpu1.processor_number != processor_number):
        for i in range(4):
            if cpu0.cache[i][1]==direction:
                cpu0.cache[i][0]='I'

    


    



####################################################################GUI####################################################################

#start tkinter window
root = Tk()


######################################################################
class Table:
     
    def __init__(self,root,data_matrix,width):
        self.labels=[]
        self.width=width
        self.data_matrix=data_matrix
        # code for creating table
        for i in range(len(data_matrix)):
            self.labels.append([])
            for j in range(len(data_matrix[0])):
                self.e = Label(root, width=self.width, text=data_matrix[i][j],  borderwidth=2, relief="groove")
                self.e.grid(row=i, column=j)
                self.labels[i].append(self.e)

    def update(self):
        for i in range(len(self.labels)):
            for j in range(len(self.labels[0])):
                self.labels[i][j].config(text=self.data_matrix[i][j])

######################################################################  

#position frames of the tables

#labels of processor and cache (superior frame)
frame_processor_cache = Frame(root)
frame_processor_cache.pack(side=TOP)

frame_labels1 = Frame(frame_processor_cache)
frame_labels1 .pack(side=TOP)
label1=Label(frame_labels1 , width=20, text='Procesador')
label2=Label(frame_labels1 , width=20, text='Última instrucción')
label3=Label(frame_labels1 , width=20, text='Bloque 0')
label4=Label(frame_labels1 , width=20, text='Bloque 1')
label5=Label(frame_labels1 , width=20, text='Bloque 2')
label6=Label(frame_labels1 , width=20, text='Bloque 3')
label1.pack(side = LEFT)
label2.pack(side = LEFT)
label3.pack(side = LEFT)
label4.pack(side = LEFT)
label5.pack(side = LEFT)
label6.pack(side = LEFT)


frame_cache = Frame(frame_processor_cache)
frame_cache.pack(side=RIGHT)
frame_procesador=Frame(frame_processor_cache)
frame_procesador.pack(side=LEFT)

#Frame of main memory and last instruction

frame_main_instruction= Frame(root)
frame_main_instruction.pack()

label7=Label(frame_main_instruction , text='Memoria principal')
label7.pack(pady=5)

frame_main= Frame(frame_main_instruction)
frame_main.pack()

#just for space
label8=Label(frame_main_instruction , text='')
label8.pack(pady=5)

#last instruction generated
label9=Label(frame_main_instruction , text='Última instrucción generada por el sistema:'+last_instruction)
label9.pack(pady=5,side=LEFT)

#mode button
mode_button=Button(frame_main_instruction, text= "Modo paso a paso", command=temporal_mode,width=20)
mode_button.pack(pady=5,padx=5,side=RIGHT)


#create tables in frames
cache_table_GUI = Table(frame_cache,cache_matrix,20)
processor_table_GUI = Table(frame_procesador,processor_matrix,20)
main_memory_table_GUI= Table(frame_main,main_memory_matrix,15)

#When enter pressed, change cicle

root.bind('<Return>',execute_next_cicle)

# Code to add widgets will go here...

root.mainloop()

