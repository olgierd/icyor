#!/usr/bin/python3

import serial


class IcomControl:
    def __init__(self, port, baudrate, civ_addr, debug=0):
        self.CIV_ADDR = civ_addr
        self.s = serial.Serial(port, baudrate)
        self.debug = debug
        self.modes = {"LSB": 0, "USB": 1, "AM": 2, "CW": 3, "RTTY": 4, "FM": 5, "CWR": 7, "RTTYR": 8}
        self.filters = {"WIDE": 1, "NARROW": 2}

    def sendCommand(self, payload, resp_len, noack=0):
        cmd = '\xFE\xFE'+self.CIV_ADDR+'\xE0'+payload+'\xFD'
        if self.debug:
            print([hex(ord(x)) for x in cmd])
        self.s.write(cmd)
        if noack:
            return
        answer = self.s.read(resp_len+6)  # 6 = 5 bytes preamle + 1 stop byte
        return answer[5:-1]

    def strToBCD(self, f):
        tab = [chr(int(f[::-1][x:x+2][::-1], 16)) for x in range(0, len(f), 2)]
        tab = tab + (5-len(tab))*["\x00"]
        return ''.join(tab)

    # 0x00 set frequency
    def setFrequency(self, f):
        value = self.strToBCD(str(f))
        cmd = "\x00" + value
        self.sendCommand(cmd, 0, noack=1)

    # 0x01 set mode/filter
    def setModeFilter(self, mode, flt):
        if mode not in self.modes or flt not in self.filters:
            return
        cmd = "\x01" + chr(self.modes[mode]) + chr(self.filters[flt])
        self.sendCommand(cmd, 0, noack=1)

    # 0x03 read frequency
    def getFrequency(self):
        cmd = "\x03"
        ans = self.sendCommand(cmd, 5)
        frequency = ''.join([format(ord(x), "02x")[::-1] for x in ans])[::-1]
        return int(frequency)

    # 0x04 read mode/filter
    def getModeFilter(self):
        cmd = "\x04"
        ans = self.sendCommand(cmd, 2)
        return self.modes[ord(ans[0])], self.filters[ord(ans[1])]

    # 0x07 select VFO
    def setVFO(self, vfo):
        vfos = {"A": "\x00", "B": "\x01", "EQUAL": "\xA0", "SWAP": "\xB0"}
        if vfo not in vfos:
            return
        cmd = "\x07" + vfo
        self.sendCommand(cmd, 0)

    # 0x12 set antenna
    def setAntenna(self, ant):
        if ant not in [1, 2]:
            return
        cmd = "\x12" + chr(ant-1)
        self.sendCommand(cmd, 0)

    # 0x14 set parameter
    def setParameter(self, parameter, value):
        if value < 0 or value > 255:
            return
        cmd = "\x14" + "\x0C" + chr(int(str(value/100), 16)) + chr(int(str(value % 100), 16))
        self.sendCommand(cmd, 0)

    def toggleFilter(self):
        mode, flt = self.getModeFilter()
        self.setModeFilter(mode, "NARROW" if flt == "WIDE" else "NARROW")
