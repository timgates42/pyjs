
class Video(Widget):

    def __init__(self, src=None, **kwargs):
        obj = DOM.createElement("object")
        DOM.setAttribute(obj, "type", "application/x-mplayer2")
        DOM.setAttribute(obj, "pluginspage",
                "http://www.microsoft.com/windows/windowsmedia/default.aspx")
        self.setElement(obj)
        self.embed = DOM.createElement("embed")
        obj.appendChild(self.embed)

        if src:
            self.setSrc(src)

        Widget.__init__(self, **kwargs)

    def setWidth(self, width):
        DOM.setAttribute(self.embed, "width", width)

    def setHeight(self, height):
        DOM.setAttribute(self.embed, "height", height)

    def setControls(self, controls):
        DOM.setBooleanAttribute(self.embed, "showcontrols", controls)

    def setStatusbar(self, statusbar):
        DOM.setBooleanAttribute(self.embed, "showstatusbar", statusbar)

    def setLoop(self, autorewind):
        DOM.setBooleanAttribute(self.embed, "autorewind", autorewind)

    def setAutoplay(self, autostart):
        DOM.setBooleanAttribute(self.embed, "autostart", autostart)

