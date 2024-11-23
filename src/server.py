import os
import socket
import threading
import time
import pydirectinput

from dotenv import load_dotenv
from screeninfo import get_monitors
from termcolor import colored


load_dotenv()

host = os.getenv('SERVER_HOST', '0.0.0.0')
port = int(os.getenv('SERVER_PORT', 5555))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(colored(f'# YUMMI CONTROLLER server started on port {port}', 'green'))

screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

key_press_duration = float(os.getenv('KEY_PRESS_DURATION', 0.03))

def move_mouse_to_coords(x, y):
    screen_x = int(x * screen_width)
    screen_y = int(y * screen_height)

    pydirectinput.moveTo(screen_x, screen_y)

def press_key(key: str):
    try:
        pydirectinput.keyDown(key)

        time.sleep(key_press_duration)

        pydirectinput.keyUp(key)

    except ValueError as ex:
        print(colored(f'Invalid key: {key}. Error: {ex}', 'red'))

    except Exception as ex:
        print(colored(f'Unexpected error while pressing {key}: {ex}', 'red'))

def handle_input(command : str):
    try:
        if command.startswith('mouse_coords'):
            parts = command.split(':')[1].strip()
            x, y = map(float, parts.split(','))

            threading.Thread(target=move_mouse_to_coords, args=(x, y), daemon=True).start()
            print(colored('- moving mouse...', 'light_green'))

            return

        if command.startswith('key'):
            key = command.split(':')[1].strip()

            threading.Thread(target=press_key, args=(key,), daemon=True).start()
            print(colored(f'- pressed key [{key}]', 'light_green'))

            return
    except ValueError as ex:
        return

while True:
    try:
        print(colored(f'# Waiting for new connection...', 'white'))

        conn, addr = server_socket.accept()
        print(colored(f'# Connection established with {addr}', 'green'))

        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(colored(f'# Client {addr} disconnected.', 'yellow'))
                break

            commands = data.split(';')
            for comm in commands:
                handle_input(comm)

        conn.close()

    except Exception as e:
        print(colored(f'Error: {e}', 'red'))
