#!/usr/bin/python

from flask import Flask, g
import IcomControl


app = Flask(__name__)


def icom():
    if not hasattr(g, 'icom'):
        g.icom = IcomControl.IcomControl('/dev/ttyUSB0', 19200, "\x77")
        print "Icom init"
    return g.icom

@app.route('/setfreq')
def setfreq(frequency):
    icom().setFrequency(frequency)

@app.route('/getfreq')
def getfreq():
    return str(icom().getFrequency())

@app.route('/getmodefilter')
def getmodefilter():
    mode, flt = icom().getModeFilter()
    return "Mode: " + mode + " | Filter: " + flt


if __name__ == "__main__":
    app.run(host='0.0.0.0')
