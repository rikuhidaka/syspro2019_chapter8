# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time
import RPi.GPIO as GPIO
import smbus
import datetime
import json
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/syspro-chapter8.json"

cred = credentials.Certificate('/home/pi/syspro-chapter8.json')
firebase_admin.initialize_app(cred)
i2c = smbus.SMBus(1)
address = 0x48

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.HIGH)
time.sleep(1)
GPIO.output(14, GPIO.LOW)

db = firestore.Client()

# コールバック関数を作成する
def on_snapshot(doc_snapshot, changes, read_time):
    for change in changes:
        print(u'New cmd: {}'.format(change.document.id))
        led = change.document.to_dict()["led"]
        print(u'LED: {}'.format(led))
        if led == "ON":
            print "ON"
            # ONにする処理
	    GPIO.output(14,GPIO.HIGH)
	    time.sleep(1)
        elif led == "OFF":
            print "OFF"
            # OFFにする
	    GPIO.output(14,GPIO.LOW)
	    time.sleep(1)

on_ref = db.collection('led').where(u'led', u'==', u'ON')
off_ref = db.collection('led').where(u'led', u'==', u'OFF')

# 監視を開始する
doc_watch = on_ref.on_snapshot(on_snapshot)
doc_watch = off_ref.on_snapshot(on_snapshot)

# 温度センサと接続できないうちはこの無限ループを使う
while True:
    pass