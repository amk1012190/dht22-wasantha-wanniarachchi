import time
import network
import dht
from machine import pin
from umqtt.simple import MQTTClient

# my id
my_id = "amk1012190"
broker = "iot.research.hamk.fi"

temp_topic = "HAMK/Fo/DHT22/" + my_id + "/temperature"
hum_topic = "HAMK/Fo/DHT22/" + my_id + "/humidity"

# wifi
ssid = "Infinix HOT 10"
password = "1234567890"

# dht22 sensor
sensor = dht.DHT22(Pin(28))

# connect wifi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while wifi.isconnected() == False:
    time.sleep(1)
print("wifi connected")

# connect mqtt
client = MQTTClient(my_id, broker)
client.connect()
print("mqtt connected")

old_temp = 0
old_hum = 0

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print(temp, hum)

    if temp != old_temp or hum != old_hum:
        client.publish(temp_topic, str(temp))
        client.publish(hum_topic, str(hum))
        print("sent")
        old_temp = temp
        old_hum = hum
    else:
        print("not sent, same value")

    time.sleep(10)
