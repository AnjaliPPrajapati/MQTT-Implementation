import paho.mqtt.client as paho
import random
import time
from datetime import datetime
import json

def on_publish(client, userdata, result): 
    print('Message published successfully..!',flush=True)

client = paho.Client('Sensor_publisher')
topics = ['sensors/temperature', 'sensors/humidity']
client.connect('mqtt_broker', 1883, keepalive = 60)
client.on_publish = on_publish
# Assuming that we are getting the data from sensor after every 1 min
for i in range(15):
    random_topic = random.choice(topics)   # To select random topic on which message needs to be published
    sensor_reading = {
        'sensor_id': "SI" + str(int(time.time() * 1000)),
        'value': random.randrange(1,100),
        'timestamp': str(datetime.now())
    }
    print('Publishing Sensor reading: ',sensor_reading, flush=True)
    client.publish(random_topic, json.dumps(sensor_reading))
    time.sleep(60) # sleep for 60 seconds after every publish
    # time.sleep(20) # testing purpose