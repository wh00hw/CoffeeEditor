
from .constants import *
from .utils import flatten
import usb.core

EEPROM_24LC_FAMILY = {'FamilyID': 10, 'FamilyType': 13, 'SearchPriority': 13, 'FamilyName': 'EEPROMS/24LC', 'ProgEntryScript': 191, 'ProgExitScript': 192, 'ReadDevIDScript': 0, 'DeviceIDMask': 0, 'BlankValue': 255, 'BytesPerLocation': 1, 'AddressIncrement': 1, 'PartDetect': False, 'ProgEntryVPPScript': 0, 'UNUSED1': 0, 'EEMemBytesPerWord': 0, 'EEMemAddressIncrement': 0, 'UserIDHexBytes': 0, 'UserIDBytes': 0, 'ProgMemHexBytes': 1, 'EEMemHexBytes': 0, 'ProgMemShift': 0, 'TestMemoryStart': 0, 'TestMemoryLength': 0, 'Vpp': 0.0}
EEPROM_24LC02B_PART = {'PartName': '24LC02B', 'Family': 10, 'DeviceID': 4294967295, 'ProgramMem': 256, 'EEMem': 0, 'EEAddr': 0, 'ConfigWords': 0, 'ConfigAddr': 0, 'UserIDWords': 0, 'UserIDAddr': 0, 'BandGapMask': 0, 'ConfigMasks': [1, 255, 8, 0, 0, 0, 0, 0, 0], 'ConfigBlank': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'CPMask': 0, 'CPConfig': 0, 'OSSCALSave': False, 'IgnoreAddress': 0, 'VddMin': 3.299999952316284, 'VddMax': 5.0, 'VddErase': 3.299999952316284, 'CalibrationWords': 0, 'ChipEraseScript': 183, 'ProgMemAddrSetScript': 193, 'ProgMemAddrBytes': 3, 'ProgMemRdScript': 194, 'ProgMemRdWords': 64, 'EERdPrepScript': 0, 'EERdScript': 0, 'EERdLocations': 0, 'UserIDRdPrepScript': 0, 'UserIDRdScript': 0, 'ConfigRdPrepScript': 0, 'ConfigRdScript': 0, 'ProgMemWrPrepScript': 0, 'ProgMemWrScript': 195, 'ProgMemWrWords': 8, 'ProgMemPanelBufs': 0, 'ProgMemPanelOffset': 0, 'EEWrPrepScript': 0, 'EEWrScript': 0, 'EEWrLocations': 0, 'UserIDWrPrepScript': 0, 'UserIDWrScript': 0, 'ConfigWrPrepScript': 0, 'ConfigWrScript': 0, 'OSCCALRdScript': 0, 'OSCCALWrScript': 0, 'DPMask': 0, 'WriteCfgOnErase': False, 'BlankCheckSkipUsrIDs': False, 'IgnoreBytes': 0, 'ChipErasePrepScript': 0, 'BootFlash': 0, 'Config9Mask': 0, 'Config9Blank': 0, 'ProgMemEraseScript': 0, 'EEMemEraseScript': 0, 'ConfigMemEraseScript': 0, 'reserved1EraseScript': 0, 'reserved2EraseScript': 0, 'TestMemoryRdScript': 0, 'TestMemoryRdWords': 0, 'EERowEraseScript': 0, 'EERowEraseWords': 0, 'ExportToMPLAB': False, 'DebugHaltScript': 0, 'DebugRunScript': 0, 'DebugStatusScript': 0, 'DebugReadExecVerScript': 0, 'DebugSingleStepScript': 0, 'DebugBulkWrDataScript': 0, 'DebugBulkRdDataScript': 0, 'DebugWriteVectorScript': 0, 'DebugReadVectorScript': 0, 'DebugRowEraseScript': 0, 'DebugRowEraseSize': 0, 'DebugReserved5Script': 0, 'DebugReserved6Script': 0, 'DebugReserved7Script': 0, 'DebugReserved8Script': 0, 'LVPScript': 0}
class PICkit:
    def __init__(self):
        self.default_speed = 0

        ### multiple programmers on the bus? f'it. assume one.
        self.device = usb.core.find(idVendor=ID_VENDOR,
                                    idProduct=ID_PRODUCT)
        #print('FOUND:', self.device)

        ### Ignore the various race/reset issues with configurations
        ### http://libusb.sourceforge.net/api-1.0/libusb_caveats.html#configsel
        self.device.set_configuration(CONFIG_VENDOR)

        interface = self.device.get_active_configuration()[0,0]
        endpoints = interface.endpoints()

        ### for now, don't worry about !=2 endpoints
        assert len(endpoints) == 2
        if endpoints[0].bEndpointAddress == ENDPOINT_IN:
            self.ep_in = endpoints[0]
            self.ep_out = endpoints[1]
        else:
            self.ep_in = endpoints[1]
            self.ep_out = endpoints[0]
        assert self.ep_in.bEndpointAddress == ENDPOINT_IN
        assert self.ep_out.bEndpointAddress == ENDPOINT_OUT

        ### claim the interface?

        self.write(FWCMD_FIRMWARE_VERSION)
        result = self.read(3)
        ### check for bootloader mode
        print('VERSION:', tuple(result))

    def write(self, *values):
        v = bytes(flatten(values))  # ensures all values in [0,255]
        #print('WRITE:', v)
        #if v[0] != FWCMD_FIRMWARE_VERSION: return
        return self.ep_out.write(v)

    def read(self, amt=64):
        ### ignore AMT. read frames are always 64 bytes.
        ### what to do?
        assert amt <= 64
        return bytes(self.ep_in.read(64))[:amt]

    def run_scripts(self, *args):
        flat = flatten(args)
        return self.write(FWCMD_EXECUTE_SCRIPT,
                          len(flat),
                          flat,
                          )

    def vdd_on(self):
        # REFERENCE: CPICkitFunctions::VddOn()
        ### NOTE: assume targetSelfPowered = False
        return self.run_scripts(SCMD_VDD_GND_OFF,
                                SCMD_VDD_ON,
                                )

    def vdd_off(self):
        # REFERENCE: CPICkitFunctions::VddOff()
        ### NOTE: assume targetSelfPowered = False
        return self.run_scripts(SCMD_VDD_OFF,
                                SCMD_VDD_GND_ON,
                                )

    def set_speed(self, speed=None):
        # REFERENCE: CPICkitFunctions::SetProgrammingSpeed()
        if speed is None:
            speed = self.default_speed
        self.run_scripts(SCMD_SET_ICSP_SPEED,
                         speed,
                         )

    def set_vdd(self, voltage, threshold):
        # REFERENCE: CPICkitFunctions::SetVDDVoltage()

        voltage = max(voltage, 2.5)

        ### magic. need explanation
        ccp = int((voltage*32 + 10.5) * 64)
        fault = min((threshold*voltage / 5) * 255, 210.0)

        return self.write(
            FWCMD_SETVDD,
            ccp &  0x0FF,  # low-byte
            ccp // 0x100,  # high-byte
            int(fault),
            )

    def set_vpp(self, voltage, threshold):
        # REFERENCE: CPICkitFunctions::SetVppVoltage()

        ### magic. need explanation
        vppADC = voltage * 18.61
        vFault = threshold * voltage * 1.61

        return self.write(
            FWCMD_SETVPP,
            0x40,  # cppValue
            int(vppADC),
            int(vFault),
            )
