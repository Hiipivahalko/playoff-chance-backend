from flask import jsonify
from types import MethodType

from flask_restful import Resource, request
import json
from random import randint

from .reg_model import REG_MODEL

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
'Seattle Kraken',\
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
'Seattle Kraken': '',\
'Vancouver Canucks': 'Vancouver_Canucks.svg',\
'Vegas Golden Knights': 'Vegas_Golden_Knights.svg.png',\
}


class CheckStatus(Resource):
    def get(self):
        return {"data": True}


class TeamNames(Resource):
    def get(self):
        return {'data': teams}

class Predict(Resource):
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

