from tkinter import *
from threading import Thread
import time
from turtle import right
from gui import *



#############################################################global variables########################################################3
clock=0



#Lists require to be in a matrix to be put on the table
#L1,L2,L3,L4
cache_matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#Main memory
main_memory_matrix=[[0,0,0,0,0,0,0,0]]
#Processor and its last instruction
processor_matrix=[['Procesador 1','P0 : READ 0100'],['Procesador 2',''],['Procesador 3',''],['Procesador 4','']]
#Last instruction
last_instruction=''


######################################################################################################################################
#controls the clock
def timer():
    while(True):
        global clock
        clock=1
        time.sleep(1)
        clock=0
        time.sleep(1)



#runs the processor
def processor():
    for i in range(len(cache_matrix)):
        for j in range(len(cache_matrix[0])):
            cache_matrix[i][j]=cache_matrix[i][j]+2
    time.sleep(3)
    #print(cache_matrix)
    processor()
            
    


#t = Table(frame)

def update_gui():
    time.sleep(3)
    cache_table_GUI.data_matrix=cache_matrix
    cache_table_GUI.update()
    update_gui()



#create processor threads
clock_control = Thread(target=timer)
cpu1 = Thread(target=processor)
cpu2 = Thread(target=processor)
cpu3 = Thread(target=processor)
cpu4 = Thread(target=processor)
gui = Thread(target=update_gui)

clock_control.start()
cpu1.start()
cpu2.start()
cpu3.start()
cpu4.start()
gui.start()




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

label9=Label(frame_main_instruction , text='Última instrucción generada por el sistema:'+last_instruction)
label9.pack(pady=5,side=LEFT)



#create tables in frames
cache_table_GUI = Table(frame_cache,cache_matrix,20)
processor_table_GUI = Table(frame_procesador,processor_matrix,20)
main_memory_table_GUI= Table(frame_main,main_memory_matrix,15)

# Code to add widgets will go here...
root.mainloop()