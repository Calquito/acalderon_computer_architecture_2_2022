from threading import Thread
import time
import random
from tkinter import *
from tkinter import messagebox

from config import *
from GUI_Table import Table
from MESI import MESI
from memory_instructions import *

#processor class

class Processor:
    def __init__(self,processor_number,pressed_next_cicle,cache,current_instruction,instruction_entered):
        self.processor_number=processor_number
        self.pressed_next_cicle=pressed_next_cicle
        self.cache=cache
        self.current_instruction=current_instruction
        self.instruction_entered=instruction_entered
    
    def write(self,direction,data):
        #check if data is in memory
        write_hit=False
        new_state=''
        hit_block_number=None

        #triggers controller
        self.controller('write',direction)

        #one way associative
        if self.cache[direction%4][1]==direction:
            write_hit==True
            hit_block_number=direction%4
                
        #transition 2
        #transition 3
        if (write_hit):
            new_state=MESI('write',self.cache[hit_block_number][0])
            self.cache[direction%4]=[new_state,direction,data]
            
        #write miss
        else:

            #using block
            processor_matrix[self.processor_number][2]=direction
            processor_matrix[self.processor_number][3]='WRITE MISS'
            processor_table_GUI.data_matrix=processor_matrix
            processor_table_GUI.update()

            write_to_memory(direction,data)
            #block doesn't exist in cache, so assume I
            new_state=MESI('write','I')
            #one way associative
            self.cache[direction%4]=[new_state,direction,data]

            #not using block
            processor_matrix[self.processor_number][2]=''
            processor_matrix[self.processor_number][3]=''
            processor_table_GUI.data_matrix=processor_matrix
            processor_table_GUI.update()
        



    def read(self,direction):
        #check if data is in memory
        read_hit=False
        new_state=''
        hit_block_number=None
        current_state=self.cache[direction%4][0]

        #one way associative
        #transition 1
        #transition 2
        if(self.cache[direction%4][1]==direction and current_state!='I'): #States M,S and E can read infinitely
            read_hit==True
            hit_block_number=direction%4

        #go to other caches
        #check_cache returns tuple with boolean that indicates if the data is in other cache, and the data if true
        #if false, go to main memory
        if (read_hit):
            #transition 6 (without E)
            new_state=MESI('read',self.cache[hit_block_number][0])
            self.cache[direction%4]=[new_state,direction,self.cache[direction%4][2]]
            #if read hit, exit
            return True

        #fetch from other cache if true, if false go to memory

        #using block
        processor_matrix[self.processor_number][2]=direction
        processor_matrix[self.processor_number][3]='READ MISS'
        processor_table_GUI.data_matrix=processor_matrix
        processor_table_GUI.update()


        cache_checked=self.controller('read',direction)
        if(cache_checked[0]):
            #veo_rd
            #transition 9
            self.cache[direction%4]=['S',direction,cache_checked[1]]
        else:
            self.cache[direction%4]=['E',direction,read_from_memory(direction)]

        #not using block
        processor_matrix[self.processor_number][2]=''
        processor_matrix[self.processor_number][3]=''
        processor_table_GUI.data_matrix=processor_matrix
        processor_table_GUI.update()



    def calc(self):
        return True

    def update_GUI_after_instruction(self):
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
        label9.config(text='??ltima instrucci??n generada por el sistema:'+last_instruction)


    def controller(self,instruction,direction):
        if(instruction=='write'):
            #veo_wr
            #transition 4
            #transition 7
            #transition 8
            invalidate_blocks(self.processor_number,direction)
            return None
        elif(instruction=='read'):
            #veo_rd
            #transition 5
            return check_caches_read(self.processor_number,direction)
        else:
            return None

    def parse_instruction(self):
        if (self.current_instruction.find('CALC')!=-1):
            self.update_GUI_after_instruction()
            self.calc()
        elif (self.current_instruction.find('READ')!=-1):
            self.update_GUI_after_instruction()
            self.read(int(self.current_instruction[10:],2))
        elif (self.current_instruction.find('WRITE')!=-1):
            self.update_GUI_after_instruction()
            self.write(int(self.current_instruction[11:15],2),int(self.current_instruction[16:],16))
        else:
            messagebox.showwarning(title=None, message='Instrucci??n no v??lida') 


    def generate_instruction(self):
        #Clock cicle
        if not paso_a_paso:
            time.sleep(clock_time)
        self.pressed_next_cicle=False

        #recursive
        while(paso_a_paso):
            #avoid infinite loop to take resources
            time.sleep(1)
            if(self.pressed_next_cicle):
                break

        #generate random instruction
        instruction_p=random.randint(0,100)

        if(self.instruction_entered):
            self.instruction_entered=False
            print('llamo')
            self.parse_instruction()
            self.generate_instruction()

        self.current_instruction= 'P'+str(self.processor_number)+':'


        #Distribucion uniforme discreta

        #CALC
        if(instruction_p<33):
            self.current_instruction+= "CALC"
        #READ
        elif(instruction_p<66):
            read_direction=random.randint(0,7)
            read_direction_binary=bin(read_direction)
            self.current_instruction+= " READ "+read_direction_binary[2:]

        #WRITE
        else:
            write_direction=random.randint(0,7)
            write_direction_binary=bin(write_direction)
            #max hex data
            data=random.randint(0,65536)
            data_hex=hex(data)
            #remove 0b and 0x
            self.current_instruction+= " WRITE "+write_direction_binary[2:]+" ; "+ data_hex[2:]

        self.update_GUI_after_instruction()

        #CALC
        if(instruction_p<33):
            self.calc()
        #READ
        elif(instruction_p<66):
            self.read(read_direction)

        #WRITE
        else:
            self.write(write_direction,data)

        self.generate_instruction()





