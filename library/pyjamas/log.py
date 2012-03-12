"""Use this to output (cumulatively) text at the bottom of the HTML page.
NOTE: This module is considered deprecated. It's the original implementation
for backward compatibility. Please use pyjamas.logging.debug() from now on."""

from pyjamas import DOM
#from pyjamas import logging
from __pyjamas__ import doc

__data = ""
__element = None
#__logger = logging.getLogger('pyjs')

def __getBodyElement():
    return doc().body

def __add_elem():
    global __element
    if __element is not None:
        return
    __element = DOM.createDiv()
    DOM.appendChild(__getBodyElement(), __element)

def write(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    global __data
    __add_elem()
    text = text.replace("\n", "<br />\n")
    __data += text
    DOM.setInnerHTML(__element, __data)

def writebr(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    write(text + "\n")
