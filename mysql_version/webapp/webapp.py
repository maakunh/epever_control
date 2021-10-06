#webapp.py
from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask.templating import DispatchingJinjaLoader
from flask.wrappers import Response


from modules import webapp_setting
from modules import webapp_common

import datetime
from dateutil.relativedelta import relativedelta #for calc month+/-
from decimal import Decimal, getcontext, ROUND_HALF_UP
c = getcontext()
c.rounding = ROUND_HALF_UP

cls_db = webapp_common.webapp_db()
cls_cmn = webapp_common.webapp_commonvalue()
cls_validation = webapp_common.webapp_validation()
cls_tool = webapp_common.webapp_tool()

#generate flask object
app = Flask(__name__)

#root
@app.route("/")
def dashboard():
    msg = ""
    flg = list()
    dt_now = datetime.datetime.now()
    #str_dt_now = dt_now.strftime('%Y-%m-%d')
    str_dt_now_key = dt_now.strftime('%Y/%m/%d')
    md = list()
    ikwh = list()
    okwh = list()
    mm = list()
    ikwhm = list()
    okwhm = list()

    #read current data
    ret = cls_db.read_record_simple_key('ALL', str_dt_now_key)
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
        print(read_db_list[0])
        lastupdate = read_db_list[0][0]
        input_voltage = read_db_list[0][1]
        input_current = read_db_list[0][2]
        input_power = float(input_voltage) * float(input_current)
        d = Decimal(input_power)
        input_power = d.quantize(Decimal('1e-2'))

        if input_power > webapp_setting.ip_err_upper():
            flg.append(cls_cmn.lvError)
        elif input_power < webapp_setting.ip_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)   #input power

        if float(input_voltage) > webapp_setting.iv_err_upper():
            flg.append(cls_cmn.lvError)
        elif float(input_voltage) < webapp_setting.iv_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)   #input voltage

        if float(input_current) > webapp_setting.ic_err_upper():
            flg.append(cls_cmn.lvError)
        elif float(input_current) < webapp_setting.ic_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)   #input current

        output_voltage = read_db_list[0][3]
        output_current = read_db_list[0][4]
        output_power = float(output_voltage) * float(output_current)
        d = Decimal(output_power)
        output_power = d.quantize(Decimal('1e-2'))

        if output_power > webapp_setting.op_err_upper():
            flg.append(cls_cmn.lvError)
        elif output_power < webapp_setting.op_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)  # output power

        if float(output_voltage) > webapp_setting.ov_err_upper():
            flg.append(cls_cmn.lvError)
        elif float(output_voltage) < webapp_setting.ov_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)  # output voltage

        if float(output_current) > webapp_setting.oc_err_upper():
            flg.append(cls_cmn.lvError)
        elif float(output_current) < webapp_setting.oc_err_under():
            flg.append(cls_cmn.lvAlert)
        else:
            flg.append(cls_cmn.lvNormal)  # output current

    #read daily power
    #this year
    i = 0
    dt_now_i = dt_now
    for i in range(7):
        dt_now_i = dt_now + datetime.timedelta(days=-i)
        sdate = dt_now_i.strftime('%Y%m%d')
        md.append(dt_now_i.strftime('%m/%d'))

        ret = cls_db.sum_power_result_ikwh(sdate)
        if ret == cls_db.lvNormal:
            read_db_list = cls_db.recordlist
            if read_db_list[0] == None:
                ikwh.append("0")
            else:
                ikwh.append(read_db_list[0])
        else:
            ikwh.append("0")

        ret = cls_db.sum_power_result_okwh(sdate)
        if ret == cls_db.lvNormal:
            read_db_list = cls_db.recordlist
            if read_db_list[0] == None:
                okwh.append("0")
            else:
                okwh.append(read_db_list[0])
        else:
            okwh.append("0")
    #last year

    #read monthly power
    #this year
    i = 0
    dt_now_i = dt_now
    for i in range(12):
        dt_now_i = dt_now + relativedelta(months=-i)
        sdate = dt_now_i.strftime('%Y%m')
        mm.append(dt_now_i.strftime('%Y/%m'))

        ret = cls_db.sum_power_result_ikwh(sdate)
        if ret == cls_db.lvNormal:
            read_db_list = cls_db.recordlist
            if read_db_list[0] == None:
                ikwhm.append("0")
            else:
                ikwhm.append(read_db_list[0])
        else:
            ikwhm.append("0")

        ret = cls_db.sum_power_result_okwh(sdate)
        if ret == cls_db.lvNormal:
            read_db_list = cls_db.recordlist
            if read_db_list[0] == None:
                okwhm.append("0")
            else:
                okwhm.append(read_db_list[0])
        else:
            okwhm.append("0")

    #last year


    return render_template("home.html", flg=flg, dt_now=lastupdate, input_voltage=input_voltage, input_current= input_current, output_voltage=output_voltage, output_current=output_current, input_power=input_power, output_power=output_power, md=md, ikwh=ikwh, okwh=okwh, mm=mm, ikwhm=ikwhm, okwhm=okwhm, msg=msg)


