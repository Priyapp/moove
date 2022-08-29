"""
Routing file
"""

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : views.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------


import logging
import requests
import json
import requests
from flask import Flask, request
from flask_restplus import Resource, Api
from scripts.geodata import GeoService
from flask_cors import CORS
from scripts.db_services import  DbServices
from scripts.utils import Utils
import datetime

# Flask app init
moove_app = Flask(__name__)

CORS_RS= CORS(moove_app, resources={r"/api/v1/*": {"origins":"*"}})

api = Api(moove_app, version="1.0", title="Moove services", description="Moove")

services_ns = api.namespace('api/v1/moove',description= "Moove API")


def collect_data():
    """
    push all data to DB - vehicle, trip, excpetion from geo tab

    :return:
    """

    flag_vehicle  = "false"
    flag_trips = "false"
    flag_exceptions  = "false"
    flag = "false"

    try:
        #getting vehicle, trip & excpetion data
        geo_service = GeoService()
        db_services = DbServices()

        res = geo_service.get_vehicle()
        vehice_res = db_services.insert_data_todb(res, "vehicle")
        if not vehice_res.get('error'):
            flag_vehicle = "true"

        res_trip = geo_service.get_trips()
        trips_res=db_services.insert_data_todb(res_trip, "trips")
        print(trips_res)
        if not trips_res.get('error'):
            flag_trips = "true"

        res_trip = geo_service.get_driving_exception()
        exceptions_res = db_services.insert_data_todb(res_trip, "exceptions")
        print(exceptions_res)
        if not exceptions_res.get('error'):
            flag_exceptions = "true"

        #only if all data gets added into the db, we can query further
        if flag_vehicle == "true" and flag_trips == "true" and flag_exceptions == "true":
            flag= "true"

    except Exception as err:
        print(err)
        logging.info({"error" : str(err)})
        flag = "error"
    print(flag)
    return flag



@services_ns.route('/trips')
@services_ns.doc(responses = {200:'success', 400: 'missing parameters', 500:'Internal server error'})
class Trips(Resource):
    def get(self):
        """
        get trip details

        :return:
        """
        api_res= {"status":'false', 'result' : None}

        # getting all vehicle, trips & exceptions
        try:

            flag = collect_data()
            if flag == "true":
                db_services = DbServices()
                trips_res = db_services.filter_trips()
                api_res['result'] = trips_res
                api_res['status'] = 'true'

        except Exception as err:
            api_res['error'] = str(err)

        logging.info({"trip-res": api_res})
        return api_res

@services_ns.route('/report')
@services_ns.param('endDate','2022-08-19T22:00:00.000')
@services_ns.param('startDate','2022-08-14T22:00:00.000')
@services_ns.param('reciever','priyapwarrier@gmail.com')
@services_ns.doc(responses = {200:'success', 400: 'missing parameters', 500:'Internal server error'})
class Report(Resource):
    def get(self):
        """
        get report

        :return:
        """
        api_res= {"status":'false', 'result' : None}

        # getting all vehicle, trips & exceptions
        try:
            start_date = request.args.get('startDate')
            stop_date = request.args.get('endDate')
            receiver = request.args.get('reciever')

            util = Utils()
            flag = collect_data() # collect all data from geotab

            if flag == "true":
                db_services = DbServices() # generating report
                trip_res = db_services.get_trip_report_data(start_date, stop_date)
                trip_res = json.loads(trip_res)

                if not trip_res.get('error'):
                    file_name = 'Geodata_{}.xlsx'.format(datetime.datetime.now())
                    excl_write_res = util.write_data(trip_res, file_name) # writing to excel file

                    if not excl_write_res.get('error'):
                        # send mail with attachement
                        send_mail_res = util.send_mail_with_excel(receiver, "Geodata-report", "PFA-GeoData", file_name)

                        api_res['email_res'] = send_mail_res
                        # api_res['result'] = trip_res
                        api_res['status'] = 'true'

        except Exception as err:
            api_res['error'] = str(err)

        logging.info({"trip-res": api_res})
        return api_res




@services_ns.route('/exceptions')
class Exceptions(Resource):
    def get(self):
        """
        get Driving exceptions

        :return:
        """
        api_res= {"status":'false', 'result' : None}
        # getting all vehicle, trips & exceptions
        try:

            flag = collect_data()
            if flag == "true":
                db_services = DbServices()
                exception_res = db_services.filter_exceptions()
                api_res['result'] = exception_res
                api_res['status'] = 'true'
        except Exception as err:
            api_res['error'] = str(err)

        # logging.info({"trip-res": api_res})
        return api_res
