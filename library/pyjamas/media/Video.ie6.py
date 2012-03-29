
class Video(Media):

    def __init__(self, src=None, **kwargs):
        print "create object"
        obj = DOM.createElement("object")
        DOM.setAttribute(obj, "type", "application/x-mplayer2")
        #obj.pluginspage = \
        #   "http://www.microsoft.com/windows/windowsmedia/default.aspx"
        print "set element"
        self.setElement(obj)

        self.srcparam = DOM.createElement("param")
        DOM.setAttribute(self.srcparam, "name", "src")
        self.ctrlparam = DOM.createElement("param")
        DOM.setAttribute(self.ctrlparam, "name", "ShowControls")
        self.statparam = DOM.createElement("param")
        DOM.setAttribute(self.statparam, "name", "ShowStatusBar")
        self.loopparam = DOM.createElement("param")
        DOM.setAttribute(self.loopparam, "name", "autorewind")
        self.playparam = DOM.createElement("param")
        DOM.setAttribute(self.playparam, "name", "autostart")

        obj.appendChild(self.srcparam)
        obj.appendChild(self.statparam)
        obj.appendChild(self.loopparam)
        obj.appendChild(self.ctrlparam)
        obj.appendChild(self.playparam)

        print "widget init"
        Media.__init__(self, **kwargs)

        print "setSrc"
        if src:
            self.setSrc(src)

    def setSrc(self, src):
        print "setSrc", src
        DOM.setAttribute(self.srcparam, "value", src)

    def setWidth(self, width):
        print "setWidth", width
        DOM.setAttribute(self.element, "width", width)

    def setHeight(self, height):
        print "setHeight", height
        DOM.setAttribute(self.element, "height", height)

    def setControls(self, controls):
        print "setControls", controls
        DOM.setBooleanAttribute(self.ctrlparam, "value", controls)

    def setStatusbar(self, statusbar):
        DOM.setBooleanAttribute(self.statparam, "value", statusbar)

    def setLoop(self, autorewind):
        DOM.setBooleanAttribute(self.loopparam, "value", autorewind)

    def setAutoplay(self, autostart):
        DOM.setBooleanAttribute(self.playparam, "value", autostart)

