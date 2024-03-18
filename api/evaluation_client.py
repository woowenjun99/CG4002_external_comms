from socket import *
from utils.encryption import SecureMessenger

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
        message = self.clientSocket.recv(2048)
        message = message.decode()
        return message.split("_", maxsplit=1)[1]