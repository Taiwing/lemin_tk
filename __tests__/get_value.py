#!/usr/bin/env python3

import tkinter as tk
from time import sleep
 
class Menu:
    def __init__(self, master, nb):
        self.master=master
        self.nb = nb
        self.var1 = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.var1)
        self.entry.pack(side=tk.TOP)
 
        self.button = tk.Button(self.master,text='get_val',command = self.get_value)
        self.button.pack(side=tk.TOP)

        self.button = tk.Button(self.master,text='print',command = self.print_value)
        self.button.pack()

        self.value = None
 
    def get_value(self):
        subroot = tk.Toplevel(self.master)
        self.sub = Menu(subroot, self.nb + 1)
        if self.sub.value != None:
            self.value = self.entry.get()
        elif self.nb > 0:
            self.value = self.entry.get()

    def print_value(self):
        print("entry:", self.entry.get())
        print("var1:", self.var1.get())
        print("value:", self.value)

    def bullshit(self):
        sleep(30)
 
if __name__=="__main__":
    root = tk.Tk()
    menu = Menu(root, 0)
    root.mainloop()
