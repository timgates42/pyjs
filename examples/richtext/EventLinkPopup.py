from pyjamas import DOM
from pyjamas.ui.PopupPanel import PopupPanel
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.Button import Button
from pyjamas.ui.TextBox import TextBox

import traceback

LABEL_WIDTH = 85
ROW_HEIGHT = 24

def open(editor):
    popup = EventLinkPopup(editor)
    if popup.refresh():
        popup.center()
    else:
        popup = None

    return popup

class EventLinkPopup(PopupPanel):

    def __init__(self, editor):
        PopupPanel.__init__(self, False, True)

        self.m_origTargetText = ""
        self.m_editor = editor

        self.setGlassEnabled(True)

        vpanel = FlowPanel()
        vpanel.setWidth("300px")

        self.m_webPageText = TextBox()
        self.m_webPageText.setText("http:#")
        self.m_webPageText.setWidth("100%")

        vpanel.add(self.m_webPageText)

        lbl = Label("Display:")

        self.m_targetText = TextBox()
        self.m_targetText.setWidth("100%")

        lpanel = HorizontalPanel()
        lpanel.add(lbl)
        #lpanel.setWidgetLeftWidth(lbl, 0, Unit.PX, LABEL_WIDTH, Unit.PX)
        lpanel.add(self.m_targetText)
        #lpanel.setWidgetLeftRight(self.m_targetText, LABEL_WIDTH, Unit.PX,
        #0, Unit.PX)
        #lpanel.setPixelSize(300, ROW_HEIGHT)

        vpanel.add(lpanel)

        self.m_fillOutCB = CheckBox("Change entire link")
        self.m_fillOutCB.setVisible(False)
        self.m_fillOutCB.addClickListener(self)
        vpanel.add(self.m_fillOutCB)

        self.m_okBut = Button("Ok", self)
        self.m_okBut.addStyleName("float-left")

        self.m_cancelBut = Button("Cancel", self)
        self.m_cancelBut.addStyleName("float-left")

        hpanel = FlowPanel()
        hpanel.add(self.m_okBut)
        hpanel.add(self.m_cancelBut)

        vpanel.add(hpanel)

        self.add(vpanel)
        self.show()

    def refresh(self):
        try:
            self.m_sel = self.m_editor.getSelection()

            self.m_range = self.m_editor.getRange()
            if self.m_range is None:
                return False
            else:
                self.m_selTexts = self.m_range.getSelectedTextElements()
                if self.m_selTexts is None:
                    return False
                else:
                    self.m_origTargetText = self.m_range.getText()
                    self.m_targetText.setValue(self.m_origTargetText)

                    anchor = getAnchor(self.m_selTexts)
                    if anchor is not None:
                        href = anchor.getHref().strip()
                        if href:
                            self.m_webPageText.setValue(href)

                        self.m_origAnchorStart = self.getAnchorLimit(
                                self.m_range.getStartPoint().getTextNode(),
                                anchor, False)
                        self.m_origAnchorEnd = self.getAnchorLimit(
                                self.m_range.getStartPoint().getTextNode(),
                                anchor, True)

                        if self.m_range.getStartPoint().equals(self.m_origAnchorStart)  and  self.m_range.getStartPoint().equals(self.m_origAnchorEnd):
                            self.m_origAnchorStart = None
                            self.m_origAnchorEnd = None

                        else:
                            self.m_fillOutCB.setVisible(True)
                            self.m_fillOutCB.setValue(True)

                            self.m_origTargetText = self.fetchStringFromTexts(
                                self.m_origAnchorStart, self.m_origAnchorEnd)
                            self.m_targetText.setText(self.m_origTargetText)





        except:
            print "exception"
            traceback.print_exc()
            return False

        return True


    def _apply(self):
        formatter = self.m_editor.getFormatter()

        link = self.m_webPageText.getText().strip()
        if not link:
            return False

        print self.m_origAnchorStart, self.m_origAnchorEnd

        if (self.m_origAnchorStart is not None)  and  self.m_fillOutCB.getValue():
            # Expand selection to these bounds
            self.m_range.setRange(self.m_origAnchorStart, self.m_origAnchorEnd)

        # Ensure the selection hasn't changed, or at least changes to the
        # expanded bounds we want
        self.m_sel.setRange(self.m_range)

        targetText = self.m_targetText.getValue()

        if self.m_range.isCursor():
            # Insert into a single cursor location
            newEle = DOM.createAnchor()
            newEle.setHref(link)
            newEle.setInnerText(targetText)

            startNode = self.m_range.getStartPoint().getTextNode()
            parentEle = startNode.getParentElement()
            offset = self.m_range.getStartPoint().getOffset()
            text = startNode.getData()

            if offset == 0:
                parentEle.insertBefore(newEle, startNode)

            else:
                if offset < text.length():
                    # Split this in two and insert the node between
                    startNode.splitText(offset)

                parentEle.insertAfter(newEle, startNode)

            self.m_sel.setRange(Range(newEle))

        elif not targetText.equals(self.m_origTargetText):
            # Replace whatever was selected with this text
            ele = self.m_range.surroundContents()
            newEle = DOM.createAnchor()
            newEle.setHref(link)
            newEle.setInnerText(targetText)
            ele.getParentElement().replaceChild(newEle, ele)

            self.m_sel.setRange(Range(newEle))
        else:
            formatter.createLink(link)


        return True


    def getAnchor(self, nodes):
        res = None

        for node in nodes:
            res = getAnchor(node)
            if res is not None:
                break

        return res


    def getAnchor(self, node):
        res = None
        ele = node.getParentElement()
        while ele is not None:
            tag = ele.getTagName()
            if tag.lower == "a":
                res = ele
                break

            ele = ele.getParentElement()

        return res


    def getAnchorLimit(self, node, anchor, forward):
        href = anchor.getHref()
        while True:
            prevNode = node
            node = Range.getAdjacentTextElement(prevNode, forward)
            if node is not None:
                cmpAnchor = getAnchor(node)
                if (cmpAnchor is None) or not href == cmpAnchor.getHref():
                    break

            if node is None:
                break

        res = RangeEndPoint()
        res.setTextNode(prevNode)
        res.setOffset(forward and prevNode.getData().length() or 0)
        return res


    def parseEventLink(self, href):
        res = 0
        idx = href.index("#event=")
        if idx > 0:
            try:
                res = href[idx+7:]
            except:
                pass

        return res


    def createEventLink(self, id):
        return "#event=" + id


    def fetchStringFromTexts(self, startPoint, endPoint):
        res = None
        texts = Range.getSelectedTextElements(
                        startPoint.getTextNode(), endPoint.getTextNode())
        if texts is not None:
            res = self.fetchStringFromTexts(texts, startPoint, endPoint)

        return res


    def fetchStringFromTexts(self, allTexts, startPoint, endPoint):
        selText = ""
        for node in allTexts:
            val = node.getData()
            if node == startPoint.getTextNode():
                if node == endPoint.getTextNode():
                    val = val.substring[startPoint.getOffset():
                                        endPoint.getOffset()]

                else:
                    val = val[startPoint.getOffset():]


            elif node == endPoint.getTextNode():
                val = val[:endPoint.getOffset()]

            selText += val

        return selText

    def onClick(self, sender):
        if sender == self.m_cancelBut:
            hide()

        elif sender == self.m_okBut:
            if self._apply():
                hide()

        elif sender == self.m_fillOutCB:
            if self.m_fillOutCB.getValue():
                self.m_origTargetText = fetchStringFromTexts(self.m_origAnchorStart,
                self.m_origAnchorEnd)
                self.m_targetText.setValue(self.m_origTargetText)

            else:
                self.m_origTargetText = self.m_range.getText()
                self.m_targetText.setValue(self.m_origTargetText)

    def checkSuggestValid(self):
        self.m_okBut.setEnabled(True)

    def execute(self):
        self.checkSuggestValid()

    def deferredCheckValid(self):
        DeferredCommand.addCommand(self)



