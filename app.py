from tkinter import Tk, Frame
from unicodedata import name
from widgets.credit import Credit
from widgets.dump import Dump
from widgets.register import Register

class App(Tk):
  def __init__(self):
    super().__init__()
    self.title('Coffee Editor')
    container = Frame(self, height=550, width=700)
    container.grid_rowconfigure(3, weight=1)
    container.grid_columnconfigure(0, weight=1)
    #Widgets
    self.credit = Credit(container=self)
    self.credit.grid(row=0, column=0, sticky="w", padx=5, pady=1)
    self.x44 = Register(container=self, name="x44")
    self.x44.grid(row=1, column=0, sticky="w", padx=5, pady=1)
    self.x54 = Register(container=self, name="x54")
    self.x54.grid(row=2, column=0, sticky="w", padx=5, pady=1)
    self.dump = Dump(container=self)
    self.dump.grid(row=3, column=0, sticky="w", padx=5, pady=1)

app = App()
app.mainloop()