import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.bind(('127.0.0.1', 1100))
s.listen(1)

output_file_name = "server_image.png"

while True:
    conn, addr = s.accept()
    chunk = conn.recv(2048)
    if not chunk: break
    
    print("Creating file...")
    with open(output_file_name, "wb") as file:
        while chunk:
            print("Received chunk...")
            file.write(chunk)
            chunk = conn.recv(2048)
    print("File done!")