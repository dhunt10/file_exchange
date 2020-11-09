import socket
import tqdm
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

server = socket.socket()
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(10)

client_socket, address = server.accept()

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filename, "wb") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
client_socket.close()
server.close()
