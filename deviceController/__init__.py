from .mqtt import mqttc
from pymongo import MongoClient

# https://stackoverflow.com/questions/41015779/how-to-use-paho-mqtt-client-in-django

mqttc.loop_start()

uri = "mongodb+srv://juegos-mentales.cqtvjtv.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
mongoc = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='certificates/mongodb-atlas-X509-cert.pem')

global_luz = {}


def mutate_luz(luz):
    global global_luz
    global_luz = luz
