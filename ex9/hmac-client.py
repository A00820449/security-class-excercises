import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def key_encrypt(bytes: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext = cipher.encrypt(bytes)
    return nonce + ciphertext

message = "my very secret message"

secret = b'my very secret secret'
h = HMAC.new(secret, digestmod=SHA256)

session_key = get_random_bytes(16)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))
server_pub_key_pem = s.recv(4096)

print("Received server public key:\n", server_pub_key_pem.decode())
server_pub_key = RSA.import_key(server_pub_key_pem.decode())
encryptor = PKCS1_OAEP.new(server_pub_key)

encryped_session_key = encryptor.encrypt(session_key)
print("Sending session key:", session_key.hex())
s.send(encryped_session_key)
s.recv(4096)

msg = key_encrypt(secret, session_key)
print("Sending secret:", secret.decode())
s.send(msg)
s.recv(4096)

h.update(message.encode())
mac = h.digest()
msg = key_encrypt(mac + message.encode(), session_key)
print("Sending mac signed message:", message)
s.send(msg)
s.recv(4096)