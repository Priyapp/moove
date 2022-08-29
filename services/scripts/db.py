"""
Script for db
"""

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : db.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------


import logging
logging.basicConfig(filename='moove.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

import mysql.connector
import scripts.config as cfg


class DbCOnnect():
    """
    Db connection
    """

    def __init__(self):
        """
        init
        """
        self.db_name =cfg.db_name

        self.username = cfg.username

        self.password=cfg.password

        self.host  = cfg.host

    def get_conn(self):

        """
        get connection
        :return: conn obj
        """

        result= {'status':'false'}
        try:

            mydb = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name
            )

            mycursor = mydb.cursor(dictionary=True)

            result['cursor'] = mycursor
            result['mydb'] = mydb
        except Exception as db_err:
            result['error'] = str(db_err)


        logging.info({"db_res": result})
        return result