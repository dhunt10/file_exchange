from socket import *
import os
import tqdm
#from encrypt import encrypt
#from decrypt import decrypt

client = socket(AF_INET, SOCK_STREAM)
client.connect(('10.0.0.26', 8080))

#with open("~/Programs/encryption/files/key.key") as f:
#    key = f.readline()

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
#while True:
filename = input("Path to file: ")
#encrypt(filename, key)
file_size = os.path.getsize(filename)
#client.recv(2048).decode("utf8")
client.send(f"{filename}{SEPARATOR}{file_size}".encode())

progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filename, "rb") as f:
    for _ in progress:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        client.sendall(bytes_read)
        progress.update(len(bytes_read))

#decrypt(filename, key)
client.close()
