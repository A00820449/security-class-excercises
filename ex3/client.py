import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

public_key_pem = ""
with open("public.pem", "r") as file:
    public_key_pem = file.read()

public_key = RSA.import_key(public_key_pem)

encryptor = PKCS1_OAEP.new(public_key)

message = "my secret message"

encrypted = encryptor.encrypt(message.encode("utf-8"))

print("Message:", message)
print("Sending:", encrypted)

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))

s.send(sendmsg)
'''
