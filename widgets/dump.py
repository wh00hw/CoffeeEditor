from tkinter import Frame, Button, Label, Text, END, messagebox
from models import dump as model
from tkfilebrowser import askopenfilename, asksaveasfilename
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
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = Controls(container=self)
        self.buttons.grid(row=0, column=0, sticky="w")
        self.label = Label(self)
        self.label.grid(row=1, column=0, sticky="w")
        self.hexdump = Text(self, height=16)
        self.hexdump.grid(row=2, column=0, sticky="w")
        self.model = model.Dump()

    def load(self):
        self.model.filename= askopenfilename(
            title='Open Dump',
            initialdir='../',
            filetypes=self.model.FILETYPES)
        self.label.config(text=f"File: {self.model.filename}")
        self.model.read()
        value = self.model.parse()
        self.master.credit.update(value)
        self.show()
    
    def save(self):
        filename = self.model.filename.split(".")
        filename[-2] = f"{filename[-2]}_edit."
        filename = "".join(filename)
        file_path = asksaveasfilename(
            title='Save Dump',
            initialdir='../',
            initialfile=filename,
            filetypes=self.model.FILETYPES)
        with open(file_path, "wb") as f:
            f.write(self.model.to_bytes())
            f.close()
        messagebox.showinfo(title="Save", message="Success!!")
    
    def edit(self, x44, x54):
        self.model.edit(x44, x54)
        self.show()
    
    def show(self):
        if self.hexdump.get("1.0", END) != '\n':
            self.hexdump.delete("1.0", 'end')
        self.hexdump.insert(END, self.model.print())