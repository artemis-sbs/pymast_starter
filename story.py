import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.pymast.pymaststory import PyMastStory
from sbs_utils.pymast.pymasttask import label
from sbs_utils import query
from sbs_utils.objects import PlayerShip, Npc


class Story(PyMastStory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_text = "This is a start project for mast"

    @label()
    def start_server(self):
        #
        # Create the player ship so the clients see it
        # This is a simple script that has one playable ship
        #
        sbs.create_new_sim()
        #yield self.delay(1)

        self.artemis =  query.to_id(PlayerShip().spawn(self.sim, 0,0,0, "Artemis", "tsn", "tsn_battle_cruiser"))
        sbs.assign_client_to_ship(0,self.artemis)

        print(f"start_server {self.start_text}")
        self.gui_section("area:2,20,80,35;")
        self.gui_text(f""" {self.start_text}""")

        yield self.await_gui({
            "Start": self.start
        })
        
    @label()
    def end_game(self):
        # 
        # Check for end game
        #
        # no more players
        
        players = query.role("__PLAYER__")
        if len(players) == 0:
            self.start_text = "You lost"
            sbs.pause_sim()
            yield self.jump(self.start_server)
        #
        # No more enemies
        #
        raiders = query.role("raider")
        if len(raiders) == 0:
            self.start_text = "You Won"
            print(f"end_game {self.start_text}")
            sbs.pause_sim()
            yield self.jump(self.start_server)
            
        yield self.delay(5)
        yield self.jump(self.end_game)

    @label()
    def start(self):
        # Create the world here

        # Create a space station
        ds1 = Npc().spawn(self.sim, 1000,0,1000, "DS1", "tsn", "starbase_command", "behav_station")

        # Create an enemy
        k001 = Npc().spawn(self.sim, -1000,0,1000, "K001", "raider", "kralien_dreadnaught", "behav_npcship")

        sbs.resume_sim()
        yield self.jump(self.end_game)


    @label()
    def start_client(self):
        #
        # This handles the change client button to return to the select_console
        #
        # event change_console:
        #     ->select_console
        # end_event
        #
        # Default the console to helm
        #
        self.task.console_select = "helm"
        yield self.jump(self.select_console)

    @label()
    def select_console(self):
        self.gui_section("area:2,20,80,35;")

        self.gui_text("""Select your console""")

        self.gui_section("area: 85,50, 99,90;row-height:200px")
        console_radio = self.gui_radio("helm,weapons, comms,science,engineering", self.task.console_select, True)
        self.gui_row("row-height: 30px;")
        self.gui_blank()
        self.gui_row("row-height: 30px;")
        self.gui_button("accept", self.console_selected)

        def on_message(sim, event):
            if event.sub_tag.startswith(console_radio.tag):
                self.task.console_select = console_radio.value
                return True

        self.await_gui(on_message=on_message)
        
    @label()
    def console_selected(self):
        sbs.assign_client_to_ship(self.task.page.client_id,self.artemis)
        self.gui_console(self.task.console_select)
        self.await_gui()
        
