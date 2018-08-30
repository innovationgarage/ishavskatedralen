import paho.mqtt.client as mqtt
import os
import time
import config as c

# From https://github.com/kiranshashiny/python-cloudmqtt-example-rpi/blob/master/app.py

client = mqtt.Client()

client.username_pw_set(c.mqttUser, c.mqttPassword)
client.connect(c.mqttServer, c.mqttPort, 60)
client.loop_start()

# If we want to hear from the cathedral
#client.subscribe (c.mqttSubscribeTo ,0 )

leds_blueandred = bytearray([0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0,
                             0, 255, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, ])
leds_allwhite = bytearray([255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                           255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ])
leds_allgray = bytearray([20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                          20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, ])

while True:
    client.publish(c.mqttPublishTo, leds_blueandred)
    time.sleep(2)
    client.publish(c.mqttPublishTo, leds_allwhite)
    time.sleep(4)
    client.publish(c.mqttPublishTo, leds_blueandred)
    time.sleep(2)
    client.publish(c.mqttPublishTo, leds_allgray)
    time.sleep(10)
