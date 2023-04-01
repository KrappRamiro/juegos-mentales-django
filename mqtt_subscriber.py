import sys
import paho.mqtt.client as paho
from time import localtime, strftime
pretty_topic = sys.argv[1]


def on_message(client, userdata, message):
    topic = message.topic.split('/')
    thingname = topic[0]
    if topic[2] == "polling":
        return
    message = message.payload.decode('utf-8')
    time = strftime("%H:%M:%S", localtime())  # for readability
    print(f"{time} - {thingname} dice: {message}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("---------   Connected to MQTT Broker!   ---------")
    else:
        print("Failed to connect, return code %d\n", rc)

    for index, cmd_topic in enumerate(sys.argv):
        if index == 0 or index == 1:  # Ignore the file name and the pretty_topic
            continue
        print(f"Subscribiendose a {cmd_topic}")
        client.subscribe(cmd_topic, 1)
    print(f'''
    #########################################################################################################
    ###########  Mostrando informacion sobre: {pretty_topic}  ############
    #########################################################################################################
    ''')


mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

print("Trying to connect with mqttc.connect")
mqttc.connect('192.168.0.10', 1883, keepalive=60)

mqttc.loop_forever()
