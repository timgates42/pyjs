import pyjd

from pyjamas import DeferredCommand
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui import RootPanel

from RichTextEditor import RichTextEditor

from pyjamas.selection.RangeEndPoint import RangeEndPoint
from pyjamas.selection.Range import Range
from pyjamas.selection.RangeUtil import getAdjacentTextElement
from pyjamas.selection import Selection

"""*
* Entry point classes define <code>onModuleLoad()</code>.
"""
class SelectionTest:

    def onSelectionChange(self, selection):
        self.refresh(selection)

    """*
    * This is the entry point method.
    """
    def onModuleLoad(self):
        dlp = DockPanel(Width="100%", Height="100%")

        self.m_rte = RichTextEditor()

        buts = FlowPanel()
        self.m_getCurr = Button("Refresh v", self)
        self.m_setHtml = Button("Set html ^", self)
        self.m_setHtml.setTitle("Set html from the lower left text area")
        self.m_toSCursor = Button("< To Cursor", self)
        self.m_toSCursor.setTitle("Set the selection to be a cursor at the beginning of the current selection")
        self.m_toECursor = Button("To Cursor >", self)
        self.m_toECursor.setTitle("Set the selection to be a cursor at the end of the current selection")
        self.m_surround = Button("Surround", self)

        grid = Grid(2, 2)
        self.m_startNode = self.createTextBox(1)
        self.m_startOffset = self.createTextBox(3)
        self.m_endNode = self.createTextBox(4)
        self.m_endOffset = self.createTextBox(5)
        self.m_select = Button("`>Select", self)
        self.m_select.setTitle("Select the texts/offsets in the boxes above")
        self.m_cursor = Button("`>Cursor", self)
        self.m_cursor.setTitle("Set cursor to text/offset of top 2 boxes above")
        grid.setWidget(0, 0, self.m_startNode)
        grid.setWidget(0, 1, self.m_startOffset)
        grid.setWidget(1, 0, self.m_endNode)
        grid.setWidget(1, 1, self.m_endOffset)

        self.m_deleteSel = Button("Delete", self)
        self.m_reset = Button("Reset", self)

        buts.add(self.m_getCurr)
        buts.add(self.m_setHtml)
        buts.add(self.m_toSCursor)
        buts.add(self.m_toECursor)
        buts.add(self.m_surround)
        buts.add(grid)
        buts.add(self.m_select)
        buts.add(self.m_cursor)

        buts.add(self.m_deleteSel)
        buts.add(self.m_reset)

        dlp.add(buts, DockPanel.WEST)

        textPanels = DockPanel()

        self.m_html = TextArea()
        self.m_html.setSize("100%", "100%")
        self.m_sel = TextArea()
        self.m_sel.setSize("100%", "100%")

        textPanels.add(self.m_sel, DockPanel.EAST)
        textPanels.add(self.m_html, DockPanel.WEST)

        dlp.add(textPanels, DockPanel.SOUTH)

        dlp.add(self.m_rte, DockPanel.CENTER)

        rp = RootPanel.get()
        rp.add(dlp)

        DeferredCommand.add(getattr(self, "set_html_focus"))

        self.reset()

    def set_html_focus(self):
        self.m_html.setFocus(True)

    def createTextBox(self, startVal):
        res = TextBox()
        res.setWidth("35px")
        res.setText(str(startVal))
        return res

    def reset(self):
        self.m_rte.setHtml(
        "The <span style=\"font-weight: bold;\">quick</span> " +
        "<span style=\"font-style: italic;\">brown </span>" +
        "fox jumped<br>ov" +
        "<a href=\"http:#google.com\">er </a>" +
        "<span style=\"text-decoration: underline;\">" +
        "<a href=\"http:#google.com\">th</a>e la</span>zy dogs<br>" +
        "Some&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; spaces<br>")


    def refresh(self, rng=None):
        if rng is None:
            rng = self.m_rte.getRange()
        self.m_html.setText(self.m_rte.getHtml())
        if rng is not None:
            if rng.isCursor():
                rep = rng.getCursor()
                self.m_sel.setText(str(rep))

            else:
                self.m_sel.setText(rng.getHtmlText())

        else:
            self.m_sel.setText("")

    def delete(self):
        rng = self.m_rte.getRange()
        if (rng is not None)  and  not rng.isCursor():
            rng.deleteContents()
            refresh()

    def toHtml(self):
        self.m_rte.setHtml(self.m_html.getText())

    def toCursor(self, start):
        rng = self.m_rte.getRange()
        if (rng is not None)  and  not rng.isCursor():
            rng.collapse(start)
            self.m_rte.getSelection()
            Selection.setRange(rng)
            self.refresh()

    def surround(self):
        rng = self.m_rte.getRange()
        if (rng is not None)  and  not rng.isCursor():
            rng.surroundContents()
            self.m_rte.getSelection()
            Selection.setRange(rng)
            self.refresh()

    def findNodeByNumber(self, num):

        doc = self.m_rte.getDocument()
        print "findNodeByNumber:doc", doc
        res = getAdjacentTextElement(doc, True)
        print "findNodeByNumber:startat", res
        while (res is not None)  and  (num > 0):
            print "findNodeByNumber?", res, num
            num -= 1
            res = getAdjacentTextElement(res, True)

        print "findNodeByNumber=", res
        return res

    def selectNodes(self, fullSel):
        startNode = int(self.m_startNode.getText())
        startOffset = int(self.m_startOffset.getText())

        startText = self.findNodeByNumber(startNode)
        print "startNode", startNode, startOffset
        print "startText", startText
        if fullSel:
            endNode = int(self.m_endNode.getText())
            endOffset = int(self.m_endOffset.getText())
            endText = self.findNodeByNumber(endNode)
        else:
            endText = startText
            endOffset = startOffset

        rng = Range(RangeEndPoint(startText, startOffset),
                    RangeEndPoint(endText, endOffset))

        self.m_rte.getSelection()
        Selection.setRange(rng)

        self.refresh()

    def onClick(self, wid):

        if wid == self.m_getCurr:
            self.refresh()

        elif wid == self.m_deleteSel:
            self.delete()

        elif wid == self.m_reset:
            self.reset()

        elif wid == self.m_toECursor:
            self.toCursor(False)

        elif wid == self.m_toSCursor:
            self.toCursor(True)

        elif wid == self.m_surround:
            self.surround()

        elif wid == self.m_setHtml:
            self.toHtml()

        elif wid == self.m_select:
            self.selectNodes(True)

        elif wid == self.m_cursor:
            self.selectNodes(False)


    def setFocus(self, wid):
        self._wid = wid # hack
        DeferredCommand.add(getattr(self, "execute_set_focus"))

    def execute_set_focus(self):
        self._wid.setFocus(True)


if __name__ == '__main__':
    pyjd.setup("public/SelectionTest.html")
    app = SelectionTest()
    app.onModuleLoad()
    pyjd.run()

