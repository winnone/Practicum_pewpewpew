import usb
import requests

from practicum import find_mcu_boards, McuBoard, PeriBoard

if len(devs) == 0:
    print("*** No practicum board found.")
    exit(1)

mcu = McuBoard(devs[0])
print("*** Practicum board found")
peri = PeriBoard(mcu)

###############################
import sys
import board
import digitalio

from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY = '910c1d15f1af40279501302195ae2f40'
ADAFRUIT_IO_USERNAME = 'winnone0'
FEED_ID = 'digital'

def connected(client):
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)
    print('Waiting for feed data…')

def disconnected(client):
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

    if payload == "OFF":
        print("Turn off LED!")
        peri.set_led_value(0)

    elif payload == "ON":
        print("Turn on LED!")
        peri.set_led_value(1)

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()
client.loop_blocking()
