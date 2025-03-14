# -*- encoding: UTF-8 -*-
# naoqi_server.py (Python 2)

import os
os.system('cls')

import socket
import pickle
import struct
import ast 
# from naoqi import ALProxy
from proxy_service import ProxyService


def convert_arg(arg):
    try:
        if isinstance(arg, unicode): # type: ignore
            return str(arg)
        if not isinstance(arg, str):
            return arg
        # try convert simple data types and container types (except `set()` and `frozen_set()`)
        return ast.literal_eval(arg)
    except ValueError as err:
        # is thrown when `ast.literal_eval(arg)` is trying to convert string repr. of `set`.
        if arg[0] == '{' or arg[0] == 's' or arg[0] == 'f':
            return eval(arg)
        
        raise ValueError(err)
    

def convert_to_py3_compatible(obj):
    if isinstance(obj, str):
        try:
            obj.decode('utf-8')
            return {'__type__': 'unicode', 'data': obj.decode('utf-8')}
        except UnicodeDecodeError:
            return {'__type__': 'bytes', 'data': obj}
    elif isinstance(obj, unicode):  # type: ignore
        return {'__type__': 'str', 'data': obj}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_py3_compatible(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_py3_compatible(v) for k, v in obj.iteritems()}
    return obj


proxy_service = ProxyService()

HOST = '127.0.0.1'  # Localhost for communication
PORT = 9559         # Port for listening to client commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
for _ in range(4): print
print("=" * 50)
print("NAOqi server is running...\n")

ACTIVE = True
while ACTIVE:
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
        print(command['args'])
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

        proxy = proxy_service.get_proxy(module_name=module_name, ip=ip, port=port)
        # print(proxy_service.pool)
        
        # Execute the requested method
        result = getattr(proxy, method)(*args)
        print("RESULT: ", type(result))
        # print('res:', result[:20])
        success = True
        
        # Always send a response
        converted_result = convert_to_py3_compatible(result)
        response = pickle.dumps({
            'success': success, 
            'result': converted_result
            }, protocol=2)
        # Send the data size as 4 bytes (big-endian)
        conn.sendall(struct.pack('>I', len(response)))
        conn.sendall(response)

    except KeyboardInterrupt:
        print("QUIT")
        conn.close()
        ACTIVE = False
        exit(0)
    
    except Exception as e:
        print("Error:", e)
        error_response = pickle.dumps({'success': False, 'result': e}, protocol=2)
        conn.sendall(error_response)
        conn.close()
        ACTIVE = False
        exit(1)

    finally:
        conn.close()
