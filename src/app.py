from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from router import TeamNames, CheckStatus, Predict

app = Flask(__name__)
CORS(app)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(TeamNames, '/api/teams')
api.add_resource(CheckStatus, '/api/status')
api.add_resource(Predict, '/api/predict')


if __name__ == '__main__':
    app.run(debug=True)