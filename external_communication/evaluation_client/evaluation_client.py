from socket import *
from external_communication.evaluation_client.encryption import SecureMessenger

class EvaluationClient:
    def __init__(self, port_num: int) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.port = port_num

    def send_message(self, message: str) -> None:
        message = SecureMessenger.encode_message(message)
        self.clientSocket.send(f"{len(message)}_".encode())
        self.clientSocket.send(message)

    def establish_handshake(self) -> None:
        self.clientSocket.connect(("0.0.0.0", self.port))
        self.send_message("hello")

    def receive_message(self) -> str:
        try:
            message = self.clientSocket.recv(2048, timeout=1.5)
            message = message.decode()
            return message.split("_", maxsplit=1)[1]
        except:
            return None