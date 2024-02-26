import sbslibs
import sbs
from  sbs_utils.handlerhooks import *
from sbs_utils.mast.label import label
from sbs_utils.procedural import query
from sbs_utils.procedural import gui
from sbs_utils.procedural import roles
from sbs_utils.procedural.execution import AWAIT, jump, set_variable, get_variable, set_shared_variable, get_shared_variable
from sbs_utils.procedural.timers import delay_sim
from sbs_utils.procedural.spawn import npc_spawn, player_spawn


start_text = "This is a start project for mast"

@label()
def start_server():
    #
    # Create the player ship so the clients see it
    # This is a simple script that has one playable ship
    #
    sbs.create_new_sim()


    # create a player ship
    artemis =  query.to_id(player_spawn(0,0,-500, "Artemis", "tsn", "tsn_battle_cruiser"))
    set_shared_variable("artemis", artemis)
    # Client screen need to be assigned to a ship
    # this assigns the main screen to artemis
    sbs.assign_client_to_ship(0,artemis)

    # Queue an area to place gui content
    gui.gui_section("area:2,20,80,35;")
    # Queue a text gui content
    gui.gui_text(f""" {start_text}""")

    # Present the queued Gui Content
    # as well as a set of buttons
    #
    # Buttons have text, and the can specify 
    # a label to run when selected
    
    yield AWAIT(gui.gui({
         "Start": start
    }))
    
@label()
def end_game():
    global start_text
    # 
    # Check for end game
    #
    # no more players
    
    players = roles.role("__PLAYER__")
    if len(players) == 0:
        start_text = "You lost"
        sbs.pause_sim()
        yield jump(start_server)
    #
    # No more enemies
    #
    raiders = roles.role("raider")
    if len(raiders) == 0:
        start_text = "You Won"
        print(f"end_game {start_text}")
        sbs.pause_sim()
        yield jump(start_server)
        
    yield AWAIT(delay_sim(5))
    yield jump(end_game)

@label()
def start():
    # Create the world here

    # Create a space station
    ds1 = npc_spawn( 1000,0,1000, "DS1", "tsn", "starbase_command", "behav_station")

    # Create an enemy
    k001 = npc_spawn(-1000,0,1000, "K001", "raider", "kralien_battleship", "behav_npcship")

    sbs.resume_sim()
    # jump to the end game label
    yield jump(end_game)


@label()
def start_client():
    #
    # This handles the change client button to return to the select_console
    #
    # event change_console:
    #     ->select_console
    # end_event
    #
    # Default the console to helm
    #
    set_variable("console_select",  "helm")
    yield jump(select_console)

@label()
def select_console():

    # Queue an area to play content
    gui.gui_section("area:2,20,80,35;")

    # Queue up some text
    gui.gui_text("""Select your console""")

    # Queue another area to place content
    gui.gui_section("area: 85,50, 99,90;row-height:200px")
    # Queue a set of radio button for the consoles
    gui.gui_vradio("helm,weapons,comms,science,engineering", var="console_select")
    # Add a new row to the area
    gui.gui_row("row-height: 30px;")
    # Queue blank spot to separate the accept button
    gui.gui_blank()
    # Add another row for the accept button
    # This time forcing the height of the row
    gui.gui_row("row-height: 30px;")
    # Queue up the accept button
    # The button takes the text and a label to called
    # when the button is pressed
    gui.gui_button("accept", jump=console_selected)

    
    # Show the queued gui content (no buttons)
    # And this is where you specify the on_message function so it is called
    yield AWAIT(gui.gui())
    #yield AWAIT(gui.gui({"accept": console_selected}))
    
@label()
def console_selected():
    # This is called when the accept button is pressed
    # Assign the gui client to Artemis
    sbs.assign_client_to_ship(get_variable("client_id"),get_variable("artemis"))
    # Queue showing the widgets for the console selected 
    gui.gui_console(get_variable("console_select"))
    # Present the queued gui content
    yield AWAIT(gui.gui())
    
