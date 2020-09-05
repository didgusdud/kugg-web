# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:49:15 2020

@author: 6794c
"""
import usersLeagueReceiver
import usersInfoReceiver
import usersMatchlistreceiver

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
        self.usersMatchlist_receiver = usersMatchlistreceiver.UsersMatchlistReceiver(
            self.API_KEY, self.usersMatchlist_csv_name)
        
    def run(self):
        usersLeague_df = self.usersLeague_receiver.run()
        usersInfo_df = self.usersInfo_receiver.run(usersLeague_df)
        usersMatchlist = self.usersMatchlist_receiver.run(usersInfo_df)
        
        
# datareceiver = DataReceiver()
# datareceiver.run()