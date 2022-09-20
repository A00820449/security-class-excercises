import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)

private_key_pem = ""
with open("private.pem", "r") as file:
    private_key_pem = file.read()

private_key = RSA.import_key(private_key_pem)
encryptor = PKCS1_OAEP.new(private_key)

while True:
    conn, addr = s.accept()
    data = conn.recv(4096)
    if not data: break

    decrypted = encryptor.decrypt(data).decode("utf-8")

    print ("Received:", data)
    print("Decoded:", decrypted)
    