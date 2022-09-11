from ast import In
from tkinter import *
from threading import Thread
import time
import random


#############################################################global variables########################################################3
clock_time=3



#Lists require to be in a matrix to be put on the table
#L1,L2,L3,L4
cache_matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#Main memory
main_memory_matrix=[[0,0,0,0,0,0,0,0]]
#Processor and its last instruction
processor_matrix=[['Procesador 0',''],['Procesador 1',''],['Procesador 2',''],['Procesador 3','']]
#Last instruction
last_instruction=''

#temporal_mode
paso_a_paso=False
######################################################################################################################################

#processor class

class Processor:
    def __init__(self,number,pressed_next_cicle):
        self.number=number
        self.pressed_next_cicle=pressed_next_cicle
    def generate_instruction(self):
        #Clock cicle
        if not paso_a_paso:
            time.sleep(clock_time)
        self.pressed_next_cicle=False

        #generate random instruction
        instruction_p=random.randint(0,100)
        self.current_instruction= 'P'+str(self.number)+':'

        #CALC
        if(instruction_p<33):
            self.current_instruction+= "CALC"
        #READ
        elif(instruction_p<66):
            read_direction=random.randint(0,15)
            read_direction_binary=bin(read_direction)
            self.current_instruction+= " READ "+read_direction_binary[2:]

        #WRITE
        else:
            write_direction=random.randint(0,15)
            write_direction_binary=bin(write_direction)
            #max hex data
            data=random.randint(0,65535)
            data_hex=hex(data)
            #remove 0b and 0x
            self.current_instruction+= " WRITE "+write_direction_binary[2:]+" ; "+ data_hex[2:]

        #update processors matrix
        processor_matrix[self.number][1]=self.current_instruction
        processor_table_GUI.data_matrix=processor_matrix
        processor_table_GUI.update()

        #update cache matrix
        cache_matrix[1][3]=cache_matrix[1][3]+2
        cache_table_GUI.data_matrix=cache_matrix
        cache_table_GUI.update()

        #update last instruction
        last_instruction=self.current_instruction
        label9.config(text='Última instrucción generada por el sistema:'+last_instruction)

        #recursive
        if paso_a_paso:
            while(paso_a_paso):
                #avoid infinite loop to take resources
                time.sleep(1)
                print(self.pressed_next_cicle)
                if(self.pressed_next_cicle):
                    break
        self.generate_instruction()


            
            



#create processor instances
cpu0= Processor(0,False)
cpu1= Processor(1,False)
cpu2= Processor(2,False)
cpu3= Processor(3,False)



#create processor threads
cpu0_thread = Thread(target=cpu0.generate_instruction)
cpu1_thread = Thread(target=cpu1.generate_instruction)
cpu2_thread = Thread(target=cpu2.generate_instruction)
cpu3_thread = Thread(target=cpu3.generate_instruction)


cpu0_thread.start()
cpu1_thread.start()
cpu2_thread.start()
cpu3_thread.start()

#change temporal mode
def temporal_mode():
    global paso_a_paso
    paso_a_paso= not paso_a_paso
    print(paso_a_paso)
    if (paso_a_paso):
        mode_button.config(text="Modo ejecución continua")
    else:
        mode_button.config(text="Modo paso a paso")
    
#execute next cicle in "paso a paso" mode
def execute_next_cicle(e):
    print("dsa")
    cpu0.pressed_next_cicle=True
    cpu1.pressed_next_cicle=True
    cpu2.pressed_next_cicle=True
    cpu3.pressed_next_cicle=True



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

