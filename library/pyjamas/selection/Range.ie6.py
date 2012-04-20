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
* IE implementation of range, which emulates the methods of the W3C standard.
* IE's range object doesn't have any methods for directly getting/setting
* the end points to structural elements of the DOM, so we have to incrementally
* search/modify ranges to intiut self.
*
* @author John Kozura
"""
BOUNDARY_STRINGS = [ "StartToStart", "StartToEnd", "EndToEnd", "EndToStart"]

# Used for deleting/replacing values of a range
REPLACING_STRING = "DeL3EteTh1s"

def cloneRange(rng):
    JS("""
    return rng.duplicate();
    """)


def compareBoundaryPoint(rng, compare, how):
    if isinstance(how, int):
        how = BOUNDARY_STRINGS[how]
    JS("""
    return rng.compareEndPoints(how, compare);
    """)


"""*
* For IE, do this by copying the HTML string
*
* @see com.bfr.client.selection.impl.RangeImpl#copyContents(com.bfr.client.selection.impl.RangeImpl.JSRange, com.google.gwt.dom.client.Element)
"""
def copyContents(rng, copyInto):
    copyInto.setInnerHTML(getHtmlText(rng))


def createFromDocument(doc):
    JS("""
    return doc.body.createTextRange();
    """)


def createRange(doc, startPoint, startOffset, endPoint, endOffset):
    """
    * IE code to make this work - create a range on the start and the end
    * point, then move the end point to include the second
    """
    JSRange res = createRangeOnText(startPoint, startOffset)
    if startPoint == endPoint:
        # Shortcut if the start and end texts are the same
        moveEndCharacter(res, endOffset - startOffset)
     else:
        endRange = createRangeOnText(endPoint, endOffset)
        moveRangePoint(res, endRange, BOUNDARY_STRINGS[Range.END_TO_END])


    return res


"""*
* IE has no function for doing this with a range vs with a selection, so
* instead use pasteHTML, then remove the resulting element.
*
* @see com.bfr.client.selection.impl.RangeImpl#deleteContents(com.bfr.client.selection.impl.RangeImpl.JSRange)
"""
def deleteContents(rng):
    Text txt = placeholdRange(rng)
    if txt is not None:
        txt.removeFromParent()



def extractContents(rng, copyInto):
    copyContents(rng, copyInto)
    deleteContents(rng)


def fillRangePoints(rng):
    JSRange selRange = rng._getJSRange()
    if selRange is None:
        return

    RangeEndPoint start = getRangeEndPoint(rng, selRange, True)
    RangeEndPoint end = getRangeEndPoint(rng, selRange, False)

    canonicalize(start, end)

    rng._setRange(start, end)


"""*
* Place to put any checks and corrections to result in a consistent
* cursor.  Either of the range points passed may be modified by this
* function.
*
* @param start Start range point to check
* @param end End range point to check
"""
def canonicalize(start, end):
    if start is not None:
        # This checks if the cursor is at the end of one text range, and
        # the beginning of the next, as IE will do this for adjacent nodes..
        if (start.getTextNode() is not None)  and  (start.getTextNode().getNextSibling() == end.getTextNode())  and  (start.getTextNode().getLength() == start.getOffset())  and  (end.getOffset() == 0):
            end.setTextNode(start.getTextNode(), False)




def getCommonAncestor(rng):
    JS("""
    return rng.parentElement();
    """)

def getHtmlText(rng):
    JS("""
    return rng.htmlText;
    """)


def getText(rng):
    JS("""
    return rng.text;
    """)


"""*
* For IE, do this by copying the contents, then creating a dummy element
* and replacing it with this element.
*
* @see com.bfr.client.selection.impl.RangeImpl#surroundContents(com.bfr.client.selection.impl.RangeImpl.JSRange, com.google.gwt.dom.client.Element)
"""
def surroundContents(rng, copyInto):
    copyContents(rng, copyInto)
    Text txt = placeholdRange(rng)
    if txt is not None:
        txt.getParentElement().replaceChild(copyInto, txt)



def collapseRange(rng, start):
    JS("""
    rng.collapse(start);
    """)


"""*
* Create a 0-width js range on the first text element of this parent.
*
* @param parent
* @return
"""
def createRangeOnFirst(parent):
    JS("""
    var res = parent.ownerDocument.body.createTextRange();
    res.moveToElementText(parent);
    res.collapse(true);
    return res;
    """)


"""*
* Create a range with a range that has its start and end point within
* the given text and at the given offset.  This emulates capabilities of
* the W3C standard..
*
* @param setText
* @param offset
* @return
"""
def createRangeOnText(setText, offset):
    Element parent = setText.getParentElement()
    JSRange res = createRangeOnFirst(parent)
    Element testElement = getTestElement(parent.getOwnerDocument())

    # Can't directly select the text, but we can select a fake element
    # before it, then move the selection...
    try:
        parent.insertBefore(testElement, setText)
        moveToElementText(res, testElement)
        moveCharacter(res, offset)
    except:
        pass

    # Ensure the test element gets removed from the document
    testElement.removeFromParent()


    return res


"""*
* Get the IE start or end point of the given range, have to search for it
* to find it properly.
*
* @param range used to get the document
* @param selRange the selection we are getting the point of
* @param start whether to get the start or end point
* @return RangeEndPoint representing this, or None on error
"""
def getRangeEndPoint(rng, selRange, start):
    res = None

    # Create a cursor at either the beginning or end of the range, to
    # get that point's immediate parent
    checkRange = cloneRange(selRange)
    collapseRange(checkRange, start)
    parent = getCommonAncestor(checkRange)

    String compareFcn =
    BOUNDARY_STRINGS[start ? Range.START_TO_START : Range.END_TO_END]

    # Test element we move around the document to check relative selection
    testElement = getTestElement(rng.getDocument())

    try:
        # Move the test element backwards past nodes until we are in front
        # of the desired range endpoint
        compNode = parent.getLastChild()
        while compNode is not None:
            parent.insertBefore(testElement, compNode)
            moveToElementText(checkRange, testElement)
            if compareBoundaryPoint(checkRange, selRange, compareFcn) <= 0:
                break
            compNode = testElement.getPreviousSibling()


        if compNode is None:
            # Sometimes selection at beginning of a span causes a fail
            compNode = testElement.getNextSibling()


        if compNode is None:
            pass

        elif compNode.getNodeType() == Node.ELEMENT_NODE:
            # We only represent text elements right now, so if this is not
            # then go find one.  Check if the desired selection is at the
            # beginning or end of this element, first select the entire
            # element to determine whether the endpoint is at the
            # beginning or the end of it, ie whether to look forward or
            # backward.
            testElement.removeFromParent()
            moveToElementText(checkRange, compNode)
            comp = compareBoundaryPoint(checkRange, selRange, compareFcn)
            dirn = (comp == 0) ? !start : (comp < 0)
            closest = Range.getAdjacentTextElement(compNode, parent,
                                dirn, True)
            if closest is None:
                dirn = not dirn
                closest = Range.getAdjacentTextElement(compNode, parent,
                                dirn, True)


            if closest is not None:
                # Found a text node in one direction or the other
                res = RangeEndPoint(closest,
                        dirn and 0 or closest.getLength())

         else:
            # Get the proper offset, move the end of the check range to the
            # boundary of the actual range and get its length
            moveRangePoint(checkRange, selRange,
            BOUNDARY_STRINGS[start ? Range.END_TO_START
            : Range.END_TO_END])
            res = RangeEndPoint((Text)compNode,
            getText(checkRange).length())


    except:
        logging.log("Failed to find IE selection")

    # Make sure this gets removed from the document no matter what
    testElement.removeFromParent()

    return res or RangeEndPoint()


def getTestElement(document):
    global m_lastDocument
    global m_testElement
    # Create an element to search for the cursor with, cache it so we
    # don't create a ton of these unnecessarily
    if document != m_lastDocument:
        m_lastDocument = document
        m_testElement = m_lastDocument.createDivElement()

    return m_testElement


"""*
* Move both the start and end point of this range
"""
def moveCharacter(rng, chars):
    JS("""
    return rng.move("character", chars);
    """)


"""*
* Move just the end point of this range
"""
def moveEndCharacter(rng, chars):
    JS("""
    return rng.moveEnd("character", chars);
    """)


def moveRangePoint(rng, moveTo, how):
    JS("""
    rng.setEndPoint(how, moveTo);
    """)


def moveToElementText(rng, element):
    JS("""
    rng.moveToElementText(element);
    """)


def placeholdPaste(rng, str):
    JS("""
    rng.pasteHTML(str);
    """)


"""*
* Since there's no good delete for an arbitrary range, simply replace it
* with this text that nobody would use, then go find it so we can
* delete or replace it in other functions.  This depends on IE creating a
* single text element that includes exactly this string (and no user also
* has this exact text on their page..)
*
* An alternative but far more complicated method would be to try to do
* this via setting the selection, doing the delete/replace, and then
* restoring the selection.
*
* @param range The range to replace with a text node
* @return the text node that replaced the contents of range
"""
def placeholdRange(rng):
    # Paranoid, include a random number to reduce chance this string
    # would occur in the text..
    replaceString = REPLACING_STRING +
    (int)(Integer.MAX_VALUE * Math.random())

    parent = getCommonAncestor(rng)
    placeholdPaste(rng, replaceString)

    res = Range.getAdjacentTextElement(parent, True)
    while res is not None:
        if replaceString == res.getData():
            break
        res = Range.getAdjacentTextElement(res, True)

    return res



