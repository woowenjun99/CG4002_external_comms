from utils.logger import Logger
from logging import ERROR
from external_communication.mqtt.mqtt_server import MqttServer
from multiprocessing import Queue

def mqtt_server_process(incoming_from_mqtt_queue: Queue):
    try:
        mqtt = MqttServer(incoming_from_mqtt_queue)
        mqtt.initialise_server()
    except Exception as e:
        Logger.log(e, level=ERROR)