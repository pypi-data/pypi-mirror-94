#!python
# -*- coding:utf-8 -*-

import cPyHiSLIP
import time,sys

def test():
    #dev=cPyHiSLIP.HiSLIP(b"172.28.68.228")
    dev=cPyHiSLIP.HiSLIP(b"169.254.29.115")
    print (dev.ask(b"*IDN?"))
    dev.write(b":WAV:SOUR CHAN1;")
    dev.write(b":WAV:POIN 1000000;")
    print ("Point:",dev.ask(b":WAV:POIN?;"))
    while 1:
        dev.ask(b":SINGLE;*OPC?")
        #print(dev.ask(b"*STB;"),end=",")
        # dev.write(b":WAV:DATA?")
        # #time.sleep(0.5)
        # wf=dev.read()
        wf=dev.ask(b":WAV:DATA?")
        print (len(wf),end=", ")
        sys.stdout.flush()
        del wf
    dev.write(b":STOP;")

def test_kikusui():
    dev=cPyHiSLIP.HiSLIP(b"169.254.100.192") # Kikusui PS . no
    print (dev.ask(b"*IDN?"))
    dev.write(b":WAV:SOUR CHAN1;")
    dev.write(b":WAV:POIN 1000000;")
    print ("Point:",dev.ask(b":WAV:POIN?;"))
    while 1:
        dev.ask(b":SINGLE;*OPC?")
        #print(dev.ask(b"*STB;"),end=",")
        # dev.write(b":WAV:DATA?")
        # #time.sleep(0.5)
        # wf=dev.read()
        wf=dev.ask(b":WAV:DATA?")
        print (len(wf),end=", ")
        sys.stdout.flush()
        del wf
    dev.write(b":STOP;")

if __name__ == "__main__":
    test()
    

