from Player import *
from PlayerList import PlayerList
from GW_Squad import GW_Squad
tqdm.pandas()

class Plan:
    def __init__(self,id):
        self.id = id

        r = requests.get(base_url+'bootstrap-static/').json()

        players = pd.json_normalize(r['elements'])
        teams = pd.json_normalize(r['teams'])
        positions = pd.json_normalize(r['element_types'])

        self.team_list = teams["name"].values

        r = 0
        self.next_GW = 0
        while r != {'detail': 'Not found.'}:
            self.next_GW = self.next_GW + 1
            url = "https://fantasy.premierleague.com/api/entry/"+ str(self.id) + "/event/" + str(self.next_GW) + "/picks/"
            r = requests.get(url).json()
        
        self.page = 0

        self.reset_plan()

        #print(self.next_GW + self.page)
        #self.future_GWs[self.page].print_squad()
        #Importing fixtures

        url = "https://fantasy.premierleague.com/api/fixtures/"
        r = requests.get(url).json()
        fixtures = pd.json_normalize(r)

        #FDR table
        #Team "id"s go from 1-20
        #Setting up 2D array 20* 38 - add difficulty and DGWs to 3rd dimension
        self.FDR = [0]*20
        for i in range(20):
            self.FDR[i] = [0 for j in range(38)]

        for GW in range(1,39):
            GW_fixtures = fixtures[fixtures["event"]==GW]
            for team_id in range(1,21):
                fixture_details = []
                home_fixture_indices = []
                away_fixture_indices = []
                #Check home column
                if team_id in GW_fixtures["team_h"].values:
                    for i in range(len(GW_fixtures["team_h"].values)):
                        if GW_fixtures["team_h"].values[i] == team_id:
                            home_fixture_indices.append(i)

                    for k in range(len(home_fixture_indices)):
                        opponent = GW_fixtures["team_a"].values[home_fixture_indices[k]].item()
                        difficulty = GW_fixtures["team_h_difficulty"].values[home_fixture_indices[k]].item()
                        fixture_details.append(opponent)
                        fixture_details.append("H")
                        fixture_details.append(difficulty)

                #Check away column
                if team_id in GW_fixtures["team_a"].values:
                    for i in range(len(GW_fixtures["team_a"].values)):
                        if GW_fixtures["team_a"].values[i] == team_id:
                            away_fixture_indices.append(i)

                    for k in range(len(away_fixture_indices)):
                        opponent = GW_fixtures["team_h"].values[away_fixture_indices[k]].item()
                        difficulty = GW_fixtures["team_a_difficulty"].values[away_fixture_indices[k]].item()

                        #Insert away fixtures in correct spot between/before/after home fixtures
                        home_fixture_indices.append(away_fixture_indices[k])
                        home_fixture_indices.sort()
                        new_index = home_fixture_indices.index(away_fixture_indices[k])
                        fixture_details.insert(3*new_index,opponent)
                        fixture_details.insert(3*new_index+1,"A")
                        fixture_details.insert(3*new_index+2,difficulty)
 

                self.FDR[team_id-1][GW-1] = fixture_details
                

    def print_fixtures(self,GW):
        for i in range(20):
            print_list = []
            for j in range(len(self.FDR[i][GW-1])):
                if j%3==0:
                    print_list.append(self.team_list[self.FDR[i][GW-1][j]-1])
                else:
                    print_list.append(self.FDR[i][GW-1][j])
            print(print_list)


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

    def send_current_players(self):
        temp_player_list = []
        temp_id_list = []
        for i in range(15):
            temp_player_list.append(self.future_GWs[self.page].squad[i].web_name)
            temp_id_list.append(self.future_GWs[self.page].squad[i].id)
        return [temp_player_list,temp_id_list]
    

