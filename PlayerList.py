from Player import *
tqdm.pandas()

class PlayerList:
    def __init__(self):
        self.filter()

    def get_List(self):
        return self.List

    def reset_list(self):
        self.List = [0] * (players.shape[0] - 1)
        for i in range(players.shape[0]-1):
            CurrentPlayer = Player(i+1)
            self.List[i] = Player(i+1)


    def display_List(self):
        for i in range(len(self.List)):
            print(self.List[i].web_name
                  ,self.List[i].id
                  )

    def filter(self,position = "all", team = "all", max_price = "any", sort_by = "now_cost", include_managers = False, descending = True):
        self.reset_list()

        #Filter by position
        if position in ["Goalkeepers","Defenders","Midfielders","Forwards","Managers"]:
            sub_list = []
            for i in range(len(self.List)):
                if self.List[i].plural_position == position:
                    sub_list.append(self.List[i])
            self.List = sub_list

        #Filter by team
        #######NOT FUTURE SEASON PROOF#######
        if team in ["Arsenal","Aston Villa","Bournemouth","Brentford","Brighton","Chelsea","Crystal Palace","Everton","Fulham","Ipswich","Leicester","Liverpool","Man City","Man Utd","Newcastle","Nott'm Forest","Southampton","Spurs","West Ham","Wolves"]:
            sub_list = []
            for i in range(len(self.List)):
                if self.List[i].team_full_name == team:
                    sub_list.append(self.List[i])
            self.List = sub_list

        #Filter by max_price
        if isinstance(max_price, float) or isinstance(max_price, int):
            sub_list = []
            for i in range(len(self.List)):
                if self.List[i].now_cost <= max_price*10:
                    sub_list.append(self.List[i])
            self.List = sub_list            

        #Filter managers out
        if not include_managers:
            sub_list = []
            for i in range(len(self.List)):
                if self.List[i].plural_position != "Managers":
                    sub_list.append(self.List[i])
            self.List = sub_list 

        #If unrecognised sort_by entry, sort_by cost
        if sort_by not in ["first_name","second_name","web_name","now_cost","form","ownership","current_points","total_points","GW_transfers_in","GW_transfers_out","total_bonus","xG","xG_per90","xA","xA_per90","xGI","xGI_per90"]:
            sort_by = "now_cost"
       
        #Insertion sort using temp list of sort_by attribute
        temp_list = [0]*len(self.List)
        if sort_by in ["now_cost","form","ownership","current_points","total_points","GW_transfers_in","GW_transfers_out","total_bonus","xG","xG_per90","xA","xA_per90","xGI","xGI_per90"]:
            for i in range(len(temp_list)):
                temp_list[i] = getattr(self.List[i],sort_by)                 
        else:
            for i in range(len(temp_list)):
                temp_list[i] = unidecode(getattr(self.List[i],sort_by)) 

        for i in range(1, len(self.List)): 
            key1 = self.List[i] 
            key2 = temp_list[i]
            j = i-1
            if sort_by in ["now_cost","form","ownership","current_points","total_points","GW_transfers_in","GW_transfers_out","total_bonus"]:
                while j >= 0 and key2 > temp_list[j]:
                    self.List[j+1] = self.List[j] 
                    temp_list[j+1] = temp_list[j]
                    j = j - 1
            else:
                while j >= 0 and key2 < temp_list[j]:
                    self.List[j+1] = self.List[j] 
                    temp_list[j+1] = temp_list[j]
                    j = j - 1
            self.List[j+1] = key1 
            temp_list[j+1] = key2

        #Reordering
        if not descending:
            self.List.reverse()        

        return

    def search(self,search_string):
        sub_list = []

        for i in range(len(search_string)):
            if search_string[i] not in "abcdefghijklmnopqrstuvwxyz.ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return

        for i in range(len(self.List)):
            if search_string.lower() == unidecode(self.List[i].first_name.lower())[0:len(search_string)] or search_string.lower() == unidecode(self.List[i].second_name.lower())[0:len(search_string)] or search_string.lower() == unidecode(self.List[i].web_name.lower())[0:len(search_string)]:
                sub_list.append(self.List[i]) 

        self.List = sub_list

