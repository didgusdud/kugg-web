# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:47:28 2020

@author: 6794c
"""
import pickle
import numpy as np

class ObjectAnalysis:
    def __init__(self, first_object_model=None, object_kills_model=None, object_killsAnd_first_model=None):
        # ObjectAnalysis.py in kugg-web/menu/
        self.model_dic_path = "./static/analysis_models/"
        self.first_object_model=None
        self.object_kills_model=None
        self.object_killsAnd_first_model=None
        self.update_model("first_object_model")
        self.update_model("object_kills_model")
        self.update_model("object_killsAnd_first_model")
    
    # parameter = pickle file
    def update_model(self, object_model):
        if object_model == "first_object_model":
            model_path = self.model_dic_path+"dt_model1.pkl"
            with open(model_path, 'rb') as file:
                self.first_object_model = pickle.load(file)
                return 1
            
        elif object_model == "object_kills_model":
            model_path = self.model_dic_path+"dt_model2.pkl"
            with open(model_path, 'rb') as file:
                self.object_kills_model = pickle.load(file)
                return 2
                
        elif object_model == "object_killsAnd_first_model":
            model_path = self.model_dic_path+"dt_model3.pkl"
            with open(model_path, 'rb') as file:
                self.object_killsAnd_first_model = pickle.load(file)
                return 3
        else:
            print("wrong input")
            return -1
    
    def first_object_predict(self, fdragon, fharry, fblood, ftower,
                             fbaron, finhib):
        predict_array = self.first_object_model.predict_proba(
            np.array[fblood, finhib, ftower, fharry, fdragon, fbaron].reshape(1, -1))
        
        # ex. 0.641095145921092....
        return predict_array[0][1]
    
    def object_kills_predict(self, dragonkills, baronkills, inhibkills,
                             harrykills, towerkills):
        predict_array = self.object_kills_model.predict_proba(
            np.array[harrykills, inhibkills, towerkills, baronkills,
                     dragonkills].reshape(1, -1))
        
        # ex. 0.124412512451231....
        return predict_array[0][1]
    
    def object_killsAnd_first_model(self, fdragon, fharry, fblood, ftower, fbaron, 
                                    finhib, dragonkills, baronkills, inhibkills,
                                    harrykills, towerkills):
        predict_array = predict_array = self.object_kills_model.predict_proba(
            np.array[harrykills, fharry, inhibkills, fblood, towerkills, dragonkills, baronkills,
                     finhib, fdragon, fbaron, ftower].reshape(1, -1))
        
        return predict_array[0][1]
