#!python3
# -*- coding:utf-8 -*-
"""

"""

import select,os,sys

#from pyhislip import HiSLIP
from cPyHiSLIP import HiSLIP
#from cVXI11 import Vxi11Device
#from PyUSBTMC import USB488_device
from logging import info,warn,debug, error
import logging
#logging.getLogger().setLevel(logging.DEBUG)

class PWR(HiSLIP):
    """
    This device support only synchronized mode. So it is safe to use ask(), anytime.
    SYST:ERR?\n *ESR?
    SYST:ERR:COUN?
    STAT:OPER? /STAT:OPER:COND?
    STAT:OPER:INST?
    STAT:QUES?
    SYST:COMM:RLST? 
    FETC[<n>]:ALL?/MEAS[<n>]:ALL?
    SYSTem:ERRor:TRACe ON|OFF
    """
    def __init__(self,host="192.168.2.5"):
        super(PWR, self).__init__()
        self.connect(host)
        try:
            self.vdev=Vxi11Device(host.encode(),"inst0".encode())
        except:
            pass
        self.set_max_message_size(4096)

    def write(self, data):
        super(PWR, self).write(data)
        return self.most_recent_message_id
    
    def read_waiting(self):
        return self.read()
        
    def readstb(self):# status_query
        """
        message_types["AsyncStatusQuery"] = 21                   # C, A
        message_types["AsyncStatusResponse"] = 22                # S, A
        """
        return self.status_query()

    def OPC(self,callback=None):
        return self.ask("*OPC;\n")
        
def test(host="192.168.2.5"):
    dev=PWR(host)
    #print("actual maximum message size is:",dev.MAXIMUM_MESSAGE_SIZE)
    sys.stdout.flush()
    print("Overlap_mode:",dev.overlap_mode)
    dev.device_clear()
    print("Overlap_mode after_device clear:",dev.overlap_mode)
    dev.request_lock() # exclusive lock
    print (dev.ask(b"*IDN?;\n"))
    print (dev.ask(b"*IDN?;\n"))
    #print (dev.vdev.qIDN())
    dev.release_lock()
    print ("lock info",dev.lock_info())

    print (dev.ask(b"FETC:ALL?;\n"))
    print (dev.ask(b"MEAS:ALL?;\n"))
    return dev

def test_SRQ(dev):
    import time
    print("SRQ test:")
    dev.write(b"*CLS;\n")
    dev.write(b"TRIG:TRAN:SOUR BUS;\n")
    dev.write(b"INIT:TRAN;\n")# 'イニシエート
    print("*ESE:", dev.ask(b"*ESE?;\n"))
    print("*SRE:", dev.ask(b"*SRE?;\n"), dev.status_query())
    dev.write(b"*SRE 32;\n")
    dev.write(b"*ESE 1;\n")
    #dev.write("TRIG:TRAN;\n") # ' ソフトウェアトリガを与える
    def callback(dev=dev):
        time.sleep(1.0)
    #dev.start_SRQ_thread(callback=callback)
    s=time.time()
    #print("thread status1:",dev.srq_thread.is_alive())
    #dev.write("TRIG:TRAN;\n") # ' ソフトウェアトリガを与える
    dev.write(b"*CLS;*TRG;*OPC;\n")
    #print("thread status2:",dev.srq_thread.is_alive())
    dev.wait_Service_Request(3000)
    #r=dev.srq_thread.join()
    r=dev.wait_Service_Request(3000)
    print(r)
    e=time.time()-s
    #debug("thread status3: thread_alive:{} dt:{:.3f}".format(dev.srq_thread.is_alive(),e))
    print(dev.status_query())
    print("*SRE:", dev.ask(b"*SRE?;\n"))
    dev.write(b"*CLS;\n"); print("*STB:",
                                 dev.ask(b"*STB?;\n"), dev.status_query())
    dev.write(b"*CLS;\n"); print("CLS:", dev.status_query())
    print("*ESR", dev.ask(b"*ESR?;\n"), dev.status_query())
    print ("SYS error", dev.ask(b"SYST:ERR?;\n"))
    return 

