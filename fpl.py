#%%
from Player import *
from PlayerList import PlayerList
from GW_Squad import GW_Squad
from Plan import Plan
import time
import jupyter
import dearpygui.dearpygui as dpg
#newPlan = Plan(566579)

#Salah = Player(328)
#Fernandes = Player(366)
#Bowen = Player(514)
#Fernandes.Compare_to(Bowen)

#testList = PlayerList()
#testList.filter(sort_by="xGI",descending=False)
#testList.search("Na")
#testList.display_List()

# %%
dpg.create_context()
dpg.create_viewport(title='Custom Title')
dpg.set_global_font_scale(3)

with dpg.window(label="MainWindow",width = 600, height=250,tag="main_window"):

    dpg.add_button(label="Player1",tag="player1")

    dpg.add_text("Enter Team ID",tag="Team_ID_Instruction")
    input_field = dpg.add_input_text(label="Enter ID",tag="input_box")

    def submit_id_button_click(sender, app_data):
        entered_text = dpg.get_value(input_field)
        if entered_text.isdigit():
            dpg.delete_item("Team_ID_Instruction")
            dpg.delete_item("input_box")
            dpg.delete_item("Submit_button")

    dpg.add_button(label="Submit",callback=submit_id_button_click, tag="Submit_button")

dpg.set_primary_window("main_window",True)        
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()