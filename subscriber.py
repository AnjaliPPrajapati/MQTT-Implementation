import paho.mqtt.client as paho
import pymongo
import time
from datetime import datetime
import json
import redis

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')
print('Pymongo client created in subscriber',flush = True)
Sensor_database = mongo_client['sensor_database']
print('Database connected in subscriber ',flush = True)
sensor_readings = Sensor_database['sensor_readings']
print('Collection Connected in subscriber',flush = True)

redisCli = redis.Redis(
    host='redis',
    port=6379,
    charset="utf-8",
    decode_responses=True
    )
print('Redis connected in subscriber...!',flush = True)

def onMessage(client, userdata, msg):
    print("Message Recieved on topic ", msg.topic, ": ", msg.payload.decode(), flush = True)
    data_from_sensor = json.loads(msg.payload.decode())
    reading_id = "RI" + str(int(time.time() * 1000)) 
    if data_from_sensor:
        sensor_data = {
            'record_id' : reading_id, # unique id for every reading from sensor
            'sensor_id' : data_from_sensor['sensor_id'] if 'sensor_id' in data_from_sensor else '',
            'value' : data_from_sensor['value'] if 'value' in data_from_sensor else '',
            'timestamp': datetime.fromisoformat(data_from_sensor['timestamp']) if 'timestamp' in data_from_sensor else '',
            'sensor_topic': msg.topic,
            'is_deleted': False,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        data_insertion_output = sensor_readings.insert_one(sensor_data)
        if data_insertion_output:
            print('Record inserted in mongodb: ',list(sensor_readings.find({'record_id': reading_id})),flush=True)
            if redisCli.llen('sensor_readings') < 10:
                redisCli.rpush('sensor_readings',json.dumps(data_from_sensor)) # To append the element at the end of the list
                print('Current data stored in redis less than 10: ',redisCli.lrange('sensor_readings',0,-1),flush = True)
            else:
                removed_element = redisCli.lpop('sensor_readings')  # To remove the first element from the list
                redisCli.rpush('sensor_readings',json.dumps(data_from_sensor)) # To append the element at the end of the list
                print('Removed element from redis: ',removed_element, flush = True)
                print('Current data stored in redis: ',redisCli.lrange('sensor_readings',0,-1),flush = True)

client = paho.Client('sensor_subscriber')
client.on_message = onMessage
client.connect('mqtt_broker', 1883, keepalive = 60)
client.subscribe('sensors/temperature')
client.subscribe('sensors/humidity')
client.loop_forever()