def test_lock(dev):
    print("lock/rerease test\n")
    dev.request_lock(b"Shared Lock")
    print ("have a shared lock", dev.lock_info())
    dev.request_lock() # exclusive lock
    print ("have an exclusive lock",dev.lock_info())
    dev.release_lock()
    print ("have a shared lock",dev.lock_info())
    dev.release_lock()
    print ("have a no lock",dev.lock_info())    
    dev.request_lock() # exclusive lock
    print ("have an exclusive lock",dev.lock_info())
    dev.release_lock()
    print ("have no lock",dev.lock_info())    

def test_multi_response(dev):
    print("multi response test")
    dev.device_clear(1) # overlap_mode
    print("operation mode:",dev.overlap_mode)

    print ("ask:", dev.ask(b"*IDN?;\n"))
    print ("ask:", dev.ask(b"*IDN?;\n"))
    
    dev.write(b"*IDN?;\n")
    print("write message ID:", dev.most_recent_message_id)
    print(" response",  dev.read())

    dev.write(b"*IDN?;\n")
    print("message ID for *IDN?:", dev.most_recent_message_id)

    dev.write(b"*STB?;\n")
    print("message ID for *STB?:", dev.most_recent_message_id)
    print("response", dev.read_waiting())
    #print(dev.read_waiting())

    print ("write and ask")
    dev.write(b"*IDN?;\n")
    print("message ID for *IDN?:", dev.most_recent_message_id)
    try:
        print("Ask STB:",dev.ask(b"*STB?;\n"))
    except TypeError as m:
        print("Erro Msg",m)
    # message for "*IDN?;" is missing.
    finally:
        print("message ID for *STB?:", dev.most_recent_message_id)
        print("response",dev.read_waiting())
        #print(dev.read_waiting())
    dev.write(b"*IDN?;*STB?;\n")
    print("write message ID:", dev.most_recent_message_id)
    print("response:",dev.read_waiting())
    try:
            print("response:",dev.read_waiting())
    except:
        pass
    dev.device_clear(0) # overlap_mode
    
def test_multi_response_vxi11(dev):
    print("vxi11 test")
    dev=dev.vdev

    print ("ask:", dev.ask(b"*IDN?;\n"))
    
    dev.write(b"*IDN?;\n")
    print(" response",  dev.read())

    dev.write(b"*IDN?;\n")
    dev.write(b"*STB?;\n") # in cVXI11, the previous command will be ignored.
    print("responce",dev.read())
    print("more?", dev.read())

    dev.write(b"*IDN?;\n")
    dev.ask(b"*STB?;\n") # in cVXI11, the previous command will be ignored.
    print("responce",dev.read())

    print("response to a combined message")
    dev.write(b"*IDN?;*STB?;\n")
    print("response:",dev.read())

def main(host="192.168.2.5"):
    dev=test(host)
    test_lock(dev)
    test_multi_response(dev)
    test_SRQ(dev)
    print("make sure no more input from device\n")
    try:
        dev.read()
    except RuntimeError as e:
        #debug((e.args[0] == "HiSLIP::read poll:timeout"))
        #debug(e.args)
        debug(e)
    test_SRQ(dev)        
    test_lock(dev)

def measIt(cmd, host,loops=1000,repeat=4):
    """
    python3 -m timeit -n 200 -r 4 -s "import cPyHiSLIP;dev=cPyHiSLIP.HiSLIP(b'169.254.100.192');cmd=b'MEAS:CURR?'" "dev.write(cmd);dev.read();"
    """
    import timeit,os,sys
    setup="import cPyHiSLIP;dev=cPyHiSLIP.HiSLIP(b'{}');cmd=b'{}'".format(host,cmd)
    #setup="import cyhislip;dev=cyhislip.HiSLIP();dev.connect(b'{}');cmd=b'{}'".format(host,cmd)
    if "?" in cmd:
        target="dev.write(cmd);dev.read();"
    else:
        target="dev.write(cmd);"
    chid=os.fork()
    if chid == 0:
        sys.stdin.close()
        #print (target ,setup)
        # repeat < 5, number < 100
        # timeit funtions doesnot support clean up script. So you should terminate process after theser are used.
        print (timeit.repeat(stmt=target, setup=setup, number=loops,repeat=repeat))
        sys.stdout.close()
        sys.exit()
    else:
        os.waitpid(chid,0)
    return

if __name__ == "__main__":
    main(b"169.254.100.192")

    
