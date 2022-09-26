from hexdump import dump, hexdump, dehex
from utils.credit_calc import read_credit
from io import StringIO
import sys

class Dump:
    FILETYPES = (('Bin files', '*.bin'),)
    #(nibbles + spaces) * rows + (offset + spaces)
    START_x44 = (32 + 16) * 4 + (8 + 4)
    START_x54 = START_x44 + 32 + 14

    def __init__(self) -> None:
        self.dump = None
        self.filename = None
    
    def read(self):
        with open(self.filename, 'rb') as f:
            self.dump = dump(f.read())
    
    def edit(self, x44, x54):
        self.dump = self.dump[:self.START_x44] + x44 + self.dump[self.START_x44+len(x44)+1:]
        self.dump = self.dump[:self.START_x54] + x54 + self.dump[self.START_x54+len(x54)+1:]

    def print(self):
        tmp = sys.stdout
        xdump = StringIO()
        sys.stdout = xdump
        hexdump(dehex(self.dump))
        sys.stdout = tmp
        return xdump.getvalue()
    
    def parse(self):
        x44 = self.dump[self.START_x44:self.START_x44 + 8 + 3]
        x44 = x44.replace(" ", "")
        return str(read_credit(x44))
    
    def to_bytes(self):
        return dehex(self.dump)