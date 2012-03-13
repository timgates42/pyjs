"""Use this to output (cumulatively) text at the bottom of the HTML page.
NOTE: This module is considered deprecated. It's the original implementation
for backward compatibility. Please use pyjamas.logging.debug() from now on."""

from pyjamas import logging

__logger = logging.getAppendLogger('log', logging.DEBUG, '%(message)s')

def write(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    global __logger
    __logger.debug(text)

def writebr(text):
    """@deprecated(since='0.8', replacement=logging.debug)"""
    write(text + "\n")
