# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:49:15 2020

@author: 6794c
"""
import usersLeagueReceiver
import usersInfoReceiver

# input your api key when you need

class DataReceiver:
    def __init__(self):
        self.API_KEY = None
        self.usersLeague_csv_name = "usersLeague.csv"
        self.usersInfo_csv_name = "usersInfo.csv"
        self.usersMatchlist_csv_name = "usersMatchlist.csv"
        
        self.usersLeague_receiver = usersLeagueReceiver.UsersLeagueReceiver(
            self.API_KEY, self.usersLeague_csv_name)
        self.usersInfo_receiver = usersInfoReceiver.UsersInfoReceiver(
            self.API_KEY, self.usersInfo_csv_name)
        
    def usersInfo_testcode(self):
        print("loading usersLeague.csv")
        columns_list = pd.read_csv("columnsInfo_web.csv")
        columns_list = columns_list[~columns_list["usersLeague"].isna()]["usersLeague"]        
        usersLeague_df = pd.read_csv("usersLeague.csv")
        usersLeague_df.columns = columns_list
        usersLeague_df = usersLeague_df.drop("idx_col", axis=1)
        
        
    def run(self):
        usersLeague_df = self.usersLeague_receiver.run()
        
        self.usersInfo_receiver.run(usersLeague_df)
        
        
# datareceiver = DataReceiver()
# datareceiver.run()