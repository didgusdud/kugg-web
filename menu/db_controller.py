# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 14:38:24 2020

@author: 6794c
"""
import pymysql
import copy
import numpy as np
import pandas as pd

class DBController:
    def __init__(self):
        self.conn, self.cur = self.db_connect()       
        
    def db_connect(self):
        conn = pymysql.connect(host="localhost", user='loladmin', password='loladmin', db='lolanlysis')
        cur = conn.cursor()
        
        return conn, cur
    
    # usersLeagueDB type = all string
    def update_usersLeague(self, usersLeague_df):
        # tier, leagueId, queue, name, summonerId, summonerName, leaguePoints,
        #       rank, wins, losses, veteran, inactive, freshBlood, hotStreak
        insert_usersLeague_sql = "INSERT into usersleague \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        update_usersLeague_sql = "UPDATE usersleague \
            SET tier=%s, leagueId=%s, queue=%s, lname=%s, summonerName=%s, leaguePoints=%s, srank=%s, wins=%s, losses=%s, veteran=%s, sinactive=%s, freshBlood=%s, hotStreak=%s \
                WHERE summonerId=%s;"
        delete_usersLeague_sql = "DELETE FROM usersleague\
            WHERE summonerId=%s"
            
        self.cur.execute("SELECT * FROM usersleague")
        rows = self.cur.fetchall()
        request_usersLeauge_summonerId = usersLeague_df["summonerId"].values
        residual_summonerId = copy.deepcopy(request_usersLeauge_summonerId)
        
        for row in rows:
            # DB's summonerId in request summonerId
            if row[4] in request_usersLeauge_summonerId:
                # DB'S leaguepoints not same request leaguePoints
                residual_summonerId = np.delete(residual_summonerId, np.argwhere(residual_summonerId==row[4]))
                # print("0", row[6], int(usersLeague_df[usersLeague_df["summonerId"]==row[4]]["leaguePoints"].values[0]))
                if int(row[6]) != int(usersLeague_df[usersLeague_df["summonerId"]==row[4]]["leaguePoints"].values[0]):
                    
                    update_row = usersLeague_df[usersLeague_df["summonerId"]==row[4]].values[0].tolist()
                    update_row.append(row[4])
                    del update_row[4]

                    self.cur.execute(update_usersLeague_sql, update_row)
            else:
                # print(row[5], row[6])
                self.cur.execute(delete_usersLeague_sql, (row[4],))
        
        self.conn.commit()

        print("usersleague residual summerlength: ", len(residual_summonerId))

        # insert data which not inside DB
        for summonerId in residual_summonerId:
            self.cur.execute(insert_usersLeague_sql,
                             tuple(usersLeague_df[usersLeague_df["summonerId"]==summonerId].values[0]))
            
        self.conn.commit()
        # self.conn.close()
        
        return 0
        
        # extract summonerId from usersLeague for request usersInfo
    def from_usersLeague_for_usersInfo_summonerId(self, usersLeague_df):
        delete_usersInfo_sql = "DELETE FROM usersInfo WHERE summonerId=%s"
        select_usersInfo_sql = "SELECT * FROM usersInfo"
        self.cur.execute(select_usersInfo_sql)
        
        request_usersLeague_summonerId = usersLeague_df["summonerId"].values
        residual_summonerId = copy.deepcopy(request_usersLeague_summonerId)
             
        for row in self.cur.fetchall():
            residual_summonerId = np.delete(residual_summonerId, np.argwhere(residual_summonerId==row[0]))
            if row[0] not in request_usersLeague_summonerId:
            # is in DB, but not in latest usersLeague --> need delete
                self.cur.execute(delete_usersInfo_sql, row[0])
            
        self.conn.commit()
        
        return residual_summonerId
        
        
    """
    In usersInfo part, did not implement update sql because of too much requestt
    """
    def update_usersInfo(self, usersInfo_df):
        # id, accountId, puuid, name, profileIconId, revesionDate, summonerLevel
        insert_usersInfo_sql = "INSERT INTO usersinfo (summonerId, accountId, puuId, sname, profileIconId, \
            summonerLevel) VALUES (%s, %s, %s, %s, %s, %s)"

        for row in usersInfo_df.values:
            insert_row = row.tolist()
            del insert_row[-2]
            self.cur.execute(insert_usersInfo_sql, insert_row)
            
        self.conn.commit()
        
    def load_usersInfo_fromDB(self):
        select_usersInfo_sql = "SELECT accountId, revisionDate FROM usersInfo"
        
        usersInfo_df = pd.read_sql_query(select_usersInfo_sql, self.conn)
        
        
        return usersInfo_df
        
    # only given new matchlist.
    # insert new matchlist data to matchlistDB and update and update usersInfo revisionDate column
    def update_usersMatchlist(self, usersMatchlist_df):
        # index, platformId, gameId, champion, queue, season, (begin)timestamp, role, lane, accountId
        insert_usersMatchlist_sql = "INSERT INTO usersInfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        update_usersInfo_sql = "UPDATE usersInfo SET revisionDate=? WHERE accountId=?"
        
        before_account = "iniail_account"  # row[-1]
        recent_timestamp = 100 # row[5]
        for row in usersMatchlist_df.values:
            self.cur.execute(insert_usersMatchlist_sql, row.astype(str).tolist())
            if row[-1] != before_account:
                before_account = row[-1]
                recent_timestamp = row[5]
                
                # update usersInfo revisionDate 
                self.cur.execute(update_usersInfo_sql, [recent_timestamp, before_account])
            
        self.conn.commit()
        
    """matchInfo, matchTimeline method only excute insert function"""
    def update_matchInfo(self, matchInfo_df):
        insert_matchInfo_sql = "INSERT INTO matchInfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
        for row in matchInfo_df.values:
            try:
                self.cur.execute(insert_matchInfo_sql, row)
            except IntegrityError:
                pass
            
    def update_matchTimeline(self, matchTimeline_df):
        insert_matchTimeline_sql = "INSERT INTO matchTimeline VALUES (?, ?, ?)"
        
        for row in matchTimeline_df:
            try:
                self.cur.execute(insert_matchTimeline_sql, row)
            except IntegrityError:
                pass
    
    def controller_close(self):
        self.conn.close()