import itertools

def checksum(value):
    def to_base4(i):
        result = []
        while i > 0:
            result.insert(0, i % 4)
            i = i // 4
        return result
    bases = [12, 8, 4, 0]
    numerator = int(value * 100)
    sub_factor = 0
    for b in bases:
        sub_factor += numerator // 2**b
        numerator = numerator % 2**b
    result = []
    for q in to_base4(187-sub_factor):
        result.append(hex(int(q)*4)[2:].upper())
    return result

def credit(value):
    assert value <= 655.35, "Value must be lower equal than 655.35"
    bases = [14, 12, 10, 8, 6, 4, 2, 0]
    result = []
    value = int(value * 100)
    for b in bases:
        unit = value // 2**b
        value -= 2**b * unit
        result.append(f"{unit:b}".zfill(2))
    return [ hex(int(result[i] + result[i+4], 2))[2:].upper() for i in range(0, len(result) // 2)]

def read_credit(buffer):
    value = 0
    bases = [14, 12, 10, 8, 6, 4, 2, 0]
    index = 0
    for i, b in enumerate(buffer):
        if i % 2 == 0:
            continue
        value += int(b, 16) // 4 * 2**bases[index] +  int(b, 16) % 4 * 2**bases[index+4]
        index +=1
    return value / 100

def calc_0x44(value):
    ch = checksum(value)
    cr = credit(value)
    hex = "".join(list(itertools.chain(*list(zip(ch, cr)))))
    return " ".join(hex[i:i+2] for i in range(0, len(hex), 2))

def calc_0x54(reg_0x44):
    return reg_0x44[:3] + hex(int(reg_0x44[3], 16)-4)[2:].upper() + reg_0x44[4:]
