# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:22:40 2020

@author: jhs
"""
import requests
import time
import json
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime

logging.basicConfig(filename="./usersMatchList "+datetime.today().strftime("%Y-%m-%d")+".log", level=logging.INFO)

class UsersMatchlistReceiver:
    def __init__(self, api_key, csv_name):
        self.API_KEY = api_key
        self.csv_name = csv_name
        self.seasons = "13"
        
    def make_usersMatchlist_df(self, r_get_matchList, users_accountId):
        r_get_matchList_json = r_get_matchList.json()
        
        users_matchList_df = pd.DataFrame(r_get_matchList_json["matches"])
        users_matchList_df['accountId'] = users_accountId
        
        return users_matchList_df
    
    def request_usersMatchlist(self, usersInfo_df):
        # beginIndex = 0
        
        for users_accountId in usersInfo_df["accountId"]:
            beginIndex = 0
            flag = False
            
            while True:
                get_matchList = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+users_accountId \
                    +"?season="+self.seasons+"&beginIndex="+str(beginIndex)+"&api_key="+self.API_KEY
                r_get_matchList = requests.get(get_matchList)
                
                # request time out
                if r_get_matchList.status_code == 429:
                    # print("time exceed")
                    logging.warning(users_accountId+" time exceed")
                    time.sleep(30)
                    continue
                # request status code not 200(normal code)
                elif r_get_matchList.status_code != 200:
                    # print("status code = ", r_get_matchList.status_code)
                    logging.error("status code = "+str(r_get_matchList.status_code))
                    time.sleep(10)
                    continue
                
                # if no matches
                if r_get_matchList.json()['matches'] == []:
                    # print("no matches in "+users_accountId+" idx= "+str(beginIndex))
                    break
                    
                if not flag:
                    flag = True
                    users_matchList_df_after = self.make_usersMatchlist_df(r_get_matchList, users_accountId)
                else:
                    users_matchList_df = self.make_usersMatchlist_df(r_get_matchList, users_accountId)
                    users_matchList_df_after = pd.concat([users_matchList_df_after, users_matchList_df], axis=0)
                
                beginIndex+=100
            
            # find all matches
            users_matchList_df_after.to_csv(self.csv_name, mode="a", header=False)
            logging.info(users_accountId+" to csv, beginIdxx= "+str(beginIndex)+" "+str(datetime.today()))
            
    # def run(self):
    #     print("loading usersInfo.csv file")
    #     usersInfo_df = pd.read_csv("usersInfo_test.csv")
    #     columns_df = pd.read_csv("columnsInfo_web.csv")
    
    #     columns_list = columns_df[~columns_df["usersInfo"].isna()]["usersInfo"]
    #     usersInfo_df.columns = columns_list
    #     usersInfo_df = usersInfo_df.drop("idx_col", axis=1)
        
    #     print("load complete")
    #     self.request_usersMatchlist(usersInfo_df)
        
    def run(self, usersInfo_df):
        return self.request_usersMatchlist(usersInfo_df)