from paho.mqtt.client import Client, MQTTMessage
from utils.logger import Logger
from multiprocessing import Queue
from json import loads, dumps

class MqttServer:
    def __init__(
            self,
            incoming_from_mqtt_queue: Queue
        ):
        self.client = Client()
        self.incoming_from_mqtt_queue = incoming_from_mqtt_queue

    def __on_connect(self, client, userdata, flags, rc):
        Logger.log("server is connected with broker")

    def __on_message(self, client: Client, userdata, msg: MQTTMessage):
        if msg.topic.startswith("from_visualiser/visibility"):
            self.incoming_from_mqtt_queue.put(msg.payload.decode())
            return

        # message = loads(msg.payload.decode())
        # self.action_queue.put(dumps({
        #     "action": "oppStepIntoBomb",
        #     "bomb_id": message["bomb_id"],
        #     "player_id": message["player_id"]
        # }))

    def initialise_server(self):
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        status = self.client.connect("localhost", 1883, 60)
        if status == -1: raise Exception("unable to listen to port 1883")
        self.client.subscribe("from_visualiser/visibility/+")
        self.client.subscribe("from_visualiser/bomb/+")
        self.client.loop_forever()
