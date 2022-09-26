from statistics import mode
from tkinter import Frame, Label, Entry, END
from models import register as model

class Register(Frame):
    def __init__(self, container, name):
        super().__init__(container)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.label=Label(self, text=f"{name}:")
        self.output=Entry(self, name=name)
        self.label.grid(row=0, column=0, sticky="nsew")
        self.output.grid(row=0, column=1, sticky="nsew")
        self.model = model.Register(label=name)
    
    def update(self, value):
        self.output.delete(0, 'end')
        self.output.insert(END, value)
        self.model.value = value