from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from socket import *
import base64
from encryption import SecureMessenger

def decode_message(cipher_text: str):
    decoded_message = base64.b64decode(cipher_text)
    iv = decoded_message[:AES.block_size]
    secret_key = bytes("O0qOCQdm8LZ7hiuV", encoding="utf8")
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(decoded_message[AES.block_size:])
    decrypted_message = unpad(decrypted_message, AES.block_size)
    decrypted_message = decrypted_message.decode('utf8')  # Decode bytes into utf-8
    return decrypted_message

def test_secure_messenger():
    secure_text = "hello"
    encrypted = SecureMessenger().encode_message(secure_text)
    assert decode_message(encrypted) == secure_text