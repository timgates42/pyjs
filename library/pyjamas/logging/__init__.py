"""Logging module for Pyjamas, mimicking CPython's logging module."""
__author__ = 'Peter Bittner <peter.bittner@gmx.net>'

from pyjamas.logging.handlers import AppendHandler
from pyjamas.logging.handlers import ConsoleHandler
# blatantly copy everything from CPython's logging
from logging import *

PYJS_NAME = 'pyjs'

def getPrintLogger(fmt=BASIC_FORMAT, level=DEBUG, name=PYJS_NAME):
    """A logger that prints text to cout, the default output stream"""
    formatter = Formatter(fmt)
    handler = StreamHandler()
    handler.setFormatter(formatter)
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def getAppendLogger(fmt=BASIC_FORMAT, level=DEBUG, name=PYJS_NAME):
    """A logger that appends text to the end of the HTML document body"""
    formatter = Formatter(fmt)
    handler = AppendHandler()
    handler.setFormatter(formatter)
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def getConsoleLogger(fmt=BASIC_FORMAT, level=DEBUG, name=PYJS_NAME):
    """A logger that uses Firebug's console.log() function"""
    formatter = Formatter(fmt)
    handler = ConsoleHandler()
    handler.setFormatter(formatter)
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