@app.route("/power")
def power():
    msg = ""
    flg = cls_cmn.lvNormal
    dt_now = datetime.datetime.now()
    str_dt_now = dt_now.strftime('%Y-%m-%d')
    str_dt_now_key = dt_now.strftime('%Y%m%d')

    dt_back = dt_now + datetime.timedelta(days=-1)
    dt_forward = dt_now + datetime.timedelta(days=1)
    str_dt_back = dt_back.strftime('%Y-%m-%d')
    str_dt_forward = dt_forward.strftime('%Y-%m-%d')
    #if dt_forward is future date then flgoff(do not display link)
    flg_forward = cls_cmn.flgoff

    ret = cls_db.read_power_result_key(str_dt_now_key)
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.recordlist

    #make graph data
    ikwh = list()
    okwh = list()
    costsave = list()
    md = list()

    dt_nowg = dt_now
    for i in range(7):    #get data in last 7days
        md.append(dt_nowg.strftime('%m/%d'))
        ret = cls_db.count_power_result_key(dt_nowg.strftime('%Y%m%d'))
        if ret == cls_db.lvNormal:
            if cls_db.recordlist[0] > 0:
                ret = cls_db.sum_power_result_ikwh(dt_nowg.strftime('%Y%m%d'))
                if ret == cls_db.lvNormal:
                    ikwh.append(Decimal(float(cls_db.recordlist[0])).quantize(Decimal('1e-2')))

                ret = cls_db.sum_power_result_okwh(dt_nowg.strftime('%Y%m%d'))
                if ret == cls_db.lvNormal:
                    okwh.append(Decimal(float(cls_db.recordlist[0])).quantize(Decimal('1e-2')))
                    costsave.append(Decimal(float(cls_db.recordlist[0]) * float(webapp_setting.tariff())).quantize(Decimal('1e-2')))
            else:
                ikwh.append(0.0)
                okwh.append(0.0)
                costsave.append(0.0)

        dt_nowg = dt_nowg + datetime.timedelta(days=-1)

    moneyunit = webapp_setting.tariff_unit()
    tariff = webapp_setting.tariff()

    return render_template("power.html", dt_now=str_dt_now, dt_back = str_dt_back, dt_forward = str_dt_forward, read_db_list=read_db_list, md=md, ikwh=ikwh, okwh=okwh, costsave=costsave, moneyunit=moneyunit, tariff=tariff, flg=flg, msg=msg, flg_forward=flg_forward)

@app.route("/power_post",methods=["post"])
def power_post():
    msg = ""
    flg = cls_cmn.lvNormal
    res_dt_now = request.form['dt_now']
    if res_dt_now == '':
        dt_now = datetime.datetime.now()
    else:
        dt_now = datetime.datetime.strptime(res_dt_now, '%Y-%m-%d')
    str_dt_now = dt_now.strftime('%Y-%m-%d')
    str_dt_now_key = dt_now.strftime('%Y%m%d')

    dt_back = dt_now + datetime.timedelta(days=-1)
    dt_forward = dt_now + datetime.timedelta(days=1)
    #if dt_forward is future date then flgoff(do not display link)
    flg_forward = cls_cmn.flgon
    if dt_forward > datetime.datetime.now():
        flg_forward = cls_cmn.flgoff
        dt_now = datetime.datetime.now()
        dt_back = dt_now + datetime.timedelta(days=-1)
        dt_forward = dt_now + datetime.timedelta(days=1)
        msg = ""

    str_dt_now = dt_now.strftime('%Y-%m-%d')
    str_dt_back = dt_back.strftime('%Y-%m-%d')
    str_dt_forward = dt_forward.strftime('%Y-%m-%d')
    str_dt_now_key = dt_now.strftime('%Y%m%d')

    ret = cls_db.count_power_result_key(str_dt_now_key)
    if ret == cls_db.lvNormal:
        if cls_db.recordlist[0] == 0:
            #Not Found
            flg = cls_cmn.notfound
#            if dt_now < datetime.datetime.now():
#                dt_back = dt_now
#                dt_now = dt_back + datetime.timedelta(days=1)
#                dt_forward = dt_now + datetime.timedelta(days=1)
#            elif dt_now > datetime.datetime.now():
#                dt_forward = dt_now
#                dt_now = dt_forward + datetime.timedelta(days=-1)
#                dt_back = dt_now + datetime.timedelta(days=-1)
            
            msg = "Requested data is not found."

        ret = cls_db.read_power_result_key(str_dt_now_key)
        if ret == cls_db.lvNormal:
            read_db_list = cls_db.recordlist


        #make graph data
        ikwh = list()
        okwh = list()
        costsave = list()
        md = list()
        dt_nowg = dt_now
        for i in range(7):    #get data in last 7days
            md.append(dt_nowg.strftime('%m/%d'))
            ret = cls_db.count_power_result_key(dt_nowg.strftime('%Y%m%d'))
            if ret == cls_db.lvNormal:
                if cls_db.recordlist[0] > 0:
                    ret = cls_db.sum_power_result_ikwh(dt_nowg.strftime('%Y%m%d'))
                    if ret == cls_db.lvNormal:
                        ikwh.append(Decimal(float(cls_db.recordlist[0])).quantize(Decimal('1e-2')))
                    ret = cls_db.sum_power_result_okwh(dt_nowg.strftime('%Y%m%d'))
                    if ret == cls_db.lvNormal:
                        okwh.append(Decimal(float(cls_db.recordlist[0])).quantize(Decimal('1e-2')))
                        costsave.append(Decimal(float(cls_db.recordlist[0]) * float(webapp_setting.tariff())).quantize(Decimal('1e-2')))
                else:
                    ikwh.append(0.0)
                    okwh.append(0.0)
                    costsave.append(0.0)

            dt_nowg = dt_nowg + datetime.timedelta(days=-1)


        moneyunit = webapp_setting.tariff_unit()
        tariff = webapp_setting.tariff()
    
        return render_template("power.html", dt_now=str_dt_now, dt_back=str_dt_back, dt_forward=str_dt_forward, read_db_list=read_db_list, md=md, ikwh=ikwh, okwh=okwh, costsave=costsave, moneyunit=moneyunit, tariff=tariff, flg=flg, msg=msg, flg_forward=flg_forward)

@app.route("/control_history")
def read_control_history():

    ret = cls_db.read_control_history()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    return render_template("control_history.html", read_db_list=read_db_list)

