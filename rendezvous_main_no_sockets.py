# encoding: UTF-8

"""
PIG IMPLEMENTATION, the good one is goint to be implemented in C or Cython.
^--^ ___
(00){___}@
    || ||
"""
import socket
import sys
import time
from datetime import datetime
from thread import start_new_thread

import simplejson as json
from paho import mqtt

from utils import eprint
from coroutine import coroutine
from terra import Display, TemperatureSensor
from measurement import *
from config_file import OID, SENSOR1_OID

display = Display()
sensor = TemperatureSensor()

#server_address_display = '/var/run/rendezvous/terra/display'
#server_address_sensor = '/var/run/rendezvous/vaisala/sensor'


def calculate_max(current,maxx):
    return max(current, maxx)

def calculate_min(current, minn):
    return min(current, minn)

def get_max(sensor_oid):
    return get_max_temp(sensor_oid)
def get_min(sensor_oid):
    return get_min_temp(sensor_oid)



def get_current_time():
    """return current unix time"""
    return time.mktime(datetime.now().timetuple())

#@coroutine
def get_sensor_data(oid, period, target):
    """after reading this method broadcast the sensor data
        to display an save info"""
    while True:
        response = sensor.read(oid)
        if not response or response == []:
            print(response)
            print("No reponse from the senor")
            time.sleep(0.1)
            continue

        target.send(response)
        time.sleep(period)

@coroutine
def save_current_temp(oid, sensor_oid):
    while True:
        current_temp, _ , _ = (yield)
        set_current_temp(oid, sensor_oid, current_temp)

@coroutine
def save_historic_data(oid,sensor_oid):
    while True:
        current_temp, hr, _ = (yield)
        timestamp = get_current_time()
        save_measurament(timestamp, oid, sensor_oid, current_temp, hr)

@coroutine
def save_max_min(oid, sensor_oid):
    while True:
        current_temp, _, _ = (yield)
        maxt = get_max(sensor_oid)
        mint = get_min(sensor_oid)
        maxt = calculate_max(current_temp, maxt)
        mint = calculate_min(current_temp, mint)
        timestamp = get_current_time()
        set_max_temp(sensor_oid, maxt, timestamp)
        set_min_temp(sensor_oid, mint, timestamp)

@coroutine      
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets:
            target.send(item)

@coroutine
def show_current_temp(oid, sensor_oid, period):
    while True:
        result = get_current_temp(oid, sensor_oid)
        if result:
            current_temp, hr = result
        else:
            print "current temp and current hr are None"
            continue

        display.clear()
        display.write_line(0, " LECTURA ACTUAL:")
        display.write_line(1, current_temp + "C HR="+ hr )
        time.sleep(period)

@coroutine
def show_max_min_temp(sensor_oid, time):
    while True:
        maxin = get_max_temp(sensor_oid)
        minin = get_min_temp(sensor_oid)
        if maxim is None or minin is None:
            print("max temp or min temp is None")
            time.sleep(0.1)
            continue
        display.clear()
        display.write_line(0, " Maxima: " + maxin)
        display.write_line(0, " Minima: " + minin)
        time.sleep(period)



        

def rendenzvous_job():
    print("Init")
    get_sensor_data(1,60,
                    broadcast([
                        save_current_temp("heim01",1),
                        save_historic_data("heim01",1),
                        save_max_min("heim01",1)
                        ])
                    )
    print("Init: whow_current_temp")
    start_new_thread(show_current_temp,("heim01",1,60))
    time.sleep(30)
    start_new_thread(show_max_min_temp,(1,60))


if __name__ == '__main__':
    rendenzvous_job()





#display.turn_backlight(0)

