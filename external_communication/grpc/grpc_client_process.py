from external_communication.grpc.grpc_client import GrpcClient
from multiprocessing import Queue
from pb.relay_node_pb2 import GameStateRequest
from json import loads

def grpc_client_process(grpc_client_queue: Queue):
    client = GrpcClient()
    while True:
        message = loads(grpc_client_queue.get())
        client.update_game_state(GameStateRequest(player_one=message["p1"], player_two=message["p2"]))