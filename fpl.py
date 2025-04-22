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

def player1_click():
    pass
def player2_click():
    pass
def player3_click():
    pass
def player4_click():
    pass
def player5_click():
    pass
def player6_click():
    pass
def player7_click():
    pass
def player8_click():
    pass
def player9_click():
    pass
def player10_click():
    pass
def player11_click():
    pass
def player12_click():
    pass
def player13_click():
    pass
def player14_click():
    pass
def player15_click():
    pass

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

button = tk.Button(
    text="Submit",
    width=5,
    height=1,
    bg="blue",
    fg="yellow",
    command=submit_button_click
)

def create_plan(ID):

    next_GW_button = tk.Button(text = "Next GW",command=next_GW_click)
    next_GW_button.pack()

    next_GW_button = tk.Button(text = "Previous GW",command=previous_GW_click)
    next_GW_button.pack()

    global new_plan
    new_plan = Plan(ID)
    [player_list,id_list] = new_plan.send_current_players()

    add_player_buttons(player_list)



def add_player_buttons(player_list):

    global player1
    player1 = tk.Button(text=player_list[0],command=player1_click)
    global player2
    player2 = tk.Button(text=player_list[1],command=player2_click)
    global player3
    player3 = tk.Button(text=player_list[2],command=player3_click)
    global player4
    player4 = tk.Button(text=player_list[3],command=player4_click)
    global player5
    player5 = tk.Button(text=player_list[4],command=player5_click)
    global player6
    player6 = tk.Button(text=player_list[5],command=player6_click)
    global player7
    player7 = tk.Button(text=player_list[6],command=player7_click)
    global player8
    player8 = tk.Button(text=player_list[7],command=player8_click)
    global player9
    player9 = tk.Button(text=player_list[8],command=player9_click)
    global player10
    player10 = tk.Button(text=player_list[9],command=player10_click)
    global player11
    player11 = tk.Button(text=player_list[10],command=player11_click)
    global player12
    player12 = tk.Button(text=player_list[11],command=player12_click)
    global player13
    player13 = tk.Button(text=player_list[12],command=player13_click)
    global player14
    player14 = tk.Button(text=player_list[13],command=player14_click)
    global player15
    player15 = tk.Button(text=player_list[14],command=player15_click)

    global player_buttons
    player_buttons = [player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14,player15]

    for i in range(len(player_buttons)):
        player_buttons[i].pack()

entry.pack()
button.pack()

window.mainloop()