from tkinter import Frame, Label, Entry, Button, END
from models import credit as model
from utils.credit_calc import calc_0x44, calc_0x54

class Credit(Frame):
    def __init__(self, container) -> None:
        super().__init__(container)
        self.grid_rowconfigure(0, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.label=Label(self, text='Credit:')
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=1)
        self.input = Entry(self, name="credit")
        self.input.grid(row=0, column=1, sticky="w", padx=5, pady=1)
        self.button = Button(self, text="Calculate", command=self.calculate)
        self.button.grid(row=0, column=2, sticky="w", padx=5, pady=1)
        self.model = model.Credit()
    
    def update(self, value):
        self.model.value = value
        self._update_registers(float(value))
        self.input.delete(0, 'end')
        self.input.insert(END, value)
    
    def calculate(self):
        value = float(self.input.get())
        self._update_registers(value)
        self.master.dump.edit(self.master.x44.model.value, self.master.x54.model.value)
        self.master.dump.show()
    
    def _update_registers(self, value):
        x44_value = calc_0x44(value)
        self.master.x44.update(x44_value)
        x54_value = calc_0x54(x44_value)
        self.master.x54.update(calc_0x54(x54_value))