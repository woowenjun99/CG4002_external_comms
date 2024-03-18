from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from socket import *
import base64

class SecureMessenger:
    @staticmethod
    def encode_message(message: str) -> bytes:
        iv = Random.new().read(AES.block_size)
        secret_key = bytes("O0qOCQdm8LZ7hiuV", encoding="utf8")
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        encrypted_message = message.encode("utf8")
        encrypted_message = pad(encrypted_message, AES.block_size)
        encrypted_message: bytes = cipher.encrypt(encrypted_message)
        return base64.b64encode(iv + encrypted_message)