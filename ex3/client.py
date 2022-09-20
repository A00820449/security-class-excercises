import socket
from Cryptodome.Cipher import AES

key = b'my secret key123'
message = 'my secret message'
cipher = AES.new(key, AES.MODE_EAX)
encrypted = cipher.encrypt(message.encode("utf-8"))
nonce = cipher.nonce

sendmsg = nonce + encrypted

print("Message:", message)
print("Sending:", sendmsg)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))

s.send(sendmsg)
