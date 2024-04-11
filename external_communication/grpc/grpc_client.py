import grpc
from pb.relay_node_pb2_grpc import RelayNodeStub

class GrpcClient:
    def __init__(self) -> None:
        channel = grpc.insecure_channel("127.0.0.1:50052")
        self.stub = RelayNodeStub(channel)

    def update_game_state(self, message):
        self.stub.processGameState(message, wait_for_ready=True)