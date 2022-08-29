"""
Db services
"""

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : db_services.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------


import json
import logging
from scripts.db import DbCOnnect

class DbServices():
    """
    all db related serices: insertion & queries
    """

    def insert_data_todb(self, data, type):

        """
        push data
        :param data:
        :return:
        """
        dict_res= {"result" :None, "status" :"false"}

        try:
            db_obj = DbCOnnect()
            cursor_obj = db_obj.get_conn()

            if not cursor_obj.get('error'):

                if type == "vehicle":
                    sql ="INSERT IGNORE INTO vehicle (geotab_id,name,license_plate) VALUES (%s, %s, %s)"
                elif type == "trips":
                    sql = "INSERT IGNORE INTO trips (id,geotab_id,start, stop, distance, maxspeed,driver_id) VALUES (%s, %s, %s,%s, %s, %s,%s)"
                elif type == "exceptions":
                    sql = "INSERT IGNORE INTO driving_exceptions (id,rule_id,geotab_id_exptn,active_from, active_to, duration) VALUES (%s, %s, %s,%s, %s,%s)"

                cursor_obj['cursor'].executemany(sql, data['req_list'])
                cursor_obj['mydb'].commit()
                dict_res['status'] = "true"
                dict_res['result'] = "{} inserted".format(cursor_obj['cursor'].rowcount)

        except Exception as err:
            dict_res['error'] = str(err)

        return dict_res

    def filter_trips(self):
        """
        trip - last 30 days
        :return:
        """
        try:
            dict_res = {'status': 'false', 'result': None}

            db_obj = DbCOnnect()
            cursor_obj = db_obj.get_conn()

            if not cursor_obj.get('error'):
                sql = "SELECT * FROM moove.trips WHERE DATE(start) >= DATE(NOW()) - INTERVAL 30 DAY"
                cursor_obj['cursor'].execute(sql)
                trip_res = cursor_obj['cursor'].fetchall()

                dict_res['result'] = trip_res
                dict_res['status'] = "true"

        except Exception as err:
            dict_res['error'] = str(err)

        return json.dumps(dict_res, sort_keys=True, indent=6, default=str)

    def filter_exceptions(self):
        """
        to get last 30 days excpetions
        :return:
        """
        try:
            dict_res = {'status': 'false', 'result': None}

            db_obj = DbCOnnect()
            cursor_obj = db_obj.get_conn()

            if not cursor_obj.get('error'):
                sql = "SELECT V.license_plate,E.id,E.rule_id,T.start,T.stop,T.geotab_id FROM moove.driving_exceptions E INNER JOIN moove.trips T ON T.geotab_id=E.geotab_id_exptn INNER JOIN moove.vehicle V ON V.geotab_id=T.geotab_id where DATE(T.start) >= DATE(NOW()) - INTERVAL 30 DAY"

                cursor_obj['cursor'].execute(sql)
                trip_res = cursor_obj['cursor'].fetchall()

                dict_res['result'] = trip_res
                dict_res['status'] = "true"

        except Exception as err:
            dict_res['error'] = str(err)

        return json.dumps(dict_res,sort_keys=True, indent=6,default=str)

    def get_trip_report_data(self, start_date, end_date):
        """
        it gets the data required for report
        :return:
        """

        try:
            dict_res = {'status': 'false', 'result': None}

            rule_list = ['apUro_0nXOUmLV4SVlzK8Xw','abHSbCv2PKUWKSSGJMoiBnQ']

            db_obj = DbCOnnect()
            cursor_obj = db_obj.get_conn()
            all_data_list = []

            print(start_date, end_date)

            if not cursor_obj.get('error'):
                for each_rule in rule_list:
                    print(each_rule)
                    sql = "select V.license_plate,V.geotab_id,T.id,T.start,T.stop,T.distance,  E.rule_id, count(T.id) from moove.driving_exceptions E INNER JOIN moove.trips T ON  E.geotab_id_exptn=T.geotab_id INNER JOIN moove.vehicle V ON T.geotab_id=V.geotab_id where E.active_from between '"+ start_date+"' AND '"+end_date+ "' and E.rule_id='"+each_rule+"' group by T.id,E.rule_id"

                    print(sql)
                    cursor_obj['cursor'].execute(sql)
                    trip_res = cursor_obj['cursor'].fetchall()

                    dict_res['status'] = "true"

                    for each_data in trip_res:
                        all_data_list.append(each_data)

            dict_res['result'] = all_data_list
        except Exception as err:
            dict_res['error'] = str(err)

        return json.dumps(dict_res,sort_keys=True, indent=6,default=str)
