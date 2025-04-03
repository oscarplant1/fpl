import requests, json
import pandas as pd
import openpyxl
import xlwings
import time
import pprint
from unidecode import unidecode
from xlwings import Book
from pprint import pprint
from tqdm.auto import tqdm
from openpyxl import Workbook
from openpyxl import load_workbook
tqdm.pandas()

pd.set_option('display.max_columns', None)

# base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'

# get data from bootstrap-static endpoint
r = requests.get(base_url+'bootstrap-static/').json()

players = pd.json_normalize(r['elements'])
teams = pd.json_normalize(r['teams'])
positions = pd.json_normalize(r['element_types'])

class Player:
    def __init__(self,id):
        self.id = id
        
        #Filtering data frame by given id
        player_data = players[players["id"] == id]
        team_data = teams[teams["id"] == int(player_data["team"].to_string(index=False))]
        position_data = positions[positions["id"] == int(player_data["element_type"].to_string(index=False))]

        #Attributes from players data frame
        self.first_name = player_data["first_name"].to_string(index=False)
        self.second_name = player_data["second_name"].to_string(index=False)
        self.web_name = player_data["web_name"].to_string(index=False)
        self.now_cost = float(player_data["now_cost"].to_string(index=False))
        self.ownership = float(player_data["selected_by_percent"].to_string(index=False))
        self.pts_per_match = float(player_data["points_per_game"].to_string(index=False))
        self.form = float(player_data["form"].to_string(index=False))
        self.current_points = int(player_data["event_points"].to_string(index=False))
        self.total_points = int(player_data["total_points"].to_string(index=False))
        self.GW_transfers_in = int(player_data["transfers_in_event"].to_string(index=False))
        self.GW_transfers_out = int(player_data["transfers_out_event"].to_string(index=False))
        self.total_bonus = int(player_data["bonus"].to_string(index=False))
        self.status = player_data["status"].to_string(index=False)

        #Stats
        self.starts = int(player_data["starts"].to_string(index=False))
        self.minutes = int(player_data["minutes"].to_string(index=False))
        self.goals = int(player_data["goals_scored"].to_string(index=False))
        self.assists = int(player_data["assists"].to_string(index=False))
        self.xG = float(player_data["expected_goals"].to_string(index=False))
        self.xA = float(player_data["expected_assists"].to_string(index=False))
        self.xGI = float(player_data["expected_goal_involvements"].to_string(index=False))
        self.xG_per90 = float(player_data["expected_goals_per_90"].to_string(index=False))
        self.xA_per90 = float(player_data["expected_assists_per_90"].to_string(index=False))
        self.xGI_per90 = float(player_data["expected_goal_involvements_per_90"].to_string(index=False))
        self.yellow_cards = int(player_data["yellow_cards"].to_string(index=False))
        self.red_cards = int(player_data["red_cards"].to_string(index=False))
        self.own_goals = int(player_data["own_goals"].to_string(index=False))

        self.cost_change = float(player_data["cost_change_start"].to_string(index=False))
        self.starting_cost = self.now_cost - self.cost_change

        #Attributes from teams data frame
        self.team_full_name = team_data["name"].to_string(index=False)
        self.team_short_name = team_data["short_name"].to_string(index=False)
        self.team_id = team_data["id"].to_string(index=False)

        #Attributes from positions data frame
        self.singular_position = position_data["singular_name"].to_string(index=False)
        self.plural_position = position_data["plural_name"].to_string(index=False)
        self.position_short = position_data["singular_name_short"].to_string(index=False)

    def compare_to(self,Player):
        d = {self.web_name: [self.starts,self.minutes,self.goals,self.assists,self.xG,self.xG_per90,self.xA,self.xA_per90,self.xGI,self.xGI_per90,self.yellow_cards,self.red_cards,self.own_goals,
                             self.now_cost/10,self.ownership,self.pts_per_match,self.total_points,self.total_bonus], 
             Player.web_name: [Player.starts,Player.minutes,Player.goals,Player.assists,Player.xG,Player.xG_per90,Player.xA,Player.xA_per90,Player.xGI,Player.xGI_per90,Player.yellow_cards,Player.red_cards,Player.own_goals,
                               Player.now_cost/10,Player.ownership,Player.pts_per_match,Player.total_points,Player.total_bonus]}
        df = pd.DataFrame(data=d,index=["Starts","Minutes Played","Goals","Assists","xG","xG per 90","xA","xA per 90","xGI","xGI per 90","Yellow Cards","Red Cards", "Own Goals",
                                        "Cost","Ownership","Points per Match","Total Points","Total Bonus Points"])
        print(df)