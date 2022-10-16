from pydoc import cli
import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)

server_keypair = RSA.generate(1024)
decryptor = PKCS1_OAEP.new(server_keypair)
server_pubkey = server_keypair.public_key().export_key()

def decrypt(bytes: bytes, key: bytes):
    ciphertext = bytes[16:]
    nonce = bytes[:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    output = cipher.decrypt(ciphertext)
    return output

while True:
    conn, addr = s.accept()

    print("Sending server public key:\n", server_pubkey.decode())
    conn.send(server_pubkey)
    
    encrypted_session_key = conn.recv(4096)
    session_key = decryptor.decrypt(encrypted_session_key)
    print("Received session key:", session_key.hex())

    encrypted_client_public_key_nonce = conn.recv(4096)
    
    client_public_key = decrypt(encrypted_client_public_key_nonce, session_key)
    print("Received client public key:\n", client_public_key.decode())

    '''
    client_public_key_pem = conn.recv(4096)
    client_public_key = RSA.import_key(client_public_key_pem)
    verifier = pkcs1_15.new(client_public_key)
    print("Received client public key:\n", client_public_key_pem.decode())

    encrypted_message_and_signature = conn.recv(4096)
    print(encrypted_message_and_signature.hex())
    '''