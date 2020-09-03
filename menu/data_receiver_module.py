# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:49:15 2020

@author: 6794c
"""
import usersLeagueReceiver

# input your api key when you need

class DataReceiver:
    def __init__(self):
        self.API_KEY = None
        self.usersLeague_csv_name = "usersLeague.csv"
        
        self.usersLeague_receiver = usersLeagueReceiver.UsersLeague_LEAGUEV4(
            self.API_KEY, self.usersLeague_csv_name)
        
    def run(self):
        