@app.route("/read_simple")
def read_record_simple():
    msg = ""
    str_dt = list()
    str_dt2 = list()
    dt_now = datetime.datetime.now()
    str_dt_now_key = dt_now.strftime('%Y/%m/%d')
    dt_back = dt_now + datetime.timedelta(days=-1)
    dt_forward = dt_now + datetime.timedelta(days=1)
    str_dt_back = dt_back.strftime('%Y-%m-%d')
    str_dt_forward = dt_forward.strftime('%Y-%m-%d')

    str_dt.append(str_dt_now_key)
    str_dt_now_key2 = dt_now.strftime('%Y-%m-%d')
    str_dt2.append(str_dt_now_key2)

    flg_forward = cls_cmn.flgoff

    #for i in range(6):
    #    dt_back = dt_now + datetime.timedelta(days=-1)
    #    str_dt_back_key = dt_back.strftime('%Y/%m/%d')
    #    str_dt.append(str_dt_back_key)


    #make graph data
    #portlist = list()
    #portlist = webapp_setting.epever_control_portName()
    #portlist = portlist.append('ALL')
    #graphlist = list()

    #last data
    ivoltageX = list()
    icurrentX = list()
    ovoltageX = list()
    ocurrentX = list()
    ivoltageY = list()
    icurrentY = list()
    ovoltageY = list()
    ocurrentY = list()
    port = 'ALL'
    for i in range(len(str_dt)):
        strkey = str_dt[len(str_dt) - i - 1]
        ret = cls_db.count_record_simple_key(port, strkey)
        if ret == cls_db.lvNormal:
            if cls_db.read_db_list[0] > 0:    #record found
                ret = cls_db.read_record_simple_ivoltage_key(port, strkey)
                if ret == cls_db.lvNormal:
                    for rec in cls_db.read_db_list:
                        ivoltageX.append(rec[0])
                        ivoltageY.append(rec[1])

                ret = cls_db.read_record_simple_icurrent_key(port, strkey)
                if ret == cls_db.lvNormal:
                    for rec in cls_db.read_db_list:
                        icurrentX.append(rec[0])
                        icurrentY.append(rec[1])

                ret = cls_db.read_record_simple_ovoltage_key(port, strkey)
                if ret == cls_db.lvNormal:
                    for rec in cls_db.read_db_list:
                        ovoltageX.append(rec[0])
                        ovoltageY.append(rec[1])

                ret = cls_db.read_record_simple_ocurrent_key(port, strkey)
                if ret == cls_db.lvNormal:
                    for rec in cls_db.read_db_list:
                        ocurrentX.append(rec[0])
                        ocurrentY.append(rec[1])
                

    ret = cls_db.read_record_simple()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    return render_template("read_simple.html", dt_now=str_dt_now_key2, dt_back=str_dt_back, dt_forward=str_dt_forward, read_db_list=read_db_list, str_dt=str_dt2, ivoltageX=ivoltageX, icurrentX=icurrentX, ovoltageX=ovoltageX, ocurrentX=ocurrentX, ivoltageY=ivoltageY, icurrentY=icurrentY, ovoltageY=ovoltageY, ocurrentY=ocurrentY, msg=msg, flg_forward=flg_forward)