def check_caches_read(processor_number,direction):
    if(cpu0.processor_number != processor_number):
        for i in range(4):
            #if found the data, return it and in the provider the new state is shared
            if(cpu0.cache[i][1]==direction and cpu0.cache[i][0]!='I'):
                #veo_rd
                cpu0.cache[i][0]=MESI('veo_rd',cpu0.cache[i][0])
                return (True,cpu0.cache[i][2])
    if(cpu1.processor_number != processor_number):
        for i in range(4):
            if (cpu1.cache[i][1]==direction and cpu1.cache[i][0]!='I' ):
                cpu1.cache[i][0]=MESI('veo_rd',cpu1.cache[i][0])
                return (True,cpu1.cache[i][2])
    if(cpu2.processor_number != processor_number):
        for i in range(4):
            if (cpu2.cache[i][1]==direction and cpu2.cache[i][0]!='I'):
                cpu2.cache[i][0]=MESI('veo_rd',cpu2.cache[i][0])
                return (True,cpu2.cache[i][2])
    if(cpu3.processor_number != processor_number):
        for i in range(4):
            if (cpu3.cache[i][1]==direction and cpu3.cache[i][0]!='I'):
                cpu3.cache[i][0]=MESI('veo_rd',cpu3.cache[i][0])
                return (True,cpu3.cache[i][2])

    return(False,0)



            
#create processor instances
#number of processor, paso a paso, matrix: state, memory direction, data
cpu0= Processor(0,False,[['I',0,0],['I',1,0],['I',2,0],['I',3,0]],'',False)
cpu1= Processor(1,False,[['I',0,0],['I',1,0],['I',2,0],['I',3,0]],'',False)
cpu2= Processor(2,False,[['I',0,0],['I',1,0],['I',2,0],['I',3,0]],'',False)
cpu3= Processor(3,False,[['I',0,0],['I',1,0],['I',2,0],['I',3,0]],'',False)


#create processor threads
cpu0_thread = Thread(target=cpu0.generate_instruction)
cpu1_thread = Thread(target=cpu1.generate_instruction)
cpu2_thread = Thread(target=cpu2.generate_instruction)
cpu3_thread = Thread(target=cpu3.generate_instruction)


cpu0_thread.start()
cpu1_thread.start()
cpu2_thread.start()
cpu3_thread.start()

    
#execute next cicle in "paso a paso" mode
def execute_next_cicle(e):
    cpu0.pressed_next_cicle=True
    cpu1.pressed_next_cicle=True
    cpu2.pressed_next_cicle=True
    cpu3.pressed_next_cicle=True

   
