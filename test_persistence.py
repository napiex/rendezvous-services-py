import time 
from datetime import datetime
from measurement import *
from config_file import SENSOR1_OID, OID
create_sensor(OID, SENSOR1_OID)
n = datetime.now()
temp = 10
current_temp = set_current_temp(OID, SENSOR1_OID, temp) 
set_min_temp(SENSOR1_OID, current_temp, time.mktime(n.timetuple()))
current_min = get_min_temp(SENSOR1_OID)
print current_temp
print current_min
assert (current_temp == current_min), "current_temp must be equal to min_temp"
set_max_temp(SENSOR1_OID, current_temp, time.mktime(n.timetuple()))
current_max = get_max_temp(SENSOR1_OID)



