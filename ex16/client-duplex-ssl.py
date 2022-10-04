import socket, ssl, pprint

#create deault context
#context = ssl.create_default_context()
context = ssl._create_unverified_context()

    
context.check_hostname = False
#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = context.wrap_socket(s,server_hostname=socket.gethostname())

ssl_sock.connect(("127.0.0.1", 1100))

#get certificate
print("Obtaning server certificate ...\n")
cert=ssl_sock.getpeercert()
print("Peer name: ",repr(ssl_sock.getpeername())) 
print("Cipher :",ssl_sock.cipher())
print("Peer certificate :\n",pprint.pformat(cert))

#print("Sending HTTP GET request...\n")
# Set a simple HTTP request -- use httplib in actual code.
#ssl_sock.write(b"GET / HTTP/1.1\r")
ssl_sock.sendall(b'Hola XYZ Message')

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
while True:
    data = ssl_sock.recv(4096)
    pprint.pprint(data.split(b"\r\n"))
    if not data:
        break


#data = ssl_sock.recv(1024).split(b"\r\n")
#pprint.pprint(data)

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()