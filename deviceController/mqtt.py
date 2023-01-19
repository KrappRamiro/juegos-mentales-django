import paho.mqtt.client as mqtt
import ssl
import paho.mqtt.subscribe as subscribe
from . import callbacks

# region armado_conexion
# ------------------ armado de conexion --------------------------- #
aws_iot_endpoint = "a3df45vgz0yp2s-ats.iot.us-east-1.amazonaws.com"
url = "https://{}".format(aws_iot_endpoint)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)


PATH_TO_CERTIFICATE = "certificates/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1.pem"

client = mqtt.Client(client_id="myPy",
                     protocol=mqtt.MQTTv311,
                     clean_session=True,
                     )
client.tls_set(certfile=PATH_TO_CERTIFICATE,
               keyfile=PATH_TO_PRIVATE_KEY,
               ca_certs=PATH_TO_AMAZON_ROOT_CA_1,
               cert_reqs=ssl.CERT_REQUIRED)

# ------------------------------------------------------------------ #
# endregion armado_conexion

client = mqtt.Client()
client.on_connect = callbacks.on_connect
client.on_message = callbacks.on_message
client.connect(ENDPOINT, port=8883, keepalive=60)  # Port 8883 for TCP

'''
topics = {
    "$aws/things/grilletes/shadow/update": callbacks.grilletes_callback,
    "$aws/things/soporte_cuchillos/shadow/update": callbacks.soporte_cuchillos_callback,
    "$aws/things/luz/shadow/update": callbacks.luz_callback,
    "$aws/things/heladera/shadow/update": callbacks.heladera_callback,
    "$aws/things/especiero/shadow/update": callbacks.especiero_callback,
}

for topic, callback in topics.items():
    subscribe.callback(callback, topic, hostname=ENDPOINT)

'''
