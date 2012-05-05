import sys
from gi.repository import WebKit

view = WebKit.WebView()
frame = view.get_main_frame()
view.execute_script(open(sys.argv[1]+'.js').read())
view.execute_script(open('tests/test-'+sys.argv[1]+'.js').read())