@app.route("/read_simple_post",methods=["post"])
def read_record_simple_post():
    msg = ""

    res_dt_now = request.form['dt_now']
    #intbf = int(request.form['backandforward'])
    #dt_now = dt_now + datetime.timedelta(days = intbf)
    if res_dt_now == '':
        dt_now = datetime.datetime.now()
    else:
        dt_now = datetime.datetime.strptime(res_dt_now, '%Y-%m-%d')

    dt_back = dt_now + datetime.timedelta(days=-1)
    dt_forward = dt_now + datetime.timedelta(days=1)
    #if dt_forward is future date then flgoff(do not display link)
    flg_forward = cls_cmn.flgon
    if dt_forward > datetime.datetime.now():
        flg_forward = cls_cmn.flgoff
        dt_now = datetime.datetime.now()
        dt_back = dt_now + datetime.timedelta(days=-1)
        dt_forward = dt_now + datetime.timedelta(days=1)
        msg = ""

    str_dt = list()
    str_dt2 = list()
    str_dt_now_key = dt_now.strftime('%Y/%m/%d')
    str_dt.append(str_dt_now_key)
    str_dt_now_key2 = dt_now.strftime('%Y-%m-%d')
    str_dt2.append(str_dt_now_key2)

    str_dt_back = dt_back.strftime('%Y-%m-%d')
    str_dt_forward = dt_forward.strftime('%Y-%m-%d')

    #last data
    ivoltageX = list()
    icurrentX = list()
    ovoltageX = list()
    ocurrentX = list()
    ivoltageY = list()
    icurrentY = list()
    ovoltageY = list()
    ocurrentY = list()
    port = 'ALL'

    for i in range(len(str_dt)):
        strkey = str_dt[len(str_dt) - i - 1]
        ret = cls_db.count_record_simple_key(port, strkey)
        if ret == cls_db.lvNormal:
            if cls_db.read_db_list[0] == 0:   #record not found
                dt_now = dt_now + datetime.timedelta(days = -intbf)
                str_dt = list()
                str_dt2 = list()
                str_dt_now_key = dt_now.strftime('%Y/%m/%d')
                str_dt.append(str_dt_now_key)
                str_dt_now_key2 = dt_now.strftime('%Y-%m-%d')
                str_dt2.append(str_dt_now_key2)
                msg = 'requested data is not found.'
                strkey = str_dt[len(str_dt) - i - 1]

            ret = cls_db.read_record_simple_ivoltage_key(port, strkey)
            if ret == cls_db.lvNormal:
                for rec in cls_db.read_db_list:
                    ivoltageX.append(rec[0])
                    ivoltageY.append(rec[1])

            ret = cls_db.read_record_simple_icurrent_key(port, strkey)
            if ret == cls_db.lvNormal:
                for rec in cls_db.read_db_list:
                    icurrentX.append(rec[0])
                    icurrentY.append(rec[1])

            ret = cls_db.read_record_simple_ovoltage_key(port, strkey)
            if ret == cls_db.lvNormal:
                for rec in cls_db.read_db_list:
                    ovoltageX.append(rec[0])
                    ovoltageY.append(rec[1])

            ret = cls_db.read_record_simple_ocurrent_key(port, strkey)
            if ret == cls_db.lvNormal:
                for rec in cls_db.read_db_list:
                    ocurrentX.append(rec[0])
                    ocurrentY.append(rec[1])

    ret = cls_db.read_record_simple_key(port, strkey)
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    return render_template("read_simple.html", dt_now=str_dt_now_key2, dt_back=str_dt_back, dt_forward=str_dt_forward, read_db_list=read_db_list, str_dt=str_dt2, ivoltageX=ivoltageX, icurrentX=icurrentX, ovoltageX=ovoltageX, ocurrentX=ocurrentX, ivoltageY=ivoltageY, icurrentY=icurrentY, ovoltageY=ovoltageY, ocurrentY=ocurrentY, msg=msg, flg_forward=flg_forward)


@app.route("/read_all")
def read_record_all():

    ret = cls_db.read_colname()
    if ret == cls_db.lvNormal:
        read_col_list = cls_db.read_db_list
    else:
        read_col_list = []

    ret = cls_db.read_recordall()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    return render_template("read_all.html", read_col_list=read_col_list, read_db_list=read_db_list)

@app.route("/setting")
def read_setting():
    retd = ""
    msg = ""
    err_col = list()
    ret = cls_db.read_control()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    ret = cls_db.count_control()
    if ret == cls_db.lvNormal:
        count = cls_db.read_db_list[0]
    else:
        count = 0

    serial_ports = cls_tool.active_serial_ports()

    return render_template("setting.html", serial_ports=serial_ports, msg=msg, read_db_list=read_db_list, count=count, err_col=err_col, retd=retd)

