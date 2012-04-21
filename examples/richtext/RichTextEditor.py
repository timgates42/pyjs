from pyjamas import Event
from pyjamas import Timer
from pyjamas.ui.* import *
from pyjamas.ui.RichTextArea.Formatter import RichTextArea.Formatter

class RichTextEditor(Composite):
    #String BUTTON_WIDTH = "25px"
    
    
    def run(self):
        try  {
            Range rng = getSelection().getRange()
            if (self.m_timerRange is None)  or  (not self.m_timerRange.equals(rng)):
                onSelectionChange(rng)
                self.m_timerRange = rng
            
        
        def (self, ex):
            GWT.log("Error in timer selection", ex)
        
    
    
    def __init__(self):
        self.m_isInText = False
        self.m_lastText = ""
        self.trigger = False
        
        # Timer for trying real time selection change stuff
        self.m_timerRange = None
        self.m_selTimer = Timer()

        self.m_mainPanel = DockLayoutPanel(Unit.EM)
        self.m_toolbarPanel = HorizontalPanel()
        #self.m_toolbarPanel.setWidth("100%")
        self.m_toolbarPanel.addStyleName("timeline-RichTextToolbar")
        
        self.m_textW = RichTextArea()
        self.m_textW.addClickHandler(self.m_listener)
        self.m_textW.addKeyUpHandler(self.m_listener)
        self.m_textW.addMouseDownHandler(self.m_listener)
        self.m_textW.addBlurHandler(self.m_listener)
        self.m_textW.addMouseOutHandler(self.m_listener)
        self.m_textW.addMouseOverHandler(self.m_listener)
        # According to gwt doc, these do need to be set because this is a frame
        self.m_textW.setHeight("100%")
        self.m_textW.setWidth("100%")
        
        # Add buttons
        self.m_formatter = getFormatter()
        
        EditSymbolImageBundle icons = EditSymbolImageBundle.INST
        
        self.m_boldW = addToggleButton(self.m_toolbarPanel,
                                    icons.bold_icon(), "Bold")
        self.m_italicW = addToggleButton(self.m_toolbarPanel,
                                    icons.italics_icon(), "Italic")
        self.m_underlineW = addToggleButton(self.m_toolbarPanel,
                                    icons.underline_icon(), "Underline")
        self.m_subscriptW = addToggleButton(self.m_toolbarPanel,
                                    icons.subscript_icon(), "Subscript")
        self.m_superscriptW = addToggleButton(self.m_toolbarPanel,
                                    icons.superscript_icon(), "Superscript")
        self.m_strikethroughW = addToggleButton(self.m_toolbarPanel,
                                    icons.strikethrough_icon(), "Strikethrough")
        
        self.m_indentW = addPushButton(self.m_toolbarPanel,
                                    icons.indentmore_icon(), "Indent Right")
        self.m_outdentW = addPushButton(self.m_toolbarPanel,
                                    icons.indentless_icon(), "Indent Left")
        self.m_justifyLeftW = addPushButton(self.m_toolbarPanel,
                                    icons.justifyleft_icon(), "Justify Left")
        self.m_justifyCenterW = addPushButton(self.m_toolbarPanel,
                                    icons.justifycenter_icon(), "Justify Center")
        self.m_justifyRightW = addPushButton(self.m_toolbarPanel,
                                    icons.justifyright_icon(), "Justify Right")
        self.m_hrW = addPushButton(self.m_toolbarPanel,
                                icons.horizontalrule_icon(), "Horizontal Rule")
        self.m_olW = addPushButton(self.m_toolbarPanel,
                                icons.numberedlist_icon(), "Numbered List")
        self.m_ulW = addPushButton(self.m_toolbarPanel, icons.list_icon(), "List")
        self.m_newLinkW = addPushButton(self.m_toolbarPanel,
                                icons.link_icon(), "Link Document")
        self.m_removeFormatW = addPushButton(self.m_toolbarPanel,
                                icons.noformat_icon(), "No Format")
        
        self.m_mainPanel.addNorth(self.m_toolbarPanel, 2.0)
        self.m_mainPanel.add(self.m_textW)
        
        initWidget(self.m_mainPanel)
        #initWidget(self.m_scrollW)
        self.sinkEvents(Event.ONCLICK)
    
    def getFormatter(self):
        return self.m_textW.getFormatter()
    
    def getRichTextArea(self):
        return self.m_textW
    
    def addPushButton(self, panel, imagep, tip):
        PushButton pb = PushButton(Image(imagep))
        addAnyButton(panel, pb, tip)
        return pb
    
    
    def addToggleButton(self, panel, imagep, tip):
        ToggleButton tb = ToggleButton(Image(imagep))
        addAnyButton(panel, tb, tip)
        return tb
    
    
    def addAnyButton(self, panel, button, tip):
        button.addStyleName("richText-button")
        button.setTitle(tip)
        #button.setWidth(BUTTON_WIDTH)
        button.setHeight("100%")
        panel.add(button)
        #panel.setCellWidth(button, BUTTON_WIDTH)
        button.addClickHandler(self.m_listener)
    
    
    def onClick(self, event):
        Widget sender = (Widget)event.getSource()
        if sender == self.m_boldW:
            self.m_formatter.toggleBold()
         elif sender == self.m_italicW:
            self.m_formatter.toggleItalic()
         elif sender == self.m_underlineW:
            self.m_formatter.toggleUnderline()
         elif sender == self.m_subscriptW:
            self.m_formatter.toggleSubscript()
         elif sender == self.m_superscriptW:
            self.m_formatter.toggleSuperscript()
         elif sender == self.m_strikethroughW:
            self.m_formatter.toggleStrikethrough()
         elif sender == self.m_indentW:
            self.m_formatter.rightIndent()
         elif sender == self.m_outdentW:
            self.m_formatter.leftIndent()
         elif sender == self.m_justifyLeftW:
            self.m_formatter.setJustification(RichTextArea.Justification.LEFT)
         elif sender == self.m_justifyCenterW:
            self.m_formatter.setJustification(RichTextArea.Justification.CENTER)
         elif sender == self.m_justifyRightW:
            self.m_formatter.setJustification(RichTextArea.Justification.RIGHT)
         elif sender == self.m_hrW:
            self.m_formatter.insertHorizontalRule()
         elif sender == self.m_olW:
            self.m_formatter.insertOrderedList()
         elif sender == self.m_ulW:
            self.m_formatter.insertUnorderedList()
         elif sender == self.m_removeFormatW:
            self.m_formatter.removeFormat()
         elif sender == self.m_newLinkW:
            EventLinkPopup.open(RichTextEditor.this)
         elif sender == self.m_textW:
            updateStatus()
        
        checkForChange()
    
    def onKeyUp(self, event):
        Widget sender = (Widget)event.getSource()
        if sender == self.m_textW:
            updateStatus()
            checkForChange()
        
    def onMouseDown(self, event):
        self.trigger = True
    
    def onBlur(self, event):
        checkForChange()
    
    def onMouseOut(self, event):
        if self.m_isInText  and  isOnTextBorder(event):
            self.m_isInText = False
            captureSelection()
            endSelTimer()
        
    def onMouseOver(self, event):
        if not self.m_isInText:
            self.m_isInText = True
            self.m_textW.setFocus(True)
            self.m_lastRange = None
            startSelTimer()
            
    """*
    * This captures the selection when the mouse leaves the RTE, because in IE
    * the selection indicating the cursor position is lost once another widget
    * gains focus.  Could be implemented for IE only.
    """
    def captureSelection(self):
        try:
            self.m_lastRange = getSelection().getRange()
        
        def (self, ex):
            GWT.log("Error capturing selection for IE", ex)
        
    # Gets run every time the selection is changed
    def onSelectionChange(self, sel):
        pass
    
    def isOnTextBorder(self, event):
        Widget sender = (Widget)event.getSource()
        twX = self.m_textW.getAbsoluteLeft()
        twY = self.m_textW.getAbsoluteTop()
        x = event.getClientX() - twX
        y = event.getClientY() - twY
        width = self.m_textW.getOffsetWidth()
        height = self.m_textW.getOffsetHeight()
        return ((sender == self.m_textW)  and 
        ((x <= 0)  or  (x >= width)  or 
        (y <= 0)  or  (y >= height)))
    
    def startSelTimer(self):
        self.m_selTimer.scheduleRepeating(250)
    
    def endSelTimer(self):
        self.m_selTimer.cancel()
    
    def getRange(self):
        if self.m_lastRange is None:
            return getSelection().getRange()
        
        else:
            return self.m_lastRange
    
    def getSelection(self):
        Selection res = None
        try:
            JavaScriptObject window = getWindow()
            res = Selection.getSelection(window)
        
        def (self, ex):
            GWT.log("Error getting the selection", ex)
        
        return res
    
    def getWindow(self):
        IFrameElement frame = self.m_textW.getElement().cast()
        return getWindow(frame)
    
    def getWindow(self, iFrame):
        JS("""
        var iFrameWin = iFrame.contentWindow || iFrame.contentDocument;
        
        if( !iFrameWin.document )  {
            iFrameWin = iFrameWin.getParentNode(); //FBJS version of parentNode
        }
        return iFrameWin;
        """)
    
    
    def getDocument(self):
        return Selection.getDocument(getWindow())
    
    def setHtml(self, text):
        self.m_textW.setHTML(text)
        self.m_lastText = text
    
    def getHtml(self):
        return self.m_textW.getHTML()
    
    def checkForChange(self):
        String text = self.m_textW.getHTML()
        if not text.equals(self.m_lastText):
            NativeEvent nEvt = Document.get().createChangeEvent()
            ChangeEvent.fireNativeEvent(nEvt, RichTextEditor.this)
            self.m_lastText = text
        
    
    # Update edit buttons based on current cursor location
    def updateStatus(self):
        if self.m_formatter is None:
            return
        self.m_boldW.setDown(self.m_formatter.isBold())
        self.m_italicW.setDown(self.m_formatter.isItalic())
        self.m_underlineW.setDown(self.m_formatter.isUnderlined())
        self.m_subscriptW.setDown(self.m_formatter.isSubscript())
        self.m_superscriptW.setDown(self.m_formatter.isSuperscript())
        self.m_strikethroughW.setDown(self.m_formatter.isStrikethrough())
        
    
    
    def addChangeHandler(self, handler):
        return addDomHandler(handler, ChangeEvent.getType())
    
    


