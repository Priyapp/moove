"""
Script for trips
"""

#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : trips.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------

import requests
import json
import logging
logging.basicConfig(filename='moove.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
import mysql.connector

class Trips():
    """
    trips related
    """

    def filter_trips(self):
        """

        :return:
        """