#invalidate blocks
#processor number is the processor that is invalidating
def invalidate_blocks(processor_number,direction):
    if(cpu0.processor_number != processor_number):
        for i in range(4):
            if (cpu0.cache[i][1]==direction):
                cpu0.cache[i][0]='I'
                break
    if(cpu1.processor_number != processor_number):
        for i in range(4):
            if (cpu1.cache[i][1]==direction):
                cpu1.cache[i][0]='I'
                break
    if(cpu2.processor_number != processor_number):
        for i in range(4):
            if (cpu2.cache[i][1]==direction):
                cpu2.cache[i][0]='I'
                break
    if(cpu3.processor_number != processor_number):
        for i in range(4):
            if (cpu3.cache[i][1]==direction):
                cpu3.cache[i][0]='I'
                break

    
#change temporal mode
def temporal_mode():
    global paso_a_paso
    paso_a_paso= not paso_a_paso
    if (paso_a_paso):
        mode_button.config(text="Modo ejecuci??n continua")
    else:
        mode_button.config(text="Modo paso a paso")

def entered_instruction(instruction):
    if (not paso_a_paso):
        messagebox.showwarning(title=None, message='Solo se puede ingresar una instrucci??n en modo paso a paso')
    else:
        if instruction[1]=='0':
            cpu0.instruction_entered=True
            cpu0.current_instruction=instruction
        elif instruction[1]=='1':
            cpu1.instruction_entered=True
            cpu1.current_instruction=instruction
        elif instruction[1]=='2':
            cpu2.instruction_entered=True
            cpu2.current_instruction=instruction
        elif instruction[1]=='3':
            cpu3.instruction_entered=True
            cpu3.current_instruction=instruction
        else:
           messagebox.showwarning(title=None, message='Instrucci??n no v??lida') 
            


########################################################################################GUI#####################################################################

#start tkinter window
root = Tk()


#position frames of the tables

#labels of processor and cache (superior frame)
frame_processor_cache = Frame(root)
frame_processor_cache.pack(side=TOP)

frame_labels1 = Frame(frame_processor_cache)
frame_labels1 .pack(side=TOP)
label1=Label(frame_labels1 , width=20, text='Procesador')
label2=Label(frame_labels1 , width=20, text='??ltima instrucci??n')
label11=Label(frame_labels1 , width=20, text='Bloque de memoria')
label12=Label(frame_labels1 , width=20, text='Alerta Miss')
label3=Label(frame_labels1 , width=20, text='Bloque 0')
label4=Label(frame_labels1 , width=20, text='Bloque 1')
label5=Label(frame_labels1 , width=20, text='Bloque 2')
label6=Label(frame_labels1 , width=20, text='Bloque 3')
label1.pack(side = LEFT)
label2.pack(side = LEFT)
label11.pack(side = LEFT)
label12.pack(side = LEFT)
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
label9=Label(frame_main_instruction , text='??ltima instrucci??n generada por el sistema:'+last_instruction)
label9.pack(pady=5,side=LEFT)

#mode button
mode_button=Button(frame_main_instruction, text= "Modo paso a paso", command=temporal_mode,width=20)
mode_button.pack(pady=5,padx=5,side=RIGHT)

#introduce instruction

button_entry_instruction = Button(frame_main_instruction, text="Ingresar_instrucci??n", command=lambda: entered_instruction(entry_instruction.get()))
button_entry_instruction.pack(pady=5,padx=5,side=RIGHT)


entry_instruction = Entry(frame_main_instruction)
entry_instruction.pack(pady=5,padx=5,side=RIGHT)



#create tables in frames
cache_table_GUI = Table(frame_cache,cache_matrix,20)
processor_table_GUI = Table(frame_procesador,processor_matrix,20)
main_memory_table_GUI= Table(frame_main,main_memory_matrix,20)

#When enter pressed, change cicle

root.bind('<Return>',execute_next_cicle)

# Code to add widgets will go here...

root.mainloop()

