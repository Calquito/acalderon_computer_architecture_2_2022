from tkinter import *

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
