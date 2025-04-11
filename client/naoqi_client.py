# naoqi_client.py (Python 3)
import socket
import pickle
import struct


class ALProxyWrapper:
    def __init__(self, module, ip, port):
        self.module = module
        self.ip = ip
        self.port = port

    def __getattr__(self, name):
        return SubProxy(self, name)
    
    
class SubProxy:
    def __init__(self, parent, path):
        self.parent = parent
        self.path = path

    def __getattr__(self, name):
        # extend the method path when accessing attributes
        return SubProxy(self.parent, f"{self.path}.{name}")

    def __call__(self, *args):
        # final method call with full path
        command = {
            'module': self.parent.module,
            'method': self.path,
            'args': args,
            'ip': self.parent.ip,
            'port': self.parent.port
        }
        # print(f'COMMAND: \n{command}\n\n')
        return send_request(command)
    

class ALBrokerWrapper:
    def __init__(self, name, ip, port, parent_ip, parent_port):
        self.name = name
        self.ip = ip
        self.port = port
        self.parent_ip = parent_ip
        self.parent_port = parent_port

    def __getattr__(self, method):
        def wrapper(*args):
            command = {
                'module': 'ALBroker',
                'method': method,
                'args': args,
                'ip': self.ip,
                'port': self.port,
                'name': self.name,
                'parent_ip': self.parent_ip,
                'parent_port': self.parent_port
            }
            
            # print(f'COMMAND: \n{command}\n\n')
            return send_request(command)
        return wrapper
    

def send_request(command):
     # Connect to the server and send command
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9559))
        s.sendall(pickle.dumps(command, protocol=2))  # Use protocol 2 for Python 2 compatibility

        # Receive the data size (4 bajty)
        size_data = s.recv(4)
        if len(size_data) < 4:
            raise RuntimeError("Failed to receive data size")

        data_size = struct.unpack('>I', size_data)[0]

        # Accepting the entire message
        data = bytearray()
        while len(data) < data_size:
            packet = s.recv(4096)
            if not packet:
                raise RuntimeError("Connection closed before all data was received")
            data.extend(packet)
        
        # Deserialisation
        response = pickle.loads(data, encoding='latin1')
        response = restore_py2_types(response)
        
        # Check if the response contains an error
        if not response['success']:
            raise Exception(response['result'])
        
        return response['result']


def restore_py2_types(obj):
        if isinstance(obj, dict) and '__type__' in obj:
            if obj['__type__'] == 'bytes':
                return obj['data'].encode('latin1')
            elif obj['__type__'] == 'str':
                return obj['data']
            elif obj['__type__'] == 'unicode':
                return obj['data']
        elif isinstance(obj, list):
            return [restore_py2_types(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: restore_py2_types(v) for k, v in obj.items()}
        return obj
