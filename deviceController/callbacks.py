def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, message):
    # Do something
    print(" Received message " + str(message.payload)
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))
    pass


def grilletes_callback():
    pass


def soporte_cuchillos_callback():
    pass


def luz_callback():
    pass


def heladera_callback():
    pass


def especiero_callback():
    pass
