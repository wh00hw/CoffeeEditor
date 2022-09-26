from tkinter import Frame, Button, Text, filedialog, END
from models import dump as model

class Controls(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.load = Button(self, text="Load Dump", command=self.master.load)
        self.load.grid(row=0, column=0, sticky="w")
        self.save = Button(self, text="Save Dump", command=self.master.save)
        self.save.grid(row=0, column=1, sticky="w")


class Dump(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = Controls(container=self)
        self.buttons.grid(row=0, column=0, sticky="nsew")
        self.hexdump = Text(self, height=16)
        self.hexdump.grid(row=1, column=0, sticky="nsew")
        self.model = model.Dump()

    def load(self):
        self.model.filename= filedialog.askopenfilenames(
            title='Open Dump',
            initialdir='../',
            filetypes=self.model.FILETYPES
        )[0]
        self.model.read()
        value = self.model.parse()
        self.master.credit.update(value)
        self.show()
    
    def save(self):
        filename = self.model.filename.split(".")
        filename[-2] = f"{filename[-2]}_edit."
        filename = "".join(filename)
        f = filedialog.asksaveasfile(
            title='Save Dump',
            initialfile=filename,
            filetypes=self.model.FILETYPES,
            mode='wb')
        f.write(self.model.to_bytes())
        f.close()
    
    def edit(self, x44, x54):
        self.model.edit(x44, x54)
        self.show()
    
    def show(self):
        if self.hexdump.get("1.0", END) != '\n':
            self.hexdump.delete("1.0", 'end')
        self.hexdump.insert(END, self.model.print())