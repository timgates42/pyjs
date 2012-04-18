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









"""*
* Implements a text range in a Document, everything between two RangeEndPoints.
* Works with both a (browser dependent) javascript range object, and with
* the java RangeEndPoint objects, building one or the other as needed on
* demand.
*
* @author John Kozura
"""
class Range:
    # For use in compareBoundaryPoint, which end points to compare
    START_TO_START	= 0
    START_TO_END	= 1
    END_TO_END	= 2
    END_TO_START	= 3
    
    """*
    * Returns the next adjacent text node in the given direction.  Will move
    * down the hierarchy, then through siblings, then up, looking for the first
    * text node.
    *
    * This could be non-statically included in the Node class
    *
    * @param current An element to start the search from, can be any type
    *                of node.
    * @param forward whether to search forward or backward
    * @return the next (previous) text node, or None if no more
    """
    def getAdjacentTextElement(self, current, forward):
        res = getAdjacentTextElement(current, None, forward, False)
        return res
    
    
    """*
    * Returns the next adjacent text node in the given direction.  Will move
    * down the hierarchy (if traversingUp is not set), then through siblings,
    * then up (but not past topMostNode), looking for the first node
    *
    * This could be non-statically included in the Node class
    *
    * @param current An element to start the search from, can be any type
    *                of node.
    * @param topMostNode A node that this will traverse no higher than
    * @param forward whether to search forward or backward
    * @param traversingUp if True, will not look at the children of this element
    * @return the next (previous) text node, or None if no more
    """
    def getAdjacentTextElement(self, current, topMostNode, forward, traversingUp):
        res = None
        
        # If traversingUp, then the children have already been processed
        if not traversingUp:
            if current.getChildCount() > 0:
                node = forward is not None and current.getFirstChild() or \
                current.getLastChild()
                
                if node.getNodeType() == Node.TEXT_NODE:
                    res = node
                else:
                    # Depth first traversal, the recursive call deals with
                    # siblings
                    res = self.getAdjacentTextElement(node, topMostNode,
                                            forward, False)
                
            
        
        
        if res is None:
            node = forward is not None and current.getNextSibling() or \
                            current.getPreviousSibling()
            # Traverse siblings
            if node is not None:
                if node.getNodeType() == Node.TEXT_NODE:
                    res = node
                else:
                    # Depth first traversal, the recursive call deals with
                    # siblings
                    res = self.getAdjacentTextElement(node, topMostNode,
                                            forward, False)
                
            
        
        
        # Go up and over if still not found
        if (res is None)  and  (current != topMostNode):
            node = current.getParentNode()
            # Stop at document (technically could stop at "html" tag)
            if (node is not None)  and  (node.getNodeType() != Node.DOCUMENT_NODE):
                res = self.getAdjacentTextElement(node, topMostNode,
                                            forward, True)
            
        
        
        return res
    
    
    """*
    * Returns all text nodes between (and including) two arbitrary text nodes.
    * Caller must ensure startNode comes before endNode.
    *
    * @param startNode start node to traverse
    * @param endNode end node to finish traversal
    * @return A list of all text nodes between these two text nodes
    """
    def getSelectedTextElements(self, startNode, endNode):
        res = []
        
        current = startNode
        while (current is not None)  and  (current != endNode):
            res.append(current)
            
            current = self.getAdjacentTextElement(current, None, True, False)
        
        if current is None:
            # With the old way this could have been backwards, but should not
            # happen now, so this is an error
            res = None
        else:
            res.append(current)
        
        return res
    
    
    """*
    * Creates an empty range on this document
    *
    * @param doc Document to create an empty range in
    """
    def __init__(self, doc):
        self.setDocument(doc)
    
    
    """*
    * Creates a range that encompasses the given element
    *
    * @param element Element to create a range around
    """
    def __init__(self, element):
        self.setRange(element)
    
    
    """*
    * Creates a range that is a cursor at the given location
    *
    * @param cursorPoint a single point to make a cursor range
    """
    def __init__(self, cursorPoint):
        self.setCursor(cursorPoint)
    
    
    """*
    * Create a range that extends between the given points.  Caller must
    * ensure that end comes after start
    *
    * @param startPoint start point of the range
    * @param endPoint end point of the range
    """
    def __init__(self, startPoint, endPoint):
        self.setRange(startPoint, endPoint)
    
    
    """*
    * Internal method for creating a range from a JS object
    *
    * @param document
    * @param rangeObj
    """
    def __init__(self, document, rangeObj):
        self.m_document = document
        self.m_range = rangeObj
    
    
    """*
    * Internal function for retrieving the range, external callers should NOT
    * USE THIS
    *
    * @return
    """
    def _getJSRange(self):
        return self.m_range
    
    
    """*
    * Internal call to set the range, which skips some checks and settings
    * this SHOULD NOT be used externally.
    *
    * @param startPoint
    * @param endPoint
    """
    def _setRange(self, startPoint, endPoint):
        self.m_document = startPoint and startPoint.getNode().getOwnerDocument()
        self.m_startPoint = startPoint
        self.m_endPoint = endPoint
    
    
    """*
    * Collapses the range into a cursor, either to the start or end point
    *
    * @param start if True, cursor is the start point, otherwise the end point
    """
    def collapse(self, start):
        if self.m_range is not None:
            c_impl.collapse(self.m_range, start)
            self.m_startPoint = None
        
        elif start:
            self.m_endPoint = self.m_startPoint
        else:
            self.m_startPoint = self.m_endPoint
        
    
    
    """*
    * Compares an endpoint of this range with an endpoint in another range,
    * returning -1, 0, or 1 depending whether the comparison endpoint comes
    * before, at, or after this endpoint.  how is a constant determining which
    * endpoints to compare, for example Range.START_TO_START.
    *
    * @param compare Range to compare against this one.
    * @param how constant indicating which endpoints to compare
    * @return -1, 0, or 1 indicating relative order of the endpoints
    """
    def compareBoundaryPoint(self, compare, how):
        self.ensureRange()
        self.compare.ensureRange()
        
        return c_impl.compareBoundaryPoint(self.m_range, self.getJSRange(), how)
    
    
    """*
    * Make a copy of the contents of this range, into the given element.  All
    * tags required to make the range complete will be included
    *
    * @param copyInto an element to copy the contents into, ie
    *                 DOM.createSpanElement()
    """
    def copyContents(self, copyInto):
        self.ensureRange()
        c_impl.copyContents(self.m_range, copyInto)
    
    
    """*
    * Remove the contents of this range from the DOM.
    """
    def deleteContents(self):
        self.ensureRange()
        c_impl.deleteContents(self.m_range)
    
    
    def equals(self, obj):
        res = False
        
        try:
            cm = obj
            
            ensureEndPoints()
            cm.ensureEndPoints()
            res = (cm == this)  or  \
                        (self.m_startPoint.equals(cm.getStartPoint())  and  \
                        self.m_endPoint.equals(cm.getEndPoint()))
        except:
            pass
        
        return res
    
    
    """*
    * Place the contents of this range into a SPAN element, removing them
    * from the DOM.  All tags required to make the range complete will be
    * included.  This does not preserve the element object ids of the contents.
    *
    * @return a SPAN element unattached to the DOM, containing the range
    *         contents.
    """
    def extractContents(self):
        res = self.m_document.createSpanElement()
        self.extractContents(res)
        return res
    
    
    """*
    * Place the contents of this range into the given element, removing them
    * from the DOM.  All tags required to make the range complete will be
    * included.  This does not preserve the element object ids of the contents.
    *
    * @param copyInto an element to extract the contents into, ie
    *                 DOM.createSpanElement()
    """
    def extractContents(self, copyInto):
        self.ensureRange()
        c_impl.extractContents(self.m_range, copyInto)
    
    
    """*
    * Get the element that is the lowest common ancestor of both ends of the
    * range.  In other words, the smallest element that includes the range.
    *
    * @return the element that completely encompasses this range
    """
    def getCommonAncestor(self):
        self.ensureRange()
        return c_impl.getCommonAncestor(self.m_range)
    
    
    """*
    * Gets a single point of the cursor location if this is a cursor, otherwise
    * returns None.
    *
    * @return the single point if this is a cursor and not a selection
    """
    def getCursor(self):
        return self.isCursor() and self.m_startPoint or None
    
    
    """*
    * Get the DOM Document this range is within
    *
    * @return document this range is in
    """
    def getDocument(self):
        return self.m_document
    
    
    """*
    * Get the end point of the range.  Not a copy, so changing this alters
    * the range.
    *
    * @return the end point object
    """
    def getEndPoint(self):
        self.ensureEndPoints()
        return self.m_endPoint
    
    
    """*
    * Gets an HTML string represnting all elements enclosed by this range.
    *
    * @return An html string of this range
    """
    def getHtmlText(self):
        self.ensureRange()
        return c_impl.getHtmlText(self.m_range)
    
    
    """*
    * Get the JS object representing this range.  Since it is highly browser
    * dependent, it is not recommended to operate on this
    *
    * @return JavaScriptObject representing this range
    """
    def getJSRange(self):
        self.ensureRange()
        return self.m_range
    
    
    """*
    * Returns a list of all text elements that are part of this range, in order.
    *
    * @return all elements in this range
    """
    def getSelectedTextElements(self):
        return self.getSelectedTextElements(self.m_startPoint.getTextNode(),
                            self.m_endPoint.getTextNode())
    
    
    """*
    * Get the start point of the range.  Not a copy, so changing this alters
    * the range.
    *
    * @return the start point object
    """
    def getStartPoint(self):
        self.ensureEndPoints()
        return self.m_startPoint
    
    
    """*
    * Gets the plain text that is enclosed by this range
    *
    * @return A string of the text in this range
    """
    def getText(self):
        self.ensureRange()
        return c_impl.getText(self.m_range)
    
    
    """*
    * Returns whether this is a cursor, ie the start and end point are equal
    *
    * @return True if start == end
    """
    def isCursor(self):
        self.ensureEndPoints()
        return self.m_startPoint.equals(self.m_endPoint)
    
    
    """*
    * Minimize the number of text nodes included in this range.  If the start
    * point is at the end of a text node, move it to the beginning of the
    * next text node; vice versa for the end point.  The result should ensure
    * no text nodes with 0 included characters.
    """
    def minimizeTextNodes(self):
        self.ensureEndPoints()
        self.m_startPoint.minimizeBoundaryTextNodes(True)
        self.m_endPoint.minimizeBoundaryTextNodes(False)
    
    
    """*
    * TODO NOT IMPLEMENTED YET
    * Move the end points to encompass a boundary type, such as a word.
    *
    * @param topMostNode a Node not to traverse above, or None
    * @param type unit to move boundary by, such as RangeEndPoint.MOVE_WORD
    """
    def moveToBoundary(self, topMostNode, type):
        self.ensureEndPoints()
        self.m_startPoint.move(False, topMostNode, None, type, 1)
        self.m_endPoint.move(True, topMostNode, None, type, 1)
    
    
    """*
    * Sets the range to a point cursor.
    *
    * @param cursorPoint A single endpoint to create a cursor range at
    """
    def setCursor(self, cursorPoint):
        self.setRange(cursorPoint, cursorPoint)
    
    
    """*
    * Sets just the end point of the range.  New endPoint must reside within
    * the same document as the current startpoint, and must occur after it.
    *
    * @param startPoint New start point for this range
    """
    def setEndPoint(self, endPoint):
        assert ((self.m_startPoint is not None)  or 
        (endPoint.getNode().getOwnerDocument() == self.m_document))
        self.m_endPoint = endPoint
        self.m_range = None
    
    
    """*
    * Sets the range to encompass the given element.  May not work around
    * non-text containing elements.
    *
    * @param element Element to surround by this range
    * @return whether a range can be placed around this element.
    """
    def setRange(self, element):
        firstText = self.getAdjacentTextElement(element, element, True, False)
        lastText = self.getAdjacentTextElement(element, element, False, False)
        
        if (firstText is None)  or  (lastText is None):
            return False
        
        
        self.setRange(self.RangeEndPoint(firstText, 0),
        self.RangeEndPoint(lastText, lastText.getLength()))
        
        return True
    
    
    """*
    * Set the range to be between the two given points.  Both points must be
    * within the same document, and end must come after start.
    *
    * @param startPoint Start point to set the range to
    * @param endPoint End point to set the range to
    """
    def setRange(self, startPoint, endPoint):
        assert (startPoint.getNode().getOwnerDocument() ==
                    endPoint.getNode().getOwnerDocument())
        
        self._setRange(startPoint, endPoint)
        self.m_range = None
    
    
    """*
    * Sets just the start point of the range.  New startPoint must reside within
    * the same document as the current endpoint, and must occur before it.
    *
    * @param startPoint New start point for this range
    """
    def setStartPoint(self, startPoint):
        assert ((self.m_endPoint is not None)  and 
        (startPoint.getNode().getOwnerDocument() == self.m_document))
        
        self.m_startPoint = startPoint
        self.m_range = None
    
    
    """*
    * Surround all of the contents of the range with a SPAN element, which
    * replaces the content in the DOM.  All tags required to make the range
    * complete are included in the child content.  This does not preserve the
    * element object ids of the contents.  The range will surround the new
    * element after this operation.
    *
    * @return The span element that now surround the contents
    """
    def surroundContents(self):
        res = self.m_document.createSpanElement()
        self.surroundContents(res)
        return res
    
    
    """*
    * Surround all of the contents of the range with the given element, which
    * replaces the content in the DOM.  All tags required to make the range
    * complete are included in the child content.  This does not preserve the
    * element object ids of the contents.  The range will surround this
    * element after this operation.
    *
    * @param copyInto an element to place the contents into, which will replace
    *                 them in the DOM after this operation
    """
    def surroundContents(self, copyInto):
        self.ensureRange()
        c_impl.surroundContents(self.m_range, copyInto)
        self.setRange(copyInto)
    
    
    """*
    * Ensure the end points exists and are consisent with the javascript range
    """
    def ensureEndPoints(self):
        if (self.m_startPoint is None)  or  (self.m_endPoint is None):
            c_impl.fillRangePoints(this)
            self.setupLastEndpoints()
        
    
    
    """*
    * Ensure the javascript range exists and is consistent with the end points
    """
    def ensureRange(self):
        if self.rangeNeedsUpdate():
            self.m_range = c_impl.createRange(self.m_document,
                                                self.m_startPoint.getTextNode(),
                                                self.m_startPoint.getOffset(),
                                                self.m_endPoint.getTextNode(),
                                                self.m_endPoint.getOffset())
            self.setupLastEndpoints()
        
    
    
    def rangeNeedsUpdate(self):
        return (self.m_range is None)  or  \
        ((self.m_startPoint is not None)  and  \
        ((self.m_lastStartPoint is None)  or  \
        not self.m_lastStartPoint.equals(self.m_startPoint)  or  \
        (self.m_lastEndPoint is None)  or  \
        not self.m_lastEndPoint.equals(self.m_endPoint)))
    
    
    def setupLastEndpoints(self):
        self.m_lastStartPoint = self.RangeEndPoint(self.m_startPoint)
        self.m_lastEndPoint = self.RangeEndPoint(self.m_endPoint)
    
    
    """*
    * Set the document this range is contained within
    *
    * @param doc document to set
    """
    def setDocument(self, doc):
        if self.m_document != doc:
            self.m_document = doc
            self.m_range = c_impl.createFromDocument(doc)
        
    


