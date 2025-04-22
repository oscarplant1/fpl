#%%
from Player import *
from PlayerList import PlayerList
from GW_Squad import GW_Squad
from Plan import Plan
import time
import jupyter
import tkinter as tk
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

window = tk.Tk()
window.title("Hello World")

entry = tk.Entry(width=50)

def submit_button_click():
    ID = entry.get()
    if ID.isdigit():
        entry.destroy()
        button.destroy()
        create_plan(ID)

def close_selected_player():
    player_info_text.destroy()

    global next_GW_button
    next_GW_button = tk.Button(text = "Next GW",command=next_GW_click)
    next_GW_button.pack()

    global previous_GW_button
    previous_GW_button = tk.Button(text = "Previous GW",command=previous_GW_click)
    previous_GW_button.pack()

    add_player_buttons(new_plan.send_current_players()[0])

    close_button.destroy()

button = tk.Button(
    text="Submit",
    width=5,
    height=1,
    bg="blue",
    fg="yellow",
    command=submit_button_click
)

def player_click(player_number):
    for i in range(len(player_buttons)):
        player_buttons[i].destroy()
    next_GW_button.destroy()
    previous_GW_button.destroy()

    clicked_player = new_plan.future_GWs[new_plan.page].squad[player_number-1]
    
    global close_button
    close_button = tk.Button(text="X",command=close_selected_player)
    close_button.pack()

    global player_info_text
    player_info_text = tk.Text(window)
    player_info_text.pack()
    player_info_text.insert(tk.END,clicked_player.first_name + " " + clicked_player.second_name + "\n" +
                             clicked_player.team_full_name + "\n" + 
                             clicked_player.singular_position + "\n" + 
                             "Price: " + str(clicked_player.now_cost/10) + "\n" +
                             "Pts / Match: " + str(clicked_player.pts_per_match) + "\n" +
                             "Form: " + str(clicked_player.form) + "\n" +
                             "Selected by: " + str(clicked_player.ownership))

def next_GW_click():
    new_plan.page_fwd()
    for i in range(len(player_buttons)):
        player_buttons[i].destroy()
    add_player_buttons(new_plan.send_current_players()[0])

def previous_GW_click():
    new_plan.page_back()
    for i in range(len(player_buttons)):
        player_buttons[i].destroy()
    add_player_buttons(new_plan.send_current_players()[0])

def create_plan(ID):
    global next_GW_button
    next_GW_button = tk.Button(text = "Next GW",command=next_GW_click)
    next_GW_button.pack()

    global previous_GW_button
    previous_GW_button = tk.Button(text = "Previous GW",command=previous_GW_click)
    previous_GW_button.pack()

    global new_plan
    new_plan = Plan(ID)
    [player_list,id_list] = new_plan.send_current_players()

    add_player_buttons(player_list)



def add_player_buttons(player_list):

    global player1
    player1 = tk.Button(text=player_list[0],command=lambda: player_click(1))
    global player2
    player2 = tk.Button(text=player_list[1],command=lambda: player_click(2))
    global player3
    player3 = tk.Button(text=player_list[2],command=lambda: player_click(3))
    global player4
    player4 = tk.Button(text=player_list[3],command=lambda: player_click(4))
    global player5
    player5 = tk.Button(text=player_list[4],command=lambda: player_click(5))
    global player6
    player6 = tk.Button(text=player_list[5],command=lambda: player_click(6))
    global player7
    player7 = tk.Button(text=player_list[6],command=lambda: player_click(7))
    global player8
    player8 = tk.Button(text=player_list[7],command=lambda: player_click(8))
    global player9
    player9 = tk.Button(text=player_list[8],command=lambda: player_click(9))
    global player10
    player10 = tk.Button(text=player_list[9],command=lambda: player_click(10))
    global player11
    player11 = tk.Button(text=player_list[10],command=lambda: player_click(11))
    global player12
    player12 = tk.Button(text=player_list[11],command=lambda: player_click(12))
    global player13
    player13 = tk.Button(text=player_list[12],command=lambda: player_click(13))
    global player14
    player14 = tk.Button(text=player_list[13],command=lambda: player_click(14))
    global player15
    player15 = tk.Button(text=player_list[14],command=lambda: player_click(15))

    global player_buttons
    player_buttons = [player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14,player15]

    for i in range(len(player_buttons)):
        player_buttons[i].pack()

entry.pack()
button.pack()

window.mainloop()