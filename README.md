By : Anjali Prajapati

* PROBLEM STATEMENT : 
The aim is to simply implement the MQTT(Message Queuing Telemetry Transport) broker, Publisher and Subscriber in order to get and store any data from the sensors and monitor thier readings.

* Below are the tools and technologies used for the implementation:
1) Python
2) Mosquitto
3) Docker
4) Mongodb
5) Redis
6) Fast API

* Instructions to run the project:
1) Install Docker in your system
2) Take clone of the repository
3) Run the command : docker-compose up
4) For Accessing the APIs:
    Once you have successfully executed docker-compose up command, Open below link in your browser:
    http://localhost:8000/docs
    Here, you will see the list of APIs, click on any of the API you wish to access, click on try it out button. After that put in the proper reuqest body and the click on execute.
5) Below is the sample request for the APIs:
    1. /get-latest-sensor-reading: Below API will be used for fetching the latest 10 sesnsor records, if sensor_id is passed in request object then it will revert with the records from redis if present else it will fetch from mongodb
    Sample Request for filter by sensor id: {
        "sensor_id":"SI1694415188974"
    }
    
    Sample request to get all latest 10 readings:
        {
            "sensor_id":""
        }

    2. /get-sensor-reading-by-filter : In this API put in from_datetime and to_datetime and sensor_id if you wish to filter by sensor_id. If from_datetime, to_datetime and sensor_id is empty, then this will return all the records.
    Sample Request body: {
            "from_datetime": "2023-09-11T05:33:00.000",
            "to_datetime": "2023-09-11T05:37:00.000",
            "sensor_id":"SI1694410402197"
        }

    Sample request body to get all records: {
            "from_datetime": "",
            "to_datetime": "",
            "sensor_id":""
        }

* Description of services in docker-compose.yml file:
1) mqtt_broker:
    This service is used to deploy MQTT broker by using mosquitto cilent.
    Firstly we are pulling the Mosquitton image from the docker hub and then we are runnign the command 'mosquitto -v'. 
    After this we are Mapping the ports 1883 so that the broker would be accesssible through local machine also.
2) mongodb:
    This service is used to store the data in mongodb database.
    First step is to pull the mongo image from docker hub, after that we have configured the volumes to ensure data persistency and the last step is to map the port 27017 so that other services can access this database on a specific port.
3) redis:
    This service is used to store the latest 10 records in a redis (will work as a cache).
    First step is to pull the redis image from docker hub, after that we have configured the volumes to ensure data safety and the last step is to map the port 6379 so that other services can access this database on a specific port.
4) mqtt_subscriber:
    MQTT subscriber will run on this service.
    Firstly we are building the image from the Dockerfile which contains the subscriber.py file.
    After building we are running the file by the command python subscriber.py.
5) mqtt_publisher:
    Messages will be published from the MQTT publisher running on this service.
    To implement this, we are building the image from the Dockerfile which contains the publisher.py file.
    After building we are running the file by the command python publisher.py.
6) fast_api_service:
    This service is used to access the APIs for monitoring the sensor readings.

* Problems encountered while implementaion:
1) Print Logs: 
    I was not able to see the Print statements I have put for the logging purpose, after some research I found out that sometimes print statements are not flushed in docker logs until and unless we are flushing it forcefully. So, this problem was solved by putting flush = True in every print statement.
2) Date range filter: 
    Date range filter was working with only specific date format and when changing the format it was throwing error, hence I have implemented a date range serializer which converts the date string to the desired format to be applied in filter.


    
