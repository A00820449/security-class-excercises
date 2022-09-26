import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)

keypair = RSA.generate(1024)

decryptor = PKCS1_OAEP.new(keypair)
public_key_pem = keypair.public_key().export_key().decode()

while True:
    conn, addr = s.accept()

    print("Accepted connection")
    print("Sending public key:\n", public_key_pem)
    conn.send(public_key_pem.encode("utf-8"))

    data = conn.recv(4096)
    if not data: break

    decrypted = decryptor.decrypt(data).decode("utf-8")

    print ("Received:", data.hex())
    print("Decoded:", decrypted)
    