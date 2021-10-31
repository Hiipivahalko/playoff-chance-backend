
#from application import app

from flask import Flask

from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from application.router import TeamNames, CheckStatus, Predict, PredictSimulate
from application.reg_model import build_and_set_model

app = Flask(__name__)
CORS(app)
api = Api(app)

build_and_set_model()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(TeamNames, '/api/teams')
api.add_resource(CheckStatus, '/api/status')
api.add_resource(Predict, '/api/predict')
api.add_resource(PredictSimulate, '/api/predictSimulate')