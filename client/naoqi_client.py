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
            
            print(f'COMMAND: \n{command}\n\n')

            # Connect to the server and send command
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 9559))
                s.sendall(pickle.dumps(command, protocol=2))  # Use protocol 2 for Python 2 compatibility

                # Receive the data size (4 bajty)
                size_data = s.recv(4)
                if len(size_data) < 4:
                    raise RuntimeError("Failed to receive data size")

                data_size = struct.unpack('>I', size_data)[0]
                # print("Expecting", data_size, "bytes")

                # Accepting the entire message
                data = bytearray()
                while len(data) < data_size:
                    packet = s.recv(4096)
                    if not packet:
                        raise RuntimeError("Connection closed before all data was received")
                    data.extend(packet)

                # print("Received", len(data), "bytes")
                
                # Deserialisation
                response = pickle.loads(data, encoding='latin1')
                # Convert dictionary keys from bytes back to strings
                response = {k.decode('utf-8') if isinstance(k, bytes) else k: v for k, v in response.items()}
                
                # Check if the response contains an error
                if not response['success']:
                    raise Exception(response['result'])
                
                return response['result']
        return wrapper
