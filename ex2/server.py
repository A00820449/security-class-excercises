import socket
from Cryptodome.Cipher import AES

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)
key = b'my secret key123'

while True:
    conn, addr = s.accept()
    data = conn.recv(4096)
    if not data: break

    cipher = AES.new(key, AES.MODE_EAX, nonce=data[:16])

    print ("Received from client: ", data)

    decrypted = cipher.decrypt(data[16:]).decode("utf-8")
    print("Decoded:", decrypted)
    