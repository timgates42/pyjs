"""
A modification of pyjamas DeferredMethod
@author: Tobias Weber
@contact: tobi-weber@gmx.de
"""

from pyjamas.Timer import Timer 
from pyjamas import logging

log = logging.getAppendLogger(__name__, logging.DEBUG, logging.PLAIN_FORMAT)

global deferredHandlers
deferredHandlers = []
global timerIsActive
timerIsActive = False 
   
def add(handler, arguments=[]):
    deferredHandlers.append([handler, arguments])
    maybeSetDeferredHandlerTimer()
  
def flushDeferredHandlers():
    for i in range(len(deferredHandlers)):
        current = deferredHandlers[0]
        del deferredHandlers[0]
        if current:
            handler = current[0]
            args = current[1]
            handler(*args)
    
def maybeSetDeferredHandlerTimer():
    global timerIsActive
    
    if (not timerIsActive) and (not len(deferredHandlers)==0):
        Timer(1, onTimer)
        timerIsActive = True
  
def onTimer(t):
    global timerIsActive
    
    flushDeferredHandlers()
    timerIsActive = False
    maybeSetDeferredHandlerTimer() 