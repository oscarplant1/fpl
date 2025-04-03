from Player import *
from PlayerList import PlayerList
import warnings
tqdm.pandas()

class GW_Squad:
    def __init__(self,id,GW):

        self.id = id

        r = 0
        self.current_GW = 0
        while r != {'detail': 'Not found.'}:
            self.current_GW = self.current_GW + 1
            url = "https://fantasy.premierleague.com/api/entry/"+ str(self.id) + "/event/" + str(self.current_GW) + "/picks/"
            r = requests.get(url).json()
        self.current_GW = self.current_GW - 1

        self.input_GW = GW
        self.squad = [0] * 15

        self.ClearSquad()
 
        self.points = -1
        self.total_points = -1
        self.GW_rank = -1
        self.overall_rank = -1
        self.percentile_rank = -1
        self.bank = -1
        self.squad_value = -1
        self.transfers_used = -1
        self.transfers_cost = -1
        self.bench_points = -1

        self.player_positions = ["GKP","DEF","MID","FWD"]
        self.max_player_counts = [2,5,5,3]

        #Import squad
        if self.input_GW < self.current_GW:
            url = "https://fantasy.premierleague.com/api/entry/" + str(self.id) + "/event/" + str(self.input_GW) + "/picks/"
            r = requests.get(url).json()
            picks = pd.json_normalize(r["picks"])
            summary = pd.json_normalize(r["entry_history"])

            self.points = int(summary["points"].to_string(index=False))
            self.total_points = int(summary["total_points"].to_string(index=False))
            self.GW_rank = int(summary["rank"].to_string(index=False))
            self.overall_rank = int(summary["overall_rank"].to_string(index=False))
            self.percentile_GW_rank = int(summary["percentile_rank"].to_string(index=False))
            self.bank = float(summary["bank"].to_string(index=False))/10
            self.squad_value = float(summary["value"].to_string(index=False))/10
            self.transfers_used = int(summary["event_transfers"].to_string(index=False))
            self.transfers_cost = int(summary["event_transfers_cost"].to_string(index=False))
            self.bench_points = int(summary["points_on_bench"].to_string(index=False))

            for i in range(picks.shape[0]):
                current_player = Player(int(picks[picks["position"]==i+1]["element"].to_string(index=False)))
                if current_player.position_short != "MNG":
                    self.squad[i] = current_player
        else:
            url = "https://fantasy.premierleague.com/api/entry/" + str(self.id) + "/event/" + str(self.current_GW) + "/picks/"
            r = requests.get(url).json()
            picks = pd.json_normalize(r["picks"])            

            for i in range(picks.shape[0]):
                current_player = Player(int(picks[picks["position"]==i+1]["element"].to_string(index=False)))
                if current_player.position_short != "MNG":
                    self.squad[i] = current_player
        
        #Import transfer History and get purchase prices
        url = "https://fantasy.premierleague.com/api/entry/" + str(self.id) + "/transfers/"
        r = requests.get(url).json()
        transfers = pd.json_normalize(r)

        squad_ids = [0]*len(self.squad)
        now_costs = [0]*len(self.squad)
        for i in range(len(squad_ids)):
            squad_ids[i] = self.squad[i].id
            now_costs[i] = self.squad[i].now_cost

        #Getting purchase prices of squad
        self.purchase_prices = [0] * len(self.squad)
        for i in range(len(self.purchase_prices)):
            current_id = squad_ids[i]
            if not(current_id in transfers["element_in"].values):
                purchase_price = self.squad[i].starting_cost/10
            else:
                warnings.filterwarnings(
                    action='ignore', category=UserWarning, message=r"Boolean Series.*"
                )
                GW_last_transferred_in = transfers[transfers["element_in"]==current_id].max(axis = "rows")["event"]
                purchase_price = float(transfers[transfers["element_in"]==current_id][transfers["event"]==GW_last_transferred_in]["element_in_cost"].to_string(index=False))/10
            self.purchase_prices[i] = purchase_price

        #Calculate selling prices
        self.selling_prices = [0]*len(self.squad)
        for i in range(len(self.selling_prices)):
            difference = round(now_costs[i]/10 - self.purchase_prices[i],1)
            selling_price = round((difference*10//2)/10 + self.purchase_prices[i],1)
            self.selling_prices[i] = selling_price

        self.count_Positions()

    def count_Positions(self):
        player_counts = [0,0,0,0]

        for i in range(len(self.squad)):
            if not isinstance(self.squad[i],int):
                    player_counts[self.player_positions.index(self.squad[i].position_short)] += 1

        self.GKcount = player_counts[0]
        self.DEFcount = player_counts[1]
        self.MIDcount = player_counts[2]
        self.FWDcount = player_counts[3] 

    def print_squad(self):
        selected_GW = self.squad
        for i in range(len(selected_GW)):
            if isinstance(selected_GW[i],int):
                print(selected_GW[i])
            else:
                print(selected_GW[i].id,selected_GW[i].web_name)

    def remove_player(self,id):
        player_to_remove = Player(id)

        squad_ids = [0]*len(self.squad)

        for i in range(len(squad_ids)):
            squad_ids[i] = self.squad[i].id

        if id in squad_ids:
            self.selling_prices.remove(self.selling_prices[squad_ids.index(id)])
            self.purchase_prices.remove(self.purchase_prices[squad_ids.index(id)])
            self.squad.remove(self.squad[squad_ids.index(id)])
            self.count_Positions()

    def add_player(self,id):
        player_to_add = Player(id)
        player_counts = [self.GKcount,self.DEFcount,self.MIDcount,self.FWDcount]
        if player_counts[self.player_positions.index(player_to_add.position_short)] < self.max_player_counts[self.player_positions.index(player_to_add.position_short)]:
            self.squad.append(player_to_add)
            self.selling_prices.append(player_to_add.now_cost/10)
            self.purchase_prices.append(player_to_add.now_cost/10)
            player_counts[self.player_positions.index(player_to_add.position_short)] += 1

            self.GKcount = player_counts[0]
            self.DEFcount = player_counts[1]
            self.MIDcount = player_counts[2]
            self.FWDcount = player_counts[3]     

    def ClearSquad(self):
        self.squad = [0] * 15

    