"""
collect user's information
~first run = save all users information
second run~ = 
"""

import requests
import time
import json
import pandas as pd
import numpy as np
import time
import logging
import ast
from datetime import datetime

logging.basicConfig(filename="./usersInfoReceiver "+datetime.today().strftime("%Y-%m-%d")+".log", level=logging.INFO)

class UsersInfoReceiver:
    def __init__(self, api_key, file_name):
        self.API_KEY = api_key
        self.csv_name = file_name

    def make_usersInfo_df(self, r_get_summoner):
        df_userInfo = pd.DataFrame([r_get_summoner.json()])
    
        return df_userInfo
    
    def request_usersInfo(self, usersLeague_df):
        flag = False
        loop = 0
        series_entries = usersLeague_df["entries"]
        
        while True:
            try:
                get_summoner_api = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/" + series_entries[loop]["summonerId"]+"?api_key="+self.API_KEY
                r_get_summoner = requests.get(get_summoner_api)
            except KeyError:
                break
            
            # request time out
            if r_get_summoner.status_code == 429:
                logging.warning(str(loop)+" time exceed")
                time.sleep(30)
                continue
            elif r_get_summoner.status_code != 200:
                logging.error("status code = "+str(r_get_summoner.status_code))
                time.sleep(10)
                continue
            
            if not flag:
                flag = True
                usersInfo_df_after = self.make_usersInfo_df(r_get_summoner)
            else:
                usersInfo_df = self.make_usersInfo_df(r_get_summoner)
                usersInfo_df_after = pd.concat([usersInfo_df_after, usersInfo_df], axis=0).reset_index(drop=True)
                
            if loop%100==99:
                flag=False
                usersInfo_df_after.to_csv(self.csv_name, mode="a", header=False)
                logging.info(str(loop)+str(datetime.today()))
            
            loop += 1            
            
        return usersInfo_df_after
    
    def run(self, usersLeague_df):
        return self.request_usersInfo(usersLeague_df)