import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Cipher import PKCS1_OAEP

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)

server_keypair = RSA.generate(1024)
decryptor = PKCS1_OAEP.new(server_keypair)
server_pubkey = server_keypair.public_key().export_key()

def key_decrypt(bytes: bytes, key: bytes):
    ciphertext = bytes[16:]
    nonce = bytes[:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    output = cipher.decrypt(ciphertext)
    return output

while True:
    print("Waiting for connection...")
    conn, addr = s.accept()

    print("Sending server public key:\n", server_pubkey.decode())
    conn.send(server_pubkey)
    
    encrypted_session_key = conn.recv(4096)
    session_key = decryptor.decrypt(encrypted_session_key)
    print("Received session key:", session_key.hex())
    conn.send(b'ok')

    encrypted_secret_nonce = conn.recv(4096)
    secret = key_decrypt(encrypted_secret_nonce, session_key)
    print("Received client secret:", secret.decode())    
    conn.send(b'ok')

    encrypted_message_mac = conn.recv(4096)
    message_digest = key_decrypt(encrypted_message_mac, session_key)
    mac = message_digest[:32]
    message = message_digest[32:]
    print("Received message:", message.decode())
    conn.send(b'ok')

    try:
        h = HMAC.new(secret, digestmod=SHA256)
        h.update(message)
        h.verify(mac)
        print("Valid hmac signature")
    except ValueError:
        print("Not a valid hmac signature")