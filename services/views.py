from flask import Flask, request
from flask_restplus import Resource, Api
from scripts.main_services import MainService
# Flask app init
moove_app = Flask(__name__)

api = Api(moove_app, version="1.0", title="Moove services", description="Moove")

services_ns = api.namespaces('/api/v1/moove/',description= "Moove API")

class Trips(Resource):
    def get(self):
        """
        get trip details

        :return:
        """
        api_res= {"status":'false', 'result' : None}

        main_serv = MainService()

        return api_res
