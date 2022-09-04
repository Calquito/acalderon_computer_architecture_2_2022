from tkinter import *
from threading import Thread
import time


#global variables
clock=0
l1_1=[0,0,0,0]
l1_2=[0,0,0,0]
l1_3=[0,0,0,0]
l1_4=[0,0,0,0]
main=[0,0,0,0,0,0,0,0]

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
    x=3
    


#start tkinter window
root = Tk()

######################################################################
class Table:
     
    def __init__(self,root):
        self.labels=[]
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                #self.e = Label(root, width=20, text=lst[i][j])
                self.e = Label(root, width=20, text=str(clock))
                self.e.grid(row=i, column=j)
                self.labels.append(self.e)

    def update(self):
        print(len(self.labels))
        for i in self.labels:
            i.config(text=str(clock))

 
# take the data
lst = [(1,'Raj','Mumbai',19),
       (2,'Aaryan','Pune',18),
       (3,'Vaishnavi','Mumbai',20),
       (4,'Rachna','Mumbai',21),
       (5,'Shubham','Delhi',21)]
  
# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])
######################################################################  

frame = Frame(root)
frame.pack()
t = Table(frame)

def update_gui():
    time.sleep(1)
    t.update()
    update_gui()
    #print("jhdnfkjdwnfjhdsnfkdshfjdnsfkdshfdsjfndskjfbds")
    
#update_gui()   


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

#tables of cache

lst = [(1,'Raj','Mumbai',19),
       (2,'Aaryan','Pune',18),
       (3,'Vaishnavi','Mumbai',20),
       (4,'Rachna','Mumbai',21),
       (5,'Shubham','Delhi',21)]

"""clock_control.join()
cpu1.join()
cpu2.join()
cpu3.join()
cpu4.join()"""








# Code to add widgets will go here...
root.mainloop()