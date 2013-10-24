import gevent
import time
from gevent import Timeout
from gevent import monkey
monkey.patch_all()
from gevent.queue import Queue

class TaskComplete(Exception):
    pass

class Worker():
    def __init__(self,inputdict, timeout, outputmode, validation_func):
        self.threads = []
        self.queue = Queue()
        self.inputdict = inputdict
        self.timeout = timeout
        self.outputmode = outputmode
        self.validation_func = validation_func
 
    
    def infi(self, th, thm):
        k = 0
        while k<10000:
	    print 'I am in INFI ', th, thm
            time.sleep(.1)
        print "out while infi", thm
        self.queue.put_nowait(thm)
        
    
    def test(self, th, thm):
        print "inside test", thm
        self.queue.put_nowait(thm)
    
    def start(self, thm):
        print "Hii"
        self.threads.append(gevent.spawn(self.infi, 1, thm))
	self.threads.append(gevent.spawn(self.test, 2, thm))
	while self.queue.empty():
	    print "queue is empty %s" % thm
	    gevent.sleep(0)
        raise TaskComplete
        
    def stop(self):
	gevent.killall(self.threads)

def maingreenlet(inputdict, timeout, outputmode, validation_func):
    rg = Worker(inputdict, timeout, outputmode, validation_func)
    i = 0
    try:
        gevent.with_timeout(5, rg.start, i)
    except Timeout:
        print 'Exception of timeout'
	rg.stop()
	print 'Exiting all greenlets'
    except TaskComplete:
        print "Task complete message from queue" ,rg.queue.get()
    except:
	print "Hahahahah"

maingreenlet('','','','') 
