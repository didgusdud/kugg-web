# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 14:38:24 2020

@author: 6794c
"""
import sqlite3
import copy
import numpy as np

class DBController:
    def __init__(self):
        self.conn, self.cur = self.db_connect()       
        
    def db_connect(self):
        conn = sqlite3.connect("../lolraw.db")
        cur = conn.cursor()
        
        return conn, cur
    
    # usersLeagueDB type = all string
    def update_usersLeague(self, usersLeague_df):
        # tier, leagueId, queue, name, summonerId, summonerName, leaguePoints,
        #       rank, wins, losses, veteran, inactive, freshBlood, hotStreak
        insert_usersLeague_sql = "INSERT into usersLeague \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        update_usersLeague_sql = "UPDATE usersLeague \
            SET tier=?, leagueId=?, queue=?, name=?, summonerName=?,\
                leaguePoints=?, rank=?, wins=?, losses=?, veteran=?, inactive=?,\
                freshBlood=?, hotStreak=?\
            WHERE summonerId=?"
        delete_usersLeague_sql = "DELETE FROM usersLeague\
            WHERE summonerId=?"
            
        self.cur.execute("SELECT * FROM usersLeague")
        rows = self.cur.fetchall()
        request_usersLeauge_summonerId = usersLeague_df["summonerId"].values
        residual_summonerId = copy.deepcopy(request_usersLeauge_summonerId)
        
        for row in rows:
            # DB's summonerId in request summonerId
            if row[4] in request_usersLeauge_summonerId:
                # DB'S leaguepoints not same request leaguePoints
                residual_summonerId = np.delete(residual_summonerId, np.argwhere(residual_summonerId==row[4]))
                if int(row[6]) != int(usersLeague_df[usersLeague_df["summonerId"]==row[4]]["leaguePoints"].values[0]):
                    # print(row[5], row[6], usersLeague_df[usersLeague_df["summonerId"]==row[4]]["leaguePoints"].values[0])
                    self.cur.execute(update_usersLeague_sql,
                                usersLeague_df[usersLeague_df["summonerId"]==row[4]].drop("summonerId", axis=1).astype(str).values[0].tolist()+[row[4]])
            else:
                # print(row[5], row[6])
                self.cur.execute(delete_usersLeague_sql, (row[4],))
                
        # insert data which not inside DB
        for summonerId in residual_summonerId:
            self.cur.execute(insert_usersLeague_sql,
                             usersLeague_df[usersLeague_df["summonerId"]==summonerId].astype(str).values[0])
            
        self.conn.commit()
        # self.conn.close()
        
        # extract summonerId from usersLeague for request usersInfo
        def from_usersLeague_for_usersInfo_summonerId(self, usersLeague_df):
            delete_usersInfo_sql = "DELETE FROM usersInfo WHERE summonerId=?"
            self.cur.execute("SELECT * FROM usersInfo")
            
            request_usersLeague_summonerId = usersLeague_df["summonerId"].values
            residual_summonerId = copy.deepcopy(request_usersLeague_summonerId)
                 
            for row in self.cur.fetchall():
                residual_summonerId = np.delete(residual_summonerId, np.argwhere(residual_summonerId==row[0]))
                if row[0] in request_usersLeague_summonerId:
                    pass
                # is in DB, but not in latest usersLeague --> need delete
                else:
                    self.cur.execute(delete_usersInfo_sql, (row[0], ))
                
            self.conn.commit()
            
            return residual_summonerId
        
        
        """
        In usersInfo part, did not implement update sql because of too much request
        """
        def update_usersInfo(self, usersInfo_df):
            # id, accountId, puuid, name, profileIconId, revesionDate, summonerLevel
            insert_usersInfo_sql = "INSERT INTO usersInfo VALUES (?, ?, ?, ?, ?, ?, ?)"
                
            for row in usersInfo_df.values:
                self.cur.execute(insert_usersInfo_sql, row.astype(str).tolist())
                
            self.conn.commit()