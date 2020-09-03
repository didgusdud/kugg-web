import requests
import time
import json
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime

logging.basicConfig(filename="./"+datetime.today().strftime("%Y-%m-%d")+".log", level=logging.INFO)
# tier list ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
# ["challengerleagues", "grandmasterleagues", "masterleagues"]


class UsersLeagueReceiver():
    def __init__(self, api_key, file_name):
        self.API_KEY = api_key
        self.csv_name = file_name
        self.tiers = ["CHALLENGER", "GRANDMASTER", "MASTER"] # default setting
        self.divisions = []
        self.columns_list = ["miniSeries_target", "miniSeries_wins",
                    "miniSeries_losses", "miniSeries_progress"]
        
    def set_tiers(self, tiers_list):
        self.tiers = tiers_list
        
    def set_divisions(self, divisions_list):
        self.divisions = divisions_list
        
    def get_LEAGUEV4(self, r_get_league):
        r_get_league_json = r_get_league.json()
        df_league_userInfo = pd.DataFrame(r_get_league_json)
        if not "miniSeries" in df_league_userInfo.columns:
            df_league_userInfo[self.columns_list[0]] = np.nan
            df_league_userInfo[self.columns_list[1]] = np.nan
            df_league_userInfo[self.columns_list[2]] = np.nan
            df_league_userInfo[self.columns_list[3]] = np.nan
        else:
            series_miniSeries = df_league_userInfo.loc[
                df_league_userInfo["miniSeries"].notnull(), "miniSeries"]
                
            df_miniSeries_toDF = pd.DataFrame(series_miniSeries.values.tolist(),
                                                  index = series_miniSeries.index.tolist())
            df_miniSeries_toDF.columns = self.columns_list

            df_league_userInfo = pd.concat([df_league_userInfo, df_miniSeries_toDF], 
                                           axis=1)
            df_league_userInfo = df_league_userInfo.drop("miniSeries", axis=1)
    
        return df_league_userInfo

    def request_usersLeague(self):
        tiers = ["GOLD"]
        divisions = ["IV", "III", "II", "I"]
        flag = False
        
        for t in tiers:
            for d in divisions:
                page = 1
                while True:
                    get_league_api = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/"+t+"/"+d+"?page="+str(page)+"&api_key="+self.API_KEY
                    r_get_league = requests.get(get_league_api)
                    # print(t, d, page, r_get_league)
                    logging.info(t+" "+d+" "+str(page)+" "+str(r_get_league.status_code))
                    
                    # request 시간 초과
                    if r_get_league.status_code == 429:
                        # print("time exceed")
                        logging.warning("time exceed")
                        time.sleep(30)
                        continue
                    elif r_get_league.status_code != 200:
                        # print("status code = ", r_get_league.status_code)
                        logging.error("status code = "+r_get_league.status_code)
                        time.sleep(10)
                        continue
                    
                    if r_get_league.json() == []:
                        # print("page exceed")
                        logging.info("page exceed")
                        break
                    
                    if not flag:
                        flag = True
                        usersLeague_df_after = self.get_LEAGUEV4(r_get_league)
                    else:
                        usersLeague_df = self.get_LEAGUEV4(r_get_league)
                        usersLeague_df_after = pd.concat([usersLeague_df_after, usersLeague_df], axis=0).reset_index(drop=True)
                            
                    page += 1

                usersLeague_df_after.to_csv(self.csv_name, mode="a", header=False)
                flag = False
                logging.info(str(page)+str(datetime.today()))

        #    usersLeague_df_after.reset_index()
        #    usersLeague_df_after = usersLeague_df_after.drop("index")
                
        return usersLeague_df_after
    
    def make_UsersLeague(self):
        self.request_LEAGUEV4()
