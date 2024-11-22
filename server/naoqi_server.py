# -*- encoding: UTF-8 -*-
# naoqi_server.py (Python 2)

import socket
import pickle
from naoqi import ALProxy


def convert_arg(arg):
    """
    Convert argument to its appropriate type.
    """
    try:
        # Try to convert to int
        converted = int(arg)
        return converted
    except ValueError:
        pass

    try:
        # Try to convert to float
        converted = float(arg)
        return converted
    except ValueError:
        pass

    # If all else fails, return as string
    return str(arg)


HOST = '127.0.0.1'  # Localhost for communication
PORT = 9559         # Port for listening to client commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("NAOqi server is running...")

# TODO: fix a code problem of initialising new proxy connection to robot every time
while True:
    conn, addr = server_socket.accept()
    print("\nConnected by", addr, "\n")

    try:
        data = conn.recv(4096)
        if not data:
            raise ValueError("Received empty data from client")

        command = pickle.loads(data)
        module_name = str(command['module'])
        method = str(command['method'])
        args = []
        for arg in command['args']:
            args.append(convert_arg(arg))
        ip = str(command['ip'])
        port = command['port']
        
        # print(command)
        print('============================')
        print("ip: ", ip)
        print("port: ", port)
        print("module_name: ", module_name)
        print("method: ", method)
        print("args: ", args)
        print('============================\n')

        proxy = ALProxy(module_name, ip, port)
        
        # Execute the requested method
        result = getattr(proxy, method)(*args)
        success = True

        # Always send a response
        response = pickle.dumps({'success': success, 'result': result})
        conn.sendall(response)

    except KeyboardInterrupt:
        print("QUIT")
        conn.close()
        exit(0)
    
    except Exception as e:
        print("Error:", e)
        error_response = pickle.dumps({'success': False, 'result': str(e)})
        conn.sendall(error_response)
        conn.close()
        exit(1)

    finally:
        conn.close()
