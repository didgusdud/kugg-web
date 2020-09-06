import requests
import time
import json
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime

logging.basicConfig(filename="./"+datetime.today().strftime("%Y-%m-%d")+".log", level=logging.INFO)

class MatchInfoReceiver:
    def __init__(self, api_key, csv_name):
        self.API_KEY = api_key
        self.csv_name = csv_name
    
    def make_matchInfo_df(self, r_get_matchInfo):
        r_get_matchInfo_json = r_get_matchInfo.json()
        users_matchInfo_df = pd.DataFrame([r_get_matchInfo_json])
        
        return users_matchInfo_df
    
    def request_matchInfo(self, unique_gameId):
        loop = 0
        flag= False

        while True:
            get_matchInfo = "https://kr.api.riotgames.com/lol/match/v4/matches/"+ \
                str(unique_gameId[loop]) +"?api_key="+self.API_KEY
            r_get_matchInfo = requests.get(get_matchInfo)
            
            # request 시간 초과
            if r_get_matchInfo.status_code == 429:
                #print("time exceed")
                time.sleep(30)
                logging.warning(str(unique_gameId[loop])+" time exceed")
                continue
            # request가 200 이외에 다른 것들이 들어오는 경우 
            elif r_get_matchInfo.status_code != 200:
                #print("status code = ", r_get_matchInfo.status_code)
                logging.error("status code = "+str(r_get_matchInfo.status_code))
                time.sleep(10)
                continue
            
            if not flag:
                flag = True
                users_matchInfo_df_after = self.make_matchInfo_df(r_get_matchInfo)
            else:
                users_matchInfo_df = self.make_matchInfo_df(r_get_matchInfo)
                users_matchInfo_df_after = pd.concat([users_matchInfo_df_after, users_matchInfo_df], axis=0)
    
            # find all matches
            if loop%100==99:
                users_matchInfo_df_after.to_csv(self.csv_name, mode="a", header=False)
                logging.info(str(unique_gameId[loop])+" to csv, beginIdex= "+str(datetime.today()))
            
            loop +=1
            
            if loop==len(unique_gameId):
                break
        
    def run(self, unique_gameId):
        self.request_matchInfo(unique_gameId)

        