import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def key_encrypt(bytes: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext = cipher.encrypt(bytes)
    return nonce + ciphertext

message = "my very secret message"

client_keypair = RSA.generate(1024)
client_pubkey = client_keypair.public_key().export_key()
signer = pkcs1_15.new(client_keypair)

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

msg = key_encrypt(client_pubkey, session_key)
print("Sending encrypted public key:\n", client_pubkey.decode())
s.send(msg)
s.recv(4096)

h = SHA256.new(message.encode())
signature = signer.sign(h)
print("signature len:", len(signature))
message_and_signature = signature + message.encode()
msg = key_encrypt(message_and_signature, session_key)
print("Sending signed message:", message)
s.send(msg)
s.recv(4096)