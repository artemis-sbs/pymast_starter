import sbslibs
from  sbs_utils.handlerhooks import *
from sbs_utils.gui import Gui
from sbs_utils.mast.maststorypage import StoryPage
from sbs_utils.mast.maststory import MastStory

from sbs_utils.mast.mast import Mast
from sbs_utils.mast.pollresults import PollResults
from sbs_utils.mast.label import label
from story import start_server, start_client

from sbs_utils.procedural.gui import gui_reroute_server, gui_row, gui_button, gui, gui_section, gui_text
from sbs_utils.procedural.execution import AWAIT


class Story(MastStory):
    def ____init__(self):
        super.__init__()
        self.main = self.main_gui

    def test(self):
        print("Press")

    @label()
    def main_gui(self):
        #yield PollResults.OK_RUN_AGAIN
        # gui_reroute_server(server_start)
        gui_section("area: 20,20,50,50")
        gui_button("Hello", on_message=self.test)
        gui_row()
        gui_text("Hello")
        
        # g = gui()
        # while not g.done():
        #     yield PollResults.OK_RUN_AGAIN
        yield AWAIT(gui())
        


class SimpleAiPage(StoryPage):
    story = Story()
    # main_server = story.main_gui
    main_server = start_server
    main_client = start_client



Mast.include_code = True

Gui.server_start_page_class(SimpleAiPage)
Gui.client_start_page_class(SimpleAiPage)
