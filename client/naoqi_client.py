# naoqi_client.py (Python 3)
import socket
import pickle
import struct


class ALProxyWrapper:
    def __init__(self, module, ip, port):
        self.module = module
        self.ip = ip
        self.port = port

    def __getattr__(self, method):
        def wrapper(*args):
            command = {
                'module': self.module,
                'method': method,
                'args': args,
                'ip': self.ip,
                'port': self.port
            }
            
            # print(f'COMMAND: \n{command}\n\n')

            # Connect to the server and send command
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 9559))
                s.sendall(pickle.dumps(command, protocol=2))  # Use protocol 2 for Python 2 compatibility

                # Receive the response
                # response = s.recv(4096)
                # result = pickle.loads(response)
                # data = bytearray()
                # while True:
                #     response = s.recv(4096)
                #     if not response: break
                #     data.extend(response)
                # result = pickle.loads(bytes(data))

                # Přijetí velikosti dat (4 bajty)
                size_data = s.recv(4)
                if len(size_data) < 4:
                    raise RuntimeError("Failed to receive data size")

                data_size = struct.unpack('>I', size_data)[0]
                print("Expecting", data_size, "bytes")

                # Přijetí celé zprávy
                data = b''
                while len(data) < data_size:
                    packet = s.recv(min(4096, data_size - len(data)))
                    if not packet:
                        raise RuntimeError("Connection closed before all data was received")
                    data += packet
                    print(f"Data length: {len(data)}")

                print("Received", len(data), "bytes")
                result = pickle.loads(data)
                print(f"RESULT: {result}\n\n")
                
                # Check if the response contains an error
                if not result['success']:
                    raise Exception(result['result'])
                
                return result['result']
        return wrapper
