
# wifi configuration
#WIFI_SSID = 'Jean'
#WIFI_PASS = '12345678'
WIFI_SSID = 'B2bi'
WIFI_PASS = 'Bambi1958+'

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'a1vvhlkz4tgdqp-ats.iot.eu-central-1.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/aws_root.ca'
AWS_CLIENT_CERT = '/flash/cert/aws_client.cert'
AWS_PRIVATE_KEY = '/flash/cert/aws_private.key'

################## Subscribe / Publish client #################
CLIENT_ID = 'PycomPublishClient'
TOPIC = 'PublishTopic'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'PublishTopic'
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "ShadowUpdater"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Delta Listener ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "DeltaListener"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Shadow Echo ########################
THING_NAME = "lopy4_wifi"
CLIENT_ID = "ShadowEcho"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
