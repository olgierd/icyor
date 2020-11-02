#!/usr/bin/python3

import IcomControl

# icom = IcomControl.IcomControl('/dev/ttyUSB0', 19200, "\x77")
icom = IcomControl.IcomControl('/dev/ttyS0', 19200, "\x77")

icom.setAntenna(1)
icom.setModeFilter("CWR", "NARROW")
icom.setFrequency(143049850)
print(icom.getFrequency())
mode, flt = icom.getModeFilter()

print(f"Mode: {mode} | Filter: {flt}")
