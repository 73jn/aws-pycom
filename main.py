from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from network import WLAN
import time
import config
import socket

# THe TOPIC is data/thingsname/attributes
# The message is a json string
TOPIC = "data/"+config.THING_NAME+"/attributes"


print("Starting main.py (publish)...")
# Connect to wifi
wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(None, config.WIFI_PASS), timeout=50000)
while not wlan.isconnected():
    time.sleep(0.5)
print('WLAN connection succeeded!')

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
pycomAwsMQTTClient.configureLastWill(TOPIC, config.LAST_WILL_MSG, 1)

#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
    print('AWS connection succeeded')

time.sleep(2)
# Subscribe to topic
pycomAwsMQTTClient.subscribe(TOPIC, 1, customCallback)
time.sleep(2)

# Send message to host
loopCount = 0
while loopCount < 8:
	pycomAwsMQTTClient.publish(TOPIC, "New Message " + str(loopCount), 1)
	loopCount += 1
	time.sleep(5.0)
