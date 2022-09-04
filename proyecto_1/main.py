from tkinter import *
from threading import Thread
import time
from gui import *



#global variables
clock=0
l1_1=[0,0,0,0]
l1_2=[0,0,0,0]
l1_3=[0,0,0,0]
l1_4=[0,0,0,0]
main_memory=[0,0,0,0,0,0,0,0]

cache_matrix=[l1_1,l1_2,l1_3,l1_4]
main_memory_matrix=[main_memory]

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
    print(cache_matrix)
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
     
    def __init__(self,root,data_matrix):
        self.labels=[]
        self.data_matrix=data_matrix
        # code for creating table
        for i in range(len(data_matrix)):
            self.labels.append([])
            for j in range(len(data_matrix[0])):
                self.e = Label(root, width=20, text=data_matrix[i][j])
                #self.e = Label(root, width=20, text="dsdd")
                self.e.grid(row=i, column=j)
                self.labels[i].append(self.e)

    def update(self):
        for i in range(len(self.labels)):
            for j in range(len(self.labels[0])):
                self.labels[i][j].config(text=self.data_matrix[i][j])

######################################################################  

frame = Frame(root)
frame.pack()
frame2= Frame(root)
frame2.pack()
cache_table_GUI = Table(frame,cache_matrix)
main_memory_table_GUI= Table(frame2,main_memory_matrix)

# Code to add widgets will go here...
root.mainloop()