__author__ = 'Peter Bittner <peter.bittner@gmx.net>'

from pyjamas.logging.handlers import AppendHandler
from pyjamas.logging.handlers import ConsoleHandler
#from logging import *

class logging:
    """A simplified implementation of CPython's logging module for Pyjamas."""
    __levelValues = NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL = range(0, 60, 10)
    WARN = WARNING  # alias
    __severityLevels = {
        NOTSET: 'NOTSET',
        DEBUG: 'DEBUG',
        INFO: 'INFO',
        WARNING: 'WARNING',
        ERROR: 'ERROR',
        CRITICAL: 'CRITICAL'
    }
    __levelNames = __severityLevels.keys()
    __level = NOTSET
    __handler = None

    def __init__(self, level=DEBUG, handler=AppendHandler):
        """A logger, defaults: severity level DEBUG, handler AppendHandler"""
        handler.setLevel(level)
        self.__handler = handler

    def getLevelName(self, level):
        if level not in self.__levelValues:
            raise TypeError('Level must be one of: %s' % self.__levelNames)
        return self.__levelNames[level]

    def log(self, level, msg, *args, **kwargs):
        self.__handler(level, msg, *args, **kwargs)

    def debug(self, msg):
        self.log(self.DEBUG, msg)

    def info(self, msg):
        self.log(self.INFO, msg)

    def warn(self, msg):
        self.log(self.WARN, msg)

    def warning(self, msg):
        self.log(self.WARNING, msg)

    def error(self, msg):
        self.__handler('ERROR: %s' % msg)
