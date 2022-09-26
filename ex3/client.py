import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

public_key = None
with open("public.pem", "r") as file:
    public_key = RSA.import_key(file.read())

encryptor = PKCS1_OAEP.new(public_key)

#message = "this is my very secret message"
message = input("message? ")

encrypted = encryptor.encrypt(message.encode("utf-8"))

print("Message:", message)
print("Sending:", encrypted.hex())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))

s.send(encrypted)
