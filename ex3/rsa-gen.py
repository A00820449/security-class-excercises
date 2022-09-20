# This program generates a public and private key pair and saves them in a file called public.pem and private.pem respectively
from Cryptodome.PublicKey import RSA

keypair = RSA.generate(1024)

with open("public.pem", "w") as file:
    file.write(keypair.public_key().export_key().decode())

with open("private.pem", "w") as file:
    file.write(keypair.export_key().decode())