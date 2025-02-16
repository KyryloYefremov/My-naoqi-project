# client_py3.py
import socket
import pickle
import struct

def main():
    host = '127.0.0.1'
    port = 5005
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Přijmeme velikost zprávy
    size_data = s.recv(4)
    if len(size_data) < 4:
        raise RuntimeError("Failed to receive data size")

    data_size = struct.unpack('>I', size_data)[0]
    print("Expecting", data_size, "bytes")

    # Přijetí celé zprávy
    data = bytearray()
    while len(data) < data_size:
        packet = s.recv(4096)
        if not packet:
            raise RuntimeError("Connection closed before all data was received")
        data.extend(packet)

    print("Received", len(data), "bytes")
    
    # Deserializace
    response = pickle.loads(bytes(data))
    
    if response is None:
        print("Deserialization failed: Received None")
    else:
        message = response['result']
        print("Deserialization successful. Message received:")
        for i, item in enumerate(message):
            print(f"  [{i}]: {type(item)} -> {item is not None}")

    s.close()

if __name__ == "__main__":
    main()
