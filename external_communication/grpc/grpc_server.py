from pb.relay_node_pb2_grpc import RelayNodeServicer
from ai.ai_logic import AILogic
from multiprocessing import Queue
from json import dumps
import pb.relay_node_pb2 as relay__node__pb2
from utils.logger import Logger

class RelayNodeServicer(RelayNodeServicer):
    def __init__(self, action_queue: Queue):
        self.action_queue = action_queue
        self.ai = AILogic()
        super().__init__()

    def processAi(self, request, context):
        Logger.log(request)
        action = None
        if request.test_action:
            action = request.test_action
        elif not request.shoot_detected:
            received_data = []
            for value in request.values:
                received_data.append([
                    int(value.acceleration_x * 1000), 
                    int(value.acceleration_y * 1000),
                    int(value.acceleration_z * 1000),
                    int(value.gyro_x * 1000),
                    int(value.gyro_y * 1000),
                    int(value.gyro_z * 1000),
                ])
            try:
                action = self.ai.process(received_data)
            except:
                action = "gun"
        else:
            action = "gun"

        self.action_queue.put(dumps({ 
            "action": action,
            "player_id": request.player_id
        }))
        return relay__node__pb2.FromRelayNodeResponse()
    
    def processGameState(self, request, context):
        return relay__node__pb2.GameStateResponse()