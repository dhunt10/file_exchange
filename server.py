import socket
import tqdm
import os
from threading import Thread


def accepting():
    while True:
        client_socket, address = server.accept()
        Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
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


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

addresses = {}
server = socket.socket()
server.bind((SERVER_HOST, SERVER_PORT))

if __name__ == "__main__":
    server.listen(10)
    ACCEPT_THREAD = Thread(target=accepting)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
