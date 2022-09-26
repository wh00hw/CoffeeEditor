from tkinter import Tk, Frame
from widgets.credit import Credit
from widgets.dump import Dump

class App(Tk):
  def __init__(self):
    super().__init__()
    self.title('Coffee Editor')
    container = Frame(self, height=550, width=700)
    container.grid_rowconfigure(1, weight=1)
    container.grid_columnconfigure(0, weight=1)
    #Widgets
    self.credit = Credit(container=self)
    self.credit.grid(row=0, column=0, sticky="w", padx=5, pady=1)
    self.dump = Dump(container=self)
    self.dump.grid(row=1, column=0, sticky="w", padx=5, pady=1)


app = App()
app.mainloop()
  