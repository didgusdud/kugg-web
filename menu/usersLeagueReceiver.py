import requests
import time
import json
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime

logging.basicConfig(filename="./usersLeagueReceiver "+datetime.today().strftime("%Y-%m-%d")+".log", level=logging.INFO)
# tier list ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
# ["challengerleagues", "grandmasterleagues", "masterleagues"]


class UsersLeagueReceiver:
    def __init__(self, api_key, file_name):
        self.API_KEY = api_key
        self.csv_name = file_name
        self.tiers = ["challengerleagues", "grandmasterleagues", "masterleagues"] # default setting
        self.divisions = []
        # self.columns_list = ["miniSeries_target", "miniSeries_wins",
        #             "miniSeries_losses", "miniSeries_progress"]
        
    def set_tiers(self, tiers_list):
        self.tiers = tiers_list
        
    def set_divisions(self, divisions_list):
        self.divisions = divisions_list
        
    def make_usersLeague_df(self, r_get_league):
        r_get_league_json = r_get_league.json()
        df_league_userInfo = pd.DataFrame(r_get_league_json)
    
        return df_league_userInfo

    def request_usersLeague(self):
        flag = False
        
        for t in self.tiers:
            get_league_api = "https://kr.api.riotgames.com/lol/league/v4/"+t+"/by-queue/RANKED_SOLO_5x5?api_key="+self.API_KEY
            r_get_league = requests.get(get_league_api)
            # print(t, d, page, r_get_league)
            logging.info(t+" "+str(r_get_league.status_code))
            
            # request 시간 초과
            if r_get_league.status_code == 429:
                # print("time exceed")
                logging.warning("time exceed")
                time.sleep(30)
                continue
            elif r_get_league.status_code != 200:
                # print("status code = ", r_get_league.status_code)
                logging.error("status code = "+str(r_get_league.status_code))
                time.sleep(10)
                continue
            
            if not flag:
                flag = True
                usersLeague_df_after = self.make_usersLeague_df(r_get_league)
            else:
                usersLeague_df = self.make_usersLeague_df(r_get_league)
                usersLeague_df_after = pd.concat([usersLeague_df_after, usersLeague_df], axis=0).reset_index(drop=True)

        usersLeague_df_after.to_csv(self.csv_name, mode="a", header=False)
        # logging.info(str(page)+str(datetime.today()))
                
        return usersLeague_df_after
    
    def run(self):
        return self.request_usersLeague()