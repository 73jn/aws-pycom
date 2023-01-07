# Script python using boto3 to create a iot device and create a certificate for it
# We want to save the certificate and the private key in a file

import boto3
import json
import os
import sys
import time

# Create iot client
iot = boto3.client('iot', region_name='eu-central-1')

# Create a thing
responseCreateThing = iot.create_thing(
    thingName='myThingProvisioning'
)

# Create a certificate
responseCreateCert = iot.create_keys_and_certificate(
    setAsActive=True
)

# Save the certificate and the private key in a file
with open('certificate.pem.crt', 'w') as f:
    f.write(responseCreateCert['certificatePem'])
with open('responseCreateCert.pem.key', 'w') as f:
    f.write(responseCreateCert['keyPair']['PrivateKey'])

# Attach the certificate to the thing
responseAttachCertToThing = iot.attach_thing_principal(
    thingName='myThingProvisioning',
    principal=responseCreateCert['certificateArn']
)

# We already have a policy in the AWS allowIOT
# We just need to attach it to the certificate
responseAttachPol = iot.attach_policy(
    policyName='allowIOT',
    target=responseCreateCert['certificateArn']
)

# We need to wait a little bit to be sure that the certificate is attached to the thing
time.sleep(5)

# Get the endpoint
responseCreateEndpoint = iot.describe_endpoint(
    endpointType='iot:Data-ATS'
)

# Get the certificate
responseGetCert = iot.describe_certificate(
    certificateId=responseCreateCert['certificateId']
)


# Get the thing
responseGetThing = iot.describe_thing(
    thingName='myThingProvisioning'
)


# Create the json file
data = {    
    "endpoint": responseCreateEndpoint['endpointAddress'],
    "thingName": responseGetThing['thingName'],
    "certificatePem": responseGetCert['certificateDescription']['certificatePem'],
    "privateKey": responseCreateCert['keyPair']['PrivateKey']
}

# Save the json file
with open('provisioning.json', 'w') as f:
    json.dump(data, f)








