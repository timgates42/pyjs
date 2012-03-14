"""Logging handlers for Pyjamas logging based on CPython's logging handlers."""
__author__ = 'Peter Bittner <peter.bittner@gmx.net>'

from logging import Handler
from pyjamas import DOM, Window
from __pyjamas__ import doc, JS

class AlertHandler(Handler):
    """A log output handler displaying any log message using an alert popup."""
    def __init__(self):
        super(AlertHandler, self).__init__()

    def emit(self, record):
        msg = self.format(record)
        Window.alert(msg)

class AppendHandler(Handler):
    """A log output handler showing text in a <div> appended to the end of the
    HTML document. Use the 'div' property to find out the element's ID if you
    want to position or style the output in your Pyjamas application."""
    div = None
    div_id = ''
    output = ''

    def __init__(self, logger_name):
        super(AppendHandler, self).__init__()
        self.div_id = "logging_" + logger_name
        self.div_id = self.div_id.replace(' ', '_').replace('.', '')

    def __addLogElement(self):
        """Add a container in the DOM where logging output will be written to.
        This cannot be done in the constructor as it must happen late enough
        to ensure a document body (to add an element to) does already exist."""
        if self.div == None:
            self.div = DOM.createDiv()
            self.div.setAttribute('id', self.div_id)
            DOM.appendChild(doc().body, self.div)

    def emit(self, record):
        msg = self.format(record)
        msg = msg.replace("\n", "<br/>\n") + "<br/>\n"
        self.output += msg
        self.__addLogElement()
        DOM.setInnerHTML(self.div, self.output)

class ConsoleHandler(Handler):
    """A log output handler making use of Firebug's console.log() function."""
    def __init__(self):
        super(ConsoleHandler, self).__init__()

    def emit(self, record):
        msg = self.format(record)
        msg = msg.replace("'", "\\'")
        JS(" console.log(@{{msg}}); ")

