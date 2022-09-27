from .constants import SCMD_MCLR_GND_ON, SCMD_MCLR_GND_OFF
import contextlib

def iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True

def flatten(v):
    result = [ ]
    for i in v:
        if iterable(i):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result

@contextlib.contextmanager
def enable_MCU(pk):
    pk.run_scripts(SCMD_MCLR_GND_ON)
    try:
        pk.vdd_on()
        try:
            yield
        finally:
            pk.vdd_off()
    finally:
        pk.run_scripts(SCMD_MCLR_GND_OFF)