import pyjd
from pyjamas.ui.RootPanel import RootPanel
from pyjamas import DOM
from pyjamas.ui.Anchor import Anchor
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas import Window
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HTMLPanel import HTMLPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.Image import Image
from pyjamas.ui.HorizontalPanel import HorizontalPanel

def onClick(sender):
    Window.alert('I was Clicked')
    
if __name__ == '__main__':
    pyjd.setup("public/Anchor.html")
    
    # EXAMPLE 1
    a1 = Anchor(Widget = HTML('Test 1: Anchor to external site using HTML widget.'), Href='http://pyjs.org', Title = 'Test1')
    RootPanel().add(a1) 
    # EXAMPLE 2
    label = Label(text = 'Test 2: Click listener added to a label.')
    label.addClickListener(onClick)
    RootPanel().add(label) 
    # EXAMPLE 3
    a2 = Hyperlink(text = 'Hyperlink', Element = DOM.createSpan())
    a2.addClickListener(onClick)
    html2=HTMLPanel("Test 3: <span id ='t3'></span> added to HTMLPanel with click listener.")
    html2.add(a2, "t3")
    RootPanel().add(html2)
    # EXAMPLE 4
    hpanel = HorizontalPanel()
    hpanel.append(HTML('Test 4:  Anchor to external site using Image widget'))
    a3 = Anchor(Widget = Image('http://pyjs.org/assets/images/pyjs.128x128.png'), Href='http://pyjs.org', Title = 'Test4')
    hpanel.append(a3)
    
    RootPanel().add(hpanel) 
    pyjd.run()