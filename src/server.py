import os
import socket

from pynput.mouse import Controller
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()

mouse = Controller()

host = os.getenv("SERVER_HOST")
port = int(os.getenv("SERVER_PORT"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(colored(f"# YUMMI CONTROLLER server started on port {port}", "green"))

while True:
    try:
        print(colored(f"# Waiting for new connection...", "white"))

        conn, addr = server_socket.accept()
        print(colored(f"# Connection established with {addr}", "green"))

        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(colored(f"# Client {addr} disconnected.", "yellow"))
                break

            print(data)

        conn.close()

    except Exception as e:
        print(colored(f"Error: {e}", "red"))