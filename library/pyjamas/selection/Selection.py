"""
* Copyright 2010 John Kozura
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""



START_NODE	= "startContainer"
START_OFFSET	= "startOffset"
END_NODE		= "endContainer"
END_OFFSET	= "endOffset"
IS_COLLAPSED 	= "isCollapsed"


"""*
* A selection within a particular document.  Holds the singleton for a
* particlar document/window for getting and setting the selection.
*
* @author John Kozura
"""
class Selection:

    """*
    * Clears or removes any current text selection.
    """
    def clearAnySelectedText():
        self.getSelection().clear()

    """*
    * Convenience for getting the range for the current browser selection
    *
    * @return A range object representing the browser window's selection
    """
    def getBrowserRange(self):
        return self.getSelection().getRange()


    """*
    * Returns the selection for a given window, for instance an iframe
    *
    * @return The singleton instance
    """
    def getSelection(self, window):
        SelectionImpl.JSSel jsSel = c_impl.getSelection(window)
        Selection res = Selection()
        res.self.m_selection = jsSel
        res.self.m_document = getDocument(window)
        return res


    def getDocument(self, window):
        JS("""
        return window.document;
        """)


    """*
    * Returns the document Selection singleton
    *
    * @return The singleton instance
    """
    def getSelection(self):
        return Selection.getSelection(getWindow())


    def getImpl(self):
        return Selection.c_impl


    def getWindow(self):
        JS("""
        return $wnd;
        """)


    def __init__(self):
        self.m_document = None
        self.m_selection = None


    """*
    * Clears any current selection.
    """
    def clear(self):
        Selection.getImpl().clear(self.m_selection)


    """*
    * Gets the parent document associated with this selection.  Could be
    * different from the browser document if, for example this is the selection
    * within an iframe.
    *
    * @return parent document of this selection
    """
    def getDocument(self):
        return self.m_document

    """*
    * Get the javascript object representing the selection.  Since this is
    * browser dependent object, should probably not use self.
    *
    * @return a JavaScriptObject representing this selection
    """
    def getJSSelection(self):
        return self.m_selection

    """*
    * Gets the range associated with the given selection.  The endpoints are
    * captured immediately, so any changes to the selection will not affect
    * the returned range.  In some browsers (IE) this can return NULL if
    * nothing is selected in the document.
    *
    * @return A range object capturing the current selection
    """
    def getRange(self):
        res = None
        jsRange = c_impl.getJSRange(self.m_document, self.m_selection)
        if jsRange is not None:
            res = Range(self.m_document, jsRange)
            res.ensureEndPoints()

        return res


    """*
    * Tests if anything is currently being selected
    *
    * @return True if empty False otherwise
    """
    def isEmpty(self):
        return Selection.getImpl().isEmpty(self.m_selection)


    """*
    * Takes a range object and pushes it to be the selection.  The range
    * must be parented by the same window/document as the selection.  The range
    * remains separate from the selection after this operation; any changes to
    * the range are not reflected in the selection, and vice versa.
    *
    * @param newSelection What the selection should be
    """
    def setRange(self, newSelection):
        if newSelection.getDocument() == self.m_document:
            c_impl.setJSRange(self.m_selection, newSelection.getJSRange())

