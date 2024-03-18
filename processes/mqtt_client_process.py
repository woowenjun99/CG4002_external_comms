from api.mqtt_client import MqttClient
from multiprocessing import Queue
from json import loads
from utils.logger import Logger
from logging import ERROR

def mqtt_client_process(outgoing_to_mqtt_queue: Queue):
    client = MqttClient()

    while True:
        message = outgoing_to_mqtt_queue.get()
        try: client.send_message(loads(message)["topic"], message)
        except:
            Logger.log(f"message topic {loads(message)['topic']} failed. retrying", level=ERROR)
        