
class Video(Media):

    def __init__(self, src=None, **kwargs):
        print "create object"
        obj = DOM.createElement("OBJECT")
        DOM.setAttribute(obj, "type", "application/x-mplayer2")
        #DOM.setAttribute(obj, "type", "application/x-oleobject")
        #DOM.setAttribute(obj, "classid",
                                #"CLSID:22D6F312-B0F6-11D0-94AB-0080C74C7E95")
                                #"CLSID:6BF52A52-394A-11d3-B153-00C04F79FAA6")
        print "set element"
        self.setElement(obj)

        print "widget init"
        Media.__init__(self, **kwargs)

        #self.dispparam = DOM.createElement("PARAM")
        #DOM.setAttribute(self.dispparam, "NAME", "ShowDisplay")
        #DOM.setBooleanAttribute(self.dispparam, "VALUE", "false")
        #self.getElement().appendChild(self.dispparam)

        print "setSrc"
        if src:
            self.setSrc(src)

    def setSrc(self, src):
        print "setSrc", src
        self.srcparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.srcparam, "NAME", "FileName")
        DOM.setAttribute(self.srcparam, "VALUE", src)
        self.getElement().appendChild(self.srcparam)
        #obj = self.getElement()
        #obj.URL = src

    def setControls(self, controls):
        print "setControls", controls
        self.ctrlparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.ctrlparam, "NAME", "ShowControls")
        DOM.setBooleanAttribute(self.ctrlparam, "VALUE",
            controls and "true" or "false")
        self.getElement().appendChild(self.ctrlparam)

    def setStatusbar(self, statusbar):
        print "setstatus", statusbar
        self.statparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.statparam, "NAME", "ShowStatusBar")
        DOM.setBooleanAttribute(self.statparam, "VALUE",
            statusbar and "true" or "false")
        self.getElement().appendChild(self.statparam)

    def setLoop(self, autorewind):
        print "autorewind", autorewind
        self.loopparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.loopparam, "NAME", "autorewind")
        DOM.setBooleanAttribute(self.loopparam, "VALUE", 
            autorewind and "true" or "false")
        self.getElement().appendChild(self.loopparam)

    def setAutoplay(self, autostart):
        print "autoplay", autostart
        self.playparam = DOM.createElement("PARAM")
        DOM.setAttribute(self.playparam, "NAME", "autostart")
        DOM.setBooleanAttribute(self.playparam, "VALUE", 
            autostart and "true" or "false")
        self.getElement().appendChild(self.playparam)

