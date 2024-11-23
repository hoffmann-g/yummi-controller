import os
import socket
import threading
import time

from pynput import keyboard, mouse
from termcolor import colored
from dotenv import load_dotenv
from screeninfo import get_monitors


load_dotenv()

server_ip = os.getenv('SERVER_IP', "localhost")
port = int(os.getenv('SERVER_PORT', 5555))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, port))
print(colored(f'# Connected YUMMI server on {server_ip}:{port}', 'green'))

mouse_controller = mouse.Controller()

screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

q_key = os.getenv('Q_ABILITY', "1")
w_key = os.getenv('W_ABILITY', "2")
e_key = os.getenv('E_ABILITY', "3")
r_key = os.getenv('R_ABILITY', "4")

q_mouse_listen_duration = float(os.getenv('Q_MOUSE_DURATION', 1.35))
r_mouse_listen_duration = float(os.getenv('R_MOUSE_DURATION', 3.5))

def send_mouse_coords(seconds: float):
    start_time = time.time()
    while time.time() - start_time < seconds:
        x, y = mouse_controller.position

        # scale coords from 0 to 1
        scaled_x = x / screen_width
        scaled_y = y / screen_height

        message = f'mouse_coords: {scaled_x:.4f}, {scaled_y:.4f};'
        client_socket.send(message.encode())

        time.sleep(0.01)  # 10ms

def send_key_press(key: str):
    message = f'key: {key};'
    client_socket.send(message.encode())

def handle_command(key_pressed):
    try:
        key = str(key_pressed.char).upper()

        if key == q_key:
            threading.Thread(target=send_key_press, args=('Q',), daemon=True).start()
            print(colored('- key sent: [Q]', 'light_yellow'))
            threading.Thread(target=send_mouse_coords, args=(q_mouse_listen_duration,), daemon=True).start()
            print(colored('- sending mouse coords...', 'light_yellow'))

        if key == w_key:
            threading.Thread(target=send_key_press, args=('W',), daemon=True).start()
            print(colored('- key sent: [W]', 'light_yellow'))

        if key == e_key:
            threading.Thread(target=send_key_press, args=('E',), daemon=True).start()
            print(colored('- key sent: [E]', 'light_green'))

        if key == r_key:
            threading.Thread(target=send_key_press, args=('R',), daemon=True).start()
            print(colored('- key sent: [R]', 'magenta'))
            threading.Thread(target=send_mouse_coords, args=(r_mouse_listen_duration,), daemon=True).start()
            print(colored('- sending mouse coords...', 'magenta'))
    except AttributeError:
        pass

with keyboard.Listener(on_press = handle_command) as listener:
    listener.join()

