import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.pymast.pymaststorypage import PyMastStoryPage
from story import Story

class MyStoryPage(PyMastStoryPage):
    story = Story()

Gui.server_start_page_class(MyStoryPage)
Gui.client_start_page_class(MyStoryPage)
