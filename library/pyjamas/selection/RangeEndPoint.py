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
* An end point of a range, represented as a text node and offset in to it.
* Does not support potential other types of selection end points.
*
* @author John Kozura
"""
class RangeEndPoint:
    MOVE_CHARACTER 	= 1
    MOVE_WORDSTART	= 2
    MOVE_WORDEND	= 3

    # All unicode whitespace characters
    DEFAULT_WS_REXP = \
    "[\t-\r \u0085\u00A0\u1680\u180E\u2000-\u200B\u2028\u2029\u202F\u205F\u3000\uFEFF]+"

    """*
    * Set the regular expression used for detecting consecutive whitespace in a
    * string.  It must be of the form "[ \t\n]+", with all desired whitespace
    * characters between the braces.  This is used for word detection for
    * the move method.
    *
    * @param regExp String of the regular expression
    """
    def setWhitespaceRexp(self, regExp):
        c_wsRexp = RegExp.compile(regExp, "gm")


    """*
    * Create a range end point with nothing set
    """
    def __init__(self):
        super()


    """*
    * Create a range end point at the start or end of an element.  The actual
    * selection will occur at the first/last text node within this element.
    *
    * @param element element to create this end point in
    * @param start whether to make the end point at the start or the end
    """
    def __init__(self, element, start):
        this()
        setElement(element, start)


    """*
    * Create a non-textual range end point that just points to this element
    *
    * @param element Non-textual element to point to
    """
    def __init__(self, element):
        this()
        setElement(element)


    """*
    * Create a range end point at the start or end of a text node
    *
    * @param text text node this end point starts/end in
    * @param start whether to make the end point at the start or the end
    """
    def __init__(self, text, start):
        this()
        setTextNode(text, start)


    """*
    * Create a range end point with a text node and offset into it
    *
    * @param text text node this end point occurs in
    * @param offset offset characters into the text node
    """
    def __init__(self, text, offset):
        this()

        setTextNode(text)
        setOffset(offset)


    """*
    * Clone a range end point
    *
    * @param endPoint point to clone
    """
    def __init__(self, endPoint):
        this(endPoint.getTextNode(), endPoint.getOffset())


    def compareTo(self, comp):
        thisRng = Range(this)
        cmpRng = Range(comp)
        return thisRng.compareBoundaryPoint(cmpRng, Range.START_TO_START)


    def equals(self, obj):
        res = False

        try:
            comp = obj

            res = (comp == this)  or  \
            ((comp.getNode() == getNode())  and  \
            (comp.getOffset() == getOffset()))
        except ex:
            pass

        return res


    """*
    * Get the offset into the text node
    *
    * @return offset in characters
    """
    def getOffset(self):
        return self.m_offset


    """*
    * Get the string of the text node of this end point, either up to or
    * starting from the offset:
    *
    * "som|e text"
    *   True  : "e text"
    *   False : "som"
    *
    * @param asStart whether to get the text as if this is a start point
    * @return the text before or after the offset, or None if this is not set
    """
    def getString(self, asStart):
        if not isTextNode():
            return None

        res = self.m_node.getData()
        return asStart and res.substring(self.m_offset) or \
               res.substring(0, self.m_offset)


    """*
    * Get this as a node (be it text or element)
    """
    def getNode(self):
        return self.m_node


    """*
    * Get the text node of this end point, note this can be None if there are
    * no text anchors available or if this is just an element.
    *
    * @return the text node
    """
    def getTextNode(self):
        return isTextNode() and self.m_node or None


    """*
    * Get the Element of this end point, if this is not a textual end point.
    *
    * @return the text node
    """
    def getElement(self):
        return isTextNode() and None or self.m_node


    def isSpace(self, check):
        return check.isspace()


    def isTextNode(self):
        return (self.m_node is None) and False or \
               (self.m_node.getNodeType() == Node.TEXT_NODE)


    """*
    * If the offset occurs at the beginning/end of the text node, potentially
    * move to the end/beginning of the next/previous text node, to remove
    * text nodes where 0 characters are actually used.  If asStart is True then
    * move a cursor at the end of a text node to the beginning of the next
    * vice versa for False.
    *
    * @param asStart Whether to do this as a start or end range point
    """
    def minimizeBoundaryTextNodes(self, asStart):
        text = getTextNode()
        if (text is not None)  and  (self.m_offset == (asStart and text.getLength() or 0)):
            nxt = Range.getAdjacentTextElement(text, asStart)
            if nxt is not None:
                setTextNode(nxt)
                self.m_offset = asStart and 0 or nxt.getLength()




    """*
    * TODO IMPLEMENTED ONLY FOR CHARACTER
    * Move the end point forwards or backwards by one unit of type, such as
    * by a word.
    *
    * @param forward True if moving forward
    * @param topMostNode top node to not move past, or None
    * @param limit an endpoint not to move past, or None
    * @param type what unit to move by, ie MOVE_CHARACTER or MOVE_WORD
    * @param count how many of these to move by
    * @return how far this actually moved
    """
    def move(self, forward, topMostNode, limit, type, count):
        res = 0

        limitText = (limit is None) and None or limit.getTextNode()
        curr = getTextNode()
        if curr is not None:
            last = curr
            offset = getOffset()

            if type == MOVE_CHARACTER:
                while curr is not None:
                    last = curr
                    len = forward and (curr.getLength() - offset) or offset
                    if curr == limitText:
                        # If there is a limiting endpoint, may not be able to
                        # go as far
                        len = forward and (limit.getOffset() - offset) or \
                                          (offset - limit.getOffset())


                    if (len + res) < count:
                        res += len

                        if curr == limitText:
                            break


                    else:
                        # Finis
                        len = count - res
                        offset = forward and (offset + len) or (offset - len)
                        res = count
                        break


                    while True:
                        # Next node, skipping any 0-length texts
                        curr = Range.getAdjacentTextElement(curr, topMostNode,
                                                            forward, False)
                        if (curr is None)  or  (curr.getLength() != 0):
                            break

                    if curr is not None:
                        offset = forward and 0 or curr.getLength()


                """
                case MOVE_WORDSTART:
                case MOVE_WORDEND:
                if c_wsRexp is None:
                    setWhitespaceRexp(DEFAULT_WS_REXP)


                while curr is not None:

                    do {
                        # Next node, skipping any 0-length texts
                        curr = Range.getAdjacentTextElement(curr, topMostNode,
                        forward, False)
                     while  ((curr is not None)  and  (curr.getLength() == 0))

                    if curr is not None:
                        offset = forward ? 0 : curr.getLength()


                break
                """
            else:
                assert(False)

            setTextNode(last)
            setOffset(offset)

        return res


    """*
    * Sets this start point to be a non-textual element (like an image)
    """
    def setElement(self, element):
        self.m_node = element


    """*
    * Set the range end point at the start or end of an element.  The actual
    * selection will occur at the first/last text node within this element.
    *
    * @param element element to set this end point in
    * @param start whether to make the end point at the start or the end
    """
    def setElement(self, element, start):
        text = Range.getAdjacentTextElement(element, element, start, False)
        setTextNode(text, start)


    """*
    * Given an absolute x/y coordinate and an element where that coordinate
    * falls (generally obtained from an event), creates a RangeEndPoint
    * containing or closest to the coordinate.  If the point falls within a
    * non-textual element, a non-text endpoint is returned.  If the point falls
    * within a text-containing element but not within any of the actual child
    * text, tries to find the closest text point.
    *
    * @param element An element this point falls within
    * @param absX Absolute X coordinate, ie from  Event.getClientX
    * @param absY Absolute Y coordinate, ie from  Event.getClientY
    * @return A rangeendpoint where the click occured, or None if not found
    """
    def findLocation(self, element, absX, absY):
        # Convert to document-relative coordinates
        doc = element.getOwnerDocument()
        relX = absX - doc.getBodyOffsetLeft()
        offY = getTotalOffsetY(doc)
        relY = absY + offY

        if spn is None:
            spn = doc.createSpanElement()
            spn.setInnerText("X")

        body = doc.getBody()
        body.appendChild(spn)
        spn.getStyle().setPosition(Position.ABSOLUTE)
        spn.getStyle().setTop(relY, Unit.PX)
        spn.getStyle().setLeft(relX, Unit.PX)

        locRes = findLocation(doc, element, relX, relY)

        return locRes and locRes.ep


    def getTotalOffsetY(self, doc):
        JS("""
        var res = 0;
        var wind = doc.defaultView || doc.parentWindow;
        if (wind) {
            res = wind.pageYOffset;
        }
        return res;
        """)


    """
    if wind.mozInnerScreenX:
        res = res + wind.mozInnerScreenX

    elif wind.screenTop:
        res = res + wind.screenTop

    else:
        # webkit?

    """

    class FindLocRes:

        def __init__(self, ept, dist=0):
            self.ep = ept
            self.distance = dist


        def replace(self, curr, comp):
            res = curr
            if (comp is not None)  and  ((curr is None)  or  (curr.ep is None)  or  (comp.distance < curr.distance)):
                res = comp

            return res


        def isExact():
            return (self.ep is not None)  and  (self.distance == 0)


    def findLocation(self, doc, ele, relX, relY):
        res = None

        if contains(ele, relX, relY)  and  isVisible(doc, ele):
            if ele.hasChildNodes():
                # Iterate through children until we hit an exact match
                for i in range(ele.getChildCount()):
                    child = ele.getChild(i)
                    if child.getNodeType() == Node.ELEMENT_NODE:
                        tmp = findLocation(doc, child, relX, relY)

                    else:
                        tmp = findLocation(doc, child, relX, relY)

                    res = FindLocRes.replace(res, tmp)

                    if res and res.isExact():
                        break

            else:
                # If this contains but has no children, then this is it
                res = FindLocRes(RangeEndPoint(ele))



        return res


    def findLocation(self, doc, text, relX, relY):

        st = text.getData()
        if not st:
            # Theoretically it could be in here still..
            return None
        else:
            # Insert 2 spans and do a binary search to find the single
            # character that fits
            span1 = doc.createSpanElement()
            span2 = doc.createSpanElement()
            span3 = doc.createSpanElement()
            span4 = doc.createSpanElement()

            parent = text.getParentElement()
            parent.insertBefore(span1, text)
            parent.insertBefore(span2, text)
            parent.insertBefore(span3, text)
            parent.insertBefore(span4, text)
            parent.removeChild(text)

            try:
                len = st.length() / 2
                span2.setInnerText(st.substring(0, len))
                span3.setInnerText(st.substring(len))

                res = findLocation(text, span1, span2, span3, span4,
                                    relX, relY)
            except:
                res = None

            parent.insertAfter(text, span4)
            parent.removeChild(span1)
            parent.removeChild(span2)
            parent.removeChild(span3)
            parent.removeChild(span4)




        return res


    def findLocation(self, origText, span1, span2, span3, span4, relX, relY):
        res = None

        while res is None:
            if contains(span2, relX, relY):
                st = span2.getInnerText()
                if st.length() <= 1:
                    res = FindLocRes(
                    RangeEndPoint(origText,
                    span1.getInnerText().length() +
                    closerOffset(span2, relX)))

                else:
                    span4.setInnerHTML(span3.getInnerHTML() +
                    span4.getInnerHTML())
                    len = st.length() / 2
                    span2.setInnerHTML(st.substring(0, len))
                    span3.setInnerHTML(st.substring(len))


            elif contains(span3, relX, relY):
                st = span3.getInnerText()
                if st.length() <= 1:
                    res = FindLocRes(
                    RangeEndPoint(origText,
                    span1.getInnerText().length() +
                    span2.getInnerHTML().length() +
                    closerOffset(span3, relX)))

                else:
                    span1.setInnerHTML(span1.getInnerHTML() +
                    span2.getInnerHTML())
                    len = st.length() / 2
                    span2.setInnerHTML(st.substring(0, len))
                    span3.setInnerHTML(st.substring(len))


            else:
                # This might be close to one end or the other of this
                dist1 = getLocDistance(span1.hasChildNodes() and span2 \
                                        or span1, relX, relY)
                dist2 = getLocDistance(span4.hasChildNodes() and span4 \
                                        or span3,
                                        relX, relY)
                res = FindLocRes(RangeEndPoint(origText, dist1 < dist2),
                                    min(dist1, dist2))



        return res


    # 0 if closer to the left edge, 1 if closer to the right.
    def closerOffset(self, ele, relX):
        return ((relX - ele.getAbsoluteLeft()) >
                    (ele.getAbsoluteRight() - relX)) and 1 or 0


    def contains(self, ele, relX, relY):
        """
        int l = ele.getAbsoluteLeft()
        int r = ele.getAbsoluteRight()
        int t = ele.getAbsoluteTop()
        int b = ele.getAbsoluteBottom()
        """
        return ((ele.getAbsoluteLeft() <= relX)  and
                (ele.getAbsoluteRight() >= relX)  and
                (ele.getAbsoluteTop() <= relY)  and
                (ele.getAbsoluteBottom() >= relY))


    def getLocDistance(self, ele, relX, relY):

        top = ele.getAbsoluteTop()
        bot = ele.getAbsoluteBottom()

        res = 0
        if relY < bot:
            res = bot - relY

        elif relY > top:
            res = relY - top


        left = ele.getAbsoluteLeft()
        right = ele.getAbsoluteRight()
        if relX < left:
            res += left - relX

        elif relX > right:
            res += right - relX


        return res


    def isVisible(self, doc, ele):
        JS("""
        if (!ele.parentNode) return false;
        if (ele.style)  {
            if (ele.style.display == 'none') return false;
            if (ele.style.visibility == 'hidden') return false;
        }

        // Try the computed style in a standard way
        var wind = doc.defaultView || doc.parentWindow;
        if (wind && wind.getComputedStyle) {
            var style = wind.getComputedStyle(ele, null);
            if (style.display == 'none') return false;
            if (style.visibility == 'hidden') return false;
        }

        // Don't care about parents, already traversed down them
        //return isVisible(obj.parentNode);
        return true;
        """)


    """
    # Or get the computed style using IE's silly proprietary way
    # I think IE supports getComputedStyle now
    var style = obj.currentStyle
    if style:
        if style['display'] == 'none':
            return False

        if style['visibility'] == 'hidden':
            return False


    """

    """*
    * Set the offset into the text node
    *
    * @param offset offset in characters
    """
    def setOffset(self, offset):
        self.m_offset = offset


    """*
    * Set the text node this end point occurs in
    *
    * @param text text node this end point occurs in
    """
    def setTextNode(self, textNode):
        self.m_node = textNode


    """*
    * Set this range end point at the start or end of a text node
    *
    * @param text text node this end point starts/end in
    * @param start whether to make the end point at the start or the end
    """
    def setTextNode(self, textNode, start):
        setTextNode(textNode)
        if (start  or  (textNode is None)):
            offs = 0
        else:
            offs = textNode.getLength()
        setOffset(offs)


    """*
    * Get the text of this with a "|" at the offset
    *
    * @return a string representation of this endpoint
    """
    def __str__(self):
        return getString(False) + "|" + getString(True)



