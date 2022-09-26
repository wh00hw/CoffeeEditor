from tkinter import Frame, Label, Entry, Button, END
from models import credit as model
from utils.credit_calc import calc_0x44, calc_0x54

class Credit(Frame):
    def __init__(self, container) -> None:
        super().__init__(container)
        self.model = model.Credit()
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.label=Label(self, text='Credit:')
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=1)
        self.input = Entry(self, name="credit")
        self.input.grid(row=0, column=1, sticky="w", padx=5, pady=1)
        self.button = Button(self, text="Calculate", command=self.calculate)
        self.button.grid(row=0, column=2, sticky="w", padx=5, pady=1)
        #x44
        self.x44_label=Label(self, text="x44:")
        self.x44_label.grid(row=1, column=0, sticky="w", padx=5, pady=1)
        self.x44_output=Entry(self)
        self.x44_output.grid(row=1, column=1, sticky="w", padx=5, pady=1)
        #x54
        self.x54_label=Label(self, text="x54:")
        self.x54_label.grid(row=2, column=0, sticky="w", padx=5, pady=1)
        self.x54_output=Entry(self)
        self.x54_output.grid(row=2, column=1, sticky="w", padx=5, pady=1)
  
    def update(self, value):
        self.model.value = value
        self._update_registers(float(value))
        self.input.delete(0, 'end')
        self.input.insert(END, value)
    
    def calculate(self):
        value = float(self.input.get().replace(',','.'))
        x44, x55 = self._update_registers(value)
        dump = self.master.dump
        if dump.model.dump:
            dump.edit(x44, x55)
            dump.show()
    
    def _update_registers(self, value):
        x44_value = calc_0x44(value)
        self.x44_output.delete(0, 'end')
        self.x44_output.insert(END, x44_value)
        x54_value = calc_0x54(x44_value)
        self.x54_output.delete(0, 'end')
        self.x54_output.insert(END, x54_value)
        return x44_value, x54_value
