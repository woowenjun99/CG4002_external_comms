import grpc
import pb.relay_node_pb2_grpc as relay_node_pb2_grpc
from concurrent import futures
from external_communication.grpc.grpc_server import RelayNodeServicer
from utils.logger import Logger
from logging import ERROR
from multiprocessing import Queue

def grpc_server_process(
    action_queue_1: Queue, 
    action_queue_2: Queue, 
    player_turn, 
    grpc_client_queue: Queue
):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        relay_node_pb2_grpc.add_RelayNodeServicer_to_server(
            RelayNodeServicer(action_queue_1, action_queue_2, player_turn, grpc_client_queue), 
            server
        )
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()
        Logger.log("Server success")
    except Exception as e:
        Logger.log(e, level=ERROR)