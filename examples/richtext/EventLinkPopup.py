







from pyjamas import *
from pyjamas.ui.* import *
from pyjamas.ui.RichTextArea.Formatter import RichTextArea.Formatter



class EventLinkPopup extends DecoratedPopupPanel implements ClickHandler:
    int LABEL_WIDTH = 85
    int ROW_HEIGHT = 24
    
    RichTextEditor m_editor
    Selection m_sel
    Range m_range
    List<Text> m_selTexts
    String m_origTargetText = ""
    RangeEndPoint m_origAnchorStart
    RangeEndPoint m_origAnchorEnd
    
    TextBox m_webPageText
    TextBox m_targetText
    CheckBox m_fillOutCB
    Button m_okBut
    Button m_cancelBut
    
    def __init__(self, editor):
        super(False, True)
        m_editor = editor
        
        setGlassEnabled(True)
        
        FlowPanel vpanel = FlowPanel()
        vpanel.setWidth("300px")
        
        m_webPageText = TextBox()
        m_webPageText.setValue("http:#")
        m_webPageText.setWidth("100%")
        
        vpanel.add(m_webPageText)
        
        Label lbl = Label("Display:")
        
        m_targetText = TextBox()
        m_targetText.setWidth("100%")
        
        LayoutPanel lpanel = LayoutPanel()
        lpanel.add(lbl)
        lpanel.setWidgetLeftWidth(lbl, 0, Unit.PX, LABEL_WIDTH, Unit.PX)
        lpanel.add(m_targetText)
        lpanel.setWidgetLeftRight(m_targetText, LABEL_WIDTH, Unit.PX,
        0, Unit.PX)
        lpanel.setPixelSize(300, ROW_HEIGHT)
        
        vpanel.add(lpanel)
        
        m_fillOutCB = CheckBox("Change entire link")
        m_fillOutCB.setVisible(False)
        m_fillOutCB.addClickHandler(this)
        vpanel.add(m_fillOutCB)
        
        m_okBut = Button("Ok", this)
        m_okBut.addStyleName("float-left")
        
        m_cancelBut = Button("Cancel", this)
        m_cancelBut.addStyleName("float-left")
        
        FlowPanel hpanel = FlowPanel()
        hpanel.add(m_okBut)
        hpanel.add(m_cancelBut)
        
        vpanel.add(hpanel)
        
        setWidget(vpanel)
    
    
    def open(self, editor):
        EventLinkPopup popup = EventLinkPopup(editor)
        if popup.refresh():
            popup.center()
        else:
            popup = None
        
        return popup
    
    
    def refresh(self):
        try:
            m_sel = m_editor.getSelection()
            
            m_range = m_editor.getRange()
            if m_range is None:
                return False
            
            else:
                m_selTexts = m_range.getSelectedTextElements()
                if m_selTexts is None:
                    return False
                else:
                    m_origTargetText = m_range.getText()
                    m_targetText.setValue(m_origTargetText)
                    
                    AnchorElement anchor = getAnchor(m_selTexts)
                    if anchor is not None:
                        String href = anchor.getHref().trim()
                        if not href.isEmpty():
                            m_webPageText.setValue(href)
                        
                        
                        m_origAnchorStart = getAnchorLimit(
                        m_range.getStartPoint().getTextNode(),
                        anchor, False)
                        m_origAnchorEnd = getAnchorLimit(
                        m_range.getStartPoint().getTextNode(),
                        anchor, True)
                        
                        if m_range.getStartPoint().equals(m_origAnchorStart)  and  m_range.getStartPoint().equals(m_origAnchorEnd):
                            m_origAnchorStart = None
                            m_origAnchorEnd = None
                        
                        else:
                            m_fillOutCB.setVisible(True)
                            m_fillOutCB.setValue(True)
                            
                            m_origTargetText = fetchStringFromTexts(
                            m_origAnchorStart, m_origAnchorEnd)
                            m_targetText.setValue(m_origTargetText)
                        
                    
                
            
        
        def (self, ex):
            return False
        
        return True
    
    
    def apply(self):
        Formatter formatter = m_editor.getFormatter()
        
        String link
        link = m_webPageText.getValue().trim()
        if link.isEmpty():
            return False
        
        
        if (m_origAnchorStart is not None)  and  m_fillOutCB.getValue():
            # Expand selection to these bounds
            m_range.setRange(m_origAnchorStart, m_origAnchorEnd)
        
        # Ensure the selection hasn't changed, or at least changes to the
        # expanded bounds we want
        m_sel.setRange(m_range)
        
        String targetText = m_targetText.getValue()
        
        if m_range.isCursor():
            # Insert into a single cursor location
            AnchorElement newEle = AnchorElement.as(DOM.createAnchor())
            newEle.setHref(link)
            newEle.setInnerText(targetText)
            
            Text startNode = m_range.getStartPoint().getTextNode()
            Element parentEle = startNode.getParentElement()
            int offset = m_range.getStartPoint().getOffset()
            String text = startNode.getData()
            
            if offset == 0:
                parentEle.insertBefore(newEle, startNode)
            
            else:
                if offset < text.length():
                    # Split this in two and insert the node between
                    startNode.splitText(offset)
                
                parentEle.insertAfter(newEle, startNode)
            
            m_sel.setRange(Range(newEle))
        
        elif not targetText.equals(m_origTargetText):
            # Replace whatever was selected with this text
            Element ele = m_range.surroundContents()
            AnchorElement newEle = AnchorElement.as(DOM.createAnchor())
            newEle.setHref(link)
            newEle.setInnerText(targetText)
            ele.getParentElement().replaceChild(newEle, ele)
            
            m_sel.setRange(Range(newEle))
        else:
            formatter.createLink(link)
        
        
        return True
    
    
    def getAnchor(self, nodes):
        AnchorElement res = None
        
        for Text node : nodes:
            res = getAnchor(node)
            if res is not None:
                break
            
        
        return res
    
    
    def getAnchor(self, node):
        AnchorElement res = None
        for Element ele = node.getParentElement(); ele is not None; ele = ele.getParentElement():
            String tag = ele.getTagName()
            if tag.equalsIgnoreCase("A"):
                res = AnchorElement.as(ele)
                break
            
        
        return res
    
    
    RangeEndPoint getAnchorLimit(Text node,
    AnchorElement anchor,
    boolean forward) {
        Text prevNode
        String href = anchor.getHref()
        do {
            prevNode = node
            node = Range.getAdjacentTextElement(prevNode, forward)
            if node is not None:
                AnchorElement cmpAnchor = getAnchor(node)
                if (cmpAnchor is None)  or  not href.equals(cmpAnchor.getHref()):
                    break
                
            
         while node is not None)
        
        RangeEndPoint res = RangeEndPoint()
        res.setTextNode(prevNode)
        res.setOffset(forward ? prevNode.getData().length() : 0)
        return res
    
    
    def parseEventLink(self, href):
        long res = 0
        int idx = href.indexOf("#event=")
        if idx > 0:
            try:
                res = Long.parseLong(href.substring(idx + 7))
            
            catch (Exception ex) {}
        
        return res
    
    
    def createEventLink(self, id):
        return "#event=" + id
    
    
    def fetchStringFromTexts(self, startPoint, endPoint):
        String res = None
        List<Text> texts = Range.getSelectedTextElements(
        startPoint.getTextNode(), endPoint.getTextNode())
        if texts is not None:
            res = fetchStringFromTexts(texts, startPoint, endPoint)
        
        return res
    
    
    def fetchStringFromTexts(self, allTexts, startPoint, endPoint):
        String selText = ""
        for Text node : allTexts:
            String val = node.getData()
            if node == startPoint.getTextNode():
                if node == endPoint.getTextNode():
                    val = val.substring(startPoint.getOffset(),
                    endPoint.getOffset())
                
                else:
                    val = val.substring(startPoint.getOffset())
                
            
            elif node == endPoint.getTextNode():
                val = val.substring(0, endPoint.getOffset())
            
            selText += val
        
        return selText
    
    
    @Override
    def onClick(self, event):
        Widget sender = (Widget)event.getSource()
        if sender == m_cancelBut:
            hide()
        
        elif sender == m_okBut:
            if apply():
                hide()
            
        
        elif sender == m_fillOutCB:
            if m_fillOutCB.getValue():
                m_origTargetText = fetchStringFromTexts(m_origAnchorStart,
                m_origAnchorEnd)
                m_targetText.setValue(m_origTargetText)
            
            else:
                m_origTargetText = m_range.getText()
                m_targetText.setValue(m_origTargetText)
            
        
    
    
    def checkSuggestValid(self):
        m_okBut.setEnabled(True)
    
    {
        def execute(self):
            checkSuggestValid()
        
    
    
    def deferredCheckValid(self):
        DeferredCommand.addCommand(self)
    


