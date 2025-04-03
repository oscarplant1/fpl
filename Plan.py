from Player import *
from PlayerList import PlayerList
from GW_Squad import GW_Squad
tqdm.pandas()

class Plan:
    def __init__(self,id):
        self.id = id

        r = 0
        self.next_GW = 0
        while r != {'detail': 'Not found.'}:
            self.next_GW = self.next_GW + 1
            url = "https://fantasy.premierleague.com/api/entry/"+ str(self.id) + "/event/" + str(self.next_GW) + "/picks/"
            r = requests.get(url).json()
        
        self.page = 0

        self.reset_plan()

        print(self.next_GW + self.page)
        self.future_GWs[self.page].print_squad()
        #Importing fixtures

        url = "https://fantasy.premierleague.com/api/fixtures/"
        r = requests.get(url).json()
        fixtures = pd.json_normalize(r)
        
        #FDR table

        #Team "id"s go from 1-20
        #Setting up 2D array 20 * 38 - add difficulty and DGWs to 3rd dimension
        self.FDR =[[""] * 38 for i in range(20)]
    
        for column_index in range(38):
            GW = column_index + 1 
            GW_fixtures = fixtures[fixtures["event"]==GW]

            for row_index in range(20):
                team_id = row_index + 1  

                fixture_string = ""

                #Is team home team
                if team_id in GW_fixtures["team_h"].values:
                    teams_fixtures = GW_fixtures[GW_fixtures["team_h"]==team_id]
                    for i in range(teams_fixtures.shape[0]):
                        #Adding away team
                        fixture_string = fixture_string + str(int(teams_fixtures["team_a"].values[i])) + ","
                        #Adding difficulty
                        fixture_string = fixture_string + str(int(teams_fixtures["team_h_difficulty"].values[i])) + ","
                        #Adding h/a
                        fixture_string = fixture_string + "h,"
                        
                #Is team away team
                if team_id in GW_fixtures["team_a"].values:
                    teams_fixtures = GW_fixtures[GW_fixtures["team_a"]==team_id]
                    for i in range(teams_fixtures.shape[0]):
                        #Adding home team
                        fixture_string = fixture_string + str(int(teams_fixtures["team_h"].values[i])) + ","
                        #Adding difficulty
                        fixture_string = fixture_string + str(int(teams_fixtures["team_a_difficulty"].values[i])) + ","
                        #Adding h/a
                        fixture_string = fixture_string + "a,"

                self.FDR[row_index][column_index] = fixture_string
            #print("------------------------------------")
                

    def page_fwd(self):
        if self.page < (38 - self.next_GW) and len(self.future_GWs[self.page].squad) == 15:
            self.page += 1
            print(self.next_GW + self.page)
            self.future_GWs[self.page].print_squad()
        return

    def page_back(self):
        if self.page > 0  and len(self.future_GWs[self.page].squad) == 15:
            self.page -= 1
            print(self.next_GW + self.page)
            self.future_GWs[self.page].print_squad()
        return
    
    def add_player_to_page(self,id):
        for i in range(self.page,len(self.future_GWs)):
            self.future_GWs[i].add_player(id)
        
        self.future_GWs[self.page].print_squad()
        

    def remove_player_from_page(self,id):
        for i in range(self.page,len(self.future_GWs)):
            self.future_GWs[i].remove_player(id)

        self.future_GWs[self.page].print_squad()

    def reset_GW(self,GW):
        self.future_GWs[GW - self.next_GW] = GW_Squad(self.id,GW)

    def reset_plan(self):
        #self.future_GWs = [GW_Squad(self.id,self.next_GW)]*(39 - self.next_GW)
        self.current_Squad = GW_Squad(self.id,self.next_GW)
        self.future_GWs = [self.current_Squad for i in range(39 - self.next_GW)]


    def print_GW_Squad(self,GW):
        chosen_Squad = self.future_GWs[GW - self.next_GW]
        chosen_Squad.print_squad()
    

