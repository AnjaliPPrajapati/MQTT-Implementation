from fastapi import FastAPI
import json
from pydantic import BaseModel
import paho.mqtt.client as paho
from datetime import datetime
import pymongo
import redis
import sys,os
from typing import Optional

mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/') # Connectiong to mongodb
print('Mongodb client created',flush = True)
Sensor_database = mongo_client['sensor_database']  # To access the database having name sensor_database
print('database connected..!',flush = True)
sensor_readings = Sensor_database['sensor_readings']
print('Collection connected..!',flush = True)

redisCli = redis.Redis(
    host='redis',
    port=6379,
    charset="utf-8",
    decode_responses=True
    )
print('Connected to redis...!',flush = True)

class SensorData(BaseModel):  # To validate the incoming request object
    from_datetime : Optional[str]
    to_datetime : Optional[str]
    sensor_id : Optional[str]

class RedisData(BaseModel):
    sensor_id : Optional[str]

app = FastAPI()

def print_error(func_name, error = ""): # get the most recent exception and print it in yellow color along with line number on which error is occured
    exc_type, exc_obj, exc_tb = sys.exc_info()
    yellow =  '\033[93m'
    if exc_tb:
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(yellow," Error--> ",error," | Exception type: ", exc_type, " File Name: ",fname, " Function Name: ",func_name," Line No: ", exc_tb.tb_lineno,flush = True)
    else:
        print(yellow," Function Name: ",func_name, " Error--> ",error,flush = True)

# Author : Anjali Prajpati (10th september, 2023)
# Description : Below API will be used for fetching the latest sesnsor records, if sensor_id is passed in request object then it will revert with the records from redis if present else it will fetch from mongodb
@app.post("/get-latest-sensor-reading")
def get_latest_sensor_reading(request: RedisData):
    try:
        request_object = json.loads(request.json())
        return_object = {}
        sensor_data = redisCli.lrange('sensor_readings',0,-1)
        print('sensor_data: ',sensor_data, flush = True)
        return_object = {
            'message': 'No data found'
        }
        if sensor_data:
            result = [json.loads(data) for data in sensor_data]
            if 'sensor_id' in request_object and request_object['sensor_id']:
                result = [data for data in result if data['sensor_id'] == request_object['sensor_id']]
                if not result:
                    sensor_data = list(sensor_readings.find({'sensor_id': request_object['sensor_id']},
                    {'sensor_id': 1, 'value': 1, 'timestamp': 1, '_id': 0}
                    ).sort([('timestamp',pymongo.DESCENDING)]).limit(10))
                    return_object = {
                        'message': 'Data retrieved successfully!',
                        'result': sensor_data
                    }
                else:
                    return_object = {
                        'message': 'Data retrieved successfully!',
                        'result': result
                    }
            else:
                return_object = {
                        'message': 'Data retrieved successfully!',
                        'result': result
                    }
    except Exception as error:
        print_error('get_latest_sensor_reading ',error)
        return_object = {
            'message': 'Something went wrong'
        }
    return return_object

# Author : Anjali Prajpati (10th september, 2023)
# Description : Below API will be used for fetching the sensor reading based on sensor_id and date time range filters
@app.post("/get-sensor-reading-by-filter")
def get_sensor_reading_by_filter(request: SensorData):
    try:
        request_object = json.loads(request.json())
        return_object = {}
        sensor_data = []
        if all(key in request_object and request_object[key] for key in ['from_datetime','to_datetime']):
            from_datetime = date_time_serializer(request_object["from_datetime"])
            to_datetime = date_time_serializer(request_object["to_datetime"])
            if 'sensor_id' in request_object and request_object['sensor_id']:
                sensor_data = list(sensor_readings.find(
                {    'timestamp' : {
                        '$gte': from_datetime,
                        '$lte' : to_datetime
                    }, 
                    'sensor_id': request_object['sensor_id']
                },
                {'sensor_id' : 1, 'value':1, 'timestamp':1, '_id':0 }))
            else:
                sensor_data = list(sensor_readings.find({'timestamp':{'$gte':from_datetime, '$lte':to_datetime}},
                    {'sensor_id': 1, 'value': 1, 'timestamp': 1, '_id': 0}
                ))
        elif 'sensor_id' in request_object and request_object['sensor_id']:
            sensor_data = list(sensor_readings.find({'sensor_id':request_object['sensor_id']},{'sensor_id' : 1, 'value':1, 'timestamp':1, '_id':0 }))
        else:
            sensor_data = list(sensor_readings.find({},{'sensor_id' : 1, 'value':1, 'timestamp':1, '_id':0 }))
        return_object = {
            'message': 'No data found'
        }
        if sensor_data:
            return_object = {
                'message': 'Data retrieved successfully!',
                'result': sensor_data
            }
    except Exception as error:
        print_error('get_sensor_reading_by_filter',error)
        return_object = {
            'message': 'Something went wrong'
        }
    return return_object



def date_time_serializer(sample_datetime):
    try:
        date_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S.%f",
            "%m/%d/%Y %H:%M:%S",
        ]
        matched_format, formatted_datetime_str = None, None
        for date_format in date_formats:
            try:
                datetime_obj = datetime.strptime(sample_datetime, date_format)
                matched_format = date_format
                break
            except ValueError:
                continue
        if matched_format:
            print(f"Input datetime string matches the format: {matched_format}")
            formatted_datetime_str = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
            formatted_datetime_str = datetime.strptime(formatted_datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            print("Input datetime string does not match any of the specified formats")
    except Exception as error:
        print("date_time_serializer() ",error)
    return formatted_datetime_str