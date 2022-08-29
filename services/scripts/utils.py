"""
utils
"""
import json
#---------------------------------------------------------------------------------
# This file is part of Moove.
# __file__ : utils.py
# Copyright(c) Moove. All right reserved

#---------------------------------------------------------------------------------


import smtplib
from email.message import EmailMessage
import xlsxwriter
import scripts.config as cfg

class Utils():
    """
    utils
    """

    def write_data(self, geo_data, file_name):
        """
        Geodata format

         # geo_data = {
            #     "result": [{
            #             "count(T.id)": 259,
            #             "distance": "2.816644",
            #             "id": "b19475E",
            #             "license_plate": "JL-433-K",
            #             "rule_id": "apUro_0nXOUmLV4SVlzK8Xw",
            #             "start": "2022-08-19 15:36:11",
            #             "stop": "2022-08-19 15:41:53"
            #         },
            #         {
            #             "count(T.id)": 259,
            #             "distance": "22.428362",
            #             "id": "b194737",
            #             "license_plate": "JL-433-K",
            #             "rule_id": "apUro_0nXOUmLV4SVlzK8Xw",
            #             "start": "2022-08-19 15:10:08",
            #             "stop": "2022-08-19 15:33:05"
            #         }
            #     ]
            # }


        :return:
        """

        dict_res = {'status':'false', 'result':None}

        try:

            workbook = xlsxwriter.Workbook(file_name)
            worksheet = workbook.add_worksheet()

            # Start from the first cell.
            # Rows and columns are zero indexed.
            row = 0
            column = 0

            header = ["License Plate", "Trip Start Date", "Trip Stop Date", "Distance Driven",
                      "Driving Exception"]

            row = 0
            col = 0
            for each_headr in header:
                worksheet.write(row, col, each_headr)
                col += 1

            # geodata format should be dict

            # geo_data=json.loads(geo_data)
            for each_item in geo_data['result']:
                # write operation perform

                print(each_item)
                worksheet.write(row, column, each_item['license_plate'])
                worksheet.write(row, column + 1, each_item['start'])
                worksheet.write(row, column + 2, each_item['stop'])
                worksheet.write(row, column + 3, each_item['distance'])
                worksheet.write(row, column + 4, each_item['count(T.id)'])

                # incrementing the value of row by one
                # with each iterations.
                row += 1
            workbook.close()

            dict_res['status'] = 'true'
            dict_res['message'] = 'Success-writing file content'

        except Exception as err:
            dict_res['error'] = str(err)

        print(dict_res)
        return dict_res


    def send_mail_with_excel(self,recipient_email, subject, content, excel_file):
        """
        :param subject:
        :param content:
        :param excel_file:
        :return:
        """

        sender_email = cfg.SENDER_EMAIL
        app_password = cfg.APP_PASSWORD

        try:
            dict_res = {'result':None, 'status':'false'}

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg.set_content(content)

            with open(excel_file, 'rb') as f:
                file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excel_file)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)

                dict_res['result'] = 'mail sent'
                dict_res['status'] = 'true'

        except Exception as err:
            dict_res['error'] = str(err)

        return dict_res

# send_mail_with_excel("priyapwarrier@gmail.com", "Geodata-report", "PFA-GeoData", "Geodata.xlsx")