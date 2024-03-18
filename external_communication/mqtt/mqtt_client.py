from paho.mqtt.client import Client
from utils.logger import Logger
from time import perf_counter

class MqttClient:
    def __on_connect(self, client: Client, userdata, flags, rc: int):
        Logger.log("client is connected with broker")

    def send_message(self, topic: str, message: str):
        start = perf_counter()
        client = Client()
        client.on_connect = self.__on_connect
        status = client.connect("localhost", 1883, 60)
        if status == -1: raise Exception("error sending message")
        client.publish(topic, message)