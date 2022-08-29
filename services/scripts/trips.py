"""
Script for trips
"""

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : trips.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------

import requests
import logging
import json
logging.basicConfig(filename='moove.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
from scripts.db import DbCOnnect

class Trips():
    """
    trips related
    """
    url = "https://my.geotab.com/apiv1"
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
                "search": {
                    "fromDate": "2022-08-14T22:00:00.000Z",
                    "toDate": "2022-08-22T22:00:00.000Z"
                }
            }
        }

        try:

            # calling trip API
            res_trips = requests.post(url=Trips.url, data=json.dumps(payload))

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

        logging.info({"result- services ": dict_res})
        return dict_res

    def filter_trips(self):
        """

        :return:
        """
        try:
            dict_res= {'status':'false', 'result':None}

            db_obj = DbCOnnect()
            cursor_obj = db_obj.get_conn()

            if not cursor_obj.get('error'):
                sql = "SELECT * FROM moove.trips WHERE DATE(start) >= DATE(NOW()) - INTERVAL 30 DAY"
                cursor_obj['cursor'].execute(sql)
                trip_res = cursor_obj['cursor'].fetchall()


                dict_res['result'] = trip_res
                dict_res['status'] ="true"

        except Exception as err:
            dict_res['error'] = str(err)

        return dict_res
trip_obj = Trips()
from flask import jsonify

# print(json.dumps(trip_obj.filter_trips()), default=json_util.default)
print(json.dumps(trip_obj.filter_trips(), indent=6, sort_keys=True, default=str))