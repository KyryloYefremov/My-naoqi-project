# NAOqi Python 2 to Python 3 Bridge

This project provides a Python 3-compatible wrapper for the NAOqi SDK, originally available only in Python 2. With this bridge, you can write code that communicates with NAO robots in Python 3, using the same syntax as NAOqi's original Python 2 library.

## Project Structure
```shell
project_root/
├── server/                         # Server-side code (Python 2)
│   ├── examples/                   # Directory with test programs
│   ├── config.py                   # Congifuration file: IP, PORT for Nao
│   ├── naoqi_server.py             # Server to execute NAOqi commands
│   ├── proxy_service.py            # File to cache proxies
│   ├── fetch_naoqi_constants.py    # Runable file to import all NAOqi constants
│
├── client/                         # Client-side code (Python 3)
│   ├── examples/                   # Directory with test programs
│   ├── naoqi3.py                   # Wrapper to emulate NAOqi in Python 3
│   ├── naoqi_client.py             # Client to communicate with Python 2 server
│   ├── config.py                   # Congifuration file: IP, PORT for Nao
│
└── README.md                       # Project documentation
```

## Compatibility
This table shows with which Nao and NAOqi SDK this bridge interface is compatible.
| Nao version | NAOqi SDK version | Compatible |
|-------------|-------------------|------------|
| Nao V4      | *NAOqi* 2.1.4     |     ✅     |
| Nao V5      | *NAOqi* 2.1.4     |     ✅     |
| Nao V6      | *NAOqi* 2.8.6+    |     ✅     |


## Main Components

- **server/naoqi_server.py** (Python 2): A server that listens for commands, executes them using the NAOqi SDK, and returns the results.
- **client/naoqi3.py** (Python 3): Provides an `ALProxy` class that emulates the NAOqi syntax, forwarding commands to `naoqi_client.py`.
- **client/naoqi_client.py** (Python 3): A client that communicates with the Python 2 server, handling command transmission and result retrieval.

## Instalation guide
**STEPS:**
1. Python 3.11.0 installation (or any other versions you would like)
2. Python 2.7.18 installation (required for NAOqi SDK)
3. NAOqi SDK instalation
4. Setup first project and install NAOqi3
5. Running first program

### Step 1: Install Python 3 (if not installed)
_This step is required if you don't have Python 3 installed on your system. If you already have Python 3, you can skip this step._

