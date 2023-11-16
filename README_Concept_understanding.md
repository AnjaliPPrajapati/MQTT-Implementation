* What is MQTT:
  - MQTT stands for Message Queue Telemetry Transport.
  - It is a Protocol which works on Publisher - Subscirber Model(Pub-Sub).
  - Components of MQTT:
    * Publisher:
      Publishers are the clients who publishes the content or data to the Broker.
      
      When publishing content, they specify two main components: the Topic (the destination for the content) and the Payload (the actual data to be delivered to subscribers).
    * Subscriber:
      Subscribers are clients that subscribe to specific topics from the broker.
      
      The broker then sends the published content to all subscribers interested in the subscribed topics.
    * Broker:
      Brokers are used for the connection between the Publisher and Subscriber.
      
      When a publisher sends content to the broker, the broker identifies the associated topic and delivers the content to all relevant subscribers.
    * Topic:
      Broker contains multiple Topics. For Eg. home/hall/temperature, home/kitchen/temperature, home/hall/humidity, home/kitchen/bulb, home/kitchen/fan etc. In the example home/hall/temperature, we are subscribing the topic temperature from the home/hall.
      - Wildcards: Wildcards are used to subscribe multiple topics at once.
        
        Suppose you have to subscribe the temperature topic of all the home regions like hall, kitchen, bedroom etc, then in this case we can subscribe the topic as 'home/+/teperature' where '+' indicates that subscribe to the topic temperature of all the regions of home. This is called is single level wildcards.
        
        Now, let's say you want to subscribe the all the topics of home, then you will subscrie the topics as 'home/#' where '#' means all topics within home. This is called as multi level wildcards.
  - We can understand the publisher - subsciber model by the example of You Tube(Broker), Users(subscriber) subscribe to channels(Topic), and channel owners(publisher) publish content, which is then delivered to all subscribers of the channel.
  - Methods of MQTT:
    * Connect: Connect method is used to extablish a connection between publisher and broker or subscriber and broker.
    * Disconnect: Used to close the connection.
    * Publish : This method id used to publish the data to the particular topic.
    * Subscribe: This method is used to subscribe the topics.
  - Real world Use case in IOT:
    * MQTT is used by the many industries to get the information like temperature or humidity from the sensors.
    * MQTT can be used in IOT for making smart home appliances. For example you have a bulb and a fan in your home and you have created a smart switch for both of these, now you have two topics home/fan and home/bulb. In this case we give command(like on or off) to the smart switches from our phone or laptop and the switches then checks whether the command is for which topic and then accordingly it makes the actions.

* Implementaion Details:
    - We have used the Mosquitto which is an open source broker.
    - The Paho Python library provides an MQTT client that enables Python applications to communicate with MQTT brokers.
 
  - QOS levels in MQTT:
    QOS(Quality of service) Levels in MQTT are defined as the quality of delivery.
    
    There are three QOS levels: 1) QOS0(When you know your publisher and subscriber have stable connection and you are ok if some messages are getting dropped)  2) QOS1(when you want your every message should be recieved and you are ok with the duplicates) 3) QOS2(when you want your every messages should be recieved and duplicates are not allowed)
    
    Please refer for more details: https://cedalo.com/blog/understanding-mqtt-qos/
    
