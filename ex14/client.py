import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

#message = "this is my very secret message"
message = input("message? ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))

print("Connected to server")

public_key_pem = s.recv(4096).decode("utf-8")

print("Received public key:\n", public_key_pem)

public_key = RSA.import_key(public_key_pem)
encryptor = PKCS1_OAEP.new(public_key)

encrypted = encryptor.encrypt(message.encode("utf-8"))

print("Message:", message)
print("Sending:", encrypted.hex())

s.send(encrypted)