1. Go to [official Python website](https://www.python.org/downloads/release/python-3110/) to download Python 3.11.0.
2. Scroll to the very end of the page and you will see different installers.
3. Select installer based on your PC system architecture:
   - Windows installer (64-bit) if you have 64-bit system architecture
   - Windows installer (32-bit) if you have 32-bit system architecture
   <img width="1164" alt="python3110_install" src="https://github.com/user-attachments/assets/8c95ae13-5f94-43f9-9da9-ae56f0dd3338" />
   - In this tutorial the 64-bit version will be selected.
4. Click on it to start downloading.
5. After the installation is complete, open the installed file. You should see similar to this window:  
![00_install_python3110](https://github.com/user-attachments/assets/b19cb1f6-7f38-4c38-9593-5c4c9fec6590)  
6. Firstly, select "Add python.exe to PATH" and click "Customize installation"
![02_install_python3110](https://github.com/user-attachments/assets/d88f2c5e-d433-4acb-9f22-876d6f71f59e)  
7. Then check if first two optional features (checkboxes) are selected. Then click "Next"  
![03_install_python3110](https://github.com/user-attachments/assets/49dd439a-6f9c-47c5-83a3-23e8cb524cce)  
8. Select "Install Python for all users" (admin account is required) and check if all options from 2 to 5 are selected.  
Install location can be leaved as default. Click "Install".  
![04_install_python3110](https://github.com/user-attachments/assets/8e69f333-4737-408e-80d7-a378a85e32ce)  
10. Wait for installation to be finished.  
![05_install_python3110](https://github.com/user-attachments/assets/ae6a79be-38f7-408b-a522-b42016ef8f83)  
11. The close installation window.  
![06_install_python3110](https://github.com/user-attachments/assets/68cbd9b9-e73a-48b8-b626-debc1a78c30d)  
12. Check the installation:
   - open CMD console or Windows PowerShell
   - type: `python --version`
   - as an output you should see `Python 3.11.0`

**You have successfully installed Python 3 on your computer!**

### Step 2: Install Python 2.7.18 (required)

1. First, go to this [official link](https://www.python.org/downloads/release/python-2718/) to install exactly Python 2.7.18 32-bit edition.
2. Scroll down and click on this installer: **Windows x86 MSI installer**  
<img width="1168" alt="python2718_installer" src="https://github.com/user-attachments/assets/ecd1e243-e7e9-4e7b-bd51-5900a6602790" />  
3. After the installation is complete, open the installed file. You should see similar to this window.  
<img alt="01_install_python2718" src="https://github.com/user-attachments/assets/04c9ba70-1fef-4307-9388-d4b0027be4ed" />  <br>
4. Select the option: "Install for all users" and click "Next".  <br>
<img alt="02_install_python2718" src="https://github.com/user-attachments/assets/37049bbb-575e-4be4-9d81-a629019d3e89" />  <br>
5. Change installation location from `C:\Python27` to `C:\Program Files\Python27` and click "Next".  <br>
<img alt="03_install_python2718" src="https://github.com/user-attachments/assets/b1529642-6180-43f6-bbc3-70608a648c39" /> <br>
<img alt="04_install_python2718" src="https://github.com/user-attachments/assets/5434300f-f556-4adb-898f-e2e07d440cec" /> <br>
6. Here hust click "Next".  <br>
<img alt="05_install_python2718" src="https://github.com/user-attachments/assets/dafcde58-b57f-4b49-a85d-29db96f6b409" /> <br>
7. The installation should be started.  <br>
<img alt="06_install_python2718" src="https://github.com/user-attachments/assets/0e507d8f-9815-4797-8d22-dbaa3c64354d" /> <br>
8. Click "Finish" to exit the installation.  <br>
<img alt="07_install_python2718" src="https://github.com/user-attachments/assets/c0e9d248-f346-43a8-8469-6692eb6c79af" /> <br>

**You have successfully installed Python 2.7.18 on your computer!**

### Step 3: install NAOqi SDK 2.1.4 and add it to Python global dependencies (required)
1. Firstlly, install NAOqi SDK from this repository by clicking on this link [pynaoqi.rar](pynaoqi.rar) and clicking on an install icon. <br>
<img width="1096" alt="install_rar" src="https://github.com/user-attachments/assets/04311ba5-5ec0-421d-80df-892bb33b058a" />  <br>
2. After the installation is complete, extract the archive. After the extraction you should see a folder `📁 pynaoqi`.
3. Then copy entire folder `pynaoqi` and place it in folder with the path: `C:\Program Files\Python27\Lib\site-packages`.
4. Next click "Win" button on your keyboard and type "Edit the system environment variables". Then click "Enter".
5. You should see this window opened:  <br>
<img alt="01_install_naoqisdk" src="https://github.com/user-attachments/assets/3e94c685-60bc-4608-a2a1-9fbc92e2cd37" />  <br>
6. Then click on "Environment variables": <br>
<img alt="02_install_naoqisdk" src="https://github.com/user-attachments/assets/fd52181d-f165-407f-941c-9a0b18f1be9e" />  <br>
7. Click on "New": <br>
<img alt="03_install_naoqisdk" src="https://github.com/user-attachments/assets/2bde41f2-e9a5-4677-a6f3-d0eba2535f1f" />  <br>
8. Create new variable with name `PYTHONPATH` and value `your-path-to-python27\Lib\site-packages\pynaoqi\lib` and click "Ok": <br>
<img alt="04_install_naoqisdk" src="https://github.com/user-attachments/assets/10829a62-0cf5-4a16-82a6-39a6b425a835" />  <br>
9. Check if new variable was successfully added and click "Ok".  <br>
<img alt="05_install_naoqisdk" src="https://github.com/user-attachments/assets/9a07adbf-c9ea-4d42-977a-dd695da4cd70" />  <br>
10. Exit by clicking on "Ok".  <br>
<img alt="06_install_naoqisdk" src="https://github.com/user-attachments/assets/f8caa170-b60c-4ed5-8211-fdf3dbdcace5" />  <br>

**You have successfully installed and added NAOqi SDK to your Python 2.7.18 environment!**

### Step 4: Setup first project and install NAOqi3 (required)
_For this part you need to have a git system installed on your computer._ <br>
_Also you need to have a Python IDE installed on your computer (for example PyCharm)._ <br>

This part will describe how to create new project in PyCharm, clone NAOqi3 from this repository and setup all required settings.

1. Create a new PyCharm project.
2. Open ternimal and clone the NAOqi3 from this repository: `git clone https://github.com/KyryloYefremov/My-naoqi-project`.
3. Navigate to `.\My-naoqi-project\server` folder, then create a new virtual environment with Python 2.7.18 and activate it.
4. Open another terminal window, navigate to `.\My-naoqi-project\client` folder, then create a new virtual environment with Python 3.11.0 and activate it.
5. Then you will be having two terminals: one opened at `.\My-naoqi-project\server` folder with activated virtual env. for Python 2 and second opened at `.\My-naoqi-project\client` folder with activated virtual env. for Python 3.
6. To try to run a Python 3 program on NAOqi3, navigate to `.\My-naoqi-project\client\config.py` and uncommit or create NAO IP address and NAO port.
7. Then run `naoqi_server.py` in Python 2 terminal running this command: `python naiqi_server.py`.
8. After this you can try to run any Python 3 test example from folder `client\examples`. Try to run in Python 3 terminal for example: `python .\examples\core\test_say_hello.py`.

**❗️❗️❗️ Important information ❗️❗️❗️**

After successfully installing and launching NAOqi3, you can remove all `examples\` folders (both in `server\` and `client\`) or leave it for inspiration. All files you actually require are: `client\naoqi_client.py`, `client\fetch_naoqi_constants.py`, `client\config.py` (to have NAO configs stored), `client\naoqi3.py`, `server\naoqi_server.py`, `server\proxy_service.py`.

## Technical Details
### Server (Python 2):
Listens on a specified port for incoming commands from the client.
Deserializes the received command, executes it using NAOqi, and returns the result.
### Client (Python 3):
Provides ALProxy via naoqi3.py that mirrors the Python 2 NAOqi API.
Forwards all method calls to naoqi_client.py, which serializes and sends commands to the server.
### Communication Protocol:
The client and server communicate using sockets, with commands and responses serialized using pickle to handle complex data.
