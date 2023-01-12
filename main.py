from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from network import WLAN
import time
import config
import socket


import machine
from pycoproc_1 import Pycoproc
import pycom

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE


py = Pycoproc(Pycoproc.PYSENSE) # Init board pysense
si = SI7006A20(py)
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")

lt = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

li = LIS2HH12(py)

print("Starting main.py (publish)...")
# Connect to wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(None, config.WIFI_PASS), timeout=50000)
while not wlan.isconnected():
	time.sleep(0.5)
print('WLAN connection succeeded!')


MOVING = 0
def moving_cb(pin):
	print('moving detected')
	global MOVING
	if pin() == 1:
		MOVING = 1




print("ACCELEROMETER_READING")
li.enable_activity_interrupt(1000, 200, moving_cb) 
time.sleep(2)
ACCELEROMETER_DATA = bytes([MOVING])
print("ACCELEROMETER_DATA: ", ACCELEROMETER_DATA)


# Create a JSON Message to send to AWS IoT
def createJSONMessageTemp():
	global ACCELEROMETER_DATA
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"temperature":' + str(si.temperature())
	JSONMessage += '}'
	return JSONMessage

def createJSONMessageHumidity():
	global ACCELEROMETER_DATA
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"humidity":' + str(si.humidity())
	JSONMessage += '}'
	return JSONMessage

def createJSONMessageLight1():
	global ACCELEROMETER_DATA
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"light1":' + str(lt.light()[0])
	JSONMessage += '}'
	return JSONMessage

def createJSONMessageLight2():
	global ACCELEROMETER_DATA
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"light2":' + str(lt.light()[1])
	JSONMessage += '}'
	return JSONMessage

def createJSONMessageAccelerometer():
	global ACCELEROMETER_DATA
	global MOVING
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"accelerometer":' + str(MOVING)
	JSONMessage += '}'
	return JSONMessage

def createJSONMessage():
	global ACCELEROMETER_DATA
	global MOVING
	global si
	global lt
	# Create a JSON Message to send to AWS IoT
	JSONMessage = '{'
	JSONMessage += '"temperature":' + str(si.temperature())
	JSONMessage += ', "humidity":' + str(si.humidity())
	JSONMessage += ', "light1":' + str(lt.light()[0])
	JSONMessage += ', "light2":' + str(lt.light()[1])
	JSONMessage += ', "accelerometer":' + str(MOVING)
	JSONMessage += '}'
	return JSONMessage





# THe TOPIC is data/thingsname/attributes
# The message is a json string
TOPIC = "data/"+config.THING_NAME+"/attributes"
TOPIC_TEMP = "data/"+config.THING_NAME+"/temperature"
TOPIC_HUMIDITY = "data/"+config.THING_NAME+"/humidity"
TOPIC_LIGHT1 = "data/"+config.THING_NAME+"/light1"
TOPIC_LIGHT2 = "data/"+config.THING_NAME+"/light2"
TOPIC_ACCELEROMETER = "data/"+config.THING_NAME+"/accelerometer"





# user specified callback function
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

print(socket.dnsserver())

# configure the MQTT client
pycomAwsMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
pycomAwsMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
pycomAwsMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)

pycomAwsMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
#pycomAwsMQTTClient.configureLastWill(TOPIC, config.LAST_WILL_MSG, 1)

#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
	print('AWS connection succeeded')

# Subscribe to topic 
#pycomAwsMQTTClient.subscribe(TOPIC, 1, customCallback)

# Subscribe to topic temperature, humidity, light1, light2, accelerometer
#pycomAwsMQTTClient.subscribe(TOPIC_TEMP, 1, customCallback)
#pycomAwsMQTTClient.subscribe(TOPIC_HUMIDITY, 1, customCallback)
# pycomAwsMQTTClient.subscribe(TOPIC_LIGHT1, 1, customCallback)
# pycomAwsMQTTClient.subscribe(TOPIC_LIGHT2, 1, customCallback)
# pycomAwsMQTTClient.subscribe(TOPIC_ACCELEROMETER, 1, customCallback)

time.sleep(2)

# Send message to host
pycomAwsMQTTClient.publish(TOPIC, createJSONMessage(), 1)

# Publish to topic temperature, humidity, light1, light2, accelerometer
#pycomAwsMQTTClient.publish(TOPIC_TEMP, createJSONMessageTemp(), 1)
#pycomAwsMQTTClient.publish(TOPIC_HUMIDITY, createJSONMessageHumidity(), 1)
#pycomAwsMQTTClient.publish(TOPIC_LIGHT1, createJSONMessageLight1(), 1)
#pycomAwsMQTTClient.publish(TOPIC_LIGHT2, createJSONMessageLight2(), 1)
#pycomAwsMQTTClient.publish(TOPIC_ACCELEROMETER, createJSONMessageAccelerometer(), 1)
time.sleep(2)
pycomAwsMQTTClient.disconnect()
wlan.disconnect()
print('AWS connection closed')
time.sleep(2)
# Deepsleep
machine.deepsleep(1000)
