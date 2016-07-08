import sqlite3 as lite
import paho.mqtt.client as mqtt

con = None
cur = None
try:
	con = lite.connect('rendezvous.db')
	cur = con.cursor()
	create_status_query = """CREATE TABLE IF NOT EXISTS
					Status(Oid TEXT PRIMARY KEY, Sensoroid TEXT , Temperature REAL,
					hr REAL, Maxtemp REAL, TimestampMaxtemp INT, Mintemp REAL, TimestampMintemp INT)"""
	create_historic_query = """CREATE TABLE IF NOT EXISTS 
							Historic(Timestamp INT, Oid TEXT, Sensor_oid TEXT,
							Temperature REAL, Hr REAL)"""

	cur.execute(create_historic_query)
	print("Database Historic created")
	cur.execute(create_status_query)
	print("Database Status created")

	# uptime, num of sensors, sensors_status, display status, rssi, ??
except Exception as e:
	print e
	
def create_sensor(oid, sensor_oid):
	cur.execute('INSERT OR REPLACE INTO Status(Oid, Sensoroid) VALUES(?, ?)',(oid, sensor_oid))
	con.commit()

def set_current_temp(oid, sensor_oid, current_temp):
	cur.execute('UPDATE Status SET Temperature = ? WHERE Oid = ? AND Sensoroid = ?',(current_temp, oid, sensor_oid))
	con.commit()

def get_current_temp(oid, sensor_oid):
	cur.execute('SELECT Temperature, hr FROM Status WHERE Oid = ? AND Sensoroid = ?'(oid, sensor_oid))
	result = cur.fetchone()
	if result:
		return result 
	return None

def save_measurament(timestamp, oid, sensor_oid, temp, hr):
	cur.execute('INSERT INTO Historic VALUES(?, ?, ?, ?, ?)',(timestamp, oid, sensor_oid, temp, hr))
	con.commit()

def get_max_temp(sensor_oid):
	cur.execute('SELECT Maxtemp FROM Status WHERE Sensoroid = ?', (sensor_oid,))
	result = cur.fetchone()
	if result:
		return result[0]
	return None

def set_max_temp(sensor_oid, max_temp, timestamp):
	cur.execute("UPDATE Status SET Maxtemp = ?, TimestampMaxtemp = ? WHERE Sensoroid = ?", (max_temp, timestamp, sensor_oid))
	con.commit()

def get_min_temp(sensor_oid):
	cur.execute('SELECT Mintemp FROM Status WHERE Sensoroid = ?', (sensor_oid,))
	result = cur.fetchone()
	if result:
		return result[0]
	return None

def set_min_temp(sensor_oid, min_temp, timestamp):
	cur.execute("UPDATE Status SET Mintemp = ?, TimestampMintemp = ? WHERE Sensoroid = ?", (min_temp, timestamp, sensor_oid))
	con.commit()


#Persist on Rendezvous Analitics

print("initializing mqtt client:")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect()




