from flask import jsonify
from types import MethodType

from flask_restful import Resource, request
import json
from random import randint
import pandas as pd
import numpy as np




teams = ['Carolina Hurricanes',\
'Columbus Blue Jackets',\
'New Jersey Devils',\
'New York Islanders',\
'New York Rangers',\
'Philadelphia Flyers',\
'Pittsburgh Penguins',\
'Washington Capitals',\
'Boston Bruins',\
'Buffalo Sabres',\
'Detroit Red Wings',\
'Florida Panthers',\
'Montreal Canadiens',\
'Ottawa Senators',\
'Tampa Bay Lightning',\
'Toronto Maple Leafs',\
'Arizona Coyotes',\
'Chicago Blackhawks',\
'Colorado Avalanche',\
'Dallas Stars',\
"Minnesota Wild",\
'Nashville Predators',\
'St. Louis Blues',\
'Winnipeg Jets',\
'Anaheim Ducks',\
'Calgary Flames',\
'Edmonton Oilers',\
'Los Angeles Kings',\
'San Jose Sharks',\
'Vancouver Canucks',\
'Vegas Golden Knights',\
]

teams.sort()

teams_logo = {'Carolina Hurricanes': 'carolina.png',\
'Columbus Blue Jackets': 'Columbus_Blue_Jackets.svg.png',\
'New Jersey Devils': 'New_Jersey_Devils.svg.png',\
'New York Islanders': 'New_York_Islanders.svg.png',\
'New York Rangers': 'New_York_Rangers.svg.png',\
'Philadelphia Flyers': 'Philadelphia_Flyers_logo.svg',\
'Pittsburgh Penguins': 'Philadelphia_Flyers_logo.svg',\
'Washington Capitals': 'Washington_Capitals.svg',\
'Boston Bruins': 'Boston_Bruins.svg.png',\
'Buffalo Sabres': 'Buffalo_Sabres.svg.png',\
'Detroit Red Wings': 'Detroit_Red_Wings.svg',\
'Florida Panthers': 'Florida_Panthers.svg.png',\
'Montreal Canadiens': 'Montreal_Canadiens.svg.png',\
'Ottawa Senators': 'Ottawa_Senators.svg',\
'Tampa Bay Lightning': 'Tampa_Bay_Lightning.svg',\
'Toronto Maple Leafs': 'Toronto_Maple_Leafs.svg',\
'Arizona Coyotes': 'Arizona_Coyotes.svg.png',\
'Chicago Blackhawks': 'Chicago_Blackhawksin.svg',\
'Colorado Avalanche': 'Colorado_Avalanche.svg',\
'Dallas Stars': 'Dallas_Stars.svg',\
"Minnesota Wild": 'Minnesota_Wild.svg',\
'Nashville Predators': 'Nashville_Predators.svg.png',\
'St. Louis Blues': 'St_Louis_Blues.svg.png',\
'Winnipeg Jets': 'Winnipeg_Jets.svg',\
'Anaheim Ducks': 'Anaheim.svg',\
'Calgary Flames': 'Calgary_Flames.svg.png',\
'Edmonton Oilers': 'Edmonton_Oilers.svg',\
'Los Angeles Kings': 'LA_Kings.svg',\
'San Jose Sharks': 'San_Jose_Sharks.svg.png',\
'Vancouver Canucks': 'Vancouver_Canucks.svg',\
'Vegas Golden Knights': 'Vegas_Golden_Knights.svg.png',\
}

cols = ['PIM', 'Forward', 'Defense', 'goalie_performance',\
       'star_player', 'GF/GP', 'GA/GP', 'PP%', 'PK%', 'Net PP%', 'Net PK%',\
       'Shots/GP', 'SA/GP', 'FOW%']

predict_conversion = {
    0: 'NO',
    1: 'YES',
    2: 'MAYBE'
}


class CheckStatus(Resource):
    def get(self):
        return {"data": True}


class TeamNames(Resource):
    def get(self):
        return {'data': teams}

class Predict(Resource):
    
    def post(self):
        from .reg_model import REG_MODEL
        next_val = randint(0,2)
        req_data = request.get_json(force=True)
        #print(req_data)
        #print(req_data['team'])
        data = np.array([[req_data['pim'],req_data['f_p'], req_data['d_p'], req_data['g_p'], req_data['start_p'], req_data['gf_gp'],\
            req_data['ga_gp'], req_data['pp'], req_data['pk'], req_data['net_pp'], req_data['net_pk'], req_data['shots_gp'],\
            req_data['sa_gp'], req_data['fow']] ])
        df = pd.DataFrame(data=data, columns=cols)
        #print(df)
        pred = REG_MODEL.predict(df)
        print(pred)
        vals = ['YES', 'NO', 'MAYBE']
        result = {'data' : predict_conversion[pred[0]]}
        #print(result)
        return result, 200
        #return jsonify(result= vals[next_val])

class PredictSimulate(Resource):
    def post(self):
        next_val = randint(0,2)
        req_data = request.get_json(force=True)
        #print(req_data)
        #print(req_data['team'])
        
        vals = ['YES', 'NO', 'MAYBE']
        result = {'data' : vals[next_val]}
        #print(result)
        return result, 200
        #return jsonify(result= vals[next_val])

