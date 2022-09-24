import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1100))

print("Opening file...")
with open("client_image.png", "rb") as file:
    file_data = file.read(2048)

    while file_data:
        print("Sending chunk...")
        s.send(file_data)
        file_data = file.read(2048)
print("File sent!")