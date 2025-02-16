# -*- encoding: UTF-8 -*-
# server_py2.py
import socket
import pickle
import struct
import random

import random
import string

def generate_message():
    # Okrajové případy pro šířku a výšku
    width = random.choice([0, 1, random.randint(100, 640)])
    height = random.choice([0, 1, random.randint(100, 480)])

    # Počet vrstev (může být normální nebo 0 pro okrajový případ)
    layers = random.choice([0, 3])

    # Color space s ne-ASCII znaky
    color_space = random.choice([
        'kBGRColorSpace', 
        u'kÑonASCIIñSpace',  # Ne-ASCII znaky
        None                 # None jako okrajový případ
    ])
    
    # Časové značky
    timestamp_sec = random.choice([0, -1, random.randint(0, 1000)])  # Záporná hodnota jako okrajový případ
    timestamp_usec = random.choice([0, -1, random.randint(0, 1000000)])
    
    # Obrázková data: prázdný array, normální data nebo data s problematickými bajty
    image_data = random.choice([
        bytearray(),  # Prázdný array
        bytearray([random.randint(0, 255) for _ in range(width * height * layers)]),  # Normální data
        bytearray([0x00, 0x99, 0xFF, 0x00, 0x99, 0xFF]),  # Obsahující problematické bajty (např. 0x99)
        None  # None jako okrajový případ
    ])

    # Kamera ID (normální hodnoty a okrajové případy)
    camera_id = random.choice([-1, 0, 1, 999])  # Záporná hodnota a extrémní hodnota jako okrajový případ

    # Úhly (normální hodnoty a extrémní hodnoty)
    left_angle = random.choice([-float('inf'), float('inf'), random.uniform(-1.0, 1.0)])
    top_angle = random.choice([-float('inf'), float('inf'), random.uniform(-1.0, 1.0)])
    right_angle = random.choice([-float('inf'), float('inf'), random.uniform(-1.0, 1.0)])
    bottom_angle = random.choice([-float('inf'), float('inf'), random.uniform(-1.0, 1.0)])

    # Sestavení zprávy
    message = [
        width,
        height,
        layers,
        color_space,
        timestamp_sec,
        timestamp_usec,
        image_data,
        camera_id,
        left_angle,
        top_angle,
        right_angle,
        bottom_angle
    ]

    return message


def main():
    host = '0.0.0.0'
    port = 5005
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    print("Server is listening on port", port)
    conn, addr = s.accept()
    print("Connected by", addr)

    message = generate_message()
    # message = bytearray([0x01, 0x02, 0x99, 0x03, 0x04])
    data = pickle.dumps({'success': True, 'result': message}, protocol=2)  # Používáme protocol=2 kvůli kompatibilitě

    conn.sendall(struct.pack('>I', len(data)))  # Posíláme velikost dat
    conn.sendall(data)  # Posíláme samotná data
    print("Data sent to client")
    print("Sending ", str(len(data)), " bytes")

    conn.close()

if __name__ == "__main__":
    main()
