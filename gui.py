from tkinter import *
from credit_calc import *
from tkinter import filedialog as fd
from hexdump import dump, hexdump, dehex
from io import StringIO
import sys

window = Tk()

class Dump:
    FILETYPES = (('Bin files', '*.bin'),)
    #(nibbles + spaces) * rows + (offset + spaces)
    START_x44 = (32 + 16) * 4 + (8 + 4)
    START_x54 = START_x44 + 32 + 14

    def __init__(self, win, x, y, callback) -> None:
        self.button = Button(
            win,
            text='Open Dump',
            command=self.select_file)
        self.button.place(x=x, y=y)
        self.save = Button(
            win,
            text='Save Dump',
            command=self.save)
        self.save.place(x=x+100, y=y)
        self.text = Text(win, height=20, width=80)
        self.text.place(x=x, y=y+30)
        self.callback = callback
        self.dump_file = None
    
    def read(self, filename):
        with open(filename, 'rb') as f:
            self.dump = dump(f.read())

    def edit(self, x44, x54):
        import pdb
        pdb.set_trace()
        self.dump = self.dump[:self.START_x44] + x44 + self.dump[self.START_x44+len(x44)+1:]
        self.dump = self.dump[:self.START_x54] + x54 + self.dump[self.START_x54+len(x54)+1:]

    def show(self):
        if self.text.get("1.0", END) != '\n':
            self.text.delete("1.0", 'end')
        tmp = sys.stdout
        xdump = StringIO()
        sys.stdout = xdump
        hexdump(dehex(self.dump))
        sys.stdout = tmp
        self.text.insert(END, xdump.getvalue())

    def parse(self):
        x44 = self.dump[self.START_x44:self.START_x44 + 8 + 3]
        x44 = x44.replace(" ", "")
        credit_input = self.button.master.children['!entry']
        credit_input.delete(0, 'end')
        credit_input.insert(END, str(read_credit(x44)))
        self.callback()

    def select_file(self):
        self.filename = fd.askopenfilename(
            title='Open Dump',
            initialdir='../',
            filetypes=self.FILETYPES)
        self.read(self.filename)
        self.parse()
        self.show()

    def save(self):
        filename = self.filename.split(".")
        filename[-2] = f"{filename[-2]}_edit."
        filename = "".join(filename)
        f = fd.asksaveasfile(
            title='Save Dump',
            initialfile=filename,
            filetypes=self.FILETYPES,
            mode='wb')
        f.write(dehex(self.dump))
        f.close()           

class Credit:
    def __init__(self, win, x, y) -> None:
        self.label=Label(win, text='Credit:')
        self.label.place(x=x, y=y)
        self.input = Entry()
        self.input.place(x=x+50, y=y)

class Register:
    def __init__(self, win, label, x, y) -> None:
        self.label=Label(win, text=label)
        self.label.place(x=x, y=y)
        self.output=Entry()
        self.output.place(x=x+50, y=y)
    
    def update(self, value):
        self.output.delete(0, 'end')
        self.output.insert(END, value)

class Editor:
    def __init__(self, win):
        #Credit Label
        self.credit = Credit(win, 10, 20)
        #Select dump
        self.dump = Dump(win, 10, 150, self.refresh)
        #Register 0x44
        self.x44 = Register(win, "0x44:", 10, 50)
        #Register 0x54
        self.x54 = Register(win, "0x54:", 10, 70)
        #Calculare Credit button
        self.button=Button(win, text='Calculate', command=self.on_calculate)
        self.button.place(x=10, y=100)
    
    def refresh(self):
        val = float(self.credit.input.get())
        x44 = calc_0x44(val)
        self.x44.update(x44)
        x54 = calc_0x54(x44)
        self.x54.update(x54)
        return x44, x54
    
    def on_calculate(self):
        x44, x54 = self.refresh()
        self.dump.edit(x44, x54)
        self.dump.show()
      


editor = Editor(window)
window.title('Coffee Editor')
window.geometry("700x550+10+10")
window.mainloop()
