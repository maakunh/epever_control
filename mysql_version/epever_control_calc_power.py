#epever_control_calc_power.py

import datetime
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
c = getcontext()
c.rounding = ROUND_HALF_UP

import epever_control_common
print(len(sys.argv))
if (len(sys.argv) < 2):
    dt_now = datetime.datetime.now()
    dateh = dt_now.strftime('%Y/%m/%d %H')
    dateh_num = dt_now.strftime('%Y%m%d%H')
else:
    strargv = sys.argv[1]
    dateh =  strargv[0:4] + "/" + strargv[4:6] + "/" + strargv[6:8] + " " + strargv[8:10]
    dateh_num = strargv[0:4] + strargv[4:6] + strargv[6:8] + strargv[8:10]

print(dateh)
cls_tool = epever_control_common.epever_control_tool()
ret = cls_tool.calc_power(dateh)
cls_cmnv = epever_control_common.epever_control_commonvalue()
if ret == cls_cmnv.lvNormal:
    cls_db = epever_control_common.epever_control_db()
    ret = cls_db.count_power_result(dateh_num)
    if ret == cls_db.lvNormal:
        if cls_db.recordlist[0] > 0:
            ret = cls_db.update_power_result(dateh_num, str(Decimal(cls_tool.ikwh).quantize(Decimal('1e-2'))), str(Decimal(cls_tool.okwh).quantize(Decimal('1e-2'))))
        else:
            ret = cls_db.write_power_result([dateh_num, str(Decimal(cls_tool.ikwh).quantize(Decimal('1e-2'))), str(Decimal(cls_tool.okwh).quantize(Decimal('1e-2')))])
else:
    ret = cls_cmnv.lvError

sys.exit(ret)