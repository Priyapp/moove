"""
Script for all services
"""
import datetime

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : geodata.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------


import requests
import json
import logging
import scripts.db as Db
import datetime
from datetime import timedelta
logging.basicConfig(filename='moove.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
import mysql.connector

class GeoService():
    """

    """
    url = "https://my.geotab.com/apiv1"

    def get_vehicle(self):

        """
        to get vehicle  data
        :return: result from vehicle
        """
        dict_res = {"status":"false","result":None, 'message':'error while fetching geotab data'}
        list_req_data = []
        payload= {
            "method": "Get",
            "params": {
                "typeName": "Device",
                "credentials": {
                    "database": "moove",
                    "sessionId": "2nR_L-I6A8F0K5DVF8srFQ",
                    "userName": "moovechallengeuser@mooveconnected.com"
        }
    }
}
        try:

            # calling vehicle api
            res_vehicle = requests.post(url=GeoService.url, data=json.dumps(payload))

            if res_vehicle.status_code == 200:
                dict_res['result'] = res_vehicle.json()
                dict_res['message'] = "fetched geotab data successfully"
                dict_res['status'] = "true"

                # taking only required data for DB
                for each_data in res_vehicle.json()['result']:
                    each_veh_list = []
                    each_veh_list.append(each_data['id'])
                    each_veh_list.append(each_data['comment'])
                    each_veh_list.append(each_data['licensePlate'])

                    each_veh_tuple = tuple(each_veh_list)

                    list_req_data.append(each_veh_tuple)

                dict_res['req_list'] = list_req_data
        except Exception as err:
            dict_res['error'] = str(err)

        logging.info({"result- vehicle ": dict_res})
        return dict_res

    def get_trips(self):

        """
        to get services  data
        :return: result from services
        """
        dict_res = {"status": "false", "result": None, 'message': 'error while fetching geotab data'}
        list_req_data = []
        payload = {
                "method": "Get",
                "params": {
                    "typeName": "Trip",
                    "credentials": {
                        "database": "moove",
                        "sessionId": "2nR_L-I6A8F0K5DVF8srFQ",
                        "userName": "moovechallengeuser@mooveconnected.com"
                    },
                    "search":{
                        "fromDate":"2022-08-14T22:00:00.000Z",
                        "toDate": "2022-08-22T22:00:00.000Z"
                    }
                }
            }
        current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        payload['params']['search']['toDate']= current_time
        fromDate = (datetime.datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z") # 30 days back
        payload['params']['search']['fromDate'] = fromDate

        try:

            # calling trip API
            res_trips = requests.post(url=GeoService.url, data=json.dumps(payload))


            if res_trips.status_code == 200:
                dict_res['result'] = res_trips.json()
                dict_res['message'] = "Fetched geotab data successfully"
                dict_res['status'] = "true"

                # taking only required data for DB
                for each_data in res_trips.json()['result']:

                    each_trip_list = []
                    each_trip_list.append(each_data['id'])
                    each_trip_list.append(each_data['device']['id'])
                    each_trip_list.append(each_data['start'])
                    each_trip_list.append(each_data['stop'])
                    each_trip_list.append(each_data['distance'])
                    each_trip_list.append(each_data['maximumSpeed'])
                    each_trip_list.append(each_data['driver']['id'])
                    each_trip_tuple = tuple(each_trip_list)

                    list_req_data.append(each_trip_tuple)

                dict_res['req_list'] = list_req_data

        except Exception as err:
            dict_res['error'] = str(err)

        logging.info({"result- trips ": dict_res})
        return dict_res

    def get_driving_exception(self):

        """
        to get services  data
        :return: result from services
        """
        dict_res = {"status": "false", "result": None, 'message': 'error while fetching geotab data'}
        list_req_data = []
        payload = {
            "method": "Get",
            "params": {
                "typeName": "ExceptionEvent",
                "credentials": {
                    "database": "moove",
                    "sessionId": "2nR_L-I6A8F0K5DVF8srFQ",
                    "userName": "moovechallengeuser@mooveconnected.com"
                },
                "search":{
                    "fromDate":"2022-08-14T22:00:00.000Z",
                    "toDate": "2022-09-22T22:00:00.000Z"
                }
            }
        }

        try:


            res_excpetions = requests.post(url=GeoService.url, data=json.dumps(payload))

            if res_excpetions.status_code == 200:
                dict_res['result'] = res_excpetions.json()
                dict_res['message'] = "Fetched geotab data successfully"
                dict_res['status'] = "true"

                # taking only required data for DB
                for each_data in res_excpetions.json()['result']:
                    each_except_list = []
                    each_except_list.append(each_data['id'])
                    each_except_list.append(each_data['rule']['id'])
                    each_except_list.append(each_data['device']['id'])
                    each_except_list.append(each_data['activeFrom'])
                    each_except_list.append(each_data['activeTo'])
                    each_except_list.append(each_data['duration'])
                    each_trip_tuple = tuple(each_except_list)

                    list_req_data.append(each_trip_tuple)

                dict_res['req_list'] = list_req_data

        except Exception as err:
            dict_res['error'] = str(err)

        logging.info({"result- exceptions": dict_res})
        return dict_res

    def insert_data_todb(self, data, type):

        """
        push data
        :param data:
        :return:
        """
        dict_res= {"result":None, "status":"false"}

        try:
            # mydb = mysql.connector.connect(
            # host = "localhost",
            # user = "user",
            # password = "user",
            # database = "moove"
            # )

            db_obj = Db.DbConnect()
            cursor_obj = db_obj.get_conn()
            if not cursor_obj.get('error'):

                if type == "vehicle":
                    sql ="INSERT IGNORE INTO vehicle (geotab_id,name,license_plate) VALUES (%s, %s, %s)"
                elif type == "services":
                    sql = "INSERT IGNORE INTO trips (id,geotab_id,start, stop, distance, maxspeed,driver_id) VALUES (%s, %s, %s,%s, %s, %s,%s)"
                elif type == "exceptions":
                    sql = "INSERT IGNORE INTO driving_exceptions (id,rule_id,geotab_id,active_from, active_to, duration) VALUES (%s, %s, %s,%s, %s,%s)"

                cursor_obj['cursor'].executemany(sql, data['req_list'])
                cursor_obj['mydb'].commit()
                dict_res['status'] = "true"
                dict_res['result'] = "{} inserted".format(cursor_obj['cursor'].rowcount)

        except Exception as err:
            print(err)
            dict_res['error'] = str(err)

        return dict_res

#
# m_serv = GeoService()
# res=m_serv.get_vehicle()
# print(m_serv.insert_data_todb(res,"vehicle"))
# res_trip=m_serv.get_trips()
# print(m_serv.insert_data_todb(res_trip,"services"))
# res_trip=m_serv.get_driving_exception()
# print(m_serv.insert_data_todb(res_trip,"exceptions"))




