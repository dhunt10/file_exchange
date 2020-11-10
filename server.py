import socket
import tqdm
import os
from threading import Thread


def accepting():
    while True:
        client_socket, address = server.accept()
        login(client_socket)
        #Thread(target=login, args=(client_socket,))
        #Thread(target=handle_client, args=(client_socket,)).start()

def login(client_socket):
    users = get_users()
    try:
        client_socket.send(bytes("Username: ", "utf8"))
        username = client_socket.recv(BUFFER_SIZE).decode("utf8")
        client_socket.send(bytes("Password: ", "utf8"))
        password = client_socket.recv(BUFFER_SIZE).decode("utf8")
        if users['users'][username] == password:
            os.system('cd {}'.format(os.path.join(username)))
            client_socket.send(bytes('0', "utf8"))
            Thread(target=handle_client, args=(client_socket,)).start()
    except KeyError:
        make_account(client_socket)

def make_account(client_socket):
    client_socket.send(bytes("Enter a username: ", "utf8"))
    username = client_socket.recv(BUFFER_SIZE).decode("utf8")
    client_socket.send(bytes("Enter a password: ", "utf8"))
    password = client_socket.recv(BUFFER_SIZE).decode("utf8")

    user = {username : password}
    users['users'].update(user)
    os.system('mkdir {}'.format(username))
    f = open('resources/users.txt', 'w')
    f.write(str(users))
    f.close()
    print("debug point")
    login()

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

def get_users():
    print("i am here")
    try:
        users = eval(open('resources/users.txt', 'r').read())
    except SyntaxError:
        users = ''
    return users

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12500
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

users = get_users()

server = socket.socket()
server.bind((SERVER_HOST, SERVER_PORT))

if __name__ == "__main__":
    server.listen(10)
    ACCEPT_THREAD = Thread(target=accepting)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