@app.route("/setting_post",methods=["post"])
def update_setting():
    retd = ""
    msg = ""
    err_col = list()
    ret = cls_db.read_control()
    action = request.form['action']
    if ret == cls_db.lvNormal:
        if action == "update":
            read_db_list = cls_db.read_db_list
            for read_db in read_db_list:
                cls_db.num = int(request.form['num_' + str(read_db[0])])
                retd = retd + "|num: " + str(cls_db.num) + " col: "
                if cls_validation.num(cls_db.num) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.voltage_max = request.form['voltage_max_' + str(read_db[0])]
                if cls_validation.voltage(cls_db.voltage_max) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.voltage_min = request.form['voltage_min_' + str(read_db[0])]
                if cls_validation.voltage(cls_db.voltage_min) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.starttime = request.form['starttime_' + str(read_db[0])]
                if cls_validation.starttime(cls_db.starttime) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.duration = request.form['duration_' + str(read_db[0])]
                if cls_validation.duration(cls_db.duration) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.relay1 = request.form['relay1_' + str(read_db[0])]
                if cls_validation.relay(cls_db.relay1) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.relay2 = request.form['relay2_' + str(read_db[0])]
                if cls_validation.relay(cls_db.relay2) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                cls_db.relay3 = request.form['relay3_' + str(read_db[0])]
                if cls_validation.relay(cls_db.relay3) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"

                if ret == cls_cmn.lvNormal:
                    ret = cls_db.update_control()
                    if ret == cls_db.lvNormal:
                        msg = "update success"
                        err_col.append(cls_cmn.lvNormal)
                        retd = ""
                    else:
                        msg = "update error"
                        err_col.append(cls_cmn.lvError)
                else:
                    msg = "input value format is/are not correct"

        elif action == "add":
            ret2 = cls_db.max_num_control()
            lvalue = list()
            if ret2 == cls_db.lvNormal:
                num = int(cls_db.read_db_list[0]) + 1
                print("num=" + str(num))
                retd = retd + "0"
                lvalue.append(num)

                voltage_max = request.form['voltage_max_new']
                if cls_validation.voltage(voltage_max) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(voltage_max)

                voltage_min = request.form['voltage_min_new']
                if cls_validation.voltage(voltage_min) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(voltage_min)

                starttime = request.form['starttime_new']
                if cls_validation.starttime(starttime) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(starttime)

                duration = request.form['duration_new']
                if cls_validation.duration(duration) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(duration)

                relay1 = request.form['relay1_new']
                if cls_validation.relay(relay1) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(relay1)

                relay2 = request.form['relay2_new']
                if cls_validation.relay(relay2) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(relay2)

                relay3 = request.form['relay3_new']
                if cls_validation.relay(relay3) == cls_validation.lvError:
                    ret = cls_cmn.lvError
                    retd = retd + "1"
                else:
                    retd = retd + "0"
                    lvalue.append(relay3)

                if ret == cls_cmn.lvNormal:
                    ret = cls_db.write_control(lvalue)
                    if ret == cls_db.lvNormal:
                        msg = "add success"
                        err_col.append(cls_cmn.lvNormal)
                        retd = ""
                    else:
                        msg = "add error"
                        err_col.append(cls_cmn.lvError)
                else:
                    msg = "input value format is/are not correct"


    else:
        msg = "control list read error"

    ret = cls_db.read_control()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    ret = cls_db.count_control()
    if ret == cls_db.lvNormal:
        count = cls_db.read_db_list[0]
    else:
        count = 0

    serial_ports = cls_tool.active_serial_ports()


    return render_template("setting.html", serial_ports=serial_ports, msg=msg, read_db_list=read_db_list, count=count, err_col=err_col, retd=retd)

@app.route("/setting_post_delete",methods=["post"])
def delete_setting():
    retd = ""
    msg = ""
    err_col = list()

    #delete process
    num = int(request.form['del_num'])
    ret = cls_db.delete_control(num)
    if ret == cls_db.lvNormal:
        pass
    else:
        msg = "delete error"

    ret = cls_db.read_control()
    if ret == cls_db.lvNormal:
        read_db_list = cls_db.read_db_list
    else:
        read_db_list = []

    ret = cls_db.count_control()
    if ret == cls_db.lvNormal:
        count = cls_db.read_db_list[0]
    else:
        count = 0

    serial_ports = cls_tool.active_serial_ports()

    return render_template("setting.html", serial_ports=serial_ports, msg=msg, read_db_list=read_db_list, count=count, err_col=err_col, retd=retd)
