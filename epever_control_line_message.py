#epever_control_line_message.py
#epever control line message ver 1.0 Update: 29/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code get the result of epever control, send LINE message. 


import LINE_Messaging_API_setting
import epever_control_common
import epever_control_setting
import datetime
import sys

#Initialize
cls_epever_control_common_value = epever_control_common.epever_control_commonvalue()
dbPath = epever_control_setting.line_message_dbpath()

#LINE Messaging API
cls_Line_Messaging_API_setting = LINE_Messaging_API_setting.LINE_Messaging_API()

#database
cls_epever_control_db = epever_control_common.epever_control_db()

#Get unsend list
ret = cls_epever_control_db.read_line_message_unsend_to_on(dbPath, cls_epever_control_common_value.update_flg_linemsg_on)
if ret == cls_epever_control_common_value.lvNormal:
    unsend_list = cls_epever_control_db.linemsg_send_list
    print(unsend_list)
    dt_now = datetime.datetime.now()
    for unsend in unsend_list:

        print (unsend[0])
        print (unsend[1])
        print (unsend[2])
        print (unsend[3])
        print (unsend[4])
        ret = cls_Line_Messaging_API_setting.post_messages(unsend[1]  + '\r\n' + " request date : " + unsend[2])
        if ret == cls_epever_control_common_value.lvNormal:
            ret == cls_epever_control_db.update_line_message_unsent_to_sent(dbPath, dt_now.strftime('%Y/%m/%d %H:%M:%S'), unsend[4])
            #if ret == cls_epever_control_common_value.lvNormal:
            if ret == cls_epever_control_common_value.lvError:
                sys.exit(1)
elif ret == cls_epever_control_common_value.lvError:
    sys.exit(1)
