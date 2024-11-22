# naoqi_client.py (Python 3)
import socket
import pickle

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
                response = s.recv(4096)
                result = pickle.loads(response)
                
                # Check if the response contains an error
                if not result['success']:
                    raise Exception(result['result'])
                
                return result['result']
        return wrapper
