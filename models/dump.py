from hexdump import dump, hexdump, dehex
from tools.credit_calc import read_credit
from io import StringIO
import sys

class Dump:
    FILETYPES = (('Bin files', '*.bin'),)
    #(nibbles + spaces) * rows + (offset + spaces)
    START_x44 = 204 #(32 + 16) * 4 + (8 + 4)
    START_x54 = 252 #START_x44 + 32 + 14
    OFFSET = 11

    def __init__(self) -> None:
        self.dump = None
        self.filename = None
    
    def read(self):
        with open(self.filename, 'rb') as f:
            self.dump = dump(f.read())
    
    def edit(self, x44, x54):
        old_x44 = self.dump[self.START_x44:self.START_x44+self.OFFSET]
        self.dump = self.dump.replace(old_x44, x44)
        old_x54 = self.dump[self.START_x54:self.START_x54+self.OFFSET]
        self.dump = self.dump.replace(old_x54, x54)

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