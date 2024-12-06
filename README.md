# NAOqi Python 2 to Python 3 Bridge

This project provides a Python 3-compatible wrapper for the NAOqi SDK, originally available only in Python 2. With this bridge, you can write code that communicates with NAO robots in Python 3, using the same syntax as NAOqi's original Python 2 library.

## Project Structure
```shell
my_naoqi_project/
├── server/                         # Server-side code (Python 2)
│   ├── venv_py2/                   # Python 2 virtual environment
│   ├── naoqi_server.py             # Server to execute NAOqi commands
│   └── requirements.txt            # Python 2 dependencies
│
├── client/                         # Client-side code (Python 3)
│   ├── venv_py3/                   # Python 3 virtual environment
│   ├── naoqi3.py                   # Wrapper to emulate NAOqi in Python 3
│   ├── naoqi_client.py             # Client to communicate with Python 2 server
│   ├── main.py                     # Example usage in Python 3
│   └── requirements.txt            # Python 3 dependencies
│
└── README.md                       # Project documentation
```

## How It Works

This project uses a Python 2 server to execute NAOqi commands and a Python 3 client that mimics the syntax of the NAOqi API. When you call NAOqi functions in Python 3, the client sends the commands to the Python 2 server, which performs the actions and returns the results back to the Python 3 client.

## Main Components

- **server/naoqi_server.py** (Python 2): A server that listens for commands, executes them using the NAOqi SDK, and returns the results.
- **client/naoqi3.py** (Python 3): Provides an `ALProxy` class that emulates the NAOqi syntax, forwarding commands to `naoqi_client.py`.
- **client/naoqi_client.py** (Python 3): A client that communicates with the Python 2 server, handling command transmission and result retrieval.

## Setup Instructions

### Step 1: Set up the Python 2 Environment (Server)

1. Go to the `server/` directory:

   ```bash
   cd my_naoqi_project/server
   ```

2. Create a Python 2 virtual environment:
```bash
"C:\Python27\python.exe" -m virtualenv venv_py2
```

3. Activate the Python 2 environment 
```bash
.\venv_py2\Scripts\activate
```

### Step 2: Set up the Python 3 Environment (Client)

1. Go to the client/ directory:
```bash
cd ../client
```
2. Create a Python 3 virtual environment:
```bash
"C:\Python311\python.exe" -m venv venv_py3
```
3. Activate the Python 3 environment 
```bash
.\venv_py3\Scripts\activate
```

## Running the Project

### 1. Start the Python 2 Server

```bash
cd .\server\
python naoqi_server.py
```
The server will start and listen for commands from the Python 3 client.

### 2. Run the Python 3 Client
```bash
cd .\client\
python main.py
```


## Example Code
In ```client/main.py```, you can see an example of how to use the ```ALProxy``` class in Python 3, similar to the Python 2 syntax.
```python
# main.py (Python 3)
from naoqi3 import ALProxy

IP = "192.168.1.1"  # Replace with your robot's IP address
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hello, world!")
```

### Explanation of the Code
- ```ALProxy("ALTextToSpeech", IP, 9559)``` creates a proxy for the ```ALTextToSpeech``` module, using the same syntax as in Python 2.
- ```tts.say("Hello, world!")``` sends the ```say``` command to the Python 2 server, which executes it via NAOqi and makes the robot speak.


## Technical Details
### Server (Python 2):
Listens on a specified port for incoming commands from the client.
Deserializes the received command, executes it using NAOqi, and returns the result.
### Client (Python 3):
Provides ALProxy via naoqi3.py that mirrors the Python 2 NAOqi API.
Forwards all method calls to naoqi_client.py, which serializes and sends commands to the server.
### Communication Protocol:
The client and server communicate using sockets, with commands and responses serialized using pickle to handle complex data.
