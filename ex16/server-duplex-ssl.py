import socket, ssl

#create a context and load certification file and keyfile
#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context = ssl._create_unverified_context()
#context.load_cert_chain(certfile="selfsigned.cer", keyfile="private.key")
context.load_cert_chain(certfile="RRV-selfsigned.cer", keyfile="RRV-private.key")

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen()
print("Listening in port 1100 ...\n")

while True:
    conn, addr = s.accept()
    connstream = context.wrap_socket(conn, server_side=True)
    #conn.send(b"I will send certificate with key ")
    connstream.send(b"I will send certificate with key ")
    data = connstream.recv(4096)
    #ata = connstream.read()
    if not data: break
    print ("Received from client: ",data.decode("ascii"))
    
'''
connection,address=s.accept();
with connection:
    a=connection.recv(1024);
    print(a.decode("ascii"))
    connection.close();
'